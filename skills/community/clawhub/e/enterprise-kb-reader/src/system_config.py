#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统级配置管理器 - kb-reader版本
"""

import os
import json
from dataclasses import dataclass

@dataclass
class SystemConfig:
    """系统知识库配置"""
    shared_kb_path: str = ""
    data_path: str = ""
    documents_path: str = ""
    collection_name: str = "enterprise_kb"
    vector_dimension: int = 1024

def get_system_kb_path() -> str:
    """获取系统级知识库路径"""
    if os.name == 'nt':  # Windows
        base_path = os.path.join(os.environ.get('PROGRAMDATA', 'C:/ProgramData'), 'kb-data')
    else:  # Linux/Mac
        system_path = '/usr/local/share/kb-data'
        user_path = os.path.expanduser('~/.local/share/kb-data')
        
        # 检查系统路径是否存在
        if os.path.exists(system_path):
            base_path = system_path
        else:
            base_path = user_path
    
    return base_path

def load_system_config() -> SystemConfig:
    """加载系统配置"""
    base_path = get_system_kb_path()
    
    if not os.path.exists(base_path):
        print(f"⚠️ 系统知识库目录不存在: {base_path}")
        print("请先运行 kb-manager setup 创建系统环境")
    
    data_path = os.path.join(base_path, "chroma_db")
    documents_path = os.path.join(base_path, "documents")
    
    return SystemConfig(
        shared_kb_path=base_path,
        data_path=data_path,
        documents_path=documents_path
    )