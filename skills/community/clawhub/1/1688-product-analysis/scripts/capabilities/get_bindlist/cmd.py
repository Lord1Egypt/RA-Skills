#!/usr/bin/env python3
"""多店铺绑定列表查询 CLI 入口"""

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error
from capabilities.get_bindlist.service import get_bindlist

COMMAND_NAME = "get_bindlist"
COMMAND_DESC = "查询当前用户绑定的多店铺列表（含各店铺 loginId）"


def main():
    try:
        shops = get_bindlist()
        print_output(True, "绑定店铺查询成功", {"count": len(shops), "shops": shops})
    except Exception as e:
        print_error(e, {"count": 0, "shops": []})


if __name__ == "__main__":
    main()
