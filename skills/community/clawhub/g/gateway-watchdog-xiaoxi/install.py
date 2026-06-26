#!/usr/bin/env python3
"""
一键安装并启动 Gateway Watchdog
用户只需运行此脚本即可实现 7/24 运行
"""

import subprocess
import sys
import os
import urllib.request
from pathlib import Path

REPO_URL = "https://raw.githubusercontent.com/adminlove520/openclaw-gateway-watchdog-v2/main/gateway_watchdog.py"

def download_watchdog():
    """下载 gateway_watchdog.py"""
    script_path = Path(__file__).parent.resolve() / "gateway_watchdog.py"
    
    if script_path.exists():
        print(f"✅ gateway_watchdog.py 已存在")
        return script_path
    
    print("📥 正在下载 gateway_watchdog.py...")
    try:
        urllib.request.urlretrieve(REPO_URL, script_path)
        print(f"✅ 下载完成: {script_path}")
        return script_path
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return None

def main():
    print("=" * 50)
    print("🚀 OpenClaw Gateway 7/24 运行")
    print("=" * 50)
    
    # 1. 下载脚本
    script_path = download_watchdog()
    if not script_path:
        sys.exit(1)
    
    # 2. 启动 watchdog
    print("\n🚀 启动 Gateway Watchdog...")
    try:
        result = subprocess.run(
            [sys.executable, str(script_path), "start"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.returncode != 0 and result.stderr:
            print(result.stderr)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)
    
    print("\n✅ 完成！Gateway 将 7/24 运行")

if __name__ == "__main__":
    main()
