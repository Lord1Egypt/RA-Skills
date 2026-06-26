#!/usr/bin/env python3
"""转人工询盘查询 CLI 入口 -- 翻页查看指定日期的转人工询盘记录"""

COMMAND_NAME = "transfer_inquiries"
COMMAND_DESC = "查询转人工询盘记录（指定日期、分页）"

import os
import sys
import argparse
from datetime import date

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error

from capabilities.transfer_inquiries.service import (
    query_transfer_inquiries,
    format_inquiries_markdown,
)


def main():
    parser = argparse.ArgumentParser(
        description="查询转人工询盘记录（指定日期、分页）",
        allow_abbrev=False,
    )
    parser.add_argument("--date", "-d", default="today",
                        help="查询日期：'today' 或 'YYYY-MM-DD'（默认 today）")
    parser.add_argument("--page-num", "-p", type=int, default=1,
                        help="页码（>=1，默认 1）")
    parser.add_argument("--page-size", "-s", type=int, default=10,
                        help="每页大小（1~100，默认 10）")
    args = parser.parse_args()

    try:
        # 日期格式校验
        query_date = args.date.strip()
        if query_date != "today":
            try:
                date.fromisoformat(query_date)
            except ValueError:
                print_output(False, "日期格式错误，请使用 'today' 或 'YYYY-MM-DD' 格式", {})
                return

        # 分页参数边界校验
        if args.page_num < 1:
            print_output(False, "页码 --page-num 必须 >= 1", {})
            return
        if args.page_size < 1 or args.page_size > 100:
            print_output(False, "每页大小 --page-size 必须在 1~100 之间", {})
            return

        result = query_transfer_inquiries(
            date=query_date,
            page_num=args.page_num,
            page_size=args.page_size,
        )
        markdown = format_inquiries_markdown(result)

        print_output(True, markdown, result)
    except KeyboardInterrupt:
        print_output(False, "用户中断操作", {})
    except Exception as e:
        print_error(e, {})


if __name__ == "__main__":
    main()
