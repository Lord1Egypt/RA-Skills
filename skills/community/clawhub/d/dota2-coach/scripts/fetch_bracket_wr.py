#!/usr/bin/env python3
"""
从 OpenDota heroStats API 拉取分段胜率+选择率
并入 heroes_db.json

分段选择率 = 该英雄在该分段的pick / 该分段所有英雄总pick

分段映射（中国服）：
  1: 先锋 / 2: 卫士 / 3: 中军 / 4: 统帅
  5: 传奇 / 6: 万古流芳 / 7: 超凡入圣 / 8: 冠绝

用法: python3 fetch_bracket_wr.py
"""
import json, urllib.request

SCRIPT_DIR = '/root/.openclaw/workspace/magi/skills/dota2-coach/scripts'
HEROES_FILE = f'{SCRIPT_DIR}/heroes_db.json'

BRACKET_NAMES = {
    1: '先锋', 2: '卫士', 3: '中军', 4: '统帅',
    5: '传奇', 6: '万古流芳', 7: '超凡入圣', 8: '冠绝',
}

url = 'https://api.opendota.com/api/heroStats'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=30) as r:
    data = json.loads(r.read())

# 先算各分段的总pick（所有英雄pick之和）
bracket_totals = {i: 0 for i in range(1, 8)}
for entry in data:
    for i in range(1, 8):
        pick_key = f'{i}_pick'
        if pick_key in entry:
            bracket_totals[i] += entry[pick_key]

with open(HEROES_FILE) as f:
    heroes = json.load(f)

hero_by_key = {h['key']: h for h in heroes}

for entry in data:
    name = entry.get('name', '')
    key = name.replace('npc_dota_hero_', '')
    
    if key not in hero_by_key:
        continue
    
    bracket_data = {}
    for i in range(1, 8):
        pick_key = f'{i}_pick'
        win_key = f'{i}_win'
        if pick_key in entry and win_key in entry:
            picks = entry[pick_key]
            wins = entry[win_key]
            wr = round(wins / picks * 100, 1) if picks > 0 else 0
            share = round(picks / bracket_totals[i] * 100, 2) if bracket_totals[i] > 0 else 0
            bracket_data[BRACKET_NAMES[i]] = {'wr': wr, 'picks': picks, 'share': share}
    
    hero_by_key[key]['bracket_wr'] = bracket_data

with open(HEROES_FILE, 'w') as f:
    json.dump(heroes, f, ensure_ascii=False, indent=2)

with open(HEROES_FILE) as f:
    heroes = json.load(f)
antimage = next(h for h in heroes if h['key'] == 'antimage')
zhongjun = antimage['bracket_wr']['中军']
print(f"antimage 中军: wr={zhongjun['wr']}%, picks={zhongjun['picks']}, share={zhongjun['share']}%")
print(f"Total heroes: {len([h for h in heroes if 'bracket_wr' in h])}")
