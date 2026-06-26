#!/usr/bin/env python3
"""
config.py - 全局配置模块（避免跨脚本重复定义）

功能:
- 统一路径计算逻辑
- 支持跨系统/跨用户部署
- 所有脚本通过 import config 引用配置值
"""

import os

# 工作空间基础路径
WORKSPACE_BASE = os.path.expanduser("~/.openclaw")

# 当前技能名称（可动态调整）
SKILL_NAME = "daily-recorder-assistant"

# 当前技能目录路径
CURRENT_SKILL_PATH = os.path.join(WORKSPACE_BASE, "workspace", "skills", SKILL_NAME)

# 资源路径计算函数
def get_state_file_path():
    """返回 state.json 路径"""
    return os.path.join(CURRENT_SKILL_PATH, "state.json")

def get_reference_dir_path():
    """返回 references/目录路径"""
    return os.path.join(CURRENT_SKILL_PATH, "references")

def get_assets_dir_path():
    """返回 assets/目录路径"""
    return os.path.join(CURRENT_SKILL_PATH, "assets")

def get_template_file_path(template_name):
    """动态获取特定模板文件路径"""
    template_map = {
        "notes-template": os.path.join(get_assets_dir_path(), "notes-template.md"),
        "plan-template": os.path.join(get_assets_dir_path(), "plan-template.md")
    }
    return template_map.get(template_name, None)

# Notes 目录路径（固定）
NOTE_BASE_DIR = os.path.join(WORKSPACE_BASE, "workspace", "notes")
DAILY_RECORDER_SUBDIR = "daily-recorder"
PLAN_SUBDIR = "plans"

# References/Assets 目录导出常量
REFERENCE_DIR = get_reference_dir_path()
ASSETS_DIR = get_assets_dir_path()

# 默认频道配置（fallback value）
DEFAULT_CHANNEL = "feishu"

def get_daily_recorder_dir_path():
    """返回每日记录子目录，命名规范：YYYY-MM-DD-day_N.md"""
    return os.path.join(NOTE_BASE_DIR, DAILY_RECORDER_SUBDIR)
