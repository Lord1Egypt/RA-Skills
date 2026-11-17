#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""塔吊布置识图：从 DXF/DWG 或 cad_scan 详情 JSON 提取塔吊位置与证据。

输出的是“识图候选”，不是选型、验算或施工方案：
  * INSERT 块插入点 + 块基点 + 旋转/缩放 → 回转中心（仿射变换）；
  * 块名/图层/邻近文字 → 塔吊身份候选；
  * 明确写“臂长/起重臂长”的文字 → jib_length_m；
  * 圆只记 radius_circles_m，**绝不把圆半径当臂长**。

边界：不判断覆盖范围是否满足、不验算基础/附着/群塔防碰撞、不输出数量或造价。
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from cad_contract import contractize_payload, reader_version  # noqa: E402

SCHEMA = "cad-crane-layout/v1"
RULES_PATH = ROOT / "packs" / "crane-layout" / "rules.json"
CST = timezone(timedelta(hours=8))


def load_rules() -> dict[str, Any]:
    return json.loads(RULES_PATH.read_text(encoding="utf-8"))


# ---------------------------------------------------------------- 基础工具
def _num(value: Any) -> float | None:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if math.isfinite(out) else None


def _pt(x: Any, y: Any) -> tuple[float, float] | None:
    px, py = _num(x), _num(y)
    if px is None or py is None:
        return None
    return px, py


def _dist(a: tuple[float, float] | None, b: tuple[float, float] | None) -> float | None:
    if a is None or b is None:
        return None
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _now() -> str:
    return datetime.now(CST).isoformat(timespec="seconds")


def _slug(value: Any) -> str:
    text = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff._-]+", "_", str(value or "").strip())
    return text.strip("_") or "NA"


def _match_first(value: str, patterns: list[str]) -> tuple[str, str] | tuple[None, None]:
    for pattern in patterns:
        match = re.search(pattern, value or "", re.I)
        if match:
            return match.group(0), pattern
    return None, None


def _is_negative(value: str, patterns: list[str]) -> str | None:
    for pattern in patterns:
        if re.search(pattern, value or "", re.I):
            return pattern
    return None


def _normalize_record(raw: dict[str, Any], file_index: int = 0, file_name: str = "") -> dict[str, Any]:
    kind = str(raw.get("kind") or raw.get("type") or "").upper()
    text = str(raw.get("text") or raw.get("raw") or "").strip()
    block_name = raw.get("block_name") or (text if kind == "INSERT" else None)
    bp = raw.get("base_point")
    if isinstance(bp, (list, tuple)) and len(bp) >= 2:
        base_point = [_num(bp[0]), _num(bp[1])]
    else:
        base_point = None
    scales = []
    for key in ("xscale", "yscale", "zscale"):
        value = _num(raw.get(key))
        scales.append(1.0 if value is None else value)
    ext = raw.get("extrusion")
    extrusion = None
    if isinstance(ext, (list, tuple)) and len(ext) >= 3:
        extrusion = [_num(ext[0]) or 0.0, _num(ext[1]) or 0.0, _num(ext[2]) or 1.0]
    return {
        "kind": kind,
        "text": text,
        "block_name": str(block_name).strip() if block_name else None,
        "layer": str(raw.get("layer") or "").strip(),
        "x": _num(raw.get("x")),
        "y": _num(raw.get("y")),
        "z": _num(raw.get("z")),
        "rotation": _num(raw.get("rotation")) or 0.0,
        "xscale": scales[0],
        "yscale": scales[1],
        "zscale": scales[2],
        "base_point": base_point,
        "base_point_source": raw.get("base_point_source"),
        "extrusion": extrusion,
        "file": file_index,
        "file_name": file_name,
        "sheet": raw.get("sheet"),
        "space": raw.get("space"),
        "handle": raw.get("handle"),
    }


def _circle_row(raw: Any, file_index: int = 0) -> list[Any] | None:
    if not isinstance(raw, (list, tuple)) or len(raw) < 3:
        return None
    x, y, r = _num(raw[0]), _num(raw[1]), _num(raw[2])
    if x is None or y is None or r is None:
        return None
    layer = str(raw[3] or "") if len(raw) > 3 else ""
    return [x, y, r, layer, file_index]


# ---------------------------------------------------------------- 三种输入
def _load_dxf(path: Path, max_rows: int, log) -> tuple[list[dict], list[list], dict, list[str]]:
    import cad_scan
    recs, _layers, notes, meta = cad_scan.dxf_records(str(path), max_rows, log, include_insert=True)
    circles, cnotes = cad_scan.dxf_circle_entities(str(path), log=log)
    rows = [_normalize_record(r, 0, path.name) for r in recs if isinstance(r, dict)]
    return rows, [c for c in (_circle_row(x, 0) for x in circles) if c], meta, notes + cnotes


def _load_dwg(path: Path, max_rows: int, log) -> tuple[list[dict], list[list], dict, list[str]]:
    import cad_scan
    recs, _layers, notes, meta = cad_scan.dwg_records(
        str(path), {"text", "mtext", "attrib", "insert"}, 60.0, max_rows, log)
    circles: list[list] = []
    try:
        raw_circles, cnotes = cad_scan.circle_entities(str(path), 60.0, log)
        circles = [c for c in (_circle_row(x, 0) for x in raw_circles) if c]
        notes = notes + cnotes
    except Exception as exc:  # 圆是旁证，解不出不影响塔吊位置
        notes = notes + [f"圆实体提取失败 {type(exc).__name__} {exc}"]
    rows = [_normalize_record(r, 0, path.name) for r in recs if isinstance(r, dict)]
    return rows, circles, meta, notes


def _load_detail(path: Path) -> tuple[list[dict], list[list], dict, list[str], list[str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    files = data.get("files") or []
    names: dict[int, str] = {}
    for i, item in enumerate(files):
        if isinstance(item, dict):
            names[i] = str(item.get("name") or item.get("path") or "")
        else:
            names[i] = str(item or "")
    rows: list[dict] = []
    for raw in data.get("text_records") or []:
        if not isinstance(raw, dict):
            continue
        idx = raw.get("file")
        file_index = int(idx) if isinstance(idx, int) else 0
        rows.append(_normalize_record(raw, file_index, names.get(file_index, "")))
    circles = [c for c in (_circle_row(x, int(x[4]) if len(x) > 4 and isinstance(x[4], int) else 0)
                           for x in data.get("geometry_entities") or []) if c]
    meta = data.get("meta") if isinstance(data.get("meta"), dict) else {}
    notes = [str(x) for x in data.get("notes") or [] if str(x).strip()]
    return rows, circles, meta, notes, [str(p) for p in data.get("source_paths") or []]


def load_input(path: Path, max_rows: int, log) -> tuple[list[dict], list[list], dict, list[str], list[str], str]:
    suffix = path.suffix.lower()
    if suffix == ".dxf":
        rows, circles, meta, notes = _load_dxf(path, max_rows, log)
        return rows, circles, meta, notes, [str(path.resolve())], "dxf"
    if suffix == ".dwg":
        rows, circles, meta, notes = _load_dwg(path, max_rows, log)
        return rows, circles, meta, notes, [str(path.resolve())], "dwg"
    if suffix in (".json", ".crane.json"):
        rows, circles, meta, notes, source_paths = _load_detail(path)
        return rows, circles, meta, notes, source_paths, "detail_json"
    raise SystemExit(f"不支持的输入：{path}（只接受 .dxf/.dwg/cad_scan 详情 .json）")


# ---------------------------------------------------------------- 回转中心
def _center_of(rec: dict[str, Any], unit_factor: float) -> tuple[tuple[float, float] | None, str]:
    insert = _pt(rec.get("x"), rec.get("y"))
    if insert is None:
        return None, "missing_insert_point"
    base = rec.get("base_point")
    if not isinstance(base, (list, tuple)) or len(base) < 2 or base[0] is None or base[1] is None:
        return None, "base_point_unavailable"
    ext = rec.get("extrusion")
    if isinstance(ext, (list, tuple)) and len(ext) >= 3:
        ex, ey, ez = (_num(ext[0]) or 0.0, _num(ext[1]) or 0.0, _num(ext[2]) or 1.0)
        if abs(ex) > 1e-9 or abs(ey) > 1e-9 or abs(ez - 1.0) > 1e-9:
            return None, "unsupported_ocs"
    sx, sy = _num(rec.get("xscale")) or 1.0, _num(rec.get("yscale")) or 1.0
    if abs(sx) < 1e-12 or abs(sy) < 1e-12:
        return None, "zero_scale"
    theta = math.radians(_num(rec.get("rotation")) or 0.0)
    dx = (0.0 - float(base[0])) * sx
    dy = (0.0 - float(base[1])) * sy
    cos_t, sin_t = math.cos(theta), math.sin(theta)
    cx = insert[0] + dx * cos_t - dy * sin_t
    cy = insert[1] + dx * sin_t + dy * cos_t
    return (cx * unit_factor, cy * unit_factor), "insert_affine"


# ---------------------------------------------------------------- 塔吊识别
def detect_towers(rows: list[dict], rules: dict, unit_factor: float, unit_basis: str,
                  extra_block_patterns: list[str] | None = None,
                  extra_layer_patterns: list[str] | None = None) -> tuple[list[dict], list[dict]]:
    conf = rules.get("confidence") or {}
    thresholds = rules.get("thresholds") or {}
    label_radius = float(thresholds.get("label_bind_radius_m", 30.0))
    block_patterns = list(rules.get("block_patterns") or []) + list(extra_block_patterns or [])
    layer_patterns = list(rules.get("layer_patterns") or []) + list(extra_layer_patterns or [])
    towers: list[dict] = []
    rejected: list[dict] = []

    texts = [r for r in rows if r["kind"] != "INSERT" and r["text"] and r["x"] is not None]
    inserts = [r for r in rows if r["kind"] == "INSERT" and r["block_name"]]

    for rec in inserts:
        block = rec["block_name"]
        layer = rec["layer"]
        block_hit, block_pattern = _match_first(block, block_patterns)
        layer_hit, layer_pattern = _match_first(layer, layer_patterns)
        negative = _is_negative(f"{block} {layer}", rules.get("negative_patterns") or [])
        if negative:
            rejected.append({"block_name": block, "layer": layer, "reason": f"negative_pattern:{negative}"})
            continue
        if not block_hit and not layer_hit:
            continue

        insert_pt = _pt(rec.get("x"), rec.get("y"))
        center, transform_status = _center_of(rec, unit_factor)
        anchor = center or (tuple(v * unit_factor for v in insert_pt) if insert_pt else None)

        nearby: list[dict] = []
        label_hits: list[dict] = []
        for text in texts:
            if text["file"] != rec["file"]:
                continue
            if rec.get("sheet") is not None and text.get("sheet") is not None and rec["sheet"] != text["sheet"]:
                continue
            tpt = _pt(text.get("x"), text.get("y"))
            distance = _dist(anchor, (tpt[0] * unit_factor, tpt[1] * unit_factor) if tpt else None)
            if distance is None or distance > label_radius:
                continue
            item = {
                "text": text["text"],
                "layer": text["layer"],
                "x": text.get("x"),
                "y": text.get("y"),
                "distance_m": round(distance, 3),
            }
            nearby.append(item)
            if _match_first(text["text"], rules.get("label_patterns") or [])[0]:
                label_hits.append(item)
        nearby.sort(key=lambda row: (row["distance_m"], row["text"]))

        if block_hit:
            strong = bool(re.search(r"塔|TOWER|QTZ", block, re.I))
            score = float(conf.get("block_strong" if strong else "block_generic", 0.85))
        else:
            score = float(conf.get("layer_only", 0.48))
        if layer_hit:
            score = min(0.96, score + 0.04)
        if label_hits:
            score = min(0.96, score + 0.05)
        if transform_status != "insert_affine":
            score = min(score, 0.75)

        reasons: list[str] = []
        if not block_hit:
            reasons.append("low_confidence_inference")
        if not layer:
            reasons.append("missing_layer")
        if transform_status == "base_point_unavailable":
            reasons.append("missing_block_definition")
        elif transform_status in ("unsupported_ocs", "zero_scale", "missing_insert_point"):
            reasons.append("incomplete_geometry")
        if abs(abs(float(rec.get("xscale") or 1.0)) - abs(float(rec.get("yscale") or 1.0))) > 1e-6:
            reasons.append("geometry_conflict")
        if unit_basis != "explicit":
            reasons.append("missing_unit")
        reasons = list(dict.fromkeys(reasons))

        towers.append({
            "crane_id": "",  # 去重后统一编号
            "text": block,
            "block_name": block,
            "block_pattern": block_pattern,
            "layer": layer or None,
            "layer_pattern": layer_pattern,
            "file": rec["file"],
            "file_name": rec.get("file_name"),
            "sheet": rec.get("sheet"),
            "space": rec.get("space"),
            "handle": rec.get("handle"),
            "insert_point_m": (round(insert_pt[0] * unit_factor, 4), round(insert_pt[1] * unit_factor, 4)) if insert_pt else None,
            "insert_point_drawing": [insert_pt[0], insert_pt[1]] if insert_pt else None,
            "insert_xyz_mm": [insert_pt[0], insert_pt[1], rec.get("z")] if insert_pt else None,
            "rotation_deg": round(float(rec.get("rotation") or 0.0), 6),
            "block_base_point_m": [round(float(rec["base_point"][0]) * unit_factor, 4),
                                   round(float(rec["base_point"][1]) * unit_factor, 4)]
            if isinstance(rec.get("base_point"), (list, tuple)) and rec["base_point"][0] is not None else None,
            "base_point_source": rec.get("base_point_source"),
            "scale": [rec.get("xscale"), rec.get("yscale"), rec.get("zscale")],
            "transform_status": transform_status,
            "center_xy_m": (round(center[0], 4), round(center[1], 4)) if center else None,
            "center_source": "insert_affine" if center else "none",
            # 本脚本不做“邻近文字/圆反推中心”，所以只有插入块仿射变换一种来源。
            # 中心不可算时如实写 unavailable，不伪造 estimated。
            "center_status": "insert_point" if center else "unavailable",
            "model": None,
            "model_text": None,
            "model_status": "unknown",
            "jib_length_m": None,
            "jib_length_source": "none",
            "nearby_texts": nearby[:8],
            "label_evidence": label_hits[:5],
            "evidence": [
                {"kind": "insert", "block_name": block, "layer": layer or None,
                 "coord": [rec.get("x"), rec.get("y")], "rotation_deg": rec.get("rotation"),
                 "scale": [rec.get("xscale"), rec.get("yscale"), rec.get("zscale")],
                 "base_point": rec.get("base_point"), "base_point_source": rec.get("base_point_source")},
            ] + [{"kind": "text", **item} for item in (label_hits or nearby[:3])],
            "confidence": round(score, 4),
            "status": "candidate" if score >= 0.70 else "review",
            "review_reasons": reasons,
            "review_note": "；".join(reasons),
            "x": rec.get("x"),
            "y": rec.get("y"),
            "_anchor_m": tuple(anchor) if anchor else None,
        })

    towers = _dedupe_towers(towers, float(thresholds.get("dedupe_radius_m", 2.0)))
    towers.sort(key=lambda t: (t["file"], t.get("sheet") or -1, t["crane_id"]))
    return towers, rejected


def _dedupe_towers(towers: list[dict], radius_m: float) -> list[dict]:
    ranked = sorted(
        towers,
        key=lambda t: (
            -len(t.get("evidence") or []),
            -float(t.get("confidence") or 0.0),
            t["file"], t.get("sheet") or -1,
            (t.get("center_xy_m") or t.get("insert_point_m") or [0, 0])[0],
            (t.get("center_xy_m") or t.get("insert_point_m") or [0, 0])[1],
            str(t.get("block_name") or ""),
        ),
    )
    kept: list[dict] = []
    for tower in ranked:
        point = tower.get("_anchor_m")
        duplicate = False
        for other in kept:
            if other["file"] != tower["file"]:
                continue
            if other.get("sheet") != tower.get("sheet"):
                continue
            distance = _dist(point, other.get("_anchor_m"))
            if distance is not None and distance <= radius_m:
                duplicate = True
                other.setdefault("duplicates", []).append({
                    "block_name": tower.get("block_name"),
                    "layer": tower.get("layer"),
                    "insert_point_m": tower.get("insert_point_m"),
                    "distance_m": round(distance, 3),
                })
                break
        if not duplicate:
            kept.append(tower)

    order = sorted(kept, key=lambda t: (t["file"], t.get("sheet") or -1,
                                        (t.get("center_xy_m") or t.get("insert_point_m") or [0, 0])[0],
                                        (t.get("center_xy_m") or t.get("insert_point_m") or [0, 0])[1],
                                        str(t.get("block_name") or "")))
    counters: dict[tuple[str, str], int] = {}
    for tower in order:
        key = (_slug(tower.get("layer") or "NOLAYER"), _slug(tower.get("block_name")))
        counters[key] = counters.get(key, 0) + 1
        tower["crane_id"] = f"{key[0]}|{key[1]}|{counters[key]:02d}"
    return order


# ---------------------------------------------------------------- 型号/臂长绑定
def bind_text_evidence(towers: list[dict], rows: list[dict], circles: list[list],
                       rules: dict, unit_factor: float) -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    thresholds = rules.get("thresholds") or {}
    model_radius = float(thresholds.get("model_bind_radius_m", 15.0))
    jib_radius = float(thresholds.get("jib_bind_radius_m", 20.0))
    circle_radius = float(thresholds.get("circle_bind_radius_m", 10.0))
    label_radius = float(thresholds.get("label_bind_radius_m", 30.0))
    min_circle = float(thresholds.get("min_circle_radius_m", 0.2))
    max_circle = float(thresholds.get("max_circle_radius_m", 150.0))
    min_jib = float(thresholds.get("min_jib_m", 10.0))
    max_jib = float(thresholds.get("max_jib_m", 120.0))
    model_re = re.compile(rules.get("model_pattern") or r"(?!)", re.I)

    model_rows: list[dict] = []
    jib_rows: list[dict] = []
    reviews: list[dict] = []

    def anchor_of(tower: dict) -> tuple[float, float] | None:
        return tower.get("_anchor_m")

    def nearest_tower(point: tuple[float, float], file_index: int, limit: float) -> tuple[dict | None, float | None, bool]:
        ranked: list[tuple[float, dict]] = []
        for tower in towers:
            if tower["file"] != file_index:
                continue
            distance = _dist(point, anchor_of(tower))
            if distance is not None:
                ranked.append((distance, tower))
        if not ranked:
            return None, None, False
        ranked.sort(key=lambda item: (item[0], item[1]["crane_id"]))
        distance, tower = ranked[0]
        if distance > limit:
            return None, distance, False
        ambiguous = len(ranked) > 1 and (ranked[1][0] - distance) <= 1.0
        return tower, distance, ambiguous

    # 型号：块名本身是强证据；邻近文字必须落在外接半径内，且不能是“最近文字即型号”。
    for tower in towers:
        block = tower.get("block_name") or ""
        match = model_re.search(block)
        if match:
            model_rows.append({
                "crane_id": tower["crane_id"],
                "model": re.sub(r"\s+", "", match.group(0).upper()),
                "text": block,
                "source": "block_name",
                "distance_m": 0.0,
                "layer": tower.get("layer"),
                "file": tower.get("file"),
                "confidence": float((rules.get("confidence") or {}).get("model_block", 0.9)),
                "status": "candidate",
                "evidence": [{"kind": "block_name", "text": block, "layer": tower.get("layer")}],
            })

    for rec in rows:
        if rec["kind"] == "INSERT" or not rec["text"] or rec.get("x") is None:
            continue
        for match in model_re.finditer(rec["text"]):
            model = re.sub(r"\s+", "", match.group(0).upper())
            point = (float(rec["x"]) * unit_factor, float(rec["y"]) * unit_factor)
            tower, distance, ambiguous = nearest_tower(point, rec["file"], model_radius)
            if tower is None:
                continue
            label_hit = _match_first(rec["text"], rules.get("label_patterns") or [])[0]
            layer_hit = _match_first(rec["layer"], rules.get("layer_patterns") or [])[0]
            # 只有“图层属于塔吊”或“文字自带塔吊/型号标签”才认可；
            # 单纯离得近不算，避免把轴线编号、构件编号当型号。
            strong_context = bool(label_hit or layer_hit or re.search(r"型号", rec["text"]))
            if not strong_context:
                reviews.append({
                    "type": "model_text_context_weak",
                    "crane_id": tower["crane_id"],
                    "message": f"附近文字 {rec['text'][:40]} 命中型号样式，但无塔吊图层/标签，未采纳",
                    "evidence": [{"text": rec["text"], "layer": rec["layer"], "distance_m": round(distance or 0, 3)}],
                })
                continue
            status = "review" if ambiguous else "candidate"
            model_rows.append({
                "crane_id": tower["crane_id"],
                "model": model,
                "text": rec["text"],
                "source": "text",
                "distance_m": round(distance or 0.0, 3),
                "layer": rec["layer"],
                "file": rec["file"],
                "confidence": float((rules.get("confidence") or {}).get("model_text", 0.82)),
                "status": status,
                "binding_ambiguous": ambiguous,
                "evidence": [{"kind": "text", "text": rec["text"], "layer": rec["layer"],
                              "coord": [rec.get("x"), rec.get("y")], "distance_m": round(distance or 0.0, 3)}],
            })

    # 臂长：只认“臂长/起重臂长”明确文字；幅度、工作半径、R= 一律不采纳。
    excluded = rules.get("excluded_jib_keywords") or []
    for rec in rows:
        if rec["kind"] == "INSERT" or not rec["text"] or rec.get("x") is None:
            continue
        if any(re.search(pattern, rec["text"], re.I) for pattern in excluded):
            continue
        for pattern in rules.get("jib_patterns") or []:
            for match in re.finditer(pattern, rec["text"], re.I):
                value = _num(match.group(1))
                if value is None:
                    continue
                point = (float(rec["x"]) * unit_factor, float(rec["y"]) * unit_factor)
                tower, distance, ambiguous = nearest_tower(point, rec["file"], jib_radius)
                if tower is None:
                    continue
                in_range = min_jib <= value <= max_jib
                jib_rows.append({
                    "crane_id": tower["crane_id"],
                    "value": value,
                    "unit": "m",
                    "text": rec["text"],
                    "pattern": pattern,
                    "distance_m": round(distance or 0.0, 3),
                    "layer": rec["layer"],
                    "file": rec["file"],
                    "status": "candidate" if in_range and not ambiguous else "review",
                    "binding_ambiguous": ambiguous,
                    "in_range": in_range,
                    "evidence": [{"kind": "text", "text": rec["text"], "layer": rec["layer"],
                                  "coord": [rec.get("x"), rec.get("y")],
                                  "distance_m": round(distance or 0.0, 3)}],
                })

    # 汇总到塔吊：多型号=ambiguous；多臂长=conflict；无证据=unknown/none。
    by_crane_models: dict[str, list[dict]] = {}
    for row in model_rows:
        if row.get("status") == "candidate" and not row.get("binding_ambiguous"):
            by_crane_models.setdefault(row["crane_id"], []).append(row)
    by_crane_jib: dict[str, list[dict]] = {}
    for row in jib_rows:
        if row.get("status") == "candidate":
            by_crane_jib.setdefault(row["crane_id"], []).append(row)

    for tower in towers:
        model_rows_for_tower = by_crane_models.get(tower["crane_id"], [])
        models = {row["model"] for row in model_rows_for_tower}
        if len(models) == 1:
            tower["model"] = next(iter(models))
            tower["model_text"] = model_rows_for_tower[0].get("text")
            tower["model_status"] = "candidate"
        elif len(models) > 1:
            # 严格保持 model_status ∈ {candidate, unknown}；冲突用独立标志暴露，不硬选。
            tower["model_status"] = "unknown"
            tower["model_ambiguity"] = sorted(models)
            tower["review_reasons"] = list(dict.fromkeys(tower["review_reasons"] + ["ambiguous_text_binding"]))
        else:
            tower["model_status"] = "unknown"

        jibs = {row["value"] for row in by_crane_jib.get(tower["crane_id"], [])}
        if len(jibs) == 1:
            tower["jib_length_m"] = next(iter(jibs))
            tower["jib_length_source"] = "text"
        elif len(jibs) > 1:
            # 臂长来源只保留 text/none；冲突值放 jib_conflict_values，臂长留空。
            tower["jib_length_source"] = "none"
            tower["jib_conflict_values"] = sorted(jibs)
            tower["review_reasons"] = list(dict.fromkeys(tower["review_reasons"] + ["ambiguous_text_binding"]))
        else:
            tower["jib_length_source"] = "none"

        tower["review_note"] = "；".join(tower["review_reasons"])
        if tower["review_reasons"]:
            tower["status"] = "review"
            tower["confidence"] = min(float(tower["confidence"]), 0.72)

    # 圆：只作旁证，绝不写入 jib_length_m。
    circle_rows: list[dict] = []
    for circle in circles:
        x, y, radius, layer, file_index = circle
        radius_m = float(radius) * unit_factor
        if not (min_circle <= radius_m <= max_circle):
            continue
        point = (float(x) * unit_factor, float(y) * unit_factor)
        annotation_layer = bool(re.search(r"图例|标注|LEGEND|ANNO|DIM|TEXT", layer or "", re.I))
        # 图例/标注圈的绑定半径放宽到 label 半径，否则 20 m 外的模板圈会直接消失；
        # 但它只进 radius_circles_m(source=annotation)，绝不当臂长。
        circle_limit = max(circle_radius, label_radius) if annotation_layer else circle_radius
        tower, distance, _ambiguous = nearest_tower(point, file_index, circle_limit)
        if tower is None:
            continue
        insert = tower.get("insert_point_m")
        insert_distance = _dist(point, tuple(insert) if insert else None)
        # 规则口径：距插入点 >1 m 或落在图例/标注图层的圆，只作 annotation 旁证。
        circle_source = "annotation" if annotation_layer or (insert_distance is not None and insert_distance > 1.0) else "geometry"
        circle_rows.append({
            "crane_id": tower["crane_id"],
            "center_xy_m": [round(point[0], 4), round(point[1], 4)],
            "radius_m": round(radius_m, 4),
            "distance_m": round(distance or 0.0, 4),
            "insert_distance_m": round(insert_distance, 4) if insert_distance is not None else None,
            "source": circle_source,
            "layer": layer,
            "file": file_index,
            "used_as_jib_length": False,
            "note": "圆半径仅作旁证；未写入 jib_length_m",
        })

    for tower in towers:
        tower["radius_circles_m"] = [
            row for row in circle_rows if row["crane_id"] == tower["crane_id"]
        ]
        if not tower["radius_circles_m"]:
            reviews.append({
                "type": "no_radius_circle",
                "crane_id": tower["crane_id"],
                "message": "回转中心附近未找到可用圆实体；不影响位置候选，但缺少半径旁证",
                "evidence": [{"center_xy_m": tower.get("center_xy_m")}],
            })
        if tower["model_status"] == "unknown":
            reviews.append({"type": "model_unknown", "crane_id": tower["crane_id"],
                            "message": "未找到型号的明确文字/块名证据"})
        if tower.get("model_ambiguity"):
            reviews.append({"type": "model_ambiguous", "crane_id": tower["crane_id"],
                            "message": "同一塔吊附近出现多个不同型号，未强行选择"})
        if tower["jib_length_source"] == "none":
            reviews.append({"type": "jib_unknown", "crane_id": tower["crane_id"],
                            "message": "未找到“臂长/起重臂长”明确文字；圆半径不当作臂长"})
        if tower.get("jib_conflict_values"):
            reviews.append({"type": "jib_conflict", "crane_id": tower["crane_id"],
                            "message": "同一塔吊附近出现多个不同臂长值，未强行选择"})
        if tower["transform_status"] != "insert_affine":
            reviews.append({"type": "center_unavailable", "crane_id": tower["crane_id"],
                            "message": f"回转中心不可算：{tower['transform_status']}（不伪造中心坐标）"})

    for tower in towers:
        tower.pop("_anchor_m", None)
    return model_rows, jib_rows, circle_rows, reviews


# ---------------------------------------------------------------- 输出
def build_payload(input_path: Path, rows: list[dict], circles: list[list], meta: dict,
                  notes: list[str], source_paths: list[str], input_kind: str,
                  unit: str, rules: dict, started_at: str, argv: list[str],
                  extra_block_patterns: list[str] | None = None,
                  extra_layer_patterns: list[str] | None = None,
                  unit_explicit: bool = True) -> dict:
    unit_factor = 0.001 if unit == "mm" else 1.0
    # 只有 CLI 显式给出 --drawing-unit 才算 explicit；默认 mm 仅用于计算，
    # 不能冒充单位已知，否则会把“按 mm 猜”的坐标混进主线。
    unit_basis = "explicit" if unit_explicit else "assumed_mm"
    towers, rejected = detect_towers(rows, rules, unit_factor, unit_basis,
                                     extra_block_patterns, extra_layer_patterns)
    model_rows, jib_rows, circle_rows, reviews = bind_text_evidence(
        towers, rows, circles, rules, unit_factor)

    # 单位来源：CLI 明确给出才算 explicit；默认 mm 必须标 missing_unit，不冒充已知。
    if unit_basis != "explicit":
        for tower in towers:
            if "missing_unit" not in tower["review_reasons"]:
                tower["review_reasons"].append("missing_unit")
            tower["review_note"] = "；".join(tower["review_reasons"])
            tower["status"] = "review"
            tower["confidence"] = min(float(tower["confidence"]), 0.72)

    summary = {
        "tower_cranes": len(towers),
        "confirmed_towers": sum(1 for t in towers if t["status"] == "candidate"),
        "review_towers": sum(1 for t in towers if t["status"] == "review"),
        "model_candidates": sum(1 for r in model_rows if r.get("status") == "candidate"),
        "jib_evidence": sum(1 for r in jib_rows if r.get("status") == "candidate"),
        "radius_circles": len(circle_rows),
        "rejected_blocks": len(rejected),
        "review_items": len(reviews),
    }
    payload = {
        "schema": SCHEMA,
        "reader_version": reader_version(),
        "generated_at": _now(),
        "source": {
            "input": input_path.name,
            "input_kind": input_kind,
            "source_paths": source_paths,
            "file_count": len({r["file"] for r in rows}) or 1,
        },
        "units": {
            "drawing_unit": unit,
            "length_factor_m": unit_factor,
            "basis": unit_basis,
        },
        "summary": summary,
        # 任务契约首选名 crane_layout[]；towers 为同内容兼容别名，二者指向同一列表。
        "crane_layout": towers,
        "towers": towers,
        "model_candidates": model_rows,
        "jib_evidence": jib_rows,
        "radius_circles": circle_rows,
        "rejected_blocks": rejected,
        "review": reviews,
        "notes": notes,
        "limitations": [
            "只输出识图与几何候选；不判断塔吊覆盖是否满足、不验算基础/附着/群塔防碰撞。",
            "回转中心由 INSERT 插入点、块基点、旋转和缩放推算；DWG 直读拿不到块基点时中心为 null。",
            "圆半径只进 radius_circles_m，绝不当臂长；臂长只认“臂长/起重臂长”明确文字。",
            "型号只认块名或塔吊图层/标签附近的明确型号文字，不按命名规则反推。",
            "默认按 mm 解释坐标；未显式指定单位时所有塔吊进 review。",
        ],
        "boundary": "识图候选，final_quantity=false；不选型、不验算、不替代厂家资料、施工方案和审批。",
    }
    source_names = [Path(p).name for p in source_paths] or [input_path.name]
    contractize_payload(
        payload,
        source=source_names,
        source_path=source_paths[0] if source_paths else None,
        run_info={
            "command": "cad_crane_geometry",
            "argv": argv,
            "started_at": started_at,
            "finished_at": _now(),
            "input_kind": input_kind,
        },
    )
    return payload


def _fmt(value: Any, digits: int = 3) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.{digits}f}".rstrip("0").rstrip(".")
    return str(value)


def write_outputs(payload: dict, input_path: Path, out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = input_path.stem
    if stem.endswith(".crane"):
        stem = stem[:-6]
    json_path = out_dir / f"{stem}.crane.json"
    md_path = out_dir / f"{stem}.crane.md"
    csv_path = out_dir / f"{stem}.crane.csv"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")

    lines = [
        f"# 塔吊布置识图 · {input_path.name}",
        "",
        f"- 塔吊候选：{payload['summary']['tower_cranes']}（confirmed {payload['summary']['confirmed_towers']} / review {payload['summary']['review_towers']}）",
        f"- 型号候选：{payload['summary']['model_candidates']}；臂长证据：{payload['summary']['jib_evidence']}；圆旁证：{payload['summary']['radius_circles']}",
        f"- 单位：{payload['units']['drawing_unit']}（{payload['units']['basis']}）",
        "",
        "| crane_id | 块名 | 图层 | 回转中心 (m) | 旋转° | 型号 | 臂长 m | 状态 |",
        "|---|---|---|---|---:|---|---:|---|",
    ]
    for tower in payload["towers"]:
        center = tower.get("center_xy_m")
        center_text = f"{_fmt(center[0])}, {_fmt(center[1])}" if center else "—"
        lines.append(
            f"| {tower['crane_id']} | {tower.get('block_name') or ''} | {tower.get('layer') or ''} | "
            f"{center_text} | {_fmt(tower.get('rotation_deg'))} | {tower.get('model') or ''} | "
            f"{_fmt(tower.get('jib_length_m'))} | {tower['status']} |"
        )
    lines += ["", "## 型号证据", ""]
    if payload["model_candidates"]:
        lines += ["| crane_id | 型号 | 来源 | 距离 m | 原文 | 状态 |", "|---|---|---|---:|---|---|"]
        for row in payload["model_candidates"]:
            lines.append(f"| {row['crane_id']} | {row['model']} | {row['source']} | {_fmt(row.get('distance_m'))} | {row['text']} | {row['status']} |")
    else:
        lines.append("无。未找到块名或邻近文字中的明确型号。")
    lines += ["", "## 臂长证据", ""]
    if payload["jib_evidence"]:
        lines += ["| crane_id | 臂长 m | 距离 m | 原文 | 状态 |", "|---|---:|---:|---|---|"]
        for row in payload["jib_evidence"]:
            lines.append(f"| {row['crane_id']} | {_fmt(row.get('value'))} | {_fmt(row.get('distance_m'))} | {row['text']} | {row['status']} |")
    else:
        lines.append("无。圆半径不当作臂长。")
    lines += ["", "## 圆旁证（不参与臂长）", ""]
    if payload["radius_circles"]:
        lines += ["| crane_id | 半径 m | 圆心 (m) | 距中心 m | 图层 |", "|---|---:|---|---:|---|"]
        for row in payload["radius_circles"]:
            center = row["center_xy_m"]
            lines.append(f"| {row['crane_id']} | {_fmt(row['radius_m'])} | {_fmt(center[0])}, {_fmt(center[1])} | {_fmt(row['distance_m'])} | {row.get('layer') or ''} |")
    else:
        lines.append("无。")
    lines += ["", "## 复核项", ""]
    if payload["review"]:
        for item in payload["review"]:
            cid = item.get("crane_id")
            lines.append(f"- {'[' + cid + '] ' if cid else ''}{item['type']}：{item['message']}")
    else:
        lines.append("无。")
    lines += ["", "## 边界", "", payload["boundary"], ""]
    md_path.write_text("\n".join(lines), encoding="utf-8")

    with csv_path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["crane_id", "block_name", "layer", "file", "sheet", "insert_x_m", "insert_y_m",
                         "center_x_m", "center_y_m", "rotation_deg", "model", "model_status",
                         "jib_length_m", "jib_length_source", "confidence", "status"])
        for tower in payload["towers"]:
            insert = tower.get("insert_point_m") or [None, None]
            center = tower.get("center_xy_m") or [None, None]
            writer.writerow([
                tower["crane_id"], tower.get("block_name"), tower.get("layer"),
                tower.get("file_name") or tower.get("file"), tower.get("sheet"),
                _fmt(insert[0]), _fmt(insert[1]), _fmt(center[0]), _fmt(center[1]),
                _fmt(tower.get("rotation_deg")), tower.get("model"), tower.get("model_status"),
                _fmt(tower.get("jib_length_m")), tower.get("jib_length_source"),
                _fmt(tower.get("confidence")), tower.get("status"),
            ])
    return [json_path, md_path, csv_path]


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(
        description="塔吊布置识图：插入点→回转中心、型号/臂长证据；不选型、不验算。")
    parser.add_argument("input", help="DXF/DWG 或 cad_scan --detail-json 产物")
    parser.add_argument("--out-dir", default=None, help="输出目录（默认输入同目录 crane-out）")
    parser.add_argument("--drawing-unit", choices=["mm", "m"], default=None,
                        help="图纸单位；不填默认按 mm 解释并全部进 review")
    parser.add_argument("--max-rows", type=int, default=200000, help="文字/块引用行数上限")
    parser.add_argument("--source-drawing", default=None,
                        help="详情 JSON 输入时，指定原图路径用于 source_sha256")
    parser.add_argument("--block", action="append", default=[],
                        help="额外块名匹配（可重复；逗号分隔，按字面量匹配）")
    parser.add_argument("--layer", action="append", default=[],
                        help="额外图层匹配（可重复；逗号分隔，按字面量匹配）")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    started_at = _now()
    input_path = Path(args.input).expanduser()
    if not input_path.is_file():
        print(f"❌ 输入不存在：{input_path}", file=sys.stderr)
        return 2
    log = (lambda _s: None) if args.quiet else (lambda s: print(s, file=sys.stderr))

    try:
        rows, circles, meta, notes, source_paths, input_kind = load_input(input_path, args.max_rows, log)
    except SystemExit as exc:
        print(f"❌ {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"❌ 解析失败：{type(exc).__name__} {exc}", file=sys.stderr)
        return 3

    if args.source_drawing:
        source_paths = [str(Path(args.source_drawing).expanduser().resolve())]
    rules = load_rules()
    unit = args.drawing_unit or "mm"
    extra_blocks = [re.escape(v.strip()) for raw in args.block for v in raw.split(",") if v.strip()]
    extra_layers = [re.escape(v.strip()) for raw in args.layer for v in raw.split(",") if v.strip()]
    payload = build_payload(input_path, rows, circles, meta, notes, source_paths, input_kind,
                            unit, rules, started_at, argv, extra_blocks, extra_layers,
                            unit_explicit=args.drawing_unit is not None)
    out_dir = Path(args.out_dir).expanduser() if args.out_dir else input_path.parent / "crane-out"
    written = write_outputs(payload, input_path, out_dir)
    print(f"塔吊候选 {payload['summary']['tower_cranes']} 个；输出 " + "、".join(str(p) for p in written))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
