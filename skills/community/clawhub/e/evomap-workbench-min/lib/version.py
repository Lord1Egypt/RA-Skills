#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
版本标识 - 仅在功能调用时显示
"""

import sys

# 版本标识
VERSION = "v1.0.11"
NAME = "EvoMap WorkBench"
FULL_NAME = f"🧬 {NAME} {VERSION}"

# 显示控制
_show_version = False

def enable_version_display(enabled: bool = True):
    """启用/禁用版本显示"""
    global _show_version
    _show_version = enabled

def get_version_string() -> str:
    """获取版本字符串"""
    return FULL_NAME

def print_version():
    """打印版本信息"""
    if _show_version:
        print(FULL_NAME)

def with_version(func):
    """装饰器：在函数执行时显示版本"""
    def wrapper(*args, **kwargs):
        if _show_version:
            print(f"🧬 {NAME} {VERSION} - {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
