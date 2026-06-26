# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://www.gequhai.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

def parse_song_list(html):
    """解析歌曲列表"""
    soup = BeautifulSoup(html, "html.parser")
    songs = []
    
    for tr in soup.select("table tbody tr"):
        tds = tr.select("td")
        if len(tds) >= 2:
            rank = tds[0].get_text(strip=True)
            link = tds[1].select_one("a")
            title = link.get_text(strip=True) if link else ""
            href = link.get("href", "") if link else ""
            song_id = href.split("/")[-1] if href else None
            artist = tds[2].get_text(strip=True) if len(tds) > 2 else ""
            
            songs.append({
                "rank": rank,
                "id": song_id,
                "title": title,
                "artist": artist,
            })
    
    return songs

result = {}

# 获取新歌榜
try:
    resp = requests.get(f"{BASE_URL}/top/new", headers=HEADERS, timeout=15)
    resp.encoding = "utf-8"
    result["new"] = parse_song_list(resp.text)
except Exception as e:
    result["new_error"] = str(e)

# 获取飙升榜
try:
    resp = requests.get(f"{BASE_URL}/top/surge", headers=HEADERS, timeout=15)
    resp.encoding = "utf-8"
    result["surge"] = parse_song_list(resp.text)
except Exception as e:
    result["surge_error"] = str(e)

# 获取抖音榜
try:
    resp = requests.get(f"{BASE_URL}/top/douyin", headers=HEADERS, timeout=15)
    resp.encoding = "utf-8"
    result["douyin"] = parse_song_list(resp.text)
except Exception as e:
    result["douyin_error"] = str(e)

# 输出JSON
print(json.dumps(result, ensure_ascii=False, indent=2))
