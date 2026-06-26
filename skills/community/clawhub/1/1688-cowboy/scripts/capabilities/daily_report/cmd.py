#!/usr/bin/env python3
"""工作日报 CLI 入口 -- 查看牛仔的工作数据"""

COMMAND_NAME = "daily_report"
COMMAND_DESC = "查看工作日报（当日/历史）"

import os
import sys
import argparse
from datetime import date

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error

from capabilities.daily_report.service import get_daily_report, format_report_markdown


def main():
    parser = argparse.ArgumentParser(description="查看牛仔工作日报")
    parser.add_argument("--date", "-d", default="today",
                        help="查询日期：'today' 或 'YYYY-MM-DD'（默认 today）")
    args = parser.parse_args()

    try:
        # 参数校验
        query_date = args.date.strip()
        if query_date != "today":
            # 校验日期格式
            try:
                date.fromisoformat(query_date)
            except ValueError:
                print_output(False, "日期格式错误，请使用 'today' 或 'YYYY-MM-DD' 格式", {})
                return

        result = get_daily_report(query_date)
        markdown = format_report_markdown(result)

        print_output(True, markdown, result)
    except KeyboardInterrupt:
        print_output(False, "用户中断操作", {})
    except Exception as e:
        print_error(e, {})


if __name__ == "__main__":
    main()
