#!/usr/bin/env python3
"""
最近活动记录查询
用法: python3 activities.py <jwt_token> [userId] [limit]
"""
import sys
import requests
from datetime import datetime

API_BASE = "https://connect.garmin.cn"

def get_activities(jwt, user_id="116181268", limit=10):
    headers = {
        'Authorization': f'Bearer {jwt}',
        'nk': 'NT',
        'Accept': 'application/json'
    }
    sess = requests.Session()
    sess.headers.update(headers)
    
    r = sess.get(
        f'{API_BASE}/activitylist-service/activities/{user_id}',
        params={'limit': limit, 'start': 0}
    )
    
    if r.status_code != 200:
        print(f"获取失败: {r.status_code}")
        return
    
    acts = r.json()
    if not isinstance(acts, list):
        acts = []
    
    print(f"🏃 最近 {len(acts)} 条活动记录:")
    print("-" * 50)
    for a in acts:
        t = a.get('startTimeLocal', '')[:10]
        sport = a.get('activityType', {}).get('typeKey', 'N/A')
        dist = round(a.get('distance', 0) / 1000, 1)
        dur = a.get('duration', 0)
        hm = f"{int(dur//3600)}h{int(dur%3600//60)}m" if dur else 'N/A'
        cal = a.get('activeKilocalories', 0)
        print(f"  {t}  {sport:<15} {dist:>5}km  {hm:<8}  {cal:>5}kcal")

if __name__ == '__main__':
    jwt = sys.argv[1] if len(sys.argv) > 1 else None
    if not jwt:
        print("用法: activities.py <jwt_token> [userId] [limit]")
        sys.exit(1)
    user_id = sys.argv[2] if len(sys.argv) > 2 else "116181268"
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    get_activities(jwt, user_id, limit)
