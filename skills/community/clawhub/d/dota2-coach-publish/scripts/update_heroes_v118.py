#!/usr/bin/env python3
"""
v1.1.8 英雄基础属性更新（修复版）
- 修复 key 映射（影魔/不朽尸王/末日使者/殁境神蚀者/百戏大王）
- 修复 troll_warlord damage_min/max（当前为 None，直接设值）
"""
import json, os, shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HEROES_FILE = f'{SCRIPT_DIR}/heroes_db.json'
BACKUP_FILE = f'{SCRIPT_DIR}/../backup_v118_20260731/heroes_db_pre_attr.json'

# 已回滚到备份状态，所以直接写
# 格式：(hero_key, field, old, new, desc)
# old=None 表示跳过旧值检查（用于当前为 None 的字段如 damage_min）
patches = [
    ("earth_spirit",        "int",          18,   17,   "基础智力 18→17"),
    ("legion_commander",    "str",          24,   25,   "基础力量 24→25"),
    ("legion_commander",    "str_gain",     3.1,  3.0,  "力量成长 3.1→3.0"),
    ("legion_commander",    "damage_min",   None, 58,   "1级攻击力下限 57→58"),
    ("legion_commander",    "damage_max",   None, 62,   "1级攻击力上限 61→62"),
    ("troll_warlord",       "agi",          23,   24,   "基础敏捷 23→24"),
    ("troll_warlord",       "damage_min",   None, 51,   "1级攻击力下限 50→51"),
    ("troll_warlord",       "damage_max",   None, 59,   "1级攻击力上限 58→59"),
    ("pugna",               "int",          26,   27,   "基础智力 26→27"),
    ("nevermore",           "int",          18,   16,   "基础智力 18→16"),
    ("axe",                 "agi",          20,   18,   "基础敏捷 20→18"),
    ("jakiro",              "int_gain",     3.0,  3.3,  "智力成长 3.0→3.3"),
    ("death_prophet",       "agi_gain",     2,    2.3,  "敏捷成长 2→2.3"),
    ("mars",                "int_gain",     2.2,  2.4,  "智力成长 2.2→2.4"),
    ("lina",                "agi",          23,   21,   "基础敏捷 23→21"),
    ("undying",             "move_speed",   300,  295,  "基础移动速度 300→295"),
    ("ember_spirit",        "move_speed",   300,  295,  "基础移动速度 300→295"),
    ("doom_bringer",        "attack_range", 200,  175,  "攻击距离 200→175"),
]

# 跳过
skipped = [
    "tiny: 基础生命恢复 -1.0 — heroes_db.json 无 health_regen 字段",
    "troll_warlord: 基础攻击速度 100→105 — 无 base_attack_speed 字段",
    "legion_commander: 基础攻击速度 100→105 — 无 base_attack_speed 字段",
    "treant: 基础攻击速度 100→90 — 无 base_attack_speed 字段",
    "lone_druid: 熊灵基础护甲 -1 — 不在 heroes_db.json 里",
    "death_prophet: 攻击力成长 +3.6→+3.7 — 无 attack_gain 字段",
    "zuus: 攻击速度 30→20（霹雳之手）— 技能属性，在 abilities_db 里处理",
]

def main():
    backup_dir = os.path.dirname(BACKUP_FILE)
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir, exist_ok=True)
    if not os.path.exists(BACKUP_FILE):
        shutil.copy2(HEROES_FILE, BACKUP_FILE)
        print(f'已备份: {BACKUP_FILE}')
    else:
        print(f'备份已存在: {BACKUP_FILE}')

    with open(HEROES_FILE, 'r', encoding='utf-8') as f:
        heroes = json.load(f)
    heroes_by_key = {h['key']: h for h in heroes}

    applied, failed = [], []

    for hero_key, field, old, new, desc in patches:
        if hero_key not in heroes_by_key:
            failed.append(f'{hero_key}.{field}: 英雄未找到')
            continue
        hero = heroes_by_key[hero_key]
        cur = hero.get(field)
        # 如果是 damage_min/max 且当前为 None，直接设值
        if cur is None and old is None:
            hero[field] = new
            applied.append((hero_key, field, cur, new, desc))
        elif cur == old:
            hero[field] = new
            applied.append((hero_key, field, cur, new, desc))
        else:
            failed.append(f'{hero_key}.{field}: 当前={cur}, 期望={old}')

    if applied:
        with open(HEROES_FILE, 'w', encoding='utf-8') as f:
            json.dump(heroes, f, ensure_ascii=False, indent=2)

    print(f'\n=== 成功: {len(applied)} / 失败: {len(failed)} ===\n')
    for hk, f, o, n, d in applied:
        print(f'  ✅ {hk}.{f}: {o} → {n} ({d})')
    if failed:
        print('\n=== 失败 ===')
        for line in failed:
            print(f'  ❌ {line}')
    print(f'\n=== 跳过: {len(skipped)} 项 ===')
    for s in skipped:
        print(f'  ⏭  {s}')

if __name__ == '__main__':
    main()