#!/usr/bin/env python3
"""
Dimension Inspection Shared Utilities:
- Excel merged cell reading
- Header and column mapping auto-detection
- Tolerance parsing / numeric parsing
- Judgement text normalization
"""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Any, Dict, List, Optional, Tuple


PASS_VALUES = set(["OK", "合格", "√", "○"])
FAIL_VALUES = set(["NOK", "不合格", "NG", "×", "X"])
NONSTANDARD_PASS_VALUES = set(["PASS", "通过", "正确"])
HEADER_KEYWORDS = {
    "seq": ["序号", "NO", "NO.", "SEQ", "顺序号", "Seq", "No"],
    "item": ["检查项目", "项目", "尺寸", "测点", "测量项目", "特性", "Inspection Item", "Item", "Characteristic"],
    "std": ["质量标准", "公差", "标准", "规格", "Tolerance", "要求", "基准", "Standard", "Spec"],
    "method": ["检查方法", "方法", "测量方法", "Method", "检具", "测量工具", "Measurement Method"],
    "data": ["检查数据", "实测值", "数据", "Measurement", "测量值", "实测", "Data", "Value"],
    "judge": ["判定结果", "判定", "结果", "OK/NG", "结论", "Judgement", "Result", "Judge"],
}


def build_merged_map(ws) -> Dict[Tuple[int, int], Tuple[int, int]]:
    merged_map = {}
    for mr in ws.merged_cells.ranges:
        min_col = mr.min_col
        min_row = mr.min_row
        for row_idx in range(mr.min_row, mr.max_row + 1):
            for col_idx in range(mr.min_col, mr.max_col + 1):
                if row_idx != min_row or col_idx != min_col:
                    merged_map[(row_idx, col_idx)] = (min_row, min_col)
    return merged_map


def get_cell_value(ws, row_idx: int, col_idx: int, merged_map: Dict[Tuple[int, int], Tuple[int, int]]) -> Any:
    target = merged_map.get((row_idx, col_idx))
    if target:
        return ws.cell(target[0], target[1]).value
    return ws.cell(row_idx, col_idx).value


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value)
    text = text.replace("\r", "\n").replace("\u3000", " ")
    text = text.replace("（", "(").replace("）", ")")
    text = text.replace("＜", "<=").replace("＞", ">=")
    text = text.replace("≤", "<=").replace("≥", ">=")
    text = text.replace("﹢", "+").replace("－", "-")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", "\n", text)
    return text.strip()


def compact_text(value: Any) -> str:
    return clean_text(value).replace(" ", "").replace("\n", "")


def normalize_header(value: Any) -> str:
    return clean_text(value).upper()


def maybe_parse_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        if math.isnan(value):
            return None
        return float(value)
    text = clean_text(value)
    if not text:
        return None
    text = text.replace(",", "")
    text = text.replace("Φ", "").replace("φ", "")
    match = re.search(r"[-+]?\d+(?:\.\d+)?", text)
    if not match:
        return None
    try:
        return float(match.group(0))
    except ValueError:
        return None


def count_decimals(value: Any) -> Optional[int]:
    text = clean_text(value)
    if not text:
        return None
    match = re.search(r"[-+]?\d+\.(\d+)", text)
    if match:
        return len(match.group(1))
    if maybe_parse_float(value) is not None:
        return 0
    return None


def is_numeric_like(value: Any) -> bool:
    return maybe_parse_float(value) is not None


def is_pass_marker_value(value: Any) -> bool:
    text = clean_text(value)
    if not text:
        return False
    upper_text = text.upper()
    return (
        text in PASS_VALUES
        or upper_text in PASS_VALUES
        or text in FAIL_VALUES
        or upper_text in FAIL_VALUES
        or text in NONSTANDARD_PASS_VALUES
        or upper_text in NONSTANDARD_PASS_VALUES
    )


def is_measurement_value(value: Any) -> bool:
    if value is None or isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        if isinstance(value, float) and math.isnan(value):
            return False
        return True

    text = compact_text(value)
    if not text:
        return False
    if is_pass_marker_value(text):
        return True

    normalized = text.upper()
    normalized = normalized.replace("Φ", "").replace("φ", "")
    normalized = normalized.replace("MM", "")
    normalized = normalized.replace("MPA", "")
    normalized = normalized.replace("°", "")
    return bool(re.fullmatch(r"[-+]?\d+(?:\.\d+)?", normalized))


def contains_numeric_spec(text: str) -> bool:
    normalized = compact_text(text)
    return bool(re.search(r"\d", normalized) and re.search(r"(±|\+|/|<=|>=|<|>)", normalized))


def classify_judge_text(judge_text: Any) -> Tuple[str, str]:
    text = clean_text(judge_text)
    upper_text = text.upper()
    if not text:
        return "missing", text
    if text in PASS_VALUES or upper_text in PASS_VALUES:
        return "pass", "OK" if upper_text == "OK" else text
    if text in FAIL_VALUES or upper_text in FAIL_VALUES:
        return "fail", upper_text if upper_text in set(["NOK", "NG"]) else text
    if text in NONSTANDARD_PASS_VALUES or upper_text in NONSTANDARD_PASS_VALUES:
        return "nonstandard_pass", upper_text if upper_text == "PASS" else text
    return "other", text


def normalize_std_text(text: Any) -> str:
    normalized = compact_text(text)
    normalized = normalized.replace("°", "")
    normalized = normalized.replace("MPA", "")
    normalized = normalized.replace("MM", "")
    normalized = normalized.replace("Φ", "").replace("φ", "")
    return normalized


def parse_tolerance(text: Any) -> Optional[Dict[str, Any]]:
    raw = clean_text(text)
    if not raw:
        return None
    normalized = normalize_std_text(raw)
    normalized = normalized.replace("＋", "+").replace("／", "/")

    match = re.search(r"([+-]?\d+(?:\.\d+)?)±([+-]?\d+(?:\.\d+)?)", normalized)
    if match:
        nominal = float(match.group(1))
        delta = abs(float(match.group(2)))
        return {
            "kind": "plus_minus",
            "nominal": nominal,
            "lower": nominal - delta,
            "upper": nominal + delta,
            "text": raw,
        }

    match = re.search(r"([+-]?\d+(?:\.\d+)?)\(\+([+-]?\d+(?:\.\d+)?)/(-?\d+(?:\.\d+)?)\)", normalized)
    if match:
        nominal = float(match.group(1))
        upper_delta = float(match.group(2))
        lower_delta = float(match.group(3))
        return {
            "kind": "bilateral_parenthesized",
            "nominal": nominal,
            "lower": nominal + lower_delta,
            "upper": nominal + upper_delta,
            "text": raw,
        }

    match = re.search(r"([+-]?\d+(?:\.\d+)?)\+([+-]?\d+(?:\.\d+)?)/-([+-]?\d+(?:\.\d+)?)", normalized)
    if match:
        nominal = float(match.group(1))
        upper_delta = float(match.group(2))
        lower_delta = float(match.group(3))
        return {
            "kind": "bilateral_slash",
            "nominal": nominal,
            "lower": nominal - lower_delta,
            "upper": nominal + upper_delta,
            "text": raw,
        }

    match = re.search(r"([+-]?\d+(?:\.\d+)?)\(\+([+-]?\d+(?:\.\d+)?)/0\)", normalized)
    if match:
        nominal = float(match.group(1))
        upper_delta = float(match.group(2))
        return {
            "kind": "upper_only_parenthesized",
            "nominal": nominal,
            "lower": nominal,
            "upper": nominal + upper_delta,
            "text": raw,
        }

    match = re.search(r"([+-]?\d+(?:\.\d+)?)\+([+-]?\d+(?:\.\d+)?)", normalized)
    if match:
        nominal = float(match.group(1))
        upper_delta = float(match.group(2))
        return {
            "kind": "upper_only",
            "nominal": nominal,
            "lower": nominal,
            "upper": nominal + upper_delta,
            "text": raw,
        }

    match = re.search(r"([+-]?\d+(?:\.\d+)?)-([+-]?\d+(?:\.\d+)?)", normalized)
    if match and "±" not in normalized and "/-" not in normalized:
        nominal = float(match.group(1))
        lower_delta = float(match.group(2))
        if not normalized.startswith("-"):
            return {
                "kind": "lower_only",
                "nominal": nominal,
                "lower": nominal - lower_delta,
                "upper": nominal,
                "text": raw,
            }

    match = re.search(r"(>=|>)([+-]?\d+(?:\.\d+)?)", normalized)
    if match:
        return {
            "kind": "lower_bound",
            "nominal": None,
            "lower": float(match.group(2)),
            "upper": None,
            "text": raw,
        }

    match = re.search(r"(<=|<)([+-]?\d+(?:\.\d+)?)", normalized)
    if match:
        return {
            "kind": "upper_bound",
            "nominal": None,
            "lower": None,
            "upper": float(match.group(2)),
            "text": raw,
        }

    return None


def evaluate_value_against_tolerance(value: float, tolerance: Dict[str, Any]) -> Tuple[bool, Optional[float]]:
    lower = tolerance.get("lower")
    upper = tolerance.get("upper")
    if lower is not None and value < lower:
        return False, value - lower
    if upper is not None and value > upper:
        return False, upper - value
    margins = []
    if lower is not None:
        margins.append(value - lower)
    if upper is not None:
        margins.append(upper - value)
    if not margins:
        return True, None
    return True, min(margins)


def find_header_row_and_columns(ws, merged_map: Dict[Tuple[int, int], Tuple[int, int]], max_scan_rows: int = 40) -> Optional[Dict[str, Any]]:
    best = None
    scan_rows = min(max_scan_rows, ws.max_row)
    for row_idx in range(1, scan_rows + 1):
        row_map = {}
        score = 0
        for col_idx in range(1, ws.max_column + 1):
            text = normalize_header(get_cell_value(ws, row_idx, col_idx, merged_map))
            if not text:
                continue
            for key, keywords in HEADER_KEYWORDS.items():
                if any(keyword.upper() in text for keyword in keywords):
                    row_map.setdefault(key, col_idx)
        for required_key in ["seq", "item", "std", "judge"]:
            if required_key in row_map:
                score += 2
        for optional_key in ["method", "data"]:
            if optional_key in row_map:
                score += 1
        if score >= 6 and (best is None or score > best["score"]):
            best = {"header_row": row_idx, "columns": row_map, "score": score}
    return best


def build_column_profile(ws, merged_map, start_row: int, end_row: int, col_idx: int) -> Dict[str, int]:
    profile = {
        "col": col_idx,
        "non_empty": 0,
        "measurement_like": 0,
        "pass_like": 0,
        "numeric_like": 0,
    }
    for row_idx in range(start_row, end_row + 1):
        value = get_cell_value(ws, row_idx, col_idx, merged_map)
        if not clean_text(value):
            continue
        profile["non_empty"] += 1
        if is_measurement_value(value):
            profile["measurement_like"] += 1
        if is_pass_marker_value(value):
            profile["pass_like"] += 1
        if is_numeric_like(value):
            profile["numeric_like"] += 1
    return profile


def is_data_column_profile(profile: Dict[str, int]) -> bool:
    non_empty = profile["non_empty"]
    if non_empty == 0:
        return False
    measurement_ratio = profile["measurement_like"] / float(non_empty)
    pass_ratio = profile["pass_like"] / float(non_empty)
    return measurement_ratio >= 0.6 or (profile["measurement_like"] >= 2 and pass_ratio >= 0.4)


def select_active_data_block(active_cols: List[int], judge_col: int) -> Optional[Tuple[int, int]]:
    if not active_cols:
        return None
    sorted_cols = sorted(active_cols)
    blocks = []
    block_start = sorted_cols[0]
    block_end = sorted_cols[0]
    for col_idx in sorted_cols[1:]:
        if col_idx == block_end + 1:
            block_end = col_idx
            continue
        blocks.append((block_start, block_end))
        block_start = col_idx
        block_end = col_idx
    blocks.append((block_start, block_end))

    best_block = None
    best_score = None
    for start_col, end_col in blocks:
        distance_to_judge = abs((judge_col - 1) - end_col)
        width = end_col - start_col + 1
        score = (distance_to_judge, -width, -end_col)
        if best_score is None or score < best_score:
            best_score = score
            best_block = (start_col, end_col)
    return best_block


def detect_data_region(
    ws,
    merged_map,
    header_row: int,
    data_start_row: int,
    columns: Dict[str, int],
    max_sample_rows: int = 20,
) -> Tuple[int, int, int]:
    judge_col = columns.get("judge", ws.max_column)
    excluded_cols = set()
    for key in ["seq", "item", "std", "method", "judge"]:
        col_idx = columns.get(key)
        if col_idx:
            excluded_cols.add(col_idx)

    sample_start_row = max(data_start_row, header_row + 1)
    sample_end_row = min(ws.max_row, sample_start_row + max_sample_rows - 1)
    profiles = []
    for col_idx in range(1, judge_col):
        if col_idx in excluded_cols:
            continue
        profile = build_column_profile(ws, merged_map, sample_start_row, sample_end_row, col_idx)
        profiles.append(profile)

    active_cols = [profile["col"] for profile in profiles if is_data_column_profile(profile)]
    active_block = select_active_data_block(active_cols, judge_col)

    hinted_start = columns.get("data")
    if hinted_start and hinted_start < judge_col and hinted_start not in excluded_cols:
        hinted_end = judge_col - 1
        hinted_active = [profile["col"] for profile in profiles if profile["col"] >= hinted_start and is_data_column_profile(profile)]
        hinted_block = select_active_data_block(hinted_active, judge_col)
        if hinted_block:
            start_col = min(hinted_start, hinted_block[0])
            end_col = max(hinted_start, hinted_block[1])
            return start_col, max(end_col - start_col + 1, 1), judge_col
        return hinted_start, max(judge_col - hinted_start, 1), judge_col

    if active_block:
        start_col, end_col = active_block
        return start_col, max(end_col - start_col + 1, 1), judge_col

    fallback_start = max(
        columns.get("method", 0),
        columns.get("std", 0),
        columns.get("item", 0),
        columns.get("seq", 0),
    ) + 1
    fallback_start = max(1, min(fallback_start, max(judge_col - 1, 1)))
    fallback_end = max(fallback_start, judge_col - 1)
    return fallback_start, max(fallback_end - fallback_start + 1, 1), judge_col


def detect_data_start_row(ws, merged_map, header_row: int, seq_col: int, max_scan_rows: int = 10) -> int:
    start = header_row + 1
    scan_end = min(ws.max_row, header_row + max_scan_rows)
    for row_idx in range(header_row + 1, scan_end + 1):
        seq_value = clean_text(get_cell_value(ws, row_idx, seq_col, merged_map))
        if not seq_value:
            continue
        if seq_value.replace(" ", "").isdigit():
            return row_idx
    return start


def infer_layout(ws, merged_map, cli_overrides: Optional[Dict[str, Optional[int]]] = None) -> Dict[str, Any]:
    cli_overrides = cli_overrides or {}
    detected = find_header_row_and_columns(ws, merged_map) or {"header_row": 1, "columns": {}}
    columns = dict(detected.get("columns", {}))

    mapping = {
        "seq_col": cli_overrides.get("seq_col") or columns.get("seq") or 2,
        "item_col": cli_overrides.get("item_col") or columns.get("item") or 3,
        "std_col": cli_overrides.get("std_col") or columns.get("std") or 5,
        "method_col": cli_overrides.get("method_col") or columns.get("method") or 7,
        "judge_col": cli_overrides.get("judge_col") or columns.get("judge") or min(ws.max_column, 12),
        "header_row": cli_overrides.get("header_row") or detected.get("header_row") or 1,
    }
    provisional_data_start_row = cli_overrides.get("data_start_row") or detect_data_start_row(
        ws, merged_map, mapping["header_row"], mapping["seq_col"]
    )
    data_start, data_cols, judge_col = detect_data_region(
        ws,
        merged_map,
        mapping["header_row"],
        provisional_data_start_row,
        columns,
    )
    mapping["data_start"] = cli_overrides.get("data_start") or data_start
    mapping["data_cols"] = cli_overrides.get("data_cols") or data_cols
    mapping["judge_col"] = cli_overrides.get("judge_col") or judge_col
    mapping["data_start_row"] = provisional_data_start_row
    return mapping


def extract_rows_from_sheet(ws, sheet_name: str, cli_overrides: Optional[Dict[str, Optional[int]]] = None) -> Dict[str, Any]:
    merged_map = build_merged_map(ws)
    layout = infer_layout(ws, merged_map, cli_overrides=cli_overrides)
    rows = []
    for row_idx in range(layout["data_start_row"], ws.max_row + 1):
        seq_raw = get_cell_value(ws, row_idx, layout["seq_col"], merged_map)
        seq_text = clean_text(seq_raw)
        if not seq_text:
            continue
        if not seq_text.replace(" ", "").isdigit():
            continue

        item = clean_text(get_cell_value(ws, row_idx, layout["item_col"], merged_map))
        std = clean_text(get_cell_value(ws, row_idx, layout["std_col"], merged_map))
        method = clean_text(get_cell_value(ws, row_idx, layout["method_col"], merged_map))
        judge = clean_text(get_cell_value(ws, row_idx, layout["judge_col"], merged_map))
        values = []
        raw_values = []
        for col_idx in range(layout["data_start"], layout["data_start"] + layout["data_cols"]):
            cell_value = get_cell_value(ws, row_idx, col_idx, merged_map)
            raw_values.append(cell_value)
            values.append(cell_value)

        if not item and not std and not judge and not any(clean_text(v) for v in values):
            continue
        rows.append(
            {
                "sheet": sheet_name,
                "row_index": row_idx,
                "seq": int(seq_text.replace(" ", "")),
                "item": item,
                "std": std,
                "method": method,
                "values": values,
                "judge": judge,
                "raw_values": raw_values,
            }
        )
    return {"layout": layout, "rows": rows}


def summarize_precision(rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    by_method = {}
    method_counter = {}
    for row in rows:
        method = row.get("method") or "Not specified"
        decimals = [count_decimals(value) for value in row.get("values", [])]
        decimals = [value for value in decimals if value is not None]
        if not decimals:
            continue
        method_counter.setdefault(method, []).extend(decimals)

    for method, values in method_counter.items():
        counter = Counter(values)
        dominant = counter.most_common(1)[0][0]
        by_method[method] = {
            "dominant_decimals": dominant,
            "distribution": dict(counter),
        }
    return by_method
