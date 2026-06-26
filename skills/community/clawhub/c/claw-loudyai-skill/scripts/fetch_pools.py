#!/usr/bin/env python3
"""
获取进行中的奖池列表
"""
import requests
import json
import os

API_BASE = "https://api.loudy.ai/app-api/open-api/v1"
LOUDY_API_KEY = os.environ.get("LOUDY_API_KEY", "")

def fetch_earning_pools():
    """获取进行中的奖池列表"""
    url = f"{API_BASE}/earning-pools"
    headers = {
        "X-API-Key": LOUDY_API_KEY,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    response = requests.get(url, headers=headers)
    data = response.json()
    if data.get("code") != 0 and data.get("code") != 200:
        print(f"Error: {data.get('msg')}")
        return []
    
    pools = data.get("data", [])
    # 过滤进行中的奖池
    ongoing_pools = [p for p in pools if p.get("status") == "Ongoing"]
    
    return ongoing_pools

def main():
    pools = fetch_earning_pools()
    print(json.dumps(pools, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
