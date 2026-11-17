#!/usr/bin/env python
"""
执行/应用结果落账服务

主 Agent 每处理完一个任务（执行完成、执行失败、应用回执到达）都调用一次，
把结果合并进台账对应任务。台账是「执行结果展示」与「Excel 导出」的唯一数据源，
未落账的结果不会出现在产物里。
"""

from _const import TASK_STATUSES, APPLY_STATUSES
from _errors import ParamError
from _ledger import load_ledger, find_task, update_task, summary_stats


def save_result(
    task_id: str = None,
    item_id: str = None,
    op: str = None,
    status: str = None,
    result_summary: str = None,
    result_images: list = None,
    apply_status: str = None,
    apply_detail: str = None,
    error: str = None,
    base_dir: str = None,
) -> dict:
    """
    落账单条任务结果。

    status/apply_status 只需传本次发生变化的字段；未传字段保持台账原值。
    result_images 为完整覆盖式更新（传入即替换），None 表示不动。
    """
    ledger = load_ledger(base_dir)
    task = find_task(ledger, task_id=task_id, item_id=item_id, op=op)

    updates = {}
    if status is not None:
        if status not in TASK_STATUSES:
            raise ParamError(
                "非法任务状态 {}；合法取值：{}".format(status, "/".join(TASK_STATUSES))
            )
        updates["status"] = status
    if apply_status is not None:
        if apply_status not in APPLY_STATUSES:
            raise ParamError(
                "非法应用状态 {}；合法取值：{}".format(apply_status, "/".join(APPLY_STATUSES))
            )
        updates["apply_status"] = apply_status
    if result_summary is not None:
        updates["result_summary"] = str(result_summary)
    if result_images is not None:
        if not isinstance(result_images, list):
            raise ParamError("result_images 必须是数组（图片 URL 或本地产物路径）")
        updates["result_images"] = [str(u) for u in result_images]
    if apply_detail is not None:
        updates["apply_detail"] = str(apply_detail)
    if error is not None:
        updates["error"] = str(error)
    if not updates:
        raise ParamError("本次调用没有传入任何要更新的字段（status/apply_status/result_summary/result_images/apply_detail/error 至少其一）")

    update_task(ledger, task, updates, base_dir)
    stats = summary_stats(ledger)

    return {
        "task_id": task.get("task_id"),
        "item_id": task.get("item_id"),
        "op": task.get("op"),
        "status": task.get("status"),
        "apply_status": task.get("apply_status"),
        "batch_stats": stats,
    }
