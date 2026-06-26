#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮件配置加载模块
"""

import os
import json
import sys

# 外部配置路径（不会被 skill 更新覆盖）
EXTERNAL_CONFIG_DIR = os.path.expanduser("~/.openclaw/config")
EXTERNAL_CONFIG_FILE = os.path.join(EXTERNAL_CONFIG_DIR, "ai-news-email.json")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.getcwd()
USER_CONFIG_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "user_config") if SCRIPT_DIR else os.getcwd()
CONFIG_FILE = os.path.join(USER_CONFIG_DIR, "email_config.json") if USER_CONFIG_DIR else ""
DEFAULT_CONFIG_FILE = os.path.join(SCRIPT_DIR, "email_config.json.default") if SCRIPT_DIR else ""


def ensure_external_config():
    """确保外部配置文件存在，如果不存在则自动创建"""
    if os.path.exists(EXTERNAL_CONFIG_FILE):
        return False
    
    os.makedirs(EXTERNAL_CONFIG_DIR, exist_ok=True)
    
    template = None
    if os.path.exists(DEFAULT_CONFIG_FILE):
        try:
            with open(DEFAULT_CONFIG_FILE, 'r', encoding='utf-8') as f:
                template = json.load(f)
        except:
            pass
    
    if template:
        try:
            if 'smtp_config' in template:
                template['smtp_config']['enabled'] = False
            if 'recipient_config' in template:
                template['recipient_config']['enabled'] = False
            
            with open(EXTERNAL_CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(template, f, ensure_ascii=False, indent=2)
            return True
        except:
            pass
    
    return False


def load_email_config():
    """加载邮件配置（优先级：外部配置 > user_config > 默认配置）"""
    
    if not os.path.exists(EXTERNAL_CONFIG_FILE):
        ensure_external_config()
    
    if os.path.exists(EXTERNAL_CONFIG_FILE):
        try:
            with open(EXTERNAL_CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    
    if CONFIG_FILE and os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    
    return None
    
    # 3. 读取默认配置
    if os.path.exists(DEFAULT_CONFIG_FILE):
        try:
            with open(DEFAULT_CONFIG_FILE, 'r', encoding='utf-8') as f:
                print("[INFO] 使用默认邮件配置")
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] 无法加载默认配置: {e}")
            return None
    
    return None


if __name__ == "__main__":
    config = load_email_config()
    print("邮件配置:", config)