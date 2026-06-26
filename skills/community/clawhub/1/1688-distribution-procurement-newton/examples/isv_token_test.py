#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ISV Token 测试脚本 — 通过 cli.py 调用 isv_token 命令

用法：
  python3 examples/isv_token_test.py
"""

import subprocess
import sys
import os

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ========== 配置 ==========
APP_KEY = "8884967"
EXPIRE_HOURS = "24"
FORCE_REFRESH = "true"   # true=强制刷新，忽略本地缓存
# ==========================

CLI = [sys.executable, os.path.join(_PROJECT_ROOT, "scripts", "cli.py")]


def run(desc, args):
    """执行 cli.py 命令并打印结果"""
    print("=" * 50)
    print(desc)
    print(f"命令: python3 scripts/cli.py {' '.join(args)}")
    print("=" * 50)
    result = subprocess.run(CLI + args, capture_output=True, text=True, cwd=_PROJECT_ROOT)
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip(), file=sys.stderr)
    print()


def main():
    print(f"APP_KEY: {APP_KEY}")
    print(f"FORCE_REFRESH: {FORCE_REFRESH}")
    print()

    # 1. 获取 token（强制刷新）
    run("1. 获取 ISV Token（强制刷新）", [
        "isv_token", "fetch",
        f"--app_key={APP_KEY}",
        f"--expire_hours={EXPIRE_HOURS}",
        f"--force_refresh={FORCE_REFRESH}",
    ])

    # 2. 查看 token 状态
    run("2. 查看 Token 状态", [
        "isv_token", "status",
        f"--app_key={APP_KEY}",
    ])

    # 3. 再次获取（不强制刷新，应命中缓存）
    run("3. 再次获取（应命中本地缓存）", [
        "isv_token", "fetch",
        f"--app_key={APP_KEY}",
        f"--expire_hours={EXPIRE_HOURS}",
        "--force_refresh=false",
    ])


if __name__ == "__main__":
    main()
