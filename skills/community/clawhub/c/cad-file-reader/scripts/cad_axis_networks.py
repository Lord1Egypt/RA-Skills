#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""可选 axis_networks[] 轴网/轴号候选（cad-file-reader/v0 契约扩展，向后兼容）。

只消费 cad_scan 已产出的详情JSON（text_records + geometry_segments，
geometry_layers 可选）；本模块不改写既有业务数组，只在 payload 追加可选字段：

- data["axis_networks"]          : list[axis network]
- data["axis_networks_summary"]  : {networks, usable, degraded, sheets}
- data["contract"]["axis_networks"] : 同 data["axis_networks"]（仅当 contract 已存在）

识别口径（人看图看轴线）：
1. 轴号文字：图层含 AXIS/轴号/轴标/轴网/定位，文本为纯数字（数字轴）或单字母（字母轴）。
2. 轴线：在轴号坐标附近找同方向长线段作几何佐证（坐标降为佐证，不强制）。
3. 轴格区间：同一 sheet 内按坐标排序，相邻轴距即开间（grid.spans）。

识别不到轴网如实标 missing/degraded，不允许伪装成 pass。
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Optional

AXIS_LABEL_LAYER = re.compile(r"AXIS|轴号|轴标|轴网|定位", re.I)
NUMERIC_AXIS = re.compile(r"^([0-9]{1,3})$")
ALPHA_AXIS = re.compile(r"^([A-ZА-Я])$")
AXIS_MATCH_TOL = 250.0      # 轴号与轴线坐标容差(mm)
MIN_LINE_LEN = 1200.0       # 用于佐证的轴线最短长度(mm)
MIN_GROUP = 3               # 少于该轴数只能 degraded
VIEW_SPLIT_CEIL = 30000.0   # 跨视图断点：开间超过该值视为另一套轴网
AXIS_NETWORK_SCHEMA = "cad-axis-networks/v1"


def _float(value: Any) -> Optional[float]:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _norm(label: str, layer: str, x: Any, y: Any) -> str:
    one = f"{label}|{layer}|{x:.3f}|{y:.3f}"
    return one


def axis_label_candidates(data: dict[str, Any]) -> list[dict[str, Any]]:
    """从 text_records 提取轴号文字候选（按 sheet/坐标记录原始证据）。"""
    out: list[dict[str, Any]] = []
    records = data.get("text_records") or []
    for raw in records:
        if not isinstance(raw, dict):
            continue
        text = str(raw.get("text", "")).strip()
        if not text:
            continue
        layer = str(raw.get("layer", "") or "")
        if not AXIS_LABEL_LAYER.search(layer):
            continue
        axis_type = None
        if NUMERIC_AXIS.match(text):
            axis_type = "numeric"
        elif ALPHA_AXIS.match(text):
            axis_type = "alpha"
        else:
            continue
        x = _float(raw.get("x"))
        y = _float(raw.get("y"))
        if x is None or y is None:
            continue
        sheet = raw.get("sheet")
        out.append({
            "axis_id": text,
            "label": text,
            "axis_type": axis_type,
            "x": x,
            "y": y,
            "sheet": sheet,
            "layer": layer,
            "kind": str(raw.get("kind", "TEXT")),
            "file": raw.get("file"),
            "file_name": raw.get("file_name"),
            "handle": raw.get("handle"),
        })
    return out


def _geometry_segments(data: dict[str, Any]) -> list[list[float]]:
    """压平 cad_scan 的 geometry_segments（一层文件分组可选）。"""
    gs = data.get("geometry_segments") or []
    out: list[list[float]] = []
    for group in gs:
        if not isinstance(group, list):
            continue
        if group and isinstance(group[0], list):
            for seg in group:
                if isinstance(seg, (list, tuple)) and len(seg) >= 4:
                    nums = [_float(v) for v in seg[:4]]
                    if all(n is not None for n in nums):
                        out.append([float(n) for n in nums])  # type: ignore[misc]
        else:
            for seg in group:
                if isinstance(seg, (list, tuple)) and len(seg) >= 4:
                    nums = [_float(v) for v in seg[:4]]
                    if all(n is not None for n in nums):
                        out.append([float(n) for n in nums])  # type: ignore[misc]
    return out


def _line_index(segments: list[list[float]]):
    """按几何方向建桶：V=竖直、H=水平。"""
    v: dict[float, list[list[float]]] = defaultdict(list)
    h: dict[float, list[list[float]]] = defaultdict(list)
    for seg in segments:
        x1, y1, x2, y2 = seg[:4]
        if x1 is None or y1 is None or x2 is None or y2 is None:
            continue
        if abs(y2 - y1) <= 1e-3 and abs(x2 - x1) >= MIN_LINE_LEN:
            h[y1].append([min(x1, x2), max(x1, x2), x1, x2])
        elif abs(x2 - x1) <= 1e-3 and abs(y2 - y1) >= MIN_LINE_LEN:
            v[x1].append([min(y1, y2), max(y1, y2), y1, y2])
    for bucket in (v, h):
        for key in list(bucket.keys()):
            bucket[key].sort()
    return v, h


def _near(positions: dict[float, list[list[float]]], target: float, tolerance: float) -> Optional[list[float]]:
    """返回与 target 最近的线段 [a,b]，无则 None。"""
    best = None
    best_dx = tolerance + 1.0
    # 只在容差内的键中找一个最近的
    for pos, spans in positions.items():
        dx = abs(pos - target)
        if dx > tolerance or dx > best_dx:
            continue
        best_dx = dx
        best = spans[0] if spans else None
    return best


def _dedupe_axes(cands: list[dict[str, Any]], direction: str) -> list[dict[str, Any]]:
    """同一根轴的首尾常有重复轴号（如数字同时标在顶部/底部），按坐标位置去重。"""
    seen: set[float] = set()
    out: list[dict[str, Any]] = []
    for cand in sorted(cands, key=lambda c: c["x"] if direction == "V" else c["y"]):
        pos = cand["x"] if direction == "V" else cand["y"]
        if any(abs(pos - other) <= 1.0 for other in seen):
            # 保留最早出现；重复轴号只留给更靠近轴线的证据记录
            continue
        seen.add(pos)
        out.append(cand)
    return out


def _split_views(axes: list[dict[str, Any]], direction: str) -> list[list[dict[str, Any]]]:
    """开间远超正常范围时按视图断开。"""
    if not axes:
        return []
    clusters: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = [axes[0]]
    for a, b in zip(axes, axes[1:]):
        pos_a = a["x"] if direction == "V" else a["y"]
        pos_b = b["x"] if direction == "V" else b["y"]
        if abs(pos_b - pos_a) > VIEW_SPLIT_CEIL:
            clusters.append(current)
            current = []
        current.append(b)
    clusters.append(current)
    return clusters


def axis_networks(data: dict[str, Any]) -> list[dict[str, Any]]:
    """从已解析产物还原轴网候选；缺轴网时返回 [] 并可由调用方标 missing。"""
    cands = axis_label_candidates(data)
    if not cands:
        return []
    segments = _geometry_segments(data)
    v_idx, h_idx = _line_index(segments)

    by_sheet: dict[Any, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: {"numeric": [], "alpha": []})
    for cand in cands:
        by_sheet[cand["sheet"]][cand["axis_type"]].append(cand)

    networks: list[dict[str, Any]] = []
    for sheet, groups in by_sheet.items():
        # 数字轴→竖直排列；字母轴→水平排列
        for axis_type, direction in (("numeric", "V"), ("alpha", "H")):
            uniq = _dedupe_axes(groups[axis_type], direction)
            for view in _split_views(uniq, direction):
                if len(view) < 2:
                    continue  # 单独 1 轴不构成轴网
                axes_out: list[dict[str, Any]] = []
                matched = 0
                positions: list[float] = []
                for cand in view:
                    pos = cand["x"] if direction == "V" else cand["y"]
                    along = cand["y"] if direction == "V" else cand["x"]
                    span = None
                    if direction == "V":
                        line = _near(v_idx, pos, AXIS_MATCH_TOL)
                    else:
                        line = _near(h_idx, pos, AXIS_MATCH_TOL)
                    if line:
                        span = [round(line[0], 1), round(line[1], 1)]
                        matched += 1
                    evidence = [{
                        "kind": cand["kind"],
                        "text": cand["label"],
                        "layer": cand["layer"],
                    }]
                    if cand.get("file_name") or cand.get("file"):
                        evidence[0]["file"] = cand.get("file_name") or cand.get("file")
                    if cand.get("handle") is not None:
                        evidence[0]["handle"] = cand["handle"]
                    axes_out.append({
                        "axis_id": cand["label"],
                        "label": cand["label"],
                        "pos": round(pos, 3),
                        "along": round(along, 3),
                        "line_span": span,
                        "evidence": evidence,
                    })
                    positions.append(pos)
                spans = [round(positions[i + 1] - positions[i], 1) for i in range(len(positions) - 1)]
                usable = len(positions) >= MIN_GROUP
                ratio = matched / len(positions) if positions else 0.0
                confidence = round(min(0.98, 0.55 * (len(positions) / MIN_GROUP) + 0.25 * ratio), 2)
                # 基线置信度并不安全性高：轴上几何佐证缺失时主动降档（无轴降级原则）
                if segments and matched == 0:
                    confidence = round(min(confidence, 0.55), 2)
                elif ratio < 0.5:
                    confidence = round(min(confidence, 0.70), 2)
                status = "usable" if usable else "degraded"
                if segments and matched == 0:
                    geometry_status = "no_line_match"
                elif not segments:
                    geometry_status = "no_geometry_input"
                else:
                    geometry_status = "matched"
                networks.append({
                    "schema": AXIS_NETWORK_SCHEMA,
                    "sheet": sheet,
                    "floor": sheet,
                    "axis_type": axis_type,
                    "direction": direction,
                    "axis_count": len(positions),
                    "grid": {
                        "positions": [round(p, 4) for p in positions],
                        "spans": spans,
                        "total_span": round(sum(spans), 1) if spans else 0.0,
                    },
                    "axes": axes_out,
                    "geometry_matched": matched,
                    "geometry_status": geometry_status,
                    "confidence": confidence,
                    "status": status,
                    "basis": {"text": len(positions), "geometry": bool(segments)},
                })
    networks.sort(key=lambda n: (-n["axis_count"], str(n["sheet"]), n["axis_type"]))
    return networks


def axis_networks_summary(networks: list[dict[str, Any]]) -> dict[str, Any]:
    usable = [n for n in networks if n["status"] == "usable"]
    degraded = [n for n in networks if n["status"] == "degraded"]
    sheets = sorted({str(n["sheet"]) for n in networks if n["sheet"] is not None})
    return {
        "networks": len(networks),
        "usable": len(usable),
        "degraded": len(degraded),
        "sheets": sheets,
        "status": "available" if usable else ("degraded" if degraded else "missing"),
    }


def merge_axis_networks(data: dict[str, Any]) -> dict[str, Any]:
    """把 axis_networks 追加进已有 payload/contract；不改写既有业务数组。"""
    nets = axis_networks(data)
    data["axis_networks"] = nets
    data["axis_networks_summary"] = axis_networks_summary(nets)
    contract = data.get("contract")
    if isinstance(contract, dict):
        contract["axis_networks"] = nets
        contract["axis_networks_summary"] = data["axis_networks_summary"]
    return data


def _main() -> None:
    ap = argparse.ArgumentParser(description="从 cad_scan 详情 JSON 提取可选 axis_networks[]")
    ap.add_argument("--inputs", nargs="+", required=True, help="cad_scan 详情 JSON（可直接复用已有产物）")
    ap.add_argument("--out", default="", help="输出报告 JSON 路径；默认 stdout")
    args = ap.parse_args()

    rows = []
    total = 0
    usable = 0
    degraded = 0
    for value in args.inputs:
        path = Path(value)
        data = json.loads(path.read_text(encoding="utf-8"))
        merge_axis_networks(data)
        summary = data["axis_networks_summary"]
        total += summary["networks"]
        usable += summary["usable"]
        degraded += summary["degraded"]
        rows.append({
            "file": path.name,
            "path": str(path),
            "network_count": summary["networks"],
            "usable": summary["usable"],
            "degraded": summary["degraded"],
            "status": summary["status"],
            "axis_networks": data["axis_networks"],
        })
    payload = {
        "schema": AXIS_NETWORK_SCHEMA,
        "inputs": len(rows),
        "summary": {"networks": total, "usable": usable, "degraded": degraded},
        "files": rows,
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(json.dumps(payload["summary"], ensure_ascii=False))
    else:
        print(text)


if __name__ == "__main__":
    _main()
