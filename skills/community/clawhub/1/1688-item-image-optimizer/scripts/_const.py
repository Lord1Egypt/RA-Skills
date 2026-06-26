#!/usr/bin/env python3
"""
1688-item-image-optimizer 全局常量
"""

import os
from pathlib import Path

# Skill 版本
SKILL_VERSION = "1.0.0"

# Skill 名称
SKILL_NAME = "1688-item-image-optimizer"

# 后端 API 工具码
TOOL_CODE = "1688_item_image_optimizer_interface"

# ── OpenClaw 配置文件路径──────────────────────────────────────────────────────
# 优先读取 OPENCLAW_CONFIG_DIR 环境变量，默认 ~/.openclaw
OPENCLAW_CONFIG_PATH: Path = Path(
    os.environ.get("OPENCLAW_CONFIG_DIR", Path.home() / ".openclaw")
) / "openclaw.json"
