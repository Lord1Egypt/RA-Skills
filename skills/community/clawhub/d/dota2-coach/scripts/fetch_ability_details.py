#!/usr/bin/env python3
"""
从 OpenDota /api/constants/abilities 拉取技能详情（CD、蓝耗、范围、是否无视魔免、描述），
合并到 abilities_db.json 里。
"""
import json
import subprocess

def fetch_ability_details():
    url = "https://api.opendota.com/api/constants/abilities"
    result = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
    return json.loads(result.stdout)

def get_ability_field(ability_data, key, attrib_header_keyword=None):
    """从 ability data 中提取指定字段"""
    if ability_data is None:
        return None
    
    # 尝试直接从字段取
    val = ability_data.get(key)
    if val is not None:
        return val
    
    # 从 attrib 里找
    if attrib_header_keyword:
        for attr in ability_data.get('attrib', []):
            if attrib_header_keyword.lower() in attr.get('header', '').lower():
                return attr.get('value')
    
    return None

def main():
    # 加载现有数据
    with open('scripts/abilities_db.json', 'r', encoding='utf-8') as f:
        abilities_db = json.load(f)
    
    # 拉取 OpenDota abilities
    print("正在从 OpenDota 拉取技能详情...")
    od_abilities = fetch_ability_details()
    print(f"共获取 {len(od_abilities)} 个技能数据")
    
    # 建立 key -> ability data 的映射
    # OpenDota 的 key 就是 ability key 如 oracle_fortunes_end
    
    updated = 0
    for hero in abilities_db:
        hero_key = hero['hero_key']
        for ability in hero['abilities']:
            ab_key = ability['key']
            od_data = od_abilities.get(ab_key)
            if od_data:
                # 提取字段
                cd = get_ability_field(od_data, 'cd', 'COOLDOWN')
                mc = get_ability_field(od_data, 'mc', 'MANA COST')
                cast_range = get_ability_field(od_data, None, 'CAST RANGE')
                bkb_pierce = od_data.get('bkbpierce')  # Yes/No
                desc = od_data.get('desc', '')
                
                ability['cd'] = cd
                ability['mc'] = mc
                ability['cast_range'] = cast_range
                ability['bkbpierce'] = bkb_pierce
                ability['desc'] = desc
                updated += 1
    
    print(f"更新了 {updated} 个技能详情")
    
    # 保存
    with open('scripts/abilities_db.json', 'w', encoding='utf-8') as f:
        json.dump(abilities_db, f, ensure_ascii=False, indent=2)
    print("已保存到 scripts/abilities_db.json")

if __name__ == '__main__':
    main()
