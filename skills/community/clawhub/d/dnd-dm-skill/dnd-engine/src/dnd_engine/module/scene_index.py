"""
场景级模块索引：将章节文件拆分为按场景行号索引，实现按需懒加载
"""
import os
import re
import json

def build_scene_index(filepath):
    """
    扫描章节文件，建立场景级行号索引

    参数:
        filepath: str - 章节文件路径

    返回:
        dict: 场景索引 {scenes: list, total_lines: int}
    """
    if not os.path.exists(filepath):
        return {"error": f"File not found: {filepath}", "scenes": []}

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    total_lines = len(lines)
    scenes = []
    current_scene = None
    intro_lines = []

    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith('## ') and not s.startswith('### '):
            # Save previous scene
            if current_scene:
                current_scene['end_line'] = i
                scenes.append(current_scene)

            title = s.lstrip('# ')
            current_scene = {
                'title': title,
                'start_line': i + 1,  # 1-indexed
                'end_line': total_lines,
                'type': 'section',
                'subsections': [],
                'line_count': 0,
                'tags': []
            }

            # Assign tags based on title — 通用关键词，适用于任何语言的 D&D 模组
            title_lower = title.lower()
            if any(kw in title for kw in ['运作', '运行']) or any(kw in title_lower for kw in ['running the', 'how to', 'running this', 'about this']):
                current_scene['tags'] = ['intro']
            elif any(kw in title for kw in ['战斗', '遭遇', '冲突', '攻击', '伏击']) or any(kw in title_lower for kw in ['battle', 'fight', 'combat', 'ambush', 'assault', 'skirmish']):
                current_scene['tags'] = ['combat', 'encounter']
            elif any(kw in title for kw in ['大厅', '地城', '教堂', '墓', '要塞', '堡垒', '塔', '神殿', '墓穴']) or any(kw in title_lower for kw in ['dungeon', 'temple', 'keep', 'fort', 'castle', 'tower', 'cathedral', 'crypt']):
                current_scene['tags'] = ['exploration', 'dungeon']
            elif any(kw in title for kw in ['逃出', '离开', '前往', '穿越', '旅行', '出发']) or any(kw in title_lower for kw in ['escape', 'depart', 'travel', 'journey', 'road', 'toward', 'leave']):
                current_scene['tags'] = ['transition']
            elif any(kw in title for kw in ['小镇', '村庄', '城市', '旅馆', '市场', '广场', '港口', '酒馆']) or any(kw in title_lower for kw in ['town', 'village', 'city', 'tavern', 'inn', 'market', 'harbor', 'square']):
                current_scene['tags'] = ['exploration', 'social']
            else:
                current_scene['tags'] = ['exploration']

        elif s.startswith('### ') and current_scene:
            sub_title = s.lstrip('# ')
            current_scene['subsections'].append({
                'title': sub_title,
                'line': i + 1,
                'tags': []
            })
            if any(kw in sub_title for kw in ['战斗', '遭遇', '陷阱', '推销', '巡逻']):
                current_scene['tags'].append('combat')

        elif s.startswith('#### ') and current_scene:
            # Sub-items (rooms within a dungeon)
            current_scene['subsections'].append({
                'title': s.lstrip('# '),
                'line': i + 1,
                'type': 'room'
            })

    # Save last scene
    if current_scene:
        current_scene['end_line'] = total_lines
        scenes.append(current_scene)

    # Calculate line counts
    for scene in scenes:
        scene['line_count'] = scene['end_line'] - scene['start_line'] + 1

    return {
        "filepath": filepath,
        "total_lines": total_lines,
        "scenes": scenes,
    }


def save_scene_index(module_name, index, output_dir='srd'):
    """
    保存场景索引到 srd/scenes_index.json
    支持同一模组的多个章节文件共存

    参数:
        module_name: str - 模组名
        index: dict - build_scene_index() 返回的结果
        output_dir: str - 输出目录

    返回:
        str: 保存路径
    """
    os.makedirs(output_dir, exist_ok=True)
    outpath = os.path.join(output_dir, 'scenes_index.json')

    # Load existing or create new
    existing = {}
    if os.path.exists(outpath):
        with open(outpath, 'r', encoding='utf-8') as f:
            try:
                existing = json.load(f)
            except json.JSONDecodeError:
                existing = {}

    # Store under module_name:filename to prevent overwrites
    filename = os.path.basename(index.get('filepath', 'unknown'))
    store_key = f'{module_name}:{filename}'
    existing[store_key] = index
    if '_current_scene' not in existing or existing['_current_scene'] is None:
        existing['_current_scene'] = None
    if '_current_module_file' not in existing:
        existing['_current_module_file'] = store_key

    with open(outpath, 'w', encoding='utf-8') as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    return outpath


def load_current_scene(filepath, scene_title):
    """
    加载指定场景的原文行范围

    参数:
        filepath: str - 章节文件路径
        scene_title: str - 场景标题

    返回:
        str: 该场景的原文文本，如未找到返回 None
    """
    index = build_scene_index(filepath)
    for scene in index['scenes']:
        if scene['title'] == scene_title:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            # Extract lines (0-indexed: start_line-1 to end_line)
            start = scene['start_line'] - 1
            end = scene['end_line']
            return ''.join(lines[start:end])

    return None


def load_scene_by_index(module_name=None, scene_index_path='srd/scenes_index.json'):
    """
    从已保存的场景索引中加载当前场景

    参数:
        module_name: str - 可选，用于显示日志
        scene_index_path: str - 索引文件路径

    返回:
        dict: {scene_title, content, chapter_file, tags} 或 None
    """
    if not os.path.exists(scene_index_path):
        return None

    with open(scene_index_path, 'r', encoding='utf-8') as f:
        index_data = json.load(f)

    current_scene = index_data.get('_current_scene')
    current_file_key = index_data.get('_current_module_file')

    if not current_scene or not current_file_key:
        return None

    chapter_data = index_data.get(current_file_key)
    if not chapter_data:
        return None

    filepath = chapter_data.get('filepath')
    if not filepath or not os.path.exists(filepath):
        return None

    for scene in chapter_data.get('scenes', []):
        if scene['title'] == current_scene:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            start = scene['start_line'] - 1
            end = scene['end_line']
            content = ''.join(lines[start:end])
            return {
                'scene_title': current_scene,
                'content': content,
                'line_count': scene['line_count'],
                'chapter_file': os.path.basename(filepath),
                'tags': scene['tags'],
            }

    return None


def set_current_scene(current_file_key, scene_title, scene_index_path='srd/scenes_index.json'):
    """
    设置当前场景，供下次 load_scene_by_index 使用

    参数:
        module_name: str
        scene_title: str
        scene_index_path: str
    """
    if os.path.exists(scene_index_path):
        with open(scene_index_path, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
    else:
        index_data = {}

    # Update both current scene and the module file it belongs to
    # module_name (now current_file_key) identifies the chapter file
    index_data['_current_scene'] = scene_title
    index_data['_current_module_file'] = current_file_key
    with open(scene_index_path, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
