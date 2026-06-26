#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
install_pyfai_env.py — Helper for checking Python and installing pyFAI environments
install_pyfai_env.py — 检查 Python 并安装 pyFAI 环境的辅助脚本
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lib.install_env import main


if __name__ == "__main__":
    raise SystemExit(main())
