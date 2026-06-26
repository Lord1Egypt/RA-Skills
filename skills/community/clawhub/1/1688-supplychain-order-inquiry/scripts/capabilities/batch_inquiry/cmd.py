#!/usr/bin/env python3
"""批量订单询盘 CLI 入口 -- 并行执行多个独立询盘任务"""

COMMAND_NAME = "batch_inquiry"
COMMAND_DESC = "批量订单询盘（并行执行多个询盘任务）"

import json
import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error
from capabilities.batch_inquiry.service import batch_inquiry


def _parse_tasks(args) -> list:
    """从 --tasks 或 --tasks-file 解析任务列表"""
    if args.tasks:
        raw = args.tasks
    elif args.tasks_file:
        if not os.path.isfile(args.tasks_file):
            raise ValueError("文件不存在: {}".format(args.tasks_file))
        with open(args.tasks_file, "r", encoding="utf-8") as f:
            raw = f.read()
    else:
        return None  # 由调用方处理

    try:
        tasks = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError("JSON 解析失败: {}".format(e))

    if not isinstance(tasks, list):
        raise ValueError("tasks 必须是 JSON 数组")

    return tasks


def main():
    parser = argparse.ArgumentParser(description="批量订单询盘 - 并行执行多个询盘任务")
    parser.add_argument("--tasks", "-t", default="",
                        help='JSON 字符串：任务数组，每个元素包含 order_ids(必填)、question(必填)、local_images(可选)、image_urls(可选)、orders_status(可选)')
    parser.add_argument("--tasks-file", "-f", default="",
                        help="JSON 文件路径（与 --tasks 二选一）")
    args = parser.parse_args()

    if not args.tasks and not args.tasks_file:
        parser.error("必须提供 --tasks 或 --tasks-file 其中之一")

    try:
        tasks = _parse_tasks(args)
        if tasks is None:
            parser.error("必须提供 --tasks 或 --tasks-file 其中之一")

        result = batch_inquiry(tasks=tasks)

        # 构建 markdown 摘要
        total_tasks = result.get("total_tasks", 0)
        success_count = result.get("success_count", 0)
        total_orders = result.get("total_orders_inquired", 0)
        elapsed = result.get("elapsed_seconds", 0)

        if success_count > 0:
            message = "批量询盘完成：{}/{} 成功，共 {} 个订单（耗时 {}s）".format(
                success_count, total_tasks, total_orders, elapsed)
        else:
            message = "批量询盘全部失败（{} 个任务），请检查参数后重试".format(total_tasks)

        output_data = {
            "total_tasks": total_tasks,
            "success_count": success_count,
            "fail_count": result.get("fail_count", 0),
            "total_orders_inquired": total_orders,
            "elapsed_seconds": elapsed,
            "results": result.get("results", []),
        }

        print_output(result.get("success", False), message, output_data)
    except KeyboardInterrupt:
        print_output(False, "用户中断操作", {})
    except Exception as e:
        print_error(e, {})


if __name__ == "__main__":
    main()
