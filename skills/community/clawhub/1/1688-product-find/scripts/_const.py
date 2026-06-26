#!/usr/bin/env python3
"""
全局常量

仅存放纯常量定义，不包含运行时逻辑。
配置路径解析逻辑在 _auth.py 中实现。
"""

import os
from pathlib import Path

# Skill 版本
SKILL_VERSION = "1.7.0"

# ── Skill 根目录（基于 __file__ 绝对路径，不依赖 CWD）─────────────────────────
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))   # scripts/
SKILL_ROOT = SCRIPT_DIR.parent                                   # skill 根目录
