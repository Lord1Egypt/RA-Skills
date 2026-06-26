#!/usr/bin/env python3
"""1688招商活动查询 CLI入口"""

COMMAND_NAME = "1688_enroll_activity_query"
COMMAND_DESC = "查询1688招商活动列表"

import importlib
import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_raw
from _output import make_output, print_output, print_error
_service = importlib.import_module("capabilities.1688_enroll_activity_query.service")
query_enroll_activities = _service.query_enroll_activities


def main():
    if not get_ak_raw():
        print_output(make_output(
            success=False,
            markdown="❌ AK 未配置，无法查询活动。\n\n运行: `cli.py configure YOUR_AK`",
            data={"data": {}},
        ))
        return

    parser = argparse.ArgumentParser(description="1688招商活动查询")
    parser.add_argument("--pageNo", "-p", type=int, default=1, help="当前分页，默认1")
    parser.add_argument("--pageSize", "-s", type=int, default=10, help="分页大小，默认10")
    parser.add_argument("--keyword", "-k", type=str, default="", help="活动Id或名称")
    args = parser.parse_args()

    try:
        result = query_enroll_activities(args.pageNo, args.pageSize, args.keyword)
#         activities = result.get("data", [])
#         total = result.get("total", 0)

#         if not activities:
#             markdown = "未查询到符合条件的招商活动。"
#         else:
#             lines = [f"共找到 **{total}** 个活动（第 {result.get('pageNo', 1)} 页）：\n"]
#             for item in activities:
#                 activity_id = item.get("activityId", item.get("id", ""))
#                 activity_name = item.get("activityName", item.get("name", ""))
#                 lines.append(f"- **{activity_name}**（ID: {activity_id}）")
#             markdown = "\n".join(lines)

        print_output(make_output(success=True, data=result))
    except Exception as exc:
        print_error(exc, {"data": {}})


if __name__ == "__main__":
    main()
