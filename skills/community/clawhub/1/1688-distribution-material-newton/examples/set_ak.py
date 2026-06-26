#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AK 配置设置 — 通过 configure/cmd.py 设置 AK
"""

import subprocess
import sys
import os

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    print("=" * 60)
    print("AK 配置")
    print("=" * 60)
    print()
    print("获取 AK：打开 https://clawhub.1688.com 点击右上角钥匙🔑图标")
    print()

    ak = input("请输入 AK: ").strip()

    if not ak:
        print("\n❌ AK 不能为空")
        return

    cmd = [sys.executable, os.path.join(_PROJECT_ROOT, "scripts", "capabilities", "configure", "cmd.py"), ak]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=_PROJECT_ROOT)

    output = result.stdout.strip()
    if output:
        print()
        print(output)
    if result.stderr:
        print(result.stderr.strip(), file=sys.stderr)

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
