from __future__ import annotations

import json
import re
from datetime import datetime
from typing import Any, Callable

import dataworks_client as client

from acceptance_rate_constants import (
    CAPITAL_TOTAL_DROP_RATIO_THRESHOLD,
    FACTOR_LABELS,
    FUNDING_ENTITY,
    MAIN_ENTITY,
    METRIC_ACCEPTANCE_RATE,
    METRIC_CAPITAL_COUNT,
    METRIC_ROUTING_AMOUNT,
    MODEL_SET_NAME,
    PRIMARY_DISPLAY_TABLE_COLUMNS,
    PRIMARY_DRILL_DOWN_ABSOLUTE_THRESHOLD,
    PRIMARY_DRILL_DOWN_MAX_SLICES,
    PRIMARY_DRILL_DOWN_RELATIVE_THRESHOLD,
    TERMINAL_REASON_TEXT,
)


def json_dumps(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).split())


def to_float(value: Any) -> float:
    if value in (None, ""):
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    text = normalize_text(value).replace(",", "")
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


def format_asset_dimension_hit(hit: dict[str, Any]) -> str:
    factor_label = normalize_text(hit.get("factor_label"))
    bucket = normalize_text(hit.get("bucket"))
    share_delta = format_percent(max(to_float(hit.get("share_delta")), 0.0))
    current_rate = format_percent(to_float(hit.get("current_acceptance_rate")))
    drag_amount = format_wan(to_float(hit.get("bucket_drag_amount")))
    drag_threshold = format_wan(to_float(hit.get("bucket_drag_threshold")))
    return (
        f"资产{factor_label}维度的 {bucket} 占比上升 {share_delta}，当前承接率 {current_rate}，"
        f"对应影响路由金额约 {drag_amount}，单桶识别门槛 {drag_threshold}。"
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


def build_slice_display(if_qd: str, irr24_new: str) -> str:
    return f"{normalize_text(if_qd)} | {normalize_text(irr24_new)}"


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


def normalize_combo_factor_items(factor_items: list[dict[str, Any]]) -> list[dict[str, str]]:
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


def build_combo_key(factor_items: list[dict[str, Any]]) -> str:
    normalized_items = normalize_combo_factor_items(factor_items)
    return "&&".join(f'{item["factor_key"]}={item["bucket"]}' for item in normalized_items)


def build_combo_display(factor_items: list[dict[str, Any]]) -> str:
    normalized_items = normalize_combo_factor_items(factor_items)
    return " + ".join(f'{item["factor_label"]}:{item["bucket"]}' for item in normalized_items)


def classify_primary_impact_type(*, delta_rate: float, route_share_delta: float) -> str:
    rate_down = delta_rate < 0
    share_up = route_share_delta > 0
    if rate_down and share_up:
        return "双重影响"
    if rate_down:
        return "承接率下滑"
    if share_up:
        return "结构放大"
    return "其他"


def build_primary_display_rows(abnormal_slices: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in abnormal_slices:
        current_rate = to_float(item.get("current_acceptance_rate"))
        baseline_rate = to_float(item.get("baseline_acceptance_rate"))
        delta_rate = to_float(item.get("acceptance_rate_delta"))
        current_route_amount = to_float(item.get("current_route_amount"))
        drag_amount = to_float(item.get("drag_amount"))
        rows.append(
            {
                "analysis_rank": item.get("analysis_rank"),
                "slice_key": item.get("slice_key"),
                "slice_display": item.get("slice_display"),
                "current_acceptance_rate_text": format_percent(current_rate),
                "baseline_acceptance_rate_text": format_percent(baseline_rate),
                "impact_route_amount_text": format_wan(current_route_amount),
                "drag_route_amount_text": format_wan(drag_amount),
                "acceptance_rate_delta_bp_text": format_bp(delta_rate),
            }
        )
    return rows


def select_primary_drill_down_candidates(
    abnormal_slices: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if not abnormal_slices:
        return [], {
            "absolute_threshold": round_float(PRIMARY_DRILL_DOWN_ABSOLUTE_THRESHOLD, 2),
            "relative_threshold": round_float(PRIMARY_DRILL_DOWN_RELATIVE_THRESHOLD, 6),
            "effective_threshold": round_float(PRIMARY_DRILL_DOWN_ABSOLUTE_THRESHOLD, 2),
            "max_slices": PRIMARY_DRILL_DOWN_MAX_SLICES,
            "total_abnormal_drag_amount": 0.0,
            "threshold_matched_slice_count": 0,
            "selected_slice_count": 0,
            "cap_applied": False,
            "fallback_top1_used": False,
        }

    total_abnormal_drag_amount = sum(to_float(item.get("drag_amount")) for item in abnormal_slices)
    effective_threshold = max(
        PRIMARY_DRILL_DOWN_ABSOLUTE_THRESHOLD,
        total_abnormal_drag_amount * PRIMARY_DRILL_DOWN_RELATIVE_THRESHOLD,
    )
    threshold_matched = [
        item for item in abnormal_slices
        if to_float(item.get("drag_amount")) >= effective_threshold
    ]
    fallback_top1_used = False
    if not threshold_matched:
        candidates = abnormal_slices[:1]
        fallback_top1_used = True
        threshold_matched_slice_count = 0
    else:
        candidates = threshold_matched
        threshold_matched_slice_count = len(threshold_matched)
    cap_applied = len(candidates) > PRIMARY_DRILL_DOWN_MAX_SLICES
    if cap_applied:
        candidates = candidates[:PRIMARY_DRILL_DOWN_MAX_SLICES]
    return candidates, {
        "absolute_threshold": round_float(PRIMARY_DRILL_DOWN_ABSOLUTE_THRESHOLD, 2),
        "relative_threshold": round_float(PRIMARY_DRILL_DOWN_RELATIVE_THRESHOLD, 6),
        "effective_threshold": round_float(effective_threshold, 2),
        "max_slices": PRIMARY_DRILL_DOWN_MAX_SLICES,
        "total_abnormal_drag_amount": round_float(total_abnormal_drag_amount, 2),
        "threshold_matched_slice_count": threshold_matched_slice_count,
        "selected_slice_count": len(candidates),
        "cap_applied": cap_applied,
        "fallback_top1_used": fallback_top1_used,
    }


def build_primary_drill_down_explanation(
    *,
    abnormal_slice_count: int,
    drill_down_rule: dict[str, Any],
) -> str:
    effective_threshold_text = format_wan(to_float(drill_down_rule.get("effective_threshold")))
    total_drag_text = format_wan(to_float(drill_down_rule.get("total_abnormal_drag_amount")))
    max_slices = int(to_float(drill_down_rule.get("max_slices")))
    threshold_matched_slice_count = int(to_float(drill_down_rule.get("threshold_matched_slice_count")))
    selected_slice_count = int(to_float(drill_down_rule.get("selected_slice_count")))
    fallback_top1_used = bool(drill_down_rule.get("fallback_top1_used"))
    cap_applied = bool(drill_down_rule.get("cap_applied"))
    if abnormal_slice_count <= 0:
        return "当前没有承接率下降切片，因此不进入后续切片下钻。"
    rule_prefix = (
        f"当前共定位 {abnormal_slice_count} 个承接率下降切片，表格展示全部切片；"
        "后续下钻规则固定为：先按拖累路由金额门槛筛选，只有拖累路由金额达到 "
        "max(20万, 全部异常切片总拖累金额 × 5%) 的切片才进入后续归因；"
        f"若达到门槛的切片超过 {max_slices} 个，则只继续拖累路由金额最高的前 {max_slices} 个；"
        "若一个都没达到门槛，则保底继续分析拖累路由金额最高的 1 个切片。"
    )
    threshold_formula_text = (
        f"本次全部异常切片总拖累路由金额为 {total_drag_text}，"
        f"因此实际门槛 = max(20万, {total_drag_text} × 5%) = {effective_threshold_text}。"
    )
    if fallback_top1_used:
        return (
            f"{rule_prefix}{threshold_formula_text}"
            "本次没有任何切片达到门槛，因此保底继续分析拖累路由金额最高的 1 个切片。"
        )
    if cap_applied:
        return (
            f"{rule_prefix}{threshold_formula_text}"
            f"本次共有 {threshold_matched_slice_count} 个切片达到门槛，因超过最多继续 {max_slices} 个的上限，"
            f"后续只继续拖累路由金额最高的前 {selected_slice_count} 个。"
        )
    return (
        f"{rule_prefix}{threshold_formula_text}"
        f"本次共有 {threshold_matched_slice_count} 个切片达到门槛，未超过最多继续 {max_slices} 个的上限，"
        f"后续继续这 {selected_slice_count} 个切片。"
    )


def build_primary_analysis_sequence(abnormal_slices: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sequence: list[dict[str, Any]] = []
    for item in abnormal_slices:
        sequence.append(
            {
                "analysis_rank": item.get("analysis_rank"),
                "slice_key": item.get("slice_key"),
                "slice_display": item.get("slice_display"),
                "if_qd": item.get("if_qd"),
                "irr24_new": item.get("irr24_new"),
                "current_acceptance_rate": round_float(to_float(item.get("current_rate")), 6),
                "baseline_acceptance_rate": round_float(to_float(item.get("baseline_rate")), 6),
                "acceptance_rate_delta": round_float(to_float(item.get("delta_rate")), 6),
                "current_route_amount": round_float(to_float(item.get("current_route_amount")), 2),
                "baseline_route_amount": round_float(to_float(item.get("baseline_route_amount")), 2),
                "current_route_share": round_float(to_float(item.get("current_route_share")), 6),
                "baseline_route_share": round_float(to_float(item.get("baseline_route_share")), 6),
                "route_share_delta": round_float(to_float(item.get("route_share_delta")), 6),
                "drag_amount": round_float(to_float(item.get("drag_amount")), 2),
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
    threshold_ratio: float = CAPITAL_TOTAL_DROP_RATIO_THRESHOLD,
    evaluated: bool,
    skipped_reason: str | None = None,
) -> dict[str, Any]:
    current_value = round_float(current, 2)
    baseline_value = round_float(baseline, 2)
    delta = None if current is None or baseline is None else round_float(current - baseline, 2)
    drop = None if current is None or baseline is None else round_float(baseline - current, 2)
    drop_ratio = None
    if current is not None and baseline is not None and baseline > 0:
        drop_ratio = round_float((baseline - current) / baseline, 6)
    hit_drop_threshold = None if drop_ratio is None else drop_ratio >= threshold_ratio
    threshold_ratio_value = round_float(threshold_ratio, 6)
    if not evaluated:
        decision_reason = "当前未完成准入资方总量下降比例判断。"
    elif drop_ratio is None:
        decision_reason = "对比期准入资方个数为 0 或缺失，无法按比例判断是否明显下降。"
    elif hit_drop_threshold:
        decision_reason = (
            f"当前期较对比期下降 {format_percent(drop_ratio)}，"
            f"已超过以上期准入资方个数为基准的 {format_percent(threshold_ratio)} 阈值。"
        )
    else:
        decision_reason = (
            f"当前期较对比期下降 {format_percent(drop_ratio)}，"
            f"未超过以上期准入资方个数为基准的 {format_percent(threshold_ratio)} 阈值。"
        )
    return {
        "evaluated": evaluated,
        "current": current_value,
        "baseline": baseline_value,
        "delta": delta,
        "drop": drop,
        "drop_ratio": drop_ratio,
        "drop_ratio_text": format_percent(drop_ratio) if drop_ratio is not None else "-",
        "threshold": threshold_ratio_value,
        "threshold_ratio": threshold_ratio_value,
        "threshold_ratio_text": format_percent(threshold_ratio),
        "threshold_basis": "baseline_capital_count",
        "hit_drop_threshold": hit_drop_threshold,
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
    }


def build_empty_primary_display() -> dict[str, Any]:
    return {
        "overall_summary": {},
        "table_title": "异常切片（按少承接金额估算排序）",
        "table_columns": PRIMARY_DISPLAY_TABLE_COLUMNS,
        "abnormal_slice_rows": [],
        "markdown_table": "",
        "render_summary": {
            "llm_render_field": "primary_display.markdown_table",
            "display_scope_text": "",
            "drill_down_scope_text": "",
            "must_use_markdown_table_verbatim": True,
            "instruction": "第一阶段给模型展示时只能直接复用 primary_display.markdown_table；table_columns 和 abnormal_slice_rows 只保留给非 LLM 兼容或程序消费，不要根据 analysis_sequence 重新拼表。",
        },
    }


def normalize_slice_component(value: Any) -> str:
    return normalize_text(value).replace(" ", "").lower()


def slice_key_matches(left: str, right: str) -> bool:
    try:
        left_if_qd, left_irr24_new = left.split("|", 1)
        right_if_qd, right_irr24_new = right.split("|", 1)
    except ValueError:
        return normalize_slice_component(left) == normalize_slice_component(right)
    return (
        normalize_slice_component(left_if_qd) == normalize_slice_component(right_if_qd)
        and normalize_slice_component(left_irr24_new) == normalize_slice_component(right_irr24_new)
    )


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
        current_label_start = parse_datetime_text(current_start, is_end=False).date()
        current_label_end = parse_datetime_text(current_end, is_end=True).date()
        baseline_label_start = parse_datetime_text(baseline_start, is_end=False).date()
        baseline_label_end = parse_datetime_text(baseline_end, is_end=True).date()
        context["period_semantics"] = {
            "week_start_day": "monday",
            "display_notation": "[start, end]",
            "primary_query_strategy": "merged_window_then_split",
            "description": "周粒度对话展示优先使用周一到周日的实际分析周段；一级诊断会先把当前期和对比期合成一个总查询窗口，按两段实际日期并集做 dt 筛选，再按周桶拆成 current / baseline。",
        }
        context["current_period_label"] = {
            "start": current_label_start.isoformat(),
            "end": current_label_end.isoformat(),
            "text": f"{current_label_start.isoformat()}~{current_label_end.isoformat()}",
        }
        context["baseline_period_label"] = {
            "start": baseline_label_start.isoformat(),
            "end": baseline_label_end.isoformat(),
            "text": f"{baseline_label_start.isoformat()}~{baseline_label_end.isoformat()}",
        }
    return context


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
    if "无效" in text:
        return "身份证无效"
    if "有效" in text:
        return "身份证有效"
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
    if "新疆" in text:
        return "新疆"
    if "西藏" in text:
        return "西藏"
    return "其他地区"


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
    if factor_key == "grade_level_round":
        return normalize_risk_bucket(raw_value)
    return normalize_text(raw_value)


def parse_age_upper_bound(value: Any) -> int | None:
    text = normalize_text(value)
    if not text:
        return None
    match = re.search(r"(\d+)\s*-\s*(\d+)", text)
    if match:
        return int(match.group(2))
    digits = [int(item) for item in re.findall(r"\d+", text)]
    if digits:
        return digits[-1]
    return None


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
        floor_days = to_float(project_row.get("chk_identity_card_effc_term_floor_days"))
        if bucket == "身份证无效":
            return floor_days > 0
        if bucket == "身份证有效":
            return floor_days <= 0
        return False
    if factor_key == "identity_province_name":
        allowed_provinces = parse_allowed_provinces(project_row.get("allow_identity_city_prov"))
        if bucket in {"新疆", "西藏"}:
            return bool(allowed_provinces) and bucket not in allowed_provinces
        return False
    if factor_key == "age_rand":
        upper_bound = parse_age_upper_bound(project_row.get("age_range"))
        if upper_bound is None:
            return False
        if bucket == "55+":
            return upper_bound < 55
        if bucket == "50-54":
            return upper_bound <= 54
        return False
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
        client.dimension("if_qd", MAIN_ENTITY),
        client.dimension("irr24_new", MAIN_ENTITY),
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
                client.dimension("grade_level_round", MAIN_ENTITY),
            ]
        )
    return dimensions


def build_funding_dimensions() -> list[dict[str, Any]]:
    return [
        client.dimension("age_range", FUNDING_ENTITY),
        client.dimension("allow_identity_city_prov", FUNDING_ENTITY),
        client.dimension("capital_project_name", FUNDING_ENTITY),
        client.dimension("chk_identity_card_effc_term_floor_days", FUNDING_ENTITY),
        client.dimension("cp_dj", FUNDING_ENTITY),
        client.dimension("week", FUNDING_ENTITY, "day"),
    ]


def build_main_rules(
    *,
    start: str,
    end: str,
    if_qd: str | None = None,
    irr24_new: str | None = None,
) -> str:
    rules = [
        client.build_time_rule(
            name="dt",
            entity_name=MAIN_ENTITY,
            start=normalize_boundary(start, is_end=False),
            end=normalize_boundary(end, is_end=True),
        )
    ]
    if if_qd:
        rules.append(client.build_equals_rule(name="if_qd", entity_name=MAIN_ENTITY, value=if_qd))
    if irr24_new:
        rules.append(client.build_equals_rule(name="irr24_new", entity_name=MAIN_ENTITY, value=irr24_new))
    return client.build_filter(rules)


def build_funding_rules(*, start: str, end: str) -> str:
    return client.build_filter(
        [
            client.build_time_rule(
                name="fk_dt",
                entity_name=FUNDING_ENTITY,
                start=normalize_boundary(start, is_end=False),
                end=normalize_boundary(end, is_end=True),
            )
        ]
    )


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
        route_amount = to_float(client.extract_row_value(row, METRIC_ROUTING_AMOUNT))
        acceptance_rate = to_float(client.extract_row_value(row, METRIC_ACCEPTANCE_RATE))
        accepted_amount = route_amount * acceptance_rate
        normalized_row: dict[str, Any] = {
            "route_amount": route_amount,
            "accepted_amount": accepted_amount,
            "acceptance_rate": safe_div(accepted_amount, route_amount),
        }
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
        if "capital_count_metric" in record:
            target["capital_count_metric"] = target.get("capital_count_metric", 0.0) + to_float(record.get("capital_count_metric"))
    for target in grouped.values():
        target["acceptance_rate"] = safe_div(
            to_float(target.get("accepted_amount")),
            to_float(target.get("route_amount")),
        )
    return list(grouped.values())


def _aggregate_slice_map(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    aggregated = _aggregate_records(records, ["if_qd", "irr24_new"])
    slice_map: dict[str, dict[str, Any]] = {}
    for item in aggregated:
        slice_key = f'{item["if_qd"]}|{item["irr24_new"]}'
        item["slice_key"] = slice_key
        slice_map[slice_key] = item
    return slice_map


def _compute_structure_signal(
    *,
    comparisons: list[dict[str, Any]],
    overall_baseline_rate: float,
) -> dict[str, Any]:
    structural_effect = 0.0
    driver_slices: list[dict[str, Any]] = []
    for item in comparisons:
        baseline_rate = item.get("baseline_rate")
        current_share = to_float(item.get("current_route_share"))
        baseline_share = to_float(item.get("baseline_route_share"))
        if baseline_rate is None:
            continue
        share_delta = current_share - baseline_share
        structural_effect += share_delta * (baseline_rate - overall_baseline_rate)
        if share_delta > 0 and baseline_rate < overall_baseline_rate:
            driver_slices.append(
                {
                    "slice_key": item["slice_key"],
                    "baseline_rate": baseline_rate,
                    "share_delta": round_float(share_delta, 6),
                }
            )
    return {
        "is_structural": structural_effect < 0 and bool(driver_slices),
        "structural_effect": round_float(structural_effect, 6),
        "driver_slices": driver_slices,
    }
