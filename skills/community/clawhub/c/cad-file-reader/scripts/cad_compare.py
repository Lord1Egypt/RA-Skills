#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""图纸对比候选（P5）：识别图层、块、文字和几何变化，不解释工程量变化。

所有输出均为 `drawing_changes` 识图候选，固定 final_quantity=false。
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

SCHEMA = "cad-file-reader-compare/v1"

from cad_common import compact, file_name
def rounded(value: Any, tolerance: float) -> Any:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(x):
        return None
    step = max(1e-12, float(tolerance))
    return round(x / step) * step

def norm_text_row(data: dict[str, Any], row: dict[str, Any], tolerance: float) -> dict[str, Any]:
    return {
        "text": compact(row.get("text", "")),
        "layer": compact(row.get("layer", "")),
        "kind": compact(row.get("kind", "")),
        "sheet": row.get("sheet"),
        "file": file_name(data, row.get("file")) if row.get("file") is not None else compact(row.get("file_name")),
        "x": row.get("x"),
        "y": row.get("y"),
        "rx": rounded(row.get("x"), tolerance),
        "ry": rounded(row.get("y"), tolerance),
    }

def norm_geometry_row(data: dict[str, Any], seg: Any, layer: Any, tolerance: float) -> dict[str, Any] | None:
    if not isinstance(seg, (list, tuple)) or len(seg) < 4:
        return None
    try:
        vals = [float(v) for v in seg[:4]]
    except (TypeError, ValueError):
        return None
    if not all(math.isfinite(v) for v in vals):
        return None
    if (vals[0], vals[1]) > (vals[2], vals[3]):
        vals = [vals[2], vals[3], vals[0], vals[1]]
    rx = [rounded(v, tolerance) for v in vals]
    if any(v is None for v in rx):
        return None
    length = math.hypot(vals[2] - vals[0], vals[3] - vals[1])
    angle = math.degrees(math.atan2(vals[3] - vals[1], vals[2] - vals[0])) % 180.0
    return {
        "geometry": [round(v, 6) for v in vals],
        "layer": compact(layer),
        "length": round(length, 6),
        "angle": round(angle, 6),
        "key": (compact(layer), *rx),
        "class_key": (compact(layer), rounded(length, tolerance), rounded(angle, 0.01)),
        "center": ((vals[0] + vals[2]) / 2, (vals[1] + vals[3]) / 2),
    }

def change_row(change_type: str, object_type: str, text: str, base: Any = None, target: Any = None, **extra: Any) -> dict[str, Any]:
    evidence: list[dict[str, Any]] = []
    if base is not None:
        evidence.append({"side": "base", **base})
    if target is not None:
        evidence.append({"side": "target", **target})
    row: dict[str, Any] = {
        "id": f"{change_type}:{object_type}:{compact(text)}:{len(evidence)}:{len(extra)}",
        "text": compact(text),
        "change_type": change_type,
        "object_type": object_type,
        "layer": (base or {}).get("layer") or (target or {}).get("layer") or None,
        "block_name": (base or {}).get("block_name") or (target or {}).get("block_name") or None,
        "confidence": 0.95,
        "status": "candidate",
        "review_reasons": [],
        "evidence": evidence,
        "method": "detail_json_diff",
    }
    row.update(extra)
    return row

def compare_layers(base: dict[str, Any], target: dict[str, Any], out: list[dict[str, Any]]) -> None:
    b = {str(x) for x in base.get("layers") or []}
    t = {str(x) for x in target.get("layers") or []}
    for name in sorted(b - t):
        out.append(change_row("removed_layer", "layer", name, {"layer": name}))
    for name in sorted(t - b):
        out.append(change_row("added_layer", "layer", name, None, {"layer": name}))

def compare_blocks(base: dict[str, Any], target: dict[str, Any], out: list[dict[str, Any]]) -> None:
    def refs(data: dict[str, Any]) -> dict[str, int]:
        raw = (data.get("meta") or {}).get("block_refs") or {}
        if isinstance(raw, dict):
            return {str(k): int(v) for k, v in raw.items() if k is not None}
        if isinstance(raw, list):
            return dict(Counter(str(x) for x in raw if x is not None))
        return {}
    b, t = refs(base), refs(target)
    for name in sorted((set(b) | set(t))):
        bc, tc = b.get(name, 0), t.get(name, 0)
        if bc and not tc:
            out.append(change_row("removed_block", "block", name, {"block_name": name, "count": bc}))
        elif tc and not bc:
            out.append(change_row("added_block", "block", name, None, {"block_name": name, "count": tc}))
        elif bc != tc:
            out.append(change_row("block_count_changed", "block", name, {"block_name": name, "count": bc}, {"block_name": name, "count": tc}, base_count=bc, target_count=tc, delta=tc - bc))

def pair_unmatched(base_rows: list[dict[str, Any]], target_rows: list[dict[str, Any]], group_key: Any, distance_key: Any, tolerance: float) -> tuple[set[int], set[int], list[tuple[int, int, float]]]:
    base_groups: dict[Any, list[int]] = defaultdict(list)
    target_groups: dict[Any, list[int]] = defaultdict(list)
    for i, row in enumerate(base_rows):
        base_groups[group_key(row)].append(i)
    for i, row in enumerate(target_rows):
        target_groups[group_key(row)].append(i)
    matches: list[tuple[int, int, float]] = []
    used_b: set[int] = set()
    used_t: set[int] = set()
    for key in sorted(base_groups.keys() & target_groups.keys(), key=lambda x: str(x)):
        candidates = [(distance_key(base_rows[i], target_rows[j]), i, j) for i in base_groups[key] if i not in used_b for j in target_groups[key] if j not in used_t]
        for distance, i, j in sorted(candidates, key=lambda x: (x[0], x[1], x[2])):
            if i in used_b or j in used_t or distance > tolerance:
                continue
            used_b.add(i); used_t.add(j)
            matches.append((i, j, distance))
    return used_b, used_t, matches

def compare_texts(base: dict[str, Any], target: dict[str, Any], tolerance: float, max_changes: int, out: list[dict[str, Any]]) -> dict[str, int]:
    b = [norm_text_row(base, x, tolerance) for x in base.get("text_records") or [] if isinstance(x, dict) and compact(x.get("text"))]
    t = [norm_text_row(target, x, tolerance) for x in target.get("text_records") or [] if isinstance(x, dict) and compact(x.get("text"))]
    def exact_key(x):
        return (x["text"], x["layer"], x["kind"], x["rx"], x["ry"])
    b_by_exact: dict[tuple[Any, ...], int] = Counter(exact_key(x) for x in b)
    t_by_exact: dict[tuple[Any, ...], int] = Counter(exact_key(x) for x in t)
    b_matched = b_by_exact & t_by_exact
    t_matched = b_by_exact & t_by_exact
    base_unmatched: list[dict[str, Any]] = []
    target_unmatched: list[dict[str, Any]] = []
    for row in b:
        key = exact_key(row)
        if b_matched[key] > 0:
            b_matched[key] -= 1
        else:
            base_unmatched.append(row)
    for row in t:
        key = exact_key(row)
        if t_matched[key] > 0:
            t_matched[key] -= 1
        else:
            target_unmatched.append(row)
    def distance(a: dict[str, Any], c: dict[str, Any]) -> float:
        try:
            return math.hypot(float(a["x"]) - float(c["x"]), float(a["y"]) - float(c["y"]))
        except (TypeError, ValueError):
            return float("inf")
    groups_b: dict[tuple[str, str], list[int]] = defaultdict(list)
    groups_t: dict[tuple[str, str], list[int]] = defaultdict(list)
    for i, row in enumerate(base_unmatched):
        groups_b[(row["text"], row["kind"])].append(i)
    for j, row in enumerate(target_unmatched):
        groups_t[(row["text"], row["kind"])].append(j)
    matches: list[tuple[int, int, float]] = []
    used_b: set[int] = set()
    used_t: set[int] = set()
    for key in sorted(set(groups_b) & set(groups_t)):
        candidates = []
        for i in groups_b[key]:
            if i in used_b:
                continue
            for j in groups_t[key]:
                if j in used_t:
                    continue
                candidates.append((distance(base_unmatched[i], target_unmatched[j]), i, j))
        for d, i, j in sorted(candidates, key=lambda x: (x[0], x[1], x[2])):
            if i in used_b or j in used_t:
                continue
            used_b.add(i); used_t.add(j); matches.append((i, j, d))
    counts: Counter[str] = Counter()
    for i, j, d in matches:
        row = change_row("moved_text", "text", base_unmatched[i]["text"], {"layer": base_unmatched[i]["layer"], "coord": [base_unmatched[i]["x"], base_unmatched[i]["y"]], "file": base_unmatched[i]["file"], "sheet": base_unmatched[i]["sheet"]}, {"layer": target_unmatched[j]["layer"], "coord": [target_unmatched[j]["x"], target_unmatched[j]["y"]], "file": target_unmatched[j]["file"], "sheet": target_unmatched[j]["sheet"]}, distance_drawing_units=round(d, 3))
        out.append(row); counts["moved_text"] += 1
    for i in sorted(set(range(len(base_unmatched))) - used_b):
        row = base_unmatched[i]
        out.append(change_row("removed_text", "text", row["text"], {"layer": row["layer"], "coord": [row["x"], row["y"]], "file": row["file"], "sheet": row["sheet"]})); counts["removed_text"] += 1
    for j in sorted(set(range(len(target_unmatched))) - used_t):
        row = target_unmatched[j]
        out.append(change_row("added_text", "text", row["text"], None, {"layer": row["layer"], "coord": [row["x"], row["y"]], "file": row["file"], "sheet": row["sheet"]})); counts["added_text"] += 1
    return counts

def compare_geometry(base: dict[str, Any], target: dict[str, Any], tolerance: float, max_changes: int, out: list[dict[str, Any]]) -> dict[str, int]:
    def rows(data: dict[str, Any]) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        for fi, segments in enumerate(data.get("geometry_segments") or []):
            layer_files = data.get("geometry_layers") or []
            layers = layer_files[fi] if fi < len(layer_files) else []
            for si, seg in enumerate(segments or []):
                layer = layers[si] if si < len(layers) else ""
                row = norm_geometry_row(data, seg, layer, tolerance)
                if row:
                    row["file"] = file_name(data, fi)
                    result.append(row)
        return result
    b, t = rows(base), rows(target)
    b_exact = Counter(x["key"] for x in b)
    t_exact = Counter(x["key"] for x in t)
    b_matched = b_exact & t_exact
    t_matched = b_exact & t_exact
    b_rest: list[dict[str, Any]] = []
    t_rest: list[dict[str, Any]] = []
    for x in b:
        if b_matched[x["key"]] > 0:
            b_matched[x["key"]] -= 1
        else:
            b_rest.append(x)
    for x in t:
        if t_matched[x["key"]] > 0:
            t_matched[x["key"]] -= 1
        else:
            t_rest.append(x)
    def distance(a: dict[str, Any], c: dict[str, Any]) -> float:
        return math.hypot(a["center"][0] - c["center"][0], a["center"][1] - c["center"][1])
    used_b, used_t, matches_list = pair_unmatched(b_rest, t_rest, lambda x: x["class_key"], distance, tolerance * 10)
    counts = Counter()
    pairs = sorted(matches_list, key=lambda x: (x[2], x[0], x[1]))
    for i, j, d in pairs:
        row = change_row("moved_geometry", "geometry", f"geometry:{b_rest[i]['layer']}", {
            "layer": b_rest[i]["layer"], "geometry": b_rest[i]["geometry"], "file": b_rest[i]["file"]
        }, {
            "layer": t_rest[j]["layer"], "geometry": t_rest[j]["geometry"], "file": t_rest[j]["file"]
        }, distance_drawing_units=round(d, 3))
        out.append(row); counts["moved_geometry"] += 1
    for i in sorted(set(range(len(b_rest))) - used_b):
        x = b_rest[i]
        out.append(change_row("removed_geometry", "geometry", f"geometry:{x['layer']}", {"layer": x["layer"], "geometry": x["geometry"], "file": x["file"]})); counts["removed_geometry"] += 1
    for j in sorted(set(range(len(t_rest))) - used_t):
        x = t_rest[j]
        out.append(change_row("added_geometry", "geometry", f"geometry:{x['layer']}", None, {"layer": x["layer"], "geometry": x["geometry"], "file": x["file"]})); counts["added_geometry"] += 1
    return counts

def compare_files(base_path: Path, target_path: Path, tolerance: float, max_changes: int) -> dict[str, Any]:
    base = json.loads(base_path.read_text(encoding="utf-8"))
    target = json.loads(target_path.read_text(encoding="utf-8"))
    changes: list[dict[str, Any]] = []
    compare_layers(base, target, changes)
    compare_blocks(base, target, changes)
    text_counts = compare_texts(base, target, tolerance, max_changes, changes)
    geom_counts = compare_geometry(base, target, tolerance, max_changes, changes)
    truncated = len(changes) > max_changes
    changes = sorted(changes[:max_changes], key=lambda x: (x["change_type"], x["object_type"], x["text"], x["layer"] or ""))
    counts = Counter(x["change_type"] for x in changes)
    summary = {
        "base_source": base_path.name,
        "target_source": target_path.name,
        "tolerance_drawing_units": tolerance,
        "max_changes": max_changes,
        "changes_output": len(changes),
        "truncated": truncated,
        **{f"added_text": text_counts.get("added_text", 0), "removed_text": text_counts.get("removed_text", 0), "moved_text": text_counts.get("moved_text", 0), "added_geometry": geom_counts.get("added_geometry", 0), "removed_geometry": geom_counts.get("removed_geometry", 0), "moved_geometry": geom_counts.get("moved_geometry", 0)},
    }
    payload = {
        "schema": SCHEMA,
        "source_file": f"{base_path.name} -> {target_path.name}",
        "summary": summary,
        "drawing_changes": changes,
        "change_summary": dict(sorted(counts.items())),
        "boundary": "只输出图纸差异候选；不输出工程量增减、材料量、造价或结算量。",
    }
    return contractize_payload(payload, source=f"{base_path.name}->{target_path.name}")

def write_markdown(payload: dict[str, Any], path: Path) -> None:
    s = payload["summary"]
    lines = [
        "# 图纸对比候选", "",
        f"- 基准：`{s['base_source']}`",
        f"- 目标：`{s['target_source']}`",
        f"- 输出变化 {s['changes_output']}；截断：{s['truncated']}",
        f"- 文字：新增 {s['added_text']}，删除 {s['removed_text']}，移动 {s['moved_text']}",
        f"- 几何：新增 {s['added_geometry']}，删除 {s['removed_geometry']}，移动 {s['moved_geometry']}",
        "", "> 本文件只输出差异候选，不输出工程量、材料量或造价。", "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")

def write_csv(payload: dict[str, Any], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.writer(fh)
        writer.writerow(["change_type", "object_type", "text", "layer", "block_name", "status", "evidence"])
        for row in payload["drawing_changes"]:
            writer.writerow([row["change_type"], row["object_type"], row["text"], row.get("layer"), row.get("block_name"), row["status"], json.dumps(row["evidence"], ensure_ascii=False)])

def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    parser = argparse.ArgumentParser(description="对比 cad_scan 详情 JSON 的图层/块/文字/几何变化。")
    parser.add_argument("base", help="基准详情 JSON")
    parser.add_argument("target", help="目标详情 JSON")
    parser.add_argument("--out-dir", default="图纸对比", help="输出目录")
    parser.add_argument("--tolerance", type=float, default=1.0, help="坐标归一/移动判定基础容差，图面单位")
    parser.add_argument("--max-changes", type=int, default=5000, help="最大输出变化数")
    args = parser.parse_args()
    if args.tolerance <= 0 or args.max_changes < 0:
        parser.error("容差必须大于 0，最大变化数必须非负")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = compare_files(Path(args.base), Path(args.target), args.tolerance, args.max_changes)
    stem = f"{Path(args.base).stem}__{Path(args.target).stem}.compare.json"
    json_path = out_dir / stem
    md_path = json_path.with_suffix(".md")
    csv_path = out_dir / f"{Path(args.base).stem}__{Path(args.target).stem}.compare.csv"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(payload, md_path)
    write_csv(payload, csv_path)
    print(json.dumps({"base": args.base, "target": args.target, "summary": payload["summary"], "outputs": [str(json_path), str(md_path), str(csv_path)]}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
