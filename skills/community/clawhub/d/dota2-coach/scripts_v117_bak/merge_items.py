#!/usr/bin/env python3
"""
合并 dotabase items.json 和本地 items_db.json
- dotabase 提供 description、lore、cooldown、icon 等丰富字段
- 本地提供 key（程序化ID）、qual、notes

用法: python3 merge_items.py
"""
import json

DOTABASE_FILE = '/tmp/dotabase_items.json'
LOCAL_FILE = '/root/.openclaw/workspace/magi/skills/dota2-coach/scripts/items_db.json'
OUTPUT_FILE = '/root/.openclaw/workspace/magi/skills/dota2-coach/scripts/items_db.json'

# 加载本地 items（用于获取 key、qual、notes）
with open(LOCAL_FILE) as f:
    local_items = json.load(f)

# 建立 name -> local_item 的映射
local_by_name = {item['name']: item for item in local_items}

# 加载 dotabase items
with open(DOTABASE_FILE) as f:
    dotabase_items = json.load(f)

# 合并
merged = []
for item in dotabase_items:
    name = item.get('name', '')
    local = local_by_name.get(name, {})
    
    # 构建 key（从 name 推导，比如 "Black King Bar" -> "black_king_bar"）
    key = local.get('key', '')
    if not key:
        # 从 name 推导
        key = name.lower().replace(' ', '_').replace("'", '').replace('-', '_')
    
    merged.append({
        'id': item.get('id'),
        'key': key,
        'name': name,
        'localized_name': item.get('localized_name', ''),
        'cost': item.get('cost'),
        'qual': local.get('qual', ''),
        'notes': local.get('notes', ''),
        'description': item.get('description', ''),
        'lore': item.get('lore', ''),
        'cooldown': item.get('cooldown'),
        'mana_cost': item.get('mana_cost'),
        'cast_range': item.get('cast_range'),
        'neutral_tier': item.get('neutral_tier'),
        'is_neutral_enhancement': item.get('is_neutral_enhancement', False),
        'secret_shop': item.get('secret_shop', False),
        'shop_tags': item.get('shop_tags', ''),
    })

# 按 id 排序
merged.sort(key=lambda x: x.get('id', 0))

with open(OUTPUT_FILE, 'w') as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

neutral = sum(1 for x in merged if x.get('is_neutral_enhancement'))
print(f'Merged {len(merged)} items ({neutral} neutral items)')
