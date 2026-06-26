# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import sys
import base64
from pathlib import Path

BASE_URL = "https://www.gequhai.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

SESSION = requests.Session()

def search_songs(keyword):
    """搜索歌曲"""
    url = f"{BASE_URL}/s/{keyword}"
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

def decode_modified_base64(encoded):
    """解码base64"""
    try:
        modified = encoded.replace("#", "H").replace("%", "S")
        decoded = base64.b64decode(modified).decode("utf-8")
        return decoded
    except:
        return None

def get_download_url(song_id):
    """获取下载链接"""
    url = f"{BASE_URL}/play/{song_id}"
    
    # 先访问播放页面
    resp = SESSION.get(url, headers=HEADERS, timeout=15)
    resp.encoding = "utf-8"
    
    result = {"id": song_id}
    
    # 提取标题和歌手
    match = __import__("re").search(r"window\.mp3_title\s*=\s*['\"]([^'\"]+)['\"]", resp.text)
    if match:
        result["title"] = match.group(1)
    
    match = __import__("re").search(r"window\.mp3_author\s*=\s*['\"]([^'\"]+)['\"]", resp.text)
    if match:
        result["artist"] = match.group(1)
    
    match = __import__("re").search(r"window\.play_id\s*=\s*['\"]([^'\"]+)['\"]", resp.text)
    if match:
        result["play_id"] = match.group(1)
    
    match = __import__("re").search(r"window\.mp3_type\s*=\s*(\d+)", resp.text)
    if match:
        result["type"] = int(match.group(1))
    
    # 提取高品质链接
    match = __import__("re").search(r"window\.mp3_extra_url\s*=\s*['\"]([^'\"]+)['\"]", resp.text)
    if match:
        extra_url = match.group(1)
        if extra_url:
            decoded = decode_modified_base64(extra_url)
            if decoded:
                if any(ext in decoded.lower() for ext in [".mp3", ".flac", ".m4a"]):
                    result["download_url_hq"] = decoded
                else:
                    result["netdisk_url"] = decoded
    
    # 通过API获取标准链接
    if result.get("play_id"):
        api_url = f"{BASE_URL}/api/music"
        api_headers = {
            **HEADERS,
            "X-Requested-With": "XMLHttpRequest",
            "X-Custom-Header": "SecretKey",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": BASE_URL,
            "Referer": f"{BASE_URL}/play/{song_id}",
        }
        
        try:
            api_resp = SESSION.post(
                api_url,
                headers=api_headers,
                data={"id": result["play_id"], "type": result.get("type", 0)},
                timeout=10
            )
            data = api_resp.json()
            if data.get("code") == 200:
                result["url"] = data["data"]["url"]
        except Exception as e:
            result["api_error"] = str(e)
    
    return result

# 搜索歌曲
keyword = "梦底"
print(f"搜索: {keyword}")
songs = search_songs(keyword)
print(f"找到 {len(songs)} 首歌曲")

if songs:
    # 获取第一首歌
    first = songs[0]
    print(f"下载: {first['title']} - {first['artist']}")
    
    # 获取下载链接
    detail = get_download_url(first["id"])
    
    output = {
        "search": songs[:5],
        "download_info": detail
    }
    
    # 保存结果
    with open(r"C:\Users\an\.openclaw\workspace\skills\gequhai-music\data\download_info.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print("OK")
else:
    print("未找到歌曲")
