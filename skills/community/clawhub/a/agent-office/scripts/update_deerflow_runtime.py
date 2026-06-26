#!/usr/bin/env python3
"""Update the shared embedded DeerFlow runtime for Agent Office."""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from deerflow_runtime import ensure_deerflow_runtime


def main() -> int:
    info = ensure_deerflow_runtime(update=True)
    print("✅ DeerFlow 共享 runtime 已更新")
    print(f"   runtime: {info['runtime_root']}")
    print(f"   python:  {info['runtime_python']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
