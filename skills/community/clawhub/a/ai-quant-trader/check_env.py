#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查Python环境
"""

import sys
import os

print("=" * 60)
print("Python环境检查")
print("=" * 60)

print(f"Python版本: {sys.version}")
print(f"Python路径: {sys.executable}")
print(f"工作目录: {os.getcwd()}")
print(f"Python路径列表: {sys.path[:3]}...")

print("\n检查基本模块:")
for module in ["json", "os", "sys", "datetime", "math"]:
    try:
        __import__(module)
        print(f"  ✅ {module}")
    except:
        print(f"  ❌ {module}")

print("\n检查数据科学模块:")
for module in ["pandas", "numpy"]:
    try:
        __import__(module)
        print(f"  ✅ {module}")
    except ImportError as e:
        print(f"  ❌ {module}: {e}")

print("\n检查AKShare:")
try:
    import akshare
    print(f"  ✅ akshare v{akshare.__version__}")
except ImportError as e:
    print(f"  ❌ akshare: {e}")

print("\n" + "=" * 60)
print("环境检查完成")
print("=" * 60)