#!/usr/bin/env python3
"""
币安广场热帖获取工具 - 散户讨论话题
"""
import json
import requests
import time
from datetime import datetime

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Origin": "https://www.bmwweb.cc",
    "Referer": "https://www.bmwweb.cc/zh-CN/square",
    "Bnc-Uuid": "2510c36b-606d-450c-ade3-4cde8745680b",
    "Clienttype": "web",
    "Versioncode": "web",
    "Cookie": "bnc-uid=2510c36b-606d-450c-ade3-4cde8745680b; lang=zh-CN"
}

BAN_KEYWORDS = ["官方", "交易所", "财经", "研究院", "机构", "认证", "Admin", "admin", "官方账号"]

def fetch_posts(page=1, size=50):
    url = "https://www.bmwweb.cc/bapi/composite/v9/friendly/pgc/feed/feed-recommend/list"
    payload = {"pageIndex": page, "pageSize": size, "scene": "web-homepage", "contentIds": []}
    try:
        r = requests.post(url, headers=HEADERS, json=payload, timeout=10)
        r.raise_for_status()
        d = r.json()
        return d.get("data", {}).get("vos", []) if d.get("success") else []
    except Exception as e:
        print(f"请求失败: {e}")
        return []

def is_retail_user(post):
    if post.get("authorVerificationType", 0) > 0: return False
    if post.get("authorRole", 0) != 0: return False
    name = post.get("authorName", "")
    for kw in BAN_KEYWORDS:
        if kw.lower() in name.lower(): return False
    return True

def is_recent(timestamp):
    return (int(time.time()) - timestamp) <= 12 * 3600

def fmt_time(ts):
    return datetime.fromtimestamp(ts).strftime("%m-%d %H:%M")

def main():
    print("=" * 95)
    print("【币安广场】12小时内散户讨论话题")
    print("=" * 95)
    
    posts = fetch_posts(1, 50)
    print(f"获取: {len(posts)} | ", end="")
    
    valid = [p for p in posts if is_recent(p.get("date", 0)) and is_retail_user(p)]
    valid.sort(key=lambda x: x.get("commentCount", 0), reverse=True)
    
    print(f"散户帖: {len(valid)} | 显示前15条\n")
    
    header = f"{'内容摘要':<55} | {'作者':<10} | {'时间':<8} | {'浏览':>7} | {'评论':>5}"
    print(header)
    print("-" * 95)
    
    for p in valid[:15]:
        content = p.get("content", "")[:52]
        author = p.get("authorName", "")[:9]
        t = fmt_time(p.get("date", 0))
        views = f"{p.get('viewCount', 0):,}"
        comments = p.get("commentCount", 0)
        print(f"{content:<55} | {author:<10} | {t:<8} | {views:>7} | {comments:>5}")
    
    print("\n说明: 已过滤大V、机构账号，只保留12小时内普通用户讨论")

if __name__ == "__main__":
    main()
