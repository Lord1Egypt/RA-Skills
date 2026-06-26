"""
角色状态实时管理：live_party.json 读写
"""
import json
import os
from datetime import datetime

LIVE_FILE = 'live_party.json'


def get_all_characters():
    """
    从 live_party.json 获取全部角色数据
    
    返回:
        dict: {"party": list[dict], "location": str, ...} 或默认空结构
    """
    if not os.path.exists(LIVE_FILE):
        return {"party": [], "location": "", "timestamp": "", "gold": 0}
    try:
        with open(LIVE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {"party": [], "location": "", "timestamp": "", "gold": 0}


def get_character(name):
    """
    根据名字查找单个角色
    
    参数:
        name: str - 角色名
    
    返回:
        dict: 该角色数据，或 None
    """
    data = get_all_characters()
    for char in data.get('party', []):
        if char.get('name') == name:
            return char
    return None


def update_party(party_data):
    """
    更新 live_party.json，全部覆盖写入
    
    参数:
        party_data: dict - 新的队伍数据（从存档或实时变更产生）
    
    返回:
        bool: 是否写入成功
    """
    try:
        party_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(LIVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(party_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def update_character(name, updates):
    """
    更新单个角色的特定字段（就地修改）
    
    参数:
        name: str - 角色名
        updates: dict - 要更新的字段
    
    返回:
        bool: 是否成功
    """
    data = get_all_characters()
    for char in data.get('party', []):
        if char.get('name') == name:
            char.update(updates)
            return update_party(data)
    return False


def update_hp(name, new_hp):
    """快速更新角色 HP"""
    return update_character(name, {"hp": new_hp})


def update_spell_slots(name, level, used):
    """快速更新法术位消耗"""
    data = get_all_characters()
    for char in data.get('party', []):
        if char.get('name') == name:
            slots = char.get('spellSlots', [])
            while len(slots) < level:
                slots.append({"level": len(slots)+1, "total": 0, "used": 0})
            slots[level-1]["used"] = used
            char["spellSlots"] = slots
            return update_party(data)
    return False


def find_item_in_party(item_name):
    """
    搜索物品在哪个角色身上
    
    参数:
        item_name: str - 物品名（支持部分匹配）
    
    返回:
        list[dict]: [{"character": str, "item": dict, "equipped": bool}, ...]
    """
    data = get_all_characters()
    results = []
    for char in data.get('party', []):
        for item in char.get('inventory', []) + char.get('equipment', []):
            if item_name.lower() in item.get('name', '').lower():
                results.append({
                    "character": char.get('name', '?'),
                    "item": item,
                    "equipped": item.get('equipped', False),
                })
    return results


def get_party_summary():
    """
    获取队伍简要摘要（用于快速查看）
    
    返回:
        str: 摘要文本
    """
    data = get_all_characters()
    lines = [
        f"━━━ 队伍状态 ━━━  📍 {data.get('location', '?')}",
        "",
        "| 角色 | HP | AC | 等级 |",
        "|:---:|:--:|:--:|:----:|",
    ]
    for char in data.get('party', []):
        lines.append(
            f"| {char.get('emoji','')} **{char.get('name','?')}** | "
            f"**{char.get('hp','?')}/{char.get('maxHp','?')}** | "
            f"**{char.get('ac','?')}** | "
            f"Lv.{char.get('level',1)} |"
        )
    return "\n".join(lines)
