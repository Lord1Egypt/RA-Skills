#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 cad_scan 详情 JSON 提炼总图/场地识图中间数据和证据。

边界：只识别总图、竖向、管线、道路、挡墙/边坡、停车、景观图纸类型/系统/构件/标注；
不输出土方量、道路面积、管线长度、材料量、造价或结算量。
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
RULES_PATH = ROOT / "packs" / "site-geometry" / "rules.json"
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
    sfiles = data.get("geometry_segments") or []
    lfiles = data.get("geometry_layers") or []
    for fi, segs in enumerate(sfiles):
        layers = lfiles[fi] if fi < len(lfiles) else []
        for si, seg in enumerate(segs or []):
            if not isinstance(seg, (list, tuple)) or len(seg) < 4:
                continue
            yield fi, si, compact(layers[si]) if si < len(layers) else "", seg


def drawing_type_candidates(records, rules):
    out, seen = [], set()
    for rec in records:
        kind, _r, pat = match_rule(rec["text"], rules.get("view_rules") or [], "type")
        if not kind:
            continue
        key = (context_of(rec), kind)
        if key in seen:
            continue
        seen.add(key)
        out.append({"type": kind, "raw": rec["text"], "pattern": pat, "confidence": float((rules.get("confidence") or {}).get("direct_label", 0.95)), "status": "candidate", "evidence": [evidence_of(rec)]})
    return out


def scale_unit_audit(records, rules):
    scale_re = re.compile(rules.get("scale_pattern") or r"1\s*[:：]\s*\d{1,4}")
    ups = rules.get("unit_patterns") or {}
    grouped = {}
    for rec in records:
        ctx = context_of(rec)
        item = grouped.setdefault(ctx, {"file": ctx[0], "sheet": ctx[1], "space": ctx[2], "scales": [], "units": [], "evidence": []})
        for m in scale_re.finditer(rec["text"]):
            sc = re.sub(r"\s+", "", m.group(0)).replace("：", ":")
            if sc not in item["scales"]:
                item["scales"].append(sc)
        for unit, pats in ups.items():
            for pat in pats or []:
                if re.search(str(pat), rec["text"], re.I) and unit not in item["units"]:
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
        system, _r, pat = match_rule(rec["text"], rules.get("system_rules") or [], "system")
        if not system:
            continue
        key = (context_of(rec), system, rec.get("layer"), rec["text"])
        if key in seen:
            continue
        seen.add(key)
        out.append({"system": system, "raw": rec["text"], "pattern": pat, "layer": rec.get("layer"), "file": rec.get("file_name"), "sheet": rec.get("sheet"), "confidence": float((rules.get("confidence") or {}).get("pattern_match", 0.78)), "status": "candidate", "evidence": [evidence_of(rec)]})
    for fi, _si, layer, _seg in iter_geometry(data):
        system, _r, pat = match_rule(layer, rules.get("system_rules") or [], "system")
        if not system:
            continue
        fname = data_file_name(data, fi)
        key = (fname, None, system, layer)
        if key in seen:
            continue
        seen.add(key)
        out.append({"system": system, "raw": layer, "pattern": pat, "layer": layer, "file": fname, "confidence": float((rules.get("confidence") or {}).get("geometry_pattern", 0.86)), "status": "candidate", "evidence": [{"layer": layer, "file": fname, "kind": "geometry_layer"}]})
    return out


def component_candidates(records, rules):
    out, seen = [], set()
    for rec in records:
        category, rule, pat = match_rule(f"{rec['text']} {rec.get('layer','')}", rules.get("component_rules") or [], "category")
        if not category:
            continue
        key = (context_of(rec), category, rec["text"], rec.get("layer"), rec.get("x"), rec.get("y"))
        if key in seen:
            continue
        seen.add(key)
        out.append({"type": "component", "category": category, "system": (rule or {}).get("system") or "", "raw": rec["text"], "pattern": pat, "layer": rec.get("layer"), "file": rec.get("file_name"), "sheet": rec.get("sheet"), "x": rec.get("x"), "y": rec.get("y"), "confidence": float((rules.get("confidence") or {}).get("direct_label", 0.95)) if rec.get("kind") in {"INSERT", "ATTRIB"} else float((rules.get("confidence") or {}).get("pattern_match", 0.78)), "status": "candidate", "evidence": [evidence_of(rec)]})
    return out


def reference_candidates(records, rules):
    out, seen = [], set()
    combos = [
        ("chainage", rules.get("chainage_pattern")),
        ("coordinate", rules.get("coordinate_pattern")),
        ("elevation", rules.get("elevation_pattern")),
    ]
    for ref_type, pat in combos:
        if not pat:
            continue
        regex = re.compile(str(pat), re.I)
        for rec in records:
            for m in regex.finditer(rec["text"]):
                value = compact(m.group(0))
                key = (context_of(rec), ref_type, value, rec.get("layer"), rec.get("x"), rec.get("y"))
                if key in seen:
                    continue
                seen.add(key)
                out.append({"type": "reference", "reference_type": ref_type, "value": value, "layer": rec.get("layer"), "file": rec.get("file_name"), "sheet": rec.get("sheet"), "x": rec.get("x"), "y": rec.get("y"), "confidence": float((rules.get("confidence") or {}).get("direct_label", 0.95)), "status": "candidate", "evidence": [evidence_of(rec)]})
    return out


def site_geometry(data, rules):
    out, unmatched = [], Counter()
    for fi, _si, layer, seg in iter_geometry(data):
        fname = data_file_name(data, fi)
        x1, y1, x2, y2 = (round(float(v), 3) for v in seg[:4])
        category, rule, pat = match_rule(f"{layer}", rules.get("layer_rules") or [], "category")
        if category:
            out.append({"type": "site_geometry", "category": category, "system": (rule or {}).get("system") or "", "pattern": pat, "layer": layer, "file": fname, "sheet": sheet_for_point(data, (x1 + x2) / 2, (y1 + y2) / 2), "geometry": [x1, y1, x2, y2], "confidence": float((rules.get("confidence") or {}).get("geometry_pattern", 0.86)), "status": "candidate", "evidence": [{"layer": layer, "kind": "geometry", "coord": [x1, y1, x2, y2], "file": fname, "sheet": sheet_for_point(data, (x1 + x2) / 2, (y1 + y2) / 2)}]})
        else:
            unmatched[layer or "<空图层>"] += 1
    return out, unmatched


def analyze_file(path, rules):
    data = json.loads(path.read_text(encoding="utf-8"))
    records = read_records(data)
    views = drawing_type_candidates(records, rules)
    audit = scale_unit_audit(records, rules)
    systems = system_candidates(records, data, rules)
    components = component_candidates(records, rules)
    references = reference_candidates(records, rules)
    geometry, unmatched_layers = site_geometry(data, rules)
    review = []
    if not views:
        review.append({"type": "drawing_type", "reason": "未识别到总图/场地图纸类型文字", "evidence": []})
    for row in audit:
        if row.get("status") != "candidate":
            review.append({"type": "scale_unit", "reason": row.get("review_reason") or "比例或单位需确认", "evidence": row.get("evidence", [])})
    if not data.get("geometry_segments") or not data.get("geometry_layers"):
        review.append({"type": "input_geometry", "reason": "输入缺少 geometry_segments 或 geometry_layers；请用 cad_scan --with-geom --with-geom-layer", "evidence": []})
    for layer, count in unmatched_layers.most_common(50):
        review.append({"type": "site_layer", "reason": f"场地图层未分类：{layer}（{count} 段）", "evidence": [{"layer": layer}]})
    summary = {"drawing_types": len(views), "systems": len(systems), "components": len(components), "references": len(references), "site_geometry": len(geometry), "review_items": len(review)}
    return {"schema": "cad-site-geometry/v1", "source_file": path.name, "summary": summary, "drawing_types": views, "scale_unit_audit": audit, "systems": systems, "components": components, "references": references, "site_geometry": geometry, "review": review, "boundary": "只输出总图/场地识图候选、证据和复核项；不输出土方量、道路面积、管线长度、材料量、造价或结算量。"}


def write_markdown(payload, path):
    s = payload["summary"]
    lines = ["# 总图/场地识图 / 中间数据复核", "", f"- 源文件：`{payload['source_file']}`", f"- 候选：图纸类型 {s['drawing_types']}，系统 {s['systems']}，构件 {s['components']}，标注 {s['references']}，几何段 {s['site_geometry']}，待复核 {s['review_items']}", "", "## 构件候选", ""]
    if payload["components"]:
        lines += ["| 构件 | 类别 | 系统 | 图层 |", "|---|---|---|---|"]
        for row in payload["components"][:120]:
            lines.append(f"| {row['raw']} | {row['category']} | {row.get('system','')} | {row.get('layer','')} |")
    else:
        lines.append("无")
    lines += ["", "## 标注候选", ""]
    if payload["references"]:
        lines += ["| 类型 | 值 | 图层 |", "|---|---|---|"]
        for row in payload["references"][:120]:
            lines.append(f"| {row['reference_type']} | {row['value']} | {row.get('layer','')} |")
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
        for row in payload["components"]:
            writer.writerow(["component", row["category"], row.get("system", ""), row["raw"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{row.get('x')},{row.get('y')}", row["status"], row.get("pattern", "")])
        for row in payload["references"]:
            writer.writerow(["reference", row["reference_type"], "", row["value"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{row.get('x')},{row.get('y')}", row["status"], ""])
        for row in payload["site_geometry"]:
            geom = row["geometry"]
            writer.writerow(["site_geometry", row["category"], row.get("system", ""), row["category"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{geom[0]},{geom[1]}->{geom[2]},{geom[3]}", row["status"], row.get("review_reason", "")])
        for row in payload["review"]:
            writer.writerow(["review", "", "", row["type"], "", "", "", "", "review", row["reason"]])


def main():
    import pyboot
    pyboot.ensure_utf8_io()
    parser = argparse.ArgumentParser(description="从 cad_scan 详情 JSON 提取总图/场地识图中间数据。")
    parser.add_argument("inputs", nargs="+")
    parser.add_argument("--out-dir", default="场地识图")
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
        jp, mp, cp = out_dir / f"{src.stem}.site.json", out_dir / f"{src.stem}.site.md", out_dir / f"{src.stem}.site.csv"
        jp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        write_markdown(payload, mp)
        write_csv(payload, cp)
    print(json.dumps({"source": [str(x) for x in args.inputs], "summary": payload["summary"], "outputs": [str(x) for x in (jp, mp, cp)]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
