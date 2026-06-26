#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 环境检查
"""

import sys
import subprocess


def check_python_version():
    """检查 Python 版本"""
    version = sys.version_info
    print(f"Python 版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ 需要 Python 3.8 或更高版本")
        return False
    
    print("✅ Python 版本符合要求")
    return True


def check_requests():
    """检查 requests 库"""
    try:
        import requests
        print(f"✅ requests 已安装 (版本: {requests.__version__})")
        return True
    except ImportError:
        print("❌ requests 未安装")
        return False


def install_requests():
    """安装 requests 库"""
    print("\n正在安装 requests...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
        print("✅ requests 安装成功")
        return True
    except subprocess.CalledProcessError:
        print("❌ requests 安装失败，请手动执行: pip install requests")
        return False


def main():
    print("=" * 60)
    print("Python 环境检查")
    print("=" * 60)
    print()
    
    # 检查 Python 版本
    if not check_python_version():
        print("\n请安装 Python 3.8+：https://www.python.org/downloads/")
        return
    
    print()
    
    # 检查 requests
    if not check_requests():
        choice = input("\n是否自动安装 requests？(y/n): ").strip().lower()
        if choice == 'y':
            install_requests()
        else:
            print("请手动执行: pip install requests")
    
    print()
    print("=" * 60)
    print("✅ 环境检查完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
