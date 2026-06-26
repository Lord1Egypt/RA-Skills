#!/usr/bin/env python3
# Channel Follow-up Check Script
# 每日跟进检查脚本

import json
from datetime import datetime, timedelta

def check_followups(channels):
    """检查今日待跟进渠道"""
    today = datetime.now()
    followups = []
    
    for channel in channels:
        last_followup = datetime.fromisoformat(channel['last_followup'])
        days_since = (today - last_followup).days
        
        if days_since >= channel['followup_interval']:
            followups.append({
                'name': channel['name'],
                'score': channel['score'],
                'days_since': days_since,
                'template': 'A' if channel['score'] >= 80 else 'B'
            })
    
    return sorted(followups, key=lambda x: x['score'], reverse=True)

if __name__ == '__main__':
    # 示例数据
    channels = [
        {'name': 'Tech With Tim', 'score': 83, 'last_followup': '2026-03-22', 'followup_interval': 2},
        {'name': 'Sabrina', 'score': 83, 'last_followup': '2026-03-23', 'followup_interval': 2},
        {'name': 'Florian', 'score': 82, 'last_followup': '2026-03-21', 'followup_interval': 3}
    ]
    
    followups = check_followups(channels)
    print(f"今日待跟进 ({len(followups)}个):")
    for f in followups:
        print(f"  - {f['name']}: {f['score']}分，{f['days_since']}天前，模板{f['template']}")
