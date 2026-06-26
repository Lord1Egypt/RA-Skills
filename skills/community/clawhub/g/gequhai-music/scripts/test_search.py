# -*- coding: utf-8 -*-
import requests

BASE_URL = "https://www.gequhai.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

# 测试访问主页
print("测试访问歌曲海...")
try:
    resp = requests.get(BASE_URL, headers=HEADERS, timeout=15)
    print(f"状态码: {resp.status_code}")
    print(f"内容长度: {len(resp.text)}")
except Exception as e:
    print(f"访问失败: {e}")

# 测试热门歌曲页面
print("\n测试访问热门歌曲页面...")
try:
    resp = requests.get(f"{BASE_URL}/hot-music/", headers=HEADERS, timeout=15)
    print(f"状态码: {resp.status_code}")
    print(f"内容长度: {len(resp.text)}")
except Exception as e:
    print(f"访问失败: {e}")

# 测试新歌榜
print("\n测试访问新歌榜...")
try:
    resp = requests.get(f"{BASE_URL}/top/new", headers=HEADERS, timeout=15)
    print(f"状态码: {resp.status_code}")
    print(f"内容长度: {len(resp.text)}")
except Exception as e:
    print(f"访问失败: {e}")
