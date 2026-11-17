#!/usr/bin/env python3
"""多店铺绑定关系查询 CLI 入口"""

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error

from capabilities.get_bindlist.service import get_bindlist

COMMAND_NAME = "get_bindlist"
COMMAND_DESC = "获取当前用户的多店铺绑定关系及AK"

def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法查询绑定关系。\n\n运行: `cli.py configure YOUR_AK`",
                     {"data": {}})
        return

    try:
        result = get_bindlist()
        print_output(True, "多店铺绑定关系查询成功", {
            "data": result,
        })
    except Exception as e:
        print_error(e, {"data": {}})

if __name__ == "__main__":
    main()
