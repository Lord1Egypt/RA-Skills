#!/usr/bin/env python3
"""
用 OpenDota hero_abilities 重建 abilities_db.json
- 技能顺序：从 OpenDota 的 abilities 数组（游戏内 QWER 顺序）
- 先天技能：从 dota2.com.cn 的 is_innate=true（innate_abilities.json）
- 中文名：从 abilities_cn.json
- A杖/魔晶：保留原 abilities_db.json 的 scepter_grants/shard_grants
版本：7.41 | 2026-04-29
"""
import json
import os
import urllib.request
import urllib.error

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_json(filename):
    path = os.path.join(SCRIPT_DIR, filename)
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}

def save_json(filename, data):
    path = os.path.join(SCRIPT_DIR, filename)
    with open(path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def fetch_hero_abilities():
    """从 OpenDota 获取所有英雄技能数据"""
    url = "https://api.opendota.com/api/constants/hero_abilities"
    print(f"[OpenDota] 获取 hero_abilities...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"[错误] 获取失败: {e}")
        return None

def fetch_dota2cn_innate():
    """从 dota2.com.cn 获取先天技能列表"""
    url = "https://www.dota2.com.cn/datafeed/abilitylist?task=abilitylist&lang=zhcn"
    print(f"[dota2.com.cn] 获取 innate...")
    try:
        req = urllib.request.Request(url, headers={"Referer": "https://www.dota2.com.cn/", "User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        abilities = data['result']['data']['itemabilities']
        innate = [a for a in abilities if a.get('is_innate') == True]
        return {a['name']: a.get('name_loc', '') for a in innate}
    except Exception as e:
        print(f"[错误] dota2.com.cn 获取失败: {e}")
        return {}

def rebuild_abilities():
    # 加载数据
    abilities_db_old = load_json('abilities_db.json')  # 现有数据（保留 scepter/shard）
    abilities_cn = load_json('abilities_cn.json')
    abilities_cn_map = abilities_cn.get('abilities', {})
    innate_cn = load_json('innate_abilities.json')  # dota2.com.cn 先天技能

    # 构建 innate_keys 集合（用于快速判断）
    innate_keys = set()
    for hero_innates in innate_cn.values():
        if isinstance(hero_innates, dict):
            innate_keys.update(hero_innates.keys())

    # 转成 dict 方便查 scepter/shard
    old_db = {entry['hero_key']: {a['key']: a for a in entry['abilities']}
              for entry in abilities_db_old}

    # 加载 heroes_db 用于验证
    heroes_db = load_json('heroes_db.json')
    heroes_keys = {h['key'] for h in heroes_db}

    # 从 OpenDota 获取
    odo_data = fetch_hero_abilities()
    if not odo_data:
        print("[错误] OpenDota 数据获取失败，退出")
        return

    new_abilities_db = []

    for hero_key, hero_data in odo_data.items():
        if not hero_key.startswith('npc_dota_hero_'):
            continue
        hero_key = hero_key.replace('npc_dota_hero_', '')
        if hero_key not in heroes_keys:
            continue

        abilities_list = hero_data.get('abilities', [])
        old_abilities_map = old_db.get(hero_key, {})

        # 过滤掉 generic_hidden，展平嵌套 list
        flat_keys = []
        for a in abilities_list:
            if a == 'generic_hidden':
                continue
            if isinstance(a, list):
                flat_keys.extend(a)
            elif isinstance(a, str):
                flat_keys.append(a)

        # 构建技能详情
        abilities_detail = []
        for ability_key in flat_keys:
            old_ab = old_abilities_map.get(ability_key, {})
            cn_entry = abilities_cn_map.get(ability_key, {})
            cn_name = cn_entry.get('name_loc') or ability_key

            ability_entry = {
                'key': ability_key,
                'name': cn_name,
                'mc': cn_entry.get('mana_cost'),
                'cd': cn_entry.get('cooldown'),
                'behavior': cn_entry.get('behavior') or '',
                'scepter_grants': old_ab.get('scepter_grants', False),
                'shard_grants': old_ab.get('shard_grants', False),
            }

            if ability_key in innate_keys:
                ability_entry['is_innate'] = True

            abilities_detail.append(ability_entry)

        new_abilities_db.append({
            'hero_key': hero_key,
            'abilities': abilities_detail,
            'talents': []
        })

    new_abilities_db.sort(key=lambda x: x['hero_key'])
    save_json('abilities_db.json', new_abilities_db)
    
    innate_count = sum(1 for e in new_abilities_db for a in e['abilities'] if a.get('is_innate'))
    print(f"[完成] 重建 abilities_db.json：{len(new_abilities_db)} 个英雄，{innate_count} 个先天技能")

if __name__ == '__main__':
    rebuild_abilities()
