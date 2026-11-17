#!/usr/bin/env python3
"""微信通知 CLI 入口"""

COMMAND_NAME = "wx_push"
COMMAND_DESC = "发送微信通知"

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error

from capabilities.wx_push.service import send_wx_push


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法发送微信通知。\n\n运行: `cli.py configure YOUR_AK`",
                     {"data": {}})
        return

    parser = argparse.ArgumentParser(description="微信通知")
    parser.add_argument("--text", "-x", required=True, help="微信通知内容（纯文本）")
    args = parser.parse_args()

    try:
        result = send_wx_push(args.text)
        print_output(True, "微信通知发送成功", {"data": result})
    except Exception as exc:
        print_error(exc, {"data": {}})


if __name__ == "__main__":
    main()
