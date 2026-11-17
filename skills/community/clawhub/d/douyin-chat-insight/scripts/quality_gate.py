"""Lightweight gates before claiming completion."""
from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple

ABS_PATH_RE = re.compile(r"(?:/Users|/home|/Volumes)/\S+|\\\\Users\\\\")


def gate_inventory(inv: dict) -> Tuple[bool, List[str]]:
    errs: List[str] = []
    warns: List[str] = []
    rows = inv.get("conversations") or []
    if not rows:
        errs.append("inventory 会话列表为空")
        return False, errs
    empty = [r for r in rows if int(r.get("messages_kept") or r.get("messages_total") or 0) <= 0]
    if len(empty) == len(rows):
        errs.append("全部会话有效消息为 0（空导出/仅 header/过滤后无正文）")
    elif empty:
        names = ", ".join(str(r.get("name") or r.get("index")) for r in empty[:5])
        warns.append(f"部分会话无有效消息: {names}")
    # privacy: inventory should not leak abs paths
    blob = str(inv)
    if ABS_PATH_RE.search(blob):
        errs.append("inventory 结果含私人绝对路径（source_path 未脱敏）")
    inv.setdefault("warnings", [])
    inv["warnings"].extend(warns)
    return (len(errs) == 0, errs + [f"WARN: {w}" for w in warns])


def gate_deep(result: dict) -> Tuple[bool, List[str]]:
    errs: List[str] = []
    if result.get("status") != "deep_analyze":
        errs.append("不是 deep_analyze 结果")
    scope = result.get("scope") or {}
    if int(scope.get("messages_analyzed") or 0) <= 0:
        errs.append("分析消息数为 0")
    blocks = result.get("blocks") or {}
    totals = sum(
        len(blocks.get(k) or [])
        for k in ("hard_facts", "open_contradictions", "demand_quotes", "actions")
    )
    if totals == 0:
        errs.append("四块全空：导出可能无有效正文，或过滤过严")
    blob = str(result)
    if ABS_PATH_RE.search(blob):
        errs.append("报告含私人绝对路径（违反隐私门）")
    return (len(errs) == 0, errs)


def assert_no_default_max_group(deep_requested: bool, conv_specified: bool) -> None:
    if deep_requested and not conv_specified:
        raise ValueError("深挖必须显式指定 --conv（禁止默认最大群）")
