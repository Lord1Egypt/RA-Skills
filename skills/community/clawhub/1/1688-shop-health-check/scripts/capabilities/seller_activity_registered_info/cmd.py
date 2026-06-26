#!/usr/bin/env python3
"""商家活动参与信息查询 CLI 入口"""

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error

from capabilities.seller_activity_registered_info.service import get_activity_registered_info

COMMAND_NAME = "seller_activity_registered_info"
COMMAND_DESC = "获取商家近 30 天活动参与及效果数据"

def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法查询活动数据。\n\n运行: `cli.py configure YOUR_AK`",
                     {"data": {}})
        return

    parser = argparse.ArgumentParser(description="商家近 30 天活动参与信息查询（商家身份由 AK 自动识别，无需提供 user_id）")
    parser.parse_args()

    try:
        result = get_activity_registered_info()
        print_output(True, "活动参与信息查询成功", {
            "data": result,
        })
    except Exception as e:
        print_error(e, {"data": {}})

if __name__ == "__main__":
    main()
