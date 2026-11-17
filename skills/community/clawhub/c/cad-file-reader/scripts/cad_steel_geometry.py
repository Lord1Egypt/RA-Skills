#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 cad_scan 详情 JSON 提炼钢结构识图中间数据和证据。

边界：只识别图纸类型、钢结构系统、构件、截面、连接、材料、涂装、节点、
轴网/标高和图层几何证据；不输出重量、面积、长度汇总、材料量、造价或结算量。
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / "packs" / "steel-geometry" / "rules.json"
from cad_contract import contractize_payload

from cad_common import compact, load_rules, segment_length
def data_file_name(data: dict[str, Any], value: Any) -> str:
    if isinstance(value, dict):
        return compact(value.get("name") or value.get("path"))
    files = data.get("files") or []
    if isinstance(value, int) and 0 <= value < len(files):
        item = files[value]
        if isinstance(item, dict):
            return compact(item.get("name") or item.get("path"))
        return compact(item)
    return compact(value)

def evidence_of(record: dict[str, Any]) -> dict[str, Any]:
    ev: dict[str, Any] = {
        "text": compact(record.get("text", "")),
        "layer": record.get("layer"),
        "kind": record.get("kind"),
        "space": record.get("space"),
    }
    if record.get("x") is not None or record.get("y") is not None:
        ev["coord"] = [record.get("x"), record.get("y")]
    for key in ("file", "file_name", "sheet", "handle"):
        if record.get(key) is not None:
            ev[key] = record.get(key)
    return {k: v for k, v in ev.items() if v not in (None, "")}

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
        out.append({
            "text": text,
            "layer": compact(raw.get("layer", "")),
            "kind": compact(raw.get("kind") or raw.get("type", "")),
            "space": raw.get("space"),
            "x": raw.get("x"),
            "y": raw.get("y"),
            "sheet": raw.get("sheet"),
            "file": raw.get("file"),
            "file_name": file_name,
            "handle": raw.get("handle"),
            "_index": i,
        })
    return out

def context_of(record: dict[str, Any]) -> tuple[Any, Any, Any]:
    return (compact(record.get("file_name") or record.get("file")), record.get("sheet"), record.get("space"))

def pattern_hit(value: str, pattern: Any) -> bool:
    token = str(pattern).upper()
    if re.fullmatch(r"[A-Z]{1,3}", token):
        return bool(re.search(rf"(?<![A-Z0-9]){re.escape(token)}(?![A-Z0-9])", value))
    return token in value

def match_rule(text: Any, rules: list[dict[str, Any]], key: str) -> tuple[str, dict[str, Any], str]:
    value = compact(text).upper()
    for rule in rules:
        for pattern in rule.get("patterns") or []:
            if pattern_hit(value, pattern):
                return str(rule.get(key) or ""), rule, str(pattern)
    return "", {}, ""

def sheet_for_point(data: dict[str, Any], x: Any, y: Any) -> Any:
    try:
        px, py = float(x), float(y)
    except (TypeError, ValueError):
        return None
    sheets = ((data.get("meta") or {}).get("sheets")) or data.get("sheets") or []
    for sheet in sheets:
        if not isinstance(sheet, dict):
            continue
        bbox = sheet.get("bbox")
        if not isinstance(bbox, (list, tuple)) or len(bbox) < 4:
            continue
        try:
            x0, y0, x1, y1 = (float(v) for v in bbox[:4])
        except (TypeError, ValueError):
            continue
        if x0 <= px <= x1 and y0 <= py <= y1:
            return sheet.get("id", sheet.get("sheet"))
    return None

def iter_geometry(data: dict[str, Any]):
    segment_files = data.get("geometry_segments") or []
    layer_files = data.get("geometry_layers") or []
    for fi, segments in enumerate(segment_files):
        layers = layer_files[fi] if fi < len(layer_files) else []
        for si, seg in enumerate(segments or []):
            if not isinstance(seg, (list, tuple)) or len(seg) < 4:
                continue
            layer = compact(layers[si]) if si < len(layers) else ""
            yield fi, si, layer, seg

def drawing_type_candidates(records: list[dict[str, Any]], rules: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    for rec in records:
        kind, _rule, pattern = match_rule(rec["text"], rules.get("view_rules") or [], "type")
        if not kind:
            continue
        key = (context_of(rec), kind)
        if key in seen:
            continue
        seen.add(key)
        out.append({
            "type": kind,
            "raw": rec["text"],
            "pattern": pattern,
            "confidence": float((rules.get("confidence") or {}).get("direct_label", 0.95)),
            "status": "candidate",
            "evidence": [evidence_of(rec)],
        })
    return out

def system_candidates(records: list[dict[str, Any]], data: dict[str, Any], rules: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    system_rules = rules.get("system_rules") or []
    for rec in records:
        system, _rule, pattern = match_rule(rec["text"], system_rules, "system")
        if not system:
            continue
        key = (context_of(rec), system, rec.get("layer"), rec["text"])
        if key in seen:
            continue
        seen.add(key)
        out.append({
            "system": system,
            "raw": rec["text"],
            "pattern": pattern,
            "layer": rec.get("layer"),
            "file": rec.get("file_name"),
            "sheet": rec.get("sheet"),
            "confidence": float((rules.get("confidence") or {}).get("pattern_match", 0.78)),
            "status": "candidate",
            "evidence": [evidence_of(rec)],
        })
    for fi, _si, layer, _seg in iter_geometry(data):
        system, _rule, pattern = match_rule(layer, system_rules, "system")
        if not system:
            continue
        file_name = data_file_name(data, fi)
        key = (file_name, None, system, layer)
        if key in seen:
            continue
        seen.add(key)
        out.append({
            "system": system,
            "raw": layer,
            "pattern": pattern,
            "layer": layer,
            "file": file_name,
            "confidence": float((rules.get("confidence") or {}).get("geometry_pattern", 0.86)),
            "status": "candidate",
            "evidence": [{"layer": layer, "file": file_name, "kind": "geometry_layer"}],
        })
    return out

def scale_unit_audit(records: list[dict[str, Any]], rules: dict[str, Any]) -> list[dict[str, Any]]:
    scale_re = re.compile(rules.get("scale_pattern") or r"1\s*[:：]\s*\d{1,4}")
    unit_patterns = rules.get("unit_patterns") or {}
    grouped: dict[tuple[Any, ...], dict[str, Any]] = {}
    for rec in records:
        ctx = context_of(rec)
        item = grouped.setdefault(ctx, {"file": ctx[0], "sheet": ctx[1], "space": ctx[2], "scales": [], "units": [], "evidence": []})
        text = rec["text"]
        for m in scale_re.finditer(text):
            scale = re.sub(r"\s+", "", m.group(0)).replace("：", ":")
            if scale not in item["scales"]:
                item["scales"].append(scale)
        for unit, patterns in unit_patterns.items():
            for pattern in patterns or []:
                if re.search(str(pattern), text, re.I):
                    if unit not in item["units"]:
                        item["units"].append(unit)
                    break
        if item["scales"] or item["units"]:
            item["evidence"].append(evidence_of(rec))
    out: list[dict[str, Any]] = []
    for item in grouped.values():
        missing = []
        if not item["scales"]:
            missing.append("缺图框比例")
        if not item["units"]:
            missing.append("缺图纸单位")
        item["status"] = "candidate" if not missing else "review"
        item["review_reason"] = "；".join(missing)
        item["confidence"] = float((rules.get("confidence") or {}).get("direct_label", 0.95)) if not missing else float((rules.get("confidence") or {}).get("inferred", 0.5))
        out.append(item)
    return out

def member_candidates(records: list[dict[str, Any]], rules: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    code_re = re.compile(rules.get("member_code_pattern") or r"(?<![A-Z0-9])(GZ|GL|GJ|XG|ZC|LT|TL|ML|GS|GC|GG|FHB|JDB)\\s*[-_]?\\s*\\d{1,4}[A-Za-z]?(?![A-Z0-9])", re.I)
    prefixes = {str(k).upper(): v for k, v in (rules.get("member_prefixes") or {}).items()}
    for rec in records:
        text = rec["text"]
        layer = rec.get("layer") or ""
        category, rule, pattern = match_rule(f"{text} {layer}", rules.get("member_rules") or [], "category")
        codes = list(code_re.finditer(text))
        if category:
            name = codes[0].group(0).upper() if codes else text
            key = (context_of(rec), category, name, layer, rec.get("x"), rec.get("y"))
            if key not in seen:
                seen.add(key)
                out.append({
                    "type": "member",
                    "name": name,
                    "code": codes[0].group(0).upper() if codes else "",
                    "category": category,
                    "system": (rule or {}).get("system") or "",
                    "pattern": pattern,
                    "layer": layer,
                    "file": rec.get("file_name"),
                    "sheet": rec.get("sheet"),
                    "x": rec.get("x"),
                    "y": rec.get("y"),
                    "confidence": float((rules.get("confidence") or {}).get("direct_label", 0.95) if rec.get("kind") in {"INSERT", "ATTRIB"} else (rules.get("confidence") or {}).get("pattern_match", 0.78)),
                    "status": "candidate",
                    "review_reason": "",
                    "evidence": [evidence_of(rec)],
                })
        for match in codes:
            code = match.group(0).upper()
            prefix = re.split(r"[-_ ]", code, maxsplit=1)[0]
            mapped = prefixes.get(prefix, "")
            if category and mapped == category:
                continue
            key = (context_of(rec), mapped or "unknown", code, layer, rec.get("x"), rec.get("y"))
            if key in seen:
                continue
            seen.add(key)
            out.append({
                "type": "member",
                "name": code,
                "code": code,
                "category": mapped or "other_steel",
                "system": "",
                "pattern": "member_code",
                "layer": layer,
                "file": rec.get("file_name"),
                "sheet": rec.get("sheet"),
                "x": rec.get("x"),
                "y": rec.get("y"),
                "confidence": float((rules.get("confidence") or {}).get("pattern_match", 0.78)),
                "status": "candidate" if mapped else "review",
                "review_reason": "" if mapped else "构件编号前缀未映射到构件类别",
                "evidence": [evidence_of(rec)],
            })
    return out

def section_candidates(records: list[dict[str, Any]], rules: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    for section_type, patterns in (rules.get("section_patterns") or {}).items():
        for pattern in patterns or []:
            regex = re.compile(str(pattern), re.I)
            for rec in records:
                for match in regex.finditer(rec["text"]):
                    value = compact(match.group(0))
                    key = (context_of(rec), section_type, value, rec.get("layer"), rec.get("x"), rec.get("y"))
                    if key in seen:
                        continue
                    seen.add(key)
                    out.append({
                        "type": "section",
                        "section_type": section_type,
                        "text": value,
                        "layer": rec.get("layer"),
                        "file": rec.get("file_name"),
                        "sheet": rec.get("sheet"),
                        "x": rec.get("x"),
                        "y": rec.get("y"),
                        "confidence": float((rules.get("confidence") or {}).get("direct_label", 0.95)),
                        "status": "candidate",
                        "evidence": [evidence_of(rec)],
                    })
    return out

def connection_candidates(records: list[dict[str, Any]], rules: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    for rec in records:
        category, rule, pattern = match_rule(f"{rec['text']} {rec.get('layer', '')}", rules.get("connection_rules") or [], "category")
        if not category:
            continue
        key = (context_of(rec), category, rec["text"], rec.get("layer"), rec.get("x"), rec.get("y"))
        if key in seen:
            continue
        seen.add(key)
        out.append({
            "type": "connection",
            "category": category,
            "system": (rule or {}).get("system") or "connection",
            "raw": rec["text"],
            "pattern": pattern,
            "layer": rec.get("layer"),
            "file": rec.get("file_name"),
            "sheet": rec.get("sheet"),
            "x": rec.get("x"),
            "y": rec.get("y"),
            "confidence": float((rules.get("confidence") or {}).get("pattern_match", 0.78)),
            "status": "candidate",
            "evidence": [evidence_of(rec)],
        })
    return out

def material_candidates(records: list[dict[str, Any]], rules: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    for grade, patterns in (rules.get("material_patterns") or {}).items():
        for pattern in patterns or []:
            regex = re.compile(str(pattern), re.I)
            for rec in records:
                for match in regex.finditer(rec["text"]):
                    key = (context_of(rec), grade, rec.get("layer"), rec.get("x"), rec.get("y"))
                    if key in seen:
                        continue
                    seen.add(key)
                    out.append({
                        "type": "material",
                        "grade": grade,
                        "raw": compact(match.group(0)),
                        "layer": rec.get("layer"),
                        "file": rec.get("file_name"),
                        "sheet": rec.get("sheet"),
                        "x": rec.get("x"),
                        "y": rec.get("y"),
                        "confidence": float((rules.get("confidence") or {}).get("direct_label", 0.95)),
                        "status": "candidate",
                        "evidence": [evidence_of(rec)],
                    })
    return out

def finish_candidates(records: list[dict[str, Any]], rules: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    for rec in records:
        category, _rule, pattern = match_rule(f"{rec['text']} {rec.get('layer', '')}", rules.get("finish_rules") or [], "category")
        if not category:
            continue
        key = (context_of(rec), category, rec["text"], rec.get("layer"), rec.get("x"), rec.get("y"))
        if key in seen:
            continue
        seen.add(key)
        out.append({
            "type": "finish",
            "category": category,
            "raw": rec["text"],
            "pattern": pattern,
            "layer": rec.get("layer"),
            "file": rec.get("file_name"),
            "sheet": rec.get("sheet"),
            "x": rec.get("x"),
            "y": rec.get("y"),
            "confidence": float((rules.get("confidence") or {}).get("pattern_match", 0.78)),
            "status": "candidate",
            "evidence": [evidence_of(rec)],
        })
    return out

def node_index(records: list[dict[str, Any]], rules: dict[str, Any]) -> list[dict[str, Any]]:
    regex = re.compile(rules.get("node_pattern") or r"(?<![A-Z0-9])(?:JD|NODE|节点|详图)\\s*[-_#]?\\s*\\d{1,4}[A-Za-z]?(?![A-Z0-9])", re.I)
    out: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    for rec in records:
        for match in regex.finditer(rec["text"]):
            node_id = compact(match.group(0)).upper()
            key = (context_of(rec), node_id, rec.get("layer"), rec.get("x"), rec.get("y"))
            if key in seen:
                continue
            seen.add(key)
            out.append({
                "type": "node",
                "id": node_id,
                "raw": rec["text"],
                "layer": rec.get("layer"),
                "file": rec.get("file_name"),
                "sheet": rec.get("sheet"),
                "x": rec.get("x"),
                "y": rec.get("y"),
                "confidence": float((rules.get("confidence") or {}).get("direct_label", 0.95)),
                "status": "candidate",
                "evidence": [evidence_of(rec)],
            })
    return out

def grid_candidates(records: list[dict[str, Any]], rules: dict[str, Any]) -> list[dict[str, Any]]:
    patterns = [
        ("axis", rules.get("axis_pattern") or r"(?<![A-Z0-9])(?:[A-Z]{1,3}|[一二三四五六七八九十]+|\\d{1,3})\\s*(?:轴|轴线)(?![A-Z0-9])"),
        ("elevation", rules.get("elevation_pattern") or r"(?<![A-Z0-9])(?:标高|EL|ELEV|±)\\s*[-+]?\\d+(?:\\.\\d+)?(?![A-Z0-9])"),
    ]
    out: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    for grid_type, pattern in patterns:
        regex = re.compile(str(pattern), re.I)
        for rec in records:
            for match in regex.finditer(rec["text"]):
                value = compact(match.group(0))
                key = (context_of(rec), grid_type, value, rec.get("layer"), rec.get("x"), rec.get("y"))
                if key in seen:
                    continue
                seen.add(key)
                out.append({
                    "type": grid_type,
                    "value": value,
                    "layer": rec.get("layer"),
                    "file": rec.get("file_name"),
                    "sheet": rec.get("sheet"),
                    "x": rec.get("x"),
                    "y": rec.get("y"),
                    "confidence": float((rules.get("confidence") or {}).get("pattern_match", 0.78)),
                    "status": "candidate",
                    "evidence": [evidence_of(rec)],
                })
    return out

def steel_geometry(data: dict[str, Any], rules: dict[str, Any]) -> tuple[list[dict[str, Any]], Counter]:
    out: list[dict[str, Any]] = []
    unmatched: Counter = Counter()
    layer_patterns = [str(x).upper() for x in (rules.get("steel_layer_patterns") or [])]
    for fi, si, layer, seg in iter_geometry(data):
        upper_layer = compact(layer).upper()
        if not layer_patterns or not any(token in upper_layer for token in layer_patterns):
            continue
        category, rule, pattern = match_rule(layer, rules.get("member_rules") or [], "category")
        try:
            x1, y1, x2, y2 = (float(v) for v in seg[:4])
        except (TypeError, ValueError):
            continue
        file_name = data_file_name(data, fi)
        sheet = sheet_for_point(data, (x1 + x2) / 2.0, (y1 + y2) / 2.0)
        status = "candidate" if category else "review"
        out.append({
            "type": "steel_geometry",
            "category": category or "unclassified_steel",
            "system": (rule or {}).get("system") or "",
            "pattern": pattern,
            "layer": layer,
            "file": file_name,
            "file_index": fi,
            "sheet": sheet,
            "geometry": [round(x1, 3), round(y1, 3), round(x2, 3), round(y2, 3)],
            "length_drawing_units": round(segment_length(seg), 3),
            "confidence": float((rules.get("confidence") or {}).get("geometry_pattern", 0.86)),
            "status": status,
            "review_reason": "" if category else "钢构件图层未映射到构件类别",
            "evidence": [{"layer": layer, "kind": "geometry", "coord": [round(x1, 3), round(y1, 3), round(x2, 3), round(y2, 3)], "file": file_name, "sheet": sheet}],
        })
        if not category:
            unmatched[layer or "<空图层>"] += 1
    return out, unmatched

def connectivity_audit(geometry: list[dict[str, Any]], tolerance: float = 5.0, max_segments: int = 5000) -> dict[str, Any]:
    by_context: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in geometry[:max_segments]:
        by_context[(row.get("file"), row.get("sheet"), row.get("layer"))].append(row)
    open_endpoints: list[dict[str, Any]] = []
    junction_candidates: list[dict[str, Any]] = []
    isolated_segments: list[dict[str, Any]] = []
    for (file_name, sheet, layer), rows in by_context.items():
        clusters: dict[tuple[int, int], list[tuple[float, float, int]]] = defaultdict(list)
        for i, row in enumerate(rows):
            geom = row.get("geometry") or []
            if len(geom) < 4:
                continue
            for x, y in ((geom[0], geom[1]), (geom[2], geom[3])):
                key = (round(float(x) / tolerance), round(float(y) / tolerance))
                clusters[key].append((float(x), float(y), i))
        for key, points in clusters.items():
            if len(points) == 1:
                x, y, i = points[0]
                open_endpoints.append({"file": file_name, "sheet": sheet, "layer": layer, "x": x, "y": y, "geometry_index": i, "status": "review", "review_reason": "端点未吸附到同图层钢构件线段"})
            elif len(points) >= 3:
                x, y, _i = points[0]
                junction_candidates.append({"file": file_name, "sheet": sheet, "layer": layer, "x": x, "y": y, "degree": len(points), "status": "candidate", "review_reason": "多端点汇聚，需回图确认连接节点"})
        for i, row in enumerate(rows):
            geom = row.get("geometry") or []
            if len(geom) < 4:
                continue
            endpoints = [
                clusters.get((round(float(geom[0]) / tolerance), round(float(geom[1]) / tolerance)), []),
                clusters.get((round(float(geom[2]) / tolerance), round(float(geom[3]) / tolerance)), []),
            ]
            if len(endpoints[0]) == 1 and len(endpoints[1]) == 1:
                isolated_segments.append({"file": file_name, "sheet": sheet, "layer": layer, "geometry_index": i, "geometry": geom, "status": "review", "review_reason": "两端均未与其他同图层钢构件线段吸附"})
    return {
        "tolerance_drawing_units": tolerance,
        "open_endpoints": open_endpoints[:100],
        "junction_candidates": junction_candidates[:100],
        "isolated_segments": isolated_segments[:100],
        "summary": {
            "open_endpoints": len(open_endpoints),
            "junction_candidates": len(junction_candidates),
            "isolated_segments": len(isolated_segments),
        },
        "boundary": "只做端点吸附和钢构件连通性候选；不输出长度汇总、重量、面积、工程量或材料量。",
    }

def analyze_file(path: Path, rules: dict[str, Any], snap_tolerance: float) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    records = read_records(data)
    views = drawing_type_candidates(records, rules)
    systems = system_candidates(records, data, rules)
    audit = scale_unit_audit(records, rules)
    members = member_candidates(records, rules)
    sections = section_candidates(records, rules)
    connections = connection_candidates(records, rules)
    materials = material_candidates(records, rules)
    finishes = finish_candidates(records, rules)
    nodes = node_index(records, rules)
    grids = grid_candidates(records, rules)
    geometry, unmatched_layers = steel_geometry(data, rules)
    connectivity = connectivity_audit(geometry, snap_tolerance)
    review: list[dict[str, Any]] = []
    if not views:
        review.append({"type": "drawing_type", "reason": "未识别到钢结构图纸类型文字", "evidence": []})
    for row in audit:
        if row.get("status") != "candidate":
            review.append({"type": "scale_unit", "reason": row.get("review_reason") or "比例或单位需确认", "evidence": row.get("evidence", [])})
    if not data.get("geometry_segments") or not data.get("geometry_layers"):
        review.append({"type": "input_geometry", "reason": "输入缺少 geometry_segments 或 geometry_layers；请用 cad_scan --with-geom --with-geom-layer", "evidence": []})
    for layer, count in unmatched_layers.most_common(50):
        review.append({"type": "steel_layer", "reason": f"钢结构图层未分类：{layer}（{count} 段）", "evidence": [{"layer": layer}]})
    if members and not sections:
        review.append({"type": "section_schedule", "reason": "识别到钢构件但未提取到截面规格", "evidence": []})
    if members and not materials:
        review.append({"type": "material_schedule", "reason": "识别到钢构件但未提取到钢材牌号", "evidence": []})
    summary = {
        "drawing_types": len(views),
        "systems": len(systems),
        "members": len(members),
        "sections": len(sections),
        "connections": len(connections),
        "materials": len(materials),
        "finishes": len(finishes),
        "nodes": len(nodes),
        "grids": len(grids),
        "geometry_segments": len(geometry),
        "connectivity_open_endpoints": connectivity["summary"]["open_endpoints"],
        "connectivity_junctions": connectivity["summary"]["junction_candidates"],
        "review_items": len(review),
    }
    return {
        "schema": "cad-steel-geometry/v1",
        "source_file": path.name,
        "summary": summary,
        "drawing_types": views,
        "scale_unit_audit": audit,
        "systems": systems,
        "members": members,
        "sections": sections,
        "connections": connections,
        "materials": materials,
        "finishes": finishes,
        "nodes": nodes,
        "grids": grids,
        "steel_geometry": geometry,
        "connectivity": connectivity,
        "review": review,
        "boundary": "只输出钢结构识图候选、证据和连通性审计；不输出重量、面积、长度汇总、材料量、造价或结算量。",
    }

def write_markdown(payload: dict[str, Any], path: Path) -> None:
    s = payload["summary"]
    lines = [
        "# 钢结构识图 / 中间数据复核",
        "",
        f"- 源文件：`{payload['source_file']}`",
        f"- 候选：图纸类型 {s['drawing_types']}，系统 {s['systems']}，构件 {s['members']}，截面 {s['sections']}，连接 {s['connections']}，材料 {s['materials']}，涂装 {s['finishes']}，节点 {s['nodes']}，轴网/标高 {s['grids']}，几何段 {s['geometry_segments']}，待复核 {s['review_items']}",
        f"- 连通性：开放端点 {s['connectivity_open_endpoints']}，汇聚候选 {s['connectivity_junctions']}",
        "",
        "## 图纸类型",
        "",
    ]
    if payload["drawing_types"]:
        lines += ["| 类型 | 原文 | 置信 | 图层 |", "|---|---|---:|---|"]
        for row in payload["drawing_types"][:80]:
            ev = (row.get("evidence") or [{}])[0]
            lines.append(f"| {row['type']} | {row['raw']} | {row['confidence']:.2f} | {ev.get('layer', '')} |")
    else:
        lines.append("无")
    lines += ["", "## 钢结构系统", ""]
    if payload["systems"]:
        lines += ["| 系统 | 原文/图层 | 图层 | 置信 |", "|---|---|---|---:|"]
        for row in payload["systems"][:120]:
            lines.append(f"| {row['system']} | {row['raw']} | {row.get('layer', '')} | {row['confidence']:.2f} |")
    else:
        lines.append("无")
    lines += ["", "## 构件候选", ""]
    if payload["members"]:
        lines += ["| 名称/编号 | 类别 | 系统 | 图层 | 状态 |", "|---|---|---|---|---|"]
        for row in payload["members"][:120]:
            lines.append(f"| {row['name']} | {row['category']} | {row.get('system', '')} | {row.get('layer', '')} | {row['status']} |")
    else:
        lines.append("无")
    lines += ["", "## 截面候选", ""]
    if payload["sections"]:
        lines += ["| 类型 | 原文 | 图层 |", "|---|---|---|"]
        for row in payload["sections"][:120]:
            lines.append(f"| {row['section_type']} | {row['text']} | {row.get('layer', '')} |")
    else:
        lines.append("无")
    lines += ["", "## 连接候选", ""]
    if payload["connections"]:
        lines += ["| 类别 | 原文 | 图层 |", "|---|---|---|"]
        for row in payload["connections"][:120]:
            lines.append(f"| {row['category']} | {row['raw']} | {row.get('layer', '')} |")
    else:
        lines.append("无")
    lines += ["", "## 材料与涂装", ""]
    if payload["materials"] or payload["finishes"]:
        lines += ["| 类型 | 值 | 图层 |", "|---|---|---|"]
        for row in payload["materials"][:80]:
            lines.append(f"| material | {row['grade']} | {row.get('layer', '')} |")
        for row in payload["finishes"][:80]:
            lines.append(f"| finish | {row['category']} | {row.get('layer', '')} |")
    else:
        lines.append("无")
    lines += ["", "## 节点与轴网", ""]
    if payload["nodes"] or payload["grids"]:
        lines += ["| 类型 | 值 | 图层 |", "|---|---|---|"]
        for row in payload["nodes"][:80]:
            lines.append(f"| node | {row['id']} | {row.get('layer', '')} |")
        for row in payload["grids"][:80]:
            lines.append(f"| {row['type']} | {row['value']} | {row.get('layer', '')} |")
    else:
        lines.append("无")
    lines += ["", "## 待复核", ""]
    if payload["review"]:
        lines += ["| 类型 | 原因 |", "|---|---|"]
        for row in payload["review"][:120]:
            lines.append(f"| {row['type']} | {row['reason']} |")
    else:
        lines.append("无")
    lines += ["", f"> {payload['boundary']}", ""]
    path.write_text("\n".join(lines), encoding="utf-8")

def write_csv(payload: dict[str, Any], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.writer(fh)
        writer.writerow(["row_type", "category", "system", "name", "layer", "file", "sheet", "coordinate", "status", "evidence"])
        for row in payload["drawing_types"]:
            ev = (row.get("evidence") or [{}])[0]
            writer.writerow(["drawing_type", "", "", row["type"], ev.get("layer", ""), ev.get("file_name", ""), ev.get("sheet", ""), ev.get("coord", ""), row["status"], row["raw"]])
        for row in payload["systems"]:
            writer.writerow(["system", "", row["system"], row["raw"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), "", row["status"], row.get("pattern", "")])
        for row in payload["members"]:
            writer.writerow(["member", row["category"], row.get("system", ""), row["name"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{row.get('x')},{row.get('y')}", row["status"], row.get("review_reason", "")])
        for row in payload["sections"]:
            writer.writerow(["section", row["section_type"], "", row["text"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{row.get('x')},{row.get('y')}", row["status"], ""])
        for row in payload["connections"]:
            writer.writerow(["connection", row["category"], row.get("system", ""), row["raw"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{row.get('x')},{row.get('y')}", row["status"], row.get("pattern", "")])
        for row in payload["materials"]:
            writer.writerow(["material", row["grade"], "", row["raw"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{row.get('x')},{row.get('y')}", row["status"], ""])
        for row in payload["finishes"]:
            writer.writerow(["finish", row["category"], "", row["raw"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{row.get('x')},{row.get('y')}", row["status"], row.get("pattern", "")])
        for row in payload["nodes"]:
            writer.writerow(["node", "", "", row["id"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{row.get('x')},{row.get('y')}", row["status"], row.get("raw", "")])
        for row in payload["grids"]:
            writer.writerow([row["type"], "", "", row["value"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{row.get('x')},{row.get('y')}", row["status"], ""])
        for row in payload["steel_geometry"]:
            geom = row["geometry"]
            writer.writerow(["steel_geometry", row["category"], row.get("system", ""), row["category"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{geom[0]},{geom[1]}->{geom[2]},{geom[3]}", row["status"], row.get("review_reason", "")])
        for row in payload["review"]:
            writer.writerow(["review", "", "", row["type"], "", "", "", "", "review", row["reason"]])

def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    parser = argparse.ArgumentParser(description="从 cad_scan 详情 JSON 提取钢结构识图中间数据。")
    parser.add_argument("inputs", nargs="+", help="cad_scan 生成的 --detail-json 文件")
    parser.add_argument("--out-dir", default="钢结构识图", help="输出目录")
    parser.add_argument("--rules", default=str(RULES_PATH), help="钢结构识图规则 JSON")
    parser.add_argument("--snap-tolerance", type=float, default=5.0, help="端点吸附容差，图面单位")
    args = parser.parse_args()

    rules = load_rules(Path(args.rules))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[str] = []
    for value in args.inputs:
        src = Path(value)
        if not src.exists():
            raise FileNotFoundError(src)
        payload = analyze_file(src, rules, args.snap_tolerance)
        payload = contractize_payload(payload, source=src.name)
        json_path = out_dir / f"{src.stem}.steel.json"
        md_path = out_dir / f"{src.stem}.steel.md"
        csv_path = out_dir / f"{src.stem}.steel.csv"
        json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        write_markdown(payload, md_path)
        write_csv(payload, csv_path)
        outputs.extend([str(json_path), str(md_path), str(csv_path)])
        print(json.dumps({"source": str(src), "summary": payload["summary"], "outputs": [str(json_path), str(md_path), str(csv_path)]}, ensure_ascii=False))
    return 0 if outputs else 4

if __name__ == "__main__":
    raise SystemExit(main())
