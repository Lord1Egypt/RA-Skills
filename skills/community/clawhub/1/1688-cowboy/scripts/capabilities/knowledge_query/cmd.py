#!/usr/bin/env python3
"""查询待完善知识 CLI 入口"""

COMMAND_NAME = "knowledge_query"
COMMAND_DESC = "查询待完善知识列表"

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error
from capabilities.knowledge_query.service import query_pending_knowledge


def main():
    parser = argparse.ArgumentParser(description="查询待完善知识列表", allow_abbrev=False)
    parser.add_argument("--page", "-p", type=int, default=1, help="页码（>=1，默认 1）")
    parser.add_argument("--page-size", type=int, default=10, help="每页条数（1~100，默认 10）")
    args = parser.parse_args()

    try:
        # 分页参数边界校验：与 transfer_inquiries 保持一致，防 AI 传入超大 page_size 拉大数据 / 压后端
        if args.page < 1:
            print_output(False, "页码 --page 必须 >= 1", {})
            return
        if args.page_size < 1 or args.page_size > 100:
            print_output(False, "每页大小 --page-size 必须在 1~100 之间", {})
            return

        result = query_pending_knowledge(page=args.page, page_size=args.page_size)
        print_output(True, result["markdown"], result["data"])
    except KeyboardInterrupt:
        print_output(False, "用户中断操作", {})
    except Exception as e:
        print_error(e, {})


if __name__ == "__main__":
    main()
