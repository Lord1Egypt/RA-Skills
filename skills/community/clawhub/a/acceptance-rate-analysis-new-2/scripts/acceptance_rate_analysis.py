from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from collections import defaultdict
from datetime import datetime
from itertools import combinations
from pathlib import Path
from typing import Any

from loguru import logger


CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

import dataworks_client as client
from acceptance_rate_constants import (
    ASSET_BUCKET_DRAG_ABSOLUTE_THRESHOLD,
    ASSET_BUCKET_DRAG_RELATIVE_THRESHOLD,
    ASSET_COMBO_DRAG_ABSOLUTE_THRESHOLD,
    ASSET_COMBO_DRAG_RELATIVE_THRESHOLD,
    ASSET_COMBO_TABLE_COLUMNS,
    ASSET_FACTOR_TABLE_COLUMNS,
    CAPITAL_TOTAL_DROP_RATIO_THRESHOLD,
    FACTOR_LABELS,
    FUNDING_SUPPORTED_FACTORS,
    FUNDING_ENTITY,
    MAIN_ENTITY,
    METRIC_ACCEPTANCE_RATE,
    METRIC_CAPITAL_COUNT,
    METRIC_FUNDING_AMOUNT,
    METRIC_ROUTING_AMOUNT,
    MODEL_SET_NAME,
    PRIMARY_DRILL_DOWN_ABSOLUTE_THRESHOLD,
    PRIMARY_DRILL_DOWN_MAX_SLICES,
    PRIMARY_DRILL_DOWN_RELATIVE_THRESHOLD,
    PRIMARY_DISPLAY_TABLE_COLUMNS,
    SUPPORTED_GRANULARITIES,
    TERMINAL_REASON_TEXT,
)
DEFAULT_ACCESS_TOKEN = client.DEFAULT_ACCESS_TOKEN
DEBUG_LOG_FILE = CURRENT_DIR / "acceptance_rate_analysis_debug.txt"


def configure_stdio() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8")
            except Exception:
                continue


def configure_debug_logging() -> None:
    DEBUG_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logger.remove()
    logger.add(
        DEBUG_LOG_FILE,
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {name}:{function}:{line} - {message}",
        encoding="utf-8",
        mode="a",
    )
    run_session_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    logger.info("========== 调试会话开始 run_session_id={} log_file={} ==========", run_session_id, str(DEBUG_LOG_FILE))


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
    # 双重影响 = 切片承接率本身下降，同时该切片在当前期路由占比上升。
    # 也就是“切片自己变差”与“结构占比抬升放大影响”同时成立。
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


def log_stage_event(stage: str, event: str, **fields: Any) -> None:
    if fields:
        logger.info(
            "[{}] {} {}",
            stage,
            event,
            json.dumps(fields, ensure_ascii=False, sort_keys=True, default=str),
        )
    else:
        logger.info("[{}] {}", stage, event)


def load_token_from_known_locations() -> str:
    for env_name in (
        "BIGDATA_ACCESS_TOKEN",
        "bigdata_access_token",
        "DATAWORKS_METRIC_QUERY_ACCESS_KEY",
        "dataworks_metric_query_access_key",
    ):
        value = os.getenv(env_name)
        if value:
            return value

    env_path = Path.home() / ".openclaw" / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if "=" not in line:
                continue
            key, raw_value = line.split("=", 1)
            if key.strip() in {
                "BIGDATA_ACCESS_TOKEN",
                "bigdata_access_token",
                "DATAWORKS_METRIC_QUERY_ACCESS_KEY",
                "dataworks_metric_query_access_key",
            }:
                value = raw_value.strip().strip('"').strip("'")
                if value:
                    return value

    return DEFAULT_ACCESS_TOKEN


def resolve_access_token(explicit_token: str | None) -> str:
    if explicit_token:
        return explicit_token
    return load_token_from_known_locations()


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
        item for item in records
        if bucket_value_matches(item.get(time_dimension), granularity=granularity, expected_bucket=current_bucket)
    ]
    baseline_records = [
        item for item in records
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
    predicate,
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


# 第一阶段起，统一改走抽离后的 helper 实现，确保阶段逻辑只依赖外置模块。
from acceptance_rate_support import (
    _aggregate_records,
    _aggregate_slice_map,
    _compute_structure_signal,
    _extract_metric_total,
    _normalized_metric_rows,
    _project_sensitive_to_factor,
    _query_rows,
    bucket_key,
    bucket_label_for_value,
    bucket_route_share,
    bucket_value_matches,
    build_capital_total_judgement,
    build_combo_display,
    build_combo_key,
    build_context,
    build_distribution_judgement,
    build_empty_primary_display,
    build_factor_dimension_trace,
    build_funding_dimensions,
    build_funding_rules,
    build_main_dimensions,
    build_main_rules,
    build_markdown_table,
    build_period_debug_snapshot,
    build_primary_analysis_sequence,
    build_primary_display_rows,
    build_primary_drill_down_explanation,
    build_query_window_label,
    build_reason,
    build_root_cause,
    build_slice_display,
    business_view,
    classify_primary_impact_type,
    factor_bucket_value,
    factor_label_for_key,
    format_asset_dimension_hit,
    format_bp,
    format_percent,
    format_percent_or_dash,
    format_wan,
    format_wan_or_dash,
    format_yes_no,
    json_dumps,
    normalize_boundary,
    normalize_combo_factor_items,
    normalize_cp_dj,
    normalize_granularity,
    normalize_slice_component,
    normalize_text,
    parse_age_upper_bound,
    parse_allow_bucket,
    parse_allowed_provinces,
    parse_datetime_text,
    round_float,
    safe_div,
    select_primary_drill_down_candidates,
    slice_key_matches,
    split_primary_records_by_granularity_bucket,
    stage_analysis_step,
    time_dimension_name,
    to_float,
    union_time_range,
    unsupported_granularity_error,
    validate_granularity_window,
    weighted_median,
)


def run_primary_stage(
    *,
    granularity: str,
    current_start: str,
    current_end: str,
    baseline_start: str,
    baseline_end: str,
    access_token: str,
    endpoint: str | None = None,
    if_qd: str | None = None,
    irr24_new: str | None = None,
) -> dict[str, Any]:
    normalized_granularity = normalize_granularity(granularity)
    time_dimension = time_dimension_name(normalized_granularity)

    logger.info(
        "[run_primary_stage] 开始一级诊断 granularity={} normalized={} "
        "current=[{} ~ {}] baseline=[{} ~ {}] slice_filter=[{}|{}]",
        granularity,
        normalized_granularity,
        current_start,
        current_end,
        baseline_start,
        baseline_end,
        if_qd or "",
        irr24_new or "",
    )

    # 第一步只做一级诊断：
    # 1. 先把当前周期和对比周期合成一个查询窗口，减少重复取数；
    # 2. 再按用户指定粒度对应的时间维度拆成 current / baseline；
    # 3. 最后判断大盘是否下降、是否是结构迁移、是否存在异常切片。
    metrics = [
        client.metric(METRIC_ACCEPTANCE_RATE),
        client.metric(METRIC_ROUTING_AMOUNT),
    ]
    dimensions = build_main_dimensions(granularity=normalized_granularity)
    context = build_context(
        granularity=granularity,
        current_start=current_start,
        current_end=current_end,
        baseline_start=baseline_start,
        baseline_end=baseline_end,
    )

    # 当前版本只明确支持 day / week 两档，避免在未确认口径上静默猜测。
    if normalized_granularity not in SUPPORTED_GRANULARITIES:
        error = unsupported_granularity_error(normalized_granularity)
        logger.warning(
            "[run_primary_stage] 粒度不支持，终止(R8) normalized_granularity={}",
            normalized_granularity,
        )
        return {
            "context": context,
            "overall": {},
            "analysis_sequence": [],
            "structure_signal": {},
            "terminal_reason": "R8",
            "next_action": "stop",
            "primary_display": build_empty_primary_display(),
            "business_view": business_view(
                headline="当前粒度暂未接入",
                summary="当前版本仅支持日粒度和周粒度的一级诊断。",
                evidence=[f"收到粒度：{normalized_granularity}。"],
            ),
            "errors": [error],
        }

    # 单个分析窗口必须只落在一个粒度桶内，否则 current / baseline 会产生歧义。
    current_window_error = validate_granularity_window(normalized_granularity, current_start, current_end)
    baseline_window_error = validate_granularity_window(normalized_granularity, baseline_start, baseline_end)
    if current_window_error or baseline_window_error:
        errors = [item for item in [current_window_error, baseline_window_error] if item]
        logger.warning(
            "[run_primary_stage] 时间窗校验失败，终止(R8) errors={}",
            errors,
        )
        return {
            "context": context,
            "overall": {},
            "analysis_sequence": [],
            "structure_signal": {},
            "terminal_reason": "R8",
            "next_action": "stop",
            "primary_display": build_empty_primary_display(),
            "business_view": business_view(
                headline="一级诊断时间窗不满足当前粒度要求",
                summary="当前时间窗跨越了多个粒度桶，暂时无法直接计算当前期与对比期。",
                evidence=errors,
            ),
            "errors": errors,
        }

    logger.debug(
        "[run_primary_stage] 粒度与时间窗校验通过 time_dimension={}",
        time_dimension,
    )

    query_start, query_end = union_time_range(
        current_start=current_start,
        current_end=current_end,
        baseline_start=baseline_start,
        baseline_end=baseline_end,
    )
    # 第一级只保留汇总和固定表格，不再把原始查询明细直接回传给上层模型。
    query_result, query_error = _query_rows(
        access_token=access_token,
        metric_list=metrics,
        dimension_list=dimensions,
        filter_payload=build_main_rules(
            start=query_start,
            end=query_end,
            if_qd=if_qd,
            irr24_new=irr24_new,
        ),
        endpoint=endpoint,
    )

    if query_error:
        trace = {
            "context": context,
            "overall": {},
            "analysis_sequence": [],
            "structure_signal": {},
            "terminal_reason": "R8",
            "next_action": "stop",
            "primary_display": build_empty_primary_display(),
            "business_view": business_view(
                headline="当前无法完成一级诊断",
                summary="主数据查询失败，暂时无法判断承接率是否下降。",
                evidence=[query_error],
            ),
            "errors": [query_error],
        }
        return trace

    all_records = _normalized_metric_rows(query_result.get("rows", []), [time_dimension, "if_qd", "irr24_new"])
    
    current_records, baseline_records = split_primary_records_by_granularity_bucket(
        records=all_records,
        granularity=normalized_granularity,
        current_start=current_start,
        current_end=current_end,
        baseline_start=baseline_start,
        baseline_end=baseline_end,
    )

    if not current_records or not baseline_records:
        errors: list[str] = []
        if not current_records:
            errors.append(f"当前周期未匹配到粒度桶 {bucket_key(current_start, granularity=normalized_granularity, is_end=False)} 的数据。")
        if not baseline_records:
            errors.append(f"对比周期未匹配到粒度桶 {bucket_key(baseline_start, granularity=normalized_granularity, is_end=False)} 的数据。")
        return {
            "context": context,
            "overall": {},
            "analysis_sequence": [],
            "structure_signal": {},
            "terminal_reason": "R8",
            "next_action": "stop",
            "primary_display": build_empty_primary_display(),
            "business_view": business_view(
                headline="一级诊断数据不足",
                summary="单次查询已完成，但当前周期或对比周期没有匹配到可用于对比的周桶数据。",
                evidence=errors,
            ),
            "errors": errors,
        }

    # 先把 current / baseline 各自聚合成切片 map，再计算大盘和切片级变化。
    current_slice_map = _aggregate_slice_map(current_records)
    baseline_slice_map = _aggregate_slice_map(baseline_records)

    current_route_amount = sum(to_float(item["route_amount"]) for item in current_slice_map.values())
    baseline_route_amount = sum(to_float(item["route_amount"]) for item in baseline_slice_map.values())
    current_accepted_amount = sum(to_float(item["accepted_amount"]) for item in current_slice_map.values())
    baseline_accepted_amount = sum(to_float(item["accepted_amount"]) for item in baseline_slice_map.values())

    current_rate = safe_div(current_accepted_amount, current_route_amount)
    baseline_rate = safe_div(baseline_accepted_amount, baseline_route_amount)
    overall_delta = current_rate - baseline_rate

    # 切片层同时保留：
    # - 切片自身承接率变化 delta_rate
    # - 当前期路由金额
    # - 结构迁移要看的占比变化 route_share_delta
    # - 影响排序要看的 drag_amount
    comparisons: list[dict[str, Any]] = []
    all_slice_keys = sorted(set(current_slice_map) | set(baseline_slice_map))
    abnormal_slices: list[dict[str, Any]] = []
    for slice_key in all_slice_keys:
        current_item = current_slice_map.get(slice_key, {})
        baseline_item = baseline_slice_map.get(slice_key, {})
        current_slice_rate = current_item.get("acceptance_rate")
        baseline_slice_rate = baseline_item.get("acceptance_rate")
        current_slice_route = to_float(current_item.get("route_amount"))
        baseline_slice_route = to_float(baseline_item.get("route_amount"))
        current_route_share = safe_div(current_slice_route, current_route_amount)
        baseline_route_share = safe_div(baseline_slice_route, baseline_route_amount)
        delta_rate = None
        drag_amount = 0.0
        if current_item and baseline_item:
            delta_rate = to_float(current_slice_rate) - to_float(baseline_slice_rate)
            drag_amount = max(to_float(baseline_slice_rate) - to_float(current_slice_rate), 0.0) * current_slice_route

        comparison = {
            "slice_key": slice_key,
            "slice_display": build_slice_display(
                current_item.get("if_qd") or baseline_item.get("if_qd") or "",
                current_item.get("irr24_new") or baseline_item.get("irr24_new") or "",
            ),
            "if_qd": current_item.get("if_qd") or baseline_item.get("if_qd") or "",
            "irr24_new": current_item.get("irr24_new") or baseline_item.get("irr24_new") or "",
            "current_rate": round_float(current_slice_rate, 6) if current_item else None,
            "baseline_rate": round_float(baseline_slice_rate, 6) if baseline_item else None,
            "delta_rate": round_float(delta_rate, 6),
            "current_route_amount": round_float(current_slice_route, 2),
            "baseline_route_amount": round_float(baseline_slice_route, 2),
            "current_route_share": round_float(current_route_share, 6),
            "baseline_route_share": round_float(baseline_route_share, 6),
            "route_share_delta": round_float(current_route_share - baseline_route_share, 6),
            "drag_amount": round_float(drag_amount, 2),
        }
        comparisons.append(comparison)
        if delta_rate is not None and delta_rate < 0:
            abnormal_slices.append(comparison)

    abnormal_slices.sort(key=lambda item: (to_float(item["drag_amount"]), abs(to_float(item["delta_rate"]))), reverse=True)
    for index, item in enumerate(abnormal_slices, start=1):
        item["analysis_rank"] = index
    structure_signal = _compute_structure_signal(
        comparisons=comparisons,
        overall_baseline_rate=baseline_rate,
    )
    selected_slices, drill_down_rule = select_primary_drill_down_candidates(abnormal_slices)
    analysis_sequence = build_primary_analysis_sequence(selected_slices)
    drill_down_explanation = build_primary_drill_down_explanation(
        abnormal_slice_count=len(abnormal_slices),
        drill_down_rule=drill_down_rule,
    )

    terminal_reason: str | None = None
    next_action = "run_capital"
    if overall_delta >= 0:
        terminal_reason = "R1"
        next_action = "stop"
    elif not abnormal_slices and structure_signal["is_structural"]:
        terminal_reason = "R2"
        next_action = "stop"
    elif not abnormal_slices:
        terminal_reason = "R8"
        next_action = "stop"

    if terminal_reason == "R1":
        business = business_view(
            headline="大盘承接率未下降",
            summary="当前周期整体承接率未低于对比周期，不需要继续下钻异常切片。",
            evidence=[
                f'当前承接率 {round_float(current_rate, 6)}，对比期承接率 {round_float(baseline_rate, 6)}。',
            ],
        )
    elif terminal_reason == "R2":
        business = business_view(
            headline="更偏向一级切片结构迁移",
            summary="切片自身承接率未明显变差，但低承接率切片占比上升，导致大盘下降。",
            evidence=[
                f'结构效应 {structure_signal["structural_effect"]}。',
                f'结构迁移切片数 {len(structure_signal["driver_slices"])}。',
            ],
        )
    elif terminal_reason == "R8":
        business = business_view(
            headline="一级诊断证据不足",
            summary="大盘下降，但当前一级切片证据不足以继续归因。",
            evidence=[],
        )
    else:
        business = business_view(
            headline="已定位异常切片",
            summary=(
                f"大盘下降，已定位 {len(abnormal_slices)} 个异常切片；"
                "表格会展示全部异常切片，后续会先按拖累路由金额门槛筛选；"
                "达到门槛的切片最多继续 5 个，若一个都没达到门槛则保底继续 1 个。"
            ),
            evidence=[
                f'大盘承接率从 {round_float(baseline_rate, 6)} 下降到 {round_float(current_rate, 6)}。',
                drill_down_explanation,
            ],
        )

    all_abnormal_rows = build_primary_display_rows(build_primary_analysis_sequence(abnormal_slices))
    primary_display = {
        "overall_summary": {
            "current_acceptance_rate": round_float(current_rate, 6),
            "baseline_acceptance_rate": round_float(baseline_rate, 6),
            "acceptance_rate_delta": round_float(overall_delta, 6),
            "acceptance_rate_delta_bp": round_float(overall_delta * 10000, 2),
            "current_acceptance_rate_text": format_percent(current_rate),
            "baseline_acceptance_rate_text": format_percent(baseline_rate),
            "acceptance_rate_delta_bp_text": format_bp(overall_delta),
            "current_route_amount": round_float(current_route_amount, 2),
            "baseline_route_amount": round_float(baseline_route_amount, 2),
            "current_route_amount_text": format_wan(current_route_amount),
            "baseline_route_amount_text": format_wan(baseline_route_amount),
            "abnormal_slice_count": len(abnormal_slices),
            "drill_down_slice_count": len(analysis_sequence),
            "drill_down_drag_threshold": drill_down_rule["effective_threshold"],
            "drill_down_drag_threshold_text": format_wan(to_float(drill_down_rule["effective_threshold"])),
            "drill_down_rule_text": drill_down_explanation,
        },
        "table_title": "异常切片（按少承接金额估算排序）",
        "table_columns": PRIMARY_DISPLAY_TABLE_COLUMNS,
        "abnormal_slice_rows": all_abnormal_rows,
        "markdown_table": build_markdown_table(PRIMARY_DISPLAY_TABLE_COLUMNS, all_abnormal_rows),
        "render_summary": {
            "llm_render_field": "primary_display.markdown_table",
            "llm_followup_field": "primary_display.render_summary.drill_down_scope_text",
            "display_scope_text": f"异常切片表展示全部 {len(abnormal_slices)} 个承接率下降切片。",
            "drill_down_scope_text": drill_down_explanation,
            "must_use_markdown_table_verbatim": True,
            "must_show_drill_down_scope_text": True,
            "instruction": "第一阶段给模型展示时必须按顺序输出：1. 原样复用 primary_display.markdown_table；2. 紧跟着原样展示 primary_display.render_summary.drill_down_scope_text。table_columns 和 abnormal_slice_rows 只保留给非 LLM 兼容或程序消费，不要根据 analysis_sequence 重新拼表。",
        },
    }

    trace = {
        "context": context,
        "overall": {
            "current_acceptance_rate": round_float(current_rate, 6),
            "baseline_acceptance_rate": round_float(baseline_rate, 6),
            "delta_rate": round_float(overall_delta, 6),
            "current_route_amount": round_float(current_route_amount, 2),
            "baseline_route_amount": round_float(baseline_route_amount, 2),
            "is_declining": overall_delta < 0,
        },
        "analysis_sequence": analysis_sequence,
        "structure_signal": structure_signal,
        "terminal_reason": terminal_reason,
        "next_action": next_action,
        "drill_down_rule": drill_down_rule,
        "primary_display": primary_display,
        "business_view": business,
        "errors": [],
    }
    log_stage_event(
        "primary",
        "阶段完成",
        trace=trace,
    )
    return trace


def run_capital_stage(
    *,
    granularity: str,
    current_start: str,
    current_end: str,
    baseline_start: str,
    baseline_end: str,
    slice_key: str,
    access_token: str,
    endpoint: str | None = None,
) -> dict[str, Any]:
    normalized_granularity = normalize_granularity(granularity)
    log_stage_event(
        "capital",
        "开始阶段",
        slice_key=slice_key,
        granularity=normalized_granularity,
        current_start=current_start,
        current_end=current_end,
        baseline_start=baseline_start,
        baseline_end=baseline_end,
    )
    context = build_context(
        granularity=granularity,
        current_start=current_start,
        current_end=current_end,
        baseline_start=baseline_start,
        baseline_end=baseline_end,
    )
    if normalized_granularity not in SUPPORTED_GRANULARITIES:
        error = unsupported_granularity_error(normalized_granularity)
        trace = {
            "context": context,
            "slice_key": slice_key,
            "slice_display": slice_key,
            "capital_distribution_stats": [],
            "weighted_mean_delta": None,
            "weighted_median_delta": None,
            "low_bucket_share_delta": {},
            "high_bucket_share_delta": {},
            "analysis_steps": [
                stage_analysis_step(
                    step="粒度校验",
                    analysis="先确认当前阶段是否支持这个粒度。",
                    evidence=[error],
                    conclusion="当前版本不支持这个粒度，第二阶段停止执行。",
                )
            ],
            "terminal_reason": "R8",
            "terminal_reason_text": build_reason("R8"),
            "next_action": "stop",
            "business_view": business_view(
                headline="当前粒度暂未接入",
                summary="当前版本仅支持日粒度和周粒度的资方分布诊断。",
                evidence=[error],
            ),
            "root_cause": build_root_cause(
                "unsupported_granularity",
                "资方分布阶段收到当前版本未支持的粒度。",
                granularity=normalized_granularity,
            ),
            "errors": [error],
        }
        log_stage_event("capital", "阶段失败", slice_key=slice_key, trace=trace)
        return trace
    current_period = context["current_period"]
    baseline_period = context["baseline_period"]

    if_qd, irr24_new = slice_key.split("|", 1)
    slice_display = build_slice_display(if_qd, irr24_new)
    total_capital_drop_ratio_threshold = CAPITAL_TOTAL_DROP_RATIO_THRESHOLD
    total_metrics = [client.metric(METRIC_CAPITAL_COUNT)]
    total_dimensions = build_main_dimensions(granularity=normalized_granularity)
    current_filter = build_main_rules(
        start=current_period["start"],
        end=current_period["end"],
        if_qd=if_qd,
        irr24_new=irr24_new,
    )
    baseline_filter = build_main_rules(
        start=baseline_period["start"],
        end=baseline_period["end"],
        if_qd=if_qd,
        irr24_new=irr24_new,
    )

    current_total_result, current_total_error = _query_rows(
        access_token=access_token,
        metric_list=total_metrics,
        dimension_list=total_dimensions,
        filter_payload=current_filter,
        endpoint=endpoint,
    )
    baseline_total_result, baseline_total_error = _query_rows(
        access_token=access_token,
        metric_list=total_metrics,
        dimension_list=total_dimensions,
        filter_payload=baseline_filter,
        endpoint=endpoint,
    )

    if current_total_error or baseline_total_error:
        log_stage_event(
            "capital",
            "阶段失败",
            slice_key=slice_key,
            errors=[item for item in [current_total_error, baseline_total_error] if item],
        )
        trace = {
            "context": context,
            "slice_key": slice_key,
            "slice_display": slice_display,
            "capital_distribution_stats": [],
            "capital_total_judgement": build_capital_total_judgement(
                evaluated=False,
                threshold_ratio=total_capital_drop_ratio_threshold,
                skipped_reason="capital_total_query_error",
            ),
            "distribution_judgement": build_distribution_judgement(
                evaluated=False,
                skipped_reason="capital_total_query_error",
            ),
            "analysis_steps": [
                stage_analysis_step(
                    step="准入资方总量取数",
                    analysis="先取这组订单当前期和对比期的准入资方总量指标。",
                    evidence=[item for item in [current_total_error, baseline_total_error] if item],
                    conclusion="总量查询失败，当前无法判断是否命中资方总量明显减少分支。",
                )
            ],
            "terminal_reason": "R8",
            "terminal_reason_text": build_reason("R8"),
            "next_action": "stop",
            "business_view": business_view(
                headline="没拿到准入资方总量结果",
                summary="第二阶段的第一步就没拿到准入资方总量，因此当前无法判断是否直接命中资方总量减少分支。",
                evidence=[item for item in [current_total_error, baseline_total_error] if item],
            ),
            "root_cause": build_root_cause(
                "query_error",
                "准入资方总量查询失败。",
                slice_key=slice_key,
                slice_display=slice_display,
                current_error=current_total_error,
                baseline_error=baseline_total_error,
            ),
            "errors": [item for item in [current_total_error, baseline_total_error] if item],
            "debug_query": build_period_debug_snapshot(
                current_result=current_total_result,
                baseline_result=baseline_total_result,
                current_filter=current_filter,
                baseline_filter=baseline_filter,
            ),
        }
        return trace

    current_total_rows = current_total_result.get("rows", [])
    baseline_total_rows = baseline_total_result.get("rows", [])
    if not current_total_rows or not baseline_total_rows:
        errors: list[str] = []
        if not current_total_rows:
            errors.append("当前周期没有拿到这组订单的准入资方总量数据。")
        if not baseline_total_rows:
            errors.append("对比周期没有拿到这组订单的准入资方总量数据。")
        trace = {
            "context": context,
            "slice_key": slice_key,
            "slice_display": slice_display,
            "capital_distribution_stats": [],
            "capital_total_judgement": build_capital_total_judgement(
                evaluated=False,
                threshold_ratio=total_capital_drop_ratio_threshold,
                skipped_reason="capital_total_data_missing",
            ),
            "distribution_judgement": build_distribution_judgement(
                evaluated=False,
                skipped_reason="capital_total_data_missing",
            ),
            "analysis_steps": [
                stage_analysis_step(
                    step="准入资方总量取数",
                    analysis="先取这组订单当前期和对比期的准入资方总量指标。",
                    evidence=errors,
                    conclusion="当前期或对比期缺少可比总量数据，当前无法继续判断。",
                )
            ],
            "terminal_reason": "R8",
            "terminal_reason_text": build_reason("R8"),
            "next_action": "stop",
            "business_view": business_view(
                headline="没拿到准入资方总量数据",
                summary="当前期或对比期缺少这组订单的可比准入资方总量，暂时不能判断是否命中资方总量减少分支。",
                evidence=errors,
            ),
            "root_cause": build_root_cause(
                "missing_capital_total_data",
                "资方分布阶段缺少当前期或对比期的准入资方总量数据。",
                slice_key=slice_key,
                slice_display=slice_display,
                current_row_count=len(current_total_rows),
                baseline_row_count=len(baseline_total_rows),
                current_period=current_period,
                baseline_period=baseline_period,
            ),
            "errors": errors,
            "debug_query": build_period_debug_snapshot(
                current_result=current_total_result,
                baseline_result=baseline_total_result,
                current_filter=current_filter,
                baseline_filter=baseline_filter,
            ),
        }
        log_stage_event("capital", "阶段失败", slice_key=slice_key, trace=trace)
        return trace

    total_capital_count_current, has_current_total_metric = _extract_metric_total(current_total_rows, METRIC_CAPITAL_COUNT)
    total_capital_count_baseline, has_baseline_total_metric = _extract_metric_total(baseline_total_rows, METRIC_CAPITAL_COUNT)
    if not has_current_total_metric or not has_baseline_total_metric:
        errors: list[str] = []
        if not has_current_total_metric:
            errors.append("当前周期缺少准入资方总量指标字段。")
        if not has_baseline_total_metric:
            errors.append("对比周期缺少准入资方总量指标字段。")
        trace = {
            "context": context,
            "slice_key": slice_key,
            "slice_display": slice_display,
            "capital_distribution_stats": [],
            "capital_total_judgement": build_capital_total_judgement(
                evaluated=False,
                threshold_ratio=total_capital_drop_ratio_threshold,
                skipped_reason="capital_total_metric_missing",
            ),
            "distribution_judgement": build_distribution_judgement(
                evaluated=False,
                skipped_reason="capital_total_metric_missing",
            ),
            "analysis_steps": [
                stage_analysis_step(
                    step="准入资方总量取数",
                    analysis="先取这组订单当前期和对比期的准入资方总量指标。",
                    evidence=errors,
                    conclusion="总量字段缺失，当前无法继续判断。",
                )
            ],
            "terminal_reason": "R8",
            "terminal_reason_text": build_reason("R8"),
            "next_action": "stop",
            "business_view": business_view(
                headline="准入资方总量字段缺失",
                summary="总量查询有返回，但缺少准入资方总量这个关键字段，当前无法进入后续判断分支。",
                evidence=errors,
            ),
            "root_cause": build_root_cause(
                "capital_total_metric_missing",
                "准入资方总量指标字段缺失。",
                slice_key=slice_key,
                slice_display=slice_display,
            ),
            "errors": errors,
            "debug_query": build_period_debug_snapshot(
                current_result=current_total_result,
                baseline_result=baseline_total_result,
                current_filter=current_filter,
                baseline_filter=baseline_filter,
            ),
        }
        log_stage_event("capital", "阶段失败", slice_key=slice_key, trace=trace)
        return trace

    capital_total_judgement = build_capital_total_judgement(
        current=total_capital_count_current,
        baseline=total_capital_count_baseline,
        threshold_ratio=total_capital_drop_ratio_threshold,
        evaluated=True,
    )
    if capital_total_judgement["hit_drop_threshold"]:
        distribution_judgement = build_distribution_judgement(
            evaluated=False,
            skipped_reason="capital_total_drop_threshold_hit",
        )
        trace = {
            "context": context,
            "slice_key": slice_key,
            "slice_display": slice_display,
            "capital_distribution_stats": [],
            "capital_total_judgement": capital_total_judgement,
            "distribution_judgement": distribution_judgement,
            "analysis_steps": [
                stage_analysis_step(
                    step="准入资方总量判断",
                    analysis="先看这组订单的准入资方总量有没有明显下降。",
                    evidence=[
                        f"当前准入资方总量：{capital_total_judgement['current']}。",
                        f"对比期准入资方总量：{capital_total_judgement['baseline']}。",
                        f"减少量：{capital_total_judgement['drop']}，下降比例：{capital_total_judgement['drop_ratio_text']}。",
                        f"判断阈值：以上期准入资方个数为基准，下降超过 {capital_total_judgement['threshold_ratio_text']}。",
                    ],
                    conclusion=(
                        f"当前准入资方总量较对比期下降 {capital_total_judgement['drop_ratio_text']}，"
                        f"超过 {capital_total_judgement['threshold_ratio_text']} 阈值，直接命中资方总量明显减少分支。"
                    ),
                ),
                stage_analysis_step(
                    step="资方桶分布偏移判断",
                    analysis="总量分支已经命中，因此不再继续看桶分布。",
                    evidence=[],
                    conclusion="本步跳过。",
                    status="skipped",
                ),
                stage_analysis_step(
                    step="授用信通过率兜底",
                    analysis="总量分支已经完成归因，不再进入兜底判断。",
                    evidence=[],
                    conclusion="本步跳过。",
                    status="skipped",
                ),
            ],
            "terminal_reason": "R3",
            "terminal_reason_text": build_reason("R3"),
            "next_action": "stop",
            "business_view": business_view(
                headline="这组订单的准入资方总量明显减少",
                summary="第二阶段先看总量下降比例就已经命中阈值，说明这组订单当前更像是资方总供给收缩，不需要再看资方桶分布。",
                evidence=[
                    f"当前准入资方总量 {capital_total_judgement['current']}，对比期 {capital_total_judgement['baseline']}。",
                    f"总量减少 {capital_total_judgement['drop']}，下降比例 {capital_total_judgement['drop_ratio_text']}。",
                    f"判断阈值：以上期准入资方个数为基准，下降超过 {capital_total_judgement['threshold_ratio_text']}。",
                ],
            ),
            "root_cause": build_root_cause(
                "capital_supply_total_drop",
                "资方总量明显减少，第二阶段已直接停在资方侧。",
                slice_key=slice_key,
                slice_display=slice_display,
                capital_total_judgement=capital_total_judgement,
            ),
            "errors": [],
        }
        log_stage_event("capital", "阶段完成", slice_key=slice_key, trace=trace)
        return trace

    distribution_metrics = [
        client.metric(METRIC_ACCEPTANCE_RATE),
        client.metric(METRIC_ROUTING_AMOUNT),
    ]
    distribution_dimensions = build_main_dimensions(granularity=normalized_granularity, include_allow=True)
    current_result, current_error = _query_rows(
        access_token=access_token,
        metric_list=distribution_metrics,
        dimension_list=distribution_dimensions,
        filter_payload=current_filter,
        endpoint=endpoint,
    )
    baseline_result, baseline_error = _query_rows(
        access_token=access_token,
        metric_list=distribution_metrics,
        dimension_list=distribution_dimensions,
        filter_payload=baseline_filter,
        endpoint=endpoint,
    )

    if current_error or baseline_error:
        log_stage_event(
            "capital",
            "阶段失败",
            slice_key=slice_key,
            errors=[item for item in [current_error, baseline_error] if item],
        )
        trace = {
            "context": context,
            "slice_key": slice_key,
            "slice_display": slice_display,
            "capital_distribution_stats": [],
            "capital_total_judgement": capital_total_judgement,
            "distribution_judgement": build_distribution_judgement(
                evaluated=False,
                skipped_reason="capital_distribution_query_error",
            ),
            "analysis_steps": [
                stage_analysis_step(
                    step="准入资方总量判断",
                    analysis="先看这组订单的准入资方总量有没有明显下降。",
                    evidence=[
                        f"当前准入资方总量：{capital_total_judgement['current']}。",
                        f"对比期准入资方总量：{capital_total_judgement['baseline']}。",
                        f"减少量：{capital_total_judgement['drop']}，下降比例：{capital_total_judgement['drop_ratio_text']}。",
                        f"判断阈值：以上期准入资方个数为基准，下降超过 {capital_total_judgement['threshold_ratio_text']}。",
                    ],
                    conclusion=f"总量下降比例未超过 {capital_total_judgement['threshold_ratio_text']} 阈值，因此继续看资方桶分布。",
                ),
                stage_analysis_step(
                    step="资方桶分布取数",
                    analysis="总量分支未命中后，再取当前期和对比期的资方桶分布数据。",
                    evidence=[item for item in [current_error, baseline_error] if item],
                    conclusion="分布查询失败，当前无法继续判断。",
                ),
            ],
            "terminal_reason": "R8",
            "terminal_reason_text": build_reason("R8"),
            "next_action": "stop",
            "business_view": business_view(
                headline="总量分支没命中，但桶分布没取到",
                summary="准入资方总量下降比例未超过阈值，本来应该继续看资方桶分布，但当前桶分布查询失败了。",
                evidence=[item for item in [current_error, baseline_error] if item],
            ),
            "root_cause": build_root_cause(
                "query_error",
                "资方桶分布查询失败。",
                slice_key=slice_key,
                slice_display=slice_display,
                capital_total_judgement=capital_total_judgement,
                current_error=current_error,
                baseline_error=baseline_error,
            ),
            "errors": [item for item in [current_error, baseline_error] if item],
            "debug_query": build_period_debug_snapshot(
                current_result=current_result,
                baseline_result=baseline_result,
                current_filter=current_filter,
                baseline_filter=baseline_filter,
            ),
        }
        return trace

    current_records = _normalized_metric_rows(current_result.get("rows", []), ["week", "if_qd", "irr24_new", "alllow_ly_cnt"])
    baseline_records = _normalized_metric_rows(baseline_result.get("rows", []), ["week", "if_qd", "irr24_new", "alllow_ly_cnt"])
    if not current_records or not baseline_records:
        errors: list[str] = []
        if not current_records:
            errors.append("当前周期没有拿到这组订单的资方桶分布数据。")
        if not baseline_records:
            errors.append("对比周期没有拿到这组订单的资方桶分布数据。")
        trace = {
            "context": context,
            "slice_key": slice_key,
            "slice_display": slice_display,
            "capital_distribution_stats": [],
            "capital_total_judgement": capital_total_judgement,
            "distribution_judgement": build_distribution_judgement(
                evaluated=False,
                skipped_reason="capital_distribution_data_missing",
            ),
            "analysis_steps": [
                stage_analysis_step(
                    step="准入资方总量判断",
                    analysis="先看这组订单的准入资方总量有没有明显下降。",
                    evidence=[
                        f"当前准入资方总量：{capital_total_judgement['current']}。",
                        f"对比期准入资方总量：{capital_total_judgement['baseline']}。",
                        f"减少量：{capital_total_judgement['drop']}，下降比例：{capital_total_judgement['drop_ratio_text']}。",
                        f"判断阈值：以上期准入资方个数为基准，下降超过 {capital_total_judgement['threshold_ratio_text']}。",
                    ],
                    conclusion=f"总量下降比例未超过 {capital_total_judgement['threshold_ratio_text']} 阈值，因此继续看资方桶分布。",
                ),
                stage_analysis_step(
                    step="资方桶分布取数",
                    analysis="总量分支未命中后，再取当前期和对比期的资方桶分布数据。",
                    evidence=errors,
                    conclusion="当前期或对比期缺少可比桶分布数据，当前无法继续判断。",
                )
            ],
            "terminal_reason": "R8",
            "terminal_reason_text": build_reason("R8"),
            "next_action": "stop",
            "business_view": business_view(
                headline="总量分支没命中，但桶分布数据不完整",
                summary="准入资方总量下降比例未超过阈值，本来应该继续看资方桶分布，但当前期或对比期缺少可比桶分布数据。",
                evidence=errors,
            ),
            "root_cause": build_root_cause(
                "missing_slice_data",
                "资方分布阶段缺少当前期或对比期切片数据。",
                slice_key=slice_key,
                slice_display=slice_display,
                current_row_count=len(current_records),
                baseline_row_count=len(baseline_records),
                current_period=current_period,
                baseline_period=baseline_period,
                capital_total_judgement=capital_total_judgement,
            ),
            "errors": errors,
            "debug_query": build_period_debug_snapshot(
                current_result=current_result,
                baseline_result=baseline_result,
                current_filter=current_filter,
                baseline_filter=baseline_filter,
            ),
        }
        log_stage_event("capital", "阶段失败", slice_key=slice_key, trace=trace)
        return trace

    current_buckets = _aggregate_records(current_records, ["alllow_ly_cnt"])
    baseline_buckets = _aggregate_records(baseline_records, ["alllow_ly_cnt"])
    current_bucket_map = {normalize_text(item["alllow_ly_cnt"]): item for item in current_buckets}
    baseline_bucket_map = {normalize_text(item["alllow_ly_cnt"]): item for item in baseline_buckets}

    current_total_route = sum(to_float(item["route_amount"]) for item in current_buckets)
    baseline_total_route = sum(to_float(item["route_amount"]) for item in baseline_buckets)
    weighted_mean_current = safe_div(
        sum((parse_allow_bucket(item["alllow_ly_cnt"]) or 0.0) * to_float(item["route_amount"]) for item in current_buckets),
        current_total_route,
    )
    weighted_mean_baseline = safe_div(
        sum((parse_allow_bucket(item["alllow_ly_cnt"]) or 0.0) * to_float(item["route_amount"]) for item in baseline_buckets),
        baseline_total_route,
    )
    weighted_median_current = weighted_median(
        [
            (parse_allow_bucket(item["alllow_ly_cnt"]) or 0.0, to_float(item["route_amount"]))
            for item in current_buckets
        ]
    )
    weighted_median_baseline = weighted_median(
        [
            (parse_allow_bucket(item["alllow_ly_cnt"]) or 0.0, to_float(item["route_amount"]))
            for item in baseline_buckets
        ]
    )

    low_bucket_share_current = {
        "<=2": round_float(
            bucket_route_share(
                current_buckets,
                current_total_route,
                lambda bucket_value: bucket_value is not None and bucket_value <= 2,
            ),
            6,
        ),
        "<=3": round_float(
            bucket_route_share(
                current_buckets,
                current_total_route,
                lambda bucket_value: bucket_value is not None and bucket_value <= 3,
            ),
            6,
        ),
    }
    low_bucket_share_baseline = {
        "<=2": round_float(
            bucket_route_share(
                baseline_buckets,
                baseline_total_route,
                lambda bucket_value: bucket_value is not None and bucket_value <= 2,
            ),
            6,
        ),
        "<=3": round_float(
            bucket_route_share(
                baseline_buckets,
                baseline_total_route,
                lambda bucket_value: bucket_value is not None and bucket_value <= 3,
            ),
            6,
        ),
    }
    low_bucket_share_delta = {
        "<=2": round_float(to_float(low_bucket_share_current["<=2"]) - to_float(low_bucket_share_baseline["<=2"]), 6),
        "<=3": round_float(to_float(low_bucket_share_current["<=3"]) - to_float(low_bucket_share_baseline["<=3"]), 6),
    }
    high_bucket_share_current = {
        ">=4": round_float(
            bucket_route_share(
                current_buckets,
                current_total_route,
                lambda bucket_value: bucket_value is not None and bucket_value >= 4,
            ),
            6,
        ),
        ">=5": round_float(
            bucket_route_share(
                current_buckets,
                current_total_route,
                lambda bucket_value: bucket_value is not None and bucket_value >= 5,
            ),
            6,
        ),
    }
    high_bucket_share_baseline = {
        ">=4": round_float(
            bucket_route_share(
                baseline_buckets,
                baseline_total_route,
                lambda bucket_value: bucket_value is not None and bucket_value >= 4,
            ),
            6,
        ),
        ">=5": round_float(
            bucket_route_share(
                baseline_buckets,
                baseline_total_route,
                lambda bucket_value: bucket_value is not None and bucket_value >= 5,
            ),
            6,
        ),
    }
    high_bucket_share_delta = {
        ">=4": round_float(to_float(high_bucket_share_current[">=4"]) - to_float(high_bucket_share_baseline[">=4"]), 6),
        ">=5": round_float(to_float(high_bucket_share_current[">=5"]) - to_float(high_bucket_share_baseline[">=5"]), 6),
    }

    bucket_stats: list[dict[str, Any]] = []
    for bucket_key in sorted(set(current_bucket_map) | set(baseline_bucket_map), key=lambda item: parse_allow_bucket(item) or 9999):
        current_item = current_bucket_map.get(bucket_key, {})
        baseline_item = baseline_bucket_map.get(bucket_key, {})
        bucket_stats.append(
            {
                "alllow_ly_cnt": bucket_key,
                "current_route_amount": round_float(to_float(current_item.get("route_amount")), 2),
                "baseline_route_amount": round_float(to_float(baseline_item.get("route_amount")), 2),
                "current_acceptance_rate": round_float(current_item.get("acceptance_rate"), 6) if current_item else None,
                "baseline_acceptance_rate": round_float(baseline_item.get("acceptance_rate"), 6) if baseline_item else None,
                "current_route_share": round_float(safe_div(to_float(current_item.get("route_amount")), current_total_route), 6),
                "baseline_route_share": round_float(safe_div(to_float(baseline_item.get("route_amount")), baseline_total_route), 6),
                "route_share_delta": round_float(
                    safe_div(to_float(current_item.get("route_amount")), current_total_route)
                    - safe_div(to_float(baseline_item.get("route_amount")), baseline_total_route),
                    6,
                ),
            }
        )

    weighted_mean_delta = weighted_mean_current - weighted_mean_baseline
    weighted_median_delta = None
    if weighted_median_current is not None and weighted_median_baseline is not None:
        weighted_median_delta = weighted_median_current - weighted_median_baseline

    low_bucket_share_up = (
        to_float(low_bucket_share_delta["<=2"]) >= 0.05
        or to_float(low_bucket_share_delta["<=3"]) >= 0.08
    )
    high_bucket_share_down = (
        to_float(high_bucket_share_delta[">=4"]) <= -0.05
        or to_float(high_bucket_share_delta[">=5"]) <= -0.03
    )
    central_tendency_down = (
        weighted_mean_delta <= -0.3
        or (weighted_median_delta is not None and weighted_median_delta <= -1)
    )
    structural_shift_strength = round_float(
        max(to_float(low_bucket_share_delta["<=2"]), 0.0)
        + max(to_float(low_bucket_share_delta["<=3"]), 0.0)
        + max(-to_float(high_bucket_share_delta[">=4"]), 0.0)
        + max(-to_float(high_bucket_share_delta[">=5"]), 0.0),
        6,
    )
    is_left_shift = low_bucket_share_up and high_bucket_share_down and (
        central_tendency_down or to_float(structural_shift_strength) >= 0.15
    )
    distribution_judgement = build_distribution_judgement(
        evaluated=True,
        weighted_mean_current=weighted_mean_current,
        weighted_mean_baseline=weighted_mean_baseline,
        weighted_mean_delta=weighted_mean_delta,
        weighted_median_current=weighted_median_current,
        weighted_median_baseline=weighted_median_baseline,
        weighted_median_delta=weighted_median_delta,
        low_bucket_share_current=low_bucket_share_current,
        low_bucket_share_baseline=low_bucket_share_baseline,
        low_bucket_share_delta=low_bucket_share_delta,
        high_bucket_share_current=high_bucket_share_current,
        high_bucket_share_baseline=high_bucket_share_baseline,
        high_bucket_share_delta=high_bucket_share_delta,
        low_bucket_share_up=low_bucket_share_up,
        high_bucket_share_down=high_bucket_share_down,
        central_tendency_down=central_tendency_down,
        structural_shift_strength=structural_shift_strength,
        is_left_shift=is_left_shift,
    )

    terminal_reason: str | None = None
    next_action = "run_asset"
    if not is_left_shift:
        terminal_reason = "R4"
        next_action = "stop"

    analysis_steps: list[dict[str, Any]] = [
        stage_analysis_step(
            step="准入资方总量判断",
            analysis="先看这组订单的准入资方总量有没有明显下降。",
            evidence=[
                f"当前准入资方总量：{capital_total_judgement['current']}。",
                f"对比期准入资方总量：{capital_total_judgement['baseline']}。",
                f"减少量：{capital_total_judgement['drop']}，下降比例：{capital_total_judgement['drop_ratio_text']}。",
                f"判断阈值：以上期准入资方个数为基准，下降超过 {capital_total_judgement['threshold_ratio_text']}。",
            ],
                    conclusion=f"准入资方总量下降比例未超过 {capital_total_judgement['threshold_ratio_text']} 阈值，因此继续看资方桶分布。",
        )
    ]

    if is_left_shift:
        analysis_steps.append(
            stage_analysis_step(
                step="资方桶分布偏移判断",
                analysis="总量分支未命中后，再看订单是否更多落到了少资方桶，同时高资方桶占比是否回落。",
                evidence=[
                    f"<=2 桶路由占比变化：{low_bucket_share_delta['<=2']}。",
                    f"<=3 桶路由占比变化：{low_bucket_share_delta['<=3']}。",
                    f">=4 桶路由占比变化：{high_bucket_share_delta['>=4']}。",
                    f">=5 桶路由占比变化：{high_bucket_share_delta['>=5']}。",
                    f"加权均值变化：{round_float(weighted_mean_delta, 6)}。",
                    f"加权中位数变化：{round_float(weighted_median_delta, 6)}。",
                ],
                conclusion="低资方桶占比抬升且高资方桶占比回落，资方分布出现左移，更像资产维度变化导致单笔可匹配资方减少，继续进入资产维度阶段。",
            )
        )
        analysis_steps.append(
            stage_analysis_step(
                step="授用信通过率兜底",
                analysis="已经识别到资方分布左移，本步不再走通过率兜底。",
                evidence=[],
                conclusion="本步跳过，进入下一阶段。",
                status="skipped",
            )
        )
        business = business_view(
            headline="总量分支没命中，但资方桶分布明显左移",
                summary=(
                    "第二阶段先看总量下降比例没有超过上期的 "
                    f"{capital_total_judgement['threshold_ratio_text']} 阈值，因此继续看资方桶分布；"
                    "结果显示订单明显向少资方桶偏移，更像资产维度变化导致单笔可匹配资方减少。"
                ),
            evidence=[
                f"总量下降比例 {capital_total_judgement['drop_ratio_text']}，阈值 {capital_total_judgement['threshold_ratio_text']}。",
                f"<=2 桶占比变化 {low_bucket_share_delta['<=2']}，<=3 桶占比变化 {low_bucket_share_delta['<=3']}。",
                f">=4 桶占比变化 {high_bucket_share_delta['>=4']}，>=5 桶占比变化 {high_bucket_share_delta['>=5']}。",
                f"加权均值变化 {round_float(weighted_mean_delta, 6)}，加权中位数变化 {round_float(weighted_median_delta, 6)}。",
            ],
        )
        root_cause = build_root_cause(
            "allow_count_distribution_left_shift",
            "资方总量未明显收缩，但可匹配资方桶分布向低桶偏移，需要继续看资产维度阶段。",
            slice_key=slice_key,
            slice_display=slice_display,
            capital_total_judgement=capital_total_judgement,
            distribution_judgement=distribution_judgement,
        )
    else:
        analysis_steps.append(
            stage_analysis_step(
                step="资方桶分布偏移判断",
                analysis="总量分支未命中后，再看低资方桶和高资方桶的占比是否发生了结构性偏移。",
                evidence=[
                    f"<=2 桶路由占比变化：{low_bucket_share_delta['<=2']}。",
                    f"<=3 桶路由占比变化：{low_bucket_share_delta['<=3']}。",
                    f">=4 桶路由占比变化：{high_bucket_share_delta['>=4']}。",
                    f">=5 桶路由占比变化：{high_bucket_share_delta['>=5']}。",
                    f"加权均值变化：{round_float(weighted_mean_delta, 6)}。",
                    f"加权中位数变化：{round_float(weighted_median_delta, 6)}。",
                ],
                conclusion="没有看到明确的低桶抬升加高桶回落，当前不认为资方分布发生了明显左移。",
            )
        )
        analysis_steps.append(
            stage_analysis_step(
                step="授用信通过率兜底",
                analysis="既然总量没明显收缩、分布也没明显左移，理论上下一步该检查授用信通过率或规则变化。",
                evidence=[
                    "当前脚本还没有接入授用信通过率指标。",
                    "因此只能先把结论停在“更像规则或通过率变化”，不能继续自动下钻。",
                ],
                conclusion="本切片先停在第二阶段，归因为更像规则或授用信通过率变化。",
            )
        )
        business = business_view(
            headline="总量分支和分布分支都没命中，当前更像规则或通过率变化",
                summary=(
                    "第二阶段先看总量下降比例没有超过上期的 "
                    f"{capital_total_judgement['threshold_ratio_text']} 阈值，因此继续看资方桶分布；"
                    "但分布也没有出现明显左移，所以当前更像规则或授用信通过率变化。"
                ),
            evidence=[
                f"准入资方总量减少 {capital_total_judgement['drop']}，下降比例 {capital_total_judgement['drop_ratio_text']}，未达到 {capital_total_judgement['threshold_ratio_text']}。",
                f"<=2 桶占比变化 {low_bucket_share_delta['<=2']}，>=4 桶占比变化 {high_bucket_share_delta['>=4']}。",
                "授用信通过率指标暂未接入。",
            ],
        )
        root_cause = build_root_cause(
            "credit_pass_rate_metric_unavailable",
            "总量和分布都未见明显异常，理论上应继续检查授用信通过率，但当前脚本尚未接入该指标。",
            slice_key=slice_key,
            slice_display=slice_display,
            capital_total_judgement=capital_total_judgement,
            distribution_judgement=distribution_judgement,
        )

    trace = {
        "context": context,
        "slice_key": slice_key,
        "slice_display": slice_display,
        "capital_distribution_stats": bucket_stats,
        "capital_total_judgement": capital_total_judgement,
        "distribution_judgement": distribution_judgement,
        "analysis_steps": analysis_steps,
        "terminal_reason": terminal_reason,
        "terminal_reason_text": build_reason(terminal_reason),
        "next_action": next_action,
        "business_view": business,
        "root_cause": root_cause,
        "errors": [],
    }
    log_stage_event(
        "capital",
        "阶段完成",
        slice_key=slice_key,
        trace=trace,
    )
    return trace




def _current_slice_from_primary(primary_trace: dict[str, Any], slice_key: str) -> dict[str, Any]:
    for item in primary_trace.get("analysis_sequence", []):
        if slice_key_matches(item.get("slice_key", ""), slice_key):
            return {
                "slice_key": item.get("slice_key"),
                "slice_display": item.get("slice_display"),
                "if_qd": item.get("if_qd"),
                "irr24_new": item.get("irr24_new"),
                "current_rate": item.get("current_acceptance_rate"),
                "baseline_rate": item.get("baseline_acceptance_rate"),
                "current_route_amount": item.get("current_route_amount"),
                "baseline_route_amount": item.get("baseline_route_amount"),
                "current_route_share": item.get("current_route_share"),
                "baseline_route_share": item.get("baseline_route_share"),
                "route_share_delta": item.get("route_share_delta"),
                "drag_amount": item.get("drag_amount"),
            }
    for item in primary_trace.get("slice_comparison", []):
        if slice_key_matches(item.get("slice_key", ""), slice_key):
            return item
    return {}


def build_empty_asset_display() -> dict[str, str]:
    return {
        "summary_markdown": "",
        "factor_detail_markdown": "",
        "combo_detail_markdown": "",
    }


def _build_asset_thresholds(*, current_slice_drag_amount: float) -> dict[str, dict[str, float]]:
    bucket_effective = max(
        ASSET_BUCKET_DRAG_ABSOLUTE_THRESHOLD,
        current_slice_drag_amount * ASSET_BUCKET_DRAG_RELATIVE_THRESHOLD,
    )
    combo_effective = max(
        ASSET_COMBO_DRAG_ABSOLUTE_THRESHOLD,
        current_slice_drag_amount * ASSET_COMBO_DRAG_RELATIVE_THRESHOLD,
    )
    return {
        "bucket": {
            "absolute": round_float(ASSET_BUCKET_DRAG_ABSOLUTE_THRESHOLD, 2),
            "relative": round_float(ASSET_BUCKET_DRAG_RELATIVE_THRESHOLD, 6),
            "effective": round_float(bucket_effective, 2),
        },
        "combo": {
            "absolute": round_float(ASSET_COMBO_DRAG_ABSOLUTE_THRESHOLD, 2),
            "relative": round_float(ASSET_COMBO_DRAG_RELATIVE_THRESHOLD, 6),
            "effective": round_float(combo_effective, 2),
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


def _asset_bucket_decision_reason(
    *,
    share_delta: float,
    current_bucket_rate: float | None,
    current_slice_rate: float,
    impact_route_amount: float,
    impact_threshold: float,
) -> str:
    if share_delta <= 0:
        return "当前占比没有高于对比期，未命中异常桶。"
    if current_bucket_rate is None:
        return "当前桶缺少承接率，未命中异常桶。"
    if current_bucket_rate >= current_slice_rate:
        return "当前桶承接率未低于切片整体承接率，未命中异常桶。"
    if impact_route_amount < impact_threshold:
        return f"影响路由金额 {format_wan(impact_route_amount)} 未达到门槛 {format_wan(impact_threshold)}。"
    return f"占比上升且承接更差，影响路由金额 {format_wan(impact_route_amount)} 达到门槛 {format_wan(impact_threshold)}。"


def _asset_factor_decision_reason(factor_result: dict[str, Any], bucket_threshold: float) -> str:
    if factor_result["final_decision"] == "hit":
        top_bucket = factor_result["top_bucket"]
        return (
            f"命中 {factor_result['hit_bucket_count']} 个异常桶，最强桶 {normalize_text(top_bucket.get('bucket_label'))} "
            f"影响路由金额 {format_wan(to_float(top_bucket.get('impact_route_amount')))}，已超过门槛 {format_wan(bucket_threshold)}。"
        )
    near_miss_buckets = factor_result.get("near_miss_buckets", [])
    if near_miss_buckets:
        top_bucket = near_miss_buckets[0]
        return (
            f"发现 {factor_result['near_miss_bucket_count']} 个疑似异常桶，但影响路由金额均未达到门槛；"
            f"最接近门槛的是 {normalize_text(top_bucket.get('bucket_label'))}，"
            f"影响路由金额 {format_wan(to_float(top_bucket.get('impact_route_amount')))}，"
            f"仍低于门槛 {format_wan(bucket_threshold)}。"
        )
    return "所有桶均未同时满足“占比上升、承接更差、影响路由金额达到门槛”三项条件。"


def _asset_combo_decision_reason(
    *,
    current_route: float,
    current_share: float,
    baseline_share: float,
    impact_route_amount: float,
    impact_threshold: float,
    enter_next_stage: bool,
) -> str:
    if current_route <= 0:
        return "当前期没有形成该组合的路由量，不进入下一阶段。"
    if current_share <= baseline_share:
        return (
            f"当前占比 {format_percent(current_share)} 未高于对比期 {format_percent(baseline_share)}，"
            "不进入下一阶段。"
        )
    if not enter_next_stage:
        return (
            f"影响路由金额 {format_wan(impact_route_amount)} 未达到门槛 {format_wan(impact_threshold)}，"
            "不进入下一阶段。"
        )
    return (
        f"当前占比上升且影响路由金额 {format_wan(impact_route_amount)} 达到门槛 {format_wan(impact_threshold)}，"
        "进入下一阶段。"
    )


def _build_factor_results(
    *,
    current_records: list[dict[str, Any]],
    baseline_records: list[dict[str, Any]],
    current_slice_rate: float,
    baseline_slice_rate: float,
    current_slice_route_amount: float,
    asset_thresholds: dict[str, dict[str, float]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    bucket_threshold = to_float(asset_thresholds["bucket"]["effective"])
    factor_results: list[dict[str, Any]] = []
    hit_buckets: list[dict[str, Any]] = []

    for factor_key in FACTOR_LABELS:
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
            current_share = safe_div(to_float(current_item.get("route_amount")), current_total_route)
            baseline_share = safe_div(to_float(baseline_item.get("route_amount")), baseline_total_route)
            current_bucket_rate = round_float(to_float(current_item.get("acceptance_rate")), 6) if current_item else None
            baseline_bucket_rate = round_float(to_float(baseline_item.get("acceptance_rate")), 6) if baseline_item else None
            share_delta = current_share - baseline_share
            impact_route_amount = max(share_delta, 0.0) * current_slice_route_amount * max(
                baseline_slice_rate - to_float(current_bucket_rate),
                0.0,
            )
            is_soft_signal = (
                share_delta > 0
                and current_bucket_rate is not None
                and current_bucket_rate < current_slice_rate
            )
            is_hit = (
                is_soft_signal
                and impact_route_amount >= bucket_threshold
            )
            bucket_result = {
                "factor_key": factor_key,
                "factor_label": factor_label,
                "bucket": bucket,
                "bucket_label": bucket_label_for_value(bucket),
                "current_route_amount": round_float(to_float(current_item.get("route_amount")), 2),
                "baseline_route_amount": round_float(to_float(baseline_item.get("route_amount")), 2),
                "current_acceptance_rate": current_bucket_rate,
                "baseline_acceptance_rate": baseline_bucket_rate,
                "current_route_share": round_float(current_share, 6),
                "baseline_route_share": round_float(baseline_share, 6),
                "share_delta": round_float(share_delta, 6),
                "impact_route_amount": round_float(impact_route_amount, 2),
                "impact_threshold": round_float(bucket_threshold, 2),
                "is_soft_signal": is_soft_signal,
                "is_near_miss": is_soft_signal and impact_route_amount < bucket_threshold,
                "is_hit": is_hit,
            }
            bucket_result["decision_reason"] = _asset_bucket_decision_reason(
                share_delta=share_delta,
                current_bucket_rate=current_bucket_rate,
                current_slice_rate=current_slice_rate,
                impact_route_amount=to_float(bucket_result["impact_route_amount"]),
                impact_threshold=to_float(bucket_result["impact_threshold"]),
            )
            bucket_results.append(bucket_result)
            if is_hit:
                hit_buckets.append(
                    {
                        "factor_key": factor_key,
                        "factor_label": factor_label,
                        "bucket": bucket,
                        "bucket_label": bucket_label_for_value(bucket),
                    }
                )

        bucket_results.sort(
            key=lambda item: (
                not bool(item["is_hit"]),
                -to_float(item["impact_route_amount"]),
                normalize_text(item["bucket_label"]),
            )
        )
        hit_bucket_results = [item for item in bucket_results if item["is_hit"]]
        near_miss_bucket_results = [item for item in bucket_results if item["is_near_miss"]]
        top_bucket = dict(hit_bucket_results[0]) if hit_bucket_results else None
        factor_result = {
            "factor_key": factor_key,
            "factor_label": factor_label,
            "final_decision": "hit" if hit_bucket_results else "not_hit",
            "decision_reason": "",
            "hit_bucket_count": len(hit_bucket_results),
            "near_miss_bucket_count": len(near_miss_bucket_results),
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
            "if_qd",
            "irr24_new",
            "age_rand",
            "identity_effective_date",
            "identity_province_name",
            "edu_rand",
            "grade_level_round",
        ],
    )
    for record in base_records:
        record["identity_bucket"] = factor_bucket_value("identity_effective_date", record.get("identity_effective_date"))
        record["age_bucket"] = factor_bucket_value("age_rand", record.get("age_rand"))
        record["province_bucket"] = factor_bucket_value("identity_province_name", record.get("identity_province_name"))
        record["amount_bucket"] = factor_bucket_value("edu_rand", record.get("edu_rand"))
        record["risk_bucket"] = factor_bucket_value("grade_level_round", record.get("grade_level_round"))
    return base_records


def _records_for_factor(records: list[dict[str, Any]], factor_key: str) -> list[dict[str, Any]]:
    bucket_field = {
        "identity_effective_date": "identity_bucket",
        "age_rand": "age_bucket",
        "identity_province_name": "province_bucket",
        "edu_rand": "amount_bucket",
        "grade_level_round": "risk_bucket",
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
        "grade_level_round": "risk_bucket",
    }[factor_key]
    return normalize_text(record.get(bucket_field)) == normalize_text(bucket)


def _build_combo_results(
    *,
    hits: list[dict[str, Any]],
    current_records: list[dict[str, Any]],
    baseline_records: list[dict[str, Any]],
    prev_slice_rate: float,
    current_slice_route_amount: float,
    asset_thresholds: dict[str, dict[str, float]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    combo_results: list[dict[str, Any]] = []
    combo_threshold = to_float(asset_thresholds["combo"]["effective"])
    unique_hits = {}
    for hit in hits:
        unique_hits[(hit["factor_key"], hit["bucket"])] = hit
    candidate_hits = list(unique_hits.values())
    baseline_total_route = sum(to_float(item["route_amount"]) for item in baseline_records)

    for combo_size in (2, 3):
        for combo_hits in combinations(candidate_hits, combo_size):
            factor_keys = [item["factor_key"] for item in combo_hits]
            if len(set(factor_keys)) != combo_size:
                continue
            current_subset = [
                record
                for record in current_records
                if all(_bucket_match(record, item["factor_key"], item["bucket"]) for item in combo_hits)
            ]
            baseline_subset = [
                record
                for record in baseline_records
                if all(_bucket_match(record, item["factor_key"], item["bucket"]) for item in combo_hits)
            ]
            current_route = sum(to_float(item["route_amount"]) for item in current_subset)
            baseline_route = sum(to_float(item["route_amount"]) for item in baseline_subset)
            current_share = safe_div(current_route, current_slice_route_amount)
            baseline_share = safe_div(baseline_route, baseline_total_route)
            combo_current_rate = (
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
            combo_baseline_rate = (
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
            impact_route_amount = current_route * max(prev_slice_rate - to_float(combo_current_rate), 0.0)
            factor_items = normalize_combo_factor_items(
                [
                    {
                        "factor_key": item["factor_key"],
                        "factor_label": item["factor_label"],
                        "bucket": item["bucket"],
                    }
                    for item in combo_hits
                ]
            )
            enter_next_stage = (
                current_route > 0
                and current_share > baseline_share
                and impact_route_amount >= combo_threshold
            )
            combo_result = {
                "combo_id": "",
                "combo_key": build_combo_key(factor_items),
                "combo_display": build_combo_display(factor_items),
                "factor_items": factor_items,
                "current_share": round_float(current_share, 6),
                "baseline_share": round_float(baseline_share, 6),
                "share_delta": round_float(current_share - baseline_share, 6),
                "current_acceptance_rate": combo_current_rate,
                "baseline_acceptance_rate": combo_baseline_rate,
                "impact_route_amount": round_float(impact_route_amount, 2),
                "impact_threshold": round_float(combo_threshold, 2),
                "enter_next_stage": enter_next_stage,
                "supported_for_funding": all(
                    item["factor_key"] in FUNDING_SUPPORTED_FACTORS
                    for item in combo_hits
                ),
            }
            combo_result["decision_reason"] = _asset_combo_decision_reason(
                current_route=current_route,
                current_share=current_share,
                baseline_share=baseline_share,
                impact_route_amount=to_float(combo_result["impact_route_amount"]),
                impact_threshold=to_float(combo_result["impact_threshold"]),
                enter_next_stage=enter_next_stage,
            )
            combo_results.append(combo_result)

    combo_results.sort(
        key=lambda item: (
            not bool(item["enter_next_stage"]),
            -to_float(item["impact_route_amount"]),
            normalize_text(item["combo_key"]),
        )
    )
    for combo_index, item in enumerate(combo_results, start=1):
        item["combo_id"] = f"combo_{combo_index}"
    qualified_combos = [{key: value for key, value in item.items()} for item in combo_results if item["enter_next_stage"]]
    return combo_results, qualified_combos


def _build_asset_display(
    *,
    slice_display: str,
    slice_context: dict[str, float],
    asset_thresholds: dict[str, dict[str, float]],
    factor_results: list[dict[str, Any]],
    combo_results: list[dict[str, Any]],
    qualified_combos: list[dict[str, Any]],
    soft_signal_buckets: list[dict[str, Any]],
    terminal_reason: str | None,
) -> dict[str, str]:
    hit_factor_count = sum(1 for item in factor_results if item["final_decision"] == "hit")
    hit_bucket_count = sum(int(item["hit_bucket_count"]) for item in factor_results)
    soft_signal_factor_count = sum(1 for item in factor_results if int(item.get("near_miss_bucket_count", 0)) > 0)
    entered_combo_displays = [normalize_text(item.get("combo_display")) for item in qualified_combos]
    not_entered_combo_results = [item for item in combo_results if not item["enter_next_stage"]]
    typical_reasons: list[str] = []
    for item in not_entered_combo_results:
        reason = normalize_text(item.get("decision_reason"))
        if reason and reason not in typical_reasons:
            typical_reasons.append(reason)
        if len(typical_reasons) >= 2:
            break

    summary_lines = [
        "### 第三阶段结论",
        f"- 当前切片：{slice_display}",
        f"- 当前承接率：{format_percent(to_float(slice_context['current_acceptance_rate']))}；对比期承接率：{format_percent(to_float(slice_context['baseline_acceptance_rate']))}。",
        f"- 当前路由金额：{format_wan(to_float(slice_context['current_route_amount']))}；当前切片少承接金额估算：{format_wan(to_float(slice_context['slice_drag_amount']))}。",
        (
            f"- 单桶识别门槛：max({format_wan(to_float(asset_thresholds['bucket']['absolute']))}, "
            f"切片少承接金额估算的 {format_percent(to_float(asset_thresholds['bucket']['relative']))}) = "
            f"{format_wan(to_float(asset_thresholds['bucket']['effective']))}。"
        ),
        (
            f"- 组合进入下一阶段门槛：max({format_wan(to_float(asset_thresholds['combo']['absolute']))}, "
            f"切片少承接金额估算的 {format_percent(to_float(asset_thresholds['combo']['relative']))}) = "
            f"{format_wan(to_float(asset_thresholds['combo']['effective']))}。"
        ),
    ]
    if terminal_reason == "R4":
        if soft_signal_buckets:
            top_soft_signal_amounts = [
                format_wan(to_float(item.get("impact_route_amount")))
                for item in soft_signal_buckets[:3]
            ]
            top_soft_signal_bucket_names = [
                f"{normalize_text(item.get('factor_label'))}（{normalize_text(item.get('bucket_label'))}）"
                for item in soft_signal_buckets[:3]
            ]
            summary_lines.append(
                f"- 结论：发现 {len(soft_signal_buckets)} 个疑似异常桶，涉及 {soft_signal_factor_count} 个资产维度；"
                f"影响路由金额分别为 {'、'.join(top_soft_signal_amounts)}，"
                f"均未达到门槛 {format_wan(to_float(asset_thresholds['bucket']['effective']))}，因此当前停在资产维度诊断。"
            )
            if top_soft_signal_bucket_names:
                summary_lines.append(f"- 疑似异常桶：{'；'.join(top_soft_signal_bucket_names)}。")
        else:
            summary_lines.append("- 结论：所有资产维度都没有命中单桶识别门槛，当前归因先停在资产维度诊断。")
        summary_lines.append("- 进入下一阶段的组合：无。")
    elif terminal_reason == "R5":
        summary_lines.append(
            f"- 结论：已识别 {hit_factor_count} 个资产维度、{hit_bucket_count} 个异常桶，但没有组合达到第四阶段门槛，当前归因先停在资产维度诊断。"
        )
        summary_lines.append("- 进入下一阶段的组合：无。")
        if typical_reasons:
            summary_lines.append(f"- 未进入下一阶段的典型原因：{'；'.join(typical_reasons)}")
    else:
        summary_lines.append(
            f"- 结论：已识别 {len(qualified_combos)} 个组合达到第四阶段门槛，继续看敏感资方侧收缩。"
        )
        summary_lines.append(
            f"- 进入下一阶段的组合：{'；'.join(item for item in entered_combo_displays if item) if entered_combo_displays else '无'}"
        )
        if typical_reasons:
            summary_lines.append(f"- 未进入下一阶段的典型原因：{'；'.join(typical_reasons)}")

    factor_lines = [
        "### 每个因子明细",
        (
            f"单桶识别门槛：max({format_wan(to_float(asset_thresholds['bucket']['absolute']))}, "
            f"切片少承接金额估算的 {format_percent(to_float(asset_thresholds['bucket']['relative']))}) = "
            f"{format_wan(to_float(asset_thresholds['bucket']['effective']))}。"
        ),
    ]
    for factor_result in factor_results:
        factor_lines.append("")
        factor_lines.append(f"#### {normalize_text(factor_result['factor_label'])}")
        factor_lines.append(f"结论：{normalize_text(factor_result['decision_reason'])}")
        factor_lines.append(
            build_markdown_table(
                ASSET_FACTOR_TABLE_COLUMNS,
                [
                    {
                        "factor_label": normalize_text(bucket["factor_label"]),
                        "bucket_label": normalize_text(bucket["bucket_label"]),
                        "current_route_amount_text": format_wan_or_dash(bucket["current_route_amount"]),
                        "baseline_route_amount_text": format_wan_or_dash(bucket["baseline_route_amount"]),
                        "current_acceptance_rate_text": format_percent_or_dash(bucket["current_acceptance_rate"]),
                        "baseline_acceptance_rate_text": format_percent_or_dash(bucket["baseline_acceptance_rate"]),
                        "current_route_share_text": format_percent_or_dash(bucket["current_route_share"]),
                        "baseline_route_share_text": format_percent_or_dash(bucket["baseline_route_share"]),
                        "share_delta_text": format_percent_or_dash(bucket["share_delta"]),
                        "impact_route_amount_text": format_wan_or_dash(bucket["impact_route_amount"]),
                        "impact_threshold_text": format_wan_or_dash(bucket["impact_threshold"]),
                        "is_hit_text": format_yes_no(bool(bucket["is_hit"])),
                        "decision_reason": normalize_text(bucket["decision_reason"]),
                    }
                    for bucket in factor_result["buckets"]
                ],
            )
        )

    combo_lines = [
        "### 每种组合明细",
        (
            f"组合进入下一阶段门槛：max({format_wan(to_float(asset_thresholds['combo']['absolute']))}, "
            f"切片少承接金额估算的 {format_percent(to_float(asset_thresholds['combo']['relative']))}) = "
            f"{format_wan(to_float(asset_thresholds['combo']['effective']))}。"
        ),
    ]
    combo_table_rows = [
        {
            "combo_id": normalize_text(item["combo_id"]),
            "combo_display": normalize_text(item["combo_display"]),
            "current_share_text": format_percent_or_dash(item["current_share"]),
            "baseline_share_text": format_percent_or_dash(item["baseline_share"]),
            "share_delta_text": format_percent_or_dash(item["share_delta"]),
            "current_acceptance_rate_text": format_percent_or_dash(item["current_acceptance_rate"]),
            "baseline_acceptance_rate_text": format_percent_or_dash(item["baseline_acceptance_rate"]),
            "impact_route_amount_text": format_wan_or_dash(item["impact_route_amount"]),
            "impact_threshold_text": format_wan_or_dash(item["impact_threshold"]),
            "enter_next_stage_text": format_yes_no(bool(item["enter_next_stage"])),
            "supported_for_funding_text": format_yes_no(bool(item["supported_for_funding"])),
            "decision_reason": normalize_text(item["decision_reason"]),
        }
        for item in combo_results
    ]
    if not combo_table_rows:
        combo_table_rows = [
            {
                "combo_id": "-",
                "combo_display": "当前没有可校验的 2 维或 3 维组合",
                "current_share_text": "-",
                "baseline_share_text": "-",
                "share_delta_text": "-",
                "current_acceptance_rate_text": "-",
                "baseline_acceptance_rate_text": "-",
                "impact_route_amount_text": "-",
                "impact_threshold_text": format_wan_or_dash(asset_thresholds["combo"]["effective"]),
                "enter_next_stage_text": "否",
                "supported_for_funding_text": "-",
                "decision_reason": "命中的异常桶不足以组成 2 维或 3 维组合。",
            }
        ]
    combo_lines.append("")
    combo_lines.append(build_markdown_table(ASSET_COMBO_TABLE_COLUMNS, combo_table_rows))

    return {
        "summary_markdown": "\n".join(summary_lines),
        "factor_detail_markdown": "\n".join(factor_lines),
        "combo_detail_markdown": "\n".join(combo_lines),
    }


def run_asset_stage(
    *,
    granularity: str,
    current_start: str,
    current_end: str,
    baseline_start: str,
    baseline_end: str,
    slice_key: str,
    access_token: str,
    endpoint: str | None = None,
    primary_trace: dict[str, Any] | None = None,
) -> dict[str, Any]:
    slice_display = slice_key
    normalized_granularity = normalize_granularity(granularity)
    base_context = build_context(
        granularity=granularity,
        current_start=current_start,
        current_end=current_end,
        baseline_start=baseline_start,
        baseline_end=baseline_end,
    )

    def build_asset_failure_trace(
        *,
        context: dict[str, Any],
        headline: str,
        summary: str,
        root_cause: dict[str, Any],
        errors: list[str],
        debug_query: dict[str, Any] | None = None,
        slice_snapshot: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        trace = {
            "context": context,
            "slice_key": slice_key,
            "slice_display": slice_display,
            "qualified_combos": [],
            "asset_thresholds": {},
            "slice_context": {},
            "soft_signal_buckets": [],
            "factor_results": [],
            "combo_results": [],
            "asset_display": build_empty_asset_display(),
            "terminal_reason": "R8",
            "terminal_reason_text": build_reason("R8"),
            "next_action": "stop",
            "business_view": business_view(
                headline=headline,
                summary=summary,
                evidence=errors,
            ),
            "root_cause": root_cause,
            "errors": errors,
        }
        if debug_query is not None:
            trace["debug_query"] = debug_query
        if slice_snapshot is not None:
            trace["slice_snapshot"] = slice_snapshot
        return trace

    if normalized_granularity not in SUPPORTED_GRANULARITIES:
        error = unsupported_granularity_error(normalized_granularity)
        trace = build_asset_failure_trace(
            context=base_context,
            headline="当前粒度暂未接入",
            summary="当前版本仅支持日粒度和周粒度的资产维度诊断。",
            root_cause=build_root_cause(
                "unsupported_granularity",
                "资产维度阶段收到当前版本未支持的粒度。",
                granularity=normalized_granularity,
            ),
            errors=[error],
            slice_snapshot={},
        )
        log_stage_event("asset", "阶段失败", slice_key=slice_key, trace=trace)
        return trace
    if_qd, irr24_new = slice_key.split("|", 1)
    slice_display = build_slice_display(if_qd, irr24_new)
    log_stage_event(
        "asset",
        "开始阶段",
        slice_key=slice_key,
        granularity=normalized_granularity,
        current_start=current_start,
        current_end=current_end,
        baseline_start=baseline_start,
        baseline_end=baseline_end,
    )
    primary_trace = primary_trace or run_primary_stage(
        granularity=normalized_granularity,
        current_start=current_start,
        current_end=current_end,
        baseline_start=baseline_start,
        baseline_end=baseline_end,
        access_token=access_token,
        endpoint=endpoint,
        if_qd=if_qd,
        irr24_new=irr24_new,
    )
    slice_snapshot = _current_slice_from_primary(primary_trace, slice_key)
    if not slice_snapshot:
        context = primary_trace.get("context", base_context)
        available_slice_keys = [
            item.get("slice_key", "")
            for item in primary_trace.get("analysis_sequence", []) or primary_trace.get("slice_comparison", [])
        ]
        trace = build_asset_failure_trace(
            context=context,
            headline="没拿到这组订单的一级快照",
            summary="当前无法继续做资产维度诊断，常见原因是切片写法和一级结果不一致，或者一级诊断里本来就没有取到这组订单。",
            root_cause=build_root_cause(
                "missing_primary_snapshot",
                "资产阶段没有在一级诊断结果中找到对应切片快照。",
                requested_slice_key=slice_key,
                requested_slice_display=slice_display,
                available_slice_keys=available_slice_keys[:20],
                primary_row_count=len(available_slice_keys),
            ),
            errors=[
                f"请求切片：{slice_display}。",
                f"一级结果中的候选切片数：{len(available_slice_keys)}。",
                f"一级诊断结果中未找到切片 {slice_key}。",
            ],
            slice_snapshot={},
        )
        log_stage_event("asset", "阶段失败", slice_key=slice_key, trace=trace)
        return trace

    current_period = primary_trace["context"]["current_period"]
    baseline_period = primary_trace["context"]["baseline_period"]
    metrics = [
        client.metric(METRIC_ACCEPTANCE_RATE),
        client.metric(METRIC_ROUTING_AMOUNT),
    ]
    dimensions = build_main_dimensions(granularity=normalized_granularity, include_asset=True)
    current_filter = build_main_rules(
        start=current_period["start"],
        end=current_period["end"],
        if_qd=if_qd,
        irr24_new=irr24_new,
    )
    baseline_filter = build_main_rules(
        start=baseline_period["start"],
        end=baseline_period["end"],
        if_qd=if_qd,
        irr24_new=irr24_new,
    )
    current_result, current_error = _query_rows(
        access_token=access_token,
        metric_list=metrics,
        dimension_list=dimensions,
        filter_payload=current_filter,
        endpoint=endpoint,
    )
    baseline_result, baseline_error = _query_rows(
        access_token=access_token,
        metric_list=metrics,
        dimension_list=dimensions,
        filter_payload=baseline_filter,
        endpoint=endpoint,
    )

    if current_error or baseline_error:
        query_errors = [item for item in [current_error, baseline_error] if item]
        trace = build_asset_failure_trace(
            context=primary_trace["context"],
            headline="没拿到这组订单的资产维度分析结果",
            summary="当前无法完成这组订单的资产维度诊断，因为资产维度查询本身失败了。",
            root_cause=build_root_cause(
                "query_error",
                "资产维度查询失败。",
                slice_key=slice_key,
                slice_display=slice_display,
                current_error=current_error,
                baseline_error=baseline_error,
            ),
            errors=query_errors,
            debug_query=build_period_debug_snapshot(
                current_result=current_result,
                baseline_result=baseline_result,
                current_filter=current_filter,
                baseline_filter=baseline_filter,
            ),
            slice_snapshot=slice_snapshot,
        )
        log_stage_event("asset", "阶段失败", slice_key=slice_key, trace=trace)
        return trace

    current_records = _prepare_asset_records(current_result.get("rows", []))
    baseline_records = _prepare_asset_records(baseline_result.get("rows", []))
    if not current_records or not baseline_records:
        errors: list[str] = []
        if not current_records:
            errors.append("当前周期没有拿到这组订单的资产维度数据。")
        if not baseline_records:
            errors.append("对比周期没有拿到这组订单的资产维度数据。")
        trace = build_asset_failure_trace(
            context=primary_trace["context"],
            headline="没拿到这组订单的资产维度数据",
            summary="当前期或对比期缺少这组订单的可比资产维度数据，暂时不能继续判断是不是资产维度变化导致下降。",
            root_cause=build_root_cause(
                "missing_slice_data",
                "资产维度阶段缺少当前期或对比期切片数据。",
                slice_key=slice_key,
                slice_display=slice_display,
                current_row_count=len(current_records),
                baseline_row_count=len(baseline_records),
                current_period=current_period,
                baseline_period=baseline_period,
            ),
            errors=errors,
            debug_query=build_period_debug_snapshot(
                current_result=current_result,
                baseline_result=baseline_result,
                current_filter=current_filter,
                baseline_filter=baseline_filter,
            ),
            slice_snapshot=slice_snapshot,
        )
        log_stage_event("asset", "阶段失败", slice_key=slice_key, trace=trace)
        return trace

    current_slice_rate = to_float(slice_snapshot.get("current_rate"))
    baseline_slice_rate = to_float(slice_snapshot.get("baseline_rate"))
    current_slice_route_amount = to_float(slice_snapshot.get("current_route_amount"))
    current_slice_drag_amount = to_float(slice_snapshot.get("drag_amount"))
    asset_thresholds = _build_asset_thresholds(current_slice_drag_amount=current_slice_drag_amount)
    slice_context = _build_asset_slice_context(
        current_slice_rate=current_slice_rate,
        baseline_slice_rate=baseline_slice_rate,
        current_slice_route_amount=current_slice_route_amount,
        current_slice_drag_amount=current_slice_drag_amount,
    )
    factor_results, hit_buckets = _build_factor_results(
        current_records=current_records,
        baseline_records=baseline_records,
        current_slice_rate=current_slice_rate,
        baseline_slice_rate=baseline_slice_rate,
        current_slice_route_amount=current_slice_route_amount,
        asset_thresholds=asset_thresholds,
    )
    combo_results, qualified_combos = _build_combo_results(
        hits=hit_buckets,
        current_records=current_records,
        baseline_records=baseline_records,
        prev_slice_rate=baseline_slice_rate,
        current_slice_route_amount=current_slice_route_amount,
        asset_thresholds=asset_thresholds,
    )
    hit_factor_results = [item for item in factor_results if item["final_decision"] == "hit"]
    strongest_hit_buckets = sorted(
        [
            dict(bucket)
            for factor_result in hit_factor_results
            for bucket in factor_result["buckets"]
            if bucket["is_hit"]
        ],
        key=lambda item: to_float(item["impact_route_amount"]),
        reverse=True,
    )
    soft_signal_buckets = sorted(
        [
            dict(bucket)
            for factor_result in factor_results
            for bucket in factor_result["buckets"]
            if bucket.get("is_near_miss")
        ],
        key=lambda item: to_float(item["impact_route_amount"]),
        reverse=True,
    )

    terminal_reason: str | None = None
    next_action = "run_funding"
    root_cause: dict[str, Any] | None = None
    if not hit_factor_results:
        terminal_reason = "R4"
        next_action = "stop"
        if soft_signal_buckets:
            root_cause = build_root_cause(
                "asset_dimension_signals_below_bucket_threshold",
                "资产维度发现了若干疑似异常桶，但影响路由金额均未达到识别门槛。",
                slice_key=slice_key,
                slice_display=slice_display,
                bucket_drag_absolute_threshold=ASSET_BUCKET_DRAG_ABSOLUTE_THRESHOLD,
                bucket_drag_relative_threshold=ASSET_BUCKET_DRAG_RELATIVE_THRESHOLD,
                bucket_drag_effective_threshold=asset_thresholds["bucket"]["effective"],
                slice_drag_amount=round_float(current_slice_drag_amount, 2),
                strongest_near_misses=[
                    {
                        "factor_label": normalize_text(item.get("factor_label")),
                        "bucket_label": normalize_text(item.get("bucket_label")),
                        "impact_route_amount": round_float(to_float(item.get("impact_route_amount")), 2),
                        "impact_threshold": round_float(to_float(item.get("impact_threshold")), 2),
                    }
                    for item in soft_signal_buckets[:5]
                ],
            )
        else:
            root_cause = build_root_cause(
                "no_asset_dimension_anomaly",
                "资产维度里没有发现达到识别门槛的异常桶。",
                slice_key=slice_key,
                slice_display=slice_display,
                bucket_drag_absolute_threshold=ASSET_BUCKET_DRAG_ABSOLUTE_THRESHOLD,
                bucket_drag_relative_threshold=ASSET_BUCKET_DRAG_RELATIVE_THRESHOLD,
                bucket_drag_effective_threshold=asset_thresholds["bucket"]["effective"],
                slice_drag_amount=round_float(current_slice_drag_amount, 2),
            )
    elif not qualified_combos:
        terminal_reason = "R5"
        next_action = "stop"
        root_cause = build_root_cause(
            "asset_dimension_changes_below_combo_threshold",
            "资产维度已经出现异常桶，但没有形成达到第四阶段门槛的高影响组合。",
            slice_key=slice_key,
            slice_display=slice_display,
            combo_drag_absolute_threshold=ASSET_COMBO_DRAG_ABSOLUTE_THRESHOLD,
            combo_drag_relative_threshold=ASSET_COMBO_DRAG_RELATIVE_THRESHOLD,
            combo_drag_effective_threshold=asset_thresholds["combo"]["effective"],
            slice_drag_amount=round_float(current_slice_drag_amount, 2),
            strongest_hits=[
                {
                    "factor_label": normalize_text(item.get("factor_label")),
                    "bucket_label": normalize_text(item.get("bucket_label")),
                    "impact_route_amount": round_float(to_float(item.get("impact_route_amount")), 2),
                    "impact_threshold": round_float(to_float(item.get("impact_threshold")), 2),
                }
                for item in strongest_hit_buckets[:5]
            ],
        )
    asset_display = _build_asset_display(
        slice_display=slice_display,
        slice_context=slice_context,
        asset_thresholds=asset_thresholds,
        factor_results=factor_results,
        combo_results=combo_results,
        qualified_combos=qualified_combos,
        soft_signal_buckets=soft_signal_buckets,
        terminal_reason=terminal_reason,
    )
    if terminal_reason == "R4":
        if soft_signal_buckets:
            terminal_reason_text = "资产维度发现疑似异常桶，但影响路由金额未达到识别门槛"
        else:
            terminal_reason_text = "资产维度未发现达到识别门槛的高影响异常桶"
    elif terminal_reason == "R5":
        terminal_reason_text = "资产维度已出现异常桶，但未形成达到第四阶段门槛的高影响组合"
    else:
        terminal_reason_text = build_reason(terminal_reason)

    trace = {
        "slice_key": slice_key,
        "slice_display": slice_display,
        "qualified_combos": qualified_combos,
        "asset_thresholds": asset_thresholds,
        "slice_context": slice_context,
        "soft_signal_buckets": soft_signal_buckets,
        "factor_results": factor_results,
        "combo_results": combo_results,
        "asset_display": asset_display,
        "terminal_reason": terminal_reason,
        "terminal_reason_text": terminal_reason_text,
        "next_action": next_action,
        "root_cause": root_cause,
        "errors": [],
        "context": primary_trace["context"],
    }
    log_stage_event("asset", "阶段完成", slice_key=slice_key, trace=trace)
    return trace




def run_funding_stage(
    *,
    granularity: str,
    current_start: str,
    current_end: str,
    baseline_start: str,
    baseline_end: str,
    slice_key: str,
    combo_id: str | None,
    combo_key: str | None,
    access_token: str,
    endpoint: str | None = None,
    asset_trace: dict[str, Any] | None = None,
) -> dict[str, Any]:
    normalized_granularity = normalize_granularity(granularity)
    if normalized_granularity not in SUPPORTED_GRANULARITIES:
        context = build_context(
            granularity=granularity,
            current_start=current_start,
            current_end=current_end,
            baseline_start=baseline_start,
            baseline_end=baseline_end,
        )
        error = unsupported_granularity_error(normalized_granularity)
        trace = {
            "context": context,
            "slice_key": slice_key,
            "combo_id": normalize_text(combo_id),
            "combo_key": normalize_text(combo_key),
            "combo_display": "",
            "matched_projects": [],
            "funding_amount_delta": None,
            "project_count_delta": None,
            "terminal_reason": "R8",
            "terminal_reason_text": build_reason("R8"),
            "business_view": business_view(
                headline="当前粒度暂未接入",
                summary="当前版本仅支持日粒度和周粒度的第四阶段闭环分析。",
                evidence=[error],
            ),
            "root_cause": build_root_cause(
                "unsupported_granularity",
                "第四阶段收到当前版本未支持的粒度。",
                granularity=normalized_granularity,
            ),
            "errors": [error],
        }
        log_stage_event("funding", "阶段失败", slice_key=slice_key, trace=trace)
        return trace
    normalized_combo_id = normalize_text(combo_id)
    normalized_combo_key = normalize_text(combo_key)
    requested_combo_ref = normalized_combo_key or normalized_combo_id
    log_stage_event(
        "funding",
        "开始阶段",
        slice_key=slice_key,
        combo_id=normalized_combo_id,
        combo_key=normalized_combo_key,
        granularity=normalized_granularity,
        current_start=current_start,
        current_end=current_end,
        baseline_start=baseline_start,
        baseline_end=baseline_end,
    )
    asset_trace = asset_trace or run_asset_stage(
        granularity=granularity,
        current_start=current_start,
        current_end=current_end,
        baseline_start=baseline_start,
        baseline_end=baseline_end,
        slice_key=slice_key,
        access_token=access_token,
        endpoint=endpoint,
    )
    qualified_combos = asset_trace.get("qualified_combos", [])
    if not qualified_combos:
        abnormal_factor_labels = [
            normalize_text(item.get("factor_label"))
            for item in asset_trace.get("factor_results", [])
            if normalize_text(item.get("final_decision")) == "hit"
        ]
        if not abnormal_factor_labels:
            abnormal_factor_labels = [
                normalize_text(item.get("factor_label"))
                for item in asset_trace.get("abnormal_factors", [])
            ]
        evidence: list[str] = []
        if abnormal_factor_labels:
            evidence.append(f'资产维度阶段只命中了这些异常维度：{"、".join(label for label in abnormal_factor_labels if label)}。')
        evidence.append("但资产维度阶段没有产出可进入第四阶段的高影响组合。")
        if requested_combo_ref:
            evidence.append(f"当前请求的组合引用：{requested_combo_ref}。")
        log_stage_event(
            "funding",
            "阶段失败",
            slice_key=slice_key,
            combo_id=normalized_combo_id,
            combo_key=normalized_combo_key,
            error="资产阶段没有产出可闭环组合",
        )
        trace = {
            "slice_key": slice_key,
            "combo_id": normalized_combo_id,
            "combo_key": normalized_combo_key,
            "combo_display": "",
            "matched_projects": [],
            "funding_amount_delta": None,
            "project_count_delta": None,
            "terminal_reason": "R8",
            "terminal_reason_text": build_reason("R8"),
            "business_view": business_view(
                headline="当前不该进入资金闭环阶段",
                summary="资产维度阶段只识别到异常维度，还没有形成满足第四阶段门槛的高影响组合，因此当前不能继续往下跑。",
                evidence=evidence,
            ),
            "root_cause": build_root_cause(
                "missing_qualified_combos",
                "资产阶段未产出可进入第四阶段的组合。",
                slice_key=slice_key,
                requested_combo_id=normalized_combo_id,
                requested_combo_key=normalized_combo_key,
                abnormal_factor_labels=[label for label in abnormal_factor_labels if label],
                asset_terminal_reason=asset_trace.get("terminal_reason"),
                asset_next_action=asset_trace.get("next_action"),
            ),
            "errors": ["资产阶段没有产出 qualified_combos，不能继续运行 funding。"],
        }
        return trace

    combo = None
    if normalized_combo_key:
        combo = next((item for item in qualified_combos if normalize_text(item.get("combo_key")) == normalized_combo_key), None)
    elif normalized_combo_id:
        combo = next((item for item in qualified_combos if normalize_text(item.get("combo_id")) == normalized_combo_id), None)
    if combo is None:
        available_combo_refs = [
            {
                "combo_id": normalize_text(item.get("combo_id")),
                "combo_key": normalize_text(item.get("combo_key")),
                "combo_display": normalize_text(item.get("combo_display")),
            }
            for item in qualified_combos
        ]
        log_stage_event(
            "funding",
            "阶段失败",
            slice_key=slice_key,
            combo_id=normalized_combo_id,
            combo_key=normalized_combo_key,
            error=f"未在 asset trace 中找到组合 {requested_combo_ref}",
        )
        trace = {
            "slice_key": slice_key,
            "combo_id": normalized_combo_id,
            "combo_key": normalized_combo_key,
            "combo_display": "",
            "matched_projects": [],
            "funding_amount_delta": None,
            "project_count_delta": None,
            "terminal_reason": "R8",
            "terminal_reason_text": build_reason("R8"),
            "business_view": business_view(
                headline="资金闭环失败",
                summary="当前请求的组合引用和资产阶段真实产出的可闭环组合对不上，无法继续做第四阶段闭环。",
                evidence=[
                    f"当前请求的组合引用：{requested_combo_ref}。",
                    f"资产阶段可用组合数：{len(available_combo_refs)}。",
                ],
            ),
            "root_cause": build_root_cause(
                "combo_reference_mismatch",
                "资金阶段收到的组合引用与资产阶段产出的 qualified_combos 不一致。",
                slice_key=slice_key,
                requested_combo_id=normalized_combo_id,
                requested_combo_key=normalized_combo_key,
                available_combos=available_combo_refs,
            ),
            "errors": [f"未在 asset trace 中找到组合 {requested_combo_ref}。"],
        }
        return trace

    unsupported_items = [
        item for item in combo["factor_items"]
        if item["factor_key"] not in FUNDING_SUPPORTED_FACTORS
    ]
    if unsupported_items:
        log_stage_event(
            "funding",
            "阶段失败",
            slice_key=slice_key,
            combo_id=normalize_text(combo.get("combo_id")),
            combo_key=normalize_text(combo.get("combo_key")),
            unsupported_factors=[item["factor_label"] for item in unsupported_items],
        )
        trace = {
            "slice_key": slice_key,
            "combo_id": normalize_text(combo.get("combo_id")),
            "combo_key": normalize_text(combo.get("combo_key")),
            "combo_display": normalize_text(combo.get("combo_display")),
            "matched_projects": [],
            "funding_amount_delta": None,
            "project_count_delta": None,
            "terminal_reason": "R8",
            "terminal_reason_text": build_reason("R8"),
            "business_view": business_view(
                headline="当前组合暂不支持资金侧闭环",
                summary="该组合包含当前版本未接入资金映射字段的因子，暂时无法判断是否对应敏感资方收缩。",
                evidence=[f'未支持因子：{",".join(item["factor_label"] for item in unsupported_items)}。'],
            ),
            "root_cause": build_root_cause(
                "unsupported_funding_factors",
                "组合包含当前资金闭环阶段尚未支持映射的因子。",
                slice_key=slice_key,
                combo_id=normalize_text(combo.get("combo_id")),
                combo_key=normalize_text(combo.get("combo_key")),
                unsupported_factors=[item["factor_label"] for item in unsupported_items],
            ),
            "errors": [f'组合 {normalize_text(combo.get("combo_id"))} 包含当前版本不支持闭环的因子：{",".join(item["factor_label"] for item in unsupported_items)}'],
        }
        return trace

    asset_slice_key = normalize_text(asset_trace.get("slice_key")) or slice_key
    irr24_new = ""
    if "|" in asset_slice_key:
        _, irr24_new = asset_slice_key.split("|", 1)
    if not irr24_new:
        irr24_new = normalize_text(asset_trace.get("slice_snapshot", {}).get("irr24_new"))
    target_cp_dj = normalize_cp_dj(irr24_new)
    current_period = asset_trace["context"]["current_period"]
    baseline_period = asset_trace["context"]["baseline_period"]

    metrics = [client.metric(METRIC_FUNDING_AMOUNT, "放款金额-资金项目", "simple")]
    dimensions = build_funding_dimensions()
    current_result, current_error = _query_rows(
        access_token=access_token,
        metric_list=metrics,
        row_dimension_list=dimensions,
        filter_payload=build_funding_rules(
            start=current_period["start"],
            end=current_period["end"],
        ),
        endpoint=endpoint,
    )
    baseline_result, baseline_error = _query_rows(
        access_token=access_token,
        metric_list=metrics,
        row_dimension_list=dimensions,
        filter_payload=build_funding_rules(
            start=baseline_period["start"],
            end=baseline_period["end"],
        ),
        endpoint=endpoint,
    )

    if current_error or baseline_error:
        log_stage_event(
            "funding",
            "阶段失败",
            slice_key=slice_key,
            combo_id=normalize_text(combo.get("combo_id")),
            combo_key=normalize_text(combo.get("combo_key")),
            errors=[item for item in [current_error, baseline_error] if item],
        )
        trace = {
            "slice_key": slice_key,
            "combo_id": normalize_text(combo.get("combo_id")),
            "combo_key": normalize_text(combo.get("combo_key")),
            "combo_display": normalize_text(combo.get("combo_display")),
            "matched_projects": [],
            "funding_amount_delta": None,
            "project_count_delta": None,
            "terminal_reason": "R8",
            "terminal_reason_text": build_reason("R8"),
            "business_view": business_view(
                headline="资金项目查询失败",
                summary="当前无法完成该组合的敏感资方侧闭环判断。",
                evidence=[item for item in [current_error, baseline_error] if item],
            ),
            "root_cause": build_root_cause(
                "query_error",
                "资金项目查询失败。",
                slice_key=slice_key,
                combo_id=normalize_text(combo.get("combo_id")),
                combo_key=normalize_text(combo.get("combo_key")),
                current_error=current_error,
                baseline_error=baseline_error,
            ),
            "errors": [item for item in [current_error, baseline_error] if item],
        }
        return trace

    def normalize_funding_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        normalized: list[dict[str, Any]] = []
        for row in rows:
            normalized_cp_dj = normalize_cp_dj(client.extract_row_value(row, "cp_dj"))
            if normalized_cp_dj != target_cp_dj:
                continue
            project_row = {
                "capital_project_name": normalize_text(client.extract_row_value(row, "capital_project_name")),
                "age_range": normalize_text(client.extract_row_value(row, "age_range")),
                "allow_identity_city_prov": normalize_text(client.extract_row_value(row, "allow_identity_city_prov")),
                "chk_identity_card_effc_term_floor_days": normalize_text(client.extract_row_value(row, "chk_identity_card_effc_term_floor_days")),
                "cp_dj": normalize_text(client.extract_row_value(row, "cp_dj")),
                "funding_amount": to_float(client.extract_row_value(row, METRIC_FUNDING_AMOUNT)),
            }
            normalized.append(project_row)
        return normalized

    current_projects = normalize_funding_rows(current_result.get("rows", []))
    baseline_projects = normalize_funding_rows(baseline_result.get("rows", []))

    def is_sensitive(project_row: dict[str, Any]) -> bool:
        return all(_project_sensitive_to_factor(project_row, factor_item) for factor_item in combo["factor_items"])

    current_matched = [item for item in current_projects if is_sensitive(item)]
    baseline_matched = [item for item in baseline_projects if is_sensitive(item)]
    if not current_matched and not baseline_matched:
        log_stage_event(
            "funding",
            "阶段失败",
            slice_key=slice_key,
            combo_id=normalize_text(combo.get("combo_id")),
            combo_key=normalize_text(combo.get("combo_key")),
            error=f'未找到与组合 {normalize_text(combo.get("combo_id"))} 匹配的敏感资方相关项目',
        )
        trace = {
            "slice_key": slice_key,
            "combo_id": normalize_text(combo.get("combo_id")),
            "combo_key": normalize_text(combo.get("combo_key")),
            "combo_display": normalize_text(combo.get("combo_display")),
            "matched_projects": [],
            "funding_amount_delta": None,
            "project_count_delta": None,
            "terminal_reason": "R8",
            "terminal_reason_text": build_reason("R8"),
            "business_view": business_view(
                headline="未找到对应敏感资方相关项目",
                summary="当前字段条件下未识别出与该异常组合直接对应的敏感资方相关项目，暂时无法完成敏感资方侧闭环。",
                evidence=[f'组合 {normalize_text(combo.get("combo_id"))} 没有匹配到敏感资方相关项目。'],
            ),
            "root_cause": build_root_cause(
                "no_sensitive_projects_matched",
                "资金模型中没有识别到与该组合直接对应的敏感资方相关项目。",
                slice_key=slice_key,
                combo_id=normalize_text(combo.get("combo_id")),
                combo_key=normalize_text(combo.get("combo_key")),
                combo_display=normalize_text(combo.get("combo_display")),
            ),
            "errors": [f'未找到与组合 {normalize_text(combo.get("combo_id"))} 匹配的敏感资方相关项目。'],
        }
        return trace

    grouped_projects: dict[str, dict[str, Any]] = {}
    for row in baseline_matched:
        project_name = row["capital_project_name"] or "UNKNOWN"
        grouped = grouped_projects.setdefault(
            project_name,
            {"capital_project_name": project_name, "baseline_funding_amount": 0.0, "current_funding_amount": 0.0},
        )
        grouped["baseline_funding_amount"] += row["funding_amount"]
    for row in current_matched:
        project_name = row["capital_project_name"] or "UNKNOWN"
        grouped = grouped_projects.setdefault(
            project_name,
            {"capital_project_name": project_name, "baseline_funding_amount": 0.0, "current_funding_amount": 0.0},
        )
        grouped["current_funding_amount"] += row["funding_amount"]

    matched_projects = sorted(
        [
            {
                "capital_project_name": project_name,
                "baseline_funding_amount": round_float(values["baseline_funding_amount"], 2),
                "current_funding_amount": round_float(values["current_funding_amount"], 2),
                "funding_amount_delta": round_float(values["current_funding_amount"] - values["baseline_funding_amount"], 2),
            }
            for project_name, values in grouped_projects.items()
        ],
        key=lambda item: abs(to_float(item["funding_amount_delta"])),
        reverse=True,
    )

    baseline_total = sum(to_float(item["baseline_funding_amount"]) for item in matched_projects)
    current_total = sum(to_float(item["current_funding_amount"]) for item in matched_projects)
    baseline_project_count = sum(1 for item in matched_projects if to_float(item["baseline_funding_amount"]) > 0)
    current_project_count = sum(1 for item in matched_projects if to_float(item["current_funding_amount"]) > 0)
    funding_amount_delta = current_total - baseline_total
    project_count_delta = current_project_count - baseline_project_count

    terminal_reason = "R7" if current_total < baseline_total and current_project_count <= baseline_project_count else "R6"
    if terminal_reason == "R7":
        business = business_view(
            headline="已闭环到敏感资方收缩",
            summary="异常组合对应的敏感资方相关项目数量未增加，且放款金额下降，可以将下降进一步闭环到敏感资方侧。",
            evidence=[
                f"敏感资方相关项目放款金额变化 {round_float(funding_amount_delta, 2)}。",
                f"敏感资方相关项目数变化 {project_count_delta}。",
            ],
        )
    else:
        business = business_view(
            headline="组合异常成立，但未完成敏感资方侧闭环",
            summary="异常组合已经成立，但敏感资方相关项目未呈现同步收缩，暂时不能把原因直接落到敏感资方变化。",
            evidence=[
                f"敏感资方相关项目放款金额变化 {round_float(funding_amount_delta, 2)}。",
                f"敏感资方相关项目数变化 {project_count_delta}。",
            ],
        )
    trace = {
        "slice_key": slice_key,
        "combo_id": normalize_text(combo.get("combo_id")),
        "combo_key": normalize_text(combo.get("combo_key")),
        "combo_display": normalize_text(combo.get("combo_display")),
        "matched_projects": matched_projects,
        "funding_amount_delta": round_float(funding_amount_delta, 2),
        "project_count_delta": project_count_delta,
        "baseline_project_count": baseline_project_count,
        "current_project_count": current_project_count,
        "terminal_reason": terminal_reason,
        "terminal_reason_text": build_reason(terminal_reason),
        "business_view": business,
        "root_cause": None,
        "errors": [],
    }
    log_stage_event(
        "funding",
        "阶段完成",
        slice_key=slice_key,
        combo_id=normalize_text(combo.get("combo_id")),
        combo_key=normalize_text(combo.get("combo_key")),
        trace=trace,
    )
    return trace


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="承接率下降归因阶段式脚本。")
    subparsers = parser.add_subparsers(dest="command", required=True)

    primary_parser = subparsers.add_parser("primary", help="一级诊断：判断大盘、定位异常切片。")
    primary_parser.add_argument("--granularity", required=True)
    primary_parser.add_argument("--current-start", required=True)
    primary_parser.add_argument("--current-end", required=True)
    primary_parser.add_argument("--baseline-start", required=True)
    primary_parser.add_argument("--baseline-end", required=True)
    primary_parser.add_argument("--access-token", default="")
    primary_parser.add_argument("--endpoint", default="")

    capital_parser = subparsers.add_parser("capital", help="资方分布诊断。")
    capital_parser.add_argument("--granularity", required=True)
    capital_parser.add_argument("--current-start", required=True)
    capital_parser.add_argument("--current-end", required=True)
    capital_parser.add_argument("--baseline-start", required=True)
    capital_parser.add_argument("--baseline-end", required=True)
    capital_parser.add_argument("--slice-key", required=True)
    capital_parser.add_argument("--access-token", default="")
    capital_parser.add_argument("--endpoint", default="")

    asset_parser = subparsers.add_parser("asset", help="资产维度诊断。")
    asset_parser.add_argument("--granularity", required=True)
    asset_parser.add_argument("--current-start", required=True)
    asset_parser.add_argument("--current-end", required=True)
    asset_parser.add_argument("--baseline-start", required=True)
    asset_parser.add_argument("--baseline-end", required=True)
    asset_parser.add_argument("--slice-key", required=True)
    asset_parser.add_argument("--access-token", default="")
    asset_parser.add_argument("--endpoint", default="")

    funding_parser = subparsers.add_parser("funding", help="敏感资方闭环（基于资金项目映射）。")
    funding_parser.add_argument("--granularity", required=True)
    funding_parser.add_argument("--current-start", required=True)
    funding_parser.add_argument("--current-end", required=True)
    funding_parser.add_argument("--baseline-start", required=True)
    funding_parser.add_argument("--baseline-end", required=True)
    funding_parser.add_argument("--slice-key", required=True)
    funding_parser.add_argument("--combo-id", default="")
    funding_parser.add_argument("--combo-key", default="")
    funding_parser.add_argument("--access-token", default="")
    funding_parser.add_argument("--endpoint", default="")
    return parser


def main(argv: list[str] | None = None) -> int:
    configure_stdio()
    configure_debug_logging()
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "command", "") == "funding" and not (normalize_text(getattr(args, "combo_key", "")) or normalize_text(getattr(args, "combo_id", ""))):
        parser.error("funding 阶段至少需要传入 --combo-key 或 --combo-id。")
    access_token = resolve_access_token(getattr(args, "access_token", "") or None)
    endpoint = getattr(args, "endpoint", "") or None
    logger.info(
        "命令开始执行 {}",
        json.dumps(
            {
                "command": getattr(args, "command", ""),
                "argv": argv or sys.argv[1:],
                "debug_log_file": str(DEBUG_LOG_FILE),
            },
            ensure_ascii=False,
            default=str,
        ),
    )

    if args.command == "primary":
        result = run_primary_stage(
            granularity=args.granularity,
            current_start=args.current_start,
            current_end=args.current_end,
            baseline_start=args.baseline_start,
            baseline_end=args.baseline_end,
            access_token=access_token,
            endpoint=endpoint,
        )
    elif args.command == "capital":
        result = run_capital_stage(
            granularity=args.granularity,
            current_start=args.current_start,
            current_end=args.current_end,
            baseline_start=args.baseline_start,
            baseline_end=args.baseline_end,
            slice_key=args.slice_key,
            access_token=access_token,
            endpoint=endpoint,
        )
    elif args.command == "asset":
        result = run_asset_stage(
            granularity=args.granularity,
            current_start=args.current_start,
            current_end=args.current_end,
            baseline_start=args.baseline_start,
            baseline_end=args.baseline_end,
            slice_key=args.slice_key,
            access_token=access_token,
            endpoint=endpoint,
        )
    else:
        result = run_funding_stage(
            granularity=args.granularity,
            current_start=args.current_start,
            current_end=args.current_end,
            baseline_start=args.baseline_start,
            baseline_end=args.baseline_end,
            slice_key=args.slice_key,
            combo_id=args.combo_id or None,
            combo_key=args.combo_key or None,
            access_token=access_token,
            endpoint=endpoint,
        )

    print(json_dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

