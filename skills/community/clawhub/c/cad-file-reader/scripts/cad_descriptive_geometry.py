#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 cad_scan 详情 JSON 提炼成装饰识图中间数据和投影审计。"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / "packs" / "descriptive-geometry" / "rules.json"
from cad_contract import contractize_payload

from cad_common import compact, load_rules
def evidence_of(record: dict[str, Any]) -> dict[str, Any]:
    ev = {
        "text": compact(record.get("text", "")),
        "layer": record.get("layer"),
        "kind": record.get("kind"),
        "space": record.get("space"),
    }
    if record.get("x") is not None or record.get("y") is not None:
        ev["coord"] = [record.get("x"), record.get("y")]
    for key in ("file", "file_name", "sheet", "sheet_id", "handle"):
        if record.get(key) is not None:
            ev[key] = record.get(key)
    return {k: v for k, v in ev.items() if v not in (None, "")}

def data_file_name(data: dict[str, Any], value: Any) -> str:
    """把 cad_scan 的文件索引还原为文件名。"""
    if isinstance(value, dict):
        return parse_file_name(value.get("name") or value.get("path"))
    files = data.get("files") or []
    if isinstance(value, int) and 0 <= value < len(files):
        item = files[value]
        return data_file_name(data, item)
    return parse_file_name(value)

def read_records(data: dict[str, Any]) -> list[dict[str, Any]]:
    records = data.get("text_records") or data.get("texts") or []
    out: list[dict[str, Any]] = []
    for i, raw in enumerate(records):
        if not isinstance(raw, dict):
            continue
        text = compact(raw.get("text", ""))
        if not text:
            continue
        file_name = raw.get("file_name")
        if file_name is None:
            file_name = data_file_name(data, raw.get("file"))
        rec = {
            "text": text,
            "layer": raw.get("layer"),
            "kind": raw.get("kind") or raw.get("type"),
            "space": raw.get("space"),
            "x": raw.get("x"),
            "y": raw.get("y"),
            "sheet": raw.get("sheet"),
            "file": raw.get("file"),
            "file_name": file_name,
            "handle": raw.get("handle"),
            "_index": i,
        }
        out.append(rec)
    return out

def context_of(record: dict[str, Any]) -> tuple[str, Any, Any]:
    return (
        parse_file_name(record.get("file_name") or record.get("file")),
        record.get("sheet"),
        record.get("space"),
    )

def match_view(text: str, rules: dict[str, Any]) -> tuple[str, float]:
    for view_type, patterns in rules["view_types"].items():
        for pattern in patterns:
            if pattern in text:
                return view_type, float(rules["confidence"]["direct_label"])
    return "", 0.0

def match_room(text: str, rules: dict[str, Any]) -> str:
    for pattern in rules["room_patterns"]:
        if pattern in text:
            return pattern
    return ""

def opening_candidates(text: str, rules: dict[str, Any]) -> list[str]:
    heads = "|".join(re.escape(x) for x in rules["opening_patterns"])
    pat = re.compile(rf"(?<![A-Za-z0-9])({heads})[-_]?(\d{{1,4}})(?![0-9A-Za-z])", re.I)
    candidates = [m.group(0).upper() for m in pat.finditer(text)]
    exclusions = rules.get("opening_exclusion_patterns", [])
    if not exclusions:
        return candidates
    has_geometry_context = bool(
        re.search(rules["dimension_pattern"], text, re.I)
        or re.search(r"\d\s*(?:樘|个|扇|处)", text)
        or re.search(r"门窗(?:表|明细)", text)
    )
    out: list[str] = []
    for code in candidates:
        if not has_geometry_context and any(
            re.fullmatch(str(pattern), code, re.I) for pattern in exclusions
        ):
            continue
        out.append(code)
    return out

def practice_part(code: str, text: str, rules: dict[str, Any]) -> str:
    for part, prefixes in rules.get("practice_code_prefixes", {}).items():
        if any(code.lower().startswith(str(prefix).lower()) for prefix in prefixes):
            return part
    for part, words in rules["practice_parts"].items():
        if any(word in text for word in words):
            return part
    return "unknown"

def practice_candidates(text: str, rules: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for match in re.finditer(rules["practice_code_pattern"], text, re.I):
        code = compact(match.group(0), 80)
        part = practice_part(code, text, rules)
        out.append(
            {
                "code": code,
                "part": part,
                "status": "candidate",
                "confidence": float(rules["confidence"]["pattern_match"]),
                "review_reason": "" if part != "unknown" else "做法部位未在原文中明确",
            }
        )
    return out

def scale_candidates(text: str, rules: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    for match in re.finditer(rules["scale_pattern"], text):
        out.append(
            {
                "scale": f"1:{match.group(1)}",
                "status": "candidate",
                "confidence": float(rules["confidence"]["direct_label"]),
                "evidence": [],
            }
        )
    return out

def unit_candidates(text: str, rules: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    matched: set[str] = set()
    for unit, patterns in rules["unit_patterns"].items():
        if unit in matched:
            continue
        hit = next(
            (
                str(pattern)
                for pattern in patterns
                if re.search(str(pattern), text, re.I)
            ),
            "",
        )
        if not hit:
            continue
        matched.add(unit)
        out.append(
                {
                    "unit": unit,
                    "status": "candidate",
                    "confidence": float(rules["confidence"]["pattern_match"]),
                    "evidence": [],
                }
            )
    return out

def parse_file_name(value: Any) -> str:
    if value is None:
        return ""
    return str(value)

def median(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return float(ordered[mid])
    return (float(ordered[mid - 1]) + float(ordered[mid])) / 2.0

def row_groups(records: list[dict[str, Any]], sheet_meta: dict[Any, dict[str, Any]]) -> list[list[dict[str, Any]]]:
    by_context: dict[tuple[Any, Any], list[dict[str, Any]]] = defaultdict(list)
    for rec in records:
        if rec.get("x") is None or rec.get("y") is None:
            continue
        by_context[(parse_file_name(rec.get("file_name") or rec.get("file")), rec.get("sheet"))].append(rec)

    groups: list[list[dict[str, Any]]] = []
    for (_file, sheet), items in by_context.items():
        meta = sheet_meta.get(sheet) if isinstance(sheet_meta, dict) else None
        tolerance = 50.0
        if meta and isinstance(meta.get("bbox"), (list, tuple)) and len(meta["bbox"]) >= 4:
            height = abs(float(meta["bbox"][3]) - float(meta["bbox"][1]))
            if height > 0:
                tolerance = max(20.0, height * 0.004)
        ordered = sorted(items, key=lambda r: (-float(r["y"]), float(r["x"])))
        current: list[dict[str, Any]] = []
        center = 0.0
        for rec in ordered:
            y = float(rec["y"])
            if not current:
                current = [rec]
                center = y
                continue
            if abs(y - center) <= tolerance:
                current.append(rec)
                center = (center * (len(current) - 1) + y) / len(current)
                continue
            groups.append(current)
            current = [rec]
            center = y
        if current:
            groups.append(current)
    return groups

def build_room_schedules(
    records: list[dict[str, Any]],
    rules: dict[str, Any],
    sheet_meta: dict[Any, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    schedules: list[dict[str, Any]] = []
    unbound: list[dict[str, Any]] = []
    unbound_seen: set[tuple[str, str, tuple[str, ...]]] = set()
    seen: set[tuple[str, str, tuple[str, ...]]] = set()
    expected = ("floor", "wall", "ceiling", "skirting")

    def make_schedule(room: str, room_rec: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
        by_code: dict[str, dict[str, Any]] = {}
        for rec in rows:
            for candidate in practice_candidates(rec["text"], rules):
                old = by_code.get(candidate["code"])
                if old is None or candidate["confidence"] > old["confidence"]:
                    item = dict(candidate)
                    item["raw"] = rec["text"]
                    item["evidence"] = [evidence_of(rec)]
                    by_code[candidate["code"]] = item
        practices = list(by_code.values())
        parts = {p["part"] for p in practices}
        missing = [part for part in expected if part not in parts]
        evidence = [evidence_of(room_rec)]
        for item in practices:
            evidence.extend(item["evidence"])
        return {
            "room": room,
            "practices": practices,
            "missing_parts": missing,
            "confidence": float(rules["confidence"]["direct_label"]) if practices else float(rules["confidence"]["context_match"]),
            "status": "review" if missing else "candidate",
            "review_reason": ("缺做法：" + "、".join(missing)) if missing else "",
            "evidence": evidence[:120],
        }

    for rec in records:
        room = match_room(rec["text"], rules)
        if room and practice_candidates(rec["text"], rules):
            item = make_schedule(room, rec, [rec])
            key = (context_key(rec), room, tuple(sorted(p["code"] for p in item["practices"])))
            if key not in seen:
                schedules.append(item)
                seen.add(key)

    for group in row_groups(records, sheet_meta):
        room_recs = [(rec, match_room(rec["text"], rules)) for rec in group]
        room_recs = [(rec, room) for rec, room in room_recs if room]
        if not room_recs:
            continue
        distinct_rooms = sorted({room for _rec, room in room_recs})
        if len(distinct_rooms) != 1:
            continue
        item = make_schedule(distinct_rooms[0], room_recs[0][0], group)
        key = (context_key(room_recs[0][0]), distinct_rooms[0], tuple(sorted(p["code"] for p in item["practices"])))
        if not item["practices"]:
            if key not in unbound_seen:
                unbound.append(
                    {
                        "room": distinct_rooms[0],
                        "confidence": item["confidence"],
                        "status": "review",
                        "review_reason": "识别到房间词，但本行未绑定做法编号",
                        "evidence": item["evidence"][:1],
                    }
                )
                unbound_seen.add(key)
        elif key not in seen:
            schedules.append(item)
            seen.add(key)
    return schedules, unbound

def context_key(record: dict[str, Any]) -> str:
    file_name = parse_file_name(record.get("file_name") or record.get("file"))
    return f"{file_name}|{record.get('sheet', '')}|{record.get('space', '')}"

def summarize_openings(openings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in openings:
        grouped[item["code"]].append(item)

    summary: list[dict[str, Any]] = []
    for code in sorted(grouped):
        items = grouped[code]
        size_counts: Counter[tuple[str, ...]] = Counter(tuple(x.get("nominal_size") or []) for x in items)
        sizes = [list(x) for x in size_counts.keys() if x]
        explicit = sorted({int(x["explicit_count"]) for x in items if x.get("explicit_count") is not None})
        record_count = len(items)
        block_count = sum(1 for x in items if str(x.get("evidence", [{}])[0].get("kind", "")).upper() == "INSERT")
        review_reasons: list[str] = []
        if not sizes:
            review_reasons.append("缺宽高尺寸")
        if len(size_counts) > 1:
            review_reasons.append("同名门窗尺寸冲突")
        if explicit:
            if len(explicit) > 1:
                review_reasons.append("原文数量冲突")
                status = "conflict"
            elif not sizes:
                status = "review"
            else:
                status = "candidate"
        elif len(size_counts) > 1 or not sizes:
            status = "review"
        else:
            status = "candidate"
        common_size = size_counts.most_common(1)[0][0]
        evidence: list[dict[str, Any]] = []
        for item in items:
            evidence.extend(item.get("evidence", []))
        context_values = sorted({context_key(x) for x in items})
        summary.append(
            {
                "code": code,
                "nominal_size": list(common_size) if common_size else [],
                "nominal_size_candidates": sizes,
                "record_count": record_count,
                "block_instance_count": block_count,
                "explicit_count": explicit[0] if len(explicit) == 1 else None,
                "explicit_count_candidates": explicit,
                "count_basis": "原文数量字段" if explicit and len(explicit) == 1 else "记录条数；不能直接当樘数",
                "confidence": min(float(x.get("confidence", 0)) for x in items),
                "status": status,
                "review_reason": "；".join(review_reasons),
                "contexts": context_values[:30],
                "evidence": evidence[:120],
            }
        )
    return summary

def scale_unit_audit(records: list[dict[str, Any]], rules: dict[str, Any], sheet_meta: dict[Any, dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, Any], dict[str, Any]] = defaultdict(
        lambda: {"scales": [], "units": [], "spaces": [], "evidence": [], "record_count": 0}
    )
    for rec in records:
        key = (parse_file_name(rec.get("file_name") or rec.get("file")), rec.get("sheet"))
        bucket = grouped[key]
        bucket["record_count"] += 1
        for candidate in scale_candidates(rec["text"], rules):
            bucket["scales"].append(candidate["scale"])
            bucket["evidence"].append(evidence_of(rec))
        for candidate in unit_candidates(rec["text"], rules):
            bucket["units"].append(candidate["unit"])
            bucket["evidence"].append(evidence_of(rec))
        if rec.get("space"):
            bucket["spaces"].append(str(rec["space"]))

    audit: list[dict[str, Any]] = []
    for (file_name, sheet), raw in grouped.items():
        scales = sorted(set(raw["scales"]))
        units = sorted(set(raw["units"]))
        spaces = sorted(set(raw["spaces"]))
        reasons: list[str] = []
        if len(scales) > 1:
            reasons.append("比例冲突")
        if len(units) > 1:
            reasons.append("单位冲突")
        if len(spaces) > 1:
            reasons.append("空间归属冲突")
        if not scales:
            reasons.append("缺比例")
        if not units:
            reasons.append("缺单位")
        status = "conflict" if (len(scales) > 1 or len(units) > 1 or len(spaces) > 1) else ("review" if reasons else "candidate")
        item = {
            "file": file_name,
            "sheet": sheet,
            "scales": scales,
            "units": units,
            "spaces": spaces,
            "record_count": raw["record_count"],
            "confidence": float(rules["confidence"]["direct_label"]) if scales and units and not reasons else float(rules["confidence"]["context_match"]),
            "status": status,
            "review_reason": "；".join(reasons),
            "evidence": raw["evidence"][:80],
        }
        if sheet in sheet_meta and isinstance(sheet_meta[sheet].get("bbox"), (list, tuple)):
            item["sheet_bbox"] = sheet_meta[sheet]["bbox"]
        audit.append(item)
    return sorted(audit, key=lambda x: (x["file"], str(x["sheet"])))

def flatten_geometry(data: dict[str, Any]) -> list[tuple[int, str, list[float]]]:
    segments_raw = data.get("geometry_segments") or []
    layers_raw = data.get("geometry_layers") or []
    files = data.get("files") or []

    def file_name(index: int) -> str:
        if index < len(files):
            value = files[index]
            if isinstance(value, dict):
                return parse_file_name(value.get("name") or value.get("path"))
            return parse_file_name(value)
        return f"file_{index}"

    # cad_scan normally writes one segment list per file.  Also tolerate a flat single-file list.
    if (
        segments_raw
        and len(segments_raw[0]) == 4
        and all(isinstance(v, (int, float)) for v in segments_raw[0])
    ):
        segments_raw = [segments_raw]
        if layers_raw and layers_raw and not isinstance(layers_raw[0], list):
            layers_raw = [layers_raw]

    out: list[tuple[int, str, list[float]]] = []
    for file_index, file_segments in enumerate(segments_raw):
        if not isinstance(file_segments, list):
            continue
        layer_list = layers_raw[file_index] if file_index < len(layers_raw) and isinstance(layers_raw[file_index], list) else []
        for segment_index, segment in enumerate(file_segments):
            if not isinstance(segment, (list, tuple)) or len(segment) < 4:
                continue
            try:
                values = [float(v) for v in segment[:4]]
            except (TypeError, ValueError):
                continue
            layer = parse_file_name(layer_list[segment_index]) if segment_index < len(layer_list) else ""
            out.append((file_index, layer, values))
    return out

def geometry_index(data: dict[str, Any], rules: dict[str, Any]) -> list[dict[str, Any]]:
    patterns = rules.get("geometry_layer_patterns", {})
    if not patterns:
        return []
    files = data.get("files") or []

    def file_name(index: int) -> str:
        if index < len(files):
            value = files[index]
            if isinstance(value, dict):
                return parse_file_name(value.get("name") or value.get("path"))
            return parse_file_name(value)
        return f"file_{index}"

    grouped: dict[tuple[int, str, str], dict[str, Any]] = defaultdict(
        lambda: {"segment_count": 0, "length": 0.0, "bbox": None, "evidence": []}
    )
    for file_index, layer, segment in flatten_geometry(data):
        for geometry_type, words in patterns.items():
            if not any(str(word).lower() in layer.lower() for word in words):
                continue
            x1, y1, x2, y2 = segment
            length = math.hypot(x2 - x1, y2 - y1)
            key = (file_index, layer, geometry_type)
            bucket = grouped[key]
            bucket["segment_count"] += 1
            bucket["length"] += length
            if bucket["bbox"] is None:
                bucket["bbox"] = [min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)]
            else:
                bbox = bucket["bbox"]
                bbox[0] = min(bbox[0], min(x1, x2))
                bbox[1] = min(bbox[1], min(y1, y2))
                bbox[2] = max(bbox[2], max(x1, x2))
                bbox[3] = max(bbox[3], max(y1, y2))
            if len(bucket["evidence"]) < 20:
                bucket["evidence"].append(
                    {
                        "file": file_name(file_index),
                        "layer": layer,
                        "segment": segment,
                        "length_drawing_units": round(length, 3),
                    }
                )
            break

    out: list[dict[str, Any]] = []
    for (file_index, layer, geometry_type), bucket in grouped.items():
        out.append(
            {
                "type": geometry_type,
                "file": file_name(file_index),
                "layer": layer,
                "segment_count": bucket["segment_count"],
                "total_length_drawing_units": round(bucket["length"], 3),
                "bbox": bucket["bbox"],
                "confidence": float(rules["confidence"]["context_match"]),
                "status": "candidate",
                "review_reason": "仅按图层索引线段；未完成闭合与投影校验",
                "evidence": bucket["evidence"],
            }
        )
    return sorted(out, key=lambda x: (x["file"], x["type"], x["layer"]))

def geometry_layer_type(layer: str, rules: dict[str, Any]) -> str:
    for kind, words in rules.get("geometry_layer_patterns", {}).items():
        if any(str(word).lower() in str(layer).lower() for word in words):
            return kind
    return ""

def sheet_for_point(sheet_meta: dict[Any, dict[str, Any]], x: float, y: float) -> Any:
    for sheet_id, meta in sheet_meta.items():
        bbox = meta.get("bbox")
        if not isinstance(bbox, (list, tuple)) or len(bbox) < 4:
            continue
        try:
            if float(bbox[0]) <= x <= float(bbox[2]) and float(bbox[1]) <= y <= float(bbox[3]):
                return sheet_id
        except (TypeError, ValueError):
            continue
    return None

def point_segment_distance(px: float, py: float, segment: list[float]) -> float:
    x1, y1, x2, y2 = segment
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(px - x1, py - y1)
    t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))
    return math.hypot(px - (x1 + t * dx), py - (y1 + t * dy))

def point_rectangle_distance(x: float, y: float, bbox: list[float]) -> float:
    x1, y1, x2, y2 = bbox
    if x1 <= x <= x2 and y1 <= y <= y2:
        return min(x - x1, x2 - x, y - y1, y2 - y)
    dx = max(x1 - x, 0.0, x - x2)
    dy = max(y1 - y, 0.0, y - y2)
    return math.hypot(dx, dy)

def intervals_cover(intervals: list[tuple[float, float]], start: float, end: float, eps: float) -> bool:
    current = start
    for a, b in sorted(intervals):
        if b < current - eps:
            continue
        if a > current + eps:
            return False
        current = max(current, b)
        if current >= end - eps:
            return True
    return current >= end - eps

def axis_aligned_rectangles(
    segments: list[tuple[str, list[float]]],
    eps: float,
    max_side_values: int = 24,
) -> tuple[list[dict[str, Any]], bool]:
    horizontal: dict[float, list[tuple[float, float, str, list[float]]]] = defaultdict(list)
    vertical: dict[float, list[tuple[float, float, str, list[float]]]] = defaultdict(list)
    non_axis = 0
    for layer, segment in segments:
        x1, y1, x2, y2 = segment
        if abs(y1 - y2) <= eps and abs(x2 - x1) > eps:
            horizontal[round((y1 + y2) / 2, 6)].append(
                (min(x1, x2), max(x1, x2), layer, segment)
            )
        elif abs(x1 - x2) <= eps and abs(y2 - y1) > eps:
            vertical[round((x1 + x2) / 2, 6)].append(
                (min(y1, y2), max(y1, y2), layer, segment)
            )
        else:
            non_axis += 1

    xs = sorted({round(key, 6) for key in vertical})
    ys = sorted({round(key, 6) for key in horizontal})
    clipped = len(xs) > max_side_values or len(ys) > max_side_values
    xs = xs[:max_side_values]
    ys = ys[:max_side_values]
    rects: list[dict[str, Any]] = []
    seen: set[tuple[float, float, float, float]] = set()
    for x1 in xs:
        for x2 in xs:
            if x2 <= x1 + eps:
                continue
            for y1 in ys:
                for y2 in ys:
                    if y2 <= y1 + eps or (x1, y1, x2, y2) in seen:
                        continue
                    bottom = [(a, b) for a, b, _layer, _seg in horizontal.get(y1, []) if b >= x1 - eps and a <= x2 + eps]
                    top = [(a, b) for a, b, _layer, _seg in horizontal.get(y2, []) if b >= x1 - eps and a <= x2 + eps]
                    left = [(a, b) for a, b, _layer, _seg in vertical.get(x1, []) if b >= y1 - eps and a <= y2 + eps]
                    right = [(a, b) for a, b, _layer, _seg in vertical.get(x2, []) if b >= y1 - eps and a <= y2 + eps]
                    if not (
                        intervals_cover(bottom, x1, x2, eps)
                        and intervals_cover(top, x1, x2, eps)
                        and intervals_cover(left, y1, y2, eps)
                        and intervals_cover(right, y1, y2, eps)
                    ):
                        continue
                    seen.add((x1, y1, x2, y2))
                    used_segments: list[dict[str, Any]] = []
                    for _a, _b, layer, segment in horizontal.get(y1, []) + horizontal.get(y2, []):
                        a, _b2, c, _d = segment
                        if min(a, c) <= x2 + eps and max(a, c) >= x1 - eps:
                            used_segments.append({"layer": layer, "segment": segment})
                    for _a, _b, layer, segment in vertical.get(x1, []) + vertical.get(x2, []):
                        a, b, _c, _d = segment
                        if min(a, b) <= y2 + eps and max(a, b) >= y1 - eps:
                            used_segments.append({"layer": layer, "segment": segment})
                    rects.append(
                        {
                            "polygon": [[x1, y1], [x2, y1], [x2, y2], [x1, y2]],
                            "bbox": [x1, y1, x2, y2],
                            "segments": used_segments[:20],
                            "non_axis_segments": non_axis,
                        }
                    )
    return rects, clipped

def room_boundaries(
    records: list[dict[str, Any]],
    data: dict[str, Any],
    rules: dict[str, Any],
    sheet_meta: dict[Any, dict[str, Any]],
) -> list[dict[str, Any]]:
    files = data.get("files") or []
    grouped: dict[tuple[int, Any], list[tuple[str, list[float]]]] = defaultdict(list)
    for file_index, layer, segment in flatten_geometry(data):
        if geometry_layer_type(layer, rules) not in {"wall", "room"}:
            continue
        x1, y1, x2, y2 = segment
        sheet = sheet_for_point(sheet_meta, (x1 + x2) / 2.0, (y1 + y2) / 2.0)
        grouped[(file_index, sheet)].append((layer, segment))

    room_records = [rec for rec in records if rec.get("x") is not None and rec.get("y") is not None and match_room(rec["text"], rules)]
    out: list[dict[str, Any]] = []
    for (file_index, sheet), segments in sorted(grouped.items(), key=lambda item: (str(item[0][0]), str(item[0][1]))):
        bboxes = [b for _layer, seg in segments for b in [seg]]
        xs = [v for seg in bboxes for v in (seg[0], seg[2])]
        ys = [v for seg in bboxes for v in (seg[1], seg[3])]
        if not xs or not ys:
            continue
        width = max(xs) - min(xs)
        height = max(ys) - min(ys)
        eps = max(0.01, math.hypot(width, height) * 0.001)
        candidates, clipped = axis_aligned_rectangles(segments, eps)
        if isinstance(file_index, int) and 0 <= file_index < len(files):
            raw_file = files[file_index]
            file_name = data_file_name(data, raw_file)
        else:
            file_name = parse_file_name(file_index)
        for number, candidate in enumerate(candidates, 1):
            bbox = candidate["bbox"]
            names = []
            for rec in room_records:
                if rec.get("sheet") is not None and sheet is not None and rec.get("sheet") != sheet:
                    continue
                x, y = float(rec["x"]), float(rec["y"])
                if bbox[0] <= x <= bbox[2] and bbox[1] <= y <= bbox[3]:
                    names.append(match_room(rec["text"], rules))
            names = sorted(set(names))
            out.append(
                {
                    "id": f"room-boundary-{len(out) + 1}",
                    "file": file_name,
                    "sheet": sheet,
                    "boundary_kind": "axis-aligned-closed-rectangle",
                    "polygon": candidate["polygon"],
                    "bbox": bbox,
                    "rooms": names,
                    "segments": candidate["segments"],
                    "confidence": float(rules["confidence"]["direct_label"]) if names else float(rules["confidence"]["context_match"]),
                    "status": "candidate" if names else "review",
                    "review_reason": "" if names else "闭合边界未绑定房间名称",
                }
            )
            if clipped:
                out[-1]["review_reason"] = (out[-1]["review_reason"] + "；坐标轴数量超限，仅检查前部分候选").strip("；")
                out[-1]["status"] = "review"
    return out

def node_detail_candidates(text: str, rules: dict[str, Any]) -> list[str]:
    out: list[str] = []
    for pattern in rules.get("node_detail_patterns", []):
        for match in re.finditer(str(pattern), text, re.I):
            value = compact(match.group(1), 40)
            if value and value not in out:
                out.append(value)
    return out

def node_detail_index(
    records: list[dict[str, Any]],
    rules: dict[str, Any],
    sheet_meta: dict[Any, dict[str, Any]],
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for rec in records:
        nodes = node_detail_candidates(rec["text"], rules)
        if not nodes:
            continue
        practices = sorted({item["code"] for item in practice_candidates(rec["text"], rules)})
        missing = []
        if not practices:
            missing.append("做法编号")
        if rec.get("x") is None or rec.get("y") is None:
            missing.append("坐标")
        evidence = evidence_of(rec)
        item = {
            "practice_codes": practices,
            "node_codes": nodes,
            "file": evidence.get("file_name") or evidence.get("file", ""),
            "sheet": rec.get("sheet"),
            "coord": [rec.get("x"), rec.get("y")] if rec.get("x") is not None or rec.get("y") is not None else None,
            "sheet_bbox": sheet_meta.get(rec.get("sheet"), {}).get("bbox") if rec.get("sheet") in sheet_meta else None,
            "evidence": [evidence],
            "confidence": float(rules["confidence"]["direct_label"]) if practices else float(rules["confidence"]["pattern_match"]),
            "status": "candidate" if not missing else "review",
            "review_reason": "缺" + "、".join(missing) if missing else "",
        }
        out.append(item)
    return out

def attribute_openings(
    openings: list[dict[str, Any]],
    records: list[dict[str, Any]],
    data: dict[str, Any],
    rules: dict[str, Any],
    sheet_meta: dict[Any, dict[str, Any]],
) -> None:
    boundaries = room_boundaries(records, data, rules, sheet_meta)
    files = data.get("files") or []
    wall_segments: list[tuple[int, Any, str, list[float], str]] = []
    for file_index, layer, segment in flatten_geometry(data):
        if geometry_layer_type(layer, rules) not in {"wall", "room"}:
            continue
        x1, y1, x2, y2 = segment
        wall_segments.append((file_index, sheet_for_point(sheet_meta, (x1 + x2) / 2.0, (y1 + y2) / 2.0), layer, segment, data_file_name(data, files[file_index]) if isinstance(file_index, int) and file_index < len(files) else parse_file_name(file_index)))

    for opening in openings:
        evidence = opening.get("evidence", [{}])[0] if opening.get("evidence") else {}
        coord = evidence.get("coord")
        geometry: dict[str, Any] = {
            "wall_layer": None,
            "wall_segment": None,
            "wall_distance_drawing_units": None,
            "room_boundary_id": None,
            "room_candidates": [],
            "status": "review",
            "review_reason": "文字无坐标，不能绑定墙线和房间",
        }
        if not coord or len(coord) < 2 or coord[0] is None or coord[1] is None:
            opening["geometry"] = geometry
            continue
        x, y = float(coord[0]), float(coord[1])
        evidence_file = evidence.get("file_name") or evidence.get("file")
        evidence_sheet = evidence.get("sheet")
        nearby = []
        for file_index, sheet, layer, segment, file_name in wall_segments:
            if evidence_file is not None:
                if isinstance(evidence_file, int) and isinstance(file_index, int) and evidence_file != file_index:
                    continue
                if not isinstance(evidence_file, int) and str(evidence_file) != str(file_name):
                    continue
            if evidence_sheet is not None and sheet is not None and evidence_sheet != sheet:
                continue
            nearby.append((point_segment_distance(x, y, segment), layer, segment, sheet, file_name))
        nearby.sort(key=lambda item: item[0])
        sheet_bbox = sheet_meta.get(evidence_sheet, {}).get("bbox") if evidence_sheet in sheet_meta else None
        if sheet_bbox and isinstance(sheet_bbox, (list, tuple)) and len(sheet_bbox) >= 4:
            diag = math.hypot(float(sheet_bbox[2]) - float(sheet_bbox[0]), float(sheet_bbox[3]) - float(sheet_bbox[1]))
            tolerance = max(1.0, diag * 0.02)
        else:
            tolerance = 1.0
        if nearby and nearby[0][0] <= tolerance:
            distance, layer, segment, sheet, _file_name = nearby[0]
            geometry.update(
                {
                    "wall_layer": layer,
                    "wall_segment": segment,
                    "wall_distance_drawing_units": round(distance, 3),
                }
            )
        else:
            geometry["review_reason"] = "附近未找到墙/房间边界线段"
        candidates = []
        for boundary in boundaries:
            if evidence_file is not None and str(boundary.get("file", "")) != str(evidence_file):
                continue
            if evidence_sheet is not None and boundary.get("sheet") is not None and evidence_sheet != boundary.get("sheet"):
                continue
            distance = point_rectangle_distance(x, y, boundary["bbox"])
            if distance <= tolerance:
                candidates.append((distance, boundary))
        candidates.sort(key=lambda item: (item[0], str(item[1]["id"])))
        room_names = []
        for _distance, boundary in candidates:
            room_names.extend(boundary.get("rooms", []))
        room_names = sorted(set(room_names))
        geometry["room_candidates"] = room_names
        if candidates:
            geometry["room_boundary_id"] = candidates[0][1]["id"]
        if not candidates and geometry["review_reason"] == "附近未找到墙/房间边界线段":
            geometry["review_reason"] = "附近未找到墙/房间边界线段和闭合房间"
        elif not room_names:
            geometry["review_reason"] = (geometry["review_reason"] + "；未绑定房间名称").strip("；")
        elif len(room_names) > 1:
            geometry["review_reason"] = (geometry["review_reason"] + "；可能跨房间，需确认").strip("；")
        else:
            geometry["review_reason"] = ""
            geometry["status"] = "candidate"
        opening["geometry"] = geometry

def height_candidates_for_boundary(
    boundary: dict[str, Any],
    records: list[dict[str, Any]],
    rules: dict[str, Any],
) -> list[dict[str, Any]]:
    """按坐标把显式墙高/层高文字绑定到闭合房间边界。"""
    pattern = rules.get("height_pattern")
    if not pattern:
        return []
    bbox = boundary.get("bbox")
    if not isinstance(bbox, (list, tuple)) or len(bbox) < 4:
        return []
    try:
        x1, y1, x2, y2 = (float(v) for v in bbox[:4])
    except (TypeError, ValueError):
        return []
    if x2 <= x1 or y2 <= y1:
        return []
    tolerance = max(0.01, min(x2 - x1, y2 - y1) * 0.005)
    boundary_file = parse_file_name(boundary.get("file", ""))
    boundary_sheet = boundary.get("sheet")
    out: list[dict[str, Any]] = []
    seen: set[tuple[float, str]] = set()
    for rec in records:
        if rec.get("x") is None or rec.get("y") is None:
            continue
        if boundary_file and str(rec.get("file_name") or rec.get("file") or "") != boundary_file:
            continue
        if boundary_sheet is not None and rec.get("sheet") is not None and rec.get("sheet") != boundary_sheet:
            continue
        try:
            x, y = float(rec["x"]), float(rec["y"])
        except (TypeError, ValueError):
            continue
        if not (x1 - tolerance <= x <= x2 + tolerance and y1 - tolerance <= y <= y2 + tolerance):
            continue
        for match in re.finditer(pattern, rec.get("text", ""), re.I):
            try:
                value = float(match.group(1))
            except (TypeError, ValueError):
                continue
            raw_unit = match.group(2).lower()
            unit = "m" if raw_unit in {"m", "米"} else "mm"
            value_m = value / 1000.0 if unit == "mm" else value
            key = (round(value_m, 6), unit)
            if key in seen:
                continue
            seen.add(key)
            out.append(
                {
                    "value": value,
                    "unit": "mm" if unit == "mm" else "m",
                    "value_m": round(value_m, 6),
                    "evidence": [evidence_of(rec)],
                    "status": "candidate",
                    "review_reason": "",
                }
            )
    return out

def subtract_and_classify_intervals(
    start: float,
    end: float,
    opening_cuts: list[tuple[float, float]],
    tolerance: float,
) -> list[tuple[float, float, str]]:
    """把墙线切成 clear/opening 子段；重叠洞口合并为一个待确认洞区。"""
    if end <= start + tolerance:
        return []
    points = [start, end]
    for a, b in opening_cuts:
        points.extend([max(start, a), min(end, b)])
    ordered = sorted({round(v, 6) for v in points if start - tolerance <= v <= end + tolerance})
    out: list[tuple[float, float, str]] = []
    for left, right in zip(ordered, ordered[1:]):
        if right <= left + tolerance:
            continue
        middle = (left + right) / 2.0
        kind = "clear"
        for a, b in opening_cuts:
            if middle >= a - tolerance and middle <= b + tolerance:
                kind = "opening"
                break
        out.append((left, right, kind))
    return out

def wall_segments(
    boundaries: list[dict[str, Any]],
    openings: list[dict[str, Any]],
    records: list[dict[str, Any]],
    data: dict[str, Any],
    rules: dict[str, Any],
    sheet_meta: dict[Any, dict[str, Any]],
) -> list[dict[str, Any]]:
    """把轴对齐房间边界拆成 clear/opening 证据段；只做中间数据，不算面积。"""
    files = data.get("files") or []
    opening_geometry: list[dict[str, Any]] = []
    for file_index, layer, segment in flatten_geometry(data):
        if geometry_layer_type(layer, rules) not in {"door", "window"}:
            continue
        x1, y1, x2, y2 = segment
        if isinstance(file_index, int) and 0 <= file_index < len(files):
            file_name = data_file_name(data, files[file_index])
        elif isinstance(file_index, int) and len(files) == 1:
            # 一个 DWG 的图层线段可能按图层拆成多组；此组越界时回挂到唯一文件。
            file_name = data_file_name(data, files[0])
        else:
            file_name = parse_file_name(file_index)
        opening_geometry.append(
            {
                "layer": layer,
                "kind": geometry_layer_type(layer, rules),
                "segment": segment,
                "file": file_name,
                "sheet": sheet_for_point(sheet_meta, (x1 + x2) / 2.0, (y1 + y2) / 2.0),
            }
        )

    out: list[dict[str, Any]] = []
    for boundary in boundaries:
        polygon = boundary.get("polygon")
        bbox = boundary.get("bbox")
        if not isinstance(polygon, list) or len(polygon) < 3 or not isinstance(bbox, (list, tuple)) or len(bbox) < 4:
            out.append(
                {
                    "id": f"wall-segment-{len(out) + 1}",
                    "boundary_id": boundary.get("id", ""),
                    "file": boundary.get("file", ""),
                    "sheet": boundary.get("sheet"),
                    "rooms": boundary.get("rooms", []),
                    "edge_index": None,
                    "direction": "non_axis",
                    "segment_kind": "non_axis",
                    "segment": [],
                    "length_drawing_units": 0.0,
                    "height_candidates": [],
                    "height_status": "review",
                    "opening_codes": [],
                    "opening_layers": [],
                    "opening_segments": [],
                    "confidence": float(rules["confidence"]["pattern_match"]),
                    "status": "review",
                    "review_reason": "房间边界不是可用的轴对齐多边形",
                }
            )
            continue

        height_candidates = height_candidates_for_boundary(boundary, records, rules)
        height_values = sorted({float(row["value_m"]) for row in height_candidates})
        if len(height_values) == 1:
            height_status = "candidate"
            height_reason = ""
        elif not height_values:
            height_status = "review"
            height_reason = "缺显式墙高/层高证据"
        else:
            height_status = "review"
            height_reason = "墙高/层高证据冲突"
        boundary_status = boundary.get("status", "review")
        try:
            bx1, by1, bx2, by2 = (float(v) for v in bbox[:4])
        except (TypeError, ValueError):
            bx1 = by1 = bx2 = by2 = 0.0
        tolerance = max(0.01, min(bx2 - bx1, by2 - by1) * 0.005)

        for edge_index, point in enumerate(polygon):
            next_point = polygon[(edge_index + 1) % len(polygon)]
            try:
                ax, ay = float(point[0]), float(point[1])
                bx, by = float(next_point[0]), float(next_point[1])
            except (TypeError, ValueError, IndexError):
                out.append(
                    {
                        "id": f"wall-segment-{len(out) + 1}",
                        "boundary_id": boundary.get("id", ""),
                        "file": boundary.get("file", ""),
                        "sheet": boundary.get("sheet"),
                        "rooms": boundary.get("rooms", []),
                        "edge_index": edge_index,
                        "direction": "non_axis",
                        "segment_kind": "non_axis",
                        "segment": [],
                        "length_drawing_units": 0.0,
                        "height_candidates": height_candidates,
                        "height_status": height_status,
                        "opening_codes": [],
                        "opening_layers": [],
                        "opening_segments": [],
                        "confidence": float(rules["confidence"]["pattern_match"]),
                        "status": "review",
                        "review_reason": "边界顶点坐标无效",
                    }
                )
                continue
            horizontal = abs(ay - by) <= tolerance
            vertical = abs(ax - bx) <= tolerance
            if horizontal:
                segment = [min(ax, bx), ay, max(ax, bx), ay]
                axis_value = ay
                interval = (segment[0], segment[2])
                direction = "horizontal"
            elif vertical:
                segment = [ax, min(ay, by), ax, max(ay, by)]
                axis_value = ax
                interval = (segment[1], segment[3])
                direction = "vertical"
            else:
                out.append(
                    {
                        "id": f"wall-segment-{len(out) + 1}",
                        "boundary_id": boundary.get("id", ""),
                        "file": boundary.get("file", ""),
                        "sheet": boundary.get("sheet"),
                        "rooms": boundary.get("rooms", []),
                        "edge_index": edge_index,
                        "direction": "non_axis",
                        "segment_kind": "non_axis",
                        "segment": [ax, ay, bx, by],
                        "length_drawing_units": round(math.hypot(bx - ax, by - ay), 3),
                        "height_candidates": height_candidates,
                        "height_status": height_status,
                        "opening_codes": [],
                        "opening_layers": [],
                        "opening_segments": [],
                        "confidence": float(rules["confidence"]["pattern_match"]),
                        "status": "review",
                        "review_reason": "非轴对齐墙段需人工确认",
                    }
                )
                continue
            if segment[2] - segment[0] <= tolerance and segment[3] - segment[1] <= tolerance:
                out.append(
                    {
                        "id": f"wall-segment-{len(out) + 1}",
                        "boundary_id": boundary.get("id", ""),
                        "file": boundary.get("file", ""),
                        "sheet": boundary.get("sheet"),
                        "rooms": boundary.get("rooms", []),
                        "edge_index": edge_index,
                        "direction": direction,
                        "segment_kind": "zero_length",
                        "segment": segment,
                        "length_drawing_units": 0.0,
                        "height_candidates": height_candidates,
                        "height_status": height_status,
                        "opening_codes": [],
                        "opening_layers": [],
                        "opening_segments": [],
                        "confidence": float(rules["confidence"]["pattern_match"]),
                        "status": "review",
                        "review_reason": "零长度墙段需人工确认",
                    }
                )
                continue

            cuts: list[tuple[float, float]] = []
            matched_layers: list[str] = []
            matched_segments: list[list[float]] = []
            for og in opening_geometry:
                if boundary.get("file") and str(og.get("file", "")) != str(boundary.get("file")):
                    continue
                if boundary.get("sheet") is not None and og.get("sheet") is not None and og.get("sheet") != boundary.get("sheet"):
                    continue
                if horizontal and abs(og["segment"][1] - axis_value) > tolerance and abs(og["segment"][3] - axis_value) > tolerance:
                    continue
                if vertical and abs(og["segment"][0] - axis_value) > tolerance and abs(og["segment"][2] - axis_value) > tolerance:
                    continue
                if horizontal:
                    lo, hi = min(og["segment"][0], og["segment"][2]), max(og["segment"][0], og["segment"][2])
                else:
                    lo, hi = min(og["segment"][1], og["segment"][3]), max(og["segment"][1], og["segment"][3])
                if hi <= interval[0] - tolerance or lo >= interval[1] + tolerance:
                    continue
                cuts.append((lo, hi))
                matched_layers.append(og["layer"])
                matched_segments.append(og["segment"])

            opening_hits: list[dict[str, Any]] = []
            for opening in openings:
                evidence = opening.get("evidence", [{}])[0] if opening.get("evidence") else {}
                coord = evidence.get("coord")
                if not isinstance(coord, (list, tuple)) or len(coord) < 2:
                    continue
                try:
                    ex, ey = float(coord[0]), float(coord[1])
                except (TypeError, ValueError):
                    continue
                if boundary.get("file") and str(evidence.get("file_name") or evidence.get("file") or "") != str(boundary.get("file")):
                    continue
                if boundary.get("sheet") is not None and evidence.get("sheet") is not None and evidence.get("sheet") != boundary.get("sheet"):
                    continue
                if horizontal:
                    if abs(ey - axis_value) > tolerance or not interval[0] - tolerance <= ex <= interval[1] + tolerance:
                        continue
                elif vertical:
                    if abs(ex - axis_value) > tolerance or not interval[0] - tolerance <= ey <= interval[1] + tolerance:
                        continue
                if opening.get("code"):
                    opening_hits.append({"code": opening["code"], "coord": [ex, ey]})

            pieces = subtract_and_classify_intervals(interval[0], interval[1], cuts, tolerance)
            if not pieces:
                pieces = [(interval[0], interval[1], "review")]
            for a, b, kind in pieces:
                if horizontal:
                    piece_segment = [a, segment[1], b, segment[3]]
                    length = b - a
                else:
                    piece_segment = [segment[0], a, segment[2], b]
                    length = b - a
                codes = [
                    hit["code"] for hit in opening_hits
                    if a - tolerance <= hit["coord"][0 if horizontal else 1] <= b + tolerance
                ]
                reasons = []
                if boundary.get("review_reason"):
                    reasons.append(boundary["review_reason"])
                if height_reason:
                    reasons.append(height_reason)
                if kind == "opening" and not matched_layers:
                    reasons.append("洞口子段未匹配门窗图层")
                status = "candidate" if boundary_status == "candidate" and height_status == "candidate" and not reasons else "review"
                out.append(
                    {
                        "id": f"wall-segment-{len(out) + 1}",
                        "boundary_id": boundary.get("id", ""),
                        "file": boundary.get("file", ""),
                        "sheet": boundary.get("sheet"),
                        "rooms": boundary.get("rooms", []),
                        "edge_index": edge_index,
                        "direction": direction,
                        "segment_kind": kind,
                        "segment": piece_segment,
                        "length_drawing_units": round(length, 3),
                        "height_candidates": height_candidates,
                        "height_status": height_status,
                        "opening_codes": codes,
                        "opening_layers": sorted(set(matched_layers)),
                        "opening_segments": matched_segments,
                        "confidence": float(rules["confidence"]["direct_label" if status == "candidate" else "pattern_match"]),
                        "status": status,
                        "review_reason": "；".join(dict.fromkeys(reasons)),
                    }
                )
    return out

def ceiling_feature_tags(text: str, rules: dict[str, Any]) -> list[str]:
    text = str(text or "")
    tags: list[str] = []
    checks = (
        ("access", rules.get("ceiling_access_patterns", [])),
        ("lighting", rules.get("ceiling_lighting_patterns", [])),
        ("shape", rules.get("ceiling_shape_patterns", [])),
        ("drop", rules.get("ceiling_influence_patterns", [])),
    )
    for tag, patterns in checks:
        if any(str(pattern).lower() in text.lower() for pattern in patterns):
            tags.append(tag)
    return tags

def ceiling_elevation_candidates(text: str, rules: dict[str, Any]) -> list[tuple[float, str]]:
    pattern = rules.get("ceiling_elevation_pattern")
    if not pattern:
        return []
    out: list[tuple[float, str]] = []
    for match in re.finditer(pattern, str(text or ""), re.I):
        try:
            value = float(match.group(1))
        except (TypeError, ValueError):
            continue
        unit = "m" if match.group(2).lower() in {"m", "米"} else "mm"
        value_m = value / 1000.0 if unit == "mm" else value
        out.append((round(value_m, 6), unit))
    return out

def ceiling_zones(
    records: list[dict[str, Any]],
    data: dict[str, Any],
    rules: dict[str, Any],
    sheet_meta: dict[Any, dict[str, Any]],
) -> list[dict[str, Any]]:
    """提取吊顶主边界、检修口、灯具带、造型和梁/降板影响候选；只做中间数据。"""
    files = data.get("files") or []
    grouped: dict[tuple[int, Any], list[tuple[str, list[float], str]]] = defaultdict(list)
    for file_index, layer, segment in flatten_geometry(data):
        kind = geometry_layer_type(layer, rules)
        if kind not in {"ceiling", "ceiling_access", "ceiling_lighting", "ceiling_shape"}:
            continue
        x1, y1, x2, y2 = segment
        grouped[(file_index, sheet_for_point(sheet_meta, (x1 + x2) / 2.0, (y1 + y2) / 2.0))].append(
            (layer, segment, kind)
        )

    influence_geometry: list[dict[str, Any]] = []
    for file_index, layer, segment in flatten_geometry(data):
        kind = geometry_layer_type(layer, rules)
        if kind not in {"beam", "drop"}:
            continue
        if isinstance(file_index, int) and 0 <= file_index < len(files):
            file_name = data_file_name(data, files[file_index])
        else:
            file_name = parse_file_name(file_index)
        x1, y1, x2, y2 = segment
        influence_geometry.append(
            {
                "file": file_name,
                "sheet": sheet_for_point(sheet_meta, (x1 + x2) / 2.0, (y1 + y2) / 2.0),
                "layer": layer,
                "type": kind,
                "segment": segment,
            }
        )

    raw: list[dict[str, Any]] = []
    for (file_index, sheet), segments in sorted(grouped.items(), key=lambda x: (str(x[0][0]), str(x[0][1]))):
        if isinstance(file_index, int) and 0 <= file_index < len(files):
            file_name = data_file_name(data, files[file_index])
        else:
            file_name = parse_file_name(file_index)
        xs = [v for _layer, seg, _kind in segments for v in (seg[0], seg[2])]
        ys = [v for _layer, seg, _kind in segments for v in (seg[1], seg[3])]
        if not xs or not ys:
            continue
        eps = max(0.01, math.hypot(max(xs) - min(xs), max(ys) - min(ys)) * 0.001)
        candidates, clipped = axis_aligned_rectangles([(layer, seg) for layer, seg, _kind in segments], eps)
        for number, candidate in enumerate(candidates, 1):
            bbox = candidate["bbox"]
            types = sorted({geometry_layer_type(item.get("layer", ""), rules) for item in candidate["segments"]})
            if "ceiling_access" in types:
                zone_kind = "ceiling_access"
            elif "ceiling_lighting" in types:
                zone_kind = "ceiling_lighting"
            elif "ceiling_shape" in types:
                zone_kind = "ceiling_shape"
            else:
                zone_kind = "ceiling"

            labels: list[dict[str, Any]] = []
            features: set[str] = set()
            rooms: list[str] = []
            elevations: list[dict[str, Any]] = []
            elevation_values: set[tuple[float, str]] = set()
            for rec in records:
                if rec.get("x") is None or rec.get("y") is None:
                    continue
                if file_name and str(rec.get("file_name") or rec.get("file") or "") != str(file_name):
                    continue
                if sheet is not None and rec.get("sheet") is not None and rec.get("sheet") != sheet:
                    continue
                try:
                    x, y = float(rec["x"]), float(rec["y"])
                except (TypeError, ValueError):
                    continue
                if not (bbox[0] <= x <= bbox[2] and bbox[1] <= y <= bbox[3]):
                    continue
                room = match_room(rec["text"], rules)
                if room and room not in rooms:
                    rooms.append(room)
                tags = ceiling_feature_tags(rec["text"], rules)
                features.update(tags)
                if tags:
                    labels.append(
                        {
                            "text": rec["text"],
                            "tags": tags,
                            "evidence": [evidence_of(rec)],
                        }
                    )
                for value_m, unit in ceiling_elevation_candidates(rec["text"], rules):
                    if (value_m, unit) not in elevation_values:
                        elevation_values.add((value_m, unit))
                        elevations.append(
                            {
                                "value_m": value_m,
                                "unit": unit,
                                "evidence": [evidence_of(rec)],
                            }
                        )

            influences: list[dict[str, Any]] = []
            for item in influence_geometry:
                if file_name and str(item.get("file", "")) != str(file_name):
                    continue
                if sheet is not None and item.get("sheet") is not None and item.get("sheet") != sheet:
                    continue
                seg = item["segment"]
                mx, my = (seg[0] + seg[2]) / 2.0, (seg[1] + seg[3]) / 2.0
                if not (bbox[0] <= mx <= bbox[2] and bbox[1] <= my <= bbox[3]):
                    continue
                copied = dict(item)
                copied["evidence"] = [{"layer": item["layer"], "segment": seg, "file": item["file"], "sheet": item["sheet"]}]
                influences.append(copied)
            if "drop" in features:
                influences.append({"type": "drop", "evidence": [item["evidence"][0] for item in labels if "drop" in item["tags"]][:1]})
            if "beam" in features:
                influences.append({"type": "beam", "evidence": [item["evidence"][0] for item in labels if "beam" in item["tags"]][:1]})

            reasons = []
            if clipped:
                reasons.append("坐标轴数量超限，仅检查前部分候选")
            if any(kind in types for kind in ("ceiling_access", "ceiling_lighting", "ceiling_shape")) and "ceiling" in types:
                reasons.append("主吊顶与附属分区混合在同一闭合候选，需确认")
            if zone_kind == "ceiling":
                if len(elevations) == 1:
                    elevation_status = "candidate"
                elif not elevations:
                    elevation_status = "review"
                    reasons.append("缺显式吊顶标高/高度证据")
                else:
                    elevation_status = "review"
                    reasons.append("吊顶标高/高度证据冲突")
                status = "candidate" if elevation_status == "candidate" and not reasons else "review"
            else:
                elevation_status = "not_required"
                status = "review" if reasons else "candidate"
            raw.append(
                {
                    "id": f"ceiling-zone-{len(raw) + 1}",
                    "zone_kind": zone_kind,
                    "file": file_name,
                    "sheet": sheet,
                    "rooms": rooms,
                    "polygon": candidate["polygon"],
                    "bbox": bbox,
                    "labels": labels,
                    "features": sorted(features),
                    "influences": influences,
                    "elevation_candidates": elevations,
                    "elevation_status": elevation_status,
                    "segments": candidate["segments"],
                    "non_axis_segments": candidate.get("non_axis_segments", []),
                    "confidence": float(rules["confidence"]["direct_label"] if labels or zone_kind != "ceiling" else rules["confidence"]["context_match"]),
                    "status": status,
                    "review_reason": "；".join(dict.fromkeys(reasons)),
                }
            )

    ordered = sorted(raw, key=lambda row: (row["bbox"][2] - row["bbox"][0]) * (row["bbox"][3] - row["bbox"][1]), reverse=True)
    for i, child in enumerate(ordered):
        if child["zone_kind"] == "ceiling":
            continue
        cb = child["bbox"]
        for parent in ordered:
            if parent is child or parent["zone_kind"] != "ceiling":
                continue
            pb = parent["bbox"]
            if pb[0] <= cb[0] and cb[2] <= pb[2] and pb[1] <= cb[1] and cb[3] <= pb[3]:
                child["parent_zone_id"] = parent["id"]
                if child["zone_kind"] not in parent["features"]:
                    parent["features"].append(child["zone_kind"].replace("ceiling_", ""))
                break
    return ordered

def stair_ramp_step_kind(text: str, rules: dict[str, Any]) -> str:
    """按文字优先判断楼梯、坡道或台阶；坡道优先于楼梯，楼梯优先于台阶。"""
    low = str(text or "").lower()
    for kind in ("ramp", "stair", "step"):
        for pattern in rules.get(f"{kind}_patterns", []):
            if str(pattern).lower() in low:
                return kind
    return ""

def stair_ramp_step_materials(text: str, rules: dict[str, Any]) -> list[str]:
    low = str(text or "").lower()
    return list(dict.fromkeys(
        str(pattern) for pattern in rules.get("stair_material_patterns", [])
        if str(pattern).lower() in low
    ))

def stair_ramp_step_area_candidates(text: str, rules: dict[str, Any]) -> list[dict[str, Any]]:
    pattern = rules.get("stair_area_pattern")
    if not pattern:
        return []
    out: list[dict[str, Any]] = []
    for match in re.finditer(pattern, str(text or ""), re.I):
        try:
            value = float(match.group(1))
        except (TypeError, ValueError):
            continue
        basis = "展开面积" if "展开" in match.group(0) else "投影面积"
        out.append(
            {
                "value": round(value, 6),
                "unit": "m2",
                "basis": basis,
                "raw": match.group(0),
                "status": "review",
                "evidence": [],
            }
        )
    return out

def stair_ramp_step_count_candidates(text: str, rules: dict[str, Any]) -> list[int]:
    pattern = rules.get("stair_count_pattern")
    if not pattern:
        return []
    out: list[int] = []
    for match in re.finditer(pattern, str(text or ""), re.I):
        try:
            value = int(match.group(1))
        except (TypeError, ValueError):
            continue
        if value not in out:
            out.append(value)
    return out

def stair_ramp_step_slope_candidates(text: str, rules: dict[str, Any]) -> list[str]:
    pattern = rules.get("stair_slope_pattern")
    if not pattern:
        return []
    return list(dict.fromkeys(match.group(0) for match in re.finditer(pattern, str(text or ""), re.I)))

def stair_ramp_step_dimension_candidates(text: str, rules: dict[str, Any]) -> list[dict[str, Any]]:
    pattern = rules.get("dimension_pattern")
    if not pattern:
        return []
    out: list[dict[str, Any]] = []
    for match in re.finditer(pattern, str(text or ""), re.I):
        out.append({"values": [match.group(1), match.group(2)], "raw": match.group(0)})
    return out

def stair_ramp_step_candidates(
    records: list[dict[str, Any]],
    data: dict[str, Any],
    rules: dict[str, Any],
    sheet_meta: dict[Any, dict[str, Any]],
) -> list[dict[str, Any]]:
    """提取楼梯/坡道/台阶初稿；只出待确认面积、材料、几何和证据，不出正式量。"""
    files = data.get("files") or []
    geometry_groups: dict[tuple[str, Any, str], list[dict[str, Any]]] = defaultdict(list)
    for file_index, layer, segment in flatten_geometry(data):
        geometry_kind = geometry_layer_type(layer, rules)
        if geometry_kind not in {"stair", "stair_landing", "ramp", "step"}:
            continue
        if isinstance(file_index, int) and 0 <= file_index < len(files):
            file_name = data_file_name(data, files[file_index])
        else:
            file_name = parse_file_name(file_index)
        x1, y1, x2, y2 = segment
        sheet = sheet_for_point(sheet_meta, (x1 + x2) / 2.0, (y1 + y2) / 2.0)
        geometry_groups[(str(file_name), sheet, geometry_kind)].append(
            {"layer": layer, "segment": segment, "file": file_name, "sheet": sheet}
        )

    out: list[dict[str, Any]] = []
    for rec in records:
        kind = stair_ramp_step_kind(rec.get("text", ""), rules)
        if not kind:
            continue
        file_name = str(rec.get("file_name") or parse_file_name(rec.get("file")))
        sheet = rec.get("sheet")
        compatible = {"stair", "stair_landing"} if kind == "stair" else {kind}
        geometry: list[dict[str, Any]] = []
        for (gfile, gsheet, gkind), items in geometry_groups.items():
            if gfile != file_name:
                continue
            if sheet is not None and gsheet is not None and gsheet != sheet:
                continue
            if gkind in compatible:
                geometry.extend(items)

        bbox = None
        if geometry:
            xs = [v for item in geometry for v in (item["segment"][0], item["segment"][2])]
            ys = [v for item in geometry for v in (item["segment"][1], item["segment"][3])]
            if xs and ys:
                bbox = [min(xs), min(ys), max(xs), max(ys)]

        rooms = []
        room = match_room(rec.get("text", ""), rules)
        if room:
            rooms.append(room)

        materials = stair_ramp_step_materials(rec.get("text", ""), rules)
        areas = stair_ramp_step_area_candidates(rec.get("text", ""), rules)
        for item in areas:
            item["evidence"] = [evidence_of(rec)]
        counts = stair_ramp_step_count_candidates(rec.get("text", ""), rules)
        slopes = stair_ramp_step_slope_candidates(rec.get("text", ""), rules)
        dimensions = stair_ramp_step_dimension_candidates(rec.get("text", ""), rules)

        reasons = ["P1 初稿：展开面积和分项材料均待人工确认"]
        if not geometry:
            reasons.append("未找到匹配的楼梯/坡道/台阶图层几何")
        if not areas:
            reasons.append("缺显式展开面积/投影面积，不能自动换算")
        if not materials:
            reasons.append("缺分项材料证据")
        if rec.get("x") is None or rec.get("y") is None:
            reasons.append("文字缺坐标，几何归属需确认")

        out.append(
            {
                "id": f"stair-ramp-step-{len(out) + 1}",
                "kind": kind,
                "file": file_name,
                "sheet": sheet,
                "space": rec.get("space"),
                "rooms": rooms,
                "raw": rec.get("text", ""),
                "evidence": [evidence_of(rec)],
                "dimensions": dimensions,
                "count_candidates": counts,
                "slope_candidates": slopes,
                "materials": [
                    {"name": name, "status": "review", "evidence": [evidence_of(rec)]}
                    for name in materials
                ],
                "area_candidates": areas,
                "pending_expanded_area": (
                    dict(areas[0])
                    if areas
                    else {
                        "value": None,
                        "unit": "m2",
                        "basis": "missing_explicit_area",
                        "status": "review",
                        "review_reason": "缺显式展开面积/投影面积，不能自动换算",
                        "evidence": [],
                    }
                ),
                "geometry": {
                    "status": "candidate" if geometry else "review",
                    "bbox": bbox,
                    "bbox_area_drawing_units2": (
                        round((bbox[2] - bbox[0]) * (bbox[3] - bbox[1]), 6)
                        if bbox else None
                    ),
                    "segment_count": len(geometry),
                    "segments": geometry[:20],
                    "review_reason": "" if geometry else "未找到匹配的楼梯/坡道/台阶图层几何",
                },
                "confidence": float(
                    rules["confidence"]["direct_label"] if geometry and (areas or materials) else rules["confidence"]["pattern_match"]
                ),
                "status": "review",
                "review_reason": "；".join(dict.fromkeys(reasons)),
                "boundary": "仅初稿：不自动确认展开面积、材料量或最终工程量。",
            }
        )
    return out

def exterior_wall_zone_kind(text: str, rules: dict[str, Any]) -> str:
    """按文字优先区分防火隔离带、女儿墙内侧、保温、饰面和外墙。"""
    low = str(text or "").lower()
    checks = (
        ("fire_barrier", rules.get("fire_barrier_patterns", [])),
        ("parapet_inner", rules.get("parapet_inner_patterns", [])),
        ("insulation", rules.get("insulation_patterns", [])),
        ("facade_finish", rules.get("facade_finish_patterns", [])),
        ("exterior_wall", rules.get("exterior_wall_patterns", [])),
    )
    for kind, patterns in checks:
        if any(str(pattern).lower() in low for pattern in patterns):
            return kind
    return ""

def exterior_wall_material_candidates(text: str, rules: dict[str, Any]) -> list[str]:
    low = str(text or "").lower()
    return list(dict.fromkeys(
        str(pattern) for pattern in rules.get("exterior_wall_material_patterns", [])
        if str(pattern).lower() in low
    ))

def exterior_wall_thickness_candidates(text: str, rules: dict[str, Any]) -> list[dict[str, Any]]:
    pattern = rules.get("exterior_wall_thickness_pattern")
    if not pattern:
        return []
    out: list[dict[str, Any]] = []
    for match in re.finditer(pattern, str(text or ""), re.I):
        raw_value = match.group(1) if match.group(1) is not None else match.group(3)
        raw_unit = match.group(2) if match.group(2) is not None else match.group(4)
        try:
            value = float(raw_value)
        except (TypeError, ValueError):
            continue
        unit = "mm" if str(raw_unit).lower() in {"mm", "毫米"} else "m"
        value_mm = value * 1000.0 if unit == "m" else value
        out.append(
            {
                "value": round(value, 6),
                "unit": unit,
                "value_mm": round(value_mm, 6),
                "raw": match.group(0),
                "status": "candidate",
                "evidence": [],
            }
        )
    return out

def exterior_elevation_candidates(text: str, rules: dict[str, Any]) -> list[dict[str, Any]]:
    pattern = rules.get("exterior_elevation_pattern")
    if not pattern:
        return []
    out: list[dict[str, Any]] = []
    for match in re.finditer(pattern, str(text or ""), re.I):
        try:
            value = float(match.group(1))
        except (TypeError, ValueError):
            continue
        raw_unit = (match.group(2) or "").lower()
        unit = "mm" if raw_unit in {"mm", "毫米"} else "m"
        value_m = value / 1000.0 if unit == "mm" else value
        out.append(
            {
                "value": round(value, 6),
                "unit": unit,
                "value_m": round(value_m, 6),
                "unit_status": "candidate" if raw_unit else "review",
                "raw": match.group(0),
                "status": "candidate",
                "evidence": [],
            }
        )
    return out

def exterior_wall_zones(
    records: list[dict[str, Any]],
    data: dict[str, Any],
    rules: dict[str, Any],
    sheet_meta: dict[Any, dict[str, Any]],
) -> list[dict[str, Any]]:
    """提取外墙分格、保温、防火隔离带和女儿墙内侧候选；只出证据，不出工程量。"""
    files = data.get("files") or []
    geometry_groups: dict[tuple[str, Any, str], list[dict[str, Any]]] = defaultdict(list)
    for file_index, layer, segment in flatten_geometry(data):
        geometry_kind = geometry_layer_type(layer, rules)
        if geometry_kind not in {"exterior_wall", "insulation", "fire_barrier", "parapet_inner", "facade_finish", "wall"}:
            continue
        if isinstance(file_index, int) and 0 <= file_index < len(files):
            file_name = data_file_name(data, files[file_index])
        else:
            file_name = parse_file_name(file_index)
        x1, y1, x2, y2 = segment
        sheet = sheet_for_point(sheet_meta, (x1 + x2) / 2.0, (y1 + y2) / 2.0)
        geometry_groups[(str(file_name), sheet, geometry_kind)].append(
            {"layer": layer, "segment": segment, "file": file_name, "sheet": sheet}
        )

    compatible = {
        "exterior_wall": {"exterior_wall", "facade_finish", "wall"},
        "insulation": {"insulation", "exterior_wall", "wall"},
        "fire_barrier": {"fire_barrier", "insulation", "exterior_wall", "wall"},
        "parapet_inner": {"parapet_inner", "insulation", "exterior_wall", "wall"},
        "facade_finish": {"facade_finish", "exterior_wall", "wall"},
    }
    out: list[dict[str, Any]] = []
    for rec in records:
        kind = exterior_wall_zone_kind(rec.get("text", ""), rules)
        if not kind:
            continue
        file_name = str(rec.get("file_name") or parse_file_name(rec.get("file")))
        sheet = rec.get("sheet")
        geometry: list[dict[str, Any]] = []
        for (gfile, gsheet, gkind), items in geometry_groups.items():
            if gfile != file_name:
                continue
            if sheet is not None and gsheet is not None and gsheet != sheet:
                continue
            if gkind in compatible.get(kind, set()):
                geometry.extend(items)
        dedup: dict[tuple[Any, tuple[float, ...]], dict[str, Any]] = {}
        for item in geometry:
            key = (item.get("layer"), tuple(item.get("segment", [])))
            dedup[key] = item
        geometry = list(dedup.values())

        bbox = None
        total_length = 0.0
        if geometry:
            xs = [v for item in geometry for v in (item["segment"][0], item["segment"][2])]
            ys = [v for item in geometry for v in (item["segment"][1], item["segment"][3])]
            if xs and ys:
                bbox = [min(xs), min(ys), max(xs), max(ys)]
            total_length = sum(
                math.hypot(item["segment"][2] - item["segment"][0], item["segment"][3] - item["segment"][1])
                for item in geometry
            )

        materials = exterior_wall_material_candidates(rec.get("text", ""), rules)
        thicknesses = exterior_wall_thickness_candidates(rec.get("text", ""), rules)
        elevations = exterior_elevation_candidates(rec.get("text", ""), rules)
        for item in thicknesses:
            item["evidence"] = [evidence_of(rec)]
        for item in elevations:
            item["evidence"] = [evidence_of(rec)]

        rooms = []
        room = match_room(rec.get("text", ""), rules)
        if room:
            rooms.append(room)

        elevation_values = {round(item["value_m"], 6) for item in elevations}
        reasons: list[str] = []
        if not geometry:
            reasons.append("未找到匹配的外墙/保温/隔离带图层几何")
        if not materials:
            reasons.append("缺材料证据")
        if kind in {"insulation", "fire_barrier", "parapet_inner"} and not thicknesses:
            reasons.append("缺保温/隔离带厚度证据")
        if kind in {"insulation", "fire_barrier", "parapet_inner"} and not elevations:
            reasons.append("缺标高/保温范围证据")
        if len(elevation_values) > 1:
            reasons.append("标高/保温范围证据冲突")
        if any(item.get("unit_status") == "review" for item in elevations):
            reasons.append("标高单位未明确，按 m 暂记待确认")
        if rec.get("x") is None or rec.get("y") is None:
            reasons.append("文字缺坐标，外墙分段归属需确认")

        status = "candidate" if not reasons else "review"
        out.append(
            {
                "id": f"exterior-wall-zone-{len(out) + 1}",
                "zone_kind": kind,
                "file": file_name,
                "sheet": sheet,
                "space": rec.get("space"),
                "rooms": rooms,
                "raw": rec.get("text", ""),
                "evidence": [evidence_of(rec)],
                "materials": [
                    {"name": name, "status": "candidate", "evidence": [evidence_of(rec)]}
                    for name in materials
                ],
                "thickness_candidates": thicknesses,
                "elevation_candidates": elevations,
                "thickness_status": "candidate" if thicknesses else "review",
                "elevation_status": "candidate" if len(elevation_values) == 1 and not any(item.get("unit_status") == "review" for item in elevations) else "review",
                "geometry": {
                    "status": "candidate" if geometry else "review",
                    "bbox": bbox,
                    "segment_count": len(geometry),
                    "total_length_drawing_units": round(total_length, 6),
                    "segments": geometry[:20],
                    "review_reason": "" if geometry else "未找到匹配的外墙/保温/隔离带图层几何",
                },
                "confidence": float(
                    rules["confidence"]["direct_label"] if status == "candidate" else rules["confidence"]["pattern_match"]
                ),
                "status": status,
                "review_reason": "；".join(dict.fromkeys(reasons)),
                "boundary": "候选中间数据；不输出外墙面积、保温面积、材料量或最终工程量。",
            }
        )
    return out

def analyze_file(path: Path, rules: dict[str, Any]) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    records = read_records(data)
    sheet_meta = {s.get("id"): s for s in (data.get("meta", {}).get("sheets") or []) if isinstance(s, dict)}

    views: list[dict[str, Any]] = []
    rooms: list[dict[str, Any]] = []
    openings: list[dict[str, Any]] = []
    practices: list[dict[str, Any]] = []
    scales: list[dict[str, Any]] = []
    units: list[dict[str, Any]] = []
    review: list[dict[str, Any]] = []

    for rec in records:
        text = rec["text"]
        view_type, confidence = match_view(text, rules)
        if view_type:
            sheet_id = rec.get("sheet")
            item = {
                "type": view_type,
                "title": text,
                "confidence": confidence,
                "status": "candidate",
                "evidence": [evidence_of(rec)],
            }
            if sheet_id in sheet_meta:
                item["sheet_bbox"] = sheet_meta[sheet_id].get("bbox")
            views.append(item)

        room = match_room(text, rules)
        if room:
            rooms.append(
                {
                    "name": room,
                    "raw": text,
                    "confidence": float(rules["confidence"]["pattern_match"]),
                    "status": "candidate",
                    "evidence": [evidence_of(rec)],
                }
            )

        for code in opening_candidates(text, rules):
            dims = re.search(rules["dimension_pattern"], text)
            count_match = re.search(r"(\d{1,4})\s*(?:樘|个|扇|处)", text)
            item = {
                "code": code,
                "raw": text,
                "confidence": float(rules["confidence"]["pattern_match"]),
                "status": "candidate",
                "evidence": [evidence_of(rec)],
            }
            if dims:
                item["nominal_size"] = [dims.group(1), dims.group(2)]
                item["confidence"] = float(rules["confidence"]["direct_label"])
            else:
                item["review_reason"] = "缺宽高尺寸"
                review.append({"type": "opening", "reason": "缺宽高尺寸", "evidence": item["evidence"]})
            if count_match:
                item["explicit_count"] = int(count_match.group(1))
            openings.append(item)

        for practice in practice_candidates(text, rules):
            practice["raw"] = text
            practice["evidence"] = [evidence_of(rec)]
            practices.append(practice)
            if practice.get("review_reason"):
                review.append({"type": "practice", "reason": practice["review_reason"], "evidence": practice["evidence"]})

        for item in scale_candidates(text, rules):
            item["evidence"] = [evidence_of(rec)]
            scales.append(item)
        for item in unit_candidates(text, rules):
            item["evidence"] = [evidence_of(rec)]
            units.append(item)

    room_schedules, unbound_room_schedules = build_room_schedules(records, rules, sheet_meta)
    audit = scale_unit_audit(records, rules, sheet_meta)
    geometry_rows = geometry_index(data, rules)
    boundaries = room_boundaries(records, data, rules, sheet_meta)
    details = node_detail_index(records, rules, sheet_meta)
    attribute_openings(openings, records, data, rules, sheet_meta)
    walls = wall_segments(boundaries, openings, records, data, rules, sheet_meta)
    ceilings = ceiling_zones(records, data, rules, sheet_meta)
    stair_ramp_steps = stair_ramp_step_candidates(records, data, rules, sheet_meta)
    exterior_walls = exterior_wall_zones(records, data, rules, sheet_meta)
    opening_summary = summarize_openings(openings)

    for item in boundaries:
        if item.get("status") != "candidate":
            review.append(
                {
                    "type": "room_boundary",
                    "reason": item.get("review_reason") or "房间边界需确认",
                    "evidence": item.get("segments", [])[:1],
                }
            )
    for item in walls:
        if item.get("status") != "candidate":
            review.append(
                {
                    "type": "wall_segment",
                    "reason": item.get("review_reason") or "墙段需确认",
                    "evidence": [{"segment": item.get("segment", [])}],
                }
            )
    for item in ceilings:
        if item.get("status") != "candidate":
            review.append(
                {
                    "type": "ceiling_zone",
                    "reason": item.get("review_reason") or "吊顶分区需确认",
                    "evidence": item.get("segments", [])[:1],
                }
            )
    for item in stair_ramp_steps:
        review.append(
            {
                "type": "stair_ramp_step",
                "reason": item.get("review_reason") or "楼梯/坡道/台阶初稿需确认",
                "evidence": item.get("evidence", [])[:1],
            }
        )
    for item in exterior_walls:
        if item.get("status") != "candidate":
            review.append(
                {
                    "type": "exterior_wall_zone",
                    "reason": item.get("review_reason") or "外墙分格/保温分区需确认",
                    "evidence": item.get("evidence", [])[:1],
                }
            )
    for item in details:
        if item.get("status") != "candidate":
            review.append(
                {
                    "type": "node_detail",
                    "reason": item.get("review_reason") or "节点索引需确认",
                    "evidence": item.get("evidence", [])[:1],
                }
            )
    for item in openings:
        geometry = item.get("geometry")
        if geometry and geometry.get("status") != "candidate":
            review.append(
                {
                    "type": "opening_geometry",
                    "reason": geometry.get("review_reason") or "门窗几何需确认",
                    "evidence": item.get("evidence", [])[:1],
                }
            )

    for item in room_schedules:
        if item["status"] == "review":
            review.append({"type": "room_schedule", "reason": item["review_reason"], "evidence": item["evidence"][:1]})
    for item in unbound_room_schedules:
        review.append({"type": "room_schedule", "reason": item["review_reason"], "evidence": item["evidence"][:1]})
    for item in opening_summary:
        if item["status"] != "candidate":
            review.append({"type": "opening_summary", "reason": item["review_reason"], "evidence": item["evidence"][:1]})
    for item in audit:
        if item["status"] != "candidate":
            review.append({"type": "scale_unit", "reason": item["review_reason"], "evidence": item["evidence"][:1]})
    for item in geometry_rows:
        review.append({"type": "geometry", "reason": item["review_reason"], "evidence": item["evidence"][:1]})

    no_coord = [r for r in records if r.get("x") is None or r.get("y") is None]
    if no_coord:
        review.append(
            {
                "type": "evidence",
                "reason": "部分文字无坐标，不能用于精确闭合",
                "count": len(no_coord),
                "evidence": [evidence_of(no_coord[0])],
            }
        )

    return {
        "schema": "cad-descriptive-geometry/v7",
        "source_file": str(path),
        "summary": {
            "records": len(records),
            "views": len(views),
            "rooms": len(rooms),
            "room_schedules": len(room_schedules),
            "openings": len(openings),
            "opening_codes": len(opening_summary),
            "practices": len(practices),
            "scales": len(scales),
            "units": len(units),
            "scale_unit_contexts": len(audit),
            "geometry_layer_groups": len(geometry_rows),
            "room_boundaries": len(boundaries),
            "room_boundary_candidates": sum(1 for row in boundaries if row.get("rooms")),
            "wall_segments": len(walls),
            "wall_segment_candidates": sum(1 for row in walls if row.get("status") == "candidate"),
            "ceiling_zones": len(ceilings),
            "ceiling_zone_candidates": sum(1 for row in ceilings if row.get("status") == "candidate"),
            "stair_ramp_steps": len(stair_ramp_steps),
            "stair_ramp_step_drafts": sum(1 for row in stair_ramp_steps if row.get("status") == "review"),
            "stair_ramp_step_materials": len({
                material.get("name", "")
                for row in stair_ramp_steps
                for material in row.get("materials", [])
                if material.get("name")
            }),
            "exterior_wall_zones": len(exterior_walls),
            "exterior_wall_zone_candidates": sum(1 for row in exterior_walls if row.get("status") == "candidate"),
            "insulation_zones": sum(1 for row in exterior_walls if row.get("zone_kind") == "insulation"),
            "fire_barrier_zones": sum(1 for row in exterior_walls if row.get("zone_kind") == "fire_barrier"),
            "parapet_inner_zones": sum(1 for row in exterior_walls if row.get("zone_kind") == "parapet_inner"),
            "node_details": len(details),
            "review_items": len(review),
        },
        "views": views,
        "rooms": rooms,
        "room_schedules": room_schedules,
        "openings": openings,
        "opening_summary": opening_summary,
        "practices": practices,
        "scales": scales,
        "units": units,
        "scale_unit_audit": audit,
        "geometry_index": geometry_rows,
        "room_boundaries": boundaries,
        "wall_segments": walls,
        "ceiling_zones": ceilings,
        "stair_ramp_steps": stair_ramp_steps,
        "exterior_wall_zones": exterior_walls,
        "node_detail_index": details,
        "review": review,
        "boundary": "候选中间数据；不输出工程量。",
    }

def write_markdown(payload: dict[str, Any], path: Path) -> None:
    summary = payload["summary"]
    lines = [
        "# 描述几何 / 装饰中间数据复核",
        "",
        f"- 源文件：`{payload['source_file']}`",
        f"- 候选：视图 {summary['views']}，房间 {summary['rooms']}，房间做法行 {summary['room_schedules']}，"
        f"门窗记录 {summary['openings']}，门窗编号 {summary['opening_codes']}，做法 {summary['practices']}，待复核 {summary['review_items']}",
        "",
        "## 视图候选",
        "",
    ]
    if payload["views"]:
        lines.append("| 类型 | 原文 | 置信 | 图层 | 坐标 |")
        lines.append("|---|---|---:|---|---|")
        for row in payload["views"][:80]:
            ev = row["evidence"][0] if row["evidence"] else {}
            lines.append(f"| {row['type']} | {row['title']} | {row['confidence']:.2f} | {ev.get('layer', '')} | {ev.get('coord', '')} |")
    else:
        lines.append("无")

    lines += ["", "## 房间做法候选", ""]
    if payload["room_schedules"]:
        lines.append("| 房间 | 地面 | 墙面 | 顶棚 | 踢脚 | 状态 | 待复核 |")
        lines.append("|---|---|---|---|---|---|---|")
        for row in payload["room_schedules"][:80]:
            def part_code(part: str) -> str:
                return "、".join(p["code"] for p in row["practices"] if p["part"] == part)

            lines.append(
                f"| {row['room']} | {part_code('floor')} | {part_code('wall')} | {part_code('ceiling')} | "
                f"{part_code('skirting')} | {row['status']} | {row['review_reason']} |"
            )
    else:
        lines.append("无")

    lines += ["", "## 门窗汇总候选", ""]
    if payload["opening_summary"]:
        lines.append("| 编号 | 名义尺寸 | 记录数 | 块实例 | 原文数量 | 数量口径 | 状态 |")
        lines.append("|---|---|---:|---:|---:|---|---|")
        for row in payload["opening_summary"][:80]:
            size = "x".join(row.get("nominal_size", [])) or ""
            lines.append(
                f"| {row['code']} | {size} | {row['record_count']} | {row['block_instance_count']} | "
                f"{row['explicit_count'] if row['explicit_count'] is not None else ''} | {row['count_basis']} | {row['status']} |"
            )
    else:
        lines.append("无")

    lines += ["", "## 比例与单位审计", ""]
    if payload["scale_unit_audit"]:
        lines.append("| 文件 | 图框 | 比例 | 单位 | 空间 | 状态 | 待复核 |")
        lines.append("|---|---|---|---|---|---|---|")
        for row in payload["scale_unit_audit"][:80]:
            lines.append(
                f"| {row['file']} | {row['sheet']} | {'、'.join(row['scales'])} | {'、'.join(row['units'])} | "
                f"{'、'.join(row['spaces']) or '未知'} | {row['status']} | {row['review_reason']} |"
            )
    else:
        lines.append("无")

    lines += ["", "## 几何图层候选", ""]
    if payload["geometry_index"]:
        lines.append("| 类型 | 文件 | 图层 | 线段数 | 总长(图面单位) | 状态 |")
        lines.append("|---|---|---|---:|---:|---|")
        for row in payload["geometry_index"][:80]:
            lines.append(
                f"| {row['type']} | {row['file']} | {row['layer']} | {row['segment_count']} | "
                f"{row['total_length_drawing_units']} | {row['status']} |"
            )
    else:
        lines.append("无")

    lines += ["", "## 房间闭合边界候选", ""]
    if payload["room_boundaries"]:
        lines.append("| 编号 | 文件 | 图框 | 房间 | 状态 |")
        lines.append("|---|---|---|---|---|")
        for row in payload["room_boundaries"][:80]:
            lines.append(
                f"| {row['id']} | {row['file']} | {row['sheet']} | {'、'.join(row['rooms']) or '未绑定'} | {row['status']} |"
            )
    else:
        lines.append("无")

    lines += ["", "## 墙段分段候选", ""]
    if payload["wall_segments"]:
        lines.append("| 编号 | 边界 | 房间 | 方向 | 类型 | 长度(图面单位) | 门窗 | 墙高 | 状态 |")
        lines.append("|---|---|---|---|---|---:|---|---|---|")
        for row in payload["wall_segments"][:120]:
            height = "、".join(f"{x['value']}{x['unit']}" for x in row.get("height_candidates", []))
            lines.append(
                f"| {row['id']} | {row['boundary_id']} | {'、'.join(row['rooms']) or '未绑定'} | {row['direction']} | "
                f"{row['segment_kind']} | {row['length_drawing_units']} | {'、'.join(row['opening_codes']) or '无'} | "
                f"{height or '缺'} | {row['status']} |"
            )
    else:
        lines.append("无")

    lines += ["", "## 顶棚分区候选", ""]
    if payload["ceiling_zones"]:
        lines.append("| 编号 | 类型 | 文件 | 图框 | 房间 | 标高候选 | 特征 | 状态 |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for row in payload["ceiling_zones"][:120]:
            elevations = "、".join(
                f"{item['value_m']}{item['unit']}" for item in row.get("elevation_candidates", [])
            )
            lines.append(
                f"| {row['id']} | {row['zone_kind']} | {row['file']} | {row['sheet']} | "
                f"{'、'.join(row['rooms']) or '未绑定'} | {elevations or '缺'} | "
                f"{'、'.join(row.get('features', [])) or '无'} | {row['status']} |"
            )
    else:
        lines.append("无")

    lines += ["", "## 楼梯/坡道/台阶初稿", ""]
    if payload["stair_ramp_steps"]:
        lines.append("| 编号 | 类型 | 文件 | 图框 | 房间 | 面积候选 | 分项材料 | 几何 | 状态 |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for row in payload["stair_ramp_steps"][:120]:
            area = row.get("pending_expanded_area", {})
            area_text = (
                f"{area.get('value')}{area.get('unit')}"
                if area.get("value") is not None
                else area.get("basis", "缺")
            )
            materials = "、".join(item.get("name", "") for item in row.get("materials", []))
            geometry = row.get("geometry", {})
            geometry_text = f"{geometry.get('segment_count', 0)}段"
            lines.append(
                f"| {row['id']} | {row['kind']} | {row['file']} | {row['sheet']} | "
                f"{'、'.join(row['rooms']) or '未绑定'} | {area_text} | {materials or '缺'} | "
                f"{geometry_text} | {row['status']} |"
            )
    else:
        lines.append("无")

    lines += ["", "## 外墙分格与保温分区候选", ""]
    if payload["exterior_wall_zones"]:
        lines.append("| 编号 | 类型 | 文件 | 图框 | 房间 | 材料 | 厚度 | 标高 | 几何 | 状态 |")
        lines.append("|---|---|---|---|---|---|---|---|---|---|")
        for row in payload["exterior_wall_zones"][:120]:
            materials = "、".join(item.get("name", "") for item in row.get("materials", []))
            thicknesses = "、".join(
                f"{item.get('value_mm')}mm" for item in row.get("thickness_candidates", [])
            )
            elevations = "、".join(
                f"{item.get('value_m')}m" for item in row.get("elevation_candidates", [])
            )
            geometry = row.get("geometry", {})
            lines.append(
                f"| {row['id']} | {row['zone_kind']} | {row['file']} | {row['sheet']} | "
                f"{'、'.join(row['rooms']) or '未绑定'} | {materials or '缺'} | {thicknesses or '缺'} | "
                f"{elevations or '缺'} | {geometry.get('segment_count', 0)}段 | {row['status']} |"
            )
    else:
        lines.append("无")

    lines += ["", "## 做法节点索引候选", ""]
    if payload["node_detail_index"]:
        lines.append("| 做法 | 节点 | 文件 | 图框 | 状态 |")
        lines.append("|---|---|---|---|---|")
        for row in payload["node_detail_index"][:80]:
            lines.append(
                f"| {'、'.join(row['practice_codes']) or '未绑定'} | {'、'.join(row['node_codes'])} | "
                f"{row['file']} | {row['sheet']} | {row['status']} |"
            )
    else:
        lines.append("无")

    lines += ["", "## 待复核", ""]
    if payload["review"]:
        for row in payload["review"][:120]:
            reason = row.get("reason", "")
            count = row.get("count", "")
            lines.append(f"- {row['type']}: {reason}{'；数量 ' + str(count) if count != '' else ''}")
    else:
        lines.append("无")
    lines += ["", "## 边界", "", "本报告只给候选中间数据和证据，不输出工程量。", ""]
    path.write_text("\n".join(lines), encoding="utf-8")

def write_csv(payload: dict[str, Any], path: Path) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["type", "key", "raw", "part", "nominal_size", "count", "confidence", "status", "review_reason"])
        for row in payload["views"]:
            writer.writerow(["view", row["type"], row["title"], "", "", "", row["confidence"], row["status"], ""])
        for row in payload["rooms"]:
            writer.writerow(["room", row["name"], row["raw"], "", "", "", row["confidence"], row["status"], ""])
        for row in payload["room_schedules"]:
            raw = " | ".join(dict.fromkeys([p.get("raw", "") for p in row["practices"]]))
            parts = "、".join(dict.fromkeys(p["part"] for p in row["practices"]))
            codes = "、".join(p["code"] for p in row["practices"])
            writer.writerow(["room_schedule", row["room"], raw, parts, codes, "", row["confidence"], row["status"], row["review_reason"]])
        for row in payload["openings"]:
            writer.writerow(
                ["opening", row["code"], row["raw"], "", "x".join(row.get("nominal_size", [])), row.get("explicit_count", ""),
                 row["confidence"], row["status"], row.get("review_reason", "")]
            )
        for row in payload["opening_summary"]:
            writer.writerow(
                ["opening_summary", row["code"], "", "", "x".join(row.get("nominal_size", [])), row.get("explicit_count", ""),
                 row["confidence"], row["status"], row["review_reason"]]
            )
        for row in payload["practices"]:
            writer.writerow(["practice", row["code"], row["raw"], row["part"], "", "", row["confidence"], row["status"], row.get("review_reason", "")])
        for row in payload["room_boundaries"]:
            writer.writerow(
                ["room_boundary", row["id"], "、".join(row["rooms"]), "rectangle", "", "", row["confidence"], row["status"], row["review_reason"]]
            )
        for row in payload["wall_segments"]:
            writer.writerow(
                ["wall_segment", row["id"], "、".join(row["rooms"]), row["segment_kind"], "", "", row["confidence"], row["status"], row["review_reason"]]
            )
        for row in payload["openings"]:
            geo = row.get("geometry", {})
            writer.writerow(
                ["opening_geometry", row["code"], geo.get("wall_layer", ""), "、".join(geo.get("room_candidates", [])), "", "",
                 row["confidence"], geo.get("status", ""), geo.get("review_reason", "")]
            )
        for row in payload["ceiling_zones"]:
            elevations = "、".join(
                f"{item['value_m']}{item['unit']}" for item in row.get("elevation_candidates", [])
            )
            writer.writerow(
                [
                    "ceiling_zone", row["id"], "、".join(row["rooms"]), row["zone_kind"], elevations, "",
                    row["confidence"], row["status"], row["review_reason"],
                ]
            )
        for row in payload["stair_ramp_steps"]:
            area = row.get("pending_expanded_area", {})
            area_text = (
                f"{area.get('value')}{area.get('unit')}"
                if area.get("value") is not None
                else area.get("basis", "")
            )
            materials = "、".join(item.get("name", "") for item in row.get("materials", []))
            counts = "、".join(str(v) for v in row.get("count_candidates", []))
            writer.writerow(
                [
                    "stair_ramp_step", row["id"], row["raw"], row["kind"], area_text, counts,
                    row["confidence"], row["status"], row["review_reason"],
                ]
            )
        for row in payload["exterior_wall_zones"]:
            thicknesses = "、".join(
                f"{item.get('value_mm')}mm" for item in row.get("thickness_candidates", [])
            )
            writer.writerow(
                [
                    "exterior_wall_zone", row["id"], row["raw"], row["zone_kind"], thicknesses, "",
                    row["confidence"], row["status"], row["review_reason"],
                ]
            )
        for row in payload["node_detail_index"]:
            writer.writerow(
                ["node_detail", "、".join(row["node_codes"]), "、".join(row["practice_codes"]), "", "", "", row["confidence"], row["status"], row["review_reason"]]
            )
        for row in payload["scale_unit_audit"]:
            writer.writerow(
                ["scale_unit", f"{row['file']}|{row['sheet']}", "", "", "、".join(row["scales"]), "",
                 row["confidence"], row["status"], row["review_reason"]]
            )

def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    parser = argparse.ArgumentParser(description="从 cad_scan 详情 JSON 提取装饰识图中间数据。")
    parser.add_argument("inputs", nargs="+", help="cad_scan 生成的 --detail-json 文件")
    parser.add_argument("--out-dir", default="描述几何", help="输出目录")
    parser.add_argument("--rules", default=str(RULES_PATH), help="规则 JSON")
    args = parser.parse_args()

    rules_path = Path(args.rules)
    rules = load_rules(rules_path)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    outputs = []

    for value in args.inputs:
        src = Path(value)
        if not src.exists():
            raise FileNotFoundError(src)
        payload = analyze_file(src, rules)
        payload = contractize_payload(payload, source=src.name)
        json_path = out_dir / f"{src.stem}.descriptive.json"
        md_path = out_dir / f"{src.stem}.descriptive.md"
        csv_path = out_dir / f"{src.stem}.descriptive.csv"
        json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        write_markdown(payload, md_path)
        write_csv(payload, csv_path)
        outputs += [str(json_path), str(md_path), str(csv_path)]
        print(
            json.dumps(
                {"source": str(src), "summary": payload["summary"], "outputs": [str(json_path), str(md_path), str(csv_path)]},
                ensure_ascii=False,
            )
        )

    if not outputs:
        print("❌无输出失败", file=sys.stderr)
        return 4
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
