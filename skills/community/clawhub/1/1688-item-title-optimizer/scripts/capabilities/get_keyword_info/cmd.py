#!/usr/bin/env python3
"""关键词信息获取 CLI 入口"""

import argparse
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error
from capabilities.get_keyword_info.service import get_keyword_info

COMMAND_NAME = "get_keyword_info"
COMMAND_DESC = "获取商品关键词信息（热搜词、曝光词等）"


def main():
    parser = argparse.ArgumentParser(description=COMMAND_DESC)
    parser.add_argument('--item_id', type=int, required=True, help='商品ID')
    parser.add_argument('--include_expo_words', action='store_true', default=True,
                        help='包含高曝光词（默认True）')
    parser.add_argument('--include_hot_words', action='store_true', default=True,
                        help='包含类目热搜词（默认True）')
    parser.add_argument('--custom_keywords', type=str, default=None,
                        help='自定义关键词，分号分隔，如"保温杯;不锈钢;便携"')
    args = parser.parse_args()

    try:
        result = get_keyword_info(
            item_id=args.item_id,
            include_expo_words=args.include_expo_words,
            include_hot_words=args.include_hot_words,
            custom_keywords=args.custom_keywords,
        )
        print_output(True, "✅ 关键词信息获取成功", result)
    except Exception as e:
        print_error(e)


if __name__ == "__main__":
    main()
