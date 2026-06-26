"""
场景缓存与存档绑定模块

功能：
  - 写入存档时：将当前活跃的 _scene_cache_*.json 嵌入到存档数据中
  - 读取存档时：从存档数据中还原 _scene_cache_*.json 到工作目录
"""
import glob
import json
import os
import re
from datetime import datetime


def _find_active_cache():
    """
    扫描工作目录，找到当前活跃的场景缓存文件
    
    返回:
        tuple[str, dict | None]: (文件名, 缓存数据) 或 (None, None)
    """
    dnd_dir = os.getcwd()  # 假设工作目录是 DND 根目录
    pattern = os.path.join(dnd_dir, '_scene_cache_*.json')
    files = glob.glob(pattern)
    
    if not files:
        return None, None
    
    # 如果只有一个缓存文件，直接返回
    if len(files) == 1:
        fpath = files[0]
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return os.path.basename(fpath), data
        except (json.JSONDecodeError, IOError):
            return None, None
    
    # 如果有多个，选择 location 与 save_data 匹配的那个（靠后做的）
    # 按修改时间排序，最新的优先
    files.sort(key=lambda fp: os.path.getmtime(fp), reverse=True)
    for fpath in files:
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return os.path.basename(fpath), data
        except (json.JSONDecodeError, IOError):
            continue
    
    return None, None


def embed_scene_cache(save_data):
    """
    将当前活跃的场景缓存嵌入存档数据
    
    在 save_data 中添加：
      - "_scene_cache": 缓存文件完整内容 (dict)
      - "_scene_cache_file": 缓存文件名 (str)
    
    参数:
        save_data: dict - 即将写入的存档数据
    """
    cache_file, cache_data = _find_active_cache()
    if cache_data is None:
        # 没有活跃缓存，清除旧记录
        save_data.pop('_scene_cache', None)
        save_data.pop('_scene_cache_file', None)
        save_data.pop('_scene_cache_timestamp', None)
        return
    
    save_data['_scene_cache'] = cache_data
    save_data['_scene_cache_file'] = cache_file
    save_data['_scene_cache_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M')


def extract_scene_cache(save_data):
    """
    从存档数据中还原场景缓存到工作目录
    
    参数:
        save_data: dict - 已载入的存档数据
    
    返回:
        str | None: 还原的缓存文件名，若无缓存则返回 None
    """
    cache_data = save_data.get('_scene_cache')
    cache_file = save_data.get('_scene_cache_file')
    
    if cache_data is None or cache_file is None:
        return None
    
    dnd_dir = os.getcwd()
    fpath = os.path.join(dnd_dir, cache_file)
    
    with open(fpath, 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2)
    
    return cache_file


def get_cache_location(save_num=None, save_data=None):
    """
    从存档中获取场景缓存的位置信息（用于加载后展示）
    
    参数:
        save_num: int - 存档编号（可选）
        save_data: dict - 已载入的存档数据（可选）
    
    返回:
        str | None: 缓存中的地点名
    """
    data = save_data
    if data is None and save_num is not None:
        fp = os.path.join('saves', f'存档{save_num}.json')
        if os.path.exists(fp):
            with open(fp, 'r', encoding='utf-8-sig') as f:
                try:
                    data = json.load(f)
                except:
                    return None
    
    if data is None:
        return None
    
    cache = data.get('_scene_cache')
    if cache and isinstance(cache, dict):
        return cache.get('location')
    return None


def cleanup_orphan_caches():
    """
    清理工作目录中未绑定存档的孤立缓存文件
    （当所有存档都不引用某缓存文件时删除）
    """
    dnd_dir = os.getcwd()
    saves_dir = os.path.join(dnd_dir, 'saves')
    
    # 扫描所有缓存的引用
    referenced_files = set()
    if os.path.isdir(saves_dir):
        for fn in os.listdir(saves_dir):
            if not fn.endswith('.json'):
                continue
            fp = os.path.join(saves_dir, fn)
            try:
                with open(fp, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                cache_file = data.get('_scene_cache_file')
                if cache_file:
                    referenced_files.add(cache_file)
            except:
                continue
    
    # 清理未引用的缓存文件
    cleaned = 0
    pattern = os.path.join(dnd_dir, '_scene_cache_*.json')
    for fp in glob.glob(pattern):
        basename = os.path.basename(fp)
        if basename not in referenced_files:
            try:
                os.remove(fp)
                cleaned += 1
            except OSError:
                pass
    
    return cleaned


def split_cache(cache_data):
    """
    将场景缓存拆为索引部分（轻量常驻）和详情部分（按需加载）。
    
    索引部分（~200 tok）：房间编号、名称、连接关系、状态、感知线索。
    详情部分（~1K+ tok）：房间描述、NPC详情、物品列表。
    
    参数:
        cache_data: dict - 原始完整场景缓存
    
    返回:
        dict: {"index": dict, "details": dict}
    """
    if not cache_data or 'rooms' not in cache_data:
        return {"index": cache_data, "details": {}}
    
    index = {
        "location": cache_data.get('location', ''),
        "location_type": cache_data.get('location_type', ''),
        "total_rooms": cache_data.get('total_rooms', 0),
        "current_room": cache_data.get('current_room', ''),
        "exploration_pct": cache_data.get('exploration_pct', 0),
        "rooms": {},
    }
    
    details = {"rooms": {}}
    
    for rid, room in cache_data.get('rooms', {}).items():
        # Index: lightweight fields
        index['rooms'][rid] = {
            "name": room.get('name', ''),
            "floor": room.get('floor', ''),
            "status": room.get('status', 'unentered'),
            "connections": room.get('connections', []),
            "hints": room.get('hints', []),
            "explored": room.get('explored', False),
        }
        
        # Details: heavyweight fields (loaded on demand)
        detail = {}
        if 'npc' in room and room['npc']:
            detail['npc'] = room['npc']
        if 'feature' in room:
            detail['feature'] = room['feature']
        if 'items' in room:
            detail['items'] = room['items']
        if 'description' in room:
            detail['description'] = room['description']
        if detail:
            details['rooms'][rid] = detail
    
    if cache_data.get('known_but_hidden'):
        index['known_but_hidden'] = cache_data['known_but_hidden']
    if cache_data.get('remaining_content'):
        index['remaining_content'] = cache_data['remaining_content']
    
    return {"index": index, "details": details}


def get_room_detail(cache_data, room_id):
    """按需获取单个房间的详细信息"""
    if not cache_data or 'details' not in cache_data:
        return {}
    if 'rooms' not in cache_data['details']:
        return {}
    return cache_data['details']['rooms'].get(room_id, {})


def get_room_index(cache_data, room_id):
    """获取单个房间的索引信息"""
    if not cache_data or 'index' not in cache_data:
        return {}
    if 'rooms' not in cache_data['index']:
        return {}
    return cache_data['index']['rooms'].get(room_id, {})


def get_nearby_rooms(cache_data, room_id, depth=1):
    """获取指定房间附近 depth 层内的房间索引（用于场景切换时预加载）"""
    if not cache_data or 'index' not in cache_data:
        return {}
    
    index = cache_data['index']
    rooms = index.get('rooms', {})
    
    if room_id not in rooms:
        return {}
    
    nearby = {room_id: rooms[room_id]}
    current_layer = [room_id]
    
    for _ in range(depth):
        next_layer = []
        for rid in current_layer:
            if rid not in rooms:
                continue
            for conn in rooms[rid].get('connections', []):
                conn_id = conn.split('(')[0].strip() if '(' in conn else conn.split('→')[0].strip()
                # Extract room code (E#, V#, D#, etc.)
                import re
                m = re.match(r'([A-Z]+\d+)', conn_id)
                if m:
                    conn_id = m.group(1)
                if conn_id in rooms and conn_id not in nearby:
                    nearby[conn_id] = rooms[conn_id]
                    next_layer.append(conn_id)
        current_layer = next_layer
    
    return nearby

