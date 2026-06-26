#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统级配置管理器 - 使用固定系统目录
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
    """
    获取系统级知识库路径
    
    Windows: C:/ProgramData/kb-data
    Linux/Mac: /usr/local/share/kb-data 或 ~/.local/share/kb-data (如果没有权限)
    """
    if os.name == 'nt':  # Windows
        # 使用 ProgramData 目录
        base_path = os.path.join(os.environ.get('PROGRAMDATA', 'C:/ProgramData'), 'kb-data')
    else:  # Linux/Mac
        # 尝试系统级目录
        system_path = '/usr/local/share/kb-data'
        user_path = os.path.expanduser('~/.local/share/kb-data')
        
        # 检查是否有系统级目录的写权限
        try:
            os.makedirs('/usr/local/share', exist_ok=True)
            test_file = '/usr/local/share/.kb_test'
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            base_path = system_path
        except (PermissionError, OSError):
            # 没有权限，使用用户目录
            base_path = user_path
    
    return base_path

def load_system_config() -> SystemConfig:
    """加载系统配置"""
    base_path = get_system_kb_path()
    
    # 确保目录存在
    os.makedirs(base_path, exist_ok=True)
    
    data_path = os.path.join(base_path, "chroma_db")
    documents_path = os.path.join(base_path, "documents")
    
    # 创建子目录
    os.makedirs(data_path, exist_ok=True)
    os.makedirs(documents_path, exist_ok=True)
    
    config = SystemConfig(
        shared_kb_path=base_path,
        data_path=data_path,
        documents_path=documents_path
    )
    
    # 保存配置文件
    config_file = os.path.join(base_path, "config.json")
    config_data = {
        "shared_kb_path": config.shared_kb_path,
        "data_path": config.data_path,
        "documents_path": config.documents_path,
        "collection_name": config.collection_name,
        "vector_dimension": config.vector_dimension
    }
    
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️ 保存配置文件失败: {e}")
    
    return config

def print_system_info():
    """打印系统信息"""
    config = load_system_config()
    
    print("📁 系统知识库路径:")
    print(f"   基础路径: {config.shared_kb_path}")
    print(f"   数据路径: {config.data_path}")
    print(f"   文档路径: {config.documents_path}")
    print()
    print("💡 所有skills自动使用此固定路径，无需额外配置")
    
    return config