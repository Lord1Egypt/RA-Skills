#!/usr/bin/env python
"""获取商品概览统计 CLI 入口"""

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error

from capabilities.get_item_overview.service import get_item_overview

COMMAND_NAME = "get_item_overview"
COMMAND_DESC = "获取商品概览统计（商品总数、销售额等）"

def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法查询商品概览。\n\n请补充有效 AK 或检查鉴权配置后重试",
                     {"data": {}})
        return

    try:
        result = get_item_overview()
        print_output(True, "商品概览查询成功", {"data": result})
    except Exception as e:
        print_error(e, {"data": {}})

if __name__ == "__main__":
    main()