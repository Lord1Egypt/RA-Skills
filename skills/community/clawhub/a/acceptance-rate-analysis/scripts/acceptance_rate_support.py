from __future__ import annotations

import json
import math
import re
from datetime import datetime, timedelta
from itertools import combinations
from typing import Any, Callable

import dataworks_client as client

from acceptance_rate_constants import (
    ASSET_BUCKET_DRAG_ABSOLUTE_THRESHOLD,
    ASSET_BUCKET_DRAG_RELATIVE_THRESHOLD,
    ASSET_RAW_GATE_DECLINING_BUCKET_RATIO,
    ASSET_RAW_GATE_MIN_COMPARABLE_BUCKETS,
    ASSET_RAW_GATE_MIN_DECLINING_BUCKETS_FLOOR,
    ASSET_RAW_GATE_ROUTE_SHARE_THRESHOLD,
    ASSET_FACTOR_OVERVIEW_TABLE_COLUMNS,
    ASSET_RANGE_ROUTE_ABSOLUTE_THRESHOLD,
    ASSET_RANGE_TABLE_COLUMNS,
    ASSET_FACTOR_TABLE_COLUMNS,
    CAPITAL_BUCKET_TABLE_COLUMNS,
    CAPITAL_TOTAL_DROP_ABSOLUTE_THRESHOLD,
    CUSTOMER_GROUP_ACCEPTANCE_THRESHOLDS,
    FACTOR_LABELS,
    FACTOR_TARGET_BUCKETS,
    FUNDING_ENTITY,
    FUNDING_SUPPORTED_FACTORS,
    MAIN_ENTITY,
    METRIC_ACCEPTANCE_RATE,
    METRIC_CAPITAL_COUNT,
    METRIC_ROUTING_AMOUNT,
    METRIC_ROUTING_COUNT,
    MODEL_SET_NAME,
    PRIMARY_CUSTOMER_GROUP_DECLINE_THRESHOLD,
    PRIMARY_CUSTOMER_GROUP_TABLE_COLUMNS,
    PRIMARY_GROUP_SLICE_TABLE_COLUMNS,
    STAGE_LABELS,
    STAGE_STATUS_TOKENS,
    STATUS_SYMBOL_LOCKED,
    STATUS_SYMBOL_MAP,
    STATUS_SYMBOL_OK,
    STATUS_SYMBOL_PENDING,
    STATUS_SYMBOL_SHIFT,
    STATUS_SYMBOL_STOP,
    TARGET_CUSTOMER_GROUPS,
    TERMINAL_REASON_TEXT,
)

# 指标解析：取数侧常用「无值」展示（承接率列 `-`、`—` 等），与 None/空串一并视为数值 0
_TO_FLOAT_EMPTY_TOKENS = frozenset({
    "-",
    "--",
    "—",  # U+2014
    "－",  # U+FF0D fullwidth hyphen-minus
    "N/A",
    "n/a",
    "NA",
    "#N/A",
})
_TO_FLOAT_EMPTY_TOKENS_LOWER = frozenset({"null", "none"})


def json_dumps(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).split())


def to_float(value: Any) -> float:
    """解析数值类指标。承接率等字段：缺失与 `-`/`—`/N/A 等占位符均映射为 0.0，参与聚合与桶级对比。"""
    if value in (None, ""):
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    text = normalize_text(value).replace(",", "")
    if not text or text in _TO_FLOAT_EMPTY_TOKENS:
        return 0.0
    if text.lower() in _TO_FLOAT_EMPTY_TOKENS_LOWER:
        return 0.0
    try:
        return float(text)
    except ValueError:
        return 0.0


def safe_div(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def round_float(value: float | None, digits: int = 6) -> float | None:
    if value is None:
        return None
    return round(value, digits)


def format_percent(value: float) -> str:
    return f"{round(value * 100, 2)}%"


def format_wan(value: float) -> str:
    return f"{round(value / 10000, 2)}万"


def format_amount_human(value: float | None) -> str:
    if value is None:
        return "-"
    actual_value = to_float(value)
    unit = "亿" if abs(actual_value) >= 100000000 else "万"
    divisor = 100000000 if unit == "亿" else 10000
    rounded = round(actual_value / divisor, 2)
    if rounded == -0.0:
        rounded = 0.0
    return f"{rounded}{unit}"


def format_bp(value: float) -> str:
    rounded = round(value * 10000, 2)
    if rounded == -0.0:
        rounded = 0.0
    return f"{rounded}bp"


def format_percent_or_dash(value: float | None) -> str:
    if value is None:
        return "-"
    return format_percent(value)


def format_wan_or_dash(value: float | None) -> str:
    if value is None:
        return "-"
    return format_wan(value)


def format_yes_no(value: bool) -> str:
    return "是" if value else "否"


# ==== 状态展示规范（方案A：状态树最小版） ====
# 顺序固定为 S1 -> S2 -> S3 -> S4，对应一级到四级阶段
STAGE_ORDER: tuple[str, ...] = ("S1", "S2", "S3", "S4")


def bold_md(value: Any) -> str:
    """把任意可显示值用 markdown 加粗包裹；空值返回原样占位 `-`。"""
    text = normalize_text(value) if value is not None else ""
    if text in ("", "-"):
        return text or "-"
    return f"**{text}**"


def emphasize_negative_text(value: Any) -> str:
    """仅在负向变化时加粗，保持原始值不变。"""
    text = normalize_text(value) if value is not None else ""
    if text in ("", "-"):
        return text or "-"
    if text.startswith("**") and text.endswith("**"):
        return text
    return bold_md(text) if text.startswith("-") else text


def status_token_for_reason(terminal_reason: str | None) -> dict[str, str]:
    """将 terminal_reason 翻译成 {stage, status, label}；未知 reason 视作待定。"""
    code = normalize_text(terminal_reason)
    token = STAGE_STATUS_TOKENS.get(code)
    if token is not None:
        return dict(token)
    return {"stage": "S?", "status": "PENDING", "label": "未识别"}


def _path_token_text(stage: str, status: str, *, terminal_reason: str | None) -> str:
    """生成单个阶段的 SX{符号} 文本（展示层不输出内部 R 码）。"""
    symbol = STATUS_SYMBOL_MAP.get(status, STATUS_SYMBOL_PENDING)
    _ = terminal_reason
    return f"{stage}{symbol}"


def build_path_segments(
    *,
    terminal_reason: str | None,
    completed_stages: list[str] | None = None,
) -> list[str]:
    """
    根据当前 terminal_reason 与已通过的阶段列表，按 S1->S4 顺序生成路径段。
    - completed_stages：本次调用前已通过（OK）的阶段，例如三级运行时 ["S1","S2"]
    - 终止阶段使用 STAGE_STATUS_TOKENS 中映射的状态符号
    - 终止阶段之后的阶段统一用 PENDING 符号 `—`
    """
    completed = list(completed_stages or [])
    token = status_token_for_reason(terminal_reason)
    terminal_stage = token.get("stage")
    terminal_status = token.get("status")
    segments: list[str] = []
    terminated = False
    for stage in STAGE_ORDER:
        if terminated:
            segments.append(f"{stage}{STATUS_SYMBOL_PENDING}")
            continue
        if terminal_status == "DATA-GAP" and stage in completed:
            # R8 在某个阶段触发，前面已通过的阶段照旧标 OK
            segments.append(_path_token_text(stage, "OK", terminal_reason=None))
            continue
        if terminal_status == "DATA-GAP" and stage not in completed:
            # DATA-GAP 落到当前阶段
            segments.append(_path_token_text(stage, "DATA-GAP", terminal_reason=terminal_reason))
            terminated = True
            continue
        if stage == terminal_stage:
            segments.append(_path_token_text(stage, terminal_status or "PENDING", terminal_reason=terminal_reason))
            terminated = True
            continue
        if stage in completed:
            segments.append(_path_token_text(stage, "OK", terminal_reason=None))
            continue
        segments.append(f"{stage}{STATUS_SYMBOL_PENDING}")
    return segments


def build_status_line(
    *,
    slice_index: int | None,
    slice_total: int | None,
    slice_display: str,
    terminal_reason: str | None,
    completed_stages: list[str] | None = None,
    conclusion_tag: str | None = None,
    task_step: int | None = None,
    task_total: int | None = None,
    task_label: str | None = None,
    show_slice_context: bool = True,
    show_stage_details: bool = True,
) -> str:
    """生成单个切片状态块（多行，业务可读，含阶段中文名与进度）。"""
    token = status_token_for_reason(terminal_reason)
    terminal_stage = normalize_text(token.get("stage"))
    terminal_status = normalize_text(token.get("status"))
    completed = set(completed_stages or [])
    progress_text = "未提供"
    if slice_total:
        current = slice_index if slice_index is not None else 0
        progress_text = f"{current}/{slice_total}"
    lines: list[str] = []
    if task_step is not None and task_total:
        task_desc = normalize_text(task_label) or "当前任务"
        lines.append(f"> 🚀 任务进度：步骤 {task_step}/{task_total} · {task_desc}")
    if show_slice_context:
        lines.extend(
            [
                f"> 📍 切片进度：{progress_text}",
                f"> 🧩 当前切片：{normalize_text(slice_display) or '[未识别切片]'}",
            ]
        )
    if show_stage_details:
        for stage in STAGE_ORDER:
            stage_label = STAGE_LABELS.get(stage, stage)
            if stage in completed:
                status_symbol = STATUS_SYMBOL_MAP["OK"]
                status_text = "已通过"
            elif terminal_stage == stage:
                status_symbol = STATUS_SYMBOL_MAP.get(terminal_status, STATUS_SYMBOL_PENDING)
                if terminal_status == "STOP":
                    status_text = normalize_text(conclusion_tag) or "终止"
                elif terminal_status == "LOCKED":
                    status_text = normalize_text(conclusion_tag) or "已闭环"
                elif terminal_status == "SHIFT":
                    status_text = normalize_text(conclusion_tag) or "结构迁移"
                elif terminal_status == "DATA-GAP":
                    status_text = normalize_text(conclusion_tag) or "证据不足"
                else:
                    status_text = normalize_text(conclusion_tag) or "进行中"
            else:
                status_symbol = STATUS_SYMBOL_PENDING
                status_text = "待执行"
            lines.append(f"> - {stage_label}：{status_symbol} {status_text}")
    else:
        if terminal_reason:
            summary_status = normalize_text(conclusion_tag) or "已结束"
            lines.append(f"> ✅ 步骤结论：{summary_status}")
        else:
            lines.append("> ✅ 步骤结论：已完成，可进入步骤2")
    return "\n".join(lines)


def build_slice_queue_line(analysis_sequence: list[dict[str, Any]]) -> str:
    """一级阶段尾部展示：异常切片队列。返回 `> 🗂️ 切片队列：...`，无切片返回空串。"""
    if not analysis_sequence:
        return ""
    items: list[str] = []
    for index, slice_item in enumerate(analysis_sequence, start=1):
        display = normalize_text(slice_item.get("slice_display")) or normalize_text(
            slice_item.get("slice_key")
        )
        items.append(f"[{index}] {display}")
    return "> 🗂️ 切片队列：" + " · ".join(items)


def build_workflow_overview_markdown() -> str:
    """一级阶段前置：两步任务模型 + 切片内阶段（简洁版）。"""
    lines = [
        "### 诊断流程总览",
        "> 🧭 任务总进度（2步）：步骤1 大盘分析+异常切片定位；步骤2 每个切片下钻归因。",
        "> 🔍 切片内阶段：二级资方分布 → 三级资产维度 → 四级敏感资方闭环（命中即停）。",
    ]
    return "\n".join(lines)


def build_global_progress_line(
    *,
    completed_count: int,
    total_count: int,
    locked_count: int = 0,
    shift_count: int = 0,
    gap_count: int = 0,
    other_stop_count: int = 0,
) -> str:
    """第五阶段顶部统一进度行，带明显图标前缀。"""
    return (
        f"> 📊 已完成 {completed_count}/{total_count} 个切片："
        f"闭环 {locked_count} · 结构迁移 {shift_count} · 证据不足 {gap_count} · 常规终止 {other_stop_count}"
    )


def conclusion_tag_for_reason(terminal_reason: str | None) -> str:
    """根据 terminal_reason 给出统一的结论标签短语。"""
    token = status_token_for_reason(terminal_reason)
    return normalize_text(token.get("label")) or "未识别"


def resolve_slice_index_from_primary(
    primary_trace: dict[str, Any] | None,
    slice_key: str,
) -> tuple[int | None, int]:
    """
    根据 primary_trace 中与 slice_key 解析当前切片在队列中的位置。
    优先 `analysis_sequence`；若为空（例如 R2 清空路由队列）则使用 `analysis_sequence_lookup`。
    返回 (slice_index_1based or None, slice_total)。slice_total=0 表示一级未产出队列。
    """
    if not primary_trace:
        return None, 0
    sequence = list(primary_trace.get("analysis_sequence") or [])
    if not sequence:
        sequence = list(primary_trace.get("analysis_sequence_lookup") or [])
    total = len(sequence)
    if not sequence:
        return None, 0
    target = normalize_text(slice_key)
    for index, item in enumerate(sequence, start=1):
        if normalize_text(item.get("slice_key")) == target or slice_key_matches(item.get("slice_key", ""), slice_key):
            return index, total
    # 找不到精确匹配时，尝试用宽松匹配（沿用主流程同一规则）
    return None, total


def append_status_line(markdown_text: str, status_line: str) -> str:
    """把 status_line 追加到既有 markdown 末尾，自动加 1 个空行分隔。"""
    base = markdown_text or ""
    line = status_line or ""
    if not line:
        return base
    if not base:
        return line
    if base.endswith("\n"):
        return base + "\n" + line
    return base + "\n\n" + line


def prepend_status_block(markdown_text: str, status_block: str) -> str:
    """把状态块放到 markdown 开头，保证用户先看到当前切片进度与阶段状态。"""
    body = markdown_text or ""
    block = status_block or ""
    if not block:
        return body
    if not body:
        return block
    return block + "\n\n" + body


def build_slice_status_summary(
    *,
    slice_display: str,
    terminal_reason: str | None,
    completed_stages: list[str] | None = None,
) -> dict[str, str]:
    """生成单个切片的状态摘要，可被第五阶段汇总表引用。"""
    completed = list(completed_stages or [])
    if not normalize_text(terminal_reason):
        stage = normalize_text(completed[-1]) if completed else ""
        status = "OK" if stage else "PENDING"
        symbol = STATUS_SYMBOL_MAP.get(status, STATUS_SYMBOL_PENDING)
        label = {
            "S1": "一级通过",
            "S2": "二级通过，进入三级资产维度",
            "S3": "三级通过，进入四级敏感资方闭环",
            "S4": "四级通过",
        }.get(stage, "阶段通过")
        return {
            "slice_display": normalize_text(slice_display),
            "terminal_reason": "",
            "end_stage": stage,
            "end_stage_label": STAGE_LABELS.get(stage, stage or "—"),
            "status": status,
            "status_symbol": symbol,
            "conclusion_tag": label,
            "is_locked": False,
            "completed_stages": completed,
        }
    token = status_token_for_reason(terminal_reason)
    stage = normalize_text(token.get("stage"))
    status = normalize_text(token.get("status"))
    symbol = STATUS_SYMBOL_MAP.get(status, STATUS_SYMBOL_PENDING)
    is_locked = status == "LOCKED"
    end_stage_label = STAGE_LABELS.get(stage, stage or "—")
    return {
        "slice_display": normalize_text(slice_display),
        "terminal_reason": normalize_text(terminal_reason),
        "end_stage": stage,
        "end_stage_label": end_stage_label,
        "status": status,
        "status_symbol": symbol,
        "conclusion_tag": conclusion_tag_for_reason(terminal_reason),
        "is_locked": is_locked,
        "completed_stages": completed,
    }


def primary_slice_sort_key(item: dict[str, Any]) -> tuple[Any, ...]:
    customer_group = normalize_text(item.get("if_irr"))
    customer_group_order = {
        normalize_text(group): index
        for index, group in enumerate(TARGET_CUSTOMER_GROUPS)
    }
    return (
        customer_group_order.get(customer_group, len(customer_group_order)),
        customer_group,
        -primary_impact_accept_amount_estimate(item),
        -abs(to_float(item.get("delta_rate", item.get("acceptance_rate_delta")))),
        normalize_text(item.get("slice_display")),
    )


def sort_primary_slices(items: list[dict[str, Any]]) -> None:
    items.sort(key=primary_slice_sort_key)


def format_asset_dimension_hit(hit: dict[str, Any]) -> str:
    factor_label = normalize_text(hit.get("factor_label"))
    bucket = normalize_text(hit.get("bucket"))
    share_delta = format_percent(max(to_float(hit.get("share_delta")), 0.0))
    current_rate = format_percent(to_float(hit.get("current_acceptance_rate")))
    drag_amount = format_wan(to_float(hit.get("bucket_drag_amount")))
    drag_threshold = format_wan(to_float(hit.get("bucket_drag_threshold")))
    return (
        f"资产{factor_label}维度的 {bucket} 占比上升 {share_delta}，当前承接率 {current_rate}，"
        f"对应单桶影响承接金额估算约 {drag_amount}，单桶识别门槛 {drag_threshold}。"
    )


def normalize_boundary(value: str, *, is_end: bool) -> str:
    text = normalize_text(value)
    if not text:
        raise ValueError("时间参数不能为空。")
    if len(text) == 10:
        return f"{text} 23:59:59" if is_end else f"{text} 00:00:00"
    return text


def build_reason(reason_code: str | None) -> str | None:
    if reason_code is None:
        return None
    return TERMINAL_REASON_TEXT.get(reason_code, reason_code)


def unsupported_granularity_error(normalized_granularity: str) -> str:
    return f"当前版本仅支持 day / week，收到粒度：{normalized_granularity}。"


def business_view(*, headline: str, summary: str, evidence: list[str] | None = None) -> dict[str, Any]:
    return {
        "headline": headline,
        "summary": summary,
        "evidence": evidence or [],
    }


def stage_analysis_step(
    *,
    step: str,
    analysis: str,
    evidence: list[str] | None = None,
    conclusion: str,
    status: str = "completed",
) -> dict[str, Any]:
    return {
        "step": step,
        "status": status,
        "analysis": analysis,
        "evidence": evidence or [],
        "conclusion": conclusion,
    }


def build_root_cause(root_type: str, message: str, **details: Any) -> dict[str, Any]:
    payload = {
        "type": root_type,
        "message": message,
    }
    if details:
        payload["details"] = details
    return payload


def build_slice_key(if_irr: str, if_qd: str | None = None, cp_dj_new: str | None = None) -> str:
    actual_if_irr = normalize_text(if_irr)
    actual_cp_dj_new = normalize_text(cp_dj_new) if cp_dj_new is not None else normalize_text(if_qd)
    if actual_if_irr and actual_cp_dj_new:
        return f"{actual_if_irr}|{actual_cp_dj_new}"
    return normalize_text("|".join(item for item in [actual_if_irr, actual_cp_dj_new] if item))


def parse_slice_key(slice_key: str) -> tuple[str, str, str]:
    parts = [normalize_text(item) for item in normalize_text(slice_key).split("|")]
    if len(parts) >= 3:
        return parts[0], parts[1], parts[2]
    if len(parts) == 2:
        return parts[0], "", parts[1]
    if len(parts) == 1:
        return parts[0], "", ""
    return "", "", ""


def build_slice_display(if_irr: str, if_qd: str | None = None, cp_dj_new: str | None = None) -> str:
    actual_if_irr, actual_if_qd, actual_cp_dj_new = parse_slice_key(
        build_slice_key(if_irr, if_qd, cp_dj_new)
    )
    if actual_if_irr:
        return f"{actual_if_irr} | {actual_cp_dj_new}"
    return f"{actual_if_qd} | {actual_cp_dj_new}"


def customer_group_threshold(value: Any) -> float | None:
    normalized = normalize_text(value)
    return CUSTOMER_GROUP_ACCEPTANCE_THRESHOLDS.get(normalized)


def selected_customer_groups(if_irr: str | None = None) -> list[str]:
    normalized = normalize_text(if_irr)
    if normalized:
        if normalized in CUSTOMER_GROUP_ACCEPTANCE_THRESHOLDS:
            return [normalized]
        return []
    return list(TARGET_CUSTOMER_GROUPS)


def build_customer_group_judgement(
    *,
    if_irr: str,
    current_acceptance_rate: float | None,
    baseline_acceptance_rate: float | None,
    threshold: float | None,
    hit_threshold: bool,
    hit_decline_threshold: bool,
    enter_slice_analysis: bool,
    group_terminal_reason: str | None,
    summary_text: str,
) -> dict[str, Any]:
    threshold_value = round_float(threshold, 6)
    return {
        "if_irr": normalize_text(if_irr),
        "threshold": threshold_value,
        "threshold_text": format_percent(threshold) if threshold is not None else "-",
        "current_acceptance_rate": round_float(current_acceptance_rate, 6),
        "baseline_acceptance_rate": round_float(baseline_acceptance_rate, 6),
        "current_acceptance_rate_text": format_percent(current_acceptance_rate) if current_acceptance_rate is not None else "-",
        "baseline_acceptance_rate_text": format_percent(baseline_acceptance_rate) if baseline_acceptance_rate is not None else "-",
        "hit_threshold": hit_threshold,
        "hit_decline_threshold": hit_decline_threshold,
        "enter_slice_analysis": enter_slice_analysis,
        "group_terminal_reason": group_terminal_reason,
        "summary_text": summary_text,
    }


def build_customer_group_summary_text(
    customer_group_judgements: list[dict[str, Any]],
    *,
    has_selected_slices: bool,
    terminal_reason: str | None = None,
) -> str:
    if not customer_group_judgements:
        return "当前没有命中纳入分析范围的目标客群，因此第一阶段停止。"

    summary_parts = [
        normalize_text(item.get("summary_text"))
        for item in customer_group_judgements
        if normalize_text(item.get("summary_text"))
    ]
    if terminal_reason in {"R1", "R8"}:
        return " ".join(summary_parts)
    if not has_selected_slices:
        if terminal_reason == "R10":
            summary_parts.append("目标客群虽然有命中过继续分析条件，但没有形成继续下钻的异常切片，因此本次停在第一阶段。")
        elif terminal_reason == "R9" or not any(
            bool(item.get("hit_threshold")) or bool(item.get("hit_decline_threshold"))
            for item in customer_group_judgements
        ):
            summary_parts.append("两类目标客群当前都没有触发继续分析条件，因此本次不继续后续归因。")
    return " ".join(summary_parts)


def primary_continue_analysis_scope_text() -> str:
    return (
        "客群入口：精优 <97%、惠选 <99%、或较对比期明显下降 abs 0.3% 以上；"
        "异常切片入口：命中客群后，所有承接率较对比期下降的 客群 + cp_dj_new 切片都继续下钻；"
        "展示方式：第一阶段会直接返回惠选客群表和精优客群表，无需再按客群拆分。"
    )


def build_primary_continue_analysis_scope_markdown() -> str:
    return "\n".join(
        [
            "### 继续分析口径",
            "- 客群入口：精优 <97%、惠选 <99%、或较对比期明显下降 abs 0.3% 以上",
            "- 异常切片入口：命中客群后，所有承接率较对比期下降的 `客群 + cp_dj_new` 切片都继续下钻",
            "- 展示方式：第一阶段直接给出惠选客群与精优客群两张分表，无需模型再拆分客群",
        ]
    )


def factor_label_for_key(factor_key: str) -> str:
    normalized = normalize_text(factor_key)
    return FACTOR_LABELS.get(normalized, normalized or "[未命名维度]")


def bucket_label_for_value(bucket: Any) -> str:
    text = normalize_text(bucket)
    return text or "[空值]"


def build_factor_dimension_trace(
    factor_bucket_stats: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    ordered_keys = list(FACTOR_LABELS)
    ordered_keys.extend(key for key in factor_bucket_stats if key not in FACTOR_LABELS)
    dimensions: list[dict[str, Any]] = []
    for factor_key in ordered_keys:
        if factor_key not in factor_bucket_stats:
            continue
        dimensions.append(
            {
                "factor_key": factor_key,
                "factor_label": factor_label_for_key(factor_key),
                "bucket_stats": factor_bucket_stats[factor_key],
            }
        )
    return dimensions


def normalize_range_factor_items(factor_items: list[dict[str, Any]]) -> list[dict[str, str]]:
    normalized_items: list[dict[str, str]] = []
    for item in factor_items:
        factor_key = normalize_text(item.get("factor_key"))
        bucket = normalize_text(item.get("bucket"))
        if not factor_key or not bucket:
            continue
        factor_label = normalize_text(item.get("factor_label")) or factor_label_for_key(factor_key)
        normalized_items.append(
            {
                "factor_key": factor_key,
                "factor_label": factor_label,
                "bucket": bucket,
            }
        )
    normalized_items.sort(key=lambda item: (item["factor_key"], item["bucket"]))
    return normalized_items


def build_range_key(factor_items: list[dict[str, Any]]) -> str:
    normalized_items = normalize_range_factor_items(factor_items)
    return "&&".join(f'{item["factor_key"]}={item["bucket"]}' for item in normalized_items)


def build_range_display(factor_items: list[dict[str, Any]]) -> str:
    normalized_items = normalize_range_factor_items(factor_items)
    return " + ".join(f'{item["factor_label"]}:{item["bucket"]}' for item in normalized_items)




def primary_impact_accept_amount_estimate(item: dict[str, Any]) -> float:
    direct_value = item.get("impact_accept_amount_estimate")
    if direct_value not in (None, ""):
        return to_float(direct_value)
    current_rate = to_float(item.get("current_rate", item.get("current_acceptance_rate")))
    baseline_rate = to_float(item.get("baseline_rate", item.get("baseline_acceptance_rate")))
    current_route_amount = to_float(item.get("current_route_amount"))
    return current_route_amount * max(baseline_rate - current_rate, 0.0)


def primary_impact_accept_amount_formula_text() -> str:
    return "影响承接金额估算 = 当前路由金额 × max(对比期承接率 - 当前承接率, 0)"




def select_primary_drill_down_candidates(
    abnormal_slices: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if not abnormal_slices:
        return [], {
            "selection_rule": "all_declining_slices_within_eligible_customer_group",
            "selection_rule_text": "命中客群入口后，该客群下所有承接率较对比期下降的切片都继续下钻。",
            "total_abnormal_impact_accept_amount_estimate": 0.0,
            "abnormal_slice_count": 0,
            "selected_slice_count": 0,
        }

    total_abnormal_impact_accept_amount_estimate = sum(
        primary_impact_accept_amount_estimate(item)
        for item in abnormal_slices
    )
    candidates = list(abnormal_slices)
    return candidates, {
        "selection_rule": "all_declining_slices_within_eligible_customer_group",
        "selection_rule_text": "命中客群入口后，该客群下所有承接率较对比期下降的切片都继续下钻。",
        "total_abnormal_impact_accept_amount_estimate": round_float(
            total_abnormal_impact_accept_amount_estimate,
            2,
        ),
        "abnormal_slice_count": len(abnormal_slices),
        "selected_slice_count": len(candidates),
    }


def build_primary_drill_down_explanation(
    *,
    abnormal_slice_count: int,
    drill_down_rule: dict[str, Any],
    group_label: str | None = None,
    include_formula: bool = True,
) -> str:
    selected_slice_count = int(to_float(drill_down_rule.get("selected_slice_count")))
    scope_prefix = f"{normalize_text(group_label)}：" if normalize_text(group_label) else ""
    formula_prefix = f"{primary_impact_accept_amount_formula_text()}。"
    if abnormal_slice_count <= 0:
        explanation = f"{scope_prefix}当前没有承接率下降切片，因此不进入后续切片下钻。"
        return f"{formula_prefix}{explanation}" if include_formula else explanation
    explanation = (
        f"{scope_prefix}当前共定位 {abnormal_slice_count} 个承接率下降切片，表格展示全部切片；"
        "命中客群入口后，该客群下所有承接率较对比期下降的切片都会继续下钻，"
        f"因此本次继续 {selected_slice_count} 个切片。"
    )
    return f"{formula_prefix}{explanation}" if include_formula else explanation


def build_primary_analysis_sequence(abnormal_slices: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sequence: list[dict[str, Any]] = []
    for item in abnormal_slices:
        sequence.append(
            {
                "analysis_rank": item.get("analysis_rank"),
                "slice_key": item.get("slice_key"),
                "slice_display": item.get("slice_display"),
                "if_irr": item.get("if_irr"),
                "cp_dj_new": item.get("cp_dj_new"),
                "current_acceptance_rate": round_float(to_float(item.get("current_rate")), 6),
                "baseline_acceptance_rate": round_float(to_float(item.get("baseline_rate")), 6),
                "acceptance_rate_delta": round_float(to_float(item.get("delta_rate")), 6),
                "current_route_amount": round_float(to_float(item.get("current_route_amount")), 2),
                "baseline_route_amount": round_float(to_float(item.get("baseline_route_amount")), 2),
                "current_route_share": round_float(to_float(item.get("current_route_share")), 6),
                "baseline_route_share": round_float(to_float(item.get("baseline_route_share")), 6),
                "route_share_delta": round_float(to_float(item.get("route_share_delta")), 6),
                "impact_accept_amount_estimate": round_float(
                    primary_impact_accept_amount_estimate(item),
                    2,
                ),
            }
        )
    return sequence


def build_markdown_table(columns: list[dict[str, str]], rows: list[dict[str, Any]]) -> str:
    def _escape_markdown_cell(value: Any) -> str:
        text = str(value)
        return text.replace("|", r"\|").replace("\n", " ")

    if not columns:
        return ""
    header = "| " + " | ".join(column["label"] for column in columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    data_lines: list[str] = []
    for row in rows:
        values: list[str] = []
        for column in columns:
            value = row.get(column["key"], "")
            if value is None:
                value = ""
            values.append(_escape_markdown_cell(value))
        data_lines.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *data_lines])
def build_primary_overall_summary_markdown(
    *,
    context: dict[str, Any],
    customer_group_rows: list[dict[str, Any]],
    current_acceptance_rate: float,
    baseline_acceptance_rate: float,
    acceptance_rate_delta: float,
    current_route_amount: float,
    baseline_route_amount: float,
) -> str:
    overall_table = build_markdown_table(
        [
            {"key": "metric", "label": "指标"},
            {"key": "baseline_text", "label": "对比期"},
            {"key": "current_text", "label": "当前期"},
            {"key": "delta_text", "label": "变化"},
        ],
        [
            {
                "metric": "承接率",
                "baseline_text": format_percent(baseline_acceptance_rate),
                "current_text": format_percent(current_acceptance_rate),
                "delta_text": emphasize_negative_text(format_percent(acceptance_rate_delta)),
            },
            {
                "metric": "路由金额",
                "baseline_text": format_amount_human(baseline_route_amount),
                "current_text": format_amount_human(current_route_amount),
                "delta_text": emphasize_negative_text(
                    format_amount_human(current_route_amount - baseline_route_amount)
                ),
            },
        ],
    )
    bolded_customer_group_rows = []
    for row in customer_group_rows:
        bolded_row = dict(row)
        if normalize_text(row.get("acceptance_rate_delta_text")) not in ("", "-"):
            bolded_row["acceptance_rate_delta_text"] = bold_md(row.get("acceptance_rate_delta_text"))
        bolded_customer_group_rows.append(bolded_row)
    customer_group_table = build_markdown_table(
        PRIMARY_CUSTOMER_GROUP_TABLE_COLUMNS, bolded_customer_group_rows
    )
    parts = [
        "### 大盘情况",
        overall_table,
        (
            f"整体大盘承接率由 {format_percent(baseline_acceptance_rate)} 变为 {format_percent(current_acceptance_rate)}，"
            f"变化 {format_percent(acceptance_rate_delta)}；"
            f"路由金额由 {format_amount_human(baseline_route_amount)} 变为 {format_amount_human(current_route_amount)}，"
            f"变化 {format_amount_human(current_route_amount - baseline_route_amount)}。"
        ),
        "",
        "### 客群承接率变化",
        customer_group_table,
    ]
    warnings = [
        normalize_text(item)
        for item in (context.get("period_warnings") or [])
        if normalize_text(item)
    ]
    if warnings:
        parts.append("提示：")
        parts.extend(f"- {item}" for item in warnings)
    return "\n".join(parts)


def build_period_debug_snapshot(
    *,
    current_result: dict[str, Any] | None = None,
    baseline_result: dict[str, Any] | None = None,
    current_filter: str | dict[str, Any] | None = None,
    baseline_filter: str | dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "current": {
            "filter": current_filter,
            "payload": (current_result or {}).get("payload"),
            "sql": (current_result or {}).get("sql"),
            "column_head_list": (current_result or {}).get("column_head_list"),
            "rows": (current_result or {}).get("rows", []),
        },
        "baseline": {
            "filter": baseline_filter,
            "payload": (baseline_result or {}).get("payload"),
            "sql": (baseline_result or {}).get("sql"),
            "column_head_list": (baseline_result or {}).get("column_head_list"),
            "rows": (baseline_result or {}).get("rows", []),
        },
    }


def build_capital_total_judgement(
    *,
    current: float | None = None,
    baseline: float | None = None,
    threshold_absolute: float = CAPITAL_TOTAL_DROP_ABSOLUTE_THRESHOLD,
    evaluated: bool,
    skipped_reason: str | None = None,
    calculation_method: str | None = None,
    weight_metric: str | None = None,
    bucket_dimension: str | None = None,
    data_quality: dict[str, Any] | None = None,
) -> dict[str, Any]:
    current_value = round_float(current, 4)
    baseline_value = round_float(baseline, 4)
    delta = None if current is None or baseline is None else round_float(current - baseline, 4)
    drop = None if current is None or baseline is None else round_float(baseline - current, 4)
    movement_direction = None
    if delta is not None:
        if delta > 0:
            movement_direction = "up"
        elif delta < 0:
            movement_direction = "down"
        else:
            movement_direction = "flat"
    hit_drop_threshold = None if drop is None else drop >= threshold_absolute
    is_non_decreasing = None if movement_direction is None else movement_direction in {"up", "flat"}
    if not evaluated:
        decision_reason = "当前未完成准入资方个数加权均值判断。"
    elif movement_direction == "up":
        decision_reason = (
            f"当前期加权均值 {_format_number_or_dash(current_value)} 家/单，"
            f"较对比期 {_format_number_or_dash(baseline_value)} 家/单 上升，"
            "该信号仅用于说明资方变化，不作为分叉终止条件，仍继续看 4-CDF 分布判断。"
        )
    elif movement_direction == "flat":
        decision_reason = (
            f"当前期加权均值 {_format_number_or_dash(current_value)} 家/单 与对比期持平，"
            "该信号仅用于说明资方变化，不作为分叉终止条件，仍继续看 4-CDF 分布判断。"
        )
    elif hit_drop_threshold:
        decision_reason = (
            f"当前期加权均值 {_format_number_or_dash(current_value)} 家/单，"
            f"较对比期 {_format_number_or_dash(baseline_value)} 家/单 下降 {_format_number_or_dash(drop)} 家，"
            "该信号仅用于说明资方变化，不作为分叉终止条件，仍继续看 4-CDF 分布判断。"
        )
    else:
        decision_reason = (
            f"当前期加权均值 {_format_number_or_dash(current_value)} 家/单，"
            f"较对比期 {_format_number_or_dash(baseline_value)} 家/单 下降 {_format_number_or_dash(drop)} 家，"
            "该信号仅用于说明资方变化，不作为分叉终止条件，继续看 4-CDF 分布判断。"
        )
    return {
        "evaluated": evaluated,
        "current": current_value,
        "baseline": baseline_value,
        "delta": delta,
        "drop": drop,
        "threshold_absolute": threshold_absolute,
        "threshold_basis": "absolute_drop_of_weighted_mean",
        "movement_direction": movement_direction,
        "is_non_decreasing": is_non_decreasing,
        "hit_drop_threshold": hit_drop_threshold,
        "calculation_method": calculation_method or "weighted_mean_allow_bucket_by_route_amount",
        "weight_metric": weight_metric or "route_amount",
        "bucket_dimension": bucket_dimension or "alllow_ly_cnt",
        "data_quality": data_quality or {},
        "decision_reason": decision_reason,
        "skipped_reason": skipped_reason,
    }


def build_distribution_judgement(
    *,
    evaluated: bool,
    skipped_reason: str | None = None,
    weighted_mean_current: float | None = None,
    weighted_mean_baseline: float | None = None,
    weighted_mean_delta: float | None = None,
    weighted_median_current: float | None = None,
    weighted_median_baseline: float | None = None,
    weighted_median_delta: float | None = None,
    low_bucket_share_current: dict[str, Any] | None = None,
    low_bucket_share_baseline: dict[str, Any] | None = None,
    low_bucket_share_delta: dict[str, Any] | None = None,
    high_bucket_share_current: dict[str, Any] | None = None,
    high_bucket_share_baseline: dict[str, Any] | None = None,
    high_bucket_share_delta: dict[str, Any] | None = None,
    low_bucket_share_up: bool | None = None,
    high_bucket_share_down: bool | None = None,
    central_tendency_down: bool | None = None,
    structural_shift_strength: float | None = None,
    is_left_shift: bool | None = None,
    distribution_basis: str | None = None,
    cdf_cutoff_stats: list[dict[str, Any]] | None = None,
    effective_cutoff_count: int | None = None,
    effective_cutoff_hit_count: int | None = None,
    effective_cutoff_hit_ratio: float | None = None,
    max_negative_cutoff_delta: float | None = None,
    has_positive_cutoff_signal: bool | None = None,
    top_bucket_deltas: list[dict[str, Any]] | None = None,
    tail_bucket_summary: dict[str, Any] | None = None,
    decision_reason: str | None = None,
) -> dict[str, Any]:
    return {
        "evaluated": evaluated,
        "skipped_reason": skipped_reason,
        "weighted_mean_current": round_float(weighted_mean_current, 6),
        "weighted_mean_baseline": round_float(weighted_mean_baseline, 6),
        "weighted_mean_delta": round_float(weighted_mean_delta, 6),
        "weighted_median_current": round_float(weighted_median_current, 6),
        "weighted_median_baseline": round_float(weighted_median_baseline, 6),
        "weighted_median_delta": round_float(weighted_median_delta, 6),
        "low_bucket_share_current": low_bucket_share_current or {},
        "low_bucket_share_baseline": low_bucket_share_baseline or {},
        "low_bucket_share_delta": low_bucket_share_delta or {},
        "high_bucket_share_current": high_bucket_share_current or {},
        "high_bucket_share_baseline": high_bucket_share_baseline or {},
        "high_bucket_share_delta": high_bucket_share_delta or {},
        "low_bucket_share_up": low_bucket_share_up,
        "high_bucket_share_down": high_bucket_share_down,
        "central_tendency_down": central_tendency_down,
        "structural_shift_strength": round_float(structural_shift_strength, 6),
        "is_left_shift": is_left_shift,
        "distribution_basis": distribution_basis or "routing_amount_full_bucket",
        "cdf_cutoff_stats": cdf_cutoff_stats or [],
        "effective_cutoff_count": effective_cutoff_count,
        "effective_cutoff_hit_count": effective_cutoff_hit_count,
        "effective_cutoff_hit_ratio": round_float(effective_cutoff_hit_ratio, 6),
        "max_negative_cutoff_delta": round_float(max_negative_cutoff_delta, 6),
        "has_positive_cutoff_signal": has_positive_cutoff_signal,
        "top_bucket_deltas": top_bucket_deltas or [],
        "tail_bucket_summary": tail_bucket_summary or {},
        "decision_reason": decision_reason or "",
    }


def build_empty_primary_display() -> dict[str, Any]:
    return {
        "overall_summary_markdown": "",
        "drill_down_scope_markdown": build_primary_continue_analysis_scope_markdown(),
        "huixuan_group_markdown": "",
        "jingyou_group_markdown": "",
        "overall_summary": {},
        "render_summary": {
            "llm_render_field": "primary_display.overall_summary_markdown",
            "llm_followup_field": "primary_display.drill_down_scope_markdown",
            "llm_group_fields": [
                "primary_display.huixuan_group_markdown",
                "primary_display.jingyou_group_markdown",
            ],
            "must_use_markdown_table_verbatim": True,
            "instruction": (
                "【强制执行】第一阶段输出时，按顺序把以下 5 个字段逐字复制进最终回复正文："
                "1. primary_display.overall_summary_markdown；"
                "2. customer_group_summary_text；"
                "3. primary_display.drill_down_scope_markdown；"
                "4. primary_display.huixuan_group_markdown（含惠选客群全部切片行，不得只复制部分行）；"
                "5. primary_display.jingyou_group_markdown（含精优客群全部切片行，不得只复制部分行）。"
                "analysis_sequence 只用于第二阶段路由，严禁用于第一阶段表格内容。"
                "在这 5 个字段全部写入回复正文之前，禁止插入任何摘要或过渡话术。"
            ),
        },
    }


def normalize_slice_component(value: Any) -> str:
    return normalize_text(value).replace(" ", "").lower()


def normalize_funding_kequn_tag(value: Any) -> str:
    text = normalize_text(value)
    if not text:
        return ""
    match = re.match(r"^(\d+\.)\s*(.+)$", text)
    if match:
        return f"{match.group(1)} {match.group(2)}"
    return text


def slice_key_matches(left: str, right: str) -> bool:
    left_if_irr, left_if_qd, left_cp_dj_new = parse_slice_key(left)
    right_if_irr, right_if_qd, right_cp_dj_new = parse_slice_key(right)
    if not left_if_irr or not right_if_irr or not left_cp_dj_new or not right_cp_dj_new:
        return normalize_slice_component(left) == normalize_slice_component(right)
    if normalize_slice_component(left_cp_dj_new) != normalize_slice_component(right_cp_dj_new):
        return False
    return normalize_slice_component(left_if_irr) == normalize_slice_component(right_if_irr)


def build_context(
    *,
    granularity: str,
    current_start: str,
    current_end: str,
    baseline_start: str,
    baseline_end: str,
) -> dict[str, Any]:
    normalized_granularity = normalize_granularity(granularity)
    context = {
        "granularity": granularity,
        "current_period": {
            "start": normalize_boundary(current_start, is_end=False),
            "end": normalize_boundary(current_end, is_end=True),
        },
        "baseline_period": {
            "start": normalize_boundary(baseline_start, is_end=False),
            "end": normalize_boundary(baseline_end, is_end=True),
        },
    }
    if normalized_granularity == "week":
        current_period_label, current_notice = build_week_period_label(
            current_start,
            current_end,
            period_name="当前周期",
        )
        baseline_period_label, baseline_notice = build_week_period_label(
            baseline_start,
            baseline_end,
            period_name="对比周期",
        )
        context["period_semantics"] = {
            "week_start_day": "monday",
            "default_week_window": "monday_to_sunday_natural_week",
            "notice_partial_week_to_user": True,
            "display_notation": "[start, end]",
            "primary_query_strategy": "merged_window_then_split",
            "description": "周粒度默认按周一到周日的自然周解释；一级诊断会先把当前期和对比期合成一个总查询窗口，按两段实际日期并集做 dt 筛选，再按周桶拆成 current / baseline；如果时间窗截至当前尚未形成完整自然周，需要显式提示用户这是周内累计口径。",
        }
        context["current_period_label"] = current_period_label
        context["baseline_period_label"] = baseline_period_label
        period_warnings = [item for item in (current_notice, baseline_notice) if item]
        if period_warnings:
            context["period_warnings"] = period_warnings
    return context


def build_week_period_label(start: str, end: str, *, period_name: str) -> tuple[dict[str, Any], str | None]:
    label_start = parse_datetime_text(start, is_end=False).date()
    label_end = parse_datetime_text(end, is_end=True).date()
    natural_week_start = label_start - timedelta(days=label_start.weekday())
    natural_week_end = natural_week_start + timedelta(days=6)
    is_full_natural_week = label_start == natural_week_start and label_end == natural_week_end
    label = {
        "start": label_start.isoformat(),
        "end": label_end.isoformat(),
        "text": f"{label_start.isoformat()}~{label_end.isoformat()}",
        "natural_week_start": natural_week_start.isoformat(),
        "natural_week_end": natural_week_end.isoformat(),
        "is_full_natural_week": is_full_natural_week,
        "week_window_type": "full_natural_week" if is_full_natural_week else "partial_natural_week",
    }
    if is_full_natural_week:
        return label, None
    notice = (
        f"{period_name} {label['text']} 不是完整自然周，默认周口径应取周一到周日；"
        "如果这是截至当前 / 周内累计 / 与上周同期口径，请向用户明确说明。"
    )
    return label, notice


def normalize_granularity(value: str) -> str:
    text = normalize_text(value).lower()
    mapping = {
        "d": "day",
        "day": "day",
        "daily": "day",
        "w": "week",
        "week": "week",
        "weekly": "week",
    }
    return mapping.get(text, text or "week")


def time_dimension_name(granularity: str) -> str:
    normalized_granularity = normalize_granularity(granularity)
    if normalized_granularity == "day":
        return "dt"
    return "week"


def parse_datetime_text(value: str, *, is_end: bool) -> datetime:
    normalized = normalize_boundary(value, is_end=is_end)
    return datetime.strptime(normalized, "%Y-%m-%d %H:%M:%S")


def union_time_range(
    *,
    current_start: str,
    current_end: str,
    baseline_start: str,
    baseline_end: str,
) -> tuple[str, str]:
    start_candidates = [
        parse_datetime_text(current_start, is_end=False),
        parse_datetime_text(baseline_start, is_end=False),
    ]
    end_candidates = [
        parse_datetime_text(current_end, is_end=True),
        parse_datetime_text(baseline_end, is_end=True),
    ]
    query_end_dt = max(end_candidates)
    query_start = min(start_candidates).strftime("%Y-%m-%d %H:%M:%S")
    query_end = query_end_dt.strftime("%Y-%m-%d %H:%M:%S")
    return query_start, query_end


def build_query_window_label(start: str, end: str, *, granularity: str) -> dict[str, Any] | None:
    normalized_granularity = normalize_granularity(granularity)
    if normalized_granularity != "week":
        return None
    start_date = parse_datetime_text(start, is_end=False).date()
    end_date = parse_datetime_text(end, is_end=True).date()
    return {
        "start": start_date.isoformat(),
        "end": end_date.isoformat(),
        "text": f"{start_date.isoformat()}~{end_date.isoformat()}",
    }


def bucket_key(value: str, *, granularity: str, is_end: bool) -> str:
    normalized_granularity = normalize_granularity(granularity)
    current = parse_datetime_text(value, is_end=is_end)
    if normalized_granularity == "day":
        return current.strftime("%Y-%m-%d")
    if normalized_granularity == "week":
        week_start = current.date().fromordinal(current.date().toordinal() - current.weekday())
        return week_start.isoformat()
    return current.strftime("%Y-%m-%d")


def validate_granularity_window(granularity: str, start: str, end: str) -> str | None:
    normalized_granularity = normalize_granularity(granularity)
    start_bucket = bucket_key(start, granularity=normalized_granularity, is_end=False)
    end_bucket = bucket_key(end, granularity=normalized_granularity, is_end=True)
    if start_bucket == end_bucket:
        return None

    labels = {
        "day": "日",
        "week": "周",
    }
    label = labels.get(normalized_granularity, normalized_granularity)
    return f"{label}粒度时间窗跨越多个{label}桶：start={normalize_boundary(start, is_end=False)}，end={normalize_boundary(end, is_end=True)}。"


def bucket_value_matches(raw_value: Any, *, granularity: str, expected_bucket: str) -> bool:
    value = normalize_text(raw_value)
    normalized_granularity = normalize_granularity(granularity)
    if not value:
        return False
    if normalized_granularity == "week":
        if value[:10] == expected_bucket[:10]:
            return True
        try:
            bucket_date = datetime.strptime(expected_bucket[:10], "%Y-%m-%d").date()
        except ValueError:
            return False
        iso_year, iso_week, _ = bucket_date.isocalendar()
        candidate_codes = {
            f"{iso_year}-W{iso_week:02d}",
            f"{iso_year}W{iso_week:02d}",
            f"W{iso_week:02d}",
        }
        return value in candidate_codes
    return value[:10] == expected_bucket[:10]


def split_primary_records_by_granularity_bucket(
    *,
    records: list[dict[str, Any]],
    granularity: str,
    current_start: str,
    current_end: str,
    baseline_start: str,
    baseline_end: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    time_dimension = time_dimension_name(granularity)
    current_bucket = bucket_key(current_start, granularity=granularity, is_end=False)
    baseline_bucket = bucket_key(baseline_start, granularity=granularity, is_end=False)

    current_records = [
        item
        for item in records
        if bucket_value_matches(item.get(time_dimension), granularity=granularity, expected_bucket=current_bucket)
    ]
    baseline_records = [
        item
        for item in records
        if bucket_value_matches(item.get(time_dimension), granularity=granularity, expected_bucket=baseline_bucket)
    ]

    return current_records, baseline_records


def parse_allow_bucket(value: Any) -> float | None:
    text = normalize_text(value)
    if not text:
        return None
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    if not match:
        return None
    return float(match.group(0))


def weighted_median(pairs: list[tuple[float, float]]) -> float | None:
    valid_pairs = [(value, weight) for value, weight in pairs if weight > 0]
    if not valid_pairs:
        return None
    valid_pairs.sort(key=lambda item: item[0])
    total_weight = sum(weight for _, weight in valid_pairs)
    threshold = total_weight / 2
    running = 0.0
    for value, weight in valid_pairs:
        running += weight
        if running >= threshold:
            return value
    return valid_pairs[-1][0]


def bucket_route_share(
    buckets: list[dict[str, Any]],
    total_route_amount: float,
    predicate: Callable[[float | None], bool],
) -> float:
    return safe_div(
        sum(
            to_float(item.get("route_amount"))
            for item in buckets
            if predicate(parse_allow_bucket(item.get("alllow_ly_cnt")))
        ),
        total_route_amount,
    )


def normalize_cp_dj(value: Any) -> str:
    text = normalize_text(value)
    if not text:
        return ""
    lowered = re.sub(r"^[0-9]+\.\s*", "", text).replace(" ", "").lower()
    if "月月付" in lowered:
        return "月月付"
    if "笔笔购" in lowered:
        return "笔笔购"
    if "小权益" in lowered or "权益" in lowered:
        return "小权益"
    if "irr24" in lowered:
        return "irr24"
    if "irr36" in lowered:
        return "irr36"
    return lowered


def normalize_identity_bucket(value: Any) -> str:
    text = normalize_text(value)
    if not text:
        return "[空值]"
    if "\u65e0\u6548" in text:
        return "\u8eab\u4efd\u8bc1\u65e0\u6548"
    if "\u6709\u6548" in text:
        return "\u8eab\u4efd\u8bc1\u6709\u6548"
    return text


def normalize_age_bucket(value: Any) -> str:
    text = normalize_text(value)
    if not text:
        return "[空值]"
    lowered = text.lower()
    if any(flag in lowered for flag in (">55", "55+", "≥55")) or text in {"55", "6.55"}:
        return "55+"
    if re.search(r"50[^0-9]*54", lowered):
        return "50-54"
    if re.search(r"\[50,\s*54\]", lowered):
        return "50-54"
    digits = [int(item) for item in re.findall(r"\d+", lowered)]
    if len(digits) >= 2 and digits[0] == 50 and digits[1] == 54:
        return "50-54"
    return "其他年龄"


def normalize_region_bucket(value: Any) -> str:
    text = normalize_text(value)
    if not text:
        return "[空值]"
    if "\u65b0\u7586" in text:
        return "\u65b0\u7586"
    if "\u897f\u85cf" in text:
        return "\u897f\u85cf"
    return "\u5176\u4ed6\u5730\u533a"


def normalize_amount_bucket(value: Any) -> str:
    text = normalize_text(value)
    if not text:
        return "[空值]"
    lowered = text.lower().replace(" ", "")
    if "5w" in lowered:
        return "5W+"
    digits = [int(item) for item in re.findall(r"\d+", lowered)]
    if any(number >= 50000 for number in digits):
        return "5W+"
    if "∞" in lowered and digits and digits[-1] >= 50000:
        return "5W+"
    return "其他金额"


def normalize_risk_bucket(value: Any) -> str:
    text = normalize_text(value)
    return text or "[空值]"


def factor_bucket_value(factor_key: str, raw_value: Any) -> str:
    if factor_key == "identity_effective_date":
        return normalize_identity_bucket(raw_value)
    if factor_key == "age_rand":
        return normalize_age_bucket(raw_value)
    if factor_key == "identity_province_name":
        return normalize_region_bucket(raw_value)
    if factor_key == "edu_rand":
        return normalize_amount_bucket(raw_value)
    if factor_key == "reloan_price_tag":
        return normalize_risk_bucket(raw_value)
    return normalize_text(raw_value)


def parse_age_interval(value: Any) -> tuple[int | None, int | None] | None:
    text = normalize_text(value)
    if not text:
        return None
    lowered = text.lower().replace(" ", "")
    range_match = re.search(r"(\d+)\s*[-~至]\s*(\d+)", lowered)
    if range_match:
        start = int(range_match.group(1))
        end = int(range_match.group(2))
        if start <= end:
            return start, end
        return end, start
    digits = [int(item) for item in re.findall(r"\d+", lowered)]
    if not digits:
        return None
    if any(flag in lowered for flag in ("+", "以上", "及以上", ">=", ">")):
        return digits[0], None
    if any(flag in lowered for flag in ("以下", "及以下", "<=", "<")):
        return None, digits[-1]
    if len(digits) >= 2:
        start = digits[0]
        end = digits[1]
        if start <= end:
            return start, end
        return end, start
    return digits[0], digits[0]


def parse_age_upper_bound(value: Any) -> int | None:
    interval = parse_age_interval(value)
    if interval is None:
        return None
    _, upper_bound = interval
    return upper_bound


def age_intervals_intersect(
    left: tuple[int | None, int | None] | None,
    right: tuple[int | None, int | None] | None,
) -> bool:
    if left is None or right is None:
        return False
    left_lower, left_upper = left
    right_lower, right_upper = right
    actual_left_lower = left_lower if left_lower is not None else float("-inf")
    actual_left_upper = left_upper if left_upper is not None else float("inf")
    actual_right_lower = right_lower if right_lower is not None else float("-inf")
    actual_right_upper = right_upper if right_upper is not None else float("inf")
    return actual_left_lower <= actual_right_upper and actual_right_lower <= actual_left_upper


def parse_allowed_provinces(value: Any) -> set[str]:
    text = normalize_text(value)
    if not text:
        return set()
    normalized = text.replace("，", ",").replace("、", ",")
    return {item.strip() for item in normalized.split(",") if item.strip()}


def _project_sensitive_to_factor(project_row: dict[str, Any], factor_item: dict[str, Any]) -> bool:
    factor_key = normalize_text(factor_item.get("factor_key"))
    bucket = normalize_text(factor_item.get("bucket"))
    if factor_key == "identity_effective_date":
        bucket = normalize_identity_bucket(bucket)
        floor_days = to_float(project_row.get("chk_identity_card_effc_term_floor_days"))
        invalid_bucket = normalize_identity_bucket("无效")
        valid_bucket = normalize_identity_bucket("有效")
        if bucket == invalid_bucket:
            return floor_days > 0
        if bucket == valid_bucket:
            return floor_days <= 0
        return False
    if factor_key == "identity_province_name":
        bucket = normalize_region_bucket(bucket)
        allowed_provinces = parse_allowed_provinces(project_row.get("allow_identity_city_prov"))
        restricted_buckets = {"\u65b0\u7586", "\u897f\u85cf"}
        if bucket in restricted_buckets:
            return bool(allowed_provinces) and bucket not in allowed_provinces
        return False
    if factor_key == "age_rand":
        bucket = normalize_age_bucket(bucket)
        project_interval = parse_age_interval(project_row.get("age_range"))
        if project_interval is None:
            return False
        target_interval = parse_age_interval(bucket)
        if bucket == "55+":
            target_interval = (55, None)
        elif bucket == "50-54":
            target_interval = (50, 54)
        if target_interval is None:
            return False
        return age_intervals_intersect(project_interval, target_interval)
    return False


def build_main_dimensions(
    *,
    granularity: str,
    include_allow: bool = False,
    include_asset: bool = False,
) -> list[dict[str, Any]]:
    time_dimension = time_dimension_name(granularity)
    dimensions = [
        client.dimension(time_dimension, MAIN_ENTITY, "day"),
        client.dimension("if_irr", MAIN_ENTITY),
        client.dimension("cp_dj_new", MAIN_ENTITY),
    ]
    if include_allow:
        dimensions.append(client.dimension("alllow_ly_cnt", MAIN_ENTITY))
    if include_asset:
        dimensions.extend(
            [
                client.dimension("age_rand", MAIN_ENTITY),
                client.dimension("identity_effective_date", MAIN_ENTITY),
                client.dimension("identity_province_name", MAIN_ENTITY),
                client.dimension("edu_rand", MAIN_ENTITY),
                client.dimension("reloan_price_tag", MAIN_ENTITY),
            ]
        )
    return dimensions


def build_funding_dimensions() -> list[dict[str, Any]]:
    return [
        client.dimension("week", FUNDING_ENTITY, "day"),
        client.dimension("kequn_tag", FUNDING_ENTITY),
        client.dimension("cp_dj", FUNDING_ENTITY),
        client.dimension("age_range", FUNDING_ENTITY),
        client.dimension("allow_identity_city_prov", FUNDING_ENTITY),
        client.dimension("capital_project_name", FUNDING_ENTITY),
        client.dimension("chk_identity_card_effc_term_floor_days", FUNDING_ENTITY),
    ]


def build_main_rules(
    *,
    start: str,
    end: str,
    if_irr: str | None = None,
    if_qd: str | None = None,
    cp_dj_new: str | None = None,
) -> str:
    del if_qd  # 第一到第四阶段统一改为按客群 + cp_dj_new 透传，不再追加账龄过滤。
    rules = [
        client.build_time_rule(
            name="dt",
            entity_name=MAIN_ENTITY,
            start=normalize_boundary(start, is_end=False),
            end=normalize_boundary(end, is_end=True),
        )
    ]
    if if_irr:
        rules.append(client.build_equals_rule(name="if_irr", entity_name=MAIN_ENTITY, value=if_irr))
    if cp_dj_new:
        rules.append(client.build_equals_rule(name="cp_dj_new", entity_name=MAIN_ENTITY, value=cp_dj_new))
    return client.build_filter(rules)


def build_funding_rules(*, start: str, end: str, kequn_tag: str | None = None) -> str:
    rules = [
        client.build_time_rule(
            name="fk_dt",
            entity_name=FUNDING_ENTITY,
            start=normalize_boundary(start, is_end=False),
            end=normalize_boundary(end, is_end=True),
        )
    ]
    normalized_kequn_tag = normalize_funding_kequn_tag(kequn_tag)
    if normalized_kequn_tag:
        rules.append(
            client.build_equals_rule(
                name="kequn_tag",
                entity_name=FUNDING_ENTITY,
                value=normalized_kequn_tag,
            )
        )
    return client.build_filter(rules)


def _query_rows(
    *,
    access_token: str,
    metric_list: list[dict[str, Any]],
    dimension_list: list[dict[str, Any]] | None = None,
    row_dimension_list: list[dict[str, Any]] | None = None,
    filter_payload: str | dict[str, Any] | None = None,
    endpoint: str | None = None,
) -> tuple[dict[str, Any], str | None]:
    try:
        result = client.query_metric_data(
            access_token=access_token,
            data_model_set_name=MODEL_SET_NAME,
            metric_list=metric_list,
            dimension_list=dimension_list,
            row_dimension_list=row_dimension_list,
            column_dimension_list=[] if row_dimension_list is not None else None,
            filter_payload=filter_payload,
            endpoint=endpoint,
        )
    except Exception as exc:
        return {}, str(exc)
    return result, None


def _normalized_metric_rows(rows: list[dict[str, Any]], dimension_fields: list[str]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for row in rows:
        route_amount_metric = client.extract_row_value(row, METRIC_ROUTING_AMOUNT)
        route_amount = to_float(route_amount_metric)
        acceptance_rate_metric = client.extract_row_value(row, METRIC_ACCEPTANCE_RATE)
        acceptance_rate = to_float(acceptance_rate_metric)
        accepted_amount = route_amount * acceptance_rate
        route_count_metric = client.extract_row_value(row, METRIC_ROUTING_COUNT)
        normalized_row: dict[str, Any] = {
            "route_amount": route_amount,
            "accepted_amount": accepted_amount,
            "acceptance_rate": safe_div(accepted_amount, route_amount),
            "source_row_count": 1,
            "route_amount_present_rows": 1 if route_amount_metric not in (None, "") else 0,
            "route_count_present_rows": 1 if route_count_metric not in (None, "") else 0,
        }
        if route_count_metric not in (None, ""):
            normalized_row["route_count"] = to_float(route_count_metric)
        capital_count_metric = client.extract_row_value(row, METRIC_CAPITAL_COUNT)
        if capital_count_metric not in (None, ""):
            normalized_row["capital_count_metric"] = to_float(capital_count_metric)
        for field_name in dimension_fields:
            normalized_row[field_name] = normalize_text(client.extract_row_value(row, field_name))
        normalized.append(normalized_row)
    return normalized


def _extract_metric_total(rows: list[dict[str, Any]], metric_name: str) -> tuple[float, bool]:
    total = 0.0
    found = False
    for row in rows:
        metric_value = client.extract_row_value(row, metric_name)
        if metric_value in (None, ""):
            continue
        found = True
        total += to_float(metric_value)
    return total, found


def _aggregate_records(records: list[dict[str, Any]], group_fields: list[str]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, ...], dict[str, Any]] = {}
    for record in records:
        key = tuple(normalize_text(record.get(field_name)) for field_name in group_fields)
        target = grouped.setdefault(
            key,
            {
                field_name: normalize_text(record.get(field_name))
                for field_name in group_fields
            },
        )
        target["route_amount"] = target.get("route_amount", 0.0) + to_float(record.get("route_amount"))
        target["accepted_amount"] = target.get("accepted_amount", 0.0) + to_float(record.get("accepted_amount"))
        target["source_row_count"] = target.get("source_row_count", 0) + int(record.get("source_row_count", 0))
        target["route_amount_present_rows"] = target.get("route_amount_present_rows", 0) + int(
            record.get("route_amount_present_rows", 0)
        )
        target["route_count_present_rows"] = target.get("route_count_present_rows", 0) + int(
            record.get("route_count_present_rows", 0)
        )
        if "route_count" in record:
            target["route_count"] = target.get("route_count", 0.0) + to_float(record.get("route_count"))
        if "capital_count_metric" in record:
            target["capital_count_metric"] = target.get("capital_count_metric", 0.0) + to_float(record.get("capital_count_metric"))
    for target in grouped.values():
        target["acceptance_rate"] = safe_div(
            to_float(target.get("accepted_amount")),
            to_float(target.get("route_amount")),
        )
    return list(grouped.values())


def _aggregate_slice_map(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    aggregated = _aggregate_records(records, ["if_irr", "cp_dj_new"])
    slice_map: dict[str, dict[str, Any]] = {}
    for item in aggregated:
        slice_key = build_slice_key(item["if_irr"], item["cp_dj_new"])
        item["slice_key"] = slice_key
        slice_map[slice_key] = item
    return slice_map




def _current_slice_from_primary(primary_trace: dict[str, Any], slice_key: str) -> dict[str, Any]:
    seq_rows = list(primary_trace.get("analysis_sequence") or [])
    if not seq_rows:
        seq_rows = list(primary_trace.get("analysis_sequence_lookup") or [])
    for item in seq_rows:
        if slice_key_matches(item.get("slice_key", ""), slice_key):
            current_rate = to_float(item.get("current_acceptance_rate"))
            baseline_rate = to_float(item.get("baseline_acceptance_rate"))
            current_route_amount = to_float(item.get("current_route_amount"))
            return {
                "slice_key": item.get("slice_key"),
                "slice_display": item.get("slice_display"),
                "if_irr": item.get("if_irr"),
                "cp_dj_new": item.get("cp_dj_new"),
                "current_rate": item.get("current_acceptance_rate"),
                "baseline_rate": item.get("baseline_acceptance_rate"),
                "current_route_amount": item.get("current_route_amount"),
                "baseline_route_amount": item.get("baseline_route_amount"),
                "impact_accept_amount_estimate": item.get("impact_accept_amount_estimate"),
                "current_route_share": item.get("current_route_share"),
                "baseline_route_share": item.get("baseline_route_share"),
                "route_share_delta": item.get("route_share_delta"),
                "drag_amount": round_float(
                    max(baseline_rate - current_rate, 0.0) * current_route_amount,
                    2,
                ),
            }
    return {}


def _build_capital_render_summary() -> dict[str, Any]:
    return {
        "llm_render_field": "capital_display.summary_markdown",
        "llm_table_field": "capital_display.bucket_table_markdown",
        "llm_followup_field": "capital_display.distribution_detail_markdown",
        "must_show_table_when_present": True,
        "must_use_markdown_table_verbatim": True,
        "instruction": (
            "第二阶段给模型展示时，这 3 个字段必须按顺序原样进入最终回复正文：1. capital_display.summary_markdown；"
            "2. 若 capital_display.bucket_table_markdown 非空，必须原样输出该表格；"
            "3. capital_display.distribution_detail_markdown。"
            "不要只在思考过程中阅读、引用、总结或消化后省略这些展示块；如果脚本已经返回可直接展示的内容，先写入最终回复正文，再补必要的业务串联。"
            "在这 3 个字段输出完成前，禁止自己先写“第二阶段结果”“资方分布左移”"
            "“继续进入第三阶段”“现在开始第三阶段”这类摘要或过渡话术。"
            "不要根据 capital_distribution_stats、capital_total_judgement 或 "
            "distribution_judgement 重新拼表、重算占比或改写判断。"
        ),
    }


def build_empty_capital_display() -> dict[str, Any]:
    return {
        "summary_markdown": "",
        "distribution_detail_markdown": "",
        "bucket_table_markdown": "",
        "render_summary": _build_capital_render_summary(),
    }


def _format_number_or_dash(value: float | None, digits: int = 2) -> str:
    if value is None:
        return "-"
    rounded = round(value, digits)
    if float(rounded).is_integer():
        return str(int(rounded))
    return str(rounded)


def _build_capital_bucket_table_markdown(bucket_stats: list[dict[str, Any]]) -> str:
    if not bucket_stats:
        return ""
    # 找到占比变化绝对值最大的桶，用于整行加粗，方便阅读最强桶
    top_index: int | None = None
    top_abs_delta = -1.0
    for index, item in enumerate(bucket_stats):
        delta_value = item.get("route_share_delta")
        if delta_value is None:
            continue
        abs_delta = abs(to_float(delta_value))
        if abs_delta > top_abs_delta:
            top_abs_delta = abs_delta
            top_index = index
    table_rows: list[dict[str, Any]] = []
    for index, item in enumerate(bucket_stats):
        is_top = index == top_index and top_abs_delta > 0
        cell = {
            "bucket_label": normalize_text(item.get("alllow_ly_cnt")) or "未识别",
            "current_route_amount_text": format_wan_or_dash(item.get("current_route_amount")),
            "baseline_route_amount_text": format_wan_or_dash(item.get("baseline_route_amount")),
            "current_route_share_text": format_percent_or_dash(item.get("current_route_share")),
            "baseline_route_share_text": format_percent_or_dash(item.get("baseline_route_share")),
            "route_share_delta_text": emphasize_negative_text(
                format_percent_or_dash(item.get("route_share_delta"))
            ),
            "current_acceptance_rate_text": format_percent_or_dash(item.get("current_acceptance_rate")),
            "baseline_acceptance_rate_text": format_percent_or_dash(item.get("baseline_acceptance_rate")),
        }
        if is_top:
            cell = {key: bold_md(value) for key, value in cell.items()}
        table_rows.append(cell)
    markdown_table = build_markdown_table(CAPITAL_BUCKET_TABLE_COLUMNS, table_rows)
    if not markdown_table:
        return ""
    return "\n".join(
        [
            "### 资方桶分布表",
            markdown_table,
        ]
    )


def _build_capital_display(
    *,
    slice_display: str,
    capital_total_judgement: dict[str, Any],
    distribution_judgement: dict[str, Any],
    bucket_stats: list[dict[str, Any]],
    analysis_steps: list[dict[str, Any]],
    terminal_reason: str | None,
    next_action: str | None,
    business: dict[str, Any],
) -> dict[str, Any]:
    skipped_reason = normalize_text(distribution_judgement.get("skipped_reason"))
    movement_direction = normalize_text(capital_total_judgement.get("movement_direction"))
    data_quality = capital_total_judgement.get("data_quality") or {}

    # ── 分叉一：准入资方加权均值判断 ──────────────────────────────────
    summary_lines = [
        "### 第二阶段：资方分布诊断",
        f"**当前切片：{slice_display}**",
        "",
        "#### 路由信号说明（过程决策 ≠ 最终归因）",
        "- 本阶段输出的是**路由信号层**：`distribution_judgement.is_left_shift` 只表示 4-CDF 是否**建议继续进入第三阶段**；**不等于**已把承接率下降**最终归因**到「资方准入分布/资方家数」本身。",
        "- 最终归因定级在**第四阶段结合资金侧闭环**后给出（见 `final_attribution_level` 相关字段）。",
        "- 下方数值（加权均值变化、4-CDF 指标）统一按 **辅助结论 + 路由判断** 理解。",
        "",
        "#### 分叉一：准入资方加权均值判断",
        "- **计算口径**：`Σ(alllow_ly_cnt × route_amount) / Σ(route_amount)`，按路由金额加权，仅纳入能解析成整数的 alllow_ly_cnt 桶",
    ]
    if capital_total_judgement.get("evaluated"):
        current_wm = capital_total_judgement.get("current")
        baseline_wm = capital_total_judgement.get("baseline")
        rel_drop_display: float | None = None
        rel_chg_display: float | None = None
        if current_wm is not None and baseline_wm is not None and float(baseline_wm) > 0:
            rel_drop_display = float(baseline_wm - current_wm) / float(baseline_wm)
            rel_chg_display = float(current_wm - baseline_wm) / float(baseline_wm)
        summary_lines += [
            f"- 当前期加权均值：**{_format_number_or_dash(current_wm)} 家/单**",
            f"- 对比期加权均值：**{_format_number_or_dash(baseline_wm)} 家/单**",
        ]
        if movement_direction == "up":
            summary_lines.append(
                f"- 变化：上升 {_format_number_or_dash(capital_total_judgement.get('delta'))} 家/单"
                f"（+{format_percent_or_dash(rel_chg_display)}）"
            )
        elif movement_direction == "flat":
            summary_lines.append("- 变化：持平，0 家/单（0%）")
        else:
            summary_lines.append(
                f"- 变化：下降 {_format_number_or_dash(capital_total_judgement.get('drop'))} 家/单"
                f"（{format_percent_or_dash(rel_drop_display)}）"
            )
        summary_lines += [
            "- **口径说明**：加权均值只用于辅助说明资方变化，不作为第二阶段分叉终止条件；4-CDF 用于判断资方侧是否进入最终归因候选，第二阶段完成后继续进入资产维度。",
        ]
        # 数据质量提示
        if any(
            to_float(data_quality.get(key)) > 0
            for key in (
                "unknown_allow_routing_cnt_current",
                "unknown_allow_routing_cnt_baseline",
                "unknown_allow_routing_amount_current",
                "unknown_allow_routing_amount_baseline",
            )
        ):
            unknown_cnt_current = _format_number_or_dash(data_quality.get("unknown_allow_routing_cnt_current"))
            unknown_cnt_baseline = _format_number_or_dash(data_quality.get("unknown_allow_routing_cnt_baseline"))
            unknown_amount_current = format_wan_or_dash(data_quality.get("unknown_allow_routing_amount_current"))
            unknown_amount_baseline = format_wan_or_dash(data_quality.get("unknown_allow_routing_amount_baseline"))
            summary_lines.append(
                f"- ⚠️ 数据质量：未识别桶已排除在加权均值外；"
                f"当前未识别桶路由单量 {unknown_cnt_current}、路由金额 {unknown_amount_current}；"
                f"对比期路由单量 {unknown_cnt_baseline}、路由金额 {unknown_amount_baseline}"
            )
        # 分叉一结论（辅助说明，不作为终止）
        summary_lines.append("")
        summary_lines += [
            "- **分叉一结论**：该段仅做总量变化说明，下一步统一进入分叉二（4-CDF）判断。",
            "",
            f"> {normalize_text(capital_total_judgement.get('decision_reason'))}",
        ]
    elif analysis_steps:
        summary_lines.append(f"- 分叉一结论：{normalize_text(analysis_steps[0].get('conclusion'))}")

    # ── 分叉二：全桶路由金额分布判断 ──────────────────────────────────
    dist_lines = ["#### 分叉二：全桶路由金额分布判断"]
    if distribution_judgement.get("evaluated"):
        wm_cur = distribution_judgement.get("weighted_mean_current")
        wm_bas = distribution_judgement.get("weighted_mean_baseline")
        wm_delta = distribution_judgement.get("weighted_mean_delta")
        wmd_cur = distribution_judgement.get("weighted_median_current")
        wmd_bas = distribution_judgement.get("weighted_median_baseline")
        wmd_delta = distribution_judgement.get("weighted_median_delta")
        eff_ratio = distribution_judgement.get("effective_cutoff_hit_ratio")
        eff_cnt = distribution_judgement.get("effective_cutoff_count") or 0
        eff_hit = distribution_judgement.get("effective_cutoff_hit_count") or 0
        max_neg = distribution_judgement.get("max_negative_cutoff_delta")
        has_pos = distribution_judgement.get("has_positive_cutoff_signal")
        central_down = distribution_judgement.get("central_tendency_down")
        is_left_shift = distribution_judgement.get("is_left_shift")

        cond1_ok = bool(central_down)
        cond2_ok = eff_ratio is not None and eff_ratio >= 0.80
        cond3_ok = max_neg is not None and max_neg >= -0.03
        cond4_ok = bool(has_pos)

        def _tick(ok: bool) -> str:
            return "✓" if ok else "✗"

        dist_lines += [
            '- **分析思路**：把路由金额按"准入资方家数"从少到多分组，看当前期是否有更多的钱流向了家数少的桶（即"左移"）。'
            "需要同时满足以下四个信号，才认为分布整体发生了明确的低家数偏移：",
            "",
            "**集中趋势**",
            f"- 加权均值：当前 **{_format_number_or_dash(wm_cur)} 家/单**，对比期 {_format_number_or_dash(wm_bas)} 家/单，变化 {_format_number_or_dash(wm_delta)}",
        ]
        if wmd_cur is not None or wmd_bas is not None:
            dist_lines.append(
                f"- 加权中位数：当前 **{_format_number_or_dash(wmd_cur)} 家/单**，对比期 {_format_number_or_dash(wmd_bas)} 家/单，变化 {_format_number_or_dash(wmd_delta)}"
            )
        dist_lines += [
            "",
            "**四信号逐项判断**",
            f"- {_tick(cond1_ok)} **信号一（总体均值下降）**："
            f"平均每笔路由准入资方从 {_format_number_or_dash(wm_bas)} 家/单降至 {_format_number_or_dash(wm_cur)} 家/单"
            f"{'，总体资方供给收缩方向成立' if cond1_ok else '，总体均值未下降，供给收缩信号不足'}",
            f"- {_tick(cond2_ok)} **信号二（偏移方向一致）**："
            f"在 {eff_cnt} 个有效金额段里，有 {eff_hit} 个呈现出向少家数方向偏移（占比 {format_percent_or_dash(eff_ratio)}）"
            f"{'，一致性达标（≥80%）' if cond2_ok else '，一致性不足（需≥80%）'}",
            f"- {_tick(cond3_ok)} **信号三（无明显反向桶）**："
            f'偏移方向最"不一致"的金额段反向幅度为 {format_percent_or_dash(max_neg)}'
            f"{'，未超过 -3pp，整体方向稳定' if cond3_ok else '，超过 -3pp 警戒线，存在明显反向金额段'}",
            f"- {_tick(cond4_ok)} **信号四（有实质性位移）**："
            f"{'至少有一个金额段偏移超过 5pp，低家数集中程度显著' if cond4_ok else '无金额段偏移幅度超过 5pp，当前变化仍属微弱扰动'}",
        ]
        # 数据质量
        if any(
            to_float(data_quality.get(key)) > 0
            for key in ("unknown_allow_routing_amount_current", "unknown_allow_routing_amount_baseline")
        ):
            dist_lines.append(
                f"- ⚠️ 数据质量：未识别桶已排除在全桶排序外；"
                f"当前未识别桶路由金额 {format_wan_or_dash(data_quality.get('unknown_allow_routing_amount_current'))}，"
                f"对比期 {format_wan_or_dash(data_quality.get('unknown_allow_routing_amount_baseline'))}"
            )
        # 分叉二决策
        dist_lines.append("")
        if is_left_shift:
            dist_lines += [
                "- **分叉二结论（路由）**：四个信号全部成立，资方分布已明显向少家数端偏移"
                "——不是个别桶的随机波动，而是整体性的低家数集中；**路由信号**建议进入第三阶段做资产侧形态定位/反证（仍非最终归因）。",
                "",
                f"> {normalize_text(distribution_judgement.get('decision_reason'))}",
            ]
        else:
            cond_fail_msgs = []
            if not cond1_ok:
                cond_fail_msgs.append("平均准入家数未下降")
            if not cond2_ok:
                cond_fail_msgs.append(f"偏移方向一致性不足（{format_percent_or_dash(eff_ratio)} < 80%）")
            if not cond3_ok:
                cond_fail_msgs.append(f"存在明显反向金额段（最大反向 {format_percent_or_dash(max_neg)}）")
            if not cond4_ok:
                cond_fail_msgs.append("无金额段偏移超过 5pp，信号偏弱")
            fail_str = "、".join(cond_fail_msgs) if cond_fail_msgs else "信号未全部成立"
            dist_lines += [
                f"- **分叉二结论（路由）**：{fail_str}，分布未形成系统性低家数左移的 4-CDF 组合；"
                "这仅表示**本阶段资方分布路由信号为 no_shift**。"
                "脚本仍**继续进入第三阶段**以完成资产侧**集中/广谱/混合**形态判别，并与第四阶段资金闭环结果共同定级（过程决策≠最终归因）。",
                "",
                f"> {normalize_text(distribution_judgement.get('decision_reason'))}",
            ]
        # 主桶变化明细
        top_bucket_deltas = distribution_judgement.get("top_bucket_deltas") or []
        if top_bucket_deltas:
            dist_lines += ["", "**变化量最大的桶（各桶路由金额占比变化）**"]
            for item in top_bucket_deltas:
                delta_val = item.get("route_share_delta")
                sign = "▲" if (delta_val or 0) > 0 else ("▼" if (delta_val or 0) < 0 else "─")
                dist_lines.append(
                    f"- 桶 {normalize_text(item.get('bucket_label')) or '未识别'} 家："
                    f" 当前 {format_percent_or_dash(item.get('current_route_share'))}，"
                    f"对比期 {format_percent_or_dash(item.get('baseline_route_share'))}，"
                    f"变化 {sign} {format_percent_or_dash(abs(delta_val) if delta_val is not None else None)}"
                )
        tail_bucket_summary = distribution_judgement.get("tail_bucket_summary") or {}
        if to_float(tail_bucket_summary.get("bucket_count")) > 0:
            dist_lines.append(
                f"- 尾部桶汇总（其余 {int(to_float(tail_bucket_summary.get('bucket_count')))} 个桶）："
                f" 当前 {format_percent_or_dash(tail_bucket_summary.get('current_route_share'))}，"
                f"对比期 {format_percent_or_dash(tail_bucket_summary.get('baseline_route_share'))}，"
                f"变化 {format_percent_or_dash(tail_bucket_summary.get('route_share_delta'))}"
            )
    else:
        # 分布判断被跳过（一般是数据不足）
        if skipped_reason and skipped_reason.startswith("capital_total_"):
            skip_msg = "分叉一判断本身未完成，因此无法进入分叉二。"
        elif len(analysis_steps) > 1:
            skip_msg = normalize_text(analysis_steps[1].get("conclusion")) or "分叉二未完成。"
        else:
            skip_msg = "当前没有进入资方桶分布判断。"
        dist_lines.append(f"- {skip_msg}")

    summary_markdown = "\n".join(summary_lines)
    distribution_detail_markdown = "\n".join(dist_lines)
    bucket_table_markdown = _build_capital_bucket_table_markdown(bucket_stats)

    dj = distribution_judgement or {}
    if dj.get("evaluated") and dj.get("is_left_shift"):
        stage2_signal = "left_shift"
    elif dj.get("evaluated"):
        stage2_signal = "no_shift"
    else:
        stage2_signal = "unknown"

    return {
        "summary_markdown": summary_markdown,
        "distribution_detail_markdown": distribution_detail_markdown,
        "bucket_table_markdown": bucket_table_markdown,
        "render_summary": _build_capital_render_summary(),
        "stage2_signal": stage2_signal,
    }


def _finalize_capital_trace(
    trace: dict[str, Any],
    *,
    slice_index: int | None = None,
    slice_total: int | None = None,
) -> dict[str, Any]:
    trace["capital_display"] = _build_capital_display(
        slice_display=normalize_text(trace.get("slice_display")),
        capital_total_judgement=trace.get("capital_total_judgement") or {},
        distribution_judgement=trace.get("distribution_judgement") or {},
        bucket_stats=trace.get("capital_distribution_stats") or [],
        analysis_steps=trace.get("analysis_steps") or [],
        terminal_reason=trace.get("terminal_reason"),
        next_action=trace.get("next_action"),
        business=trace.get("business_view") or {},
    )
    capital_display = trace["capital_display"]
    trace["stage2_signal"] = capital_display.get("stage2_signal") or "unknown"
    # ===== 状态展示规范：二级阶段开头状态块 =====
    terminal_reason = trace.get("terminal_reason")
    # 本函数仅在资本阶段已产出展示时调用，二级（S2）必已完成
    completed_stages = ["S1", "S2"]
    # R8 也保留 S1 OK，因为 R8 出现时一级已经通过
    if not terminal_reason:
        # 二级通过，进入三级
        conclusion_tag = "二级通过，进入三级资产维度"
    else:
        conclusion_tag = conclusion_tag_for_reason(terminal_reason)
    status_line = build_status_line(
        slice_index=slice_index,
        slice_total=slice_total,
        slice_display=normalize_text(trace.get("slice_display")) or normalize_text(trace.get("slice_key")),
        terminal_reason=terminal_reason,
        completed_stages=completed_stages,
        conclusion_tag=conclusion_tag,
        task_step=2,
        task_total=2,
        task_label="每个切片下钻归因",
    )
    slice_status_summary = build_slice_status_summary(
        slice_display=normalize_text(trace.get("slice_display")) or normalize_text(trace.get("slice_key")),
        terminal_reason=terminal_reason,
        completed_stages=completed_stages,
    )
    trace["status_line"] = status_line
    trace["slice_status_summary"] = slice_status_summary
    trace["slice_index"] = slice_index
    trace["slice_total"] = slice_total
    capital_display["status_line"] = status_line
    capital_display["summary_markdown"] = prepend_status_block(
        capital_display.get("summary_markdown", ""), status_line
    )
    trace.pop("terminal_reason_text", None)
    trace.pop("weighted_mean_delta", None)
    trace.pop("weighted_median_delta", None)
    trace.pop("low_bucket_share_delta", None)
    trace.pop("high_bucket_share_delta", None)
    return trace


def build_empty_asset_display() -> dict[str, str]:
    return {
        "summary_markdown": "",
        "factor_detail_markdown": "",
        "range_detail_markdown": "",
    }


def finalize_asset_trace(
    trace: dict[str, Any],
    *,
    slice_index: int | None = None,
    slice_total: int | None = None,
) -> dict[str, Any]:
    """为三级资产维度 trace 注入状态块，并前置到本阶段展示开头。"""
    terminal_reason = trace.get("terminal_reason")
    completed_stages = ["S1", "S2", "S3"] if not terminal_reason else ["S1", "S2"]
    slice_display = (
        normalize_text(trace.get("slice_display"))
        or normalize_text(trace.get("slice_key"))
    )
    if not terminal_reason:
        conclusion_tag = "三级通过，进入四级敏感资方闭环"
    else:
        conclusion_tag = conclusion_tag_for_reason(terminal_reason)
    status_line = build_status_line(
        slice_index=slice_index,
        slice_total=slice_total,
        slice_display=slice_display,
        terminal_reason=terminal_reason,
        completed_stages=completed_stages,
        conclusion_tag=conclusion_tag,
        task_step=2,
        task_total=2,
        task_label="每个切片下钻归因",
    )
    slice_status_summary = build_slice_status_summary(
        slice_display=slice_display,
        terminal_reason=terminal_reason,
        completed_stages=completed_stages,
    )
    trace["status_line"] = status_line
    trace["slice_status_summary"] = slice_status_summary
    trace["slice_index"] = slice_index
    trace["slice_total"] = slice_total
    asset_display = trace.get("asset_display") or {}
    asset_display["status_line"] = status_line
    asset_display["summary_markdown"] = prepend_status_block(
        asset_display.get("summary_markdown", ""), status_line
    )
    trace["asset_display"] = asset_display
    return trace


def finalize_funding_trace(
    trace: dict[str, Any],
    *,
    slice_index: int | None = None,
    slice_total: int | None = None,
) -> dict[str, Any]:
    """为四级资金闭环 trace 注入根级 status_line；不在 business_view.summary 内重复嵌套状态块。"""
    terminal_reason = trace.get("terminal_reason")
    completed_stages = ["S1", "S2", "S3"]
    slice_display = (
        normalize_text(trace.get("slice_display"))
        or normalize_text(trace.get("slice_key"))
    )
    if terminal_reason == "R7":
        conclusion_tag = conclusion_tag_for_reason("R7")
    elif terminal_reason in {"R6", "R8", None, ""}:
        conclusion_tag = conclusion_tag_for_reason(terminal_reason or "R6")
    else:
        conclusion_tag = conclusion_tag_for_reason(terminal_reason)
    status_line = build_status_line(
        slice_index=slice_index,
        slice_total=slice_total,
        slice_display=slice_display,
        terminal_reason=terminal_reason,
        completed_stages=completed_stages,
        conclusion_tag=conclusion_tag,
        task_step=2,
        task_total=2,
        task_label="每个切片下钻归因",
    )
    slice_status_summary = build_slice_status_summary(
        slice_display=slice_display,
        terminal_reason=terminal_reason,
        completed_stages=completed_stages,
    )
    trace["status_line"] = status_line
    trace["slice_status_summary"] = slice_status_summary
    trace["slice_index"] = slice_index
    trace["slice_total"] = slice_total
    business = trace.get("business_view") or {}
    if isinstance(business, dict):
        trace["business_view"] = business
    return trace


def compute_asset_dimension_pattern(factor_results: list[dict[str, Any]]) -> dict[str, Any]:
    """基于各因子 `broad_perf_decline` 与命中情况判别资产侧形态（集中 / 广谱 / 混合）。"""
    broad_n = sum(1 for item in factor_results if item.get("broad_perf_decline"))
    hit_n = sum(1 for item in factor_results if normalize_text(item.get("final_decision")) == "hit")

    if broad_n >= 2 and hit_n >= 1:
        pattern = "mixed_pattern"
        label = (
            "**混合**：不止一个资产维度里出现「大范围承接变差」，同时又有关键业务桶已判定异常。"
            "读结论时不要只盯某一个资产维度当唯一主因，宜结合第二阶段资方信号与第四阶段资金闭环一起解读。"
        )
    elif broad_n >= 2:
        pattern = "broad_based"
        label = (
            "**广谱下滑**：至少两个资产维度里多个桶一起承接变差，更像多条线上同时受压，而不是某一两只桶单独作怪。"
        )
    elif broad_n == 1 and hit_n >= 1:
        # 仅一个因子维度呈「因子内多桶普降」且该切片上仍有命中桶：切片级用广谱（单维），避免误标成「集中」
        pattern = "broad_based"
        label = (
            "**广谱下滑（只在一张拆表里）**：只有一个资产维度（例如风险评级）里多个档位一起承接变差，其它维度上未必同步。"
            "这描述的是**客群结构里的承压面**，不是认定「全是资产侧责任」；多档齐跌常与准入/额度在多条线上同时收紧有关，需对照第二阶段资方分布与第四阶段资金侧。"
        )
    elif hit_n >= 1:
        pattern = "concentrated"
        label = (
            "**集中**：少数维度下个别桶明显突出、其它线条相对平稳；不像「一张拆表里全线走弱」。"
            "同样只是在刻画承接结构，不是最终定责。"
        )
    elif broad_n == 1:
        pattern = "broad_based"
        label = (
            "**广谱下滑（仅单维度）**：其中一个资产维度里多个桶承接普遍变差，但该维度尚未形成命中桶时的画像；仍要结合资方与后续阶段解读。"
        )
    else:
        pattern = "no_clear_signal"
        label = (
            "**暂不明确**：资产侧暂时看不出典型的「单点爆桶」或「大面积普跌」结构，叙事要谨慎，交给后续阶段补齐证据。"
        )

    return {
        "asset_dimension_pattern": pattern,
        "asset_dimension_pattern_label": label,
        "asset_dimension_pattern_broad_factor_count": broad_n,
        "asset_dimension_pattern_hit_factor_count": hit_n,
    }


def compute_final_attribution_level(
    *,
    funding_terminal: str | None,
    asset_pattern: str,
    stage2_signal: str | None,
) -> tuple[str, str]:
    """结合第三阶段形态与第四阶段闭环结果输出最终归因定级（中文业务语义）。"""
    pat = normalize_text(asset_pattern) or "no_clear_signal"
    _ = stage2_signal  # 预留：将来可与运营策略/口径微调联动

    if funding_terminal == "R7":
        if pat in {"concentrated", "mixed_pattern"}:
            return (
                "混合驱动",
                "第四阶段已闭环到敏感资方收缩，且第三阶段呈集中或混合资产形态，解释为资方侧收缩与资产结构/桶内承接因素共同作用。",
            )
        if pat == "broad_based":
            return (
                "资方主导",
                "第四阶段已闭环到敏感资方收缩，且第三阶段呈广谱下滑形态，承接率变化更符合准入/规则侧向多桶同步传导。",
            )
        return (
            "资方主导",
            "第四阶段已闭环到敏感资方收缩；资产侧未形成单一桶主导形态时，优先落地资方侧收缩解释。",
        )

    if funding_terminal == "R6":
        if pat in {"concentrated", "mixed_pattern"}:
            return (
                "资产主导（资方待验证）",
                "最小因子范围成立但敏感资方放款未见同步收缩；资产维度呈集中或混合形态时，优先排查资产规则/客群结构，敏感资方侧需交叉验证。",
            )
        return (
            "证据不足（规则/通过率/配置方向）",
            "最小因子范围成立但敏感资方放款未见同步收缩，且资产侧呈广谱或未定型形态，尚不足以单一归因。",
        )

    if funding_terminal == "R8":
        return (
            "证据不足（资金侧无法闭环）",
            "第四阶段未能完成敏感资方侧闭环或存在字段/匹配缺口，不做最终强归因。",
        )

    return ("证据不足", "阶段证据不足以给出明确归因定级。")


def apply_final_attribution_to_funding_trace(
    trace: dict[str, Any],
    asset_trace: dict[str, Any] | None,
) -> dict[str, Any]:
    """写入 `final_attribution_level` 并将定级摘要前置到 `business_view.summary`。"""
    asset_trace = asset_trace or {}
    terminal = trace.get("terminal_reason")
    funding_terminal = terminal if isinstance(terminal, str) else None
    pattern = normalize_text(asset_trace.get("asset_dimension_pattern")) or "no_clear_signal"
    stage2_signal_raw = asset_trace.get("stage2_signal")
    stage2_signal = normalize_text(stage2_signal_raw) if isinstance(stage2_signal_raw, str) else None

    level, rationale = compute_final_attribution_level(
        funding_terminal=funding_terminal,
        asset_pattern=pattern,
        stage2_signal=stage2_signal,
    )
    trace["final_attribution_level"] = level
    trace["final_attribution_rationale"] = rationale
    trace["final_attribution_meta"] = {
        "asset_dimension_pattern": pattern,
        "stage2_signal": stage2_signal,
        "funding_terminal_reason": funding_terminal,
    }

    business = trace.get("business_view")
    if isinstance(business, dict):
        summary = normalize_text(business.get("summary"))
        prefix = f"**【归因定级】{level}。** {rationale}\n\n"
        business["summary"] = prefix + summary if summary else prefix.rstrip()
        trace["business_view"] = business
    return trace


def _build_asset_thresholds(*, current_slice_drag_amount: float) -> dict[str, dict[str, float]]:
    bucket_effective = max(
        ASSET_BUCKET_DRAG_ABSOLUTE_THRESHOLD,
        current_slice_drag_amount * ASSET_BUCKET_DRAG_RELATIVE_THRESHOLD,
    )
    return {
        "bucket": {
            "absolute": round_float(ASSET_BUCKET_DRAG_ABSOLUTE_THRESHOLD, 2),
            "relative": round_float(ASSET_BUCKET_DRAG_RELATIVE_THRESHOLD, 6),
            "effective": round_float(bucket_effective, 2),
        },
        "range": {
            "absolute": round_float(ASSET_RANGE_ROUTE_ABSOLUTE_THRESHOLD, 2),
            "effective": round_float(ASSET_RANGE_ROUTE_ABSOLUTE_THRESHOLD, 2),
        },
    }


def _build_asset_slice_context(
    *,
    current_slice_rate: float,
    baseline_slice_rate: float,
    current_slice_route_amount: float,
    current_slice_drag_amount: float,
) -> dict[str, float]:
    return {
        "current_acceptance_rate": round_float(current_slice_rate, 6),
        "baseline_acceptance_rate": round_float(baseline_slice_rate, 6),
        "current_route_amount": round_float(current_slice_route_amount, 2),
        "slice_drag_amount": round_float(current_slice_drag_amount, 2),
    }


def _asset_signal_type_text(signal_type: str) -> str:
    return {
        "combined": "性能下降 + 结构迁移",
        "perf_decline": "性能下降型",
        "structural": "结构迁移型",
        "below_threshold": "弱信号（未达门槛）",
        "not_applicable": "-",
    }.get(signal_type, "-")


def _asset_bucket_decision_reason(
    *,
    is_target_bucket: bool,
    signal_type: str,
    current_bucket_rate: float | None,
    current_slice_rate: float,
    structural_impact: float,
    perf_decline_impact: float,
    impact_threshold: float,
) -> str:
    if not is_target_bucket:
        return "非业务目标桶，仅作对比参照，不参与命中判断。"
    if current_bucket_rate is None:
        return "当前桶缺少承接率，未命中。"
    if current_bucket_rate >= current_slice_rate:
        return (
            f"当前承接率 {format_percent(current_bucket_rate)} 未低于切片均值 "
            f"{format_percent(current_slice_rate)}，未命中。"
        )
    if signal_type == "not_applicable":
        return "占比未上升且无性能下降信号，未命中。"
    parts: list[str] = []
    if structural_impact > 0:
        parts.append(f"结构迁移影响 {format_wan(structural_impact)}")
    if perf_decline_impact > 0:
        parts.append(f"性能下降影响 {format_wan(perf_decline_impact)}")
    impact_summary = "；".join(parts) if parts else "影响估算为零"
    if signal_type in ("combined", "structural", "perf_decline"):
        return f"{impact_summary}，达到门槛 {format_wan(impact_threshold)}，命中。"
    return f"{impact_summary}，均未达到门槛 {format_wan(impact_threshold)}，未命中。"


def _asset_factor_decision_reason(factor_result: dict[str, Any], bucket_threshold: float) -> str:
    broad_prefix = ""
    broad_prefix = ""
    if factor_result.get("broad_perf_decline"):
        broad_prefix = (
            f"该维度呈多桶普降（{int(factor_result.get('perf_decline_bucket_count', 0))} 个桶下降，"
            f"覆盖当前路由占比 {format_percent_or_dash(factor_result.get('perf_decline_current_share'))}），"
            "最强桶仅代表该维度内影响最大的展示桶，不应单独作为唯一主因；"
        )
    if factor_result["final_decision"] == "hit":
        top_bucket = factor_result["top_bucket"]
        bucket_label = normalize_text(top_bucket.get("bucket_label"))
        signal_type_text = normalize_text(top_bucket.get("signal_type_text")) or "异常信号"
        max_impact = max(
            to_float(top_bucket.get("structural_impact")),
            to_float(top_bucket.get("perf_decline_impact")),
        )
        return (
            f"{broad_prefix}"
            f"命中 {factor_result['hit_bucket_count']} 个异常桶；"
            f"最强桶 {bucket_label} 属于{signal_type_text}，"
            f"最大影响承接金额 {format_wan(max_impact)}，超过门槛 {format_wan(bucket_threshold)}。"
        )
    near_miss_buckets = factor_result.get("near_miss_buckets", [])
    if near_miss_buckets:
        top_bucket = near_miss_buckets[0]
        bucket_label = normalize_text(top_bucket.get("bucket_label"))
        signal_type_text = normalize_text(top_bucket.get("signal_type_text")) or "弱信号"
        max_impact = max(
            to_float(top_bucket.get("structural_impact")),
            to_float(top_bucket.get("perf_decline_impact")),
        )
        return (
            f"{broad_prefix}"
            f"有 {factor_result['near_miss_bucket_count']} 个弱信号桶，但影响均未达到门槛；"
            f"最接近的是 {bucket_label}（{signal_type_text}），"
            f"最大影响承接金额 {format_wan(max_impact)}，低于门槛 {format_wan(bucket_threshold)}。"
        )
    return broad_prefix + "所有桶均未同时满足“占比上升、低于当前切片承接率、单桶影响承接金额估算达到门槛”三项条件。"


def _asset_range_decision_reason(
    *,
    current_route_amount: float,
    current_share: float,
    baseline_share: float,
    current_acceptance_rate: float | None,
    baseline_acceptance_rate: float | None,
    current_slice_rate: float,
    route_amount_threshold: float,
    enter_next_stage: bool,
) -> str:
    if current_route_amount <= 0:
        return "当前期没有形成该候选范围的路由量，不进入下一阶段。"
    if current_acceptance_rate is None:
        return "当前期候选范围缺少承接率，不进入下一阶段。"
    if current_acceptance_rate >= current_slice_rate:
        return (
            f"当前候选范围承接率 {format_percent(current_acceptance_rate)} "
            f"未低于切片均值 {format_percent(current_slice_rate)}，不进入下一阶段。"
        )
    has_structural = current_share > baseline_share
    has_perf_decline = (
        baseline_acceptance_rate is not None
        and current_acceptance_rate < baseline_acceptance_rate
    )
    if not (has_structural or has_perf_decline):
        return "承接率低于切片均值，但占比未上升且无性能下降信号，不进入下一阶段。"
    signal_desc = (
        "结构迁移 + 性能下降"
        if (has_structural and has_perf_decline)
        else ("结构迁移" if has_structural else "性能下降")
    )
    if not enter_next_stage:
        return (
            f"具有{signal_desc}信号，但候选范围当前路由金额 {format_wan(current_route_amount)} "
            f"未达到门槛 {format_wan(route_amount_threshold)}，不进入下一阶段。"
        )
    return (
        f"具有{signal_desc}信号，候选范围当前路由金额 {format_wan(current_route_amount)} "
        f"达到门槛 {format_wan(route_amount_threshold)}，进入下一阶段。"
    )


def _asset_signal_breakdown_text(bucket_items: list[dict[str, Any]]) -> str:
    counts: dict[str, int] = {"combined": 0, "perf_decline": 0, "structural": 0}
    for item in bucket_items:
        signal_type = normalize_text(item.get("signal_type"))
        if signal_type in counts:
            counts[signal_type] += 1
    parts: list[str] = []
    for signal_type in ("combined", "perf_decline", "structural"):
        count = counts[signal_type]
        if count > 0:
            parts.append(f"{_asset_signal_type_text(signal_type)} {count} 个")
    return "；".join(parts)


def _build_factor_results(
    *,
    current_records: list[dict[str, Any]],
    baseline_records: list[dict[str, Any]],
    current_slice_rate: float,
    baseline_slice_rate: float,
    current_slice_route_amount: float,
    asset_thresholds: dict[str, dict[str, float]],
    factor_keys: list[str] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    bucket_threshold = to_float(asset_thresholds["bucket"]["effective"])
    factor_results: list[dict[str, Any]] = []
    hit_buckets: list[dict[str, Any]] = []

    ordered_factor_keys = list(FACTOR_LABELS)
    if factor_keys is not None:
        allowed = frozenset(factor_keys)
        ordered_factor_keys = [key for key in FACTOR_LABELS if key in allowed]

    for factor_key in ordered_factor_keys:
        factor_label = factor_label_for_key(factor_key)
        current_group_map = {
            item["bucket"]: item
            for item in _aggregate_records(_records_for_factor(current_records, factor_key), ["bucket"])
        }
        baseline_group_map = {
            item["bucket"]: item
            for item in _aggregate_records(_records_for_factor(baseline_records, factor_key), ["bucket"])
        }
        current_total_route = sum(to_float(item["route_amount"]) for item in current_group_map.values())
        baseline_total_route = sum(to_float(item["route_amount"]) for item in baseline_group_map.values())
        bucket_results: list[dict[str, Any]] = []

        for bucket in sorted(set(current_group_map) | set(baseline_group_map)):
            current_item = current_group_map.get(bucket, {})
            baseline_item = baseline_group_map.get(bucket, {})
            current_route_amount = to_float(current_item.get("route_amount"))
            baseline_route_amount = to_float(baseline_item.get("route_amount"))
            current_share = safe_div(current_route_amount, current_total_route)
            baseline_share = safe_div(baseline_route_amount, baseline_total_route)
            share_delta = current_share - baseline_share
            current_bucket_rate = (
                round_float(to_float(current_item.get("acceptance_rate")), 6) if current_item else None
            )
            baseline_bucket_rate = (
                round_float(to_float(baseline_item.get("acceptance_rate")), 6)
                if baseline_item and baseline_route_amount > 0
                else None
            )

            # 信号A：结构迁移——占比上升 + 当前承接率低于切片均值
            is_structural_signal = (
                share_delta > 0
                and current_bucket_rate is not None
                and current_bucket_rate < current_slice_rate
            )
            structural_impact = (
                share_delta * current_slice_route_amount
                * max(baseline_slice_rate - to_float(current_bucket_rate), 0.0)
                if is_structural_signal
                else 0.0
            )
            structural_hit = is_structural_signal and structural_impact >= bucket_threshold

            # 信号B：性能下降——桶内承接率同比下降 + 当前承接率低于切片均值
            is_perf_decline_signal = (
                current_bucket_rate is not None
                and baseline_bucket_rate is not None
                and baseline_route_amount > 0
                and current_bucket_rate < baseline_bucket_rate
                and current_bucket_rate < current_slice_rate
            )
            perf_decline_impact = (
                current_share * current_slice_route_amount
                * max(to_float(baseline_bucket_rate) - to_float(current_bucket_rate), 0.0)
                if is_perf_decline_signal
                else 0.0
            )
            perf_decline_hit = is_perf_decline_signal and perf_decline_impact >= bucket_threshold

            is_hit = structural_hit or perf_decline_hit
            is_near_miss = (is_structural_signal or is_perf_decline_signal) and not is_hit

            # 非业务目标桶不参与命中判断（仍展示于表格作对比参照）
            _target_buckets = FACTOR_TARGET_BUCKETS.get(factor_key)
            _bucket_label = bucket_label_for_value(bucket)
            is_target_bucket = _target_buckets is None or _bucket_label in _target_buckets
            if not is_target_bucket:
                is_hit = False
                is_near_miss = False

            if structural_hit and perf_decline_hit:
                signal_type = "combined"
            elif structural_hit:
                signal_type = "structural"
            elif perf_decline_hit:
                signal_type = "perf_decline"
            elif is_structural_signal or is_perf_decline_signal:
                signal_type = "below_threshold"
            else:
                signal_type = "not_applicable"

            bucket_result = {
                "factor_key": factor_key,
                "factor_label": factor_label,
                "bucket": bucket,
                "bucket_label": _bucket_label,
                "current_route_amount": round_float(current_route_amount, 2),
                "baseline_route_amount": round_float(baseline_route_amount, 2),
                "current_acceptance_rate": current_bucket_rate,
                "baseline_acceptance_rate": baseline_bucket_rate,
                "current_route_share": round_float(current_share, 6),
                "baseline_route_share": round_float(baseline_share, 6),
                "share_delta": round_float(share_delta, 6),
                "structural_impact": round_float(structural_impact, 2),
                "perf_decline_impact": round_float(perf_decline_impact, 2),
                "impact_threshold": round_float(bucket_threshold, 2),
                "signal_type": signal_type,
                "signal_type_text": _asset_signal_type_text(signal_type),
                "is_target_bucket": is_target_bucket,
                "is_structural_signal": is_structural_signal,
                "is_perf_decline_signal": is_perf_decline_signal,
                "structural_hit": structural_hit,
                "perf_decline_hit": perf_decline_hit,
                "is_hit": is_hit,
                "is_near_miss": is_near_miss,
            }
            bucket_result["decision_reason"] = _asset_bucket_decision_reason(
                is_target_bucket=is_target_bucket,
                signal_type=signal_type,
                current_bucket_rate=current_bucket_rate,
                current_slice_rate=current_slice_rate,
                structural_impact=structural_impact,
                perf_decline_impact=perf_decline_impact,
                impact_threshold=bucket_threshold,
            )
            bucket_results.append(bucket_result)
            if is_hit:
                hit_buckets.append({
                    "factor_key": factor_key,
                    "factor_label": factor_label,
                    "bucket": bucket,
                    "bucket_label": _bucket_label,
                })

        bucket_results.sort(
            key=lambda item: (
                not bool(item["is_hit"]),
                -max(to_float(item["structural_impact"]), to_float(item["perf_decline_impact"])),
                normalize_text(item["bucket_label"]),
            )
        )
        hit_bucket_results = [item for item in bucket_results if item["is_hit"]]
        near_miss_bucket_results = [item for item in bucket_results if item["is_near_miss"]]
        top_bucket = dict(hit_bucket_results[0]) if hit_bucket_results else None
        comparable_bucket_results = [
            item
            for item in bucket_results
            if item.get("current_acceptance_rate") is not None
            and item.get("baseline_acceptance_rate") is not None
        ]
        perf_decline_bucket_results = [
            item
            for item in comparable_bucket_results
            if to_float(item.get("current_acceptance_rate"))
            < to_float(item.get("baseline_acceptance_rate"))
        ]
        comparable_current_share = sum(
            to_float(item.get("current_route_share"))
            for item in comparable_bucket_results
        )
        perf_decline_current_share = sum(
            to_float(item.get("current_route_share"))
            for item in perf_decline_bucket_results
        )
        broad_perf_decline = (
            len(perf_decline_bucket_results) >= 2
            and comparable_current_share >= 0.8
            and perf_decline_current_share >= 0.8
        )
        factor_result = {
            "factor_key": factor_key,
            "factor_label": factor_label,
            "final_decision": "hit" if hit_bucket_results else "not_hit",
            "decision_reason": "",
            "hit_bucket_count": len(hit_bucket_results),
            "near_miss_bucket_count": len(near_miss_bucket_results),
            "broad_perf_decline": broad_perf_decline,
            "perf_decline_bucket_count": len(perf_decline_bucket_results),
            "perf_decline_current_share": round_float(perf_decline_current_share, 6),
            "comparable_current_share": round_float(comparable_current_share, 6),
            "factor_pattern": "broad_perf_decline" if broad_perf_decline else "localized_or_no_signal",
            "near_miss_buckets": [dict(item) for item in near_miss_bucket_results],
            "top_bucket": top_bucket,
            "buckets": bucket_results,
        }
        factor_result["decision_reason"] = _asset_factor_decision_reason(factor_result, bucket_threshold)
        factor_results.append(factor_result)

    return factor_results, hit_buckets


def _prepare_asset_records(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    base_records = _normalized_metric_rows(
        rows,
        [
            "week",
            "if_irr",
            "cp_dj_new",
            "age_rand",
            "identity_effective_date",
            "identity_province_name",
            "edu_rand",
            "reloan_price_tag",
        ],
    )
    for record in base_records:
        record["identity_bucket"] = factor_bucket_value("identity_effective_date", record.get("identity_effective_date"))
        record["age_bucket"] = factor_bucket_value("age_rand", record.get("age_rand"))
        record["province_bucket"] = factor_bucket_value("identity_province_name", record.get("identity_province_name"))
        record["amount_bucket"] = factor_bucket_value("edu_rand", record.get("edu_rand"))
        record["risk_bucket"] = factor_bucket_value("reloan_price_tag", record.get("reloan_price_tag"))
    return base_records


def _prepare_asset_records_raw(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """资产维度行聚合用原始桶键（仅空白规整，不做身份证/年龄等业务归一）。"""
    base_records = _normalized_metric_rows(
        rows,
        [
            "week",
            "if_irr",
            "cp_dj_new",
            "age_rand",
            "identity_effective_date",
            "identity_province_name",
            "edu_rand",
            "reloan_price_tag",
        ],
    )
    for record in base_records:
        record["identity_bucket"] = bucket_label_for_value(record.get("identity_effective_date"))
        record["age_bucket"] = bucket_label_for_value(record.get("age_rand"))
        record["province_bucket"] = bucket_label_for_value(record.get("identity_province_name"))
        record["amount_bucket"] = bucket_label_for_value(record.get("edu_rand"))
        record["risk_bucket"] = bucket_label_for_value(record.get("reloan_price_tag"))
    return base_records


def _raw_gate_min_declining_required(n_comparable: int) -> int:
    """下降的桶个数下限：不少于 ceil(可比桶×比例) 与全局下限的较大值，且不超过可比桶个数。"""
    if n_comparable <= 0:
        return 0
    need = max(
        ASSET_RAW_GATE_MIN_DECLINING_BUCKETS_FLOOR,
        math.ceil(n_comparable * ASSET_RAW_GATE_DECLINING_BUCKET_RATIO),
    )
    return min(n_comparable, need)


def _format_strongest_declining_bucket_line(
    perf_decline_bucket_results: list[dict[str, Any]],
) -> str:
    """在「当期承接率低于对比期」的桶中，选承接率降幅（pp）最大者（并列则看当期路由占比）。"""
    if not perf_decline_bucket_results:
        return "—"
    def pp_drop(x: dict[str, Any]) -> float:
        return to_float(x.get("baseline_acceptance_rate")) - to_float(x.get("current_acceptance_rate"))

    best = max(
        perf_decline_bucket_results,
        key=lambda x: (pp_drop(x), to_float(x.get("current_route_share"))),
    )
    label = normalize_text(best.get("bucket_label")) or "-"
    cur = to_float(best.get("current_acceptance_rate"))
    base = to_float(best.get("baseline_acceptance_rate"))
    drop_pp = round(pp_drop(best) * 100, 2)
    return (
        f"{label}：当期 {format_percent(cur)}，对比期 {format_percent(base)}（承接率低 {drop_pp} pp）"
    )


def analyze_raw_volume_single_factor(
    *,
    current_records: list[dict[str, Any]],
    baseline_records: list[dict[str, Any]],
    factor_key: str,
    current_slice_rate: float,
) -> dict[str, Any]:
    """
    单因子「广谱走弱」体积规则（须同时满足，阈值见 acceptance_rate_constants）：
    1）可比桶不少于 MIN_COMPARABLE 个；
    2）下降的桶不少于 max(下限, ⌈可比桶×比例⌉) 个；
    3）可比桶、下降桶当期路由合计占本维度均不低于 ROUTE_SHARE_THRESHOLD（默认 90%）。
    不参与业务目标桶白名单过滤；地区等桶多时默认不归一化，靠桶数比例与路由双门槛约束。
    """
    factor_label = factor_label_for_key(factor_key)
    current_group_map = {
        item["bucket"]: item
        for item in _aggregate_records(_records_for_factor(current_records, factor_key), ["bucket"])
    }
    baseline_group_map = {
        item["bucket"]: item
        for item in _aggregate_records(_records_for_factor(baseline_records, factor_key), ["bucket"])
    }
    current_total_route = sum(to_float(item["route_amount"]) for item in current_group_map.values())

    comparable_bucket_results: list[dict[str, Any]] = []
    bucket_preview: list[dict[str, Any]] = []

    for bucket in sorted(set(current_group_map) | set(baseline_group_map)):
        current_item = current_group_map.get(bucket, {})
        baseline_item = baseline_group_map.get(bucket, {})
        current_route_amount = to_float(current_item.get("route_amount"))
        baseline_route_amount = to_float(baseline_item.get("route_amount"))
        current_share = safe_div(current_route_amount, current_total_route)
        current_bucket_rate = (
            round_float(to_float(current_item.get("acceptance_rate")), 6) if current_item else None
        )
        baseline_bucket_rate = (
            round_float(to_float(baseline_item.get("acceptance_rate")), 6)
            if baseline_item and baseline_route_amount > 0
            else None
        )
        _bucket_label = bucket_label_for_value(bucket)
        is_perf_decline = (
            current_bucket_rate is not None
            and baseline_bucket_rate is not None
            and to_float(current_bucket_rate) < to_float(baseline_bucket_rate)
        )
        if current_bucket_rate is not None and baseline_bucket_rate is not None:
            comparable_bucket_results.append(
                {
                    "bucket_label": _bucket_label,
                    "current_acceptance_rate": current_bucket_rate,
                    "baseline_acceptance_rate": baseline_bucket_rate,
                    "current_route_share": current_share,
                }
            )
        bucket_preview.append(
            {
                "bucket_label": _bucket_label,
                "current_acceptance_rate": current_bucket_rate,
                "baseline_acceptance_rate": baseline_bucket_rate,
                "current_route_amount": round_float(current_route_amount, 2),
                "current_route_share": round_float(current_share, 6),
                "below_slice_mean": (
                    current_bucket_rate is not None and to_float(current_bucket_rate) < current_slice_rate
                ),
                "is_perf_decline": is_perf_decline,
            }
        )

    perf_decline_bucket_results = [
        item
        for item in comparable_bucket_results
        if to_float(item.get("current_acceptance_rate")) < to_float(item.get("baseline_acceptance_rate"))
    ]
    comparable_current_share = sum(
        to_float(item.get("current_route_share")) for item in comparable_bucket_results
    )
    perf_decline_current_share = sum(
        to_float(item.get("current_route_share")) for item in perf_decline_bucket_results
    )
    n_comp = len(comparable_bucket_results)
    n_decl = len(perf_decline_bucket_results)
    min_decl_req = _raw_gate_min_declining_required(n_comp)
    count_ok = (
        n_comp >= ASSET_RAW_GATE_MIN_COMPARABLE_BUCKETS
        and n_decl >= min_decl_req
    )
    raw_volume_decline = (
        count_ok
        and comparable_current_share >= ASSET_RAW_GATE_ROUTE_SHARE_THRESHOLD
        and perf_decline_current_share >= ASSET_RAW_GATE_ROUTE_SHARE_THRESHOLD
    )

    bucket_preview.sort(key=lambda row: -to_float(row.get("current_route_amount")))
    declining_over_comparable = (
        f"{len(perf_decline_bucket_results)}/{len(comparable_bucket_results)}"
        if comparable_bucket_results
        else "0/0"
    )
    strongest_decline_text = _format_strongest_declining_bucket_line(perf_decline_bucket_results)
    return {
        "factor_key": factor_key,
        "factor_label": factor_label,
        "raw_volume_decline": raw_volume_decline,
        "comparable_bucket_count": len(comparable_bucket_results),
        "perf_decline_bucket_count": len(perf_decline_bucket_results),
        "declining_over_comparable_text": declining_over_comparable,
        "comparable_current_share": round_float(comparable_current_share, 6),
        "perf_decline_current_share": round_float(perf_decline_current_share, 6),
        "strongest_decline_text": strongest_decline_text,
        "min_declining_buckets_required": min_decl_req,
        "bucket_preview": bucket_preview,
    }


def compute_asset_raw_volume_gate(
    current_rows: list[dict[str, Any]],
    baseline_rows: list[dict[str, Any]],
    current_slice_rate: float,
) -> tuple[list[dict[str, Any]], bool]:
    """返回各因子原始桶体积摘要，以及是否五个因子均满足体积规则普降。"""
    current_raw = _prepare_asset_records_raw(current_rows)
    baseline_raw = _prepare_asset_records_raw(baseline_rows)
    summaries: list[dict[str, Any]] = []
    all_five = True
    for factor_key in FACTOR_LABELS:
        summary = analyze_raw_volume_single_factor(
            current_records=current_raw,
            baseline_records=baseline_raw,
            factor_key=factor_key,
            current_slice_rate=current_slice_rate,
        )
        summaries.append(summary)
        if not summary.get("raw_volume_decline"):
            all_five = False
    return summaries, all_five


ASSET_R12_SUMMARY_TABLE_COLUMNS = [
    {"key": "factor_label", "label": "资产维度"},
    {"key": "raw_gate_pass_text", "label": "本维原始桶普降"},
    {"key": "declining_over_comparable_text", "label": "下降的桶/可比桶（个数）"},
    {"key": "declining_route_share_text", "label": "下降桶路由占本维合计"},
    {"key": "comparable_route_share_text", "label": "可比桶路由占本维合计"},
    {"key": "strongest_decline_text", "label": "承接率下滑最明显的桶"},
]


def _raw_volume_gate_summary_table_rows(factor_summaries: list[dict[str, Any]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in factor_summaries:
        rows.append(
            {
                "factor_label": normalize_text(item.get("factor_label")),
                "raw_gate_pass_text": format_yes_no(bool(item.get("raw_volume_decline"))),
                "declining_over_comparable_text": normalize_text(item.get("declining_over_comparable_text")),
                "declining_route_share_text": format_percent_or_dash(item.get("perf_decline_current_share")),
                "comparable_route_share_text": format_percent_or_dash(item.get("comparable_current_share")),
                "strongest_decline_text": normalize_text(item.get("strongest_decline_text")) or "—",
            }
        )
    return rows


def _r12_compact_example_buckets(preview: list[dict[str, Any]], *, max_buckets: int = 3) -> str:
    """从原始桶预览中取少量代表性桶（优先承接率下降的桶、按当期路由金额），缩短正文篇幅。"""
    if not preview:
        return "（无桶级摘录）"
    declining = [row for row in preview if row.get("is_perf_decline")]
    declining.sort(key=lambda row: -to_float(row.get("current_route_amount")))
    picked: list[dict[str, Any]] = list(declining[:max_buckets])
    seen = {normalize_text(row.get("bucket_label")) for row in picked}
    if len(picked) < max_buckets:
        by_route = sorted(preview, key=lambda row: -to_float(row.get("current_route_amount")))
        for row in by_route:
            label = normalize_text(row.get("bucket_label"))
            if label in seen:
                continue
            picked.append(row)
            seen.add(label)
            if len(picked) >= max_buckets:
                break
    parts: list[str] = []
    for row in picked[:max_buckets]:
        label = normalize_text(row.get("bucket_label")) or "-"
        cur = row.get("current_acceptance_rate")
        base = row.get("baseline_acceptance_rate")
        sh = row.get("current_route_share")
        parts.append(
            f"「{label}」当期 {format_percent_or_dash(cur)} vs 对比 {format_percent_or_dash(base)}"
            f"（当期路由占比 {format_percent_or_dash(sh)}）"
        )
    return "；".join(parts)


def _build_asset_display_r12(
    *,
    slice_display: str,
    slice_context: dict[str, float],
    factor_summaries: list[dict[str, Any]],
    capital_trace: dict[str, Any] | None = None,
) -> dict[str, str]:
    """五维原始桶体积规则全满足时的精简展示（脚本内部终端码 R12；用户可见正文不出现内部码）。"""
    stage2_hint = ""
    if capital_trace:
        sig = normalize_text(capital_trace.get("stage2_signal"))
        if sig == "left_shift":
            stage2_hint = (
                "若第二阶段曾给出「准入分布左移」类路由信号，可与本结论交叉解读（路由信号≠最终归因，"
                "但与多桶同步走弱方向一致时需重视）。"
            )
        elif sig == "no_shift":
            stage2_hint = (
                "第二阶段「未左移」仅表示资方分布的 4-CDF 路由信号未命中；仍建议对照准入加权均值与桶分布，"
                "避免与「五维普降」结论机械对立。"
            )

    summary_table_rows = _raw_volume_gate_summary_table_rows(factor_summaries)

    summary_lines = [
        "### 第三阶段结论",
        f"- 当前切片：{slice_display}",
        "",
        "**判定口径（什么叫这一维「广谱走弱」）**：**可比桶**=两期都能对上承接率；**下降的桶**=当期承接率低于对比期。"
        f"须**同时**满足：① 可比桶至少 **{ASSET_RAW_GATE_MIN_COMPARABLE_BUCKETS}** 个；② 下降的桶不少于 "
        f"**max({ASSET_RAW_GATE_MIN_DECLINING_BUCKETS_FLOOR}, ⌈可比桶数×{int(ASSET_RAW_GATE_DECLINING_BUCKET_RATIO * 100)}%⌉)** 个（桶多时要求「至少一半可比桶在跌」，不靠固定「2」）；"
        f"③ 可比桶、下降的桶的当期路由金额在本维度占比均 **≥ {format_percent(ASSET_RAW_GATE_ROUTE_SHARE_THRESHOLD)}**（默认 90%）。"
        "「地区」等因子原始省份桶很多时**暂不业务归一化**，由「过半桶 + 双路由门槛」共同压住误判。"
        "**本切片五个维度均满足**，整体呈**五维普降**，更像准入/授信规则或额度在多条线上同步变化；本技能**不自动执行**敏感资方资金明细自动核对，请结合第二阶段并按需人工核验。",
        "",
        "#### 五维体积规则摘要",
        build_markdown_table(ASSET_R12_SUMMARY_TABLE_COLUMNS, summary_table_rows),
        "",
        "_列名说明：**本维原始桶普降**在本页均为「是」（否则不会进入本 R12 模板）。"
        "「下降的桶/可比桶」如 27/31，表示 31 个可比桶里有 27 个下降。"
        f"路由合计阈值脚本为 **{format_percent(ASSET_RAW_GATE_ROUTE_SHARE_THRESHOLD)}**；桶数阈值为 "
        f"**≥ max({ASSET_RAW_GATE_MIN_DECLINING_BUCKETS_FLOOR}, ⌈可比×{int(ASSET_RAW_GATE_DECLINING_BUCKET_RATIO * 100)}%⌉)**。"
        "高龄等维度在门禁中使用**取数原始桶键**（如 `6.55` 与 `7.>55` **分列**，不归一成「55+」）。"
        "「承接率下滑最明显的桶」按降幅（pp）最大选取（并列参考当期路由占比）。_",
        "",
        "#### 形态与业务结论（画像≠定责）",
        "- **形态**：各维度均为「大范围承接走弱」，多线同步受压为主，而非孤立异常桶。",
        "- **方向提示**：承接率走弱**较大程度可能与资方准入、授信规则或额度在多条资产线上的同步收紧/迁移有关**。",
        "- **请结合第二阶段**：**准入资方加权均值变化**与**准入家数分布（4-CDF：有效 cutoff 内累计分布相对对比期是否整体抬升）**等结论，与本阶段交叉验证。",
        "- **人工核验**：在资金项目明细中抽查**放款金额、项目数**及**与主表口径的时差**；需要全量拆表明细时再从数据侧导出。",
    ]
    if stage2_hint:
        summary_lines.extend(["", f"- **与第二阶段对照**：{stage2_hint}"])

    summary_lines.extend(
        [
            "",
            f"- 当前承接率：{format_percent(to_float(slice_context['current_acceptance_rate']))}；"
            f"对比期承接率：{format_percent(to_float(slice_context['baseline_acceptance_rate']))}。"
            f" 当前路由金额：{format_wan(to_float(slice_context['current_route_amount']))}；"
            f"当前切片少承接金额估算：{format_wan(to_float(slice_context['slice_drag_amount']))}。",
        ]
    )

    factor_blocks: list[str] = [
        "### 各维度桶级摘录（节选）",
        "> 每维最多列出 **3 个**承接率下降的桶（按当期路由金额优先）；全量明细请在数据侧查询。",
    ]
    for item in factor_summaries:
        label = normalize_text(item.get("factor_label"))
        preview = item.get("bucket_preview") or []
        excerpt = _r12_compact_example_buckets(preview, max_buckets=3)
        factor_blocks.append(f"#### {label}")
        factor_blocks.append(f"- 示例：{excerpt}")

    range_lines = [
        "### 敏感资方与资金明细：本分支说明",
        "本切片在五个资产维度上均表现为「原始桶层面的大范围承接走弱」（见上文**五维体积规则摘要**）。这类结果通常**更贴近授信准入、额度或规则在多条客户线上同步变化**，而不是某一两个桶、某一个维度单独异常。",
        "",
        "因此，本技能在此结果下**不会自动进入第四阶段**（按敏感资方资金项目做逐步闭环核对），避免把「全线走弱」窄化成「只靠少数项目就能解释」。",
        "",
        "**承接率怎么往下归因**：建议**先看第二阶段**已给出的**准入资方加权均值**与**准入家数分布（路由左移/抬升等）**——那是「资方侧是否在收缩」的主证据链；本阶段五维普降与之一致时，更像规则与准入在多线上同步传导。",
        "",
        "**若仍要落到资金项目明细**：可在资金侧按与切片一致的**客群、产品**，并结合上文关心的**桶标签**筛选，自行对比两期**放款规模、项目数**（注意与主表统计口径、时点是否一致）。若另有**授信通过率、头寸**等报表，可作**旁证**，但与第二阶段「路由准入分布」**不是同一指标**，请分开解读、勿混为一谈。",
    ]

    return {
        "summary_markdown": "\n".join(summary_lines),
        "factor_detail_markdown": "\n".join(factor_blocks),
        "range_detail_markdown": "\n".join(range_lines),
    }


def compute_asset_r12_pattern_info() -> dict[str, Any]:
    return {
        "asset_dimension_pattern": "all_factors_raw_volume_decline",
        "asset_dimension_pattern_label": (
            "**五因子原始桶普降**：五个资产维度均满足可比桶体积规则下的「大范围承接走弱」分布，"
            "结构上更接近资方准入/规则在多桶同步传导（≠最终定责）。"
        ),
        "asset_dimension_pattern_broad_factor_count": 5,
        "asset_dimension_pattern_hit_factor_count": 0,
    }


def _records_for_factor(records: list[dict[str, Any]], factor_key: str) -> list[dict[str, Any]]:
    bucket_field = {
        "identity_effective_date": "identity_bucket",
        "age_rand": "age_bucket",
        "identity_province_name": "province_bucket",
        "edu_rand": "amount_bucket",
        "reloan_price_tag": "risk_bucket",
    }[factor_key]
    factor_records: list[dict[str, Any]] = []
    for record in records:
        factor_records.append(
            {
                "bucket": record[bucket_field],
                "route_amount": record["route_amount"],
                "accepted_amount": record["accepted_amount"],
            }
        )
    return factor_records


def _bucket_match(record: dict[str, Any], factor_key: str, bucket: str) -> bool:
    bucket_field = {
        "identity_effective_date": "identity_bucket",
        "age_rand": "age_bucket",
        "identity_province_name": "province_bucket",
        "edu_rand": "amount_bucket",
        "reloan_price_tag": "risk_bucket",
    }[factor_key]
    return normalize_text(record.get(bucket_field)) == normalize_text(bucket)


def _range_signature(range_item: dict[str, Any]) -> frozenset[tuple[str, str]]:
    return frozenset(
        (
            normalize_text(item.get("factor_key")),
            normalize_text(item.get("bucket")),
        )
        for item in range_item.get("factor_items", [])
    )


def _filter_minimal_qualified_ranges(range_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    在「因子集合包含关系」下去掉被真超集覆盖的窄范围；但若窄范围支持资金闭环而宽范围不支持，
    则不因宽范围达标而剔除窄范围（便于第四阶段优先跑敏感资方可映射因子）。
    """
    minimal_ranges: list[dict[str, Any]] = []
    signatures = [_range_signature(item) for item in range_results]
    for index, item in enumerate(range_results):
        current_signature = signatures[index]
        current_funding = bool(item.get("supported_for_funding"))
        superseded_by_wider = any(
            current_signature < other_signature
            and not (
                current_funding
                and not bool(range_results[other_index].get("supported_for_funding"))
            )
            for other_index, other_signature in enumerate(signatures)
            if other_index != index
        )
        if not superseded_by_wider:
            minimal_ranges.append({key: value for key, value in item.items()})
    return minimal_ranges


def _build_range_results(
    *,
    hits: list[dict[str, Any]],
    current_records: list[dict[str, Any]],
    baseline_records: list[dict[str, Any]],
    current_slice_route_amount: float,
    current_slice_rate: float,
    asset_thresholds: dict[str, dict[str, float]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    range_results: list[dict[str, Any]] = []
    range_threshold = to_float(asset_thresholds["range"]["effective"])
    unique_hits = {}
    for hit in hits:
        unique_hits[(hit["factor_key"], hit["bucket"])] = hit
    candidate_hits = list(unique_hits.values())
    baseline_total_route = sum(to_float(item["route_amount"]) for item in baseline_records)

    for range_size in (1, 2, 3):
        for range_hits in combinations(candidate_hits, range_size):
            factor_keys = [item["factor_key"] for item in range_hits]
            if len(set(factor_keys)) != range_size:
                continue
            current_subset = [
                record
                for record in current_records
                if all(_bucket_match(record, item["factor_key"], item["bucket"]) for item in range_hits)
            ]
            baseline_subset = [
                record
                for record in baseline_records
                if all(_bucket_match(record, item["factor_key"], item["bucket"]) for item in range_hits)
            ]
            current_route = sum(to_float(item["route_amount"]) for item in current_subset)
            baseline_route = sum(to_float(item["route_amount"]) for item in baseline_subset)
            current_share = safe_div(current_route, current_slice_route_amount)
            baseline_share = safe_div(baseline_route, baseline_total_route)
            range_current_rate = (
                round_float(
                    safe_div(
                        sum(to_float(item["accepted_amount"]) for item in current_subset),
                        current_route,
                    ),
                    6,
                )
                if current_route > 0
                else None
            )
            range_baseline_rate = (
                round_float(
                    safe_div(
                        sum(to_float(item["accepted_amount"]) for item in baseline_subset),
                        baseline_route,
                    ),
                    6,
                )
                if baseline_route > 0
                else None
            )
            factor_items = normalize_range_factor_items(
                [
                    {
                        "factor_key": item["factor_key"],
                        "factor_label": item["factor_label"],
                        "bucket": item["bucket"],
                    }
                    for item in range_hits
                ]
            )
            range_is_structural = current_share > baseline_share
            range_is_perf_decline = (
                range_current_rate is not None
                and range_baseline_rate is not None
                and baseline_route > 0
                and range_current_rate < range_baseline_rate
                and range_current_rate < current_slice_rate
            )
            enter_next_stage = (
                current_route >= range_threshold
                and range_current_rate is not None
                and range_current_rate < current_slice_rate
                and (range_is_structural or range_is_perf_decline)
            )
            range_result = {
                "range_id": "",
                "range_key": build_range_key(factor_items),
                "range_display": build_range_display(factor_items),
                "factor_count": len(factor_items),
                "factor_items": factor_items,
                "current_share": round_float(current_share, 6),
                "baseline_share": round_float(baseline_share, 6),
                "share_delta": round_float(current_share - baseline_share, 6),
                "current_acceptance_rate": range_current_rate,
                "baseline_acceptance_rate": range_baseline_rate,
                "current_route_amount": round_float(current_route, 2),
                "route_amount_threshold": round_float(range_threshold, 2),
                "enter_next_stage": enter_next_stage,
                "supported_for_funding": all(
                    item["factor_key"] in FUNDING_SUPPORTED_FACTORS
                    for item in range_hits
                ),
            }
            range_result["decision_reason"] = _asset_range_decision_reason(
                current_route_amount=to_float(range_result["current_route_amount"]),
                current_share=current_share,
                baseline_share=baseline_share,
                current_acceptance_rate=range_current_rate,
                baseline_acceptance_rate=range_baseline_rate,
                current_slice_rate=current_slice_rate,
                route_amount_threshold=to_float(range_result["route_amount_threshold"]),
                enter_next_stage=enter_next_stage,
            )
            range_results.append(range_result)

    range_results.sort(
        key=lambda item: (
            not bool(item["enter_next_stage"]),
            -int(item["factor_count"]),
            -to_float(item["current_route_amount"]),
            normalize_text(item["range_key"]),
        )
    )
    for range_index, item in enumerate(range_results, start=1):
        item["range_id"] = f"range_{range_index}"
    qualified_range_candidates = [
        {key: value for key, value in item.items()}
        for item in range_results
        if item["enter_next_stage"]
    ]
    qualified_ranges = _filter_minimal_qualified_ranges(qualified_range_candidates)
    qualified_ranges.sort(
        key=lambda item: (
            not bool(item.get("supported_for_funding")),
            -to_float(item.get("current_route_amount", 0)),
            normalize_text(item.get("range_key", "")),
        )
    )
    for idx, item in enumerate(qualified_ranges, start=1):
        item["range_id"] = f"range_{idx}"
    return range_results, qualified_ranges


def _build_asset_display(
    *,
    slice_display: str,
    slice_context: dict[str, float],
    asset_thresholds: dict[str, dict[str, float]],
    factor_results: list[dict[str, Any]],
    range_results: list[dict[str, Any]],
    qualified_ranges: list[dict[str, Any]],
    soft_signal_buckets: list[dict[str, Any]],
    terminal_reason: str | None,
    asset_dimension_pattern: str | None = None,
    asset_dimension_pattern_label: str | None = None,
    raw_volume_gate_summaries: list[dict[str, Any]] | None = None,
) -> dict[str, str]:
    hit_factor_count = sum(1 for item in factor_results if item["final_decision"] == "hit")
    hit_bucket_count = sum(int(item["hit_bucket_count"]) for item in factor_results)
    soft_signal_factor_count = sum(1 for item in factor_results if int(item.get("near_miss_bucket_count", 0)) > 0)
    hit_bucket_items = [
        dict(bucket)
        for factor_result in factor_results
        for bucket in factor_result["buckets"]
        if bucket["is_hit"]
    ]
    signal_breakdown_source = hit_bucket_items or soft_signal_buckets
    signal_breakdown_text = _asset_signal_breakdown_text(signal_breakdown_source)
    broad_decline_factors = [
        normalize_text(item.get("factor_label"))
        for item in factor_results
        if item.get("broad_perf_decline")
    ]
    entered_range_displays = [normalize_text(item.get("range_display")) for item in qualified_ranges]
    not_entered_range_results = [item for item in range_results if not item["enter_next_stage"]]
    typical_reasons: list[str] = []
    for item in not_entered_range_results:
        reason = normalize_text(item.get("decision_reason"))
        if reason and reason not in typical_reasons:
            typical_reasons.append(reason)
        if len(typical_reasons) >= 2:
            break

    summary_lines = [
        "### 第三阶段结论",
        f"- 当前切片：{slice_display}",
    ]
    if raw_volume_gate_summaries:
        summary_lines += [
            "",
            "#### 五维原始桶体积门禁摘要",
            "- **原始桶**：取数侧桶键（仅空白规整）；高龄 **`6.55`、`7.>55` 等不同写法分列统计**，与本页下方归一化桶（如「55+」）**不是同一套键**，数值差异属预期。",
            "- **本维原始桶普降**：「是」表示该维已同时满足可比桶数、下降桶数与双路由占比门禁——**该维不再进入下方「归一化桶」深链路**。「否」表示须继续参与下方单桶门槛与候选范围组合。",
            "",
            build_markdown_table(
                ASSET_R12_SUMMARY_TABLE_COLUMNS,
                _raw_volume_gate_summary_table_rows(raw_volume_gate_summaries),
            ),
            "",
        ]
    if normalize_text(asset_dimension_pattern_label) and normalize_text(asset_dimension_pattern):
        summary_lines += [
            "",
            "#### 形态判别（资产侧长什么样，≠最终归因）",
            f"- {normalize_text(asset_dimension_pattern_label)}",
            f"- **内部编码（可选，对照日志）**：`{normalize_text(asset_dimension_pattern)}`",
            "- **提醒**：上一段是「结构画像」白话说明，不是定责结论；最终要结合第二阶段资方与第四阶段敏感资方闭环再看。",
            "- **怕混淆读这句**：第三阶段是在拆「客群按维度长什么样」，不是在这步判断「是不是资产部门的问题」。若某一维度里多桶一起跌，常与准入规则、资方可授信量一起在多条线上变化有关，需与资方结论对照，不可单独当最终归因。",
        ]
    summary_lines += [
        f"- 当前承接率：{format_percent(to_float(slice_context['current_acceptance_rate']))}；对比期承接率：{format_percent(to_float(slice_context['baseline_acceptance_rate']))}。",
        f"- 当前路由金额：{format_wan(to_float(slice_context['current_route_amount']))}；当前切片少承接金额估算：{format_wan(to_float(slice_context['slice_drag_amount']))}。",
        (
            f"- 单桶识别门槛：max({format_wan(to_float(asset_thresholds['bucket']['absolute']))}, "
            f"切片少承接金额估算的 {format_percent(to_float(asset_thresholds['bucket']['relative']))}) = "
            f"{format_wan(to_float(asset_thresholds['bucket']['effective']))}。"
        ),
        (
            f"- 候选范围进入下一阶段门槛：候选范围当前路由金额 >= {format_wan(to_float(asset_thresholds['range']['effective']))}，"
            "且候选范围承接率低于切片均值，且具有结构迁移或性能下降信号。"
        ),
    ]
    if signal_breakdown_text:
        summary_lines.append(f"- 已识别异常桶信号类型：{signal_breakdown_text}。")
    if broad_decline_factors:
        summary_lines.append(
            "- 多桶普降提示："
            f"{'、'.join(broad_decline_factors)} 维度存在多个桶承接率同步下降；"
            "若资方分布也已左移，最终结论优先表达为资方准入/规则类影响在多个资产桶内同步体现，不要只把最强桶写成单一主因。"
        )
    if terminal_reason == "R4b":
        if soft_signal_buckets:
            top_soft_signal_bucket_names = [
                f"{normalize_text(item.get('factor_label'))}（{normalize_text(item.get('bucket_label'))}）"
                f"结构影响 {format_wan(to_float(item.get('structural_impact')))} / "
                f"性能影响 {format_wan(to_float(item.get('perf_decline_impact')))}"
                for item in soft_signal_buckets[:3]
            ]
            summary_lines.append(
                f"- 结论：发现 {len(soft_signal_buckets)} 个弱信号桶，涉及 {soft_signal_factor_count} 个资产维度，"
                f"但结构迁移影响和性能下降影响均未达到门槛 {format_wan(to_float(asset_thresholds['bucket']['effective']))}，"
                "当前归因先停在资产维度诊断。"
            )
            for name in top_soft_signal_bucket_names:
                summary_lines.append(f"  - {name}")
        else:
            summary_lines.append("- 结论：所有资产维度均无有效信号（占比未上升，或承接率不低于切片均值，或无同比可比数据），当前归因先停在资产维度诊断。")
        summary_lines.append("- 进入下一阶段的最小因子范围：无。")
    elif terminal_reason == "R5":
        summary_lines.append(
            f"- 结论：已识别 {hit_factor_count} 个资产维度、{hit_bucket_count} 个异常桶，但没有锁定到候选范围当前路由金额达到 {format_wan(to_float(asset_thresholds['range']['effective']))} 的最小因子范围，当前归因先停在资产维度诊断。"
        )
        summary_lines.append("- 进入下一阶段的最小因子范围：无。")
        if typical_reasons:
            summary_lines.append(f"- 未进入下一阶段的典型原因：{'；'.join(typical_reasons)}")
    else:
        summary_lines.append(
            f"- 结论：已识别 {len(qualified_ranges)} 个最小因子范围达到第四阶段门槛，继续看敏感资方侧收缩。"
        )
        # 摘要区不再罗列全部 range_display（多条时与下方「每个候选范围明细」表重复且过长），仅预览前几条。
        displays = [item for item in entered_range_displays if item]
        max_inline_ranges = 5
        if not displays:
            range_preview = "无"
        elif len(displays) <= max_inline_ranges:
            range_preview = "；".join(displays)
        else:
            range_preview = (
                "；".join(displays[:max_inline_ranges])
                + f"；…等共 {len(displays)} 个，完整列表见下方「每个候选范围明细」表格。"
            )
        summary_lines.append(f"- 进入下一阶段的最小因子范围（预览）：{range_preview}")
        if typical_reasons:
            summary_lines.append(f"- 未进入下一阶段的典型原因：{'；'.join(typical_reasons)}")

    partial_deep_chain = bool(
        raw_volume_gate_summaries and len(factor_results) < len(FACTOR_LABELS)
    )
    factor_overview_heading = (
        "### 未通过原始桶门禁的维度·因子总览表"
        if partial_deep_chain
        else "### 全部因子总览表"
    )
    factor_overview_intro = (
        "每行对应一个资产维度，取该维度影响最大的桶（命中优先）。"
        "「最强桶当前/对比承接率」对应该行最强桶在各期的承接率；「单桶影响门槛」= max(绝对下限, 切片少承接金额估算×3%)，与下方明细表口径一致。"
        "「最强桶」仅用于排序和定位，不等同于该维度唯一主因；若「维度结论」提示多桶普降，以多桶普降解释优先。"
        "「是否命中」= 单桶两类影响估算是否至少一类达「单桶影响门槛」；「候选范围进入第四阶段」= 是否存在包含该因子的候选范围且路由金额达下一阶段门槛（详见下方候选范围表）。"
        "性能下降影响按公式「桶在当前维度的路由占比 × 切片路由金额 × 桶承接率降幅」估算；当某桶在该维度下路由占比接近 100%，且桶内承接率降幅接近切片整体降幅时，"
        "该行数值会接近摘要里的「当前切片少承接金额估算」，属代数上的重合而非复制粘贴错误；各行不可纵向相加（同一笔路由在不同维度重复计量）。"
    )
    if partial_deep_chain:
        factor_overview_intro = (
            "**本表仅包含「本维原始桶普降」为否的维度**（已通过上方门禁的维度不再重复跑归一化深链路）。"
            + factor_overview_intro
        )
    factor_overview_lines = [
        factor_overview_heading,
        (factor_overview_intro),
    ]
    factor_overview_rows = []
    for factor_result in factor_results:
        factor_key = normalize_text(factor_result.get("factor_key"))
        overview_bucket = dict(factor_result["buckets"][0]) if factor_result.get("buckets") else {}
        has_entering_range = any(
            bool(item.get("enter_next_stage")) and any(
                normalize_text(factor_item.get("factor_key")) == factor_key
                for factor_item in item.get("factor_items", [])
            )
            for item in range_results
        )
        is_hit = normalize_text(factor_result.get("final_decision")) == "hit"
        decision_reason_text = normalize_text(factor_result.get("decision_reason")) or "-"
        is_hit_text = format_yes_no(is_hit)
        factor_overview_rows.append(
            {
                "factor_label": normalize_text(factor_result.get("factor_label")),
                "top_bucket_label": normalize_text(overview_bucket.get("bucket_label")) or "-",
                "signal_type_text": normalize_text(overview_bucket.get("signal_type_text")) or "-",
                "current_route_share_text": format_percent_or_dash(overview_bucket.get("current_route_share")),
                "baseline_route_share_text": format_percent_or_dash(overview_bucket.get("baseline_route_share")),
                "share_delta_text": format_percent_or_dash(overview_bucket.get("share_delta")),
                "current_acceptance_rate_text": format_percent_or_dash(overview_bucket.get("current_acceptance_rate")),
                "baseline_acceptance_rate_text": format_percent_or_dash(overview_bucket.get("baseline_acceptance_rate")),
                "structural_impact_text": format_wan_or_dash(overview_bucket.get("structural_impact")),
                "perf_decline_impact_text": format_wan_or_dash(overview_bucket.get("perf_decline_impact")),
                "impact_threshold_text": format_wan_or_dash(overview_bucket.get("impact_threshold")),
                # 命中行加粗「是否命中」与「维度结论」，让用户一眼看出关键维度
                "is_hit_text": bold_md(is_hit_text) if is_hit else is_hit_text,
                "has_entering_range_text": format_yes_no(has_entering_range),
                "decision_reason": bold_md(decision_reason_text) if is_hit else decision_reason_text,
            }
        )
    factor_overview_lines.append("")
    factor_overview_lines.append(
        build_markdown_table(ASSET_FACTOR_OVERVIEW_TABLE_COLUMNS, factor_overview_rows)
    )

    factor_lines = [
        *factor_overview_lines,
    ]

    range_lines = [
        "### 每个候选范围明细",
        (
            "下表列出全部候选范围；「是否进入下一阶段」与「进入门槛」「当前路由金额」对照即可判断是否达标。"
            "第四阶段 `--range-key` 必须逐字复制表中「range_key（传给第四阶段脚本）」列。"
        ),
    ]
    range_table_rows = [
        {
            "range_id": normalize_text(item["range_id"]),
            "range_display": normalize_text(item["range_display"]),
            "range_key": normalize_text(item["range_key"]),
            "factor_count_text": str(int(item["factor_count"])),
            "current_share_text": format_percent_or_dash(item["current_share"]),
            "baseline_share_text": format_percent_or_dash(item["baseline_share"]),
            "share_delta_text": emphasize_negative_text(
                format_percent_or_dash(item["share_delta"])
            ),
            "current_acceptance_rate_text": format_percent_or_dash(item["current_acceptance_rate"]),
            "baseline_acceptance_rate_text": format_percent_or_dash(item["baseline_acceptance_rate"]),
            "current_route_amount_text": format_wan_or_dash(item["current_route_amount"]),
            "route_amount_threshold_text": format_wan_or_dash(item["route_amount_threshold"]),
            "enter_next_stage_text": format_yes_no(bool(item["enter_next_stage"])),
            "supported_for_funding_text": format_yes_no(bool(item["supported_for_funding"])),
            "decision_reason": normalize_text(item["decision_reason"]),
        }
        for item in range_results
    ]
    if not range_table_rows:
        range_table_rows = [
            {
                "range_id": "-",
                "range_display": "当前没有可校验的 1 维、2 维或 3 维候选范围",
                "range_key": "-",
                "factor_count_text": "-",
                "current_share_text": "-",
                "baseline_share_text": "-",
                "share_delta_text": "-",
                "current_acceptance_rate_text": "-",
                "baseline_acceptance_rate_text": "-",
                "current_route_amount_text": "-",
                "route_amount_threshold_text": format_wan_or_dash(asset_thresholds["range"]["effective"]),
                "enter_next_stage_text": "否",
                "supported_for_funding_text": "-",
                "decision_reason": "命中的异常桶不足以组成可校验的候选范围。",
            }
        ]
    range_lines.append("")
    range_lines.append(build_markdown_table(ASSET_RANGE_TABLE_COLUMNS, range_table_rows))

    return {
        "summary_markdown": "\n".join(summary_lines),
        "factor_detail_markdown": "\n".join(factor_lines),
        "range_detail_markdown": "\n".join(range_lines),
    }
