#!/usr/bin/env python3
"""图片制作高级版权限校验命令 — CLI 入口"""

COMMAND_NAME = "verify_permission"
COMMAND_DESC = "校验当前商家图片制作高级版权限（返回 isAi/digitalModel/faceFix）"

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error
from capabilities.verify_permission.service import verify_permission


def main():
    try:
        result = verify_permission()
        is_ai = bool(result.get("isAi"))
        digital_model = bool(result.get("digitalModel"))
        md = (
            f"✅ 权限校验完成：高级版={'是' if is_ai else '否'}，"
            f"数字模特={'是' if digital_model else '否'}"
        )
        print_output(True, md, {"data": result})
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
