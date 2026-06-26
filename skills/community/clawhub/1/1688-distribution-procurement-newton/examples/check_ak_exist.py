#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AK 配置检查 — 通过 configure/cmd.py 检测 AK 是否已配置
"""

import subprocess
import sys
import os

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    print("=" * 60)
    print("AK 配置检查")
    print("=" * 60)
    print()

    cmd = [sys.executable, os.path.join(_PROJECT_ROOT, "scripts", "capabilities", "configure", "cmd.py")]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=_PROJECT_ROOT)

    output = result.stdout.strip()
    if output:
        print(output)
    if result.stderr:
        print(result.stderr.strip(), file=sys.stderr)

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
