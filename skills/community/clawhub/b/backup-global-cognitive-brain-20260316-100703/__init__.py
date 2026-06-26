# -*- coding: utf-8 -*-
"""
Global Cognitive Brain Skill for OpenClaw
全域認知系統 - 強制五層思考
"""

from .global_cognitive_brain import (
    init_memory,
    add_working_memory,
    store_event,
    update_fact,
    search_knowledge,
    extract_keywords,
    five_layer_thinking,
    select_skill,
    run,
    # Memory variables
    working_memory,
    episodic_memory,
    semantic_memory,
    meta_memory
)

__all__ = [
    'init_memory',
    'add_working_memory',
    'store_event',
    'update_fact',
    'search_knowledge',
    'extract_keywords',
    'five_layer_thinking',
    'select_skill',
    'run',
    'working_memory',
    'episodic_memory',
    'semantic_memory',
    'meta_memory'
]

__version__ = '1.0.0'
__skill_name__ = 'global_cognitive_brain'
__description__ = '全域持久腦 - 五層思考邏輯 + 自動記憶守護'
