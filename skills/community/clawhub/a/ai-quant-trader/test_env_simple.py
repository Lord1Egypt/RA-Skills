#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单环境测试
"""

import sys
import os

print("=" * 60)
print("Python环境测试")
print("=" * 60)

# 基本信息
print(f"Python版本: {sys.version}")
print(f"Python路径: {sys.executable}")
print(f"工作目录: {os.getcwd()}")

# 测试导入
print("\n测试模块导入:")
modules = ["json", "datetime", "math", "os", "sys"]

for module in modules:
    try:
        __import__(module)
        print(f"  ✅ {module}")
    except:
        print(f"  ❌ {module}")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)