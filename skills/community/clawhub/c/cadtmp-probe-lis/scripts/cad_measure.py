#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 CAD 识图中间数据生成可追溯的测量候选。

边界：只输出 length / area / volume 识图候选、计算式、比例单位依据和证据；
不输出最终工程量、清单量、材料量、扣减量、损耗、造价或结算量。
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA = "cad-measurement-candidates/v1"
from cad_contract import contractize_payload
TARGET_UNITS = {"length": "m", "area": "m2", "volume": "m3"}
UNIT_ALIASES = {
    "mm": "mm", "毫米": "mm", "cm": "cm", "厘米": "cm", "m": "m", "米": "m",
    "mm2": "mm2", "mm²": "mm2", "平方毫米": "mm2",
    "cm2": "cm2", "cm²": "cm2", "平方厘米": "cm2",
    "m2": "m2", "m²": "m2", "㎡": "m2", "平方米": "m2",
    "mm3": "mm3", "mm³": "mm3", "立方毫米": "mm3",
    "cm3": "cm3", "cm³": "cm3", "立方厘米": "cm3",
    "m3": "m3", "m³": "m3", "立方米": "m3",
}
BASE_UNIT_FACTOR = {"mm": 0.001, "cm": 0.01, "m": 1.0}
KIND_POWER = {"length": 1, "area": 2, "volume": 3}
TEXT_PATTERNS = {
    "length": re.compile(
        r"(?:长度|管长|线长|水平长度|展开长度|L)\s*[:：=]?\s*"
        r"([0-9]+(?:\.[0-9]+)?)\s*(mm|毫米|cm|厘米|m|米)",
        re.I,
    ),
    "area": re.compile(
        r"(?:面积|投影面积|展开面积|S)\s*[:：=]?\s*"
        r"([0-9]+(?:\.[0-9]+)?)\s*(mm2|mm²|平方毫米|cm2|cm²|平方厘米|m2|m²|㎡|平方米)",
        re.I,
    ),
    "volume": re.compile(
        r"(?:体积|方量|V)\s*[:：=]?\s*"
        r"([0-9]+(?:\.[0-9]+)?)\s*(mm3|mm³|立方毫米|cm3|cm³|立方厘米|m3|m³|立方米)",
        re.I,
    ),
}


def norm_unit(value: Any) -> str:
    text = str(value or "").strip().lower().replace(" ", "")
    return UNIT_ALIASES.get(text, "")


def unit_factor(kind: str, unit: str) -> float | None:
    normalized = norm_unit(unit)
    if not normalized:
        return None
    if kind == "length":
        return BASE_UNIT_FACTOR.get(normalized)
    if kind == "area":
        if normalized in BASE_UNIT_FACTOR:
            return BASE_UNIT_FACTOR[normalized] ** 2
        if normalized in {"mm2", "cm2", "m2"}:
            base = normalized[:-1]
            factor = BASE_UNIT_FACTOR.get(base)
            return factor ** 2 if factor is not None else None
        return None
    if kind == "volume":
        if normalized in BASE_UNIT_FACTOR:
            return BASE_UNIT_FACTOR[normalized] ** 3
        if normalized in {"mm3", "cm3", "m3"}:
            base = normalized[:-1]
            factor = BASE_UNIT_FACTOR.get(base)
            return factor ** 3 if factor is not None else None
        return None
    return None


def parse_scale(value: Any) -> float | None:
    text = str(value or "").strip().replace("：", ":")
    match = re.search(r"1\s*:\s*([0-9]+(?:\.[0-9]+)?)", text)
    if match:
        try:
            result = float(match.group(1))
            return result if result > 0 else None
        except ValueError:
            return None
    match = re.search(r"([0-9]+(?:\.[0-9]+)?)", text)
    if not match:
        return None
    try:
        result = float(match.group(1))
        return result if result > 0 else None
    except ValueError:
        return None


def number(value: Any) -> float | None:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def round_value(value: float | None, digits: int = 6) -> float | None:
    return None if value is None else round(value, digits)


def segment_length(segment: Any) -> float | None:
    if not isinstance(segment, (list, tuple)) or len(segment) < 4:
        return None
    values = [number(value) for value in segment[:4]]
    if any(value is None for value in values):
        return None
    return math.hypot(values[2] - values[0], values[3] - values[1])


def polygon_area(polygon: Any) -> float | None:
    if not isinstance(polygon, (list, tuple)) or len(polygon) < 3:
        return None
    points: list[tuple[float, float]] = []
    for point in polygon:
        if not isinstance(point, (list, tuple)) or len(point) < 2:
            return None
        x, y = number(point[0]), number(point[1])
        if x is None or y is None:
            return None
        points.append((x, y))
    area = 0.0
    for index, (x1, y1) in enumerate(points):
        x2, y2 = points[(index + 1) % len(points)]
        area += x1 * y2 - x2 * y1
    return abs(area) / 2.0


def bbox_area(bbox: Any) -> float | None:
    if not isinstance(bbox, (list, tuple)) or len(bbox) < 4:
        return None
    values = [number(value) for value in bbox[:4]]
    if any(value is None for value in values):
        return None
    return abs((values[2] - values[0]) * (values[3] - values[1]))


def source_file(payload: dict[str, Any], fallback: Path) -> str:
    return str(payload.get("source_file") or fallback.name)


def evidence_from(row: dict[str, Any], fallback: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    evidence = row.get("evidence")
    if isinstance(evidence, list) and evidence:
        return evidence[:20]
    item: dict[str, Any] = {}
    if fallback:
        item.update({key: value for key, value in fallback.items() if value not in (None, "", [])})
    for key in ("file", "file_name", "sheet", "layer", "coord", "segment", "geometry", "raw", "text"):
        if row.get(key) not in (None, "", []):
            item[key] = row.get(key)
    return [item] if item else []


def context_rows(payload: dict[str, Any], fallback: Path) -> list[dict[str, Any]]:
    rows = payload.get("scale_unit_audit")
    if not isinstance(rows, list):
        return []
    out = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        copied = dict(row)
        copied.setdefault("file", source_file(payload, fallback))
        out.append(copied)
    return out


def resolve_context(
    payload: dict[str, Any],
    fallback: Path,
    file_name: str,
    sheet: Any,
    args: argparse.Namespace,
) -> dict[str, Any]:
    rows = context_rows(payload, fallback)
    matching = [
        row for row in rows
        if (not file_name or not row.get("file") or str(row.get("file")) == str(file_name))
        and (sheet is None or row.get("sheet") is None or row.get("sheet") == sheet)
    ]
    if not matching and len(rows) == 1:
        matching = rows
    row = matching[0] if matching else {}
    scales = [str(value) for value in (row.get("scales") or []) if str(value).strip()]
    units = [str(value) for value in (row.get("units") or []) if str(value).strip()]
    spaces = [str(value) for value in (row.get("spaces") or []) if str(value).strip()]
    scale = parse_scale(args.scale) or (parse_scale(scales[0]) if len(scales) == 1 else None)
    unit = norm_unit(args.unit) or (norm_unit(units[0]) if len(units) == 1 else "")
    space = str(args.coordinate_space if args.coordinate_space != "auto" else (spaces[0] if len(spaces) == 1 else "model"))
    reasons: list[str] = []
    if not scale:
        reasons.append("缺比例或比例冲突" if len(scales) > 1 else "缺比例")
    if not unit:
        reasons.append("缺单位或单位冲突" if len(units) > 1 else "缺单位")
    if len(matching) > 1:
        reasons.append("同文件/图框存在多个比例单位上下文")
    if args.coordinate_space == "auto" and len(spaces) > 1:
        reasons.append("空间归属冲突")
    return {
        "scale": scale,
        "scale_label": f"1:{scale:g}" if scale else "",
        "unit": unit,
        "space": space,
        "context_status": "review" if reasons else "candidate",
        "review_reason": "；".join(dict.fromkeys(reasons)),
        "source_context": row,
    }


def convert_drawing_value(value: float | None, kind: str, context: dict[str, Any]) -> tuple[float | None, bool, str]:
    if value is None:
        return None, False, "无图面数值"
    factor = unit_factor(kind, context.get("unit", ""))
    if factor is None:
        return None, False, "单位未明确，保留图面数值"
    scale = context.get("scale")
    space = str(context.get("space") or "model").lower()
    apply_scale = space in {"paper", "layout", "图纸空间", "布局"} and scale is not None
    real = value * factor
    if apply_scale:
        real *= float(scale) ** KIND_POWER[kind]
    unit_text = context.get("unit") or ""
    if kind == "area" and unit_text:
        unit_text += "²"
    elif kind == "volume" and unit_text:
        unit_text += "³"
    formula = f"{value:g} {unit_text}"
    if apply_scale:
        formula += f" × 1:{scale:g} 比例"
    formula += f" = {real:g} {TARGET_UNITS[kind]}"
    return real, apply_scale, formula


def make_measurement(
    kind: str,
    source_path: Path,
    source_schema: str,
    source_id: str,
    basis: str,
    method: str,
    *,
    value_drawing: float | None = None,
    explicit_value: float | None = None,
    explicit_unit: str = "",
    context: dict[str, Any] | None = None,
    source_status: str = "candidate",
    confidence: str = "medium",
    review_reason: str = "",
    evidence: list[dict[str, Any]] | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    context = context or {"scale": None, "scale_label": "", "unit": "", "space": "model", "context_status": "review", "review_reason": "缺比例和单位"}
    reasons = []
    if explicit_value is not None:
        factor = unit_factor(kind, explicit_unit)
        value = explicit_value * factor if factor is not None else None
        formula = f"原文 {explicit_value:g} {explicit_unit}"
        if value is not None:
            formula += f" = {value:g} {TARGET_UNITS[kind]}"
        if value is None:
            reasons.append("原文测量单位无法换算")
        status = "candidate" if value is not None else "review"
        drawing_value = explicit_value
        drawing_unit = explicit_unit
        scale_applied = False
    else:
        value, scale_applied, formula = convert_drawing_value(value_drawing, kind, context)
        drawing_value = value_drawing
        drawing_unit = context.get("unit") or ""
        status = "candidate" if value is not None else "review"
        if context.get("context_status") != "candidate":
            reasons.append(str(context.get("review_reason") or "比例或单位需确认"))
    if source_status != "candidate":
        status = "review"
    if basis in {"bbox", "bbox_area"}:
        status = "review"
        reasons.append("外接框面积不是净面积，只能作定位证据")
    if review_reason:
        reasons.append(review_reason)
    item = {
        "id": f"measure-{source_path.stem}-{kind}-{len(str(source_id))}-{source_id or 'item'}",
        "kind": kind,
        "value": round_value(value),
        "unit": TARGET_UNITS[kind],
        "value_drawing_units": round_value(drawing_value),
        "drawing_unit": drawing_unit,
        "scale": context.get("scale_label") or "",
        "space": context.get("space") or "",
        "scale_applied": scale_applied,
        "basis": basis,
        "method": method,
        "formula": formula,
        "status": status,
        "confidence": confidence,
        "review_reason": "；".join(dict.fromkeys(reasons)),
        "final_quantity": False,
        "source_schema": source_schema,
        "source_file": str(source_path),
        "source_id": source_id,
        "evidence": evidence or [],
    }
    if extra:
        item.update(extra)
    return item


def add_length_from_geometry(
    out: list[dict[str, Any]], source_path: Path, schema: str, row: dict[str, Any], geometry: Any,
    context: dict[str, Any], *, source_status: str = "candidate", basis: str = "segment",
    method: str = "segment_sum", review_reason: str = "", confidence: str = "medium",
) -> None:
    length = number(row.get("length_drawing_units"))
    if length is None:
        length = segment_length(geometry)
    if length is None:
        return
    out.append(make_measurement(
        "length", source_path, schema, str(row.get("id") or row.get("component_id") or "segment"),
        basis, method, value_drawing=length, context=context, source_status=source_status,
        confidence=confidence, review_reason=review_reason,
        evidence=evidence_from(row, {"geometry": geometry}), extra={"source_geometry": geometry},
    ))


def extract_descriptive(payload: dict[str, Any], source_path: Path, args: argparse.Namespace, out: list[dict[str, Any]]) -> None:
    schema = str(payload.get("schema") or "cad-descriptive-geometry")
    for row in payload.get("room_boundaries") or []:
        if not isinstance(row, dict):
            continue
        context = resolve_context(payload, source_path, str(row.get("file") or ""), row.get("sheet"), args)
        area = polygon_area(row.get("polygon"))
        if area is not None:
            out.append(make_measurement(
                "area", source_path, schema, str(row.get("id") or "room-boundary"), "polygon", "shoelace",
                value_drawing=area, context=context, source_status=str(row.get("status") or "review"),
                confidence="high" if row.get("status") == "candidate" else "medium",
                review_reason=str(row.get("review_reason") or ""),
                evidence=evidence_from(row, {"file": row.get("file"), "sheet": row.get("sheet"), "polygon": row.get("polygon")}),
                extra={"rooms": row.get("rooms") or [], "source_geometry": row.get("polygon")},
            ))
    for row in payload.get("wall_segments") or []:
        if not isinstance(row, dict):
            continue
        context = resolve_context(payload, source_path, str(row.get("file") or ""), row.get("sheet"), args)
        add_length_from_geometry(
            out, source_path, schema, row, row.get("segment"), context,
            source_status=str(row.get("status") or "review"), basis="wall_segment",
            method="segment_sum", review_reason="墙段长度候选；未扣门窗洞口侧壁和构造口径",
            confidence="medium",
        )
    for row in payload.get("ceiling_zones") or []:
        if not isinstance(row, dict):
            continue
        context = resolve_context(payload, source_path, str(row.get("file") or ""), row.get("sheet"), args)
        area = polygon_area(row.get("polygon"))
        if area is not None:
            out.append(make_measurement(
                "area", source_path, schema, str(row.get("id") or "ceiling-zone"), "polygon", "shoelace",
                value_drawing=area, context=context, source_status=str(row.get("status") or "review"),
                confidence="medium", review_reason="顶棚分区面积候选；未扣灯具、检修口、梁侧和造型",
                evidence=evidence_from(row, {"file": row.get("file"), "sheet": row.get("sheet"), "polygon": row.get("polygon")}),
                extra={"rooms": row.get("rooms") or [], "zone_kind": row.get("zone_kind"), "source_geometry": row.get("polygon")},
            ))
    for row in payload.get("stair_ramp_steps") or []:
        if not isinstance(row, dict):
            continue
        context = resolve_context(payload, source_path, str(row.get("file") or ""), row.get("sheet"), args)
        for area_row in row.get("area_candidates") or []:
            if not isinstance(area_row, dict):
                continue
            explicit = number(area_row.get("value"))
            unit = str(area_row.get("unit") or "m2")
            out.append(make_measurement(
                "area", source_path, schema, str(row.get("id") or "stair-ramp-step"),
                str(area_row.get("basis") or "explicit_area"), "explicit_text",
                explicit_value=explicit, explicit_unit=unit, source_status="review", confidence="medium",
                review_reason="楼梯/坡道/台阶只作待确认初稿；展开面积和分项材料需人工确认",
                evidence=evidence_from(area_row, {"raw": area_row.get("raw")}),
                extra={"source_geometry": row.get("geometry")},
            ))
        geometry = row.get("geometry") if isinstance(row.get("geometry"), dict) else {}
        area = number(geometry.get("bbox_area_drawing_units2"))
        if area is None:
            area = bbox_area(geometry.get("bbox"))
        if area is not None:
            out.append(make_measurement(
                "area", source_path, schema, str(row.get("id") or "stair-ramp-step"), "bbox", "bbox_area",
                value_drawing=area, context=context, source_status="review", confidence="low",
                review_reason="仅楼梯/坡道/台阶外接框，不是净面积",
                evidence=evidence_from(row, {"file": row.get("file"), "sheet": row.get("sheet"), "geometry": geometry}),
                extra={"source_geometry": geometry},
            ))
    for row in payload.get("exterior_wall_zones") or []:
        if not isinstance(row, dict):
            continue
        geometry = row.get("geometry") if isinstance(row.get("geometry"), dict) else {}
        context = resolve_context(payload, source_path, str(row.get("file") or ""), row.get("sheet"), args)
        length = number(geometry.get("total_length_drawing_units"))
        if length is not None:
            out.append(make_measurement(
                "length", source_path, schema, str(row.get("id") or "exterior-wall-zone"),
                "layer_segment_sum", "segment_sum", value_drawing=length, context=context,
                source_status="review", confidence="low",
                review_reason="外墙/保温分区线段合计只作识图证据，未做立面和保温范围展开",
                evidence=evidence_from(row, {"file": row.get("file"), "sheet": row.get("sheet"), "geometry": geometry}),
                extra={"zone_kind": row.get("zone_kind"), "source_geometry": geometry},
            ))


def extract_professional(payload: dict[str, Any], source_path: Path, args: argparse.Namespace, out: list[dict[str, Any]]) -> None:
    schema = str(payload.get("schema") or "")
    if schema.startswith("cad-mep-geometry"):
        for row in payload.get("route_segments") or []:
            if not isinstance(row, dict):
                continue
            context = resolve_context(payload, source_path, str(row.get("file") or ""), row.get("sheet"), args)
            add_length_from_geometry(
                out, source_path, schema, row, row.get("geometry"), context,
                source_status="review", basis="route_segment", method="segment_sum",
                review_reason="单段路由长度只作识图证据；未做回路规格匹配、竖向路由和最终管长",
                confidence="medium",
            )
    elif schema.startswith("cad-steel-geometry"):
        for row in payload.get("steel_geometry") or []:
            if not isinstance(row, dict):
                continue
            context = resolve_context(payload, source_path, str(row.get("file") or ""), row.get("sheet"), args)
            add_length_from_geometry(
                out, source_path, schema, row, row.get("geometry"), context,
                source_status="review", basis="member_segment", method="segment_sum",
                review_reason="单段钢构件几何长度只作识图证据；未做构件长度汇总、重量或节点计算",
                confidence="medium",
            )
    elif schema.startswith("cad-municipal-geometry"):
        for row in payload.get("municipal_geometry") or []:
            if not isinstance(row, dict):
                continue
            context = resolve_context(payload, source_path, str(row.get("file") or ""), row.get("sheet"), args)
            add_length_from_geometry(
                out, source_path, schema, row, row.get("geometry"), context,
                source_status="review", basis="municipal_segment", method="segment_sum",
                review_reason="单段市政几何长度只作识图证据；未做道路、管道或构件最终长度",
                confidence="medium",
            )


def iter_text_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    records = payload.get("text_records")
    if isinstance(records, list):
        rows.extend(row for row in records if isinstance(row, dict))
    for key in ("rooms", "room_schedules", "labels", "components", "members"):
        values = payload.get(key)
        if isinstance(values, dict):
            values = list(values.values())
        if not isinstance(values, list):
            continue
        for row in values:
            if not isinstance(row, dict):
                continue
            text = row.get("raw") or row.get("text")
            if text:
                copied = dict(row)
                copied["text"] = str(text)
                rows.append(copied)
    return rows


def extract_explicit_text(payload: dict[str, Any], source_path: Path, out: list[dict[str, Any]]) -> None:
    schema = str(payload.get("schema") or "cad-scan-detail")
    seen: set[tuple[str, str, str]] = set()
    for row in iter_text_rows(payload):
        text = str(row.get("text") or "")
        for kind, pattern in TEXT_PATTERNS.items():
            for match in pattern.finditer(text):
                raw = match.group(0)
                value = number(match.group(1))
                unit = norm_unit(match.group(2))
                if value is None or not unit:
                    continue
                key = (kind, raw, str(row.get("layer") or ""))
                if key in seen:
                    continue
                seen.add(key)
                out.append(make_measurement(
                    kind, source_path, schema, str(row.get("id") or row.get("code") or row.get("layer") or "text"),
                    "explicit_text", "explicit_text", explicit_value=value, explicit_unit=unit,
                    source_status="candidate", confidence="high",
                    review_reason="原文显式测量值；仍需按专项口径核对扣减、范围和计算规则",
                    evidence=evidence_from(row, {"raw": text}),
                    extra={"raw": raw, "source_text": text},
                ))


def add_volume_candidates(payloads: list[tuple[dict[str, Any], Path]], out: list[dict[str, Any]], thickness: float | None, height: float | None) -> None:
    if thickness is None and height is None:
        return
    thickness_or_height = thickness if thickness is not None else height
    if not thickness_or_height or thickness_or_height <= 0:
        return
    basis = "area_x_thickness" if thickness is not None else "area_x_height"
    for item in list(out):
        if item.get("kind") != "area" or item.get("value") is None:
            continue
        value = float(item["value"]) * thickness_or_height
        out.append({
            "id": f"{item['id']}-volume",
            "kind": "volume",
            "value": round_value(value),
            "unit": "m3",
            "value_drawing_units": None,
            "drawing_unit": "",
            "scale": item.get("scale", ""),
            "space": item.get("space", ""),
            "scale_applied": False,
            "basis": basis,
            "method": "area_times_explicit_parameter",
            "formula": f"{item['value']:g} m2 × {thickness_or_height:g} m = {value:g} m3",
            "status": "review",
            "confidence": "low",
            "review_reason": "仅按显式面积×厚度/高度生成几何体积候选；未做洞口、构件相交、降板、做法和损耗",
            "final_quantity": False,
            "source_schema": item.get("source_schema", ""),
            "source_file": item.get("source_file", ""),
            "source_id": item.get("source_id", ""),
            "evidence": item.get("evidence", []),
        })


def analyze(inputs: list[Path], args: argparse.Namespace) -> dict[str, Any]:
    measurements: list[dict[str, Any]] = []
    inputs_meta: list[dict[str, Any]] = []
    for path in inputs:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError(f"{path} 不是 JSON 对象")
        schema = str(payload.get("schema") or "cad-scan-detail")
        inputs_meta.append({"path": str(path), "schema": schema, "summary": payload.get("summary") or {}})
        extract_explicit_text(payload, path, measurements)
        if schema.startswith("cad-descriptive-geometry"):
            extract_descriptive(payload, path, args, measurements)
        elif schema.startswith(("cad-mep-geometry", "cad-steel-geometry", "cad-municipal-geometry")):
            extract_professional(payload, path, args, measurements)
        elif isinstance(payload.get("members"), dict):
            for category, members in payload["members"].items():
                if not isinstance(members, dict):
                    continue
                for code, row in members.items():
                    if not isinstance(row, dict) or number(row.get("len_mm")) is None:
                        continue
                    context = resolve_context(payload, path, "", None, args)
                    measurements.append(make_measurement(
                        "length", path, schema, str(code), "beam_line_candidate", "segment_sum",
                        value_drawing=number(row.get("len_mm")), context=context,
                        source_status="review", confidence="low",
                        review_reason=f"{category}线候选长度只作图面证据；未做支座净跨、扣减或最终工程量",
                        evidence=[{"code": code, "file": row.get("file"), "layer": row.get("layer")}],
                        extra={"member_category": category, "member_code": code},
                    ))
    add_volume_candidates([(item, Path(item["source_file"])) for item in measurements if item.get("source_file")], measurements, args.thickness_m, args.height_m)
    review = [
        {
            "id": item["id"],
            "kind": item["kind"],
            "source_id": item["source_id"],
            "review_reason": item["review_reason"],
            "evidence": item.get("evidence", [])[:1],
        }
        for item in measurements if item.get("status") != "candidate"
    ]
    summary = {
        "measurements": len(measurements),
        "length_candidates": sum(1 for item in measurements if item.get("kind") == "length"),
        "area_candidates": sum(1 for item in measurements if item.get("kind") == "area"),
        "volume_candidates": sum(1 for item in measurements if item.get("kind") == "volume"),
        "candidate": sum(1 for item in measurements if item.get("status") == "candidate"),
        "review": sum(1 for item in measurements if item.get("status") == "review"),
        "explicit_text": sum(1 for item in measurements if item.get("basis") == "explicit_text"),
        "final_quantities": 0,
    }
    return {
        "schema": SCHEMA,
        "source_files": [str(path) for path in inputs],
        "inputs": inputs_meta,
        "summary": summary,
        "measurements": measurements,
        "review": review,
        "boundary": "只输出长度/面积/体积识图候选值、计算式、比例单位依据和证据；final_quantity=false。扣减、重叠、做法、损耗、分账、清单量、材料量和结算量由专项算量 skill 负责。",
    }


def write_markdown(payload: dict[str, Any], path: Path) -> None:
    summary = payload["summary"]
    lines = [
        "# CAD 测量候选复核",
        "",
        f"- 输入：{len(payload['source_files'])} 个 JSON",
        f"- 候选：长度 {summary['length_candidates']}，面积 {summary['area_candidates']}，体积 {summary['volume_candidates']}，待复核 {summary['review']}",
        f"- 边界：{payload['boundary']}",
        "",
        "## 测量候选",
        "",
        "| 编号 | 类型 | 值 | 图面值 | 单位/比例 | 依据 | 状态 | 待复核 |",
        "|---|---|---:|---:|---|---|---|---|",
    ]
    for item in payload["measurements"][:200]:
        lines.append(
            f"| {item['id']} | {item['kind']} | {item['value'] if item['value'] is not None else '—'} | "
            f"{item['value_drawing_units'] if item['value_drawing_units'] is not None else '—'} | "
            f"{item['unit']} {item['scale']} | {item['basis']}/{item['method']} | {item['status']} | {item['review_reason']} |"
        )
    lines += ["", "## 复核项", ""]
    for item in payload["review"][:200]:
        lines.append(f"- `{item['id']}`：{item['review_reason']}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_csv(payload: dict[str, Any], path: Path) -> None:
    fields = ["id", "kind", "value", "unit", "value_drawing_units", "drawing_unit", "scale", "space", "scale_applied", "basis", "method", "formula", "status", "confidence", "review_reason", "final_quantity", "source_schema", "source_file", "source_id"]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for item in payload["measurements"]:
            writer.writerow({key: item.get(key, "") for key in fields})


def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    parser = argparse.ArgumentParser(description="从 CAD 识图 JSON 生成长度/面积/体积测量候选；不输出最终工程量。")
    parser.add_argument("inputs", nargs="+", help="cad_scan detail 或 descriptive/mep/steel/municipal JSON")
    parser.add_argument("--out-dir", default="测量候选", help="输出目录")
    parser.add_argument("--scale", default=None, help="覆盖比例，例如 1:100")
    parser.add_argument("--unit", choices=["mm", "cm", "m"], default=None, help="覆盖图面坐标单位")
    parser.add_argument("--coordinate-space", choices=["auto", "model", "paper"], default="auto", help="auto 按 audit 的 spaces；paper 才应用图框比例")
    parser.add_argument("--thickness-m", type=float, default=None, help="面积候选×显式厚度生成体积候选（只作待复核）")
    parser.add_argument("--height-m", type=float, default=None, help="面积候选×显式高度生成体积候选（只作待复核）")
    args = parser.parse_args()
    inputs = [Path(value).expanduser().resolve() for value in args.inputs]
    for path in inputs:
        if not path.exists():
            print(f"❌输入不存在：{path}", file=sys.stderr)
            return 2
    payload = analyze(inputs, args)
    payload = contractize_payload(payload, source=[Path(v).name for v in payload.get("source_files", [])])
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "cad-measurement-candidates.json"
    md_path = out_dir / "cad-measurement-candidates.md"
    csv_path = out_dir / "cad-measurement-candidates.csv"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(payload, md_path)
    write_csv(payload, csv_path)
    print(json.dumps({"schema": SCHEMA, "summary": payload["summary"], "outputs": [str(json_path), str(md_path), str(csv_path)]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
