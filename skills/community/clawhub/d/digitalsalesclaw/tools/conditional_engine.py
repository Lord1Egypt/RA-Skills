#!/usr/bin/env python3
"""
DigitalSalesClaw - conditional_engine.py
[已合并至 engine.py]
保留本文件仅为向后兼容，新代码请使用 engine.py
"""
import json, subprocess, sys
from pathlib import Path

TOOLS_DIR = Path(__file__).parent
ENGINE = TOOLS_DIR / "engine.py"

if __name__ == "__main__":
    data = sys.stdin.read().strip() if not sys.stdin.isatty() else "{}"
    result = subprocess.run(
        ["python3", str(ENGINE)], input=data,
        capture_output=True, text=True, timeout=60,
        cwd=str(TOOLS_DIR)
    )
    print(result.stdout)
