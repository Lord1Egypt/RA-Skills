#!/usr/bin/env python3
"""
Dota 2 英雄+物品综合查询脚本
使用本地 JSON 数据库 + OpenDota API 实时数据
版本：7.41 | 最后更新：2026-04-23
"""
import sys
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
    return []

def get_heroes_from_api():
    url = "https://api.opendota.com/api/heroStats"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"[API] 获取英雄数据失败: {e}", file=sys.stderr)
        return None

def get_items_from_api():
    url = "https://api.opendota.com/api/constants/items"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"[API] 获取物品数据失败: {e}", file=sys.stderr)
        return None

def update_heroes_db():
    """更新英雄数据库（从 OpenDota）"""
    data = get_heroes_from_api()
    if data is None:
        print("[错误] 无法从API获取英雄数据")
        return False
    heroes = []
    for h in data:
        heroes.append({
            'id': h['id'],
            'name': h['localized_name'],
            'key': h['name'].replace('npc_dota_hero_',''),
            'roles': h.get('roles',[]),
            'attr': h.get('primary_attr',''),
            'attack': h.get('attack_type',''),
            'str': h.get('base_str',0),
            'agi': h.get('base_agi',0),
            'int': h.get('base_int',0),
            'str_gain': h.get('str_gain',0),
            'agi_gain': h.get('agi_gain',0),
            'int_gain': h.get('int_gain',0),
            'move_speed': h.get('move_speed',0),
            'armor': h.get('base_armor',0),
            'attack_range': h.get('attack_range',0),
            'hp': h.get('base_health',0),
            'mana': h.get('base_mana',0),
            'damage_min': h.get('base_attack_min',0),
            'damage_max': h.get('base_attack_max',0),
            'pub_pick': h.get('pub_pick',0),
            'pub_win': h.get('pub_win',0),
            'pro_pick': h.get('pro_pick',0),
            'pro_win': h.get('pro_win',0),
            '1_pick': h.get('1_pick',0), '1_win': h.get('1_win',0),
            '2_pick': h.get('2_pick',0), '2_win': h.get('2_win',0),
            '3_pick': h.get('3_pick',0), '3_win': h.get('3_win',0),
            '4_pick': h.get('4_pick',0), '4_win': h.get('4_win',0),
            '5_pick': h.get('5_pick',0), '5_win': h.get('5_win',0),
        })
    path = os.path.join(SCRIPT_DIR, "heroes_db.json")
    with open(path, 'w') as f:
        json.dump(heroes, f, ensure_ascii=False)
    print(f"英雄数据库已更新: {len(heroes)} 个英雄")
    return True

def update_cn_names():
    """从 dota2.com.cn 获取英雄和物品的中文名"""
    heroes_path = os.path.join(SCRIPT_DIR, "heroes_db.json")
    items_path = os.path.join(SCRIPT_DIR, "items_db.json")
    
    # Fetch 英雄中文名
    try:
        req = urllib.request.Request(
            "https://www.dota2.com.cn/datafeed/heroList?task=herolist",
            headers={"Referer": "https://www.dota2.com.cn/", "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            cn_heroes_data = json.loads(resp.read())['result']['heroes']
        print(f"[CN] 获取到 {len(cn_heroes_data)} 个英雄中文名")
    except Exception as e:
        print(f"[CN] 获取英雄中文名失败: {e}")
        cn_heroes_data = []
    
    # Fetch 物品中文名
    try:
        req = urllib.request.Request(
            "https://www.dota2.com.cn/datafeed/itemlist?task=itemlist",
            headers={"Referer": "https://www.dota2.com.cn/", "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            cn_items_data = json.loads(resp.read())['result']['data']['itemabilities']
        print(f"[CN] 获取到 {len(cn_items_data)} 个物品中文名")
    except Exception as e:
        print(f"[CN] 获取物品中文名失败: {e}")
        cn_items_data = []
    
    # Build CN maps
    cn_hero_map = {h['name']: h['name_loc'] for h in cn_heroes_data}
    cn_item_map = {}
    for item in cn_items_data:
        key = item['name'].replace('item_', '') if item['name'].startswith('item_') else item['name']
        cn_item_map[key] = item['name_loc']
    
    # Update heroes_db
    if os.path.exists(heroes_path):
        with open(heroes_path) as f:
            heroes = json.load(f)
        updated = 0
        for hero in heroes:
            for cn_h in cn_heroes_data:
                if cn_h['name_english_loc'] == hero['name']:
                    hero['localized_name'] = cn_h['name_loc']
                    updated += 1
                    break
        with open(heroes_path, 'w') as f:
            json.dump(heroes, f, ensure_ascii=False, indent=2)
        print(f"[CN] 英雄中文名已更新: {updated}/{len(heroes)} 个")
    
    # Update items_db
    if os.path.exists(items_path):
        with open(items_path) as f:
            items = json.load(f)
        updated = 0
        for item in items:
            key = item.get('key', '')
            if key in cn_item_map:
                item['localized_name'] = cn_item_map[key]
                updated += 1
        with open(items_path, 'w') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        print(f"[CN] 物品中文名已更新: {updated}/{len(items)} 个")
    
    return True

def update_abilities_cn():
    """从完美/dota2.com.cn 获取技能中英文对照（含先天技能标注）"""
    abilities_cn_path = os.path.join(SCRIPT_DIR, "abilities_cn.json")
    
    # 从完美 API 获取所有技能数据（含 is_innate 标注）
    try:
        req = urllib.request.Request(
            "https://www.dota2.com.cn/datafeed/abilitylist?task=abilitylist&lang=zhcn",
            headers={"Referer": "https://www.dota2.com.cn/", "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        abilities_list = data['result']['data']['itemabilities']
        print(f"[API] 获取到 {len(abilities_list)} 个技能数据")
    except Exception as e:
        print(f"[API] 获取技能数据失败: {e}")
        return False
    
    # Build abilities map + innate list
    abilities_map = {}
    innate_list = []
    for ab in abilities_list:
        name = ab.get('name', '')
        name_loc = ab.get('name_loc', '')
        name_english = ab.get('name_english_loc', '')
        is_innate = ab.get('is_innate', False)
        if name:
            abilities_map[name] = {
                'name_loc': name_loc,
                'name_english_loc': name_english,
                'is_innate': is_innate
            }
            if is_innate and name_loc:
                innate_list.append(name)
    
    output = {'abilities': abilities_map, 'innate': innate_list}
    with open(abilities_cn_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"[API] 技能中文名已保存: {len(abilities_map)} 个技能, {len(innate_list)} 个先天技能")
    return True

def update_innate_abilities():
    """根据 abilities_db.json + abilities_cn.json 生成 innte_abilities.json（127英雄全覆盖）"""
    abilities_db_path = os.path.join(SCRIPT_DIR, "abilities_db.json")
    abilities_cn_path = os.path.join(SCRIPT_DIR, "abilities_cn.json")
    innate_path = os.path.join(SCRIPT_DIR, "innate_abilities.json")
    
    if not os.path.exists(abilities_db_path):
        print(f"[错误] abilities_db.json 不存在，请先运行数据库初始化")
        return False
    if not os.path.exists(abilities_cn_path):
        print(f"[错误] abilities_cn.json 不存在，请先运行 --abilities-cn")
        return False
    
    with open(abilities_db_path, 'r', encoding='utf-8') as f:
        abilities_db = json.load(f)
    with open(abilities_cn_path, 'r', encoding='utf-8') as f:
        abilities_cn = json.load(f)
    
    cn_ab = abilities_cn.get('abilities', {})
    cn_innate = abilities_cn.get('innate', [])  # List of keys marked as innate by API
    
    def local_detect_innate(ab):
        """本地检测先天技能"""
        b = ab.get('behavior', '')
        mc = ab.get('mc')
        cd = ab.get('cd')
        
        if ab.get('scepter_grants') or ab.get('shard_grants'):
            return False
        if 'ultimate' in b:  # R技能不是先天技能
            return False
        # 明确标记
        if 'not_learnable' in b or 'innate_ui' in b:
            return True
        # 无蓝耗、无冷却的被动技能
        if mc is None and cd in [None, 0] and 'passive' in b:
            if 'skip_for_keybinds' in b:  # 跳过按键绑定但仍是能力
                return True
            if b.count('|') == 2 and 'hidden' in b:  # 只有 passive|hidden = 可能是子技能，跳过
                return False
            return True
        return False
    
    all_innates = {}
    for h in abilities_db:
        hero_key = h['hero_key']
        innate_for_hero = {}
        
        # 本地检测（主要来源）
        for ab in h['abilities']:
            if local_detect_innate(ab):
                key = ab['key']
                cn_info = cn_ab.get(key, {})
                name_cn = cn_info.get('name_loc') or cn_info.get('name_english_loc') or ab['name']
                innate_for_hero[key] = name_cn
        
        # API 列表补充（填补本地检测漏掉的）
        for ab_key in cn_innate:
            # 处理 sand_king -> sandking 等命名差异
            prefix1 = hero_key + '_'
            prefix2 = hero_key.replace('_', '') + '_'
            if ab_key.startswith(prefix1) or ab_key.startswith(prefix2):
                if ab_key not in innate_for_hero:
                    cn_name = cn_ab.get(ab_key, {}).get('name_loc', '')
                    if cn_name:
                        innate_for_hero[ab_key] = cn_name
        
        if innate_for_hero:
            all_innates[hero_key] = innate_for_hero
    
    with open(innate_path, 'w', encoding='utf-8') as f:
        json.dump(all_innates, f, ensure_ascii=False, indent=2)
    print(f"[API] 先天技能已保存: {len(all_innates)} 个英雄")
    return True

def update_talents_db():
    """从 dotabase + OpenDota + 完美API 构建天赋树数据库（英文+中文）"""
    talents_en_path = os.path.join(SCRIPT_DIR, "talents_db.json")
    talents_cn_path = os.path.join(SCRIPT_DIR, "talents_db_cn.json")
    
    # Fetch heroes for id->key mapping
    try:
        req = urllib.request.Request(
            "https://api.opendota.com/api/heroes",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        heroes_resp = urllib.request.urlopen(req, timeout=10)
        heroes_api = json.loads(heroes_resp.read())
        hero_id_to_key = {h['id']: h['name'].replace('npc_dota_hero_', '') for h in heroes_api}
        print(f"[API] 获取 {len(hero_id_to_key)} 个英雄映射")
    except Exception as e:
        print(f"[API] 获取英雄列表失败: {e}")
        return False
    
    # Fetch talents from dotabase
    try:
        req2 = urllib.request.Request(
            "https://raw.githubusercontent.com/mdiller/dotabase/master/json/talents.json",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        talents_resp = urllib.request.urlopen(req2, timeout=10)
        talents = json.loads(talents_resp.read())
        print(f"[dotabase] 获取 {len(talents)} 个天赋条目")
    except Exception as e:
        print(f"[dotabase] 获取天赋数据失败: {e}")
        return False
    
    # Fetch abilities for name mapping
    try:
        req3 = urllib.request.Request(
            "https://raw.githubusercontent.com/mdiller/dotabase/master/json/abilities.json",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        abilities_resp = urllib.request.urlopen(req3, timeout=10)
        abilities = json.loads(abilities_resp.read())
        ab_id_to_name = {ab['id']: ab.get('name', '') for ab in abilities}
        ab_id_to_localized = {ab['id']: ab.get('localized_name', '') for ab in abilities}
    except Exception as e:
        print(f"[dotabase] 获取技能数据失败: {e}")
        return False
    
    # Load abilities_cn for Chinese names
    abilities_cn_path = os.path.join(SCRIPT_DIR, "abilities_cn.json")
    if os.path.exists(abilities_cn_path):
        with open(abilities_cn_path, 'r', encoding='utf-8') as f:
            abilities_cn = json.load(f)
        cn_map = abilities_cn.get('abilities', {})
    else:
        cn_map = {}
    
    def get_cn_name(ability_key):
        info = cn_map.get(ability_key, {})
        return info.get('name_loc') or info.get('name_english_loc') or ''
    
    from collections import defaultdict
    hero_talents = defaultdict(list)
    for t in talents:
        hero_id = t.get('hero_id')
        if not hero_id:
            continue
        hero_key = hero_id_to_key.get(hero_id)
        if not hero_key:
            continue
        ability_id = t.get('ability_id')
        slot = t.get('slot', 0)
        ability_key = ab_id_to_name.get(ability_id, '')
        ability_en = ab_id_to_localized.get(ability_id, ability_key)
        ability_cn = get_cn_name(ability_key) if ability_key else ''
        
        hero_talents[hero_key].append({
            'slot': slot,
            'level': (slot // 2) * 5 + 10,
            'side': 'left' if slot % 2 == 0 else 'right',
            'ability_key': ability_key,
            'ability_en': ability_en,
            'ability_cn': ability_cn
        })
    
    # Build output
    output_en = {}
    output_cn = {}
    for hero_key, talent_list in hero_talents.items():
        level_map_en = {}
        level_map_cn = {}
        for t in talent_list:
            lvl = t['level']
            side = t['side']
            if lvl not in level_map_en:
                level_map_en[lvl] = {'left': '', 'right': ''}
                level_map_cn[lvl] = {'left': '', 'right': ''}
            level_map_en[lvl][side] = t['ability_en']
            level_map_cn[lvl][side] = t['ability_cn']
        
        output_en[hero_key] = [
            {'level': lvl, 'left': level_map_en[lvl]['left'], 'right': level_map_en[lvl]['right']}
            for lvl in sorted(level_map_en.keys())
        ]
        output_cn[hero_key] = [
            {'level': lvl, 'left': level_map_cn[lvl]['left'], 'right': level_map_cn[lvl]['right']}
            for lvl in sorted(level_map_cn.keys())
        ]
    
    with open(talents_en_path, 'w', encoding='utf-8') as f:
        json.dump(output_en, f, ensure_ascii=False, indent=2)
    print(f"[数据] 天赋树英文已保存: {len(output_en)} 个英雄")
    
    with open(talents_cn_path, 'w', encoding='utf-8') as f:
        json.dump(output_cn, f, ensure_ascii=False, indent=2)
    print(f"[数据] 天赋树中文已保存: {len(output_cn)} 个英雄")
    return True

def update_items_db():
    """更新物品数据库"""
    data = get_items_from_api()
    if data is None:
        print("[错误] 无法从API获取物品数据")
        return False
    items = []
    for k,v in data.items():
        if isinstance(v,dict) and v.get('id'):
            items.append({
                'id': v['id'],
                'key': k,
                'name': v.get('dname',''),
                'cost': v.get('cost',0),
                'qual': v.get('qual',''),
            })
    items.sort(key=lambda x: x['id'])
    path = os.path.join(SCRIPT_DIR, "items_db.json")
    with open(path, 'w') as f:
        json.dump(items, f, ensure_ascii=False)
    print(f"物品数据库已更新: {len(items)} 个物品")
    return True

def search_heroes(query, heroes):
    q = query.lower()
    results = []
    for h in heroes:
        if q in h['name'].lower() or q in h.get('key','').lower() or str(h['id']) == q:
            results.append(h)
    return results

def search_items(query, items):
    q = query.lower()
    results = []
    for it in items:
        if q in it['name'].lower() or q in it.get('key','').lower() or str(it['id']) == q:
            results.append(it)
    return results

def print_hero(h):
    print(f"\n{'='*50}")
    print(f"📊 {h['name']} (ID:{h['id']})")
    print(f"定位: {', '.join(h.get('roles', []))}")
    print(f"属性: {h.get('attr','')} / {h.get('attack','')}")
    print(f"基础属性: STR {h.get('str',0)}(+{h.get('str_gain',0)}) / AGI {h.get('agi',0)}(+{h.get('agi_gain',0)}) / INT {h.get('int',0)}(+{h.get('int_gain',0)})")
    print(f"移速: {h.get('move_speed',0)} | 护甲: {h.get('armor',0)} | 攻击范围: {h.get('attack_range',0)}")
    
    for pos, name in [(1,'Carry'),(2,'Mid'),(3,'Offlane'),(4,'SoftSupport'),(5,'HardSupport')]:
        pick = h.get(f'{pos}_pick', 0)
        if pick > 1000:
            win = h.get(f'{pos}_win', 0)
            print(f"{name}: {pick}场 胜率 {win/max(pick,1)*100:.1f}%")
    
    pub_pick = h.get('pub_pick', 0)
    pub_win = h.get('pub_win', 0)
    if pub_pick > 0:
        print(f"路人总: {pub_pick}场 胜率 {pub_win/max(pub_pick,1)*100:.1f}%")
    
    pro_pick = h.get('pro_pick', 0)
    pro_win = h.get('pro_win', 0)
    if pro_pick > 0:
        print(f"职业赛: {pro_pick}场 胜率 {pro_win/max(pro_pick,1)*100:.1f}%")
    print(f"{'='*50}")

def print_item(it):
    cost = it.get('cost', 0)
    print(f"  {it['name']} (ID:{it['id']}) | 价格:{cost} | 品质:{it.get('qual','')}")

if __name__ == "__main__":
    heroes = load_json("heroes_db.json")
    items = load_json("items_db.json")
    
    if len(sys.argv) < 2:
        print("用法: python3 fetch_hero.py <命令> [参数]")
        print("  python3 fetch_hero.py crystal        查询英雄")
        print("  python3 fetch_hero.py blink         查询物品")
        print("  python3 fetch_hero.py --update      更新数据库（OpenDota）")
        print("  python3 fetch_hero.py --cn          更新中文名（dota2.com.cn）")
        print("  python3 fetch_hero.py --list        列出所有英雄")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "--update":
        update_heroes_db()
        update_items_db()
    elif cmd == "--cn":
        update_cn_names()
    elif cmd == "--abilities-cn":
        update_abilities_cn()
    elif cmd == "--innate":
        update_innate_abilities()
    elif cmd == "--talents":
        update_talents_db()
    elif cmd == "--all":
        update_heroes_db()
        update_items_db()
        update_cn_names()
        update_abilities_cn()
        update_talents_db()
    elif cmd == "--list":
        if not heroes:
            print("[错误] 未找到heroes_db.json")
            sys.exit(1)
        print(f"\n共 {len(heroes)} 个英雄:\n")
        for h in sorted(heroes, key=lambda x: x['id']):
            print(f"  {h['id']:3d}. {h['name']}")
    elif len(sys.argv) > 2 and sys.argv[1] == "--hero":
        query = " ".join(sys.argv[2:])
        if not heroes:
            print("[错误] 未找到heroes_db.json，请先运行 --update")
            sys.exit(1)
        results = search_heroes(query, heroes)
        if results:
            for h in results:
                print_hero(h)
        else:
            print(f"未找到英雄: {query}")
    elif len(sys.argv) > 2 and sys.argv[1] == "--item":
        query = " ".join(sys.argv[2:])
        if not items:
            print("[错误] 未找到items_db.json，请先运行 --update")
            sys.exit(1)
        results = search_items(query, items)
        if results:
            for it in results[:10]:
                print_item(it)
        else:
            print(f"未找到物品: {query}")
    else:
        # 通用搜索
        query = " ".join(sys.argv[1:])
        if not heroes or not items:
            print("[错误] 数据库未初始化，请先运行 --update")
            sys.exit(1)
        hero_results = search_heroes(query, heroes)
        item_results = search_items(query, items)
        if hero_results:
            print(f"\n英雄匹配 '{query}':")
            for h in hero_results[:5]:
                print_hero(h)
        if item_results:
            print(f"\n物品匹配 '{query}':")
            for it in item_results[:10]:
                print_item(it)
        if not hero_results and not item_results:
            print(f"未找到: {query}")
