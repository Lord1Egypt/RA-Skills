#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 cad_scan 详情 JSON 提炼结构识图中间数据和证据。

边界：只识别结构图纸类型、系统、构件、配筋、节点、轴网/标高与图层几何证据；
不输出混凝土体积、面积、长度汇总、钢筋吨位、接头数量、造价或结算量。
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / "packs" / "structural-geometry" / "rules.json"
from cad_contract import contractize_payload
from cad_common import compact, load_rules, match_rule


def data_file_name(data, value):
    if isinstance(value, dict):
        return compact(value.get("name") or value.get("path"))
    files = data.get("files") or []
    if isinstance(value, int) and 0 <= value < len(files):
        item = files[value]
        return compact(item.get("name") or item.get("path")) if isinstance(item, dict) else compact(item)
    return compact(value)


def evidence_of(record):
    ev = {"text": compact(record.get("text", "")), "layer": record.get("layer"), "kind": record.get("kind"), "space": record.get("space")}
    if record.get("x") is not None or record.get("y") is not None:
        ev["coord"] = [record.get("x"), record.get("y")]
    for key in ("file", "file_name", "sheet", "handle"):
        if record.get(key) is not None:
            ev[key] = record.get(key)
    return {k: v for k, v in ev.items() if v not in (None, "")}


def read_records(data):
    records = data.get("text_records") or data.get("texts") or []
    out = []
    for i, raw in enumerate(records):
        if not isinstance(raw, dict):
            continue
        text = compact(raw.get("text", ""))
        if not text:
            continue
        fname = raw.get("file_name")
        if fname is None:
            fname = data_file_name(data, raw.get("file"))
        out.append({"text": text, "layer": compact(raw.get("layer", "")), "kind": compact(raw.get("kind") or raw.get("type", "")), "space": raw.get("space"), "x": raw.get("x"), "y": raw.get("y"), "sheet": raw.get("sheet"), "file": raw.get("file"), "file_name": fname, "handle": raw.get("handle"), "_index": i})
    return out


def context_of(r):
    return (compact(r.get("file_name") or r.get("file")), r.get("sheet"), r.get("space"))


def sheet_for_point(data, x, y):
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


def iter_geometry(data):
    segment_files = data.get("geometry_segments") or []
    layer_files = data.get("geometry_layers") or []
    for fi, segments in enumerate(segment_files):
        layers = layer_files[fi] if fi < len(layer_files) else []
        for si, seg in enumerate(segments or []):
            if not isinstance(seg, (list, tuple)) or len(seg) < 4:
                continue
            yield fi, si, compact(layers[si]) if si < len(layers) else "", seg


def drawing_type_candidates(records, rules):
    out, seen = [], set()
    for rec in records:
        kind, _rule, pattern = match_rule(rec["text"], rules.get("view_rules") or [], "type")
        if not kind:
            continue
        key = (context_of(rec), kind)
        if key in seen:
            continue
        seen.add(key)
        out.append({"type": kind, "raw": rec["text"], "pattern": pattern, "confidence": float((rules.get("confidence") or {}).get("direct_label", 0.95)), "status": "candidate", "evidence": [evidence_of(rec)]})
    return out


def scale_unit_audit(records, rules):
    scale_re = re.compile(rules.get("scale_pattern") or r"1\s*[:：]\s*\d{1,4}")
    unit_patterns = rules.get("unit_patterns") or {}
    grouped = {}
    for rec in records:
        ctx = context_of(rec)
        item = grouped.setdefault(ctx, {"file": ctx[0], "sheet": ctx[1], "space": ctx[2], "scales": [], "units": [], "evidence": []})
        for m in scale_re.finditer(rec["text"]):
            scale = re.sub(r"\s+", "", m.group(0)).replace("：", ":")
            if scale not in item["scales"]:
                item["scales"].append(scale)
        for unit, patterns in unit_patterns.items():
            for pattern in patterns or []:
                if re.search(str(pattern), rec["text"], re.I):
                    if unit not in item["units"]:
                        item["units"].append(unit)
                    break
        if item["scales"] or item["units"]:
            item["evidence"].append(evidence_of(rec))
    out = []
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


def system_candidates(records, data, rules):
    out, seen = [], set()
    for rec in records:
        system, _rule, pattern = match_rule(rec["text"], rules.get("system_rules") or [], "system")
        if not system:
            continue
        key = (context_of(rec), system, rec.get("layer"), rec["text"])
        if key in seen:
            continue
        seen.add(key)
        out.append({"system": system, "raw": rec["text"], "pattern": pattern, "layer": rec.get("layer"), "file": rec.get("file_name"), "sheet": rec.get("sheet"), "confidence": float((rules.get("confidence") or {}).get("pattern_match", 0.78)), "status": "candidate", "evidence": [evidence_of(rec)]})
    for fi, _si, layer, _seg in iter_geometry(data):
        system, _rule, pattern = match_rule(layer, rules.get("system_rules") or [], "system")
        if not system:
            continue
        fname = data_file_name(data, fi)
        key = (fname, None, system, layer)
        if key in seen:
            continue
        seen.add(key)
        out.append({"system": system, "raw": layer, "pattern": pattern, "layer": layer, "file": fname, "confidence": float((rules.get("confidence") or {}).get("geometry_pattern", 0.86)), "status": "candidate", "evidence": [{"layer": layer, "file": fname, "kind": "geometry_layer"}]})
    return out


def member_candidates(records, rules):
    out, seen = [], set()
    code_re = re.compile(rules.get("member_code_pattern") or r"(?<![A-Za-z0-9])([A-Z]{1,4}\d{1,4}[A-Za-z]?)(?![A-Za-z0-9])", re.I)
    for rec in records:
        category, rule, pattern = match_rule(f"{rec['text']} {rec.get('layer','')}", rules.get("member_rules") or [], "category")
        if not category:
            continue
        codes = list(code_re.finditer(rec["text"]))
        code = codes[0].group(0).upper() if codes else ""
        key = (context_of(rec), category, code, rec.get("layer"), rec.get("x"), rec.get("y"))
        if key in seen:
            continue
        seen.add(key)
        out.append({"type": "member", "name": code or rec["text"], "code": code, "category": category, "system": (rule or {}).get("system") or "", "pattern": pattern, "layer": rec.get("layer"), "file": rec.get("file_name"), "sheet": rec.get("sheet"), "x": rec.get("x"), "y": rec.get("y"), "confidence": float((rules.get("confidence") or {}).get("direct_label", 0.95)) if rec.get("kind") in {"INSERT", "ATTRIB"} else float((rules.get("confidence") or {}).get("pattern_match", 0.78)), "status": "candidate", "evidence": [evidence_of(rec)]})
    return out


def rebar_candidates(records, rules):
    out, seen = [], set()
    regex = re.compile(rules.get("rebar_pattern") or r"(?<![A-Za-z0-9])([A-Z]?\d{1,3}[A-Z]?(?:@|[-@])\d{2,3}(?:\(\d+\))?|[A-Z]{2,5}\d|\d+\s*[xX×])", re.I)
    for rec in records:
        for m in regex.finditer(rec["text"]):
            value = compact(m.group(0)).upper()
            key = (context_of(rec), value, rec.get("layer"), rec.get("x"), rec.get("y"))
            if key in seen:
                continue
            seen.add(key)
            out.append({"type": "rebar", "rebar_spec": value, "layer": rec.get("layer"), "file": rec.get("file_name"), "sheet": rec.get("sheet"), "x": rec.get("x"), "y": rec.get("y"), "confidence": float((rules.get("confidence") or {}).get("direct_label", 0.95)), "status": "candidate", "evidence": [evidence_of(rec)]})
    return out


def node_candidates(records, rules):
    out, seen = [], set()
    regex = re.compile(rules.get("node_pattern") or r"(?<![A-Za-z0-9])(JD|SD|YD|节点)\s*[-_]?\s*\d{1,4}[A-Za-z]?", re.I)
    for rec in records:
        for m in regex.finditer(rec["text"]):
            value = compact(m.group(0)).upper()
            key = (context_of(rec), value, rec.get("layer"), rec.get("x"), rec.get("y"))
            if key in seen:
                continue
            seen.add(key)
            out.append({"type": "node", "node_id": value, "layer": rec.get("layer"), "file": rec.get("file_name"), "sheet": rec.get("sheet"), "x": rec.get("x"), "y": rec.get("y"), "confidence": float((rules.get("confidence") or {}).get("direct_label", 0.95)), "status": "candidate", "evidence": [evidence_of(rec)]})
    return out


def grid_candidates(records, rules):
    out, seen = [], set()
    regex = re.compile(rules.get("grid_pattern") or r"(?<![A-Za-z0-9])([A-Z]{1,3}\d{0,3}|[一二三四五六七八九十]+)|\s*(?:轴|标高)\s*[-+]?\d+(?:\.\d+)?", re.I)
    for rec in records:
        for m in regex.finditer(rec["text"]):
            value = compact(m.group(0))
            if not value:
                continue
            key = (context_of(rec), value, rec.get("layer"), rec.get("x"), rec.get("y"))
            if key in seen:
                continue
            seen.add(key)
            out.append({"type": "grid", "value": value, "layer": rec.get("layer"), "file": rec.get("file_name"), "sheet": rec.get("sheet"), "x": rec.get("x"), "y": rec.get("y"), "confidence": float((rules.get("confidence") or {}).get("pattern_match", 0.78)), "status": "candidate", "evidence": [evidence_of(rec)]})
    return out


def structural_geometry(data, rules):
    out, unmatched = [], Counter()
    for fi, _si, layer, seg in iter_geometry(data):
        fname = data_file_name(data, fi)
        x1, y1, x2, y2 = (round(float(v), 3) for v in seg[:4])
        category, rule, pattern = match_rule(f"{layer}", rules.get("layer_rules") or [], "category")
        if category:
            out.append({"type": "structural_geometry", "category": category, "system": (rule or {}).get("system") or "", "pattern": pattern, "layer": layer, "file": fname, "sheet": sheet_for_point(data, (x1 + x2) / 2, (y1 + y2) / 2), "geometry": [x1, y1, x2, y2], "confidence": float((rules.get("confidence") or {}).get("geometry_pattern", 0.86)), "status": "candidate", "evidence": [{"layer": layer, "kind": "geometry", "coord": [x1, y1, x2, y2], "file": fname, "sheet": sheet_for_point(data, (x1 + x2) / 2, (y1 + y2) / 2)}]})
        else:
            unmatched[layer or "<空图层>"] += 1
    return out, unmatched


def analyze_file(path, rules):
    data = json.loads(path.read_text(encoding="utf-8"))
    records = read_records(data)
    views = drawing_type_candidates(records, rules)
    audit = scale_unit_audit(records, rules)
    systems = system_candidates(records, data, rules)
    members = member_candidates(records, rules)
    rebars = rebar_candidates(records, rules)
    nodes = node_candidates(records, rules)
    grids = grid_candidates(records, rules)
    geometry, unmatched_layers = structural_geometry(data, rules)
    review = []
    if not views:
        review.append({"type": "drawing_type", "reason": "未识别到结构图纸类型文字", "evidence": []})
    for row in audit:
        if row.get("status") != "candidate":
            review.append({"type": "scale_unit", "reason": row.get("review_reason") or "比例或单位需确认", "evidence": row.get("evidence", [])})
    if not data.get("geometry_segments") or not data.get("geometry_layers"):
        review.append({"type": "input_geometry", "reason": "输入缺少 geometry_segments 或 geometry_layers；请用 cad_scan --with-geom --with-geom-layer", "evidence": []})
    for layer, count in unmatched_layers.most_common(50):
        review.append({"type": "structural_layer", "reason": f"结构图层未分类：{layer}（{count} 段）", "evidence": [{"layer": layer}]})
    summary = {"drawing_types": len(views), "systems": len(systems), "members": len(members), "rebars": len(rebars), "nodes": len(nodes), "grids": len(grids), "structural_geometry": len(geometry), "review_items": len(review)}
    return {"schema": "cad-structural-geometry/v1", "source_file": path.name, "summary": summary, "drawing_types": views, "scale_unit_audit": audit, "systems": systems, "members": members, "rebars": rebars, "nodes": nodes, "grids": grids, "structural_geometry": geometry, "review": review, "boundary": "只输出结构识图候选、证据和复核项；不输出混凝土体积、钢筋吨位、长度汇总、材料量、造价或结算量。"}


def write_markdown(payload, path):
    s = payload["summary"]
    lines = ["# 结构识图 / 中间数据复核", "", f"- 源文件：`{payload['source_file']}`", f"- 候选：图纸类型 {s['drawing_types']}，系统 {s['systems']}，构件 {s['members']}，配筋 {s['rebars']}，节点 {s['nodes']}，轴网/标高 {s['grids']}，几何段 {s['structural_geometry']}，待复核 {s['review_items']}", "", "## 构件候选", ""]
    if payload["members"]:
        lines += ["| 构件 | 类别 | 系统 | 图层 | 状态 |", "|---|---|---|---|---|"]
        for row in payload["members"][:120]:
            lines.append(f"| {row['name']} | {row['category']} | {row.get('system','')} | {row.get('layer','')} | {row['status']} |")
    else:
        lines.append("无")
    lines += ["", "## 配筋候选", ""]
    if payload["rebars"]:
        lines += ["| 规格 | 图层 |", "|---|---|"]
        for row in payload["rebars"][:120]:
            lines.append(f"| {row['rebar_spec']} | {row.get('layer','')} |")
    else:
        lines.append("无")
    lines += ["", "## 节点与轴网", ""]
    if payload["nodes"] or payload["grids"]:
        lines += ["| 类型 | 值 | 图层 |", "|---|---|---|"]
        for row in payload["nodes"][:80]:
            lines.append(f"| node | {row['node_id']} | {row.get('layer','')} |")
        for row in payload["grids"][:80]:
            lines.append(f"| grid | {row['value']} | {row.get('layer','')} |")
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


def write_csv(payload, path):
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
        for row in payload["rebars"]:
            writer.writerow(["rebar", "", "", row["rebar_spec"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{row.get('x')},{row.get('y')}", row["status"], ""])
        for row in payload["nodes"]:
            writer.writerow(["node", "", "", row["node_id"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{row.get('x')},{row.get('y')}", row["status"], ""])
        for row in payload["grids"]:
            writer.writerow(["grid", "", "", row["value"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{row.get('x')},{row.get('y')}", row["status"], ""])
        for row in payload["structural_geometry"]:
            geom = row["geometry"]
            writer.writerow(["structural_geometry", row["category"], row.get("system", ""), row["category"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{geom[0]},{geom[1]}->{geom[2]},{geom[3]}", row["status"], row.get("review_reason", "")])
        for row in payload["review"]:
            writer.writerow(["review", "", "", row["type"], "", "", "", "", "review", row["reason"]])


def main():
    import pyboot
    pyboot.ensure_utf8_io()
    parser = argparse.ArgumentParser(description="从 cad_scan 详情 JSON 提取结构识图中间数据。")
    parser.add_argument("inputs", nargs="+")
    parser.add_argument("--out-dir", default="结构识图")
    parser.add_argument("--rules", default=str(RULES_PATH))
    args = parser.parse_args()
    rules = load_rules(Path(args.rules))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    outputs = []
    for value in args.inputs:
        src = Path(value)
        if not src.exists():
            raise FileNotFoundError(src)
        payload = analyze_file(src, rules)
        payload = contractize_payload(payload, source=src.name)
        jp, mp, cp = out_dir / f"{src.stem}.structural.json", out_dir / f"{src.stem}.structural.md", out_dir / f"{src.stem}.structural.csv"
        jp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        write_markdown(payload, mp)
        write_csv(payload, cp)
        outputs.append(f"已写出 {jp}")
    print(json.dumps({"source": [str(x) for x in args.inputs], "summary": payload["summary"], "outputs": [str(x) for x in (jp, mp, cp)]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
