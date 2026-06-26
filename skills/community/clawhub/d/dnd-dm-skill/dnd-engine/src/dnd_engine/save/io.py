"""
存档读写函数库（dnd-engine 版）

继承自 skill code/save/io.py，去掉：
  - write_save_with_summary（依赖于 LLM 层的 summary.generate）
  - echo 相关依赖（LLM 层逻辑）
保留核心的存档 CRUD + 场景缓存绑定
"""
import json
import os
import sys
from datetime import datetime
from dnd_engine.save.scene_cache import embed_scene_cache, extract_scene_cache

SAVES_DIR = 'saves'


def set_saves_dir(path):
    """允许外部设定存档目录（默认为工作目录下的 saves/）"""
    global SAVES_DIR
    SAVES_DIR = path


def _ensure_saves_dir():
    os.makedirs(SAVES_DIR, exist_ok=True)


def _get_next_save_num():
    _ensure_saves_dir()
    max_num = 0
    if os.path.isdir(SAVES_DIR):
        for fn in os.listdir(SAVES_DIR):
            if fn.startswith('存档') and fn.endswith('.json'):
                try:
                    num = int(fn.replace('存档', '').replace('.json', ''))
                    max_num = max(max_num, num)
                except ValueError:
                    continue
    return max_num + 1


def list_saves():
    _ensure_saves_dir()
    saves = []
    if not os.path.isdir(SAVES_DIR):
        return saves
    for fn in sorted(os.listdir(SAVES_DIR)):
        if not (fn.startswith('存档') and fn.endswith('.json')):
            continue
        fp = os.path.join(SAVES_DIR, fn)
        try:
            with open(fp, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
            num = int(fn.replace('存档', '').replace('.json', ''))
            party_info = ''
            if 'party' in data:
                levels = [f"{p.get('name','?')} Lv.{p.get('level',1)}" for p in data['party']]
                party_info = ', '.join(levels)
            saves.append({
                "num": num, "filename": fn,
                "timestamp": data.get('timestamp', '未知'),
                "chapter": data.get('chapter', 1),
                "location": data.get('location', '未知'),
                "party_levels": party_info,
            })
        except Exception:
            saves.append({
                "num": 0, "filename": fn,
                "timestamp": '损坏', "chapter": '?',
                "location": '无法读取', "party_levels": '',
            })
    return sorted(saves, key=lambda x: x['num'])


def load_save(save_num):
    fp = os.path.join(SAVES_DIR, f'存档{save_num}.json')
    if not os.path.exists(fp):
        return None
    try:
        with open(fp, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        extract_scene_cache(data)
        return data
    except Exception:
        return None


def write_save(save_data):
    save_num = _get_next_save_num()
    filename = f'存档{save_num}.json'
    fp = os.path.join(SAVES_DIR, filename)
    if 'timestamp' not in save_data:
        save_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    embed_scene_cache(save_data)
    with open(fp, 'w', encoding='utf-8') as f:
        json.dump(save_data, f, ensure_ascii=False, indent=2)
    return filename


def get_save_display(saves):
    if not saves:
        return "📂 没有找到存档。"
    lines = ["📂 共 {} 个存档：".format(len(saves)), ""]
    for s in saves:
        lines.append("  {}. `{}` — {}".format(s['num'], s['filename'], s['timestamp']))
        lines.append("     第{}章 · {} · {}".format(s['chapter'], s['location'], s['party_levels']))
    return "\n".join(lines)
def rebuild_live_party(save_data):
    """
    从存档数据重建 live_party.json（完整格式）。
    提取角色的完整属性、技能、攻击、法术、装备等数据。
    """
    from datetime import datetime
    
    party = []
    save_party = save_data.get('party', [])
    team = save_data.get('全队状态', {})
    
    for i, sp in enumerate(save_party):
        if isinstance(sp, str):
            continue
        name = sp.get('name', '')
        items_raw = sp.get('items', [])
        
        char = {
            'name': name,
            'race': sp.get('race', ''),
            'class': sp.get('class', ''),
            'subclass': sp.get('sub', ''),
            'level': sp.get('level', 1),
            'hp': {'current': sp.get('hp', sp.get('maxHp', 10)),
                   'max': sp.get('maxHp', sp.get('hp', 10)),
                   'temp': sp.get('tempHp', 0)},
            'ac': sp.get('ac', 10),
            'acDetail': sp.get('acDetail', ''),
            'initiative': sp.get('initiative', 0),
            'speed': sp.get('speed', 30),
            'proficiency': sp.get('proficiencyBonus', 2),
            'xp': {'current': sp.get('xp', 0), 'toNext': sp.get('lvlUpXp', 300)},
            'stats': sp.get('stats', {}),
            'saves': sp.get('savingThrows', {}),
            'skills': [],
            'resources': [],
            'features': sp.get('classFeatures', []) + sp.get('raceTraits', []),
            'attacks': sp.get('attacks', []),
            'spells': sp.get('spells', []),
            'spellcasting': sp.get('spellcasting', {}),
            'spellSlots': sp.get('spellSlots', {}),
            'equipped': sp.get('equipped', []),
            'backpack': [],
            'armor': sp.get('armor', ''),
            'gear': sp.get('gear', ''),
            'inventory': sp.get('inventory', []),
        }
        
        # Convert skills from dict format to array
        skills_dict = sp.get('skills', {})
        char['skills'] = [
            {'name': k, 'prof': v, 'expertise': False, 'mod': 0}
            for k, v in skills_dict.items() if isinstance(v, bool)
        ]
        
        # Convert saves from dict to proper format
        saves_dict = sp.get('savingThrows', {})
        char['saves'] = {k: 2 if v else 0 for k, v in saves_dict.items()}
        
        # Separate inventory into backpack
        inv = sp.get('inventory', [])
        char['backpack'] = [i.get('name', '') for i in inv if isinstance(i, dict)]
        
        party.append(char)
    
    live_data = {
        '_说明': '实时角色状态（完整格式，由 sync_live_from_save 生成）',
        '_格式版本': '2.0',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'chapter': save_data.get('chapter', 1),
        'location': save_data.get('location', ''),
        'party': party,
    }
    
    # Write to live_party.json
    fp = 'live_party.json'
    with open(fp, 'w', encoding='utf-8') as f:
        json.dump(live_data, f, ensure_ascii=False, indent=2)
    
    return live_data
