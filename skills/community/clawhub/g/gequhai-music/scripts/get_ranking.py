# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

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
            # 排名
            rank = tds[0].get_text(strip=True)
            
            # 歌曲名和链接
            link = tds[1].select_one("a")
            title = link.get_text(strip=True) if link else ""
            href = link.get("href", "") if link else ""
            song_id = href.split("/")[-1] if href else None
            
            # 歌手
            artist = tds[2].get_text(strip=True) if len(tds) > 2 else ""
            
            songs.append({
                "rank": rank,
                "id": song_id,
                "title": title,
                "artist": artist,
            })
    
    return songs

# 获取新歌榜
print("=== 新歌榜 ===")
try:
    resp = requests.get(f"{BASE_URL}/top/new", headers=HEADERS, timeout=15)
    resp.encoding = "utf-8"
    songs = parse_song_list(resp.text)
    for s in songs[:15]:
        print(f"{s['rank']}. {s['title']} - {s['artist']}")
except Exception as e:
    print(f"获取失败: {e}")

# 获取飙升榜
print("\n=== 飙升榜 ===")
try:
    resp = requests.get(f"{BASE_URL}/top/surge", headers=HEADERS, timeout=15)
    resp.encoding = "utf-8"
    songs = parse_song_list(resp.text)
    for s in songs[:15]:
        print(f"{s['rank']}. {s['title']} - {s['artist']}")
except Exception as e:
    print(f"获取失败: {e}")

# 获取抖音榜
print("\n=== 抖音榜 ===")
try:
    resp = requests.get(f"{BASE_URL}/top/douyin", headers=HEADERS, timeout=15)
    resp.encoding = "utf-8"
    songs = parse_song_list(resp.text)
    for s in songs[:15]:
        print(f"{s['rank']}. {s['title']} - {s['artist']}")
except Exception as e:
    print(f"获取失败: {e}")
