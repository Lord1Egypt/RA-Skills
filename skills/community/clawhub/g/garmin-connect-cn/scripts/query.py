#!/usr/bin/env python3
"""
Garmin Connect 数据查询
用法: python3 query.py <jwt_token> [日期 YYYY-MM-DD]
"""
import sys
import json
import requests
from datetime import datetime

API_BASE = "https://connect.garmin.cn"

def query_garmin(jwt, date=None):
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    
    headers = {
        'Authorization': f'Bearer {jwt}',
        'nk': 'NT',
        'Accept': 'application/json'
    }
    
    sess = requests.Session()
    sess.headers.update(headers)
    
    # 用户信息
    r = sess.get(f'{API_BASE}/userprofile-service/userprofile/user-settings')
    user = r.json() if r.status_code == 200 else {}
    
    print(f"👤 {user.get('displayName', 'N/A')} ({user.get('email', 'N/A')})")
    print(f"📅 查询日期: {date}")
    print("-" * 40)
    
    # 每日摘要
    r2 = sess.get(f'{API_BASE}/daily-summary-api/summary/daily/{date}')
    if r2.status_code == 200:
        d = r2.json()
        steps = d.get('totalSteps', 0)
        dist = d.get('totalDistance', 0) / 1000
        cal = d.get('activeKilocalories', 0)
        floors = d.get('totalFloorsAscended', 0)
        print(f"  �步行    {steps:>8,} 步")
        print(f"  📏 距离  {dist:>8.1f} km")
        print(f"  🔥 卡路里 {cal:>7,} kcal")
        print(f"  🏢 爬楼   {floors:>7} 层")
    else:
        print(f"  ⚠️  每日摘要获取失败 ({r2.status_code})")
    
    # 心率
    r3 = sess.get(f'{API_BASE}/usersummaryservice/api/summary/{user.get("userId","116181268")}/daily/{date}')
    if r3.status_code == 200:
        d = r3.json()
        hr = d.get('restingHeartRate', d.get('averageRestingHeartRate', 'N/A'))
        print(f"  ❤️ 静息心率 {hr}")
    print()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: query.py <jwt_token> [日期 YYYY-MM-DD]")
        sys.exit(1)
    
    jwt = sys.argv[1]
    date = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        query_garmin(jwt, date)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)
