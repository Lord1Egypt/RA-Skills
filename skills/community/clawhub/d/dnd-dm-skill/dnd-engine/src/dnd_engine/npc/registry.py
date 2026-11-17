"""
NPC 状态注册表 — 管理 NPC 的长期记忆和状态

每个 NPC 在 registry 中有一条记录，包含：
- 知识卡路径
- 当前状态（HP、等级、装备）
- 记忆日志（每次对话后的关键事件摘要）
- 最后活动时间
"""

import os, json, time
from datetime import datetime


def get_registry_path(workspace=None):
    """获取 NPC registry 文件路径"""
    base = workspace or os.getcwd()
    return os.path.join(base, '.dnd', 'npc_registry.json')


def load_registry(workspace=None):
    """加载 NPC registry"""
    path = get_registry_path(workspace)
    if not os.path.exists(path):
        return {'npc_count': 0, 'npcs': {}}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_registry(registry, workspace=None):
    """保存 NPC registry"""
    path = get_registry_path(workspace)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)


def register_npc(npc_id, card_path, workspace=None):
    """注册一个新 NPC 到 registry"""
    registry = load_registry(workspace)
    now = datetime.now().isoformat()
    
    registry['npcs'][npc_id] = {
        'id': npc_id,
        'card_path': card_path,
        'state': {
            'hp_current': 0,
            'hp_max': 0,
            'level': 1,
            'xp': 0,
            'conditions': [],
            'inventory': [],
            'memory_log': []
        },
        'last_active': now,
        'created_at': now
    }
    registry['npc_count'] = len(registry['npcs'])
    save_registry(registry, workspace)
    return registry['npcs'][npc_id]


def add_memory(npc_id, event, workspace=None):
    """给 NPC 添加一条记忆（自动裁剪到最近 20 条）"""
    registry = load_registry(workspace)
    if npc_id not in registry['npcs']:
        return False
    
    now = datetime.now().isoformat()
    registry['npcs'][npc_id]['state']['memory_log'].append({
        'time': now,
        'event': event
    })
    # 只保留最近 20 条记忆
    if len(registry['npcs'][npc_id]['state']['memory_log']) > 20:
        registry['npcs'][npc_id]['state']['memory_log'] = \
            registry['npcs'][npc_id]['state']['memory_log'][-20:]
    
    registry['npcs'][npc_id]['last_active'] = now
    save_registry(registry, workspace)
    return True


def update_state(npc_id, state_updates, workspace=None):
    """更新 NPC 状态（HP、等级等）"""
    registry = load_registry(workspace)
    if npc_id not in registry['npcs']:
        return False
    
    for key, value in state_updates.items():
        registry['npcs'][npc_id]['state'][key] = value
    
    registry['npcs'][npc_id]['last_active'] = datetime.now().isoformat()
    save_registry(registry, workspace)
    return True


def get_npc(npc_id, workspace=None):
    """获取单个 NPC 信息"""
    registry = load_registry(workspace)
    return registry['npcs'].get(npc_id)


def list_npcs(workspace=None):
    """列出所有 NPC"""
    registry = load_registry(workspace)
    return registry['npcs']


def remove_npc(npc_id, workspace=None):
    """移除 NPC（死亡或离队）"""
    registry = load_registry(workspace)
    if npc_id in registry['npcs']:
        del registry['npcs'][npc_id]
        registry['npc_count'] = len(registry['npcs'])
        save_registry(registry, workspace)
        return True
    return False
