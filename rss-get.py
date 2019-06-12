#!/usr/bin/env python

import sqlite3
import requests
from bs4 import BeautifulSoup

url = 'https://www.lowyat.net/feed/'
http_proxy = "http://10.47.20.248:8080"
https_proxy = "http://10.47.20.248:8080"
ftp_proxy = "http://10.47.20.248:8080"
user_agent = "firefox"
db_file = "rss-get.db3"
data_file = 'rss_record.db'

# You can set proxy also on OS environment:

# On linux you can also do this via the HTTP_PROXY, HTTPS_PROXY, 
# and FTP_PROXY environment variables:

# export HTTP_PROXY=10.10.1.10:3128
# export HTTPS_PROXY=10.10.1.11:1080
# export FTP_PROXY=10.10.1.10:3128

# On Windows:

# set http_proxy=10.10.1.10:3128
# set https_proxy=10.10.1.11:1080
# set ftp_proxy=10.10.1.10:3128

proxy = { 
    "http":  http_proxy, 
    "https": https_proxy, 
    "ftp":   ftp_proxy
    }

agent_string = {
    "firefox": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
    "chrome":  "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "edge":    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
    "ie":      "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko"
}

headers = {
    "User-Agent": agent_string[user_agent]
    #"From": "email@example.com"
}

download_list = {}

page = requests.get(url, headers=headers, proxies=proxy)
#print (page.status_code)
#print (page.text)
#soup = BeautifulSoup(page.text, 'lxml-xml')
#print(soup.prettify())

soup = BeautifulSoup(page.text, 'lxml-xml')
items = soup.find_all('item')

try:
    conn = sqlite3.connect(db_file)
except sqlite3.OperationalError as e:
    print(e)

c = conn.cursor()

for item in items:
    postid = item.find('post-id').text
    title = item.find('title').text
    link = item.find('link').text
    pubdate = item.find('pubDate').text
    record = 'INSERT INTO feed_record VALUES (' + postid + ', "' + pubdate + '", "' + title + '", "' + link + '", 0)'

    try:
        c.execute(record)
        download_list[postid] = link
        print('ADDED: ' + postid + ' | ' + pubdate + ' | ' + title)
    except sqlite3.IntegrityError as errmsg:
        if str(errmsg) == "UNIQUE constraint failed: feed_record.postid":
            print('SKIPPED: ' + postid + ' | ' + pubdate + ' | ' + title)
        else:
            raise

conn.commit()

#for itemid, itemlink in download_list.items():
#    itempage = requests.get(itemlink)
#    if itemoage.status_code == 200:


print(download_list)
