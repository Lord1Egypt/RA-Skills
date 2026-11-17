#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 cad_scan 详情 JSON 提炼市政专业识图中间数据和证据。

边界：只识别图纸类型、专业系统、道路/桥隧/管网构件、材料、桩号、标高、
坐标和图层几何证据；不输出工程量、材料量、造价或结算量。
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from cad_steel_geometry import (
    compact,
    connectivity_audit as _steel_connectivity_audit,
    context_of,
    data_file_name,
    evidence_of,
    iter_geometry,
    load_rules,
    match_rule,
    pattern_hit,
    read_records,
    scale_unit_audit,
    segment_length,
    sheet_for_point,
)

ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / "packs" / "municipal-geometry" / "rules.json"
from cad_contract import contractize_payload


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


def _negative_hit(text: Any, rule: dict[str, Any]) -> bool:
    value = compact(text).upper()
    return any(pattern_hit(value, pattern) for pattern in (rule.get("negative_patterns") or []))


def system_candidates(records: list[dict[str, Any]], data: dict[str, Any], rules: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    system_rules = rules.get("system_rules") or []
    for rec in records:
        system, rule, pattern = match_rule(rec["text"], system_rules, "system")
        if not system or _negative_hit(rec["text"], rule):
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
        system, rule, pattern = match_rule(layer, system_rules, "system")
        if not system or _negative_hit(layer, rule):
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


def component_candidates(records: list[dict[str, Any]], rules: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    for rec in records:
        category, rule, pattern = match_rule(f"{rec['text']} {rec.get('layer', '')}", rules.get("component_rules") or [], "category")
        if not category:
            continue
        key = (context_of(rec), category, rec["text"], rec.get("layer"), rec.get("x"), rec.get("y"))
        if key in seen:
            continue
        seen.add(key)
        out.append({
            "type": "component",
            "category": category,
            "system": (rule or {}).get("system") or "",
            "raw": rec["text"],
            "pattern": pattern,
            "layer": rec.get("layer"),
            "file": rec.get("file_name"),
            "sheet": rec.get("sheet"),
            "x": rec.get("x"),
            "y": rec.get("y"),
            "confidence": float((rules.get("confidence") or {}).get("pattern_match", 0.78)),
            "status": "candidate",
            "review_reason": "",
            "evidence": [evidence_of(rec)],
        })
    return out


def pipe_candidates(records: list[dict[str, Any]], rules: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    size_re = re.compile(rules.get("pipe_size_pattern") or r"(?:DN|De|D|d|Φ|φ)\s*\d{2,4}", re.I)
    for rec in records:
        system, _rule, pattern = match_rule(f"{rec['text']} {rec.get('layer', '')}", rules.get("pipe_rules") or [], "system")
        if not system:
            continue
        sizes = [compact(m.group(0)) for m in size_re.finditer(rec["text"])]
        key = (context_of(rec), system, rec["text"], rec.get("layer"), rec.get("x"), rec.get("y"))
        if key in seen:
            continue
        seen.add(key)
        out.append({
            "type": "pipe",
            "system": system,
            "raw": rec["text"],
            "pipe_size": sizes[0] if sizes else "",
            "pattern": pattern,
            "layer": rec.get("layer"),
            "file": rec.get("file_name"),
            "sheet": rec.get("sheet"),
            "x": rec.get("x"),
            "y": rec.get("y"),
            "confidence": float((rules.get("confidence") or {}).get("pattern_match", 0.78)),
            "status": "candidate" if sizes else "review",
            "review_reason": "" if sizes else "识别到市政管道但未提取到管径或断面尺寸",
            "evidence": [evidence_of(rec)],
        })
    return out


def material_candidates(records: list[dict[str, Any]], rules: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    for category, patterns in (rules.get("material_patterns") or {}).items():
        for pattern in patterns or []:
            regex = re.compile(str(pattern), re.I)
            for rec in records:
                for match in regex.finditer(rec["text"]):
                    value = compact(match.group(0))
                    key = (context_of(rec), category, value, rec.get("layer"), rec.get("x"), rec.get("y"))
                    if key in seen:
                        continue
                    seen.add(key)
                    out.append({
                        "type": "material",
                        "category": category,
                        "value": value,
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


def reference_candidates(records: list[dict[str, Any]], rules: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    regexes = [re.compile(str(p), re.I) for p in (rules.get("reference_patterns") or [])]
    for rec in records:
        for regex in regexes:
            for match in regex.finditer(rec["text"]):
                value = compact(match.group(0))
                key = (context_of(rec), value, rec.get("layer"), rec.get("x"), rec.get("y"))
                if key in seen:
                    continue
                seen.add(key)
                out.append({
                    "type": "reference",
                    "value": value,
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


def label_candidates(records: list[dict[str, Any]], rules: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    specs = [
        ("station", rules.get("station_pattern")),
        ("elevation", rules.get("elevation_pattern")),
        ("coordinate", rules.get("coordinate_pattern")),
        ("pipe_size", rules.get("pipe_size_pattern")),
        ("slope", rules.get("slope_pattern")),
        ("dimension", rules.get("dimension_pattern")),
    ]
    for label_type, pattern in specs:
        if not pattern:
            continue
        regex = re.compile(str(pattern), re.I)
        for rec in records:
            for match in regex.finditer(rec["text"]):
                value = compact(match.group(0))
                key = (context_of(rec), label_type, value, rec.get("layer"), rec.get("x"), rec.get("y"))
                if key in seen:
                    continue
                seen.add(key)
                out.append({
                    "type": "label",
                    "label_type": label_type,
                    "value": value,
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


def municipal_geometry(data: dict[str, Any], rules: dict[str, Any]) -> tuple[list[dict[str, Any]], Counter]:
    out: list[dict[str, Any]] = []
    unmatched: Counter = Counter()
    layer_patterns = [str(x).upper() for x in (rules.get("municipal_layer_patterns") or [])]
    for fi, _si, layer, seg in iter_geometry(data):
        upper_layer = compact(layer).upper()
        if not layer_patterns or not any(token in upper_layer for token in layer_patterns):
            continue
        category, rule, pattern = match_rule(layer, rules.get("component_rules") or [], "category")
        if not category:
            system, system_rule, system_pattern = match_rule(layer, rules.get("system_rules") or [], "system")
            if system:
                category = "unclassified_municipal"
                rule = system_rule
                pattern = system_pattern
        try:
            x1, y1, x2, y2 = (float(v) for v in seg[:4])
        except (TypeError, ValueError):
            continue
        file_name = data_file_name(data, fi)
        sheet = sheet_for_point(data, (x1 + x2) / 2.0, (y1 + y2) / 2.0)
        status = "candidate" if category and category != "unclassified_municipal" else "review"
        out.append({
            "type": "municipal_geometry",
            "category": category or "unclassified_municipal",
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
            "review_reason": "" if status == "candidate" else "市政图层未映射到构件类别",
            "evidence": [{"layer": layer, "kind": "geometry", "coord": [round(x1, 3), round(y1, 3), round(x2, 3), round(y2, 3)], "file": file_name, "sheet": sheet}],
        })
        if status != "candidate":
            unmatched[layer or "<空图层>"] += 1
    return out, unmatched


def connectivity_audit(geometry: list[dict[str, Any]], tolerance: float = 5.0, max_segments: int = 5000) -> dict[str, Any]:
    result = _steel_connectivity_audit(geometry, tolerance, max_segments)
    result["boundary"] = "只做端点吸附和市政构件连通性候选；不输出长度汇总、面积、数量、工程量或材料量。"
    return result


def analyze_file(path: Path, rules: dict[str, Any], snap_tolerance: float) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    records = read_records(data)
    views = drawing_type_candidates(records, rules)
    systems = system_candidates(records, data, rules)
    audit = scale_unit_audit(records, rules)
    components = component_candidates(records, rules)
    pipes = pipe_candidates(records, rules)
    materials = material_candidates(records, rules)
    references = reference_candidates(records, rules)
    labels = label_candidates(records, rules)
    geometry, unmatched_layers = municipal_geometry(data, rules)
    connectivity = connectivity_audit(geometry, snap_tolerance)
    review: list[dict[str, Any]] = []
    if not views:
        review.append({"type": "drawing_type", "reason": "未识别到市政图纸类型文字", "evidence": []})
    for row in audit:
        if row.get("status") != "candidate":
            review.append({"type": "scale_unit", "reason": row.get("review_reason") or "比例或单位需确认", "evidence": row.get("evidence", [])})
    if not data.get("geometry_segments") or not data.get("geometry_layers"):
        review.append({"type": "input_geometry", "reason": "输入缺少 geometry_segments 或 geometry_layers；请用 cad_scan --with-geom --with-geom-layer", "evidence": []})
    for layer, count in unmatched_layers.most_common(50):
        review.append({"type": "municipal_layer", "reason": f"市政图层未分类：{layer}（{count} 段）", "evidence": [{"layer": layer}]})
    if pipes and not any(row.get("status") == "candidate" for row in pipes):
        review.append({"type": "pipe_size", "reason": "识别到市政管道但未提取到管径或断面尺寸", "evidence": []})
    if components and not materials:
        review.append({"type": "material_schedule", "reason": "识别到市政构件但未提取到材料或做法", "evidence": []})
    summary = {
        "drawing_types": len(views),
        "systems": len(systems),
        "components": len(components),
        "pipe_candidates": len(pipes),
        "materials": len(materials),
        "references": len(references),
        "labels": len(labels),
        "geometry_segments": len(geometry),
        "connectivity_open_endpoints": connectivity["summary"]["open_endpoints"],
        "connectivity_junctions": connectivity["summary"]["junction_candidates"],
        "review_items": len(review),
    }
    return {
        "schema": "cad-municipal-geometry/v1",
        "source_file": path.name,
        "summary": summary,
        "drawing_types": views,
        "scale_unit_audit": audit,
        "systems": systems,
        "components": components,
        "pipe_network": pipes,
        "materials": materials,
        "references": references,
        "labels": labels,
        "municipal_geometry": geometry,
        "connectivity": connectivity,
        "review": review,
        "boundary": "只输出市政专业识图候选、证据和连通性审计；不输出面积、长度汇总、数量、材料量、造价或结算量。",
    }


def write_markdown(payload: dict[str, Any], path: Path) -> None:
    s = payload["summary"]
    lines = [
        "# 市政专业识图 / 中间数据复核",
        "",
        f"- 源文件：`{payload['source_file']}`",
        f"- 候选：图纸类型 {s['drawing_types']}，专业系统 {s['systems']}，构件 {s['components']}，管道 {s['pipe_candidates']}，材料 {s['materials']}，引用 {s['references']}，标注 {s['labels']}，几何段 {s['geometry_segments']}，待复核 {s['review_items']}",
        f"- 连通性：开放端点 {s['connectivity_open_endpoints']}，汇聚节点 {s['connectivity_junctions']}",
        "",
        "## 图纸类型",
        "",
    ]
    if payload["drawing_types"]:
        lines += ["| 类型 | 原文 | 图层 |", "|---|---|---|"]
        for row in payload["drawing_types"]:
            ev = (row.get("evidence") or [{}])[0]
            lines.append(f"| {row['type']} | {row['raw']} | {ev.get('layer', '')} |")
    else:
        lines.append("无")
    lines += ["", "## 专业系统", ""]
    if payload["systems"]:
        lines += ["| 系统 | 图层/原文 | 证据 |", "|---|---|---|"]
        for row in payload["systems"][:120]:
            lines.append(f"| {row['system']} | {row.get('layer') or row['raw']} | {row.get('pattern', '')} |")
    else:
        lines.append("无")
    lines += ["", "## 构件与管网", ""]
    if payload["components"] or payload["pipe_network"]:
        lines += ["| 类别 | 系统 | 原文 | 图层 |", "|---|---|---|---|"]
        for row in payload["components"][:120]:
            lines.append(f"| {row['category']} | {row.get('system', '')} | {row['raw']} | {row.get('layer', '')} |")
        for row in payload["pipe_network"][:120]:
            lines.append(f"| 管道/{row['system']} | {row['system']} | {row['raw']} | {row.get('layer', '')} |")
    else:
        lines.append("无")
    lines += ["", "## 标注与定位", ""]
    if payload["labels"]:
        lines += ["| 类型 | 值 | 图层 |", "|---|---|---|"]
        for row in payload["labels"][:160]:
            lines.append(f"| {row['label_type']} | {row['value']} | {row.get('layer', '')} |")
    else:
        lines.append("无")
    lines += ["", "## 材料与引用", ""]
    if payload["materials"] or payload["references"]:
        lines += ["| 类型 | 值 | 图层 |", "|---|---|---|"]
        for row in payload["materials"][:120]:
            lines.append(f"| {row['category']} | {row['value']} | {row.get('layer', '')} |")
        for row in payload["references"][:120]:
            lines.append(f"| reference | {row['value']} | {row.get('layer', '')} |")
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
        for row in payload["components"]:
            writer.writerow(["component", row["category"], row.get("system", ""), row["raw"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{row.get('x')},{row.get('y')}", row["status"], row.get("review_reason", "")])
        for row in payload["pipe_network"]:
            writer.writerow(["pipe", row["system"], row["system"], row.get("pipe_size", ""), row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{row.get('x')},{row.get('y')}", row["status"], row.get("review_reason", "")])
        for row in payload["materials"]:
            writer.writerow(["material", row["category"], "", row["value"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{row.get('x')},{row.get('y')}", row["status"], row["raw"]])
        for row in payload["references"]:
            writer.writerow(["reference", "", "", row["value"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{row.get('x')},{row.get('y')}", row["status"], row["raw"]])
        for row in payload["labels"]:
            writer.writerow(["label", row["label_type"], "", row["value"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{row.get('x')},{row.get('y')}", row["status"], row["raw"]])
        for row in payload["municipal_geometry"]:
            geom = row["geometry"]
            writer.writerow(["municipal_geometry", row["category"], row.get("system", ""), row["category"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{geom[0]},{geom[1]}->{geom[2]},{geom[3]}", row["status"], row.get("review_reason", "")])
        for row in payload["review"]:
            writer.writerow(["review", "", "", row["type"], "", "", "", "", "review", row["reason"]])


def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    parser = argparse.ArgumentParser(description="从 cad_scan 详情 JSON 提取市政专业识图中间数据。")
    parser.add_argument("inputs", nargs="+", help="cad_scan 生成的 --detail-json 文件")
    parser.add_argument("--out-dir", default="市政识图", help="输出目录")
    parser.add_argument("--rules", default=str(RULES_PATH), help="市政识图规则 JSON")
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
        json_path = out_dir / f"{src.stem}.municipal.json"
        md_path = out_dir / f"{src.stem}.municipal.md"
        csv_path = out_dir / f"{src.stem}.municipal.csv"
        json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        write_markdown(payload, md_path)
        write_csv(payload, csv_path)
        outputs.extend([str(json_path), str(md_path), str(csv_path)])
        print(json.dumps({"source": str(src), "summary": payload["summary"], "outputs": [str(json_path), str(md_path), str(csv_path)]}, ensure_ascii=False))
    return 0 if outputs else 4


if __name__ == "__main__":
    raise SystemExit(main())
