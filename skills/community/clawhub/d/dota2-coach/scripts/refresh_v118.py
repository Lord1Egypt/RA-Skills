#!/usr/bin/env python3
"""
v1.1.8 数据刷新专用脚本
- 用 curl 拉取（避免 urllib 403）
- 按顺序执行：heroStats 拉取 → market_share 计算 → 胜率百分位计算 → 分段胜率
- 自动备份原文件
"""
import json
import subprocess
import statistics
import os
import shutil
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HEROES_FILE = f'{SCRIPT_DIR}/heroes_db.json'
BACKUP_DIR = f'{SCRIPT_DIR}/../backup_v117_20260605'

def curl_json(url, timeout=30):
    """用 curl 拉取 JSON"""
    result = subprocess.run(
        ['curl', '-sL', url, '-H', 'User-Agent: Mozilla/5.0', '--max-time', str(timeout)],
        capture_output=True, text=True, timeout=timeout + 5
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise RuntimeError(f'curl 失败: {url}')
    return json.loads(result.stdout)

def step1_fetch_hero_stats():
    """Step 1: 拉取最新 heroStats，更新 heroes_db.json"""
    print('\n' + '='*60)
    print('Step 1: 拉取 OpenDota heroStats')
    print('='*60)
    
    data = curl_json('https://api.opendota.com/api/heroStats')
    print(f'  拉取到 {len(data)} 个英雄')
    
    with open(HEROES_FILE) as f:
        heroes = json.load(f)
    
    heroes_by_id = {h['id']: h for h in heroes}
    
    # 拉取的有 1-8_pick/win（8个段位），但原 db 只有 1-5
    # 所以我们额外加 6/7/8
    updated = 0
    for h in data:
        hid = h['id']
        if hid not in heroes_by_id:
            print(f'  [WARN] 拉取数据中 id={hid} ({h.get("localized_name")}) 不在本地 db，跳过')
            continue
        hero = heroes_by_id[hid]
        hero['pub_pick'] = h.get('pub_pick', hero.get('pub_pick', 0))
        hero['pub_win'] = h.get('pub_win', hero.get('pub_win', 0))
        hero['pro_pick'] = h.get('pro_pick', hero.get('pro_pick', 0))
        hero['pro_win'] = h.get('pro_win', hero.get('pro_win', 0))
        # 段位胜率
        for i in range(1, 9):
            hero[f'{i}_pick'] = h.get(f'{i}_pick', hero.get(f'{i}_pick', 0))
            hero[f'{i}_win'] = h.get(f'{i}_win', hero.get(f'{i}_win', 0))
        # 趋势
        hero['pub_pick_trend'] = h.get('pub_pick_trend', [])
        hero['pub_win_trend'] = h.get('pub_win_trend', [])
        updated += 1
    
    with open(HEROES_FILE, 'w') as f:
        json.dump(heroes, f, ensure_ascii=False, indent=2)
    print(f'  更新了 {updated} 个英雄的基础数据和趋势')

def step2_market_share():
    """Step 2: 计算市场占有率变化"""
    print('\n' + '='*60)
    print('Step 2: 计算 market_share_change')
    print('='*60)
    
    with open(HEROES_FILE) as f:
        heroes = json.load(f)
    
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
        share_older = sum(t[:3]) / 3 / (sum(weekly_totals[:3]) / 3) if sum(weekly_totals[:3]) > 0 else 0
        share_recent = sum(t[3:6]) / 3 / (sum(weekly_totals[3:6]) / 3) if sum(weekly_totals[3:6]) > 0 else 0
        if share_older > 0:
            hero['market_share_change'] = round((share_recent - share_older) / share_older * 100, 2)
        else:
            hero['market_share_change'] = 0
    
    with open(HEROES_FILE, 'w') as f:
        json.dump(heroes, f, ensure_ascii=False, indent=2)
    
    changes = [h['market_share_change'] for h in heroes if 'market_share_change' in h]
    if changes:
        std = statistics.stdev(changes)
        half_std = std / 2
        declining = sum(1 for c in changes if c < -half_std)
        rising = sum(1 for c in changes if c > half_std)
        print(f'  出场率变化标准差: {std:.2f}%, 阈值(半标准差): {half_std:.2f}%')
        print(f'  上升 > {half_std:.2f}%: {rising} 个')
        print(f'  下降 < -{half_std:.2f}%: {declining} 个')

def step3_hero_warnings():
    """Step 3: 计算 wr/wr_change/share/share_change + 百分位标记"""
    print('\n' + '='*60)
    print('Step 3: 计算胜率/胜率变化/出场率/出场率变化 + 百分位标记')
    print('='*60)
    
    with open(HEROES_FILE) as f:
        heroes = json.load(f)
    
    weekly_totals = [0]*6
    for h in heroes:
        t = h.get('pub_pick_trend', [])
        for i in range(min(6, len(t))):
            weekly_totals[i] += t[i]
    
    records = []
    for h in heroes:
        t = h.get('pub_pick_trend', [])
        w = h.get('pub_win_trend', [])
        if not t or not w or len(t) < 6:
            h['warn_wr'] = 'unknown'
            h['warn_wr_change'] = 'unknown'
            h['warn_share'] = 'unknown'
            h['warn_share_change'] = 'unknown'
            continue
        
        total_pick = sum(t[:6])
        total_win = sum(w[:6])
        wr = total_win / total_pick * 100 if total_pick > 0 else 0
        
        wr_old = sum(w[:3])/3 / (sum(t[:3])/3) * 100 if sum(t[:3]) > 0 else 0
        wr_new = sum(w[3:6])/3 / (sum(t[3:6])/3) * 100 if sum(t[3:6]) > 0 else 0
        wr_change = wr_new - wr_old
        
        share = sum(t[:6]) / sum(weekly_totals) * 100
        
        share_old = (sum(t[:3])/3) / (sum(weekly_totals[:3])/3) if sum(weekly_totals[:3]) > 0 else 0
        share_new = (sum(t[3:6])/3) / (sum(weekly_totals[3:6])/3) if sum(weekly_totals[3:6]) > 0 else 0
        share_change = (share_new - share_old) * 100
        
        h['wr'] = round(wr, 1)
        h['wr_change'] = round(wr_change, 1)
        h['share'] = round(share, 2)
        h['share_change'] = round(share_change, 2)
        
        records.append({
            'key': h.get('key', ''),
            'wr': wr,
            'wr_change': wr_change,
            'share': share,
            'share_change': share_change,
        })
    
    wr_vals = [r['wr'] for r in records]
    wr_chg_vals = [r['wr_change'] for r in records]
    sh_vals = [r['share'] for r in records]
    sh_chg_vals = [r['share_change'] for r in records]
    
    def percentile_flag(value, all_values, invert=False):
        n = len(all_values)
        if invert:
            rank = sum(1 for v in all_values if v <= value)
        else:
            rank = sum(1 for v in all_values if v > value)
        pct = rank / n
        if invert:
            if pct <= 0.1: return 'warn_bottom10'
            elif pct <= 0.2: return 'warn_bottom20'
            elif pct >= 0.9: return 'warn_top10'
            elif pct >= 0.8: return 'warn_top20'
        else:
            if pct <= 0.1: return 'warn_top10'
            elif pct <= 0.2: return 'warn_top20'
            elif pct >= 0.9: return 'warn_bottom10'
            elif pct >= 0.8: return 'warn_bottom20'
        return 'normal'
    
    for h in heroes:
        k = h.get('key', '')
        rec = next((r for r in records if r['key'] == k), None)
        if not rec:
            continue
        h['warn_wr'] = percentile_flag(rec['wr'], wr_vals, invert=True)
        h['warn_wr_change'] = percentile_flag(rec['wr_change'], wr_chg_vals, invert=False)
        h['warn_share'] = percentile_flag(rec['share'], sh_vals, invert=True)
        h['warn_share_change'] = percentile_flag(rec['share_change'], sh_chg_vals, invert=False)
    
    with open(HEROES_FILE, 'w') as f:
        json.dump(heroes, f, ensure_ascii=False, indent=2)
    
    for field in ['warn_wr', 'warn_wr_change', 'warn_share', 'warn_share_change']:
        cnt_b10 = sum(1 for h in heroes if h.get(field) == 'warn_bottom10')
        print(f'  {field}: 后10% {cnt_b10} 个')

def step4_bracket_wr():
    """Step 4: 拉取并计算分段胜率"""
    print('\n' + '='*60)
    print('Step 4: 拉取分段胜率（8个段位）')
    print('='*60)
    
    BRACKET_NAMES = {
        1: '先锋', 2: '卫士', 3: '中军', 4: '统帅',
        5: '传奇', 6: '万古流芳', 7: '超凡入圣', 8: '冠绝',
    }
    
    data = curl_json('https://api.opendota.com/api/heroStats')
    print(f'  拉取到 {len(data)} 个英雄')
    
    bracket_totals = {i: 0 for i in range(1, 9)}
    for entry in data:
        for i in range(1, 9):
            pick_key = f'{i}_pick'
            if pick_key in entry:
                bracket_totals[i] += entry[pick_key]
    
    with open(HEROES_FILE) as f:
        heroes = json.load(f)
    
    hero_by_key = {h['key']: h for h in heroes}
    
    updated = 0
    for entry in data:
        name = entry.get('name', '')
        key = name.replace('npc_dota_hero_', '')
        if key not in hero_by_key:
            continue
        bracket_data = {}
        for i in range(1, 9):
            pick_key = f'{i}_pick'
            win_key = f'{i}_win'
            if pick_key in entry and win_key in entry:
                picks = entry[pick_key]
                wins = entry[win_key]
                wr = round(wins / picks * 100, 1) if picks > 0 else 0
                share = round(picks / bracket_totals[i] * 100, 2) if bracket_totals[i] > 0 else 0
                bracket_data[BRACKET_NAMES[i]] = {'wr': wr, 'picks': picks, 'share': share}
        hero_by_key[key]['bracket_wr'] = bracket_data
        updated += 1
    
    with open(HEROES_FILE, 'w') as f:
        json.dump(heroes, f, ensure_ascii=False, indent=2)
    print(f'  更新了 {updated} 个英雄的分段胜率')

def main():
    print(f'开始时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    
    # 备份
    if os.path.exists(BACKUP_DIR) and os.path.isdir(BACKUP_DIR):
        print(f'备份目录已存在: {BACKUP_DIR}')
    else:
        os.makedirs(BACKUP_DIR, exist_ok=True)
        shutil.copy2(HEROES_FILE, f'{BACKUP_DIR}/heroes_db.json')
        print(f'已备份到: {BACKUP_DIR}/heroes_db.json')
    
    step1_fetch_hero_stats()
    step2_market_share()
    step3_hero_warnings()
    step4_bracket_wr()
    
    print(f'\n{"="*60}')
    print(f'完成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'{"="*60}')

if __name__ == '__main__':
    main()
