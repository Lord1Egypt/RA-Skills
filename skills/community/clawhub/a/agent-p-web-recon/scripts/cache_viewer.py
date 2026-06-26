#!/usr/bin/env python3
"""
缓存/快照查看器
用法：python cache_viewer.py <url> [--wayback|--google|--archive]
"""

import sys
import webbrowser
import requests
import json
from datetime import datetime

def get_wayback_snapshots(url):
    """获取 Wayback Machine 历史快照"""
    cdx_url = f"http://web.archive.org/cdx/search/cdx?url={url}&output=json&limit=20"
    try:
        resp = requests.get(cdx_url, timeout=10)
        data = resp.json()
        if len(data) <= 1:
            print("未找到历史快照")
            return []
        
        print(f"\n📦 Wayback Machine - 找到 {len(data)-1} 个快照:\n")
        snapshots = []
        for row in data[1:]:  # 跳过表头
            timestamp = row[1]
            original = row[2]
            status = row[4]
            archive_url = f"https://web.archive.org/web/{timestamp}/{original}"
            snapshots.append({
                'time': timestamp,
                'url': original,
                'status': status,
                'archive_url': archive_url
            })
            print(f"  [{timestamp}] {status} - {archive_url}")
        
        return snapshots
    except Exception as e:
        print(f"错误：{e}")
        return []

def get_google_cache_url(url):
    """生成 Google Cache 链接"""
    return f"https://webcache.googleusercontent.com/search?q=cache:{url}"

def check_live_status(url):
    """检查当前页面状态"""
    try:
        resp = requests.head(url, timeout=10, allow_redirects=True)
        return resp.status_code
    except:
        return None

def main():
    if len(sys.argv) < 2:
        print("用法：python cache_viewer.py <url> [--wayback|--google|--archive]")
        print("  --wayback   打开 Wayback Machine")
        print("  --google    打开 Google Cache")
        print("  --archive   打开 Archive.org")
        sys.exit(1)
    
    url = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "--wayback"
    
    print(f"🔍 目标：{url}")
    
    # 检查当前状态
    status = check_live_status(url)
    if status:
        print(f"当前状态：HTTP {status}")
    else:
        print("当前状态：无法访问")
    
    if mode == "--wayback":
        snapshots = get_wayback_snapshots(url)
        if snapshots:
            print(f"\n🌐 最新快照：{snapshots[0]['archive_url']}")
            print("在浏览器中打开？(y/n)")
            if input().lower() == 'y':
                webbrowser.open(snapshots[0]['archive_url'])
    
    elif mode == "--google":
        cache_url = get_google_cache_url(url)
        print(f"\n🔎 Google Cache: {cache_url}")
        print("在浏览器中打开？(y/n)")
        if input().lower() == 'y':
            webbrowser.open(cache_url)
    
    elif mode == "--archive":
        archive_url = f"https://web.archive.org/web/*/{url}"
        print(f"\n📚 Archive.org: {archive_url}")
        print("在浏览器中打开？(y/n)")
        if input().lower() == 'y':
            webbrowser.open(archive_url)
    
    else:
        print("未知模式，使用 --wayback")
        get_wayback_snapshots(url)

if __name__ == "__main__":
    main()
