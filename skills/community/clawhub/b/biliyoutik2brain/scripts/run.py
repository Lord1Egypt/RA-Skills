#!/usr/bin/env python3
"""BiliYouTik2Brain 技能入口包装器"""
import sys, os

# 让脚本能找到自身的模块
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SKILL_DIR)

from biliyoutik2brain.cli import main

if __name__ == "__main__":
    main()
