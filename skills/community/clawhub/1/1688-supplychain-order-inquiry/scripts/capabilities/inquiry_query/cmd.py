#!/usr/bin/env python3
"""询盘结果查询 CLI 入口 -- 根据 taskId 查询商家回复"""

COMMAND_NAME = "inquiry_query"
COMMAND_DESC = "询盘结果查询（根据 taskId 查询商家回复）"

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error
from capabilities.inquiry_query.service import inquiry_query


def main():
    parser = argparse.ArgumentParser(description="询盘结果查询 - 根据 taskId 查询商家回复")
    parser.add_argument("--task-id", "-t", required=True,
                        help="询盘任务 ID（发起询盘时生成，必填）")
    args = parser.parse_args()

    try:
        result = inquiry_query(task_id=args.task_id)

        message = "询盘结果查询完成，耗时 {}s。".format(
            result.get("elapsed_seconds", ""),
        )
        output_data = {
            "result": result.get("result", {}),
            "elapsed_seconds": result.get("elapsed_seconds", 0),
        }
        print_output(True, message, output_data)
    except KeyboardInterrupt:
        print_output(False, "用户中断操作", {})
    except Exception as e:
        print_error(e, {})


if __name__ == "__main__":
    main()
