#!/usr/bin/env python3
"""
任务台账（ledger）读写层

台账文件：1688-item-batch-opt-apply/tasks.json（位于当前工作目录，目录名与技能名
一致以与其他技能产物隔离），结构：
{
  "version": 1,
  "batch_id": "<批次ID，parse_tasks 时生成>",
  "store_name": "<店铺展示名（parse_tasks --store_name 传入，可为空；仅用于产物文件名前缀）>",
  "created_at": "<ISO8601>",
  "updated_at": "<ISO8601>",
  "tasks": [
    {
      "task_id": "T001",
      "item_id": "1078187515442",
      "item_title": "",
      "op": "main_img_opt",
      "requirements": "",
      "source": "context",
      "status": "parsed",          # 见 _const.TASK_STATUSES
      "apply_status": "pending",   # 见 _const.APPLY_STATUSES
      "result_summary": "",        # 执行结果一句话摘要
      "result_images": [],         # 执行产物图 URL / 本地产物路径
      "apply_detail": "",          # 应用回执自然语言摘要
      "error": "",                 # 失败原因（自然语言）
      "created_at": "...",
      "updated_at": "..."
    }, ...
  ]
}

约定：
- 只允许本模块读写台账；cmd/service 不直接 open()。
- 任务按 task_id 定位；task_id 由 parse_tasks 分配（T001 起，批次内自增），
  save_result/build_apply_card 只按 task_id 或 (item_id, op) 唯一定位。
"""

import json
import os
import time
from datetime import datetime, timezone, timedelta

from _const import (
    LEDGER_VERSION,
    TASK_STATUSES,
    APPLY_STATUSES,
    ledger_file,
    ledger_dir,
    store_file_prefix,
)
from _errors import LedgerError, ParamError

# 东八区时间戳
_TZ = timezone(timedelta(hours=8))


def _now() -> str:
    return datetime.now(_TZ).strftime("%Y-%m-%dT%H:%M:%S+08:00")


# 公共时间戳工具（capability 构造台账条目时使用，与台账内部保持同一时区口径）
now_iso = _now


def load_ledger(base_dir: str = None) -> dict:
    """读取台账；不存在时抛 LedgerError（台账必须由 parse_tasks 创建）。"""
    path = ledger_file(base_dir)
    if not os.path.isfile(path):
        raise LedgerError(
            "未找到任务台账（1688-item-batch-opt-apply/tasks.json）。请先运行 parse_tasks 创建批量任务后再执行本命令。"
        )
    try:
        with open(path, "r", encoding="utf-8") as f:
            ledger = json.load(f)
    except (OSError, ValueError) as exc:
        raise LedgerError("任务台账文件损坏或不可读，请重新运行 parse_tasks 重建台账")
    if not isinstance(ledger, dict) or not isinstance(ledger.get("tasks"), list):
        raise LedgerError("任务台账结构异常，请重新运行 parse_tasks 重建台账")
    if ledger.get("version") != LEDGER_VERSION:
        raise LedgerError("任务台账版本不兼容，请重新运行 parse_tasks 重建台账")
    return ledger


def save_ledger(ledger: dict, base_dir: str = None):
    """原子写回台账（临时文件 + rename）。"""
    path = ledger_file(base_dir)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    ledger["updated_at"] = _now()
    tmp_path = path + ".tmp"
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(ledger, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, path)
    except OSError as exc:
        raise LedgerError("任务台账写入失败：{}".format(exc))


def create_ledger(base_dir: str = None, store_name: str = None) -> dict:
    """新建空台账（parse_tasks 用）。

    store_name 为当前操作店铺展示名（主 Agent 从宿主店铺上下文/选店结果取得，
    可为空）；仅作为台账元数据与后续归档/导出文件名的店铺前缀，不参与鉴权。
    """
    return {
        "version": LEDGER_VERSION,
        "batch_id": "B{}{}".format(
            time.strftime("%Y%m%d%H%M%S"), os.getpid() % 1000
        ),
        "store_name": str(store_name or "").strip(),
        "created_at": _now(),
        "updated_at": _now(),
        "tasks": [],
    }


def archive_ledger(base_dir: str = None):
    """归档现存台账（parse_tasks 开新批次前调用），防多批次/多店铺产物互相覆盖。

    把 tasks.json 重命名为 tasks_<店铺前缀>_<旧batch_id>.json（店铺名取自旧台账
    store_name 字段；无店铺名时退化为 tasks_<旧batch_id>.json，与旧版兼容）；
    旧台账读不出 batch_id 时用时间戳命名；归档名也被占用时自增序号。
    tasks.json 不存在时返回 None，任何失败都静默返回 None（归档失败不阻断新批次创建）。
    """
    path = ledger_file(base_dir)
    if not os.path.isfile(path):
        return None
    old_batch = ""
    old_store = ""
    try:
        with open(path, "r", encoding="utf-8") as f:
            _old = json.load(f)
        old_batch = str(_old.get("batch_id") or "")
        old_store = store_file_prefix(_old.get("store_name"))
    except Exception:
        old_batch = ""
    ident = old_batch or time.strftime("%Y%m%d%H%M%S")
    stem = "tasks_{}_{}".format(old_store, ident) if old_store else "tasks_{}".format(ident)
    archive_dir = os.path.dirname(path)
    candidate = os.path.join(archive_dir, stem + ".json")
    seq = 1
    while os.path.exists(candidate):
        seq += 1
        candidate = os.path.join(archive_dir, "{}_{}.json".format(stem, seq))
    try:
        os.replace(path, candidate)
    except OSError:
        return None
    return candidate


def next_task_id(ledger: dict) -> str:
    """批次内自增 task_id：T001、T002…（跳过用户置为 skipped 的也占号）。"""
    max_no = 0
    for t in ledger.get("tasks", []):
        tid = str(t.get("task_id") or "")
        if tid.startswith("T") and tid[1:].isdigit():
            max_no = max(max_no, int(tid[1:]))
    return "T{:03d}".format(max_no + 1)


def append_tasks(ledger: dict, tasks: list) -> dict:
    """追加任务条目（已含完整字段），并写回时间戳。"""
    now = _now()
    for t in tasks:
        t["created_at"] = now
        t["updated_at"] = now
    ledger.setdefault("tasks", []).extend(tasks)
    return ledger


def _norm_id(v) -> str:
    return str(v or "").strip()


def find_task(ledger: dict, task_id: str = None, item_id: str = None, op: str = None) -> dict:
    """按 task_id 唯一定位；缺 task_id 时按 (item_id, op) 唯一定位（多命中抛错）。"""
    tasks = ledger.get("tasks", [])
    tid = _norm_id(task_id)
    if tid:
        for t in tasks:
            if str(t.get("task_id")) == tid:
                return t
        raise ParamError("台账中不存在 task_id={} 的任务".format(tid))
    iid = _norm_id(item_id)
    opk = _norm_id(op)
    if not iid or not opk:
        raise ParamError("定位任务必须提供 --task_id，或同时提供 --item_id 与 --op")
    hits = [t for t in tasks
            if _norm_id(t.get("item_id")) == iid and _norm_id(t.get("op")) == opk]
    if len(hits) == 1:
        return hits[0]
    if not hits:
        raise ParamError("台账中不存在 item_id={} 且 op={} 的任务".format(iid, opk))
    raise ParamError(
        "item_id={} 且 op={} 命中 {} 条任务，无法唯一定位，请改用 --task_id".format(
            iid, opk, len(hits)
        )
    )


def check_task_status(task: dict, expected: tuple) -> dict:
    """校验任务当前状态在允许集合内（用于 save_result / build_apply_card 防呆）。"""
    status = str(task.get("status") or "")
    if status not in expected:
        raise LedgerError(
            "任务 {} 当前状态为 {}，不满足本命令前置状态（{}）；请先完成上一环节".format(
                task.get("task_id"), status or "未知", "/".join(expected)
            )
        )
    return task


def update_task(ledger: dict, task: dict, updates: dict, base_dir: str = None):
    """合并更新单条任务字段并落盘。updates 中的 None 跳过（不覆盖）。"""
    for k, v in (updates or {}).items():
        if v is None:
            continue
        if k == "status" and v not in TASK_STATUSES:
            raise ParamError("非法任务状态：{}".format(v))
        if k == "apply_status" and v not in APPLY_STATUSES:
            raise ParamError("非法应用状态：{}".format(v))
        task[k] = v
    task["updated_at"] = _now()
    save_ledger(ledger, base_dir)


def summary_stats(ledger: dict) -> dict:
    """批次统计：按执行状态/应用状态计数，供卡片与导出复用。"""
    tasks = ledger.get("tasks", [])
    stats = {
        "total": len(tasks),
        "by_status": {s: 0 for s in TASK_STATUSES},
        "by_apply": {s: 0 for s in APPLY_STATUSES},
        "done": 0,
    }
    for t in tasks:
        stats["by_status"][str(t.get("status"))] = stats["by_status"].get(str(t.get("status")), 0) + 1
        stats["by_apply"][str(t.get("apply_status"))] = stats["by_apply"].get(str(t.get("apply_status")), 0) + 1
        if str(t.get("status")) in ("success", "failed", "skipped", "cancelled"):
            stats["done"] += 1
    return stats


def ledger_path_for_output(base_dir: str = None) -> str:
    """面向输出 data 的台账绝对路径。"""
    return os.path.abspath(ledger_file(base_dir))
