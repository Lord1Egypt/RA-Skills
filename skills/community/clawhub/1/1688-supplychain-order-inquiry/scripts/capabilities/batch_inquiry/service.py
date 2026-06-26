# -*- coding: utf-8 -*-
"""
批量订单询盘能力实现

使用 ProcessPoolExecutor 并行执行多个独立的 inquiry_send 任务，
一次性返回全部询盘结果。
"""

import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Dict, Any, List

from _errors import ParamError
from capabilities.inquiry_send.service import inquiry_send


_MAX_TASKS = 10
_MAX_WORKERS_CAP = 5


def _execute_single(index: int, task: dict) -> dict:
    """
    执行单个询盘任务的包装函数

    成功返回完整结果，失败返回错误信息，绝不抛出异常。
    """
    order_ids_raw = task.get("order_ids", [])
    if isinstance(order_ids_raw, str):
        order_ids = [oid.strip() for oid in order_ids_raw.split(",") if oid.strip()]
    elif isinstance(order_ids_raw, list):
        order_ids = [str(oid).strip() for oid in order_ids_raw if str(oid).strip()]
    else:
        order_ids = []

    question = task.get("question", "")
    local_images = task.get("local_images")
    image_urls = task.get("image_urls")
    orders_status = task.get("orders_status")

    if not order_ids:
        return {
            "index": index,
            "success": False,
            "order_count": 0,
            "suc": False,
            "errorMsg": "参数错误: order_ids 为空",
        }

    if not question or not question.strip():
        return {
            "index": index,
            "success": False,
            "order_count": len(order_ids),
            "suc": False,
            "errorMsg": "参数错误: question 不能为空",
        }

    try:
        result = inquiry_send(
            order_ids=order_ids,
            question=question,
            local_images=local_images,
            image_urls=image_urls,
            orders_status=orders_status,
        )

        return {
            "index": index,
            "success": True,
            "order_count": len(order_ids),
            "suc": result.get("suc", False),
            "errorMsg": result.get("errorMsg", ""),
            "elapsed_seconds": result.get("elapsed_seconds", 0),
        }
    except Exception as e:
        return {
            "index": index,
            "success": False,
            "order_count": len(order_ids),
            "suc": False,
            "errorMsg": str(e),
        }


def batch_inquiry(tasks: List[dict], max_workers: int = 5) -> Dict[str, Any]:
    """
    批量并行询盘主函数

    Args:
        tasks: 任务列表，每个任务包含 order_ids 和 question（必填）
        max_workers: 最大并行进程数（默认5，上限5）

    Returns:
        聚合结果 dict
    """
    if not tasks:
        raise ParamError("任务列表不能为空")

    if not isinstance(tasks, list):
        raise ParamError("tasks 必须是数组")

    if len(tasks) > _MAX_TASKS:
        raise ParamError("单次最多 {} 个任务，当前 {} 个".format(_MAX_TASKS, len(tasks)))

    # 校验每个 task 的必填字段
    for i, task in enumerate(tasks):
        if not isinstance(task, dict):
            raise ParamError("第 {} 个任务格式错误，必须是对象".format(i + 1))
        order_ids_raw = task.get("order_ids", [])
        has_order_ids = bool(order_ids_raw)
        if not has_order_ids:
            raise ParamError("第 {} 个任务缺少 order_ids 字段".format(i + 1))
        if not task.get("question", "").strip():
            raise ParamError("第 {} 个任务缺少 question 字段".format(i + 1))

    # 限制并发数
    effective_workers = min(len(tasks), max_workers, _MAX_WORKERS_CAP)

    print("[batch_inquiry] 启动 {} 个任务，并行进程数: {}".format(
        len(tasks), effective_workers), file=sys.stderr)

    start_time = time.time()

    # 使用索引槽位保持结果顺序
    results = [None] * len(tasks)

    with ProcessPoolExecutor(max_workers=effective_workers) as executor:
        future_to_index = {}
        for i, task in enumerate(tasks):
            future = executor.submit(_execute_single, i, task)
            future_to_index[future] = i

        for future in as_completed(future_to_index):
            result = future.result()
            idx = result["index"]
            results[idx] = result

            status = "OK" if result["success"] else "FAIL"
            print("[batch_inquiry] 任务 {}/{} 完成 [{}]: orders={}".format(
                idx + 1, len(tasks), status, result.get("order_count", 0)
            ), file=sys.stderr)

    elapsed = round(time.time() - start_time, 1)

    success_count = sum(1 for r in results if r and r["success"])
    fail_count = len(tasks) - success_count
    total_orders = sum(r.get("order_count", 0) for r in results if r)

    print("[batch_inquiry] 全部完成: {}/{} 成功, 共 {} 个订单, 耗时 {:.1f}s".format(
        success_count, len(tasks), total_orders, elapsed), file=sys.stderr)

    return {
        "success": success_count > 0,
        "total_tasks": len(tasks),
        "success_count": success_count,
        "fail_count": fail_count,
        "total_orders_inquired": total_orders,
        "elapsed_seconds": elapsed,
        "results": results,
    }
