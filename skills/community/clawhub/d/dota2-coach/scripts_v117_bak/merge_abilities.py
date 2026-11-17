#!/usr/bin/env python3
"""
从 dotabase abilities.json 提取更丰富的技能数据
保持与原有 abilities_db.json 相同的 hero_key 结构

用法: python3 merge_abilities.py
"""
import json

DOTABASE_FILE = '/tmp/dotabase_abilities.json'
OUTPUT_FILE = '/root/.openclaw/workspace/magi/skills/dota2-coach/scripts/abilities_db.json'
HEROES_FILE = '/root/.openclaw/workspace/magi/skills/dota2-coach/scripts/heroes_db.json'

# 加载英雄映射
with open(HEROES_FILE) as f:
    heroes = json.load(f)
hero_id_to_key = {h['id']: h['key'] for h in heroes}

# 加载旧的天赋数据（因为 dotabase 的 talents 没文字描述）
with open(OUTPUT_FILE) as f:
    old_db = json.load(f)
old_talents_map = {h['hero_key']: h['talents'] for h in old_db}

# 加载 dotabase abilities
with open(DOTABASE_FILE) as f:
    dotabase = json.load(f)

# 按 hero_id 分组
hero_abilities = {}
for ab in dotabase:
    hid = ab.get('hero_id')
    if not hid:
        continue
    key = hero_id_to_key.get(hid)
    if not key:
        continue
    if key not in hero_abilities:
        hero_abilities[key] = []
    hero_abilities[key].append(ab)

# 生成新数据库
result = []
for h in heroes:
    key = h['key']
    abs_list = hero_abilities.get(key, [])
    
    # 提取有 description 的主要技能
    abilities = []
    for ab in abs_list:
        if not ab.get('description'):
            continue
        abilities.append({
            'key': ab.get('name', ''),
            'name': ab.get('localized_name', ''),
            'mc': ab.get('mana_cost'),
            'cd': ab.get('cooldown'),
            'desc': ab.get('description', ''),
            'behavior': ab.get('behavior', ''),
            'cast_range': ab.get('cast_range'),
            'cast_point': ab.get('cast_point'),
            'duration': ab.get('duration'),
            'damage': ab.get('damage'),
            'scepter_grants': ab.get('scepter_grants'),
            'shard_grants': ab.get('shard_grants'),
        })
    
    result.append({
        'hero_key': key,
        'abilities': abilities,
        'talents': old_talents_map.get(key, [])
    })

with open(OUTPUT_FILE, 'w') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

total_abs = sum(len(x['abilities']) for x in result)
print(f'Updated {len(result)} heroes, total abilities: {total_abs}')
