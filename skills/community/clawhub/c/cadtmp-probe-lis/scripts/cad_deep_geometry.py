#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 cad_scan 详情 JSON 提炼深化/专项识图中间数据（给排水暖通/精装修/幕墙/人防/预制装配）。

边界：只识别图纸类型、系统、构件、标注、几何图层证据；不输出工程量、材料量、造价或结算量，
所有输出保持 final_quantity=false。
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKS = {
    "hvac_plumbing": {
        "rules": "packs/hvac-plumbing-geometry/rules.json",
        "schema": "cad-hvac-plumbing-geometry/v1",
        "geo_key": "hvac_plumbing_geometry",
        "label": "给排水/暖通深化识图",
        "suffix": "hvac_plumbing",
        "boundary": "只输出给排水/暖通深化识图候选、证据和复核项；不输出管道展开长度、风管面积、材料量、造价或结算量。",
        "review_type": "hvac_layer",
    },
    "interior_finish": {
        "rules": "packs/interior-finish-geometry/rules.json",
        "schema": "cad-interior-finish-geometry/v1",
        "geo_key": "interior_finish_geometry",
        "label": "精装修/室内深化识图",
        "suffix": "interior_finish",
        "boundary": "只输出精装修/室内深化识图候选、证据和复核项；不输出饰面面积、排版数量、材料量、造价或结算量。",
        "review_type": "interior_layer",
    },
    "curtain_wall": {
        "rules": "packs/curtain-wall-geometry/rules.json",
        "schema": "cad-curtain-wall-geometry/v1",
        "geo_key": "curtain_wall_geometry",
        "label": "幕墙专业识图",
        "suffix": "curtain_wall",
        "boundary": "只输出幕墙识图候选、证据和复核项；不输出幕墙面积、板块数量、材料量、造价或结算量。",
        "review_type": "curtain_wall_layer",
    },
    "civil_defense": {
        "rules": "packs/civil-defense-geometry/rules.json",
        "schema": "cad-civil-defense-geometry/v1",
        "geo_key": "civil_defense_geometry",
        "label": "人防工程识图",
        "suffix": "civil_defense",
        "boundary": "只输出人防工程识图候选、证据和复核项；不输出人防结构量、材料量、造价或结算量。",
        "review_type": "civil_defense_layer",
    },
    "precast": {
        "rules": "packs/precast-geometry/rules.json",
        "schema": "cad-precast-geometry/v1",
        "geo_key": "precast_geometry",
        "label": "预制装配深化识图",
        "suffix": "precast",
        "boundary": "只输出预制装配深化识图候选、证据和复核项；不输出预制构件数量、体积、材料量、造价或结算量。",
        "review_type": "precast_layer",
    },
    "bridge_tunnel_road_traffic": {
        "rules": "packs/bridge-tunnel-road-traffic/rules.json",
        "schema": "cad-bridge-tunnel-road-traffic/v1",
        "geo_key": "bridge_tunnel_road_traffic",
        "label": "桥梁/隧道/道路交通识图",
        "suffix": "bridge_tunnel_road_traffic",
        "boundary": "只输出桥梁/隧道/道路交通识图候选、证据和复核项；不输出桥隧长度、道路面积、材料量、造价或结算量。",
        "review_type": "bridge_road_layer",
    },
    "pile_foundation_slope": {
        "rules": "packs/pile-foundation-slope/rules.json",
        "schema": "cad-pile-foundation-slope/v1",
        "geo_key": "pile_foundation_slope_geometry",
        "label": "桩基/基坑/边坡识图",
        "suffix": "pile_foundation_slope",
        "boundary": "只输出桩基/基坑/边坡识图候选、证据和复核项；不输出桩长、方量、支护结构量、造价或结算量。",
        "review_type": "pile_slope_layer",
    },
    "doors_windows_stairs_insulation_waterproof": {
        "rules": "packs/doors-windows-stairs-insulation-waterproof/rules.json",
        "schema": "cad-doors-windows-stairs-insulation-waterproof/v1",
        "geo_key": "doors_windows_stairs_insulation_waterproof",
        "label": "门窗/楼梯/保温/防水识图",
        "suffix": "doors_windows_stairs_insulation_waterproof",
        "boundary": "只输出门窗/楼梯/保温/防水识图候选、证据和复核项；不输出门窗数量、面积、保温/防水展开量、材料量、造价或结算量。",
        "review_type": "dws_insul_water_layer",
    },
    "fire_prevention_accessibility_green_energy": {
        "rules": "packs/fire-prevention-accessibility-green-energy/rules.json",
        "schema": "cad-fire-prevention-accessibility-green-energy/v1",
        "geo_key": "fire_prevention_accessibility_green_energy_geometry",
        "label": "防火/无障碍/绿建节能识图",
        "suffix": "fire_prevention_accessibility_green_energy",
        "boundary": "只输出防火/无障碍/绿建节能识图候选、证据和复核项；不输出防火分区面积、疏散距离结论、绿建评分、能耗量、材料量、造价或结算量。",
        "review_type": "fire_green_layer",
    },
}

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


def iter_geometry(data):
    segment_files = data.get("geometry_segments") or []
    layer_files = data.get("geometry_layers") or []
    for fi, segments in enumerate(segment_files):
        layers = layer_files[fi] if fi < len(layer_files) else []
        for si, seg in enumerate(segments or []):
            if not isinstance(seg, (list, tuple)) or len(seg) < 4:
                continue
            yield fi, si, compact(layers[si]) if si < len(layers) else "", seg


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
    unit_patterns = rules.get("unit_patterns") or {}
    grouped = {}
    for rec in records:
        ctx = context_of(rec)
        item = grouped.setdefault(ctx, {"file": ctx[0], "sheet": ctx[1], "space": ctx[2], "scales": [], "units": [], "evidence": []})
        for m in scale_re.finditer(rec["text"]):
            sc = re.sub(r"\s+", "", m.group(0)).replace("：", ":")
            if sc not in item["scales"]:
                item["scales"].append(sc)
        for unit, pats in unit_patterns.items():
            for pat in pats or []:
                if re.search(str(pat), rec["text"], re.I) and unit not in item["units"]:
                    item["units"].append(unit)
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
    combos = list((rules.get("reference_patterns") or {}).items())
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
                out.append({"type": "reference", "reference_type": ref_type, "value": value, "layer": rec.get("layer"), "file": rec.get("file_name"), "sheet": rec.get("sheet"), "x": rec.get("x"), "y": rec.get("y"), "confidence": float((rules.get("confidence") or {}).get("pattern_match", 0.78)), "status": "candidate", "evidence": [evidence_of(rec)]})
    return out


def geo_candidates(data, rules, cfg):
    out, unmatched = [], Counter()
    for fi, _si, layer, seg in iter_geometry(data):
        fname = data_file_name(data, fi)
        x1, y1, x2, y2 = (round(float(v), 3) for v in seg[:4])
        category, rule, pat = match_rule(f"{layer}", rules.get("layer_rules") or [], "category")
        if category:
            sheet = sheet_for_point(data, (x1 + x2) / 2, (y1 + y2) / 2)
            out.append({"type": cfg["geo_key"], "category": category, "system": (rule or {}).get("system") or "", "pattern": pat, "layer": layer, "file": fname, "sheet": sheet, "geometry": [x1, y1, x2, y2], "confidence": float((rules.get("confidence") or {}).get("geometry_pattern", 0.86)), "status": "candidate", "evidence": [{"layer": layer, "kind": "geometry", "coord": [x1, y1, x2, y2], "file": fname, "sheet": sheet}]})
        else:
            unmatched[layer or "<空图层>"] += 1
    return out, unmatched


def analyze_file(path, rules, cfg):
    data = json.loads(path.read_text(encoding="utf-8"))
    records = read_records(data)
    views = drawing_type_candidates(records, rules)
    audit = scale_unit_audit(records, rules)
    systems = system_candidates(records, data, rules)
    components = component_candidates(records, rules)
    references = reference_candidates(records, rules)
    geometry, unmatched_layers = geo_candidates(data, rules, cfg)
    review = []
    if not views:
        review.append({"type": "drawing_type", "reason": f"未识别到{cfg['label']}图纸类型文字", "evidence": []})
    for row in audit:
        if row.get("status") != "candidate":
            review.append({"type": "scale_unit", "reason": row.get("review_reason") or "比例或单位需确认", "evidence": row.get("evidence", [])})
    if not data.get("geometry_segments") or not data.get("geometry_layers"):
        review.append({"type": "input_geometry", "reason": "输入缺少 geometry_segments 或 geometry_layers；请用 cad_scan --with-geom --with-geom-layer", "evidence": []})
    for layer, count in unmatched_layers.most_common(50):
        review.append({"type": cfg["review_type"], "reason": f"{cfg['label']}图层未分类：{layer}（{count} 段）", "evidence": [{"layer": layer}]})
    summary = {"drawing_types": len(views), "systems": len(systems), "components": len(components), "references": len(references), "geometry": len(geometry), "review_items": len(review)}
    payload = {
        "schema": cfg["schema"], "source_file": path.name, "summary": summary,
        "drawing_types": views, "scale_unit_audit": audit, "systems": systems,
        "components": components, "references": references, cfg["geo_key"]: geometry, "review": review,
        "boundary": cfg["boundary"],
    }
    return payload


def write_markdown(payload, path, cfg):
    s = payload["summary"]
    lines = [f"# {cfg['label']} / 中间数据复核", "", f"- 源文件：`{payload['source_file']}`",
             f"- 候选：图纸类型 {s['drawing_types']}，系统 {s['systems']}，构件 {s['components']}，标注 {s['references']}，几何段 {s['geometry']}，待复核 {s['review_items']}",
             "", "## 构件候选", ""]
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


def write_csv(payload, path, cfg):
    key = cfg["geo_key"]
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
        for row in payload[key]:
            geom = row["geometry"]
            writer.writerow([key, row["category"], row.get("system", ""), row["category"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), f"{geom[0]},{geom[1]}->{geom[2]},{geom[3]}", row["status"], row.get("review_reason", "")])
        for row in payload["review"]:
            writer.writerow(["review", "", "", row["type"], "", "", "", "", "review", row["reason"]])


def build_parser():
    parser = argparse.ArgumentParser(description="从 cad_scan 详情 JSON 提取专业深化识图中间数据。")
    parser.add_argument("inputs", nargs="+")
    parser.add_argument("--pack", required=True, choices=sorted(PACKS.keys()))
    parser.add_argument("--out-dir", default="深化识图")
    return parser


def main():
    import pyboot
    pyboot.ensure_utf8_io()
    args = build_parser().parse_args()
    cfg = PACKS[args.pack]
    rules_path = ROOT / cfg["rules"]
    rules = load_rules(rules_path)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    last = None
    for value in args.inputs:
        src = Path(value)
        if not src.exists():
            raise FileNotFoundError(src)
        payload = analyze_file(src, rules, cfg)
        payload = contractize_payload(payload, source=src.name)
        jp = out_dir / f"{src.stem}.{cfg['suffix']}.json"
        mp = out_dir / f"{src.stem}.{cfg['suffix']}.md"
        cp = out_dir / f"{src.stem}.{cfg['suffix']}.csv"
        jp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        write_markdown(payload, mp, cfg)
        write_csv(payload, cp, cfg)
        last = payload
    if last is None:
        raise SystemExit("没有可处理的输入")
    print(json.dumps({"source": [str(x) for x in args.inputs], "pack": args.pack, "summary": last["summary"], "outputs": [str(x) for x in (jp, mp, cp)]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
