#!/usr/bin/env python
"""
执行结果展示卡参数服务

汇总台账生成 route=batch-result-view 的卡片参数（钉钉文档「执行结果展示」：
进度展示 + 逐任务结果 + 应用到商品入口）。卡片参数只引用台账字段，
不内嵌图片 URL（组件按 item_id 自行取图渲染）。
"""

from _const import OP_LABELS
from _errors import ParamError
from _ledger import load_ledger, summary_stats


def build_result_card(base_dir: str = None, item_ids: list = None) -> dict:
    ledger = load_ledger(base_dir)
    tasks = ledger.get("tasks", [])

    if item_ids:
        wanted = {str(i).strip() for i in item_ids}
        tasks = [t for t in tasks if str(t.get("item_id")) in wanted]
        if not tasks:
            raise ParamError("台账中没有商品 ID 为 {} 的任务".format(", ".join(sorted(wanted))))

    if not tasks:
        raise ParamError("台账为空；请先运行 parse_tasks 创建批量任务")

    stats = summary_stats(ledger)

    # 可应用到商品的任务：执行成功、尚未应用（pending / failed / unknown 可重试）、且带商品 ID
    appliable = [
        t for t in tasks
        if str(t.get("status")) == "success"
        and str(t.get("item_id"))
        and str(t.get("apply_status")) in ("pending", "failed", "unknown")
    ]

    card = {
        "route": "batch-result-view",
        "batchId": ledger.get("batch_id"),
        "progress": {
            "total": stats["total"],
            "done": stats["done"],
            "success": stats["by_status"].get("success", 0),
            "failed": stats["by_status"].get("failed", 0),
            "skipped": stats["by_status"].get("skipped", 0),
        },
        "tasks": [
            {
                "taskId": t.get("task_id"),
                "itemId": t.get("item_id"),
                "itemTitle": t.get("item_title") or "",
                "op": t.get("op"),
                "opLabel": t.get("op_label") or OP_LABELS.get(t.get("op"), t.get("op")),
                "status": t.get("status"),
                "resultSummary": t.get("result_summary") or "",
                "applyStatus": t.get("apply_status"),
                "applyDetail": t.get("apply_detail") or "",
                "error": t.get("error") or "",
            }
            for t in tasks
        ],
        "appliableTaskIds": [t.get("task_id") for t in appliable],
    }

    return {
        "card": card,
        "batch_id": ledger.get("batch_id"),
        "appliable_count": len(appliable),
        "stats": stats,
    }
