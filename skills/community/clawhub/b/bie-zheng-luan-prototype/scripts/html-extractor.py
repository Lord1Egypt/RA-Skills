#!/usr/bin/env python3
"""
HTML页面结构提取器（入口脚本）
调用 html_extractor 包进行HTML原型深度解析

此文件作为兼容入口，实际功能由 html_extractor 包提供
"""

import sys
import os

# 确保能找到 html_extractor 包
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from html_extractor.main import main

if __name__ == "__main__":
    main()