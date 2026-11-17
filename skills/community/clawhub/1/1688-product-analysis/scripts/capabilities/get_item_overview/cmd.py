#!/usr/bin/env python3
"""获取商品概览统计 CLI 入口"""

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error

from capabilities.get_item_overview.service import get_item_overview

COMMAND_NAME = "get_item_overview"
COMMAND_DESC = "获取商品概览统计（商品总数、销售额等）"


def main():
    try:
        result = get_item_overview()
        print_output(True, "商品概览查询成功", {"data": result})
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
