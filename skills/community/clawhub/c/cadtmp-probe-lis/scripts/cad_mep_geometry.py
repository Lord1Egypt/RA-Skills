#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 cad_scan 详情 JSON 提炼安装专业识图中间数据和证据。

边界：只识别图纸对象、系统、路由、设备、文字标注和连通性候选；
不输出工程量、材料量、损耗、造价或结算量。
"""
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
RULES_PATH = ROOT / "packs" / "mep-geometry" / "rules.json"
from cad_contract import contractize_payload

from cad_common import compact, load_rules, pattern_hit, match_rule, segment_length
def data_file_name(data: dict[str, Any], value: Any) -> str:
    """把 cad_scan 的文件索引还原为文件名。"""
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
        out.append(
            {
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
            }
        )
    return out

def context_of(record: dict[str, Any]) -> tuple[str, Any, Any]:
    return (
        compact(record.get("file_name") or record.get("file")),
        record.get("sheet"),
        record.get("space"),
    )

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

def match_view(text: str, rules: dict[str, Any]) -> tuple[str, float, str]:
    kind, _rule, pattern = match_rule(text, rules.get("view_rules") or [], "type")
    confidence = float((rules.get("confidence") or {}).get("direct_label", 0.95))
    return kind, confidence, pattern

def drawing_type_candidates(records: list[dict[str, Any]], rules: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    for rec in records:
        kind, confidence, pattern = match_view(rec["text"], rules)
        if not kind:
            continue
        key = (context_of(rec), kind)
        if key in seen:
            continue
        seen.add(key)
        out.append(
            {
                "type": kind,
                "raw": rec["text"],
                "pattern": pattern,
                "confidence": confidence,
                "status": "candidate",
                "evidence": [evidence_of(rec)],
            }
        )
    return out

def scale_unit_audit(records: list[dict[str, Any]], rules: dict[str, Any]) -> list[dict[str, Any]]:
    scale_re = re.compile(rules.get("scale_pattern") or r"1\s*[:：]\s*\d{1,4}")
    unit_patterns = rules.get("unit_patterns") or {}
    grouped: dict[tuple[Any, ...], dict[str, Any]] = {}
    for rec in records:
        ctx = context_of(rec)
        item = grouped.setdefault(
            ctx,
            {"file": ctx[0], "sheet": ctx[1], "space": ctx[2], "scales": [], "units": [], "evidence": []},
        )
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

def system_candidates(
    records: list[dict[str, Any]], data: dict[str, Any], rules: dict[str, Any]
) -> list[dict[str, Any]]:
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
        out.append(
            {
                "system": system,
                "raw": rec["text"],
                "pattern": pattern,
                "layer": rec.get("layer"),
                "confidence": float((rules.get("confidence") or {}).get("pattern_match", 0.78)),
                "status": "candidate",
                "evidence": [evidence_of(rec)],
            }
        )
    for fi, si, layer, _seg in iter_geometry(data):
        system, _rule, pattern = match_rule(layer, system_rules, "system")
        if not system:
            continue
        file_name = data_file_name(data, fi)
        key = (file_name, None, system, layer)
        if key in seen:
            continue
        seen.add(key)
        out.append(
            {
                "system": system,
                "raw": layer,
                "pattern": pattern,
                "layer": layer,
                "file": file_name,
                "confidence": float((rules.get("confidence") or {}).get("geometry_pattern", 0.86)),
                "status": "candidate",
                "evidence": [{"layer": layer, "file": file_name, "kind": "geometry_layer"}],
            }
        )
    return out

def point_segment_distance(px: Any, py: Any, seg: list[Any] | tuple[Any, ...]) -> float | None:
    """点到图面线段的距离；只作证据关联，不换算实际长度。"""
    try:
        x1, y1, x2, y2 = (float(v) for v in seg[:4])
        x, y = float(px), float(py)
    except (TypeError, ValueError):
        return None
    dx, dy = x2 - x1, y2 - y1
    denom = dx * dx + dy * dy
    if denom <= 1e-12:
        return math.hypot(x - x1, y - y1)
    t = max(0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / denom))
    return math.hypot(x - (x1 + t * dx), y - (y1 + t * dy))

def extract_riser_labels(records: list[dict[str, Any]], rules: dict[str, Any]) -> list[tuple[dict[str, Any], str, str]]:
    pattern = re.compile(rules.get("riser_id_pattern") or r"(?<![A-Za-z0-9])(JL|PL|WL|YL|HL|RL)[-_]?\d+", re.I)
    prefix_system = {
        "HYL": "drainage", "SPL": "fire_water", "JL": "water_supply", "PL": "drainage",
        "TL": "drainage", "FL": "drainage", "WL": "drainage", "YL": "drainage",
        "HL": "water_supply", "RL": "water_supply", "JFL": "fire_water", "WFL": "fire_water",
    }
    out: list[tuple[dict[str, Any], str, str]] = []
    for rec in records:
        for match in pattern.finditer(rec["text"]):
            rid = match.group(0).upper()
            prefix = re.split(r"[-_ ]", rid, maxsplit=1)[0].upper()
            out.append((rec, rid, prefix_system.get(prefix, "")))
    return out

def vertical_direction(text: Any, rules: dict[str, Any]) -> str:
    value = compact(text).upper()
    for direction, patterns in (rules.get("vertical_direction_patterns") or {}).items():
        for pattern in patterns or []:
            if str(pattern).upper() in value:
                return direction
    return "unspecified"

def same_sheet(a: Any, b: Any) -> bool:
    return a is None or b is None or a == b

def vertical_route_candidates(
    records: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    data: dict[str, Any],
    rules: dict[str, Any],
    link_tolerance: float = 2000.0,
) -> list[dict[str, Any]]:
    """把立管编号/竖向文字关联到同文件、同图框的最近路由段。

    只输出关联候选和距离证据；不推导立管实际长度、层高或工程量。
    """
    out: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    for rec, rid, system in extract_riser_labels(records, rules):
        candidates: list[tuple[float, int, dict[str, Any]]] = []
        for idx, row in enumerate(routes):
            if (row.get("file") or "") != (rec.get("file_name") or ""):
                continue
            if not same_sheet(row.get("sheet"), rec.get("sheet")):
                continue
            geom = row.get("geometry") or []
            if len(geom) < 4:
                continue
            dist = point_segment_distance(rec.get("x"), rec.get("y"), geom)
            if dist is not None:
                candidates.append((dist, idx, row))
        if not candidates:
            key = (rec.get("file_name"), rec.get("sheet"), rid, None)
            if key not in seen:
                seen.add(key)
                out.append({
                    "type": "vertical_route",
                    "id": rid,
                    "system": system,
                    "route_class": "",
                    "file": rec.get("file_name"),
                    "sheet": rec.get("sheet"),
                    "x": rec.get("x"),
                    "y": rec.get("y"),
                    "direction": vertical_direction(rec.get("text", ""), rules),
                    "link_distance_drawing_units": None,
                    "status": "review",
                    "review_reason": "未找到同文件/图框的可关联路由段",
                    "evidence": [evidence_of(rec)],
                })
            continue
        same_system = [item for item in candidates if system and item[2].get("system") == system]
        pool = same_system or candidates
        dist, idx, row = min(pool, key=lambda item: item[0])
        reasons: list[str] = []
        if system and row.get("system") and row.get("system") != system:
            reasons.append("路由系统与立管系统不一致")
        if dist > link_tolerance:
            reasons.append("标注与路由距离超出关联容差")
        if row.get("sheet") is None or rec.get("sheet") is None:
            reasons.append("图框信息不完整")
        key = (rec.get("file_name"), rec.get("sheet"), rid, idx)
        if key in seen:
            continue
        seen.add(key)
        out.append({
            "type": "vertical_route",
            "id": rid,
            "system": system,
            "route_class": row.get("route_class") or "",
            "route_index": idx,
            "layer": rec.get("layer"),
            "file": rec.get("file_name"),
            "sheet": rec.get("sheet"),
            "x": rec.get("x"),
            "y": rec.get("y"),
            "geometry": row.get("geometry"),
            "direction": vertical_direction(rec.get("text", ""), rules),
            "link_distance_drawing_units": round(dist, 3),
            "status": "candidate" if not reasons else "review",
            "review_reason": "；".join(reasons),
            "evidence": [evidence_of(rec)] + list(row.get("evidence") or []),
        })

    vertical_patterns = [str(x).upper() for x in (rules.get("vertical_route_layer_patterns") or [])]
    route_rules = rules.get("route_rules") or []
    system_rules = rules.get("system_rules") or []
    for fi, si, layer, seg in iter_geometry(data):
        upper_layer = compact(layer).upper()
        if not vertical_patterns or not any(token in upper_layer for token in vertical_patterns):
            continue
        route_class, route_rule, _route_pattern = match_rule(layer, route_rules, "route_class")
        system, system_rule, _system_pattern = match_rule(layer, system_rules, "system")
        if not system and route_rule:
            system = route_rule.get("system") or ""
        try:
            x1, y1, x2, y2 = (float(v) for v in seg[:4])
        except (TypeError, ValueError):
            continue
        file_name = data_file_name(data, fi)
        sheet = sheet_for_point(data, (x1 + x2) / 2.0, (y1 + y2) / 2.0)
        key = (file_name, sheet, "geometry", si, layer, x1, y1, x2, y2)
        if key in seen:
            continue
        seen.add(key)
        out.append({
            "type": "vertical_route",
            "id": None,
            "system": system,
            "route_class": route_class,
            "layer": layer,
            "file": file_name,
            "sheet": sheet,
            "geometry": [round(x1, 3), round(y1, 3), round(x2, 3), round(y2, 3)],
            "direction": "unspecified",
            "link_distance_drawing_units": None,
            "status": "review",
            "review_reason": "竖向几何命中但无立管编号证据",
            "evidence": [{"layer": layer, "kind": "geometry", "coord": [round(x1, 3), round(y1, 3), round(x2, 3), round(y2, 3)], "file": file_name, "sheet": sheet}],
        })
    return out[:200]

def topology_audit(routes: list[dict[str, Any]], tolerance: float = 5.0, max_segments: int = 5000) -> dict[str, Any]:
    """按文件、图框、专业系统建立路由连通分量，只输出拓扑候选和复核边界。"""
    grouped: dict[tuple[Any, ...], list[tuple[int, dict[str, Any]]]] = defaultdict(list)
    for idx, row in enumerate(routes[:max_segments]):
        scope = row.get("system") or row.get("route_class") or "unknown"
        grouped[(row.get("file"), row.get("sheet"), scope)].append((idx, row))
    components: list[dict[str, Any]] = []
    for (file_name, sheet, scope), items in grouped.items():
        parent = list(range(len(items)))

        def find(i: int) -> int:
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[rb] = ra

        cluster_members: dict[tuple[int, int], list[int]] = defaultdict(list)
        endpoint_keys: dict[int, list[tuple[int, int]]] = {}
        for local_i, (_global_i, row) in enumerate(items):
            geom = row.get("geometry") or []
            if len(geom) < 4:
                endpoint_keys[local_i] = []
                continue
            keys: list[tuple[int, int]] = []
            for x, y in ((geom[0], geom[1]), (geom[2], geom[3])):
                key = (round(float(x) / tolerance), round(float(y) / tolerance))
                keys.append(key)
                cluster_members[key].append(local_i)
            endpoint_keys[local_i] = keys
        for members in cluster_members.values():
            for member in members[1:]:
                union(members[0], member)
        by_root: dict[int, list[int]] = defaultdict(list)
        for local_i in range(len(items)):
            by_root[find(local_i)].append(local_i)
        for root, local_indexes in by_root.items():
            rows = [items[i][1] for i in local_indexes]
            node_keys = {key for i in local_indexes for key in endpoint_keys.get(i, [])}
            open_endpoint_count = sum(1 for key in node_keys if len(cluster_members[key]) == 1)
            junction_count = sum(1 for key in node_keys if len(cluster_members[key]) >= 3)
            points: list[tuple[float, float]] = []
            for row in rows:
                geom = row.get("geometry") or []
                if len(geom) >= 4:
                    points.extend([(float(geom[0]), float(geom[1])), (float(geom[2]), float(geom[3]))])
            bbox = None
            if points:
                xs = [p[0] for p in points]
                ys = [p[1] for p in points]
                bbox = [round(min(xs), 3), round(min(ys), 3), round(max(xs), 3), round(max(ys), 3)]
            route_classes = sorted({str(row.get("route_class") or "") for row in rows if row.get("route_class")})
            if open_endpoint_count:
                topology_class = "open-candidate"
                status = "review"
                reason = "存在开放端点，需确认设备接口、图幅截断或未识别连接"
            elif junction_count:
                topology_class = "branched-candidate"
                status = "candidate"
                reason = "存在分支/汇聚候选，需确认三通/四通"
            else:
                topology_class = "closed-loop-candidate"
                status = "candidate"
                reason = ""
            evidence: list[dict[str, Any]] = []
            for row in rows[:5]:
                evidence.extend(list(row.get("evidence") or []))
            components.append({
                "type": "topology_component",
                "component_id": f"{file_name or ''}:{sheet if sheet is not None else ''}:{scope}:{len(components) + 1}",
                "file": file_name,
                "sheet": sheet,
                "system": scope if scope not in {"unknown"} else "",
                "scope": scope,
                "segment_count": len(rows),
                "node_count": len(node_keys),
                "open_endpoint_count": open_endpoint_count,
                "junction_count": junction_count,
                "isolated_segment_count": 1 if len(rows) == 1 and open_endpoint_count == 2 else 0,
                "route_classes": route_classes,
                "bbox": bbox,
                "topology_class": topology_class,
                "status": status,
                "review_reason": reason,
                "evidence": evidence,
            })
    summary = {
        "components": len(components),
        "closed_loop_candidates": sum(1 for row in components if row["topology_class"] == "closed-loop-candidate"),
        "branched_candidates": sum(1 for row in components if row["topology_class"] == "branched-candidate"),
        "open_components": sum(1 for row in components if row["topology_class"] == "open-candidate"),
        "isolated_segments": sum(int(row["isolated_segment_count"]) for row in components),
        "review_components": sum(1 for row in components if row["status"] != "candidate"),
    }
    return {
        "tolerance_drawing_units": tolerance,
        "components": components[:200],
        "summary": summary,
        "truncated": len(components) > 200,
        "boundary": "只做按文件/图框/系统的路由连通分量和拓扑分类候选；不输出管长、工程量或材料量。",
    }

def route_segments(
    data: dict[str, Any], rules: dict[str, Any]
) -> tuple[list[dict[str, Any]], Counter]:
    out: list[dict[str, Any]] = []
    unmatched: Counter = Counter()
    route_rules = rules.get("route_rules") or []
    for fi, si, layer, seg in iter_geometry(data):
        route_class, rule, pattern = match_rule(layer, route_rules, "route_class")
        if not route_class:
            if any(token in layer.upper() for token in ("PIPE", "WIRE", "CABLE", "TRAY", "DUCT", "MEP", "BUSB", "LGT", "HVAC", "给水", "排水", "消防", "喷淋", "风管", "桥架", "电线", "导管", "电缆", "母线", "燃气")):
                unmatched[layer or "<空图层>"] += 1
            continue
        x1, y1, x2, y2 = (float(v) for v in seg[:4])
        file_name = data_file_name(data, fi)
        sheet = sheet_for_point(data, (x1 + x2) / 2.0, (y1 + y2) / 2.0)
        out.append(
            {
                "type": "route_segment",
                "route_class": route_class,
                "system": rule.get("system") or "",
                "pattern": pattern,
                "layer": layer,
                "file": file_name,
                "file_index": fi,
                "sheet": sheet,
                "geometry": [round(x1, 3), round(y1, 3), round(x2, 3), round(y2, 3)],
                "length_drawing_units": round(segment_length(seg), 3),
                "confidence": float((rules.get("confidence") or {}).get("geometry_pattern", 0.86)),
                "status": "candidate",
                "evidence": [{"layer": layer, "kind": "geometry", "coord": [round(x1, 3), round(y1, 3), round(x2, 3), round(y2, 3)], "file": file_name, "sheet": sheet}],
            }
        )
    return out, unmatched

def equipment_candidates(records: list[dict[str, Any]], rules: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    for rec in records:
        category, rule, pattern = match_rule(rec["text"], rules.get("equipment_rules") or [], "category")
        if not category:
            continue
        key = (context_of(rec), category, rec["text"], rec.get("layer"), rec.get("x"), rec.get("y"))
        if key in seen:
            continue
        seen.add(key)
        out.append(
            {
                "type": "equipment",
                "name": rec["text"],
                "category": category,
                "system": rule.get("system") or "",
                "pattern": pattern,
                "layer": rec.get("layer"),
                "kind": rec.get("kind"),
                "x": rec.get("x"),
                "y": rec.get("y"),
                "file": rec.get("file_name"),
                "sheet": rec.get("sheet"),
                "confidence": float((rules.get("confidence") or {}).get("direct_label", 0.95) if rec.get("kind") in {"INSERT", "ATTRIB"} else (rules.get("confidence") or {}).get("pattern_match", 0.78)),
                "status": "candidate",
                "evidence": [evidence_of(rec)],
            }
        )
    return out

def riser_candidates(records: list[dict[str, Any]], rules: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for rec, rid, system in extract_riser_labels(records, rules):
        out.append(
            {
                "type": "riser",
                "id": rid,
                "system": system,
                "layer": rec.get("layer"),
                "file": rec.get("file_name"),
                "sheet": rec.get("sheet"),
                "x": rec.get("x"),
                "y": rec.get("y"),
                "confidence": float((rules.get("confidence") or {}).get("direct_label", 0.95)),
                "status": "candidate" if system else "review",
                "review_reason": "" if system else "立管前缀未映射到专业系统",
                "evidence": [evidence_of(rec)],
            }
        )
    return out

def label_candidates(records: list[dict[str, Any]], rules: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    system_rules = rules.get("system_rules") or []
    equipment_rules = rules.get("equipment_rules") or []
    pipe_re = re.compile(rules.get("pipe_spec_pattern") or r"(?<![A-Za-z0-9])(?:DN|De|D|Φ|φ)\s*-?\s*\d{2,4}(?![0-9])", re.I)
    duct_re = re.compile(rules.get("duct_spec_pattern") or r"(?<![0-9])(\d{3,5})\s*[xX×]\s*(\d{3,5})(?![0-9])")
    circuit_re = re.compile(rules.get("circuit_spec_pattern") or r"(?<![A-Za-z0-9])((?:BYJ|BV|YJV|YJY|KVV|RVV|WDZ|WDZC|NH|ZR)[A-Z0-9+./×xX-]*\d+\s*[xX×]\s*\d+)", re.I)
    tag_re = re.compile(rules.get("equipment_tag_pattern") or r"(?<![A-Za-z0-9])([A-Z]{1,4}[-_]?\d{1,4})(?![A-Za-z0-9])")
    for rec in records:
        text = rec["text"]
        layer = rec.get("layer") or ""
        system, _rule, _pattern = match_rule(f"{text} {layer}", system_rules, "system")
        for match in pipe_re.finditer(text):
            out.append({"type": "label", "label_type": "pipe_spec", "text": match.group(0), "system": system, "layer": layer, "x": rec.get("x"), "y": rec.get("y"), "file": rec.get("file_name"), "sheet": rec.get("sheet"), "status": "candidate", "confidence": float((rules.get("confidence") or {}).get("direct_label", 0.95)), "evidence": [evidence_of(rec)]})
        if any(token in (text + " " + layer).upper() for token in ("风管", "风口", "风机", "HVAC", "DUCT", "AIR")):
            for match in duct_re.finditer(text):
                out.append({"type": "label", "label_type": "duct_spec", "text": match.group(0), "system": "hvac", "layer": layer, "x": rec.get("x"), "y": rec.get("y"), "file": rec.get("file_name"), "sheet": rec.get("sheet"), "status": "candidate", "confidence": float((rules.get("confidence") or {}).get("direct_label", 0.95)), "evidence": [evidence_of(rec)]})
        for match in circuit_re.finditer(text):
            out.append({"type": "label", "label_type": "circuit_spec", "text": match.group(0), "system": "electrical", "layer": layer, "x": rec.get("x"), "y": rec.get("y"), "file": rec.get("file_name"), "sheet": rec.get("sheet"), "status": "candidate", "confidence": float((rules.get("confidence") or {}).get("direct_label", 0.95)), "evidence": [evidence_of(rec)]})
        category, _erule, _epattern = match_rule(f"{text} {layer}", equipment_rules, "category")
        if category:
            for match in tag_re.finditer(text):
                tag = match.group(1).upper()
                if any(token in tag for token in ("DN", "DE")):
                    continue
                out.append({"type": "label", "label_type": "equipment_tag", "text": tag, "system": system, "category": category, "layer": layer, "x": rec.get("x"), "y": rec.get("y"), "file": rec.get("file_name"), "sheet": rec.get("sheet"), "status": "candidate", "confidence": float((rules.get("confidence") or {}).get("pattern_match", 0.78)), "evidence": [evidence_of(rec)]})
        if system and rec.get("kind") in {"TEXT", "MTEXT", "ATTRIB"}:
            out.append({"type": "label", "label_type": "system_label", "text": text, "system": system, "layer": layer, "x": rec.get("x"), "y": rec.get("y"), "file": rec.get("file_name"), "sheet": rec.get("sheet"), "status": "candidate", "confidence": float((rules.get("confidence") or {}).get("pattern_match", 0.78)), "evidence": [evidence_of(rec)]})
    return out

def connectivity_audit(routes: list[dict[str, Any]], tolerance: float = 5.0, max_segments: int = 5000) -> dict[str, Any]:
    """只做端点吸附和连通性候选，不汇总工程量。"""
    by_context: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in routes[:max_segments]:
        by_context[(row.get("file"), row.get("sheet"), row.get("system"))].append(row)
    open_endpoints: list[dict[str, Any]] = []
    junction_candidates: list[dict[str, Any]] = []
    isolated_segments: list[dict[str, Any]] = []
    for (file_name, sheet, system), rows in by_context.items():
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
                open_endpoints.append({"file": file_name, "sheet": sheet, "system": system, "x": x, "y": y, "route_index": i, "status": "review", "review_reason": "端点未吸附到同系统管段"})
            elif len(points) >= 3:
                x, y, _i = points[0]
                junction_candidates.append({"file": file_name, "sheet": sheet, "system": system, "x": x, "y": y, "degree": len(points), "status": "candidate", "review_reason": "多端点汇聚，需回图确认三通/分支"})
        for i, row in enumerate(rows):
            geom = row.get("geometry") or []
            if len(geom) < 4:
                continue
            endpoints = [clusters.get((round(float(geom[0]) / tolerance), round(float(geom[1]) / tolerance)), []), clusters.get((round(float(geom[2]) / tolerance), round(float(geom[3]) / tolerance)), [])]
            if len(endpoints[0]) == 1 and len(endpoints[1]) == 1:
                isolated_segments.append({"file": file_name, "sheet": sheet, "system": system, "route_index": i, "geometry": geom, "status": "review", "review_reason": "两端均未与其他同系统管段吸附"})
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
        "boundary": "只做端点吸附和连通性候选；不输出管长、工程量或材料量。",
    }

def _nearest_route_endpoint(
    point: dict[str, Any],
    route_grid: dict[tuple[Any, Any, int, int], list[tuple[float, float, int, int]]],
    tolerance: float,
) -> tuple[float, int, dict[str, Any]] | None:
    """从端点空间网格中取最近管段端点；只用于关联证据，不换算工程量。"""
    try:
        px, py = float(point.get("x")), float(point.get("y"))
    except (TypeError, ValueError):
        return None
    cx, cy = math.floor(px / tolerance), math.floor(py / tolerance)
    best: tuple[float, int, dict[str, Any]] | None = None
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for x, y, route_index, end_index in route_grid.get((point.get("file"), point.get("sheet"), cx + dx, cy + dy), []):
                distance = math.hypot(px - x, py - y)
                item = (distance, route_index, end_index)
                if best is None or item < best:
                    best = item
    return best

def mep_relation_candidates(
    routes: list[dict[str, Any]],
    equipment: list[dict[str, Any]],
    risers: list[dict[str, Any]],
    link_tolerance: float = 2000.0,
    snap_tolerance: float = 5.0,
    max_relations: int = 2000,
) -> list[dict[str, Any]]:
    """输出管段端点、设备和立管的关联候选；系统冲突和缺失必须进入复核。"""
    out: list[dict[str, Any]] = []
    link_cell = max(1e-9, float(link_tolerance))
    route_grid: dict[tuple[Any, Any, int, int], list[tuple[float, float, int, int]]] = defaultdict(list)
    valid_routes: list[dict[str, Any]] = []
    for index, row in enumerate(routes[:5000]):
        geom = row.get("geometry") or []
        if not isinstance(geom, (list, tuple)) or len(geom) < 4:
            continue
        try:
            x1, y1, x2, y2 = (float(v) for v in geom[:4])
        except (TypeError, ValueError):
            continue
        valid_routes.append(row)
        route_index = len(valid_routes) - 1
        for end_index, (x, y) in enumerate(((x1, y1), (x2, y2))):
            key = (row.get("file"), row.get("sheet"), math.floor(x / link_cell), math.floor(y / link_cell))
            route_grid[key].append((x, y, route_index, end_index))

    def relation_row(
        relation_type: str, system: str, route_index: int, target: dict[str, Any],
        distance: float, extra_name: Any = None,
    ) -> dict[str, Any]:
        row = valid_routes[route_index]
        geom = row.get("geometry") or []
        target_name = target.get("name") or target.get("id") or extra_name
        reasons: list[str] = []
        confidence = 0.95
        route_system = str(row.get("system") or "")
        target_system = str(target.get("system") or "")
        if route_system and target_system and route_system != target_system:
            reasons.append("geometry_conflict")
            confidence = 0.42
        if not route_system or not target_system:
            reasons.append("low_confidence_inference")
            confidence = min(confidence, 0.72)
        if distance > link_tolerance:
            reasons.append("ambiguous_text_binding")
            confidence = 0.42
        layer = row.get("layer")
        if not layer:
            reasons.append("missing_layer")
        status = "candidate" if not reasons else "review"
        return {
            "id": f"mep-relation:{relation_type}:{route_index}:{target_name or ''}:{round(distance, 3)}",
            "relation_type": relation_type,
            "system": route_system or target_system,
            "route_index": route_index,
            "route_class": row.get("route_class") or "",
            "target_type": target.get("type") or relation_type.split("_to_")[0],
            "target_name": target_name,
            "file": row.get("file"),
            "sheet": row.get("sheet"),
            "layer": layer,
            "geometry": geom,
            "link_distance_drawing_units": round(distance, 3),
            "confidence": confidence,
            "status": status,
            "review_reasons": reasons,
            "review_reason": "；".join({
                "geometry_conflict": "设备/立管系统与管段系统不一致",
                "low_confidence_inference": "任一侧缺少专业系统标注",
                "ambiguous_text_binding": "关联距离超出容差",
                "missing_layer": "管段缺图层证据",
            }.get(x, x) for x in reasons),
            "evidence": list(row.get("evidence") or []) + list(target.get("evidence") or []),
            "method": "endpoint_spatial_link",
        }

    # 设备→管段端点关联
    for equipment_index, target in enumerate(equipment[:2000]):
        nearest = _nearest_route_endpoint(target, route_grid, link_cell)
        if nearest is None:
            continue
        distance, route_index, hit = nearest
        if distance > link_tolerance:
            continue
        row = relation_row("equipment_to_route", "", route_index, target, distance, extra_name=hit)
        row["equipment_index"] = equipment_index
        out.append(row)

    # 立管→管段端点关联
    for riser_index, target in enumerate(risers[:2000]):
        nearest = _nearest_route_endpoint(target, route_grid, link_cell)
        if nearest is None:
            continue
        distance, route_index, hit = nearest
        if distance > link_tolerance:
            continue
        row = relation_row("riser_to_route", "", route_index, target, distance, extra_name=hit)
        row["riser_index"] = riser_index
        out.append(row)

    # 同位置管段端点拓扑关联；系统不同时转复核
    endpoint_cell = max(1e-9, float(snap_tolerance))
    endpoint_grid: dict[tuple[Any, Any, int, int], list[tuple[float, float, int, int]]] = defaultdict(list)
    for route_index, row in enumerate(valid_routes):
        geom = row.get("geometry") or []
        for end_index, value in enumerate(((geom[0], geom[1]), (geom[2], geom[3]))):
            x, y = float(value[0]), float(value[1])
            key = (row.get("file"), row.get("sheet"), math.floor(x / endpoint_cell), math.floor(y / endpoint_cell))
            endpoint_grid[key].append((x, y, route_index, end_index))
    seen_clusters: set[tuple[Any, ...]] = set()
    for key, points in sorted(endpoint_grid.items(), key=lambda item: tuple(str(v) for v in item[0])):
        if len(points) < 2:
            continue
        route_indexes = tuple(sorted({p[2] for p in points}))
        if len(route_indexes) < 2 or route_indexes in seen_clusters:
            continue
        seen_clusters.add(route_indexes)
        systems = sorted({str(valid_routes[i].get("system") or "") for i in route_indexes})
        route_systems = {str(valid_routes[i].get("system") or "") for i in route_indexes}
        reasons: list[str] = []
        if len(route_systems) > 1:
            reasons.append("geometry_conflict")
        if "" in route_systems:
            reasons.append("low_confidence_inference")
        first = valid_routes[route_indexes[0]]
        geom = first.get("geometry") or []
        point = points[0]
        row = {
            "id": "mep-relation:endpoint:" + ":".join(str(x) for x in route_indexes),
            "relation_type": "endpoint_connection",
            "system": systems[0] if len(systems) == 1 else "",
            "route_indexes": list(route_indexes),
            "systems": systems,
            "file": first.get("file"),
            "sheet": first.get("sheet"),
            "layer": first.get("layer"),
            "x": point[0], "y": point[1],
            "geometry": geom,
            "confidence": 0.95 if not reasons else 0.42,
            "status": "candidate" if not reasons else "review",
            "review_reasons": reasons,
            "review_reason": "；".join({
                "geometry_conflict": "同位置端点连接了不同系统",
                "low_confidence_inference": "端点关联缺少系统标注",
            }.get(x, x) for x in reasons),
            "evidence": list(first.get("evidence") or []),
            "method": "endpoint_cluster",
        }
        out.append(row)
        if len(out) >= max_relations:
            break
    out = out[:max_relations]
    out.sort(key=lambda row: (str(row.get("relation_type")), str(row.get("file") or ""), str(row.get("sheet") or ""), str(row.get("id"))))
    return out

def analyze_file(path: Path, rules: dict[str, Any], snap_tolerance: float, link_tolerance: float = 2000.0) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    records = read_records(data)
    views = drawing_type_candidates(records, rules)
    audit = scale_unit_audit(records, rules)
    systems = system_candidates(records, data, rules)
    routes, unmatched_layers = route_segments(data, rules)
    equipment = equipment_candidates(records, rules)
    labels = label_candidates(records, rules)
    risers = riser_candidates(records, rules)
    vertical_routes = vertical_route_candidates(records, routes, data, rules, link_tolerance)
    connectivity = connectivity_audit(routes, snap_tolerance)
    topology = topology_audit(routes, snap_tolerance)
    mep_relations = mep_relation_candidates(routes, equipment, risers, link_tolerance, snap_tolerance)
    review: list[dict[str, Any]] = []
    for row in views:
        if row.get("status") != "candidate":
            review.append({"type": "drawing_type", "reason": row.get("review_reason") or "图纸类型需确认", "evidence": row.get("evidence", [])})
    for row in audit:
        if row.get("status") != "candidate":
            review.append({"type": "scale_unit", "reason": row.get("review_reason") or "比例或单位需确认", "evidence": row.get("evidence", [])})
    for row in risers:
        if row.get("status") != "candidate":
            review.append({"type": "riser", "reason": row.get("review_reason") or "立管归属需确认", "evidence": row.get("evidence", [])})
    for row in topology["components"]:
        if row.get("status") != "candidate":
            review.append({"type": "topology", "reason": row.get("review_reason") or "系统拓扑需确认", "evidence": row.get("evidence", [])})
    for row in vertical_routes:
        if row.get("status") != "candidate":
            review.append({"type": "vertical_route", "reason": row.get("review_reason") or "竖向路由需确认", "evidence": row.get("evidence", [])})
    for row in mep_relations:
        if row.get("status") != "candidate":
            review.append({"type": "mep_relation", "reason": row.get("review_reason") or "MEP 关联需确认", "evidence": row.get("evidence", [])})
    for layer, count in unmatched_layers.most_common(50):
        review.append({"type": "route_layer", "reason": f"MEP 图层未分类：{layer}（{count} 段）", "evidence": [{"layer": layer}]})
    if not data.get("geometry_segments") or not data.get("geometry_layers"):
        review.append({"type": "input_geometry", "reason": "输入缺少 geometry_segments 或 geometry_layers；请用 cad_scan --with-geom --with-geom-layer", "evidence": []})
    if not views:
        review.append({"type": "drawing_type", "reason": "未识别到安装图纸类型文字", "evidence": []})
    summary = {
        "drawing_types": len(views),
        "systems": len(systems),
        "route_segments": len(routes),
        "equipment": len(equipment),
        "labels": len(labels),
        "risers": len(risers),
        "vertical_routes": len(vertical_routes),
        "vertical_routes_review": sum(1 for row in vertical_routes if row.get("status") != "candidate"),
        "mep_relations": len(mep_relations),
        "mep_relations_review": sum(1 for row in mep_relations if row.get("status") != "candidate"),
        "topology_components": topology["summary"]["components"],
        "topology_review_components": topology["summary"]["review_components"],
        "connectivity_open_endpoints": connectivity["summary"]["open_endpoints"],
        "connectivity_junctions": connectivity["summary"]["junction_candidates"],
        "review_items": len(review),
    }
    return {
        "schema": "cad-mep-geometry/v2",
        "source_file": path.name,
        "summary": summary,
        "drawing_types": views,
        "scale_unit_audit": audit,
        "systems": systems,
        "route_segments": routes,
        "equipment": equipment,
        "labels": labels,
        "risers": risers,
        "vertical_routes": vertical_routes,
        "mep_relations": mep_relations,
        "connectivity": connectivity,
        "topology": topology,
        "review": review,
        "boundary": "只输出安装识图候选、证据、连通性审计和系统拓扑候选；不输出工程量、材料量、损耗、造价或结算量。",
    }

def write_markdown(payload: dict[str, Any], path: Path) -> None:
    s = payload["summary"]
    lines = [
        "# 安装识图 / MEP 中间数据复核",
        "",
        f"- 源文件：`{payload['source_file']}`",
        f"- 候选：图纸类型 {s['drawing_types']}，专业系统 {s['systems']}，路由段 {s['route_segments']}，设备 {s['equipment']}，标注 {s['labels']}，立管 {s['risers']}，竖向路由 {s['vertical_routes']}，拓扑组件 {s['topology_components']}，MEP关联 {s['mep_relations']}，待复核 {s['review_items']}",
        f"- 连通性：开放端点 {s['connectivity_open_endpoints']}，汇聚候选 {s['connectivity_junctions']}；拓扑复核组件 {s['topology_review_components']}，竖向路由复核 {s['vertical_routes_review']}，MEP关联复核 {s['mep_relations_review']}",
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
    lines += ["", "## 专业系统", ""]
    if payload["systems"]:
        lines += ["| 系统 | 原文/图层 | 图层 | 置信 |", "|---|---|---|---:|"]
        for row in payload["systems"][:120]:
            lines.append(f"| {row['system']} | {row['raw']} | {row.get('layer', '')} | {row['confidence']:.2f} |")
    else:
        lines.append("无")
    lines += ["", "## 路由段候选", ""]
    if payload["route_segments"]:
        lines += ["| 类别 | 系统 | 图层 | 几何 | 图面长度 | 状态 |", "|---|---|---|---|---:|---|"]
        for row in payload["route_segments"][:120]:
            geom = "→".join(f"({row['geometry'][i]},{row['geometry'][i+1]})" for i in (0, 2))
            lines.append(f"| {row['route_class']} | {row['system']} | {row['layer']} | {geom} | {row['length_drawing_units']} | {row['status']} |")
    else:
        lines.append("无")
    lines += ["", "## 系统拓扑候选", ""]
    if payload["topology"]["components"]:
        lines += ["| 范围 | 段数 | 节点 | 开放端点 | 汇聚 | 类型 | 状态 |", "|---|---:|---:|---:|---:|---|---|"]
        for row in payload["topology"]["components"][:120]:
            lines.append(f"| {row['scope']} | {row['segment_count']} | {row['node_count']} | {row['open_endpoint_count']} | {row['junction_count']} | {row['topology_class']} | {row['status']} |")
    else:
        lines.append("无")
    lines += ["", "## 竖向路由候选", ""]
    if payload["vertical_routes"]:
        lines += ["| 编号 | 系统 | 路由类别 | 关联距离 | 方向 | 状态 | 待复核 |", "|---|---|---|---:|---|---|---|"]
        for row in payload["vertical_routes"][:120]:
            lines.append(f"| {row.get('id') or '几何命中'} | {row.get('system', '')} | {row.get('route_class', '')} | {row.get('link_distance_drawing_units', '')} | {row.get('direction', '')} | {row['status']} | {row.get('review_reason', '')} |")
    else:
        lines.append("无")
    lines += ["", "## 设备与器具候选", ""]
    if payload["equipment"]:
        lines += ["| 名称 | 类别 | 系统 | 图层 | 坐标 |", "|---|---|---|---|---|"]
        for row in payload["equipment"][:120]:
            coord = f"({row.get('x')},{row.get('y')})" if row.get("x") is not None else ""
            lines.append(f"| {row['name']} | {row['category']} | {row['system']} | {row.get('layer', '')} | {coord} |")
    else:
        lines.append("无")
    lines += ["", "## 文字标注候选", ""]
    if payload["labels"]:
        lines += ["| 类型 | 原文 | 系统 | 图层 |", "|---|---|---|---|"]
        for row in payload["labels"][:120]:
            lines.append(f"| {row['label_type']} | {row['text']} | {row.get('system', '')} | {row.get('layer', '')} |")
    else:
        lines.append("无")
    lines += ["", "## 立管候选", ""]
    if payload["risers"]:
        lines += ["| 编号 | 系统 | 图层 | 状态 | 待复核 |", "|---|---|---|---|---|"]
        for row in payload["risers"][:80]:
            lines.append(f"| {row['id']} | {row.get('system', '')} | {row.get('layer', '')} | {row['status']} | {row.get('review_reason', '')} |")
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
        writer.writerow(["row_type", "system", "route_class", "name", "layer", "file", "sheet", "coordinate", "status", "evidence"])
        for row in payload["drawing_types"]:
            ev = (row.get("evidence") or [{}])[0]
            writer.writerow(["drawing_type", "", "", row["type"], ev.get("layer", ""), ev.get("file_name", ""), ev.get("sheet", ""), ev.get("coord", ""), row["status"], row["raw"]])
        for row in payload["systems"]:
            writer.writerow(["system", row["system"], "", row["raw"], row.get("layer", ""), row.get("file", ""), "", "", row["status"], row.get("pattern", "")])
        for row in payload["route_segments"]:
            geom = row["geometry"]
            writer.writerow(["route_segment", row["system"], row["route_class"], row["route_class"], row["layer"], row["file"], row.get("sheet", ""), f"{geom[0]},{geom[1]}->{geom[2]},{geom[3]}", row["status"], row["length_drawing_units"]])
        for row in payload["topology"]["components"]:
            writer.writerow(["topology", row.get("system", ""), "", row.get("topology_class", ""), "", row.get("file", ""), row.get("sheet", ""), row.get("bbox", ""), row["status"], row.get("review_reason", "")])
        for row in payload["vertical_routes"]:
            geom = row.get("geometry") or []
            coord = f"{geom[0]},{geom[1]}->{geom[2]},{geom[3]}" if len(geom) >= 4 else f"{row.get('x')},{row.get('y')}"
            writer.writerow(["vertical_route", row.get("system", ""), row.get("route_class", ""), row.get("id") or "geometry-only", row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), coord, row["status"], row.get("review_reason", "")])
        for row in payload["equipment"]:
            writer.writerow(["equipment", row.get("system", ""), "", row["name"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{row.get('x')},{row.get('y')}", row["status"], row.get("category", "")])
        for row in payload["labels"]:
            writer.writerow(["label", row.get("system", ""), row.get("label_type", ""), row["text"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{row.get('x')},{row.get('y')}", row["status"], ""])
        for row in payload["risers"]:
            writer.writerow(["riser", row.get("system", ""), "", row["id"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{row.get('x')},{row.get('y')}", row["status"], row.get("review_reason", "")])
        for row in payload.get("mep_relations", []):
            geom = row.get("geometry") or []
            coord = f"{geom[0]},{geom[1]}->{geom[2]},{geom[3]}" if len(geom) >= 4 else f"{row.get('x')},{row.get('y')}"
            writer.writerow(["mep_relation", row.get("system", ""), row.get("route_class", ""), row.get("relation_type", ""), row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), coord, row["status"], row.get("review_reason", "")])
        for row in payload["review"]:
            writer.writerow(["review", "", "", row["type"], "", "", "", "", "review", row["reason"]])

def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    parser = argparse.ArgumentParser(description="从 cad_scan 详情 JSON 提取安装专业识图中间数据。")
    parser.add_argument("inputs", nargs="+", help="cad_scan 生成的 --detail-json 文件")
    parser.add_argument("--out-dir", default="安装识图", help="输出目录")
    parser.add_argument("--rules", default=str(RULES_PATH), help="MEP 识图规则 JSON")
    parser.add_argument("--snap-tolerance", type=float, default=5.0, help="端点吸附容差，图面单位")
    parser.add_argument("--link-tolerance", type=float, default=2000.0, help="立管编号与路由段的关联距离容差，图面单位")
    args = parser.parse_args()

    rules = load_rules(Path(args.rules))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[str] = []
    for value in args.inputs:
        src = Path(value)
        if not src.exists():
            raise FileNotFoundError(src)
        payload = analyze_file(src, rules, args.snap_tolerance, args.link_tolerance)
        payload = contractize_payload(payload, source=src.name)
        json_path = out_dir / f"{src.stem}.mep.json"
        md_path = out_dir / f"{src.stem}.mep.md"
        csv_path = out_dir / f"{src.stem}.mep.csv"
        json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        write_markdown(payload, md_path)
        write_csv(payload, csv_path)
        outputs.extend([str(json_path), str(md_path), str(csv_path)])
        print(json.dumps({"source": str(src), "summary": payload["summary"], "outputs": [str(json_path), str(md_path), str(csv_path)]}, ensure_ascii=False))
    return 0 if outputs else 4

if __name__ == "__main__":
    raise SystemExit(main())
