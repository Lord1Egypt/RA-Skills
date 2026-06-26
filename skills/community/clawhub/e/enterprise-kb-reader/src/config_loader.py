#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置加载器 - 只读查询器配置管理
"""

import os
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

@dataclass
class ReaderConfig:
    """只读查询器配置"""
    embedding_provider: str = "dashscope"
    embedding_model: str = "text-embedding-v3"
    embedding_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    embedding_api_key: str = ""
    
    retrieval_top_k: int = 5
    vector_threshold: float = 0.3
    keyword_threshold: float = 0.2
    final_threshold: float = 0.2
    
    milvus_uri: str = ""
    collection_name: str = "enterprise_kb"
    vector_dimension: int = 1024
    
    documents_dir: str = ""
    max_results: int = 10
    
    enable_rerank: bool = True
    rerank_model: str = "gte-rerank-v2"

def load_config(config_path: Optional[str] = None) -> ReaderConfig:
    """加载配置"""
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config.json"
    
    config = ReaderConfig()
    
    # 从文件加载配置
    if Path(config_path).exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
            
            # 更新配置
            for key, value in file_config.items():
                snake_key = camel_to_snake(key)
                if hasattr(config, snake_key):
                    setattr(config, snake_key, value)
        except Exception as e:
            print(f"⚠️ 配置文件加载失败: {e}")
    
    # 从环境变量获取API密钥
    if not config.embedding_api_key:
        if config.embedding_provider == "dashscope":
            config.embedding_api_key = os.getenv("DASHSCOPE_API_KEY", "")
        elif config.embedding_provider == "openai":
            config.embedding_api_key = os.getenv("OPENAI_API_KEY", "")
    
    return config

def camel_to_snake(name: str) -> str:
    """驼峰命名转下划线命名"""
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()