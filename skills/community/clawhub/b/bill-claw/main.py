#!/usr/bin/env python3
"""转发到 scripts/main.py，便于在项目根目录使用 `python main.py ...`。"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_TARGET = _ROOT / "scripts" / "main.py"

if not _TARGET.is_file():
    print(f"找不到 {_TARGET}", file=sys.stderr)
    sys.exit(1)

_SCRIPTS = str(_TARGET.parent)
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)
sys.argv[0] = str(_TARGET)
runpy.run_path(str(_TARGET), run_name="__main__")
