#!/usr/bin/env python3
"""
配置文件加载器
从 config.env 加载路径配置
"""
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, 'config.env')
WORKSPACE_DIR = '~/.openclaw/workspace'

def load_config():
    """加载 config.env"""
    config = {}
    if not os.path.exists(CONFIG_FILE):
        # 不存在则新建（模板路径默认为 workspace）
        default_template = os.path.join(WORKSPACE_DIR, '教学文档模版')
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            f.write("# 课程目标达成情况分析表 - 配置文件\n")
            f.write(f"# 模板目录（请根据实际路径修改）\n")
            f.write(f"TEMPLATE_DIR={default_template}\n")
        print(f"⚠️ config.env 不存在，已新建默认配置")
        print(f"   默认模板路径: {default_template}")
        print("   请修改 config.env 中的 TEMPLATE_DIR 为实际路径后重新运行")
        sys.exit(1)

    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    return config

def get_template_dir(default=None):
    """获取模板目录"""
    config = load_config()
    template_dir = config.get('TEMPLATE_DIR')
    if template_dir:
        template_dir = os.path.expanduser(template_dir)
    if template_dir and os.path.isdir(template_dir):
        return template_dir
    return default

def get_output_dir(default=None):
    """获取输出目录"""
    config = load_config()
    return config.get('OUTPUT_DIR') or default
