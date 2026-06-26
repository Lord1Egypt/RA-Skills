#!/usr/bin/env python3
"""
检查奖池并通知用户
"""
import requests
import json
import os
import sys

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
    
    if not pools:
        print("NO_TASKS")
        sys.exit(0)
    
    print(f"FOUND {len(pools)} TASK(S):")
    for p in pools:
        print(f"赞助方: {p.get('sponsor')}")
        print(f"奖金: {p.get('price')}")
        print(f"分销方式: {p.get('distribution')}")
        print(f"平台: {p.get('platform')}")
        print(f"开始: {p.get('activityStart')}")
        print(f"截止: {p.get('activityEnd')}")
        print(f"简介: {p.get('brief')}")
        pool_id = p.get('id')
        loudy_link = f"https://loudy.ai?poolId={pool_id}"
        print(f"链接: {loudy_link}")
        print(f"---")

if __name__ == "__main__":
    main()
