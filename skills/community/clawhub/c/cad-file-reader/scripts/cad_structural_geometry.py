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
from cad_common import compact, load_rules, match_rule, start_mem_guard
from cad_axis_net import axis_nets

# 轴网候选的保留/可用门槛：0.5 是「间距有重复形态」的下限，
# 低于它基本是把墙线/标注当轴线抓出来的。
AXIS_NET_KEEP = 0.30
AXIS_NET_USABLE = 0.50


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
    # 兜底正则（规则文件未给 rebar_pattern 时使用），与 packs/structural-geometry/rules.json 保持一致。
    # 注意：绝不能出现 `\d+\s*[xX×]\s*\d+` 这类“纯数字×数字”分支——那会把梁截面、图幅、
    # 加长尺寸全部误判成配筋（实测 448/448 全误判）。配筋必须有钢筋语义（等级符号/@间距/根数×直径）。
    _FALLBACK = (
        r"(?<![A-Za-z0-9])("
        r"%%13[0-2]\d{1,2}(?:\s*@\s*\d{2,4}(?:/\d{2,4})?(?:\(\d+\))?)?(?:\s*[xX×]\s*\d+(?:\s*[xX×]\s*\d+)*)?"
        r"|\d+\s*(?:%%13[0-2]|[Φφ])\s*\d{1,2}"
        r"|[Φφ]\s*\d{1,2}(?:\s*@\s*\d{2,4}(?:/\d{2,4})?(?:\(\d+\))?)?"
        r"|(?:HPB300|HRB300|HRB335|HRB400|HRB500|CRB550|RRB400|[ABC]\d{1,2})(?:\s+\d{1,2})?\s*@\s*\d{2,4}(?:/\d{2,4})?(?:\(\d+\))?"
        r")"
    )
    regex = re.compile(rules.get("rebar_pattern") or _FALLBACK, re.I)
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


# 轴网图层名。实测这批图纸里轴网在 结_轴线 / 结_轴线尺寸 / AXIS / AXIS_TEXT /
# AXIS_NUM / SOCK-DOTE 上；而 TEL_TEXT / TEXT_喷淋 / DIM-照明 / 图框 上的短词
# 是电话、喷淋、图签内容，形态上一样像轴号，只能靠图层区分。
AXIS_LAYER = re.compile(r"轴|AXIS|SOCK-DOTE|GRID|定位", re.I)
# 严格轴号形态，与 drawing_relation.AXIS_SHAPE 保持同一口径（两处都要改）
AXIS_SHAPE = re.compile(r"^(?:\d{1,3}|[A-Z]{1,2}|\d{1,3}[/-][A-Z0-9]{1,3}|[A-Z][/-]\d{1,3})$")


def grid_candidates(records, rules):
    out, seen = [], set()
    regex = re.compile(rules.get("grid_pattern") or r"(?<![A-Za-z0-9])([A-Z]{1,3}\d{0,3}|[一二三四五六七八九十]+)|\s*(?:轴|标高)\s*[-+]?\d+(?:\.\d+)?", re.I)
    for rec in records:
        # 图层是硬前提。实测 8 万个 grid 候选里只有 0.6% 落在轴网图层上，
        # 其余来自 TEL_TEXT / TEXT_喷淋 / DIM-照明 / 图框——那是电话、喷淋、照明
        # 图签里的短词（PVC/SBS/C20/Co/Ltd），不是轴号。不加这一层过滤，
        # 任何「轴网重叠度」都只是噪声平均，看着有数其实是假的。
        on_axis = bool(AXIS_LAYER.search(rec.get("layer") or ""))
        for m in regex.finditer(rec["text"]):
            value = compact(m.group(0))
            if not value:
                continue
            # 非轴网图层只留形态严格像轴号的值（1~3 位数字 / 1~2 位大写字母 / 组合），
            # 并且标 axis_layer=False 让下游知道「这条证据弱」。
            if not on_axis and not AXIS_SHAPE.match(value):
                continue
            key = (context_of(rec), value, rec.get("layer"), rec.get("x"), rec.get("y"))
            if key in seen:
                continue
            seen.add(key)
            out.append({"type": "grid", "value": value, "layer": rec.get("layer"), "file": rec.get("file_name"), "sheet": rec.get("sheet"), "x": rec.get("x"), "y": rec.get("y"),
                        "axis_layer": on_axis,
                        "confidence": float((rules.get("confidence") or {}).get(
                            "direct_label" if on_axis else "pattern_match", 0.95 if on_axis else 0.78)),
                        "status": "candidate", "evidence": [evidence_of(rec)]})
    return out


def structural_geometry(data, rules):
    out, unmatched = [], Counter()
    for fi, _si, layer, seg in iter_geometry(data):
        fname = data_file_name(data, fi)
        x1, y1, x2, y2 = (round(float(v), 3) for v in seg[:4])
        category, rule, pattern = match_rule(f"{layer}", rules.get("layer_rules") or [], "category")
        if category:
            sheet = sheet_for_point(data, (x1 + x2) / 2, (y1 + y2) / 2)
            out.append({"type": "structural_geometry", "category": category,
                        "system": (rule or {}).get("system") or "", "pattern": pattern,
                        "layer": layer, "file": fname, "sheet": sheet,
                        "geometry": [x1, y1, x2, y2], "handle": None,
                        "source": "semantic_layer",
                        "confidence": float((rules.get("confidence") or {}).get("geometry_pattern", 0.86)),
                        "status": "candidate",
                        "evidence": [{"layer": layer, "kind": "geometry",
                                      "coord": [x1, y1, x2, y2], "file": fname,
                                      "sheet": sheet}]})
        else:
            unmatched[layer or "<空图层>"] += 1
    return out, unmatched


def _raw_geometry_source(source_block):
    """把 cad_scan 的块路径映射成下游稳定的来源字段。"""
    value = compact(source_block or "")
    if not value or value.upper() == "MODELSPACE":
        return "modelspace"
    return f"block:{value}"


def _round_nested(value, ndigits=6):
    if isinstance(value, list):
        return [_round_nested(v, ndigits) for v in value]
    if isinstance(value, dict):
        return {k: _round_nested(v, ndigits) for k, v in value.items()}
    if isinstance(value, float) and value == value and value not in (float("inf"), float("-inf")):
        return round(value, ndigits)
    return value


def block_geometry_payload(data):
    """把 cad_scan --with-block-expand 的结果整理成结构几何行、块记录与单位。

    cad_scan 已经读图并完成块变换，本函数只整理，不再读 DWG/DXF。
    原始坐标保留 6 位；缺句柄/基点时只写复核项，不伪造句柄或插入点。
    """
    rows, blocks, reviews, files = [], [], [], []
    missing_handles = 0
    missing_base_points = 0
    entries = data.get("block_geometry") or []
    for ei, entry in enumerate(entries):
        if not isinstance(entry, dict):
            continue
        source_path = compact(entry.get("source_path"))
        fname = Path(source_path).name if source_path else None
        if not fname:
            reviews.append({"type": "block_geometry_source", "reason": "块几何条目缺 source_path，无法把几何归回源图", "evidence": {"entry_index": ei}})
        units = entry.get("units") if isinstance(entry.get("units"), dict) else {}
        files.append({"file": fname, "units": units})
        for note in entry.get("notes") or []:
            reviews.append({"type": "block_geometry_note", "reason": compact(note), "evidence": {"file": fname}})
        for raw_review in entry.get("review") or []:
            if isinstance(raw_review, dict):
                item = dict(raw_review)
                item.setdefault("evidence", {})
                if isinstance(item["evidence"], dict):
                    item["evidence"] = dict(item["evidence"], file=fname)
                reviews.append(item)
        for raw_block in entry.get("blocks") or []:
            if not isinstance(raw_block, dict):
                continue
            block = _round_nested(dict(raw_block), 6)
            block["file"] = fname
            if block.get("handle") in (None, ""):
                missing_handles += 1
                block["status"] = "review"
                block["review_reason"] = "块记录缺句柄"
            if block.get("source") == "dxf_block_definition" and block.get("base_point") is None:
                missing_base_points += 1
                block["status"] = "review"
                block["review_reason"] = "块定义缺基点"
            blocks.append(block)
        for raw_seg in entry.get("segments") or []:
            if not isinstance(raw_seg, dict):
                continue
            geom = raw_seg.get("geometry")
            if not isinstance(geom, (list, tuple)) or len(geom) < 4:
                reviews.append({"type": "raw_geometry", "reason": "块展开线段缺 geometry，已跳过", "evidence": {"file": fname, "handle": raw_seg.get("handle")}})
                continue
            try:
                x1, y1, x2, y2 = (float(geom[0]), float(geom[1]), float(geom[2]), float(geom[3]))
            except (TypeError, ValueError):
                reviews.append({"type": "raw_geometry", "reason": "块展开线段坐标非数值，已跳过", "evidence": {"file": fname, "handle": raw_seg.get("handle")}})
                continue
            layer = compact(raw_seg.get("layer", ""))
            handle = raw_seg.get("handle")
            if handle in (None, ""):
                missing_handles += 1
            sheet = sheet_for_point(data, (x1 + x2) / 2, (y1 + y2) / 2)
            rows.append({
                "type": "structural_geometry", "category": "raw_geometry",
                "system": "", "pattern": "block_expand",
                "layer": layer, "file": fname, "sheet": sheet,
                "geometry": [x1, y1, x2, y2],
                "handle": handle, "source": _raw_geometry_source(raw_seg.get("source_block")),
                "source_block": compact(raw_seg.get("source_block") or "MODELSPACE"),
                "entity_kind": compact(raw_seg.get("kind", "")),
                "confidence": float(0.86),
                "status": "candidate" if handle not in (None, "") else "review",
                "review_reason": "" if handle not in (None, "") else "缺实体句柄",
                "evidence": [{"layer": layer, "kind": "geometry",
                              "coord": [x1, y1, x2, y2], "file": fname,
                              "sheet": sheet, "handle": handle,
                              "source_block": raw_seg.get("source_block")}],
            })
    if missing_handles:
        reviews.append({"type": "handle_missing", "reason": f"{missing_handles} 条块几何/块记录缺句柄；坐标可用，但无法回溯到原实体，需人工复核", "evidence": {"count": missing_handles}})
    if missing_base_points:
        reviews.append({"type": "base_point_missing", "reason": f"{missing_base_points} 条块定义缺基点；插入变换仍按旧解析器口径保留，块定位需人工复核", "evidence": {"count": missing_base_points}})
    drawing_units = sorted({str(x.get("units", {}).get("drawing_unit")) for x in files if x.get("units", {}).get("drawing_unit")})
    mm_values = sorted({float(x.get("units", {}).get("drawing_mm_per_unit")) for x in files if isinstance(x.get("units", {}).get("drawing_mm_per_unit"), (int, float))})
    if len(drawing_units) > 1 or len(mm_values) > 1:
        reviews.append({"type": "units_mixed", "reason": "多个源图的图纸单位不一致；块几何坐标只在各自图内比较，不能直接合并", "evidence": {"drawing_units": drawing_units, "drawing_mm_per_unit": mm_values}})
    units = {
        "drawing_unit": drawing_units[0] if len(drawing_units) == 1 else None,
        "drawing_mm_per_unit": mm_values[0] if len(mm_values) == 1 else None,
        "mixed": len(drawing_units) > 1 or len(mm_values) > 1,
        "files": files,
    }
    return rows, blocks, units, reviews


def block_geometry_review(data):
    """没有块展开结果时给明确复核项，不把“没开参数”误写成“图中无块”。"""
    if data.get("block_geometry"):
        return []
    return [{"type": "block_geometry_unavailable", "reason": "详情 JSON 无 block_geometry；如需块内/LINE/LWPOLYLINE 原始几何，请重跑 cad_scan 并加 --with-block-expand --detail-json", "evidence": []}]


def axis_net_candidates(data):
    """按文件抽取几何轴网。

    轴号文字在天正转出的图里基本抓不到（实测轴网图层 0 条文字），
    跨专业对照只能靠轴线本身的几何位置。这里按文件分别算，不跨文件混。
    """
    out = []
    segment_files = data.get("geometry_segments") or []
    layer_files = data.get("geometry_layers") or []
    for fi, segments in enumerate(segment_files):
        layers = layer_files[fi] if fi < len(layer_files) else []
        nets = axis_nets(segments or [], layers or [])
        fname = data_file_name(data, fi)
        for net in nets:
            if net["score"] < AXIS_NET_KEEP:
                continue
            net["file"] = fname
            out.append(net)
    # 每方向最多留 12 个，够下游比对，又不让产物膨胀
    kept, seen = [], Counter()
    for net in sorted(out, key=lambda n: -n["score"]):
        if seen[net["direction"]] >= 12:
            continue
        seen[net["direction"]] += 1
        kept.append(net)
    return kept


def tightening_geometry(payload, ndigits: int = 1) -> dict:
    """落地前瘦身：语义行 0.1mm，原始块几何至少保留 6 位。

    语义行来自图层名推断，1 位小数足够；raw_geometry 是块变换后的坐标证据，
    过度取整会让新旧解析器逐点比对失真，因此固定保留 6 位。
    """
    def rnd(v, digits):
        if isinstance(v, float) and v == v and v not in (float('inf'), float('-inf')):
            return round(v, digits)
        return v
    for row in (payload.get('structural_geometry') or []):
        digits = 6 if row.get('category') == 'raw_geometry' or row.get('source') != 'semantic_layer' else ndigits
        cleaned = []
        seen = set()
        for ev in (row.get('evidence') or []):
            coord = ev.get('coord')
            new_coord = [rnd(c, digits) for c in coord] if isinstance(coord, list) else coord
            key = (tuple(new_coord) if isinstance(new_coord, list) else new_coord,
                   ev.get('layer'), ev.get('kind'), ev.get('file'),
                   ev.get('file_name'), ev.get('sheet'), ev.get('handle'))
            if key in seen:
                continue
            seen.add(key)
            e2 = dict(ev)
            if isinstance(coord, list):
                e2['coord'] = new_coord
            cleaned.append(e2)
        if cleaned:
            row['evidence'] = cleaned
        g = row.get('geometry')
        if isinstance(g, list):
            row['geometry'] = [rnd(c, digits) for c in g]
    return payload


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
    semantic_geometry_count = len(geometry)
    raw_geometry, blocks, units, block_reviews = block_geometry_payload(data)
    geometry.extend(raw_geometry)
    nets = axis_net_candidates(data)
    usable_nets = [n for n in nets if n["score"] >= AXIS_NET_USABLE and n["gap_kinds"] >= 2]
    review = []
    if not views:
        review.append({"type": "drawing_type", "reason": "未识别到结构图纸类型文字", "evidence": []})
    for row in audit:
        if row.get("status") != "candidate":
            review.append({"type": "scale_unit", "reason": row.get("review_reason") or "比例或单位需确认", "evidence": row.get("evidence", [])})
    if not data.get("geometry_segments") or not data.get("geometry_layers"):
        review.append({"type": "input_geometry", "reason": "输入缺少 geometry_segments 或 geometry_layers；请用 cad_scan --with-geom --with-geom-layer", "evidence": []})
    elif data.get("geometry_segments") and not usable_nets:
        # 有几何但提不出轴网：说清楚，别让下游以为「这图没有轴网」
        review.append({"type": "axis_net", "reason": "几何段里未提取到可用轴网（轴线可能被画成多段短线，或不落在轴网图层），跨专业轴网核对将退回文字口径", "evidence": [{"geometry_segments": sum(len(s or []) for s in (data.get("geometry_segments") or []))}]})
    for layer, count in unmatched_layers.most_common(50):
        review.append({"type": "structural_layer", "reason": f"结构图层未分类：{layer}（{count} 段）", "evidence": [{"layer": layer}]})
    if semantic_geometry_count:
        review.append({"type": "handle_missing", "reason": f"{semantic_geometry_count} 条语义图层几何来自 geometry_segments，不含实体句柄；如需句柄级回溯请用 --with-block-expand", "evidence": {"count": semantic_geometry_count}})
    review.extend(block_geometry_review(data))
    review.extend(block_reviews)
    summary = {"drawing_types": len(views), "systems": len(systems), "members": len(members), "rebars": len(rebars), "nodes": len(nodes), "grids": len(grids), "axis_nets": len(nets), "axis_nets_usable": len(usable_nets), "structural_geometry": len(geometry), "semantic_geometry": semantic_geometry_count, "raw_geometry": len(raw_geometry), "blocks": len(blocks), "review_items": len(review)}
    return {"schema": "cad-structural-geometry/v1", "source_file": path.name,
            # 透传 cad_scan 记下的源图路径：下游按目录聚类、跨专业配对要用，
            # 只留产物名会让不同专业的图纸落进同一个簇。
            "source_paths": data.get("source_paths") or [],
            "summary": summary, "drawing_types": views, "scale_unit_audit": audit, "systems": systems, "members": members, "rebars": rebars, "nodes": nodes, "grids": grids, "axis_nets": nets, "structural_geometry": geometry, "blocks": blocks, "units": units, "review": review, "boundary": "只输出结构识图候选、证据和复核项；不输出混凝土体积、钢筋吨位、长度汇总、材料量、造价或结算量。"}


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
    guard = start_mem_guard(name="cad_structural_geometry内存闸")
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
        payload = tightening_geometry(payload)
        jp, mp, cp = out_dir / f"{src.stem}.structural.json", out_dir / f"{src.stem}.structural.md", out_dir / f"{src.stem}.structural.csv"
        jp.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        write_markdown(payload, mp)
        write_csv(payload, cp)
        outputs.append(f"已写出 {jp}")
    print(json.dumps({"source": [str(x) for x in args.inputs], "mem_guard": guard, "summary": payload["summary"], "outputs": [str(x) for x in (jp, mp, cp)]}, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
