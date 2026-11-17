#!/usr/bin/env python3
"""强制使用 workspace 版的入口包装器"""
import sys, os

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
# 把 workspace 放在 sys.path 最前面，覆盖任何 skill 版
sys.path.insert(0, os.path.dirname(WORKSPACE))

from biliyoutik2brain.cli import main

if __name__ == "__main__":
    sys.argv = [sys.argv[0]] + sys.argv[1:]
    main()
