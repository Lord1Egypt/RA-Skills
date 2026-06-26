#!/usr/bin/env python
"""获取店铺维度数据 CLI 入口"""

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error

from capabilities.get_shop_data.service import get_shop_data

COMMAND_NAME = "get_shop_data"
COMMAND_DESC = "获取店铺维度数据（支付金额、买家数等）"

def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法查询店铺数据。\n\n请补充有效 AK 或检查鉴权配置后重试",
                     {"data": {}})
        return

    try:
        result = get_shop_data()
        print_output(True, "店铺数据查询成功", {"data": result})
    except Exception as e:
        print_error(e, {"data": {}})

if __name__ == "__main__":
    main()
