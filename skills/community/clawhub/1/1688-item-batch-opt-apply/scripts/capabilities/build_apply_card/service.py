#!/usr/bin/env python
"""
批量应用卡参数服务

把主 Agent 逐任务从执行技能拿到的应用参数（如 image-agent 的
prepare_image_apply data.card_params）按 item_id 粒度合并成
route=batch-apply 的单卡参数。每项默认不应用，由用户在卡片中
逐项勾选/反选后一次确认写入（写入仍由组件完成，CLI 不写商品）。
"""

import json

from _const import OP_LABELS
from _errors import ParamError
from _ledger import load_ledger, find_task, save_ledger, now_iso, summary_stats


def build_apply_card(
    items_json: str,
    base_dir: str = None,
) -> dict:
    """
    合并逐条目应用参数为批量应用卡。

    Args:
        items_json: JSON 数组，每元素形如
            {"task_id": "T001", "card_params": {...执行技能返回的单条目应用参数...}}
            card_params 原样透传给组件（含 offerId/imageType/updatedImages/
            currentImages/isWhiteList/productInfo/loginId/store_ref 等执行技能契约字段）。

    Returns:
        {"card": {...}, "updated_count": N, "task_ids": [...]}
        卡片回传后由 save_result 落账各任务 apply_status。
    """
    try:
        items = json.loads(items_json or "")
    except ValueError:
        raise ParamError("items 不是合法 JSON 数组，请按 SKILL.md 规定格式传参")
    if not isinstance(items, list) or not items:
        raise ParamError("items 必须是非空 JSON 数组（每元素含 task_id 与 card_params）")

    ledger = load_ledger(base_dir)

    entries, task_ids = [], []
    for i, it in enumerate(items, start=1):
        if not isinstance(it, dict):
            raise ParamError("第{}个元素不是 JSON 对象".format(i))
        card_params = it.get("card_params")
        if not isinstance(card_params, dict) or not card_params:
            raise ParamError(
                "第{}个元素缺少 card_params（请传执行技能返回的单条目应用参数原样 JSON）".format(i)
            )
        task = find_task(
            ledger,
            task_id=str(it.get("task_id") or "").strip() or None,
            item_id=str(it.get("item_id") or "").strip() or None,
            op=str(it.get("op") or "").strip() or None,
        )
        if str(task.get("status")) != "success":
            raise ParamError(
                "任务 {} 执行状态为 {}，只有执行成功的任务才能进入应用".format(
                    task.get("task_id"), task.get("status")
                )
            )
        task_ids.append(task.get("task_id"))
        if not task.get("item_id"):
            raise ParamError("素材任务不能应用到商品")
        if task.get("apply_status") not in ("pending", "failed", "unknown"):
            raise ParamError("该任务已应用、等待回执或已取消，不能重复发起应用")
        if task_ids.count(task.get("task_id")) > 1:
            raise ParamError("同一任务不能重复进入应用卡")
        entries.append({
            "taskId": task.get("task_id"),
            "itemId": task.get("item_id"),
            "itemTitle": task.get("item_title") or "",
            "op": task.get("op"),
            "opLabel": task.get("op_label") or OP_LABELS.get(task.get("op"), task.get("op")),
            # 执行技能契约字段原样透传，组件按其自有 schema 渲染与写入
            "applyParams": card_params,
        })

    card = {
        "route": "batch-apply",
        "batchId": ledger.get("batch_id"),
        "items": entries,
        # 每项默认不应用；确认语义由组件实现（全选/反选/逐项开关）
        "defaultApplied": False,
    }

    # 所有条目校验完后一次落盘，避免中途失败留下部分 requested。
    for tid in task_ids:
        task = find_task(ledger, task_id=tid)
        task["apply_status"] = "requested"
        task["updated_at"] = now_iso()
    save_ledger(ledger, base_dir)

    return {
        "card": card,
        "updated_count": len(entries),
        "task_ids": task_ids,
        "stats": summary_stats(ledger),
    }
