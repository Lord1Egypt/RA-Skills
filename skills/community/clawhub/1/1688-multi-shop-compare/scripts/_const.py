#!/usr/bin/env python3
"""1688-multi-shop-compare 全局常量"""

import os
from pathlib import Path

SKILL_VERSION = "1.0.0"

OPENCLAW_CONFIG_PATH: Path = Path(
    os.environ.get("OPENCLAW_CONFIG_DIR", Path.home() / ".openclaw")
) / "openclaw.json"
