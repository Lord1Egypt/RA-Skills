#!/usr/bin/env python
"""
用户配置管理模块
存储用户的饭点、口味偏好、推荐数量等设置
"""
import json
import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".openclaw" / "skills" / "eleme-food-recommend"
CONFIG_FILE = CONFIG_DIR / "config.json"

# 默认配置
DEFAULT_CONFIG = {
    "cookie": "",
    "breakfast": "07:30",
    "lunch": "11:30",
    "dinner": "18:30",
    "flavor": "清淡",
    "recommend_count": 3,
    "location": {
        "latitude": "",
        "longitude": "",
        "address": ""
    }
}


def load_config():
    """加载配置"""
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_config(config):
    """保存配置"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def update_config(**kwargs):
    """更新配置"""
    config = load_config()
    config.update(kwargs)
    save_config(config)
    return config


def get_config(key=None):
    """获取配置项"""
    config = load_config()
    if key:
        return config.get(key)
    return config
