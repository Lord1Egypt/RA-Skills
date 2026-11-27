#!/usr/bin/env python3
"""回归执行器与离线评测器共用的断言和文本规范化逻辑。"""

from __future__ import annotations

import re
import json
import unicodedata
from typing import Any


MATCH_MODES = {"normalized", "strict"}
EXPECTED_BEHAVIORS = {"normal", "fallback", "error"}
IPV4_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
MAC_PATTERN = re.compile(r"(?i)(?<![0-9a-f])(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}(?![0-9a-f])")
HYPHEN_TRANSLATION = str.maketrans({
    "\u2010": "-",  # hyphen
    "\u2011": "-",  # non-breaking hyphen
    "\u2012": "-",  # figure dash
    "\u2013": "-",  # en dash
    "\u2014": "-",  # em dash
    "\u2212": "-",  # minus sign
    "\ufe63": "-",  # small hyphen-minus
    "\uff0d": "-",  # fullwidth hyphen-minus
    "\u00a0": " ",  # no-break space
    "\u2007": " ",  # figure space
    "\u202f": " ",  # narrow no-break space
})
MARKDOWN_PATTERNS = [
    (re.compile(r"\*\*([^*]+)\*\*"), r"\1"),
    (re.compile(r"__([^_]+)__"), r"\1"),
    (re.compile(r"`([^`]+)`"), r"\1"),
    (re.compile(r"^#{1,6}\s+", re.MULTILINE), ""),
    (re.compile(r"^\s*[-*]\s+", re.MULTILINE), ""),
]


def strip_markdown(value: Any) -> str:
    """剥离常见 Markdown 格式符号，避免格式差异导致断言失败。"""
    text = str(value)
    for pattern, replacement in MARKDOWN_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def normalize_text(value: Any) -> str:
    """统一兼容等价字符并剥离 Markdown 格式；不改变大小写，也不做模糊或同义词匹配。"""
    text = unicodedata.normalize("NFKC", strip_markdown(value)).translate(HYPHEN_TRANSLATION)
    return re.sub(r"\s+", " ", text).strip()


def get_match_mode(spec: dict[str, Any]) -> str:
    mode = str(spec.get("text_match_mode", "normalized")).strip().lower()
    if mode not in MATCH_MODES:
        raise ValueError(f"text_match_mode必须是normalized或strict，实际为{mode!r}")
    return mode


def get_expected_behavior(spec: dict[str, Any]) -> str:
    """读取用例的预期行为类型，区分正常回复、预期兜底与预期异常。"""
    behavior = str(spec.get("expected_behavior", "normal")).strip().lower()
    if behavior not in EXPECTED_BEHAVIORS:
        raise ValueError(f"expected_behavior必须是normal/fallback/error，实际为{behavior!r}")
    return behavior


def validate_case_spec(spec: dict[str, Any], case_id: str = "<case>") -> None:
    """Reject empty or contradictory assertions before a regression run starts."""
    list_fields = (
        "expected_substrings", "forbidden_substrings", "runtime_failure_substrings",
        "expected_fallback_substrings", "required_nodes", "forbidden_nodes",
    )
    for field in list_fields:
        values = _as_list(spec.get(field))
        if any(not str(value).strip() for value in values):
            raise ValueError(f"{case_id}: {field}不允许空字符串")
    for group in _as_list(spec.get("expected_any_groups")):
        values = _as_list(group)
        if not values or any(not str(value).strip() for value in values):
            raise ValueError(f"{case_id}: expected_any_groups不允许空组或空字符串")
    route_markers = spec.get("route_markers")
    if isinstance(route_markers, dict):
        for route, markers in route_markers.items():
            values = _as_list(markers)
            if not values or any(not str(value).strip() for value in values):
                raise ValueError(f"{case_id}: route_markers[{route!r}]不允许为空")

    positive = [str(value) for value in _as_list(spec.get("expected_substrings"))]
    positive.extend(str(value) for group in _as_list(spec.get("expected_any_groups")) for value in _as_list(group))
    positive.extend(str(value) for value in _as_list(spec.get("expected_fallback_substrings")))
    failures = [str(value) for value in _as_list(spec.get("runtime_failure_substrings"))]
    overlap = sorted({normalize_text(value) for value in positive} & {normalize_text(value) for value in failures})
    if overlap:
        raise ValueError(f"{case_id}: 期望文本与运行失败文本相互矛盾：{overlap}")

    behavior = get_expected_behavior(spec)
    if behavior == "fallback" and not (
        spec.get("expected_fallback_substrings") or spec.get("expected_substrings")
        or spec.get("expected_any_groups") or spec.get("required_nodes")
    ):
        raise ValueError(f"{case_id}: expected_behavior=fallback必须声明兜底文本或必经节点")


def is_expected_anomaly(flag: str, behavior: str) -> bool:
    """判断某类运行异常是否属于预期行为，避免把预期兜底或预期异常误报为问题。"""
    if behavior == "error" and flag in {"transport_or_sse_error", "http_status_error", "empty_answer"}:
        return True
    return False


def _detect_behavior_mismatch(
    behavior: str,
    result: dict[str, Any],
    answer: str,
    fallback_matches: list[str],
    fallback_markers_declared: bool,
) -> str:
    """检测实际行为与预期行为不符时返回 mismatch 标签名，否则返回空串。"""
    http_status = result.get("http_status")
    has_error = bool(result.get("errors")) or (
        isinstance(http_status, int) and not 200 <= http_status < 300
    )
    if behavior == "error" and not has_error:
        return "behavior_mismatch_expected_error"
    if behavior == "fallback" and fallback_markers_declared and not fallback_matches:
        return "behavior_mismatch_expected_fallback"
    return ""


def contains_text(haystack: Any, needle: Any, mode: str = "normalized") -> bool:
    if mode == "strict":
        return str(needle) in str(haystack)
    if mode != "normalized":
        raise ValueError(f"未知文本匹配模式：{mode!r}")
    return normalize_text(needle) in normalize_text(haystack)


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def resolve_latency_ms(result: dict[str, Any]) -> int | None:
    latency = result.get("latency_ms")
    if isinstance(latency, (int, float)) and not isinstance(latency, bool):
        return round(latency)
    duration = result.get("duration_seconds")
    if isinstance(duration, (int, float)) and not isinstance(duration, bool):
        return round(duration * 1000)
    return None


def evaluate_assertions(
    spec: dict[str, Any], result: dict[str, Any], route: str,
    *, trust_reported_runtime_flags: bool = False,
) -> dict[str, Any]:
    """按统一契约评估答案、节点、运行信号、长度和时延。"""
    validate_case_spec(spec, str(spec.get("case_id", "<case>")))
    mode = get_match_mode(spec)
    expected_behavior = get_expected_behavior(spec)
    answer = str(result.get("answer", ""))
    raw_nodes = result.get("nodes", [])
    nodes = [str(value) for value in raw_nodes] if isinstance(raw_nodes, list) else []

    missing = [
        str(value) for value in _as_list(spec.get("expected_substrings"))
        if not contains_text(answer, value, mode)
    ]
    missing_any_groups: list[list[str]] = []
    for raw_group in _as_list(spec.get("expected_any_groups")):
        group = [str(value) for value in _as_list(raw_group)]
        if group and not any(contains_text(answer, value, mode) for value in group):
            missing_any_groups.append(group)
    forbidden = [
        str(value) for value in _as_list(spec.get("forbidden_substrings"))
        if contains_text(answer, value, mode)
    ]
    missing_nodes = [
        str(value) for value in _as_list(spec.get("required_nodes"))
        if not any(contains_text(node, value, mode) for node in nodes)
    ]
    forbidden_nodes = [
        str(value) for value in _as_list(spec.get("forbidden_nodes"))
        if any(contains_text(node, value, mode) for node in nodes)
    ]

    expected_route = str(spec.get("expected_route", "")).strip()
    route_mismatch = bool(expected_route and route != expected_route)
    runtime_failure_matches = [
        str(value) for value in _as_list(spec.get("runtime_failure_substrings"))
        if contains_text(answer, value, mode)
    ]
    fallback_matches = [
        str(value) for value in _as_list(spec.get("expected_fallback_substrings"))
        if contains_text(answer, value, mode)
    ]

    answer_chars = len(answer)
    min_answer_chars = spec.get("min_answer_chars")
    answer_too_short = bool(
        isinstance(min_answer_chars, (int, float))
        and not isinstance(min_answer_chars, bool)
        and answer_chars < int(min_answer_chars)
    )
    max_answer_chars = spec.get("max_answer_chars")
    answer_too_long = bool(
        isinstance(max_answer_chars, (int, float))
        and not isinstance(max_answer_chars, bool)
        and answer_chars > int(max_answer_chars)
    )

    runtime_anomaly_flags: list[str] = []
    if result.get("errors") and not is_expected_anomaly("transport_or_sse_error", expected_behavior):
        runtime_anomaly_flags.append("transport_or_sse_error")
    http_status = result.get("http_status")
    if (
        isinstance(http_status, int)
        and not 200 <= http_status < 300
        and not is_expected_anomaly("http_status_error", expected_behavior)
    ):
        runtime_anomaly_flags.append("http_status_error")
    if not answer and not is_expected_anomaly("empty_answer", expected_behavior):
        runtime_anomaly_flags.append("empty_answer")
    if answer_too_short:
        runtime_anomaly_flags.append("answer_too_short")
    min_node_count = spec.get("min_node_count")
    if (
        isinstance(min_node_count, (int, float))
        and not isinstance(min_node_count, bool)
        and len(nodes) < int(min_node_count)
    ):
        runtime_anomaly_flags.append("node_count_below_minimum")
    if missing_nodes:
        runtime_anomaly_flags.append("required_node_missing")
    if forbidden_nodes:
        runtime_anomaly_flags.append("forbidden_node_executed")
    if runtime_failure_matches and not is_expected_anomaly("runtime_failure_text", expected_behavior):
        runtime_anomaly_flags.append("runtime_failure_text")
    behavior_mismatch = _detect_behavior_mismatch(
        expected_behavior, result, answer, fallback_matches,
        bool(_as_list(spec.get("expected_fallback_substrings"))),
    )
    if behavior_mismatch:
        runtime_anomaly_flags.append(behavior_mismatch)
    if spec.get("require_done_event") is True and result.get("done_received") is not True:
        runtime_anomaly_flags.append("done_event_missing")
    reported_flags = result.get("runtime_anomaly_flags", [])
    if trust_reported_runtime_flags and isinstance(reported_flags, list):
        for raw_flag in reported_flags:
            flag = str(raw_flag)
            if flag and flag not in runtime_anomaly_flags:
                runtime_anomaly_flags.append(flag)
    if result.get("runtime_anomaly") is True and not runtime_anomaly_flags:
        runtime_anomaly_flags.append("reported_runtime_anomaly")

    latency_ms = resolve_latency_ms(result)
    max_latency_ms = spec.get("max_latency_ms")
    latency_required = isinstance(max_latency_ms, (int, float)) and not isinstance(max_latency_ms, bool)
    latency_missing = bool(latency_required and latency_ms is None)
    latency_exceeded = bool(latency_required and latency_ms is not None and latency_ms > int(max_latency_ms))
    if latency_missing:
        runtime_anomaly_flags.append("latency_missing")

    distinct_ipv4 = sorted(set(IPV4_PATTERN.findall(answer)))
    distinct_mac = sorted({value.upper().replace("-", ":") for value in MAC_PATTERN.findall(answer)})
    max_distinct_ipv4 = spec.get("max_distinct_ipv4")
    max_distinct_mac = spec.get("max_distinct_mac")
    ipv4_count_exceeded = bool(
        isinstance(max_distinct_ipv4, (int, float)) and not isinstance(max_distinct_ipv4, bool)
        and len(distinct_ipv4) > int(max_distinct_ipv4)
    )
    mac_count_exceeded = bool(
        isinstance(max_distinct_mac, (int, float)) and not isinstance(max_distinct_mac, bool)
        and len(distinct_mac) > int(max_distinct_mac)
    )

    assertion_failed = bool(
        missing
        or missing_any_groups
        or forbidden
        or route_mismatch
        or answer_too_long
        or ipv4_count_exceeded
        or mac_count_exceeded
    )
    internal_error_count = 0
    trace_key = spec.get("runtime_trace_variable")
    if trace_key:
        variables = result.get("variables")
        raw_trace = variables.get(str(trace_key)) if isinstance(variables, dict) else None
        try:
            trace = json.loads(raw_trace) if isinstance(raw_trace, str) else raw_trace
            if not isinstance(trace, list):
                raise ValueError("trace must be a per-turn list")
            internal_error_count = len(trace)
            if internal_error_count:
                runtime_anomaly_flags.append("internal_error_record")
        except (ValueError, TypeError):
            runtime_anomaly_flags.append("runtime_trace_invalid_or_missing")
    runtime_anomaly = bool(runtime_anomaly_flags)
    return {
        "text_match_mode": mode,
        "expected_behavior": expected_behavior,
        "missing": missing,
        "missing_any_groups": missing_any_groups,
        "forbidden": forbidden,
        "missing_nodes": missing_nodes,
        "forbidden_nodes": forbidden_nodes,
        "route_mismatch": route_mismatch,
        "runtime_failure_matches": runtime_failure_matches,
        "fallback_matches": fallback_matches,
        "runtime_anomaly_flags": runtime_anomaly_flags,
        "assertion_failed": assertion_failed,
        "runtime_anomaly": runtime_anomaly,
        "internal_error_count": internal_error_count,
        "answer_chars": answer_chars,
        "answer_too_short": answer_too_short,
        "answer_too_long": answer_too_long,
        "latency_ms": latency_ms,
        "latency_missing": latency_missing,
        "latency_exceeded": latency_exceeded,
        "distinct_ipv4_count": len(distinct_ipv4),
        "distinct_mac_count": len(distinct_mac),
        "ipv4_count_exceeded": ipv4_count_exceeded,
        "mac_count_exceeded": mac_count_exceeded,
    }
