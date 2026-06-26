#!/usr/bin/env python3
"""
88syt-skill 全局常量

所有模块统一从这里 import，禁止各模块自定义同名常量。
"""

# Skill 版本
SKILL_VERSION = "0.1.0"
SKILL_NAME = "88syt-skill"
SITE = "1688"

# ── OpenClaw 配置文件路径（唯一权威来源）──────────────────────────────────────
import os
from pathlib import Path

# 优先读取 OPENCLAW_CONFIG_DIR 环境变量，默认 ~/.openclaw
OPENCLAW_CONFIG_PATH: Path = Path(
    os.environ.get("OPENCLAW_CONFIG_DIR", Path.home() / ".openclaw")
) / "openclaw.json"

# 环境变量名称
ENV_AK_NAME = "SYT_API_KEY"
