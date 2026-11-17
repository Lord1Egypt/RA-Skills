#!/usr/bin/env python
"""
任务解析服务：把主 Agent 已结构化的任务 JSON 解析为标准条目，写入台账，
并产出任务确认卡（offer_select_card route=batch-task-confirm）参数。

任意输入（Excel 指定 sheet、任意列语义、素材文件夹等）**不走脚本解析**：
主 Agent 自行读取理解结构后产出标准任务数组经 --tasks 传入，脚本只做
校验与归一化，不做自然语言理解与列语义/文件配对猜测，避免解析幻觉。
"""

import os

from _const import (
    OP_LABELS,
    OP_ALIASES,
    SOURCE_CONTEXT,
    ledger_file,
)
from _errors import ParamError
from _ledger import (
    load_ledger,
    create_ledger,
    save_ledger,
    archive_ledger,
    next_task_id,
    now_iso,
)

_NUM_RE_STR = "纯数字"


def _norm_op(raw) -> str:
    s = str(raw or "").strip().lower()
    if s in OP_ALIASES:
        return OP_ALIASES[s]
    if s in OP_LABELS:
        return s
    base = s.split("(")[0].strip()
    if base in OP_ALIASES:
        return OP_ALIASES[base]
    if base in OP_LABELS:
        return base
    return ""


def _norm_item_id(raw) -> str:
    s = str(raw or "").strip()
    if s.endswith(".0") and s[:-2].isdigit():
        s = s[:-2]
    s = s.replace("，", "").replace(",", "")
    return s if (s.isdigit() and len(s) >= 6) else ""


def _norm_input_images(raw) -> list:
    """归一化输入图列表：接受单值或数组，去空保序（https:// 或本地路径均合法）。"""
    if raw is None:
        return []
    if isinstance(raw, str):
        raw = [raw]
    if not isinstance(raw, list):
        return []
    return [str(r).strip() for r in raw if str(r or "").strip()]


def _tasks_from_context_json(tasks_json: str) -> tuple:
    """
    --tasks JSON 数组 → 标准条目。字段：item_id/op/requirements/item_title/input_images。

    两类任务：
    - 商品任务：item_id + op（input_images 可选，作为参考图）
    - 素材任务：无 item_id，但必须提供 input_images（如 Excel 多列素材融合、
      文件夹配对等非标结构由主 Agent 理解后传入）；与 folder 来源同理，
      素材任务不进入应用环节。
    """
    import json

    try:
        arr = json.loads(tasks_json)
    except ValueError:
        raise ParamError("--tasks 不是合法 JSON 数组，请按 SKILL.md 规定格式传参")
    if not isinstance(arr, list):
        raise ParamError("--tasks 必须是 JSON 数组（每元素一个任务）")

    out, errors = [], []
    for i, row in enumerate(arr, start=1):
        if not isinstance(row, dict):
            errors.append("第{}个任务不是 JSON 对象".format(i))
            continue
        item_id = _norm_item_id(row.get("item_id") or row.get("itemId") or row.get("offerId"))
        input_images = _norm_input_images(
            row.get("input_images") or row.get("inputImages") or row.get("images")
        )
        # 素材任务可带 source_file（主 Agent 从文件夹读取时标注源文件，便于追溯）
        source_file = str(row.get("source_file") or row.get("file") or "").strip()
        op = _norm_op(row.get("op"))
        if not item_id and not input_images:
            errors.append(
                "第{}个任务缺少合法商品ID（{}）或输入图片（input_images）".format(i, _NUM_RE_STR)
            )
            continue
        if not op:
            errors.append(
                "第{}个任务优化项无法识别：{}（支持：{}）".format(
                    i, row.get("op"), "/".join(sorted(OP_LABELS.values()))
                )
            )
            continue
        out.append({
            "item_id": item_id,
            "op": op,
            "requirements": str(row.get("requirements") or row.get("备注") or "").strip(),
            "item_title": str(row.get("item_title") or row.get("title") or "").strip(),
            "input_images": input_images,
            "source_file": source_file,
        })
    return out, errors


def parse_tasks(
    tasks_json: str,
    replace: bool = False,
    base_dir: str = None,
    store_name: str = None,
) -> dict:
    """
    解析任务并写入台账。

    store_name 为当前操作店铺展示名（可选，主 Agent 从宿主店铺上下文/选店结果
    取得后传入，如 phoenix-pc 多店铺策略侧提供）；写入台账 store_name 字段，
    仅用于归档/导出产物文件名前缀，避免多店铺同会话运行时产物文件名重叠，
    不参与鉴权。未传时台账 store_name 为空，产物命名退化为无前缀形态。

    Returns:
        {
          "batch_id", "store_name", "ledger_path", "tasks": [台账条目],
          "new_count", "skip_duplicates", "warnings": [...],
          "confirm_card": {...}  # offer_select_card route=batch-task-confirm 参数
        }
    """
    if not tasks_json:
        raise ParamError("必须提供 --tasks（主 Agent 已结构化的任务 JSON 数组）")
    entries, errors = _tasks_from_context_json(tasks_json)
    warnings = list(errors)
    if not entries:
        raise ParamError(
            "没有解析出有效任务；" + "；".join(warnings[:5])
        )

    # ── 台账合并 ────────────────────────────────────────────────────────────
    # 开新批次（replace 或旧台账不存在/损坏）前先归档现存 tasks.json 为
    # tasks_<店铺前缀>_<旧batch_id>.json，防多批次/多店铺同会话运行时旧批次
    # 台账被覆盖；同批次追加（非 replace 且台账可读）不归档，仅在台账缺
    # store_name 时补写本次传入的店铺名（旧台账兼容）。
    store_backfilled = False
    if replace:
        archived = archive_ledger(base_dir)
        ledger = create_ledger(base_dir, store_name=store_name)
    else:
        try:
            ledger = load_ledger(base_dir)
            archived = None
            if store_name and not str(ledger.get("store_name") or "").strip():
                # 旧台账无店铺名时补写（需落盘，即使本次没有新增任务）
                ledger["store_name"] = str(store_name).strip()
                store_backfilled = True
        except Exception:
            archived = archive_ledger(base_dir)
            ledger = create_ledger(base_dir, store_name=store_name)

    def _dedup_key(t_or_e) -> tuple:
        # 有商品 ID 的任务按 (item_id, op) 判重；素材任务无商品 ID：
        # folder 来源按 (source_file, op)，context 来源（input_images 融合类）
        # 按 (input_images 序列, op)——同批多素材任务不能互相撞 key。
        item_id = str(t_or_e.get("item_id") or "")
        if item_id:
            return (item_id, str(t_or_e.get("op")))
        src = str(t_or_e.get("source_file") or "")
        if src:
            return (src, str(t_or_e.get("op")))
        return (tuple(t_or_e.get("input_images") or []), str(t_or_e.get("op")))

    existing = {_dedup_key(t) for t in ledger.get("tasks", [])}
    new_tasks, skip_count = [], 0
    now_tasks = ledger.setdefault("tasks", [])
    for e in entries:
        key = _dedup_key(e)
        if key in existing and not replace:
            skip_count += 1
            continue
        tid = next_task_id(ledger)
        task = {
            "task_id": tid,
            "item_id": e["item_id"],
            "item_title": e.get("item_title") or "",
            "op": e["op"],
            "op_label": OP_LABELS.get(e["op"], e["op"]),
            "requirements": e.get("requirements") or "",
            "input_images": e.get("input_images") or [],
            "source": SOURCE_CONTEXT,
            "source_file": e.get("source_file") or "",
            "status": "parsed",
            "apply_status": "pending",
            "result_summary": "",
            "result_images": [],
            "apply_detail": "",
            "error": "",
            "created_at": now_iso(),
            "updated_at": now_iso(),
        }
        # 先入 ledger 再分配下一个 task_id（next_task_id 按台账现有任务计数）
        now_tasks.append(task)
        new_tasks.append(task)
        existing.add(key)

    if new_tasks or store_backfilled:
        save_ledger(ledger, base_dir)
    else:
        ledger["updated_at"] = ledger.get("updated_at")

    # ── 确认卡参数 ──────────────────────────────────────────────────────────
    card_tasks = []
    for t in ledger.get("tasks", []):
        if str(t.get("status")) == "parsed":
            card_tasks.append(t)

    confirm_card = build_confirm_card(card_tasks)

    return {
        "batch_id": ledger.get("batch_id"),
        "store_name": ledger.get("store_name") or "",
        "ledger_path": os.path.abspath(ledger_file(base_dir)),
        "archived_ledger_path": os.path.abspath(archived) if archived else "",
        "tasks": new_tasks,
        "new_count": len(new_tasks),
        "skip_duplicates": skip_count,
        "warnings": warnings,
        "confirm_card": confirm_card,
    }


def build_confirm_card(tasks: list) -> dict:
    """任务确认卡参数（route=batch-task-confirm；组件侧按多选清单渲染）。"""
    return {
        "route": "batch-task-confirm",
        "batchSize": len(tasks),
        "tasks": [
            {
                "taskId": t["task_id"],
                "itemId": t["item_id"],
                "itemTitle": t.get("item_title") or "",
                "mainImage": "",
                "op": t["op"],
                "opLabel": t.get("op_label") or t["op"],
                "requirements": t.get("requirements") or "",
                "inputImages": t.get("input_images") or [],
            }
            for t in tasks
        ],
    }
