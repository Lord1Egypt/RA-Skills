#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
integrate_with_poni.py — Streaming post-PONI pyFAI integration runner
integrate_with_poni.py — 流式 PONI 后 pyFAI 积分执行器
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lib.integrate import main


if __name__ == "__main__":
    raise SystemExit(main())
