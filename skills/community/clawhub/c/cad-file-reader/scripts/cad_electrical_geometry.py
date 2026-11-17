#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 cad_scan 详情 JSON 提炼电气专业识图中间数据。

边界：只识别图纸对象、系统、回路、路线、设备、标注、防雷接地和证据候选；
不输出工程量、材料量、损耗、回路展开、负荷、造价或结算量。
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
RULES_PATH = ROOT / "packs" / "electrical-geometry" / "rules.json"
from cad_contract import contractize_payload

from cad_common import compact, load_rules, match_rule, segment_length


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


def route_segments(
    data: dict[str, Any], rules: dict[str, Any]
) -> tuple[list[dict[str, Any]], Counter]:
    out: list[dict[str, Any]] = []
    unmatched: Counter = Counter()
    route_rules = rules.get("route_rules") or []
    for fi, si, layer, seg in iter_geometry(data):
        route_class, rule, pattern = match_rule(layer, route_rules, "route_class")
        if not route_class:
            if any(token in layer.upper() for token in ("TRAY", "WIRE", "CABLE", "CONDUIT", "DUCT", "BUSB", "LGT", "POWER", "LIGHT", "照明", "动力", "配电", "桥架", "母线", "电缆", "导线", "导管", "线槽")):
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
        text = rec["text"]
        layer = rec.get("layer") or ""
        kind = (rec.get("kind") or "").upper()
        layer_up = layer.upper()
        # 排除图纸标题/题名栏文字，避免“一层应急照明平面图”等被当作设备
        if layer_up in {"TITLE", "标题", "TITLE-LABEL"} or "TITLE" in layer_up or "题名" in layer_up or "图名" in layer_up:
            continue
        if re.search(r"(平面图|系统图|干线图|详图|大样图|目录|说明|图例)", text):
            continue
        category, rule, pattern = match_rule(f"{text} {layer}", rules.get("equipment_rules") or [], "category")
        if not category:
            continue
        key = (context_of(rec), category, text, layer, rec.get("x"), rec.get("y"))
        if key in seen:
            continue
        seen.add(key)
        reasons: list[str] = []
        if not layer:
            reasons.append("missing_layer")
        confidence = float((rules.get("confidence") or {}).get("direct_label", 0.95))
        if reasons:
            confidence = min(confidence, float((rules.get("confidence") or {}).get("pattern_match", 0.78)))
        out.append(
            {
                "type": "equipment",
                "name": text,
                "category": category,
                "system": rule.get("system") or "",
                "pattern": pattern,
                "layer": layer,
                "kind": rec.get("kind"),
                "x": rec.get("x"),
                "y": rec.get("y"),
                "file": rec.get("file_name"),
                "sheet": rec.get("sheet"),
                "confidence": confidence,
                "status": "candidate" if not reasons else "review",
                "review_reasons": reasons,
                "evidence": [evidence_of(rec)],
            }
        )
    return out


def circuit_candidates(records: list[dict[str, Any]], rules: dict[str, Any]) -> list[dict[str, Any]]:
    """识别回路编号候选（WL/WPM/L/M 等）并按图框/图层分组。只做候选与复核，不做展开。"""
    out: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    pattern = re.compile(rules.get("circuit_pattern") or r"(?<![A-Za-z0-9])((?:WL|WP|WE|WPM|WPL|WPE|EM|L|M)[-_ ]?\d{1,4})(?![A-Za-z0-9])", re.I)
    for rec in records:
        for match in pattern.finditer(rec["text"]):
            circuit = match.group(1).upper()
            prefix = re.sub(r"[-_ ]?\d{1,4}$", "", circuit)
            system = "power"
            if prefix in {"WL", "WPM", "WPL", "WPE", "L"}:
                system = "lighting"
            elif prefix in {"WE", "EM", "XE"}:
                system = "emergency"
            elif prefix in {"M", "WP"}:
                system = "power"
            elif prefix in {"FAS", "FA", "FBF", "FB", "FBN"}:
                system = "fire_alarm"
            elif prefix in {"HY", "SP"}:
                system = "fire_water" if prefix == "HY" else "sprinkler"
            elif prefix in {"AO", "DI", "DO", "AI", "MS", "BMS"}:
                system = "building_automation"
            elif prefix in {"IBMS"}:
                system = "ibms"
            elif prefix in {"XQ", "XFB", "XS", "CCTV", "PDS", "ACS", "PA", "AV"}:
                system = "weak_current_other"
            elif prefix in {"X"}:
                system = "weak_current_other"
            key = (context_of(rec), circuit, rec.get("layer"), rec.get("x"), rec.get("y"))
            if key in seen:
                continue
            seen.add(key)
            confidence = float((rules.get("confidence") or {}).get("direct_label", 0.95))
            if not rec.get("layer"):
                confidence = min(confidence, float((rules.get("confidence") or {}).get("pattern_match", 0.78)))
            out.append(
                {
                    "type": "circuit",
                    "circuit_id": circuit,
                    "prefix": prefix,
                    "system": system,
                    "layer": rec.get("layer"),
                    "x": rec.get("x"),
                    "y": rec.get("y"),
                    "file": rec.get("file_name"),
                    "sheet": rec.get("sheet"),
                    "confidence": confidence,
                    "status": "candidate",
                    "review_reason": "",
                    "source_text": rec["text"],
                    "evidence": [evidence_of(rec)],
                }
            )
    return out


def spec_candidates(records: list[dict[str, Any]], rules: dict[str, Any]) -> list[dict[str, Any]]:
    """识别回路规格候选（导线/电缆型号、桥架规格、导管规格等）。"""
    out: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    spec_re = re.compile(rules.get("spec_pattern") or r"(?<![A-Za-z0-9])(WDZ[A-Z0-9+./×xX-]*|BYJ[A-Z0-9+./×xX-]*|BV[A-Z0-9+./×xX-]*|YJV[A-Z0-9+./×xX-]*|[A-Z]{0,4}\d?\s*[xX×]\s*\d+)", re.I)
    for rec in records:
        for match in spec_re.finditer(rec["text"]):
            spec = match.group(0).upper()
            key = (context_of(rec), spec, rec.get("layer"), rec.get("x"), rec.get("y"))
            if key in seen:
                continue
            seen.add(key)
            out.append(
                {
                    "type": "spec",
                    "spec": spec,
                    "layer": rec.get("layer"),
                    "x": rec.get("x"),
                    "y": rec.get("y"),
                    "file": rec.get("file_name"),
                    "sheet": rec.get("sheet"),
                    "confidence": float((rules.get("confidence") or {}).get("direct_label", 0.95)),
                    "status": "candidate",
                    "evidence": [evidence_of(rec)],
                }
            )
    return out


def label_candidates(records: list[dict[str, Any]], rules: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    tag_re = re.compile(rules.get("equipment_tag_pattern") or r"(?<![A-Za-z0-9])([A-Z]{1,4}[-_]?\d{1,4})(?![A-Za-z0-9])", re.I)
    floor_re = re.compile(rules.get("floor_pattern") or r"^(?:B\d{1,2}|F\d{1,2}|[1-9]\d?F)$", re.I)
    for rec in records:
        text = rec["text"]
        layer = rec.get("layer") or ""
        system, _srule, _spattern = match_rule(text, rules.get("system_rules") or [], "system")
        for match in tag_re.finditer(text):
            tag = match.group(1).upper()
            if any(token in tag for token in ("DN", "DE")):
                continue
            out.append({"type": "label", "label_type": "equipment_tag", "text": tag, "system": system, "layer": layer, "x": rec.get("x"), "y": rec.get("y"), "file": rec.get("file_name"), "sheet": rec.get("sheet"), "status": "candidate", "confidence": float((rules.get("confidence") or {}).get("pattern_match", 0.78)), "evidence": [evidence_of(rec)]})
        for match in floor_re.finditer(text):
            out.append({"type": "label", "label_type": "floor", "text": match.group(0), "system": system, "layer": layer, "x": rec.get("x"), "y": rec.get("y"), "file": rec.get("file_name"), "sheet": rec.get("sheet"), "status": "candidate", "confidence": float((rules.get("confidence") or {}).get("direct_label", 0.95)), "evidence": [evidence_of(rec)]})
        if system and rec.get("kind") in {"TEXT", "MTEXT", "ATTRIB"}:
            out.append({"type": "label", "label_type": "system_label", "text": text, "system": system, "layer": layer, "x": rec.get("x"), "y": rec.get("y"), "file": rec.get("file_name"), "sheet": rec.get("sheet"), "status": "candidate", "confidence": float((rules.get("confidence") or {}).get("pattern_match", 0.78)), "evidence": [evidence_of(rec)]})
    return out


def lightning_candidates(records: list[dict[str, Any]], data: dict[str, Any], rules: dict[str, Any]) -> list[dict[str, Any]]:
    """防雷接地候选：文字与防雷设备/图层证据，缺几何时进入复核。"""
    out: list[dict[str, Any]] = []
    eq_rules = rules.get("equipment_rules") or []
    for rec in records:
        text = rec["text"]
        layer = rec.get("layer") or ""
        category, _rule, pattern = match_rule(f"{text} {layer}", eq_rules, "category")
        if category != "lightning_device":
            continue
        reasons: list[str] = []
        if not layer:
            reasons.append("missing_layer")
        if not rec.get("x") and not rec.get("y"):
            reasons.append("incomplete_geometry")
        if not any(str(p) in f"{layer} {text}" for p in ("接闪", "引下线", "均压环", "等电位", "测试卡")):
            reasons.append("low_confidence_inference")
        out.append(
            {
                "type": "lightning",
                "name": text,
                "category": category,
                "system": "lightning_protection",
                "pattern": pattern,
                "layer": layer,
                "x": rec.get("x"),
                "y": rec.get("y"),
                "file": rec.get("file_name"),
                "sheet": rec.get("sheet"),
                "confidence": float((rules.get("confidence") or {}).get("direct_label", 0.95)) if not reasons else float((rules.get("confidence") or {}).get("inferred", 0.5)),
                "status": "candidate" if not reasons else "review",
                "review_reason": "；".join(reasons),
                "evidence": [evidence_of(rec)],
            }
        )
    for fi, si, layer, seg in iter_geometry(data):
        category, _rule, pattern = match_rule(layer, eq_rules, "category")
        if category != "lightning_device":
            continue
        file_name = data_file_name(data, fi)
        x1, y1, x2, y2 = (float(v) for v in seg[:4])
        out.append(
            {
                "type": "lightning",
                "name": layer,
                "category": "lightning_device",
                "system": "lightning_protection",
                "pattern": pattern,
                "layer": layer,
                "x": (x1 + x2) / 2,
                "y": (y1 + y2) / 2,
                "file": file_name,
                "sheet": sheet_for_point(data, (x1 + x2) / 2, (y1 + y2) / 2),
                "confidence": float((rules.get("confidence") or {}).get("geometry_pattern", 0.86)),
                "status": "candidate",
                "evidence": [{"layer": layer, "kind": "geometry", "coord": [round(x1, 3), round(y1, 3), round(x2, 3), round(y2, 3)], "file": file_name}],
            }
        )
    return out



FIRE_DOMAIN = "fire_protection"
WEAK_DOMAIN = "weak_current"
INTEL_DOMAIN = "intelligent_building"
DOMAIN_LABEL = {
    FIRE_DOMAIN: "消防",
    WEAK_DOMAIN: "弱点/弱电",
    INTEL_DOMAIN: "智能化",
}


def domain_of(system: str, domain_rules: dict[str, Any]) -> str:
    """把 system 归入消防/弱点/智能化领域；domain_rules: {领域: [system,...]}。"""
    for domain, names in (domain_rules or {}).items():
        if system and system in (names or []):
            return domain
    return ""


def domain_candidates(systems, equipment, circuits, routes, labels, rules):
    """把全局候选按消防/弱点/智能化领域分组，输出带领域标签的复核用候选表。"""
    domain_rules = rules.get("domain_rules") or {}
    out = {FIRE_DOMAIN: [], WEAK_DOMAIN: [], INTEL_DOMAIN: []}
    for row in systems:
        d = domain_of(row.get("system"), domain_rules)
        if d:
            out[d].append({**row, "domain": d, "domain_label": DOMAIN_LABEL.get(d, d), "group": "system"})
    for row in equipment:
        d = domain_of(row.get("system"), domain_rules)
        if d:
            out[d].append({**row, "domain": d, "domain_label": DOMAIN_LABEL.get(d, d), "group": "equipment"})
    for row in circuits:
        d = domain_of(row.get("system"), domain_rules)
        if d:
            out[d].append({**row, "domain": d, "domain_label": DOMAIN_LABEL.get(d, d), "group": "circuit"})
    for row in routes:
        d = domain_of(row.get("system"), domain_rules)
        if not d and row.get("route_class") in ("fire_loop", "signal_bus"):
            d = FIRE_DOMAIN if row.get("route_class") == "fire_loop" else WEAK_DOMAIN
        if d:
            out[d].append({**row, "domain": d, "domain_label": DOMAIN_LABEL.get(d, d), "group": "route"})
    for row in labels:
        d = domain_of(row.get("system"), domain_rules)
        if d:
            out[d].append({**row, "domain": d, "domain_label": DOMAIN_LABEL.get(d, d), "group": "label"})
    return out


def analyze_file(path: Path, rules: dict[str, Any]) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    records = read_records(data)
    views = drawing_type_candidates(records, rules)
    audit = scale_unit_audit(records, rules)
    systems = system_candidates(records, data, rules)
    routes, unmatched_layers = route_segments(data, rules)
    equipment = equipment_candidates(records, rules)
    circuits = circuit_candidates(records, rules)
    specs = spec_candidates(records, rules)
    labels = label_candidates(records, rules)
    lightning = lightning_candidates(records, data, rules)
    review: list[dict[str, Any]] = []
    for row in views:
        if row.get("status") != "candidate":
            review.append({"type": "drawing_type", "reason": row.get("review_reason") or "图纸类型需确认", "evidence": row.get("evidence", [])})
    for row in audit:
        if row.get("status") != "candidate":
            review.append({"type": "scale_unit", "reason": row.get("review_reason") or "比例或单位需确认", "evidence": row.get("evidence", [])})
    for row in equipment:
        if row.get("status") != "candidate":
            review.append({"type": "equipment", "reason": row.get("review_reason") or "设备归属需确认", "evidence": row.get("evidence", [])})
    for row in lightning:
        if row.get("status") != "candidate":
            review.append({"type": "lightning", "reason": row.get("review_reason") or "防雷接地候选需确认", "evidence": row.get("evidence", [])})
    for layer, count in unmatched_layers.most_common(50):
        review.append({"type": "route_layer", "reason": f"电气图层未分类：{layer}（{count} 段）", "evidence": [{"layer": layer}]})
    if not data.get("geometry_segments") or not data.get("geometry_layers"):
        review.append({"type": "input_geometry", "reason": "输入缺少 geometry_segments 或 geometry_layers；请用 cad_scan --with-geom --with-geom-layer", "evidence": []})
    if not views:
        review.append({"type": "drawing_type", "reason": "未识别到电气图纸类型文字", "evidence": []})
    domains = domain_candidates(systems, equipment, circuits, routes, labels, rules)
    summary = {
        "drawing_types": len(views),
        "systems": len(systems),
        "route_segments": len(routes),
        "equipment": len(equipment),
        "circuits": len(circuits),
        "specs": len(specs),
        "labels": len(labels),
        "lightning": len(lightning),
        "fire_protection": len(domains[FIRE_DOMAIN]),
        "weak_current": len(domains[WEAK_DOMAIN]),
        "intelligent_building": len(domains[INTEL_DOMAIN]),
        "lightning_review": sum(1 for row in lightning if row.get("status") != "candidate"),
        "review_items": len(review),
    }
    return {
        "schema": "cad-electrical-geometry/v1",
        "source_file": path.name,
        "summary": summary,
        "drawing_types": views,
        "scale_unit_audit": audit,
        "systems": systems,
        "route_segments": routes,
        "equipment": equipment,
        "circuits": circuits,
        "specs": specs,
        "labels": labels,
        "lightning": lightning,
        "fire_protection": domains[FIRE_DOMAIN],
        "weak_current": domains[WEAK_DOMAIN],
        "intelligent_building": domains[INTEL_DOMAIN],
        "review": review,
        "boundary": "只输出电气识图候选、证据、系统、回路、路线、设备、标注、防雷接地、消防、弱电和智能化候选；不输出工程量、材料量、损耗、回路展开、负荷、造价或结算量。",
    }


def write_markdown(payload: dict[str, Any], path: Path) -> None:
    s = payload["summary"]
    lines = [
        "# 电气识图 / Electrical 中间数据复核",
        "",
        f"- 源文件：`{payload['source_file']}`",
        f"- 候选：图纸类型 {s['drawing_types']}，系统 {s['systems']}，路由段 {s['route_segments']}，设备 {s['equipment']}，回路 {s['circuits']}，规格 {s['specs']}，标注 {s['labels']}，防雷接地 {s['lightning']}；消防 {s['fire_protection']}，弱点/弱电 {s['weak_current']}，智能化 {s['intelligent_building']}，待复核 {s['review_items']}",
        "",
        "- 只输出识图候选和证据，不输出工程量、材料量、损耗、回路展开、负荷、造价或结算量。",
        "",
    ]
    if payload["review"]:
        lines.append("## 待复核")
        for row in payload["review"][:60]:
            ev = (row.get("evidence") or [{}])[0]
            lines.append(f"- [{row.get('type')}] {row.get('reason')} | 图层 {ev.get('layer', '—')} 坐标 {ev.get('coord', '—')}")
        lines.append("")
    lines.append("## 设备候选")
    for row in payload["equipment"][:200]:
        lines.append(f"- {row.get('name')} [{row.get('category')}] system={row.get('system')} layer={row.get('layer')} x={row.get('x')} y={row.get('y')} status={row.get('status')}")
    lines.append("")
    lines.append("## 回路/规格候选")
    for row in (payload["circuits"] + payload["specs"])[:200]:
        kind = row.get("type") or ("circuit" if "circuit_id" in row else "spec")
        label = row.get("circuit_id") or row.get("spec") or row.get("text") or ""
        lines.append(f"- [{kind}] {label} system={row.get('system')} layer={row.get('layer')} x={row.get('x')} y={row.get('y')} status={row.get('status')}")
    lines.append("")
    for domain, title in ((FIRE_DOMAIN, "消防候选"), (WEAK_DOMAIN, "弱点/弱电候选"), (INTEL_DOMAIN, "智能化候选")):
        rows = payload.get(domain) or []
        lines.append(f"## {title}（{len(rows)}）")
        for row in rows[:100]:
            lines.append(f"- [{row.get('group')}] {row.get('name') or row.get('system') or row.get('circuit_id') or row.get('text') or row.get('raw')} system={row.get('system')} layer={row.get('layer')} x={row.get('x')} y={row.get('y')} status={row.get('status')}")
        lines.append("")
    lines.append("## 防雷接地候选")
    for row in payload["lightning"][:100]:
        lines.append(f"- {row.get('name')} layer={row.get('layer')} x={row.get('x')} y={row.get('y')} status={row.get('status')} {row.get('review_reason')}")
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
            geom = row.get("geometry") or []
            coord = f"{geom[0]},{geom[1]}->{geom[2]},{geom[3]}" if len(geom) >= 4 else ""
            writer.writerow(["route_segment", row.get("system", ""), row["route_class"], row["route_class"], row["layer"], row["file"], row.get("sheet", ""), coord, row["status"], row["length_drawing_units"]])
        for row in payload["equipment"]:
            writer.writerow(["equipment", row.get("system", ""), "", row["name"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{row.get('x')},{row.get('y')}", row["status"], row.get("category", "")])
        for row in payload["circuits"]:
            writer.writerow(["circuit", row.get("system", ""), "", row["circuit_id"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{row.get('x')},{row.get('y')}", row["status"], row.get("review_reason", "")])
        for row in payload["specs"]:
            writer.writerow(["spec", "", "", row["spec"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{row.get('x')},{row.get('y')}", row["status"], ""])
        for row in payload["labels"]:
            writer.writerow(["label", row.get("system", ""), row.get("label_type", ""), row["text"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{row.get('x')},{row.get('y')}", row["status"], ""])
        for row in payload["lightning"]:
            writer.writerow(["lightning", "lightning_protection", "", row["name"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{row.get('x')},{row.get('y')}", row["status"], row.get("review_reason", "")])
        for domain in ("fire_protection", "weak_current", "intelligent_building"):
            for row in payload.get(domain) or []:
                name = row.get("name") or row.get("system") or row.get("circuit_id") or row.get("text") or row.get("raw") or ""
                writer.writerow([row.get("group"), row.get("system", ""), row.get("route_class", ""), name, row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{row.get('x')},{row.get('y')}", row["status"], row.get("domain", "")])
        for row in payload["review"]:
            writer.writerow(["review", "", "", row["type"], "", "", "", "", "review", row["reason"]])


def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    parser = argparse.ArgumentParser(description="从 cad_scan 详情 JSON 提取电气识图中间数据。")
    parser.add_argument("inputs", nargs="+", help="cad_scan 生成的 --detail-json 文件")
    parser.add_argument("--out-dir", default="电气识图", help="输出目录")
    parser.add_argument("--rules", default=str(RULES_PATH), help="电气识图规则 JSON")
    args = parser.parse_args()

    rules = load_rules(Path(args.rules))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[str] = []
    for value in args.inputs:
        src = Path(value)
        if not src.exists():
            raise FileNotFoundError(src)
        payload = analyze_file(src, rules)
        payload = contractize_payload(payload, source=src.name)
        json_path = out_dir / f"{src.stem}.electrical.json"
        md_path = out_dir / f"{src.stem}.electrical.md"
        csv_path = out_dir / f"{src.stem}.electrical.csv"
        json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        write_markdown(payload, md_path)
        write_csv(payload, csv_path)
        outputs.extend([str(json_path), str(md_path), str(csv_path)])
        print(json.dumps({"source": str(src), "summary": payload["summary"], "outputs": [str(json_path), str(md_path), str(csv_path)]}, ensure_ascii=False))
    return 0 if outputs else 4


if __name__ == "__main__":
    raise SystemExit(main())
