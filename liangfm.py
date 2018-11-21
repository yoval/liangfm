# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 03:52:14 2018

@author: fuwen
"""

import requests,json

BookID = 45
Page = 24


def get_download(MainUrl):
    s= requests.Session()
    MainResponse = s.get(MainUrl)
    MainResponse.encoding = 'utf-8'
    MainHtml = MainResponse.text
    url = 'http://liangfm.com/index.php?c=music&m=item'
    Response = s.get(url)
    Response.encoding = 'utf-8'
    html = Response.text
    html = html.encode('utf-8').decode('unicode_escape')
    song_jsons = json.loads(html)
    return song_jsons

def aria2c_download(name,DownloadUrl):
    cmd = 'aria2c -o '+name + ' ' + DownloadUrl + '\n'
    with open('download.bat','a') as f:
        f.write(cmd)
        
def ChangeFileName(filename):
    filename = filename.replace('\\','')
    filename = filename.replace('/','')
    filename = filename.replace('：','')
    filename = filename.replace('*','')
    filename = filename.replace('“','')
    filename = filename.replace('<','')
    filename = filename.replace('>','')
    filename = filename.replace('|','')
    filename = filename.replace('?','？')
    filename = filename.replace(' ','')
    filename = filename.replace('.','')
    return filename

No = 0
for page in range(Page+1)[1:]:
    MainUrl = 'http://liangfm.com/index.php?c=music&m=vols&id=%d&page=%d'%(BookID,page)
    song_jsons = get_download(MainUrl)
    for song_json in song_jsons :
        No+=1
        song_name = song_json['song_name']
        song_name = ChangeFileName(song_name)
        song_path = song_json['song_path']
        dot = song_path.split('.')
        dot = dot[len(dot)-1]
        Name = song_name + '.' + dot
        Name = str(No).zfill(3) + Name
        aria2c_download(Name,song_path)