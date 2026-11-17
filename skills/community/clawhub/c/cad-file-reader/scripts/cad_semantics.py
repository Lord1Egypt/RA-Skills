#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""图层与块语义候选（P2/P3）：只整理证据，不计算工程量。

输出：
- semantic_layers：图层语义候选
- semantic_blocks：块名语义候选
- block_instances：块实例的几何/文字/属性关联候选
所有候选固定 final_quantity=false。
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

from cad_contract import contractize_payload

SCHEMA = "cad-file-reader-semantics/v1"

LAYER_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("annotation", ("文字", "标注", "图名", "说明", "TEXT", "NOTE", "TITLE")),
    ("axis", ("轴", "AXIS", "GRID", "AXIS_TEXT")),
    ("dimension", ("尺寸", "DIM", "DIMS")),
    ("architecture", ("建筑", "墙体", "门", "窗", "家具", "房间", "地面", "天花", "吊顶", "保温", "楼梯", "电梯", "A-", "ARCH")),
    ("structure", ("结构", "梁", "板", "柱", "剪力墙", "基础", "钢筋", "承台", "桩", "钢结构", "S-")),
    ("electrical", ("电气", "照明", "插座", "电缆", "电线", "桥架", "配电", "E-", "ELEC", "LIGHT", "POWER", "CABLE", "TRAY")),
    ("water_fire", ("给水", "排水", "消防", "喷淋", "管道", "管路", "W-", "PIPE", "FIRE", "SPRINKLER")),
    ("hvac", ("暖通", "风管", "风口", "风机", "空调", "H-", "HVAC", "DUCT", "AIR")),
    ("telecom", ("弱电", "通信", "网络", "电视", "安防", "T-", "TELEC", "TELECOM", "SECURITY")),
    ("municipal", ("道路", "市政", "雨水", "污水", "检查井", "管廊", "R-", "ROAD", "STORM", "SEWER")),
]
BLOCK_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("door", ("门", "DOOR", "-D", "M-")),
    ("window", ("窗", "WINDOW", "WIN", "-C")),
    ("furniture", ("家具", "桌", "椅", "床", "柜", "沙发", "FURNITURE", "FURN")),
    ("axis", ("轴", "AXIS", "GRID", "AXISO", "TICK")),
    ("equipment", ("设备", "空调", "风机", "水泵", "配电", "灯", "EQUIP", "PUMP", "FAN", "AC-")),
    ("pipe_fitting", ("阀", "管", "喷淋", "消火栓", "VALVE", "PIPE", "HYDRANT")),
    ("annotation", ("标注", "图名", "说明", "标签", "TEXT", "LABEL", "NOTE", "TAG")),
]
ANONYMOUS_BLOCK = re.compile(r"^(\$|\*|\d+|Unknown|unnamed)", re.I)

from cad_common import compact, file_name
def classify_by_rules(value: str, rules: list[tuple[str, tuple[str, ...]]]) -> tuple[str, str, float]:
    upper = value.upper()
    for semantic, tokens in rules:
        for token in tokens:
            if str(token).upper() in upper:
                return semantic, token, 0.95
    return "unknown", "", 0.42

def bbox_of_points(points: list[tuple[float, float]]) -> list[float] | None:
    if not points:
        return None
    xs = [x for x, _y in points]
    ys = [_y for _x, y in points]
    return [min(xs), min(ys), max(xs), max(ys)]

def layer_rows(data: dict[str, Any], max_layers: int) -> tuple[list[dict[str, Any]], dict[str, int], bool]:
    names = [str(x) for x in (data.get("layers") or []) if isinstance(x, str)]
    text_by_layer: Counter[str] = Counter()
    geom_by_layer: Counter[str] = Counter()
    text_samples: dict[str, list[str]] = defaultdict(list)
    for rec in data.get("text_records") or []:
        if not isinstance(rec, dict):
            continue
        layer = compact(rec.get("layer", ""))
        text = compact(rec.get("text", ""))
        if not layer:
            continue
        text_by_layer[layer] += 1
        if text and len(text_samples[layer]) < 8:
            text_samples[layer].append(text)
    for file_layers in data.get("geometry_layers") or []:
        for layer in file_layers or []:
            geom_by_layer[compact(layer)] += 1

    rows: list[dict[str, Any]] = []
    total = len(names)
    for name in sorted(names[:max_layers]):
        semantic, token, confidence = classify_by_rules(name, LAYER_RULES)
        evidence: list[dict[str, Any]] = [
            {"kind": "layer_name", "value": name, "matched_token": token},
            {"kind": "text_count", "value": int(text_by_layer[name])},
            {"kind": "geometry_count", "value": int(geom_by_layer[name])},
        ]
        reasons: list[str] = []
        notes = ""
        if semantic == "unknown":
            content = " ".join(text_samples[name])
            inferred, itoken, iconf = classify_by_rules(content, LAYER_RULES)
            if inferred != "unknown":
                semantic, token, confidence = inferred, itoken, iconf - 0.20
                evidence.append({"kind": "text_content_inference", "matched_token": itoken, "sample": content[:120]})
            if confidence < 0.50:
                reasons = ["low_confidence_inference"]
                notes = "图层名与关联文字未匹配到语义规则，需人工确认"
        if reasons:
            status = "review"
        else:
            status = "candidate"
            notes = ""
        rows.append({
            "id": f"layer:{name}",
            "layer": name,
            "text": name,
            "semantic": semantic,
            "matched_token": token,
            "text_count": int(text_by_layer[name]),
            "geometry_count": int(geom_by_layer[name]),
            "confidence": round(confidence, 4),
            "status": status,
            "review_reasons": reasons,
            "review_reason": notes,
            "evidence": evidence,
            "method": "layer_name_or_text_inference",
        })
    return rows, {"text_count": len(text_by_layer), "geometry_count": len(geom_by_layer)}, total > max_layers

def block_semantic(name: str, block_defs: set[str] | None = None) -> tuple[str, float, list[str], list[dict[str, Any]]]:
    semantic, token, confidence = classify_by_rules(name, BLOCK_RULES)
    evidence: list[dict[str, Any]] = [{"kind": "block_name", "value": name, "matched_token": token}]
    reasons: list[str] = []
    anonymous = bool(ANONYMOUS_BLOCK.match(name))
    if anonymous:
        reasons.append("missing_block_definition")
        confidence = min(confidence, 0.42)
        evidence.append({"kind": "anonymous_name", "value": name})
    if block_defs is not None and name not in block_defs:
        reasons.append("missing_block_definition")
        evidence.append({"kind": "definition_index", "present": False})
    if semantic == "unknown":
        if "low_confidence_inference" not in reasons:
            reasons.append("low_confidence_inference")
        confidence = min(confidence, 0.42)
    return semantic, confidence, reasons, evidence

def build_spatial_index(
    rows: list[dict[str, Any]], cell: float,
) -> dict[tuple[Any, Any, int, int], list[dict[str, Any]]]:
    index: dict[tuple[Any, Any, int, int], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        x, y = row.get("x"), row.get("y")
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            continue
        if not (math.isfinite(float(x)) and math.isfinite(float(y))):
            continue
        key = (row.get("file_name"), row.get("sheet"), int(float(x) // cell), int(float(y) // cell))
        index[key].append(row)
    return index

def nearest_rows(index: dict[tuple[Any, Any, int, int], list[dict[str, Any]]], row: dict[str, Any], cell: float) -> list[dict[str, Any]]:
    x, y = row.get("x"), row.get("y")
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        return []
    if not (math.isfinite(float(x)) and math.isfinite(float(y))):
        return []
    cx, cy = int(float(x) // cell), int(float(y) // cell)
    nearby: list[dict[str, Any]] = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            nearby.extend(index.get((row.get("file_name"), row.get("sheet"), cx + dx, cy + dy), []))
    def distance(item: dict[str, Any]) -> float:
        return math.hypot(float(item.get("x", 0)) - float(x), float(item.get("y", 0)) - float(y))
    return sorted(nearby, key=distance)[:5]

def make_instance_row(
    rec: dict[str, Any], name: str, semantic: str, text_hits: list[dict[str, Any]],
    geom_hits: list[dict[str, Any]], attr_hits: list[dict[str, Any]], link_radius: float,
) -> dict[str, Any]:
    evidence: list[dict[str, Any]] = [{
        "kind": "insert", "block": name, "coord": [rec.get("x"), rec.get("y")],
        "file": rec.get("file_name"), "sheet": rec.get("sheet"), "layer": rec.get("layer"),
    }]
    if text_hits:
        evidence.append({"kind": "linked_text", "value": compact(text_hits[0].get("text")), "distance_drawing_units": round(math.hypot(float(text_hits[0].get("x", 0)) - float(rec.get("x", 0)), float(text_hits[0].get("y", 0)) - float(rec.get("y", 0))), 3)})
    if geom_hits:
        seg = geom_hits[0].get("geometry") or []
        evidence.append({"kind": "linked_geometry", "value": seg[:4], "distance_drawing_units": geom_hits[0].get("distance")})
    if attr_hits:
        evidence.append({"kind": "linked_attribute", "value": compact(attr_hits[0].get("text"))})

    reasons: list[str] = []
    confidence = 0.72
    if semantic == "unknown":
        reasons.append("low_confidence_inference")
    if not text_hits and not geom_hits and not attr_hits:
        reasons.append("ambiguous_text_binding")
        confidence = 0.42
    elif text_hits and geom_hits:
        confidence = 0.95
    elif text_hits or geom_hits or attr_hits:
        confidence = 0.78
    coord = [rec.get("x"), rec.get("y")]
    bbox = [float(coord[0]), float(coord[1]), float(coord[0]), float(coord[1])] if all(isinstance(x, (int, float)) and math.isfinite(float(x)) for x in coord) else None
    return {
        "id": f"block-instance:{rec.get('file_name', '')}:{rec.get('sheet', '')}:{rec.get('_index', '')}",
        "block_name": name,
        "text": compact(text_hits[0].get("text") if text_hits else name),
        "layer": rec.get("layer") or None,
        "block_semantic": semantic,
        "x": rec.get("x"),
        "y": rec.get("y"),
        "bbox": bbox,
        "linked_text_count": len(text_hits),
        "linked_geometry_count": len(geom_hits),
        "linked_attribute_count": len(attr_hits),
        "confidence": confidence,
        "status": "candidate" if not reasons else "review",
        "review_reasons": reasons,
        "review_reason": "；".join({
            "ambiguous_text_binding": "缺邻近文字/几何/属性关联",
            "low_confidence_inference": "块名语义需确认",
        }.get(x, x) for x in reasons),
        "evidence": evidence,
        "method": "insert_spatial_link",
    }

def block_rows(data: dict[str, Any], max_blocks: int, max_instances: int, link_radius: float):
    refs = (data.get("meta") or {}).get("block_refs") or {}
    if isinstance(refs, list):
        ref_counter = Counter(str(x) for x in refs if x)
    elif isinstance(refs, dict):
        ref_counter = Counter({str(k): int(v) for k, v in refs.items()})
    else:
        ref_counter = Counter()
    block_defs = (data.get("meta") or {}).get("block_defs")
    def_set = {str(x) for x in block_defs} if isinstance(block_defs, list) else None

    semantic_rows: list[dict[str, Any]] = []
    for name in sorted(ref_counter, key=lambda x: (-int(ref_counter[x]), x))[:max_blocks]:
        semantic, confidence, reasons, evidence = block_semantic(name, def_set)
        semantic_rows.append({
            "id": f"block:{name}",
            "block_name": name,
            "text": name,
            "semantic": semantic,
            "instance_count": int(ref_counter[name]),
            "confidence": round(confidence, 4),
            "status": "candidate" if not reasons else "review",
            "review_reasons": reasons,
            "review_reason": "；".join({
                "missing_block_definition": "块名匿名或定义索引不足",
                "low_confidence_inference": "块名语义需确认",
            }.get(x, x) for x in reasons),
            "evidence": evidence + [{"kind": "instance_count", "value": int(ref_counter[name])}],
            "method": "block_name_or_definition_index",
        })

    records: list[dict[str, Any]] = []
    for index, raw in enumerate(data.get("text_records") or []):
        if not isinstance(raw, dict):
            continue
        kind = str(raw.get("kind", "")).upper()
        if kind not in {"TEXT", "MTEXT", "INSERT", "ATTRIB"}:
            continue
        file_n = raw.get("file_name") or file_name(data, raw.get("file"))
        records.append({
            "kind": kind, "text": compact(raw.get("text")),
            "block_name": compact(raw.get("block_name") or raw.get("block") or raw.get("text")),
            "layer": raw.get("layer"), "x": raw.get("x"), "y": raw.get("y"),
            "sheet": raw.get("sheet"), "file": raw.get("file"), "file_name": file_n, "_index": index,
        })
    inserts = [x for x in records if x["kind"] == "INSERT" and x["block_name"]]
    texts = [x for x in records if x["kind"] != "INSERT" and x["text"]]
    attrs = [x for x in records if x["kind"] == "ATTRIB" and x["text"]]
    text_index = build_spatial_index(texts, max(1.0, link_radius))
    attr_index = build_spatial_index(attrs, max(1.0, link_radius))

    geom_index: dict[tuple[Any, Any, int, int], list[dict[str, Any]]] = defaultdict(list)
    for fi, segments in enumerate(data.get("geometry_segments") or []):
        layers = (data.get("geometry_layers") or [None] * (fi + 1))[fi] if fi < len(data.get("geometry_layers") or []) else []
        file_n = file_name(data, fi)
        for si, seg in enumerate(segments or []):
            if not isinstance(seg, (list, tuple)) or len(seg) < 4:
                continue
            try:
                x = (float(seg[0]) + float(seg[2])) / 2
                y = (float(seg[1]) + float(seg[3])) / 2
            except (TypeError, ValueError):
                continue
            layer = compact(layers[si]) if isinstance(layers, list) and si < len(layers) else ""
            item = {"geometry": seg, "layer": layer, "file": file_n}
            geom_index[(file_n, None, int(x // max(1.0, link_radius)), int(y // max(1.0, link_radius)))].append(item)

    semantic_map = {row["block_name"]: row["semantic"] for row in semantic_rows}
    instance_rows: list[dict[str, Any]] = []
    ordered = sorted(inserts, key=lambda x: (str(x.get("file_name", "")), str(x.get("sheet", "")), float(x.get("x", 0)) if isinstance(x.get("x"), (int, float)) else 0.0, float(x.get("y", 0)) if isinstance(x.get("y"), (int, float)) else 0.0, x.get("_index", 0)))
    for rec in ordered[:max_instances]:
        name = rec["block_name"]
        semantic = semantic_map.get(name, block_semantic(name)[0])
        text_hits = nearest_rows(text_index, rec, link_radius)
        attr_hits = nearest_rows(attr_index, rec, link_radius)
        cx, cy = int(float(rec.get("x", 0)) // max(1.0, link_radius)), int(float(rec.get("y", 0)) // max(1.0, link_radius))
        geom_hits: list[dict[str, Any]] = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                geom_hits.extend(geom_index.get((rec.get("file_name"), rec.get("sheet"), cx + dx, cy + dy), []))
        for item in geom_hits:
            seg = item.get("geometry") or []
            item["distance"] = round(math.hypot((float(seg[0]) + float(seg[2])) / 2 - float(rec.get("x", 0)), (float(seg[1]) + float(seg[3])) / 2 - float(rec.get("y", 0))), 3)
        geom_hits = sorted(geom_hits, key=lambda x: x["distance"])[:5]
        instance_rows.append(make_instance_row(rec, name, semantic, text_hits, geom_hits, attr_hits, link_radius))
    return semantic_rows, instance_rows, {
        "unique_block_names": len(ref_counter), "insert_records": len(inserts),
        "attribute_records": len(attrs), "instances_output": len(instance_rows),
        "semantic_blocks_truncated": len(semantic_rows) < len(ref_counter),
        "block_instances_truncated": len(instance_rows) < len(inserts),
        "max_blocks": max_blocks, "max_instances": max_instances,
    }

def write_markdown(payload: dict[str, Any], path: Path) -> None:
    s = payload["summary"]
    lines = [
        "# 图层与块语义候选", "",
        f"- 源文件：`{payload['source_file']}`",
        f"- 图层候选 {len(payload['semantic_layers'])}；块语义候选 {len(payload['semantic_blocks'])}；块实例候选 {len(payload['block_instances'])}",
        f"- 需复核 {payload['contract']['summary']['review_required']}；候选 {payload['contract']['summary']['candidate_count']}",
        "", "> 本文件只输出识图候选，不输出工程量、材料量或造价。", "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")

def write_csv(payload: dict[str, Any], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.writer(fh)
        writer.writerow(["section", "id", "semantic", "name", "layer", "count", "status", "review_reasons"])
        for row in payload["semantic_layers"]:
            writer.writerow(["semantic_layers", row.get("id"), row.get("semantic"), row.get("layer"), row.get("layer"), row.get("text_count"), row.get("status"), ";".join(row.get("review_reasons") or [])])
        for row in payload["semantic_blocks"]:
            writer.writerow(["semantic_blocks", row.get("id"), row.get("semantic"), row.get("block_name"), "", row.get("instance_count"), row.get("status"), ";".join(row.get("review_reasons") or [])])
        for row in payload["block_instances"]:
            writer.writerow(["block_instances", row.get("id"), row.get("block_semantic"), row.get("block_name"), row.get("layer"), "", row.get("status"), ";".join(row.get("review_reasons") or [])])

def analyze_file(path: Path, max_layers: int, max_blocks: int, max_instances: int, link_radius: float) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    layers, layer_counts, layers_truncated = layer_rows(data, max_layers)
    semantic_blocks, block_instances, block_counts = block_rows(data, max_blocks, max_instances, link_radius)
    summary = {
        "source_layers": len(data.get("layers") or []),
        "semantic_layers": len(layers),
        "semantic_layers_truncated": layers_truncated,
        "layer_text_names": layer_counts["text_count"],
        "layer_geometry_names": layer_counts["geometry_count"],
        **block_counts,
        "semantic_blocks": len(semantic_blocks),
        "block_instances": len(block_instances),
    }
    payload: dict[str, Any] = {
        "schema": SCHEMA,
        "source_file": path.name,
        "summary": summary,
        "semantic_layers": layers,
        "semantic_blocks": semantic_blocks,
        "block_instances": block_instances,
        "boundary": "只输出图层与块语义候选；不输出工程量、材料量、造价或结算量。",
    }
    return contractize_payload(payload, source=path.name)

def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    parser = argparse.ArgumentParser(description="从 cad_scan 详情 JSON 提取图层与块语义候选。")
    parser.add_argument("inputs", nargs="+", help="cad_scan 生成的 --detail-json 文件")
    parser.add_argument("--out-dir", default="语义识图", help="输出目录")
    parser.add_argument("--max-layers", type=int, default=2000)
    parser.add_argument("--max-blocks", type=int, default=2000)
    parser.add_argument("--max-instances", type=int, default=2000)
    parser.add_argument("--link-radius", type=float, default=3000.0, help="块实例关联半径，图面单位")
    args = parser.parse_args()
    if min(args.max_layers, args.max_blocks, args.max_instances) < 0 or args.link_radius <= 0:
        parser.error("上限必须非负，关联半径必须大于 0")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    outputs = 0
    for value in args.inputs:
        src = Path(value)
        if not src.exists():
            raise FileNotFoundError(src)
        payload = analyze_file(src, args.max_layers, args.max_blocks, args.max_instances, args.link_radius)
        json_path = out_dir / f"{src.stem}.semantics.json"
        md_path = out_dir / f"{src.stem}.semantics.md"
        csv_path = out_dir / f"{src.stem}.semantics.csv"
        json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        write_markdown(payload, md_path)
        write_csv(payload, csv_path)
        print(json.dumps({"source": str(src), "summary": payload["summary"], "outputs": [str(json_path), str(md_path), str(csv_path)]}, ensure_ascii=False))
        outputs += 1
    return 0 if outputs else 4

if __name__ == "__main__":
    raise SystemExit(main())
