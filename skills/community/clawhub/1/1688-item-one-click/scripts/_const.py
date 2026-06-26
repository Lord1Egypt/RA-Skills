#!/usr/bin/env python
"""
1688-item-one-click 全局常量
"""

import os
from pathlib import Path

# Skill 版本
SKILL_VERSION = "1.0.0"

# Skill 名称
SKILL_NAME = "1688-item-one-click"

# 后端 API 工具码
TOOL_CODE_BEFORE_CHECK = "tool_one_click_spi_before_check"
TOOL_CODE_EXECUTE = "tool_one_click_spi_execute"

# ── OpenClaw 配置文件路径──────────────────────────────────────────────────────
# 优先读取 OPENCLAW_CONFIG_DIR 环境变量，默认 ~/.openclaw
OPENCLAW_CONFIG_PATH: Path = Path(
    os.environ.get("OPENCLAW_CONFIG_DIR", Path.home() / ".openclaw")
) / "openclaw.json"
