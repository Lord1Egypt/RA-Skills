#!/usr/bin/env python3
"""
Utility Functions - 工具函数

提供配置文件加载、过滤条件解析等通用工具函数。
"""

import os
import sys
from typing import Dict

import yaml


def parse_filters(filter_str: str) -> Dict:
    """解析过滤条件字符串"""
    if not filter_str:
        return {}

    filters = {}
    for item in filter_str.split(","):
        if ">=" in item:
            key, val = item.split(">=")
            filters[key.strip()] = f">={val.strip()}"
        elif "<=" in item:
            key, val = item.split("<=")
            filters[key.strip()] = f"<={val.strip()}"
        else:
            key, val = item.split("=")
            filters[key.strip()] = val.strip()

    return filters


def load_config(config_path: str = None) -> Dict:
    """加载配置文件"""
    default_config = {
        "chunking": {
            "max_chunk_size": 2000,
            "min_chunk_size": 100,
            "overlap": 200,
        },
        "processing": {
            "batch_size": 5,
            "embedding_batch_size": 32,
            "max_workers": 3,
        },
        "models": {
            "embedding": "BAAI/bge-small-zh-v1.5",
            "annotation": "dashscope-coding/qwen3.5-plus",
        },
        "storage": {
            "persist_directory": "./corpus/chroma",
            "checkpoint_dir": "./corpus/cache",
        },
        "memory": {
            "limit_mb": 2500,
        },
    }

    if config_path and os.path.exists(config_path):
        with open(config_path, encoding="utf-8") as f:
            user_config = yaml.safe_load(f)
            if user_config:
                # 合并配置
                for section in [
                    "chunking",
                    "processing",
                    "models",
                    "storage",
                    "memory",
                ]:
                    if section in user_config:
                        default_config[section].update(user_config[section])

    return default_config


def setup_sqlite3():
    """
    设置 SQLite3 版本兼容性

    ChromaDB 需要 sqlite3 >= 3.35.0
    尝试使用 pysqlite3-binary 作为替代
    """
    try:
        import pysqlite3.dbapi2 as sqlite3

        print("✅ 使用 pysqlite3-binary (SQLite3", sqlite3.sqlite_version, ")")
    except ImportError:
        pass  # 回退到系统 sqlite3

    try:
        import sqlite3

        if sqlite3.sqlite_version_info < (3, 35, 0):
            try:
                import pysqlite3 as sqlite3

                sys.modules["sqlite3"] = sqlite3
            except ImportError:
                print("❌ 错误：sqlite3 版本过低 (< 3.35.0)，ChromaDB 无法运行")
                print("   请安装 pysqlite3-binary: pip3 install pysqlite3-binary --user")
                print("   或升级系统 sqlite3 到 3.35.0+")
                sys.exit(1)
    except ImportError:
        pass
