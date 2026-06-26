#!/usr/bin/env python3
"""标题热词优化 CLI 入口"""

import argparse
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error
from capabilities.optimize_title.service import optimize_title

COMMAND_NAME = "optimize_title"
COMMAND_DESC = "添加热词优化标题（规则版，快速）"


def main():
    parser = argparse.ArgumentParser(description=COMMAND_DESC)
    parser.add_argument('--item_id', type=int, required=True, help='商品ID')
    args = parser.parse_args()

    try:
        result = optimize_title(args.item_id)
        print_output(True, "✅ 标题优化完成（添加热词方式）", result)
    except Exception as e:
        print_error(e)


if __name__ == "__main__":
    main()
