#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inspect_poni.py — Inspect PONI files and detector inputs
inspect_poni.py — 检查 PONI 文件与探测器输入
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lib.inspect import main


if __name__ == "__main__":
    raise SystemExit(main())
