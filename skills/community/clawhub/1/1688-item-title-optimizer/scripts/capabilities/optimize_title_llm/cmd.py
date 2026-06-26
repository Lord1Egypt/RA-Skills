#!/usr/bin/env python3
"""标题 LLM 深度重写 CLI 入口"""

import argparse
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error
from capabilities.optimize_title_llm.service import optimize_title_llm

COMMAND_NAME = "optimize_title_llm"
COMMAND_DESC = "LLM深度重写优化标题（高质量，支持偏好）"


def main():
    parser = argparse.ArgumentParser(description=COMMAND_DESC)
    parser.add_argument('--item_id', type=int, required=True, help='商品ID')
    parser.add_argument('--preference', type=str, default=None,
                        help='用户偏好，如"加入防潮单词"')
    args = parser.parse_args()

    try:
        result = optimize_title_llm(args.item_id, args.preference)
        print_output(True, "✅ 标题优化完成（LLM深度重写）", result)
    except Exception as e:
        print_error(e)


if __name__ == "__main__":
    main()
