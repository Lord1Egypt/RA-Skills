#!/usr/bin/env python3
"""
配置加载器
仅依赖 ~/.dingtalk/config.json 和 ~/.feishu/config.json
"""
import os
import json

def load_config():
    """加载主配置（返回空dict，实际配置由各自函数读取）"""
    return {}

def get_dingtalk_config(config=None):
    """获取钉钉配置路径"""
    return {"config_path": os.path.expanduser("~/.dingtalk/config.json")}

def get_feishu_config(config=None):
    """获取飞书配置（从 ~/.feishu/config.json 读取）"""
    feishu_path = os.path.expanduser("~/.feishu/config.json")
    if os.path.exists(feishu_path):
        with open(feishu_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}
