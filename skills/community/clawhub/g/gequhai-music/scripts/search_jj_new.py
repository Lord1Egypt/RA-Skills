# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://www.gequhai.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

def search_songs(keyword, page=1):
    url = f"{BASE_URL}/s/{keyword}"
    if page > 1:
        url = f"{BASE_URL}/s/{keyword}/{page}"
    
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.encoding = "utf-8"
    
    soup = BeautifulSoup(resp.text, "html.parser")
    songs = []
    
    for tr in soup.select("table tbody tr"):
        tds = tr.select("td")
        if len(tds) >= 3:
            link = tds[1].select_one("a")
            if link:
                href = link.get("href", "")
                song_id = href.split("/")[-1] if href else None
                songs.append({
                    "id": song_id,
                    "title": link.get_text(strip=True),
                    "artist": tds[2].get_text(strip=True),
                })
    
    return songs

# 搜索林俊杰新歌
songs = search_songs("我对缘分小心翼翼")
output = {"keyword": "我对缘分小心翼翼", "total": len(songs), "songs": songs}

with open(r"C:\Users\an\.openclaw\workspace\skills\gequhai-music\data\jj_new_song.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"找到 {len(songs)} 首歌曲")
