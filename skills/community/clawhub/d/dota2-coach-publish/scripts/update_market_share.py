#!/usr/bin/env python3
"""
更新英雄数据库 + 计算市场占有率变化
每次运行自动计算出场率变化并更新 heroes_db.json
用法: python3 fetch_hero.py --update
"""
import json, subprocess, os, statistics

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HEROES_FILE = f'{SCRIPT_DIR}/heroes_db.json'

def fetch_hero_stats():
    result = subprocess.run(
        ['curl', '-sL', 'https://api.opendota.com/api/heroStats', '-H', 'User-Agent: Mozilla/5.0'],
        capture_output=True, text=True, timeout=20
    )
    return json.loads(result.stdout) if result.returncode == 0 else None

def update_trends_and_market_share():
    """从 OpenDota 拉数据，更新 heroes_db.json 的趋势字段和市场占有率变化"""
    data = fetch_hero_stats()
    if not data:
        print('[ERROR] 无法获取英雄数据')
        return False

    with open(HEROES_FILE) as f:
        heroes = json.load(f)

    heroes_by_id = {h['id']: h for h in heroes}

    # Update trend fields
    for h in data:
        hid = h['id']
        if hid in heroes_by_id:
            hero = heroes_by_id[hid]
            hero['pub_pick_trend'] = h.get('pub_pick_trend', [])
            hero['pub_win_trend'] = h.get('pub_win_trend', [])

    # Calculate market share changes
    num_weeks = 6
    weekly_totals = [0] * num_weeks
    for hero in heroes:
        t = hero.get('pub_pick_trend', [])
        for i in range(min(num_weeks, len(t))):
            weekly_totals[i] += t[i]

    for hero in heroes:
        t = hero.get('pub_pick_trend', [])
        if len(t) < 6:
            hero['market_share_change'] = 0
            continue
        share_older = sum(t[:3]) / 3 / (sum(weekly_totals[:3]) / 3)
        share_recent = sum(t[3:6]) / 3 / (sum(weekly_totals[3:6]) / 3)
        if share_older > 0:
            hero['market_share_change'] = round((share_recent - share_older) / share_older * 100, 2)
        else:
            hero['market_share_change'] = 0

    with open(HEROES_FILE, 'w') as f:
        json.dump(heroes, f, ensure_ascii=False, indent=2)

    # Summary
    changes = [h['market_share_change'] for h in heroes if 'market_share_change' in h]
    if changes:
        half_std = statistics.stdev(changes) / 2
        declining = sum(1 for c in changes if c < -half_std)
        rising = sum(1 for c in changes if c > half_std)
        print(f'[更新完成] {len(heroes)} 个英雄')
        print(f'  出场率变化标准差: {statistics.stdev(changes):.2f}%，阈值(半标准差): {half_std:.2f}%')
        print(f'  上升 > {half_std:.2f}%: {rising} 个')
        print(f'  下降 < -{half_std:.2f}%: {declining} 个')

    return True

if __name__ == '__main__':
    update_trends_and_market_share()
