#!/usr/bin/env python3
"""追踪媳妇智投Pro在ClawHub上的下载量和星标数据"""
import json
import os
import re
from datetime import datetime
from urllib.request import urlopen, Request

SKILL_URL = "https://clawhub.ai/xgs-520/ai-xifu-caopan-public"
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config")
LOG_FILE = os.path.join(LOG_DIR, "clawhub_stats.json")

def fetch_page(url):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8")

def parse_stats(html):
    """从页面HTML中提取下载量和星标"""
    downloads = None
    stars = None
    
    # 匹配 Downloads: 数字 (页面中显示为 "Downloads\n271" 这种)
    m = re.search(r'Downloads[^0-9]*(\d[\d,.]*[KMk]?)', html)
    if m:
        downloads = m.group(1).strip()
    
    # 匹配星标 (Unstar 1 / Star 0)
    m = re.search(r'(?:Unstar|Star)\s+(\d+)', html)
    if m:
        stars = int(m.group(1))
    
    return downloads, stars

def main():
    try:
        html = fetch_page(SKILL_URL)
        downloads, stars = parse_stats(html)
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = {
            "timestamp": now,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M"),
            "downloads": downloads,
            "stars": stars
        }
        
        # 读取历史数据
        history = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                try:
                    history = json.load(f)
                except json.JSONDecodeError:
                    history = []
        
        # 避免同一分钟内重复记录
        if history and history[-1].get("timestamp") == record["timestamp"]:
            print(f"[SKIP] 同一分钟已记录，跳过")
        else:
            history.append(record)
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        
        print(f"[OK] {now} | 下载量: {downloads or 'N/A'} | 星标: {stars or 'N/A'}")
        
        # 对比上次记录
        if len(history) >= 2:
            prev = history[-2]
            curr = history[-1]
            if prev.get("downloads") and curr.get("downloads"):
                try:
                    diff = int(str(curr["downloads"]).replace(",","")) - int(str(prev["downloads"]).replace(",",""))
                    if diff > 0:
                        print(f"[增长] 期间新增下载: {diff}")
                except (ValueError, TypeError):
                    pass
        
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()
