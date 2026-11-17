#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cad_clash_check.py —— 跨专业碰撞校对一条龙（cad-clash-check v0.3，轴格主判）。

把图纸（DWG/DXF）或现成识图产物塞进来，自动完成：
  识图（cad-file-reader）→ 专业判定 → 构件清单（clash_adapt）→
  两两比较 → 输出「空间碰撞候选 + 构件属性冲突」报告（json + md）。

v0.3 轴格主判（消费 cad-file-reader 可选 axis_networks[]）：
  * 构件 bbox → 轴格区间；同格不同专业 → 碰撞候选，坐标降为佐证；
  * 两侧都有可用轴网才走轴格判定；缺轴网自动退回 v0.2 坐标判定并标
    axis_missing=degraded；
  * 跨图坐标不主判，跨图轴号同格可直接配对。
v0.2 契约流（相对 0.1.x）：
  * SPEC_PIPELINE 新增 MEP（电气/暖通/给排水 → cad_mep_geometry.py）与
    building（建筑 → 结构墙 + 门窗洞口合并器 clash_building_extract.py）；
  * 构件统一带 sheet/floor/axis/坐标/类型，报告逐条给出 A/B 两侧证据；
  * 洞口语义：MEP × 门窗洞口 = 预留通道（opening_pass），不算碰撞；
    墙 × 洞口 = 正常关系；墙 × MEP = 潜在穿墙无洞（进候选，提示复核）；
  * 识图器没产出墙/洞口时如实 degraded，不冒充 pass；
  * 输出附带施工计划模板（*_construct_plan.json/md）与 v0.2 状态文件。

诚实边界（必须随结果告知）：
  * 2D 图面的**重叠/冲突倾向提示**，不是 BIM 碰撞检测（无 3D 模型）；
  * 「碰撞」= 不同专业构件在图面同位出现，是**待人工复核的候选**；
  * 不输出工程量（final_quantity=false），图纸数据只落本机。

用法
    # 一条龙：图纸直进
    python3 cad_clash_check.py 结构.dwg 给排水.dwg -o 报告/clash
    # 离线：已有识图产物（*.structural.json / *.municipal.json / *.mep.json / *.building.json）
    python3 cad_clash_check.py a.detail.json b.detail.municipal.json -o 报告/clash
    # 调参：--clash-tol 空间碰撞距离上限（图面单位，默认 800）
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clash_engine import CrossEngine, Member  # noqa: E402
import clash_adapt  # noqa: E402

DEFAULT_CLASH_TOL = 800.0    # 空间碰撞距离上限（图面单位）
GROUP_BUCKET = 20000.0       # 碰撞点分组桶尺寸（同一根管穿一排梁归一组）
MAX_CLASH_ITEMS = 2000       # 碰撞明细上限（防止刷屏）
MAX_MD_ITEMS = 40            # md 报告每组最多展示条数
STATE_SCHEMA = "cad-clash-check/v2"
STATE_FILE = "state-v2.json"

# 专业判定关键词（按序评分，取最高分；阈值 2 分起判）
SPEC_KEYWORDS: list[tuple[str, list[str]]] = [
    ("市政", ["室外管网", "市政", "综合管线", "管线综合", "雨污水", "浇灌"]),
    ("给排水", ["给排水", "喷淋", "消防给水", "室内排水", "室内给水"]),
    ("结构", ["平法", "结构", "基础平面", "桩位", "模板图"]),
    ("建筑", ["建筑施工图", "建筑平面", "建筑设计", "总平面", "户型"]),
    ("电气", ["电气", "照明平面", "配电", "防雷"]),
    ("暖通", ["暖通", "空调", "通风", "防排烟"]),
]
SPEC_SCORE_MIN = 2

_MEP_TYPES = ["route_segments", "equipment", "risers", "systems"]
_MEP_CFG = {"script": "cad_mep_geometry.py", "types": _MEP_TYPES,
            "suffix": "mep", "home": "cfr"}

# 专业 → 提取器配置（home=cfr 表示 cad-file-reader/scripts；local 表示本 skill scripts）
SPEC_PIPELINE = {
    "结构": {"script": "cad_structural_geometry.py",
            "types": ["members", "components", "structural_geometry"],
            "suffix": "structural", "home": "cfr"},
    "建筑": {"script": "clash_building_extract.py",
            "types": ["members"], "suffix": "building", "home": "local"},
    "市政": {"script": "cad_municipal_geometry.py",
            "types": ["components", "municipal_geometry", "entities"],
            "suffix": "municipal", "home": "cfr"},
    "给排水": dict(_MEP_CFG),
    "电气": dict(_MEP_CFG),
    "暖通": dict(_MEP_CFG),
    "MEP": dict(_MEP_CFG),
}


# ---------------------------------------------------------------- 专业判定
def classify_specialty(texts: list[str]) -> str:
    """按关键词命中数判定图纸专业；均不足阈值时返回 未知。"""
    sample = [str(t) for t in texts[:3000]]
    best, best_n = "未知", 0
    for spec, kws in SPEC_KEYWORDS:
        n = sum(t.count(k) for t in sample for k in kws)
        if n > best_n:
            best, best_n = spec, n
    return best if best_n >= SPEC_SCORE_MIN else "未知"


def classify_detail(data: dict) -> str:
    """识图/提取产物专业判定：文字关键词优先，无文字时按产物结构回退。"""
    texts = [t.get("text", "") if isinstance(t, dict) else str(t)
             for t in data.get("text_records") or []]
    spec = classify_specialty(texts)
    if spec != "未知":
        return spec
    keys = set(data.keys())
    if {"route_segments", "equipment", "risers", "mep_relations",
        "vertical_routes", "connectivity", "topology"} & keys:
        return "MEP"
    if {"walls", "openings", "members"} & keys and "building" in str(data.get("schema", "")):
        return "建筑"
    if "municipal_geometry" in keys or "pipe_candidates" in keys:
        return "市政"
    if "members" in keys or "steel_profiles" in keys or "connections" in keys:
        return "结构"
    return "未知"


# ---------------------------------------------------------------- 空间碰撞
def box_gap(a: list, b: list) -> float:
    """两 bbox 的间隙；重叠返回 0。"""
    dx = max(a[0] - b[2], b[0] - a[2], 0.0)
    dy = max(a[1] - b[3], b[1] - a[3], 0.0)
    return (dx * dx + dy * dy) ** 0.5


def _cells(bbox: list, cell: float) -> list[tuple[int, int]]:
    x0, y0, x1, y1 = bbox
    return [(ix, iy)
            for ix in range(int(x0 // cell), int(x1 // cell) + 1)
            for iy in range(int(y0 // cell), int(y1 // cell) + 1)]



# ---------------------------------------------------------------- 轴格判定（P2：消费 axis_networks[]，坐标降为佐证）
AXIS_GRID_SCHEMA = "cad-clash-axis-grid/v1"


def _axis_grid_for_sheet(grid: dict, sheet) -> dict | None:
    """取 sheet 对应网格；未命中时合并所有 sheet（跨 sheet 轴号通常一致）。"""
    if not grid:
        return None
    key = str(sheet)
    if key in grid:
        return grid[key]
    merged: dict[str, list] = {"V": [], "H": []}
    for g in grid.values():
        merged["V"].extend(g.get("V", []))
        merged["H"].extend(g.get("H", []))
    return merged if (merged["V"] or merged["H"]) else None


def _axis_networks_from_data(data: dict, cfr: Path | None = None):
    """已解析产物 → axis_networks 可选字段；缺字段时走 cad-file-reader 薄层增量。

    薄层增量只消费已有 text_records / geometry_segments，不重新整图识图。
    """
    nets = data.get("axis_networks")
    summary = data.get("axis_networks_summary")
    if isinstance(nets, list):
        usable = sum(1 for n in nets if n.get("status") == "usable")
        if isinstance(summary, dict):
            return nets, summary
        return nets, {"networks": len(nets), "usable": usable,
                      "degraded": len(nets) - usable,
                      "status": "available" if usable else ("degraded" if nets else "missing")}
    # P1 只更新了 $CODEX_SKILLS_DIR 副本；find_cfr 可能先命中未同步的 ~/.workbuddy 旧副本，
    # 因此薄层轴网优先定位带 cad_axis_networks.py 的 cad-file-reader/scripts。
    candidates: list[Path] = []
    if cfr is not None:
        candidates.append(cfr)
    env_val = os.environ.get("CAD_FILE_READER_HOME", "").strip()
    if env_val:
        candidates.append(Path(env_val))
    for base in (Path.home() / ".codex" / "skills",
                 Path.home() / ".workbuddy" / "skills"):
        candidates.append(base / "cad-file-reader" / "scripts")
    chosen = next((c for c in candidates
                   if c.is_dir() and (c / "cad_axis_networks.py").exists()), None)
    if chosen is None:
        try:
            chosen = find_cfr()
        except FileNotFoundError:
            chosen = None
    if chosen is not None and (chosen / "cad_axis_networks.py").exists():
        if str(chosen) not in sys.path:
            sys.path.insert(0, str(chosen))
        import cad_axis_networks as _axis_mod  # noqa: PLC0415
        nets = _axis_mod.axis_networks(data)
        return nets, _axis_mod.axis_networks_summary(nets)
    return [], {"networks": 0, "usable": 0, "degraded": 0, "sheets": [],
                "status": "missing"}


def _interval_key(iv: dict) -> str:
    if iv.get("start") and iv.get("end"):
        return f"{iv['start']}-{iv['end']}"
    return f"ax{iv.get('i', 0)}-ax{iv.get('i', 0) + 1}"


def axis_grid_from_networks(networks: list) -> dict:
    """axis_networks[] → 按 sheet 的 V/H 轴格区间索引。

    result[sheet_key] = {"V": [..], "H": [..]}；
    区间 = {"lo","hi","start","end","i","sheet","type"}（开间 = 相邻轴 pos 闭区间）。
    """
    out: dict[str, dict[str, list]] = {}
    for net in networks or []:
        direction = str(net.get("direction") or "").upper()
        if direction not in ("V", "H"):
            continue
        pos_label: list[tuple[float, str]] = []
        for a in net.get("axes") or []:
            try:
                p = float(a.get("pos"))
            except (TypeError, ValueError, AttributeError):
                continue
            pos_label.append((p, str(a.get("label") or a.get("axis_id") or "")))
        grid = net.get("grid")
        if not pos_label and isinstance(grid, dict) and grid.get("positions"):
            pos_label = [(float(p), f"ax{i}") for i, p in enumerate(grid.get("positions"))]
        pos_label.sort(key=lambda t: t[0])
        if len(pos_label) < 2:
            continue
        ivals = []
        for i in range(len(pos_label) - 1):
            ivals.append({
                "lo": pos_label[i][0], "hi": pos_label[i + 1][0],
                "start": pos_label[i][1], "end": pos_label[i + 1][1],
                "i": i, "sheet": net.get("sheet"),
                "type": net.get("axis_type", "?"),
            })
        out.setdefault(str(net.get("sheet")), {})[direction] = ivals
    return out


def _bbox_overlap(iv: dict, lo: float, hi: float) -> bool:
    return iv["lo"] <= hi and iv["hi"] >= lo


def axis_cells_for_bbox(bbox, grid) -> dict | None:
    """构件 bbox → 罩住的轴格区间。

      returns {"v": set(interval_keys), "h": set(interval_keys),
               "cells": set("Vkey/Hkey"), "partial": bool, "usable": bool}
      全格 = 同时落入 V 与 H 区间；只命中一个方向则 partial。
    """
    if not grid or not (grid.get("V") or grid.get("H")):
        return None
    x0, y0, x1, y1 = (float(v) for v in (bbox or [0, 0, 0, 0]))
    v = {_interval_key(iv) for iv in grid.get("V", []) if _bbox_overlap(iv, x0, x1)}
    h = {_interval_key(iv) for iv in grid.get("H", []) if _bbox_overlap(iv, y0, y1)}
    has_v = bool(grid.get("V"))
    has_h = bool(grid.get("H"))
    cells: set[str] = set()
    if v and h:
        cells = {f"{vk}/{hk}" for vk in v for hk in h}
    elif v or h:
        cells = set(v or h)
    partial = (has_v != has_h) or (has_v and has_h and not (v and h))
    return {"v": v, "h": h, "cells": cells,
            "partial": partial, "usable": bool(cells)}


def same_axis_cells(a: dict | None, b: dict | None) -> tuple[bool, str]:
    """两侧构件轴格交集判定（主判据：同格不同专业 → 候选）。

    坐标仅作佐证；轴号/区间标签跨图可直接配对。
    返回 (same, detail)；detail 用于报告与降级说明。
    """
    if not a or not b or not a["usable"] or not b["usable"]:
        return False, "no-axis-cells"
    inter = a["cells"] & b["cells"]
    if inter:
        return True, "cell:" + sorted(inter)[0]
    if a["partial"] or b["partial"]:
        av = a.get("v") or set()
        bv = b.get("v") or set()
        ah = a.get("h") or set()
        bh = b.get("h") or set()
        if av and bv and (av & bv):
            return True, "partial-v:" + sorted(av & bv)[0]
        if ah and bh and (ah & bh):
            return True, "partial-h:" + sorted(ah & bh)[0]
        return False, "partial-no-overlap"
    return False, "different-cell"


def _same_source(ma: dict, mb: dict) -> bool:
    """坐标佐证仅用于同源（同文件/同图）：跨图坐标不主判。

    只比 project（识图产物 source_file 派生名）；source_text 是 sheet/图层说明，
    可能跨图相同，不能作为同源证据。
    """
    pa = str(ma.get("project") or ma.get("source") or "")
    pb = str(mb.get("project") or mb.get("source") or "")
    return bool(pa) and pa == pb


def scan_clashes_axis(members_a: list[dict], members_b: list[dict],
                      grid_a: dict, grid_b: dict,
                      tol: float, max_items: int = MAX_CLASH_ITEMS):
    """轴格主判碰撞扫描：bbox→轴格区间；同格不同专业→候选；坐标降为佐证。

    若任一 side 无可用轴格，调用方应退回 scan_clashes 并标 axis_missing=degraded。
    返回 (counts, items, meta)。
    """
    cells_a = [axis_cells_for_bbox(m["bbox"], _axis_grid_for_sheet(grid_a, m.get("sheet")))
               for m in members_a]
    cells_b = [axis_cells_for_bbox(m["bbox"], _axis_grid_for_sheet(grid_b, m.get("sheet")))
               for m in members_b]
    counts = {"dup": 0, "line_line": 0, "candidate": 0, "axis_candidate": 0}
    items: list[dict] = []
    meta = {"mode": "axis-grid", "grid_a_sheets": list(grid_a.keys()),
            "grid_b_sheets": list(grid_b.keys()),
            "cells_a": sum(1 for c in cells_a if c and c["usable"]),
            "cells_b": sum(1 for c in cells_b if c and c["usable"]),
            "outside_grid_a": sum(1 for c in cells_a if c is not None and not c["usable"]),
            "outside_grid_b": sum(1 for c in cells_b if c is not None and not c["usable"])}
    for ia, ma in enumerate(members_a):
        for jb, mb in enumerate(members_b):
            yes, detail = same_axis_cells(cells_a[ia], cells_b[jb])
            if not yes:
                continue
            # 坐标佐证：同源才用于去噪；跨图坐标不主判
            if _same_source(ma, mb) and box_gap(ma["bbox"], mb["bbox"]) > tol:
                continue
            if _same_identity(ma, mb):
                counts["dup"] += 1
            elif _is_line_kind(ma) and _is_line_kind(mb):
                counts["line_line"] += 1
            else:
                counts["candidate"] += 1
                counts["axis_candidate"] += 1
                if len(items) < max_items:
                    ax = (ma["bbox"][0] + ma["bbox"][2]) / 2
                    ay = (ma["bbox"][1] + ma["bbox"][3]) / 2
                    ca = cells_a[ia] or {"cells": set()}
                    cb = cells_b[jb] or {"cells": set()}
                    item = {"a": ma["name"], "b": mb["name"],
                            "a_attrs": ma["attrs"], "b_attrs": mb["attrs"],
                            "a_src": ma["source_text"], "b_src": mb["source_text"],
                            "x": round(ax, 1), "y": round(ay, 1),
                            "gap": round(box_gap(ma["bbox"], mb["bbox"]), 1),
                            "axis_mode": "axis-grid", "axis_match": detail,
                            "a_axis_cell": sorted(ca["cells"])[0],
                            "b_axis_cell": sorted(cb["cells"])[0]}
                    item.update(_member_fields(ma))
                    for k in ("a_sheet", "a_floor", "a_axis", "a_coord",
                              "a_type", "a_kind", "a_src"):
                        item["b_" + k[2:]] = _member_fields(mb)[k]
                    items.append(item)
    return counts, items, meta


def _same_identity(ma: dict, mb: dict) -> bool:
    """两侧构件是否「同一个东西画了两遍」：同名，或同系统（类别太泛不作依据）。"""
    if ma["name"] and ma["name"] == mb["name"]:
        return True
    sa = ma["attrs"].get("系统") or ""
    sb = mb["attrs"].get("系统") or ""
    return bool(sa and sa == sb)


def _member_fields(m: dict) -> dict:
    """统一报告字段：sheet/floor/axis/坐标/类型/来源。"""
    bb = m.get("bbox") or [0, 0, 0, 0]
    return {
        "a_sheet": m.get("sheet"), "a_floor": m.get("floor", ""),
        "a_axis": m.get("grid", ""), "a_coord": [round(bb[0], 1), round(bb[1], 1)],
        "a_type": m.get("category", ""), "a_kind": m.get("kind", ""),
        "a_src": m.get("source_text", ""),
    }


def scan_clashes(members_a: list[dict], members_b: list[dict],
                 tol: float, max_items: int = MAX_CLASH_ITEMS) -> tuple[dict, list[dict]]:
    """全量分类计数（不截断）+ 明细前 max_items 项。

    分类口径：dup（同系统/同名同位——重复表达或真打架，2D 无标高不可判）/
    line_line（线×线平面交叉——正常关系）/ candidate（实体×实体、实体×线）。
    """
    cell = max(tol, 1.0)
    idx_b: dict[tuple[int, int], list[int]] = {}
    for j, mb in enumerate(members_b):
        for c in _cells(mb["bbox"], cell):
            idx_b.setdefault(c, []).append(j)
    counts = {"dup": 0, "line_line": 0, "candidate": 0}
    items: list[dict] = []
    for ia, ma in enumerate(members_a):
        seen: set[int] = set()
        for c in _cells(ma["bbox"], cell):
            for jb in idx_b.get(c, ()):
                if jb in seen:
                    continue
                seen.add(jb)
                mb = members_b[jb]
                if box_gap(ma["bbox"], mb["bbox"]) > tol:
                    continue
                if _same_identity(ma, mb):
                    counts["dup"] += 1
                elif _is_line_kind(ma) and _is_line_kind(mb):
                    counts["line_line"] += 1
                else:
                    counts["candidate"] += 1
                    if len(items) < max_items:
                        ax = (ma["bbox"][0] + ma["bbox"][2]) / 2
                        ay = (ma["bbox"][1] + ma["bbox"][3]) / 2
                        item = {"a": ma["name"], "b": mb["name"],
                                "a_attrs": ma["attrs"], "b_attrs": mb["attrs"],
                                "a_src": ma["source_text"], "b_src": mb["source_text"],
                                "x": round(ax, 1), "y": round(ay, 1),
                                "gap": round(box_gap(ma["bbox"], mb["bbox"]), 1)}
                        item.update(_member_fields(ma))
                        for k in ("a_sheet", "a_floor", "a_axis", "a_coord",
                                  "a_type", "a_kind", "a_src"):
                            item["b_" + k[2:]] = _member_fields(mb)[k]
                        items.append(item)
    return counts, items


def spatial_clash(members_a: list[dict], members_b: list[dict],
                  tol: float) -> list[dict]:
    """不同专业构件的空间碰撞候选（bbox 间隙 ≤ tol）。"""
    cell = max(tol, 1.0)
    idx_b: dict[tuple[int, int], list[int]] = {}
    for j, mb in enumerate(members_b):
        for c in _cells(mb["bbox"], cell):
            idx_b.setdefault(c, []).append(j)
    out: list[dict] = []
    for ia, ma in enumerate(members_a):
        seen: set[int] = set()
        for c in _cells(ma["bbox"], cell):
            for jb in idx_b.get(c, ()):
                if jb in seen:
                    continue
                seen.add(jb)
                mb = members_b[jb]
                gap = box_gap(ma["bbox"], mb["bbox"])
                if gap <= tol:
                    ax = (ma["bbox"][0] + ma["bbox"][2]) / 2
                    ay = (ma["bbox"][1] + ma["bbox"][3]) / 2
                    item = {"a": ma["name"], "b": mb["name"],
                            "a_attrs": ma["attrs"], "b_attrs": mb["attrs"],
                            "a_src": ma["source_text"], "b_src": mb["source_text"],
                            "a_grid": ma["grid"], "b_grid": mb["grid"],
                            "x": round(ax, 1), "y": round(ay, 1),
                            "gap": round(gap, 1), "_ia": ia, "_jb": jb}
                    item.update(_member_fields(ma))
                    for k in ("sheet", "floor", "axis", "coord", "type", "kind", "src"):
                        item["b_" + k] = _member_fields(mb)["a_" + k]
                    out.append(item)
                    if len(out) >= MAX_CLASH_ITEMS:
                        return out
    return out


def group_clashes(clashes: list[dict], bucket: float = GROUP_BUCKET) -> list[dict]:
    """碰撞点按位置桶分组：同一处打架（一根管穿一排构件）归一条，便于人工复核。"""
    groups: dict[tuple[int, int], dict] = {}
    for c in clashes:
        key = (int(c["x"] // bucket), int(c["y"] // bucket))
        g = groups.setdefault(key, {"x": c["x"], "y": c["y"], "count": 0,
                                    "a_names": set(), "b_names": set(),
                                    "min_gap": c["gap"], "samples": [],
                                    "a_axis": set(), "b_axis": set(),
                                    "a_floor": set(), "b_floor": set(),
                                    "a_type": set(), "b_type": set(),
                                    "a_sheet": set(), "b_sheet": set()})
        g["count"] += 1
        g["a_names"].add(c["a"])
        g["b_names"].add(c["b"])
        g["min_gap"] = min(g["min_gap"], c["gap"])
        g["a_axis"].add(str(c.get("a_axis", "")))
        g["b_axis"].add(str(c.get("b_axis", "")))
        g["a_floor"].add(str(c.get("a_floor", "")))
        g["b_floor"].add(str(c.get("b_floor", "")))
        g["a_type"].add(str(c.get("a_type", "")))
        g["b_type"].add(str(c.get("b_type", "")))
        g["a_sheet"].add(str(c.get("a_sheet", "")))
        g["b_sheet"].add(str(c.get("b_sheet", "")))
        if len(g["samples"]) < 5:
            g["samples"].append(c)
    out = sorted(groups.values(), key=lambda g: -g["count"])
    for g in out:
        g["a_names"] = sorted(g["a_names"])[:8]
        g["b_names"] = sorted(g["b_names"])[:8]
        g["a_axis"] = sorted({x for x in g["a_axis"] if x})[:4]
        g["b_axis"] = sorted({x for x in g["b_axis"] if x})[:4]
        g["a_floor"] = sorted({x for x in g["a_floor"] if x})[:4]
        g["b_floor"] = sorted({x for x in g["b_floor"] if x})[:4]
        g["a_type"] = sorted({x for x in g["a_type"] if x})[:4]
        g["b_type"] = sorted({x for x in g["b_type"] if x})[:4]
        g["a_sheet"] = sorted({x for x in g["a_sheet"] if x})[:4]
        g["b_sheet"] = sorted({x for x in g["b_sheet"] if x})[:4]
    return out


# ---------------------------------------------------------------- 清单加载
def load_members(detail_path: Path, spec: str) -> tuple[str, list[dict]]:
    """识图产物 → (来源名, members)。spec 决定 member_types。"""
    data = json.loads(detail_path.read_text(encoding="utf-8"))
    cfg = SPEC_PIPELINE[spec]
    types = cfg["types"]
    cl = clash_adapt.adapt(data, member_types=types)
    return cl["source"], cl["members"]


# ---------------------------------------------------------------- 识图子流程
def find_cfr() -> Path:
    """定位 cad-file-reader/scripts（显式依赖）。空字符串 env 也忽略。"""
    env_val = os.environ.get("CAD_FILE_READER_HOME", "").strip()
    env = Path(env_val) if env_val else None
    if env is not None and env.is_dir():
        return env
    for base in (Path.home() / ".workbuddy" / "skills",
                 Path.home() / ".codex" / "skills"):
        p = base / "cad-file-reader" / "scripts"
        if p.is_dir():
            return p
    raise FileNotFoundError("找不到 cad-file-reader/scripts；"
                            "请先安装 cad-file-reader 或设置 CAD_FILE_READER_HOME")


def build_detail(input_path: Path, workdir: Path, cfr: Path) -> Path:
    """DWG/DXF → 识图产物（cad_scan），返回 detail json 路径。"""
    workdir.mkdir(parents=True, exist_ok=True)
    stem = input_path.stem
    detail = workdir / f"{stem}.detail.json"
    r = subprocess.run(
        [sys.executable, str(cfr / "cad_scan.py"), str(input_path),
         "--detail-json", str(detail), "--with-geom", "--with-geom-layer",
         "--format", "json", "-o", str(workdir / f"{stem}_scan")],
        capture_output=True, text=True, timeout=1800)
    if r.returncode != 0 or not detail.exists():
        raise RuntimeError(f"识图失败 {input_path.name}: {r.stderr[-400:]}")
    return detail


def extract_specialty(detail: Path, spec: str, workdir: Path, cfr: Path) -> Path:
    """按专业跑几何提取器，返回带 *.structural/municipal/mep/building.json 的主产物。

    提取器输出命名 = {输入 stem}.{后缀}.json（如 X.detail.json → X.detail.mep.json）。
    """
    cfg = SPEC_PIPELINE[spec]
    if cfg["home"] == "local":
        script = Path(__file__).resolve().parent / cfg["script"]
    else:
        script = cfr / cfg["script"]
    geo_dir = workdir / f"{detail.stem}_geo"
    cmd = [sys.executable, str(script), str(detail), "--out-dir", str(geo_dir)]
    if spec == "建筑":
        cmd += ["--cfr", str(cfr)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    out = geo_dir / f"{detail.stem}.{cfg['suffix']}.json"
    tail = (r.stderr or "").strip()[-300:] or (r.stdout or "").strip()[-200:]
    if r.returncode != 0 or not out.exists():
        raise RuntimeError(f"{spec}几何提取失败 rc={r.returncode}: {tail}")
    return out


# ---------------------------------------------------------------- 洞口语义
def classify_opening_pairs(members_a: list[dict], members_b: list[dict],
                           tol: float) -> tuple[list[dict], list[dict]]:
    """建筑洞口与另一侧构件的关系（v0.2 洞口语义）。

    - MEP/实体 × opening（门窗洞口）：预留通道，expected，不计碰撞 → opening_pass
    - wall × opening：墙上门窗洞，正常关系 → wall_pass
    """
    opening_pass: list[dict] = []
    wall_pass: list[dict] = []
    for ma in members_a:
        for mb in members_b:
            if box_gap(ma["bbox"], mb["bbox"]) > tol:
                continue
            ka, kb = ma.get("kind"), mb.get("kind")
            if "opening" in (ka, kb):
                op = ma if ka == "opening" else mb
                other = mb if ka == "opening" else ma
                if other.get("kind") == "wall":
                    wall_pass.append({
                        "opening": op["name"], "wall": other["name"],
                        "opening_axis": op.get("grid", ""), "wall_axis": other.get("grid", ""),
                        "x": round((op["bbox"][0] + op["bbox"][2]) / 2, 1),
                        "y": round((op["bbox"][1] + op["bbox"][3]) / 2, 1),
                        "gap": round(box_gap(op["bbox"], other["bbox"]), 1),
                        "opening_sheet": op.get("sheet"), "wall_sheet": other.get("sheet"),
                    })
                elif other.get("kind") not in ("label", "opening"):
                    opening_pass.append({
                        "mep": other["name"], "opening": op["name"],
                        "mep_axis": other.get("grid", ""), "opening_axis": op.get("grid", ""),
                        "x": round((op["bbox"][0] + op["bbox"][2]) / 2, 1),
                        "y": round((op["bbox"][1] + op["bbox"][3]) / 2, 1),
                        "gap": round(box_gap(op["bbox"], other["bbox"]), 1),
                        "mep_sheet": other.get("sheet"), "opening_sheet": op.get("sheet"),
                        "mep_type": other.get("category", ""),
                    })
    return opening_pass, wall_pass


# ---------------------------------------------------------------- 报告
def compare_pair(a: dict, b: dict, place_tol: float | None) -> dict:
    """一对专业的结果：一致性（engine）+ 空间碰撞（分组）+ 洞口语义。"""
    eng = CrossEngine(place_tol=place_tol)
    ma = [Member(m["project"], m["floor"], m["grid"], m["name"], m["category"],
                 attrs=m["attrs"], source=m["source_text"], bbox=m["bbox"])
          for m in a["members"]]
    mb = [Member(m["project"], m["floor"], m["grid"], m["name"], m["category"],
                 attrs=m["attrs"], source=m["source_text"], bbox=m["bbox"])
          for m in b["members"]]
    res = eng.compare(ma, mb, side_a=a["spec"], side_b=b["spec"])
    cross = a["spec"] != b["spec"]
    items = [it for it in res.items
             if it["severity"] == "conflict"
             or (not cross and it["severity"] == "warn")]
    cnt = {"pass": 0, "warn": 0, "conflict": 0}
    for it in items:
        cnt[it["severity"]] += 1
    consistency = res.to_json()
    consistency["counts"] = cnt  # 按过滤后 items 重算，口径一致
    consistency["items"] = items

    # 洞口语义：洞口 = 预留通道/正常关系，不进碰撞候选
    opening_pass, wall_pass = classify_opening_pairs(
        a["members"], b["members"], a["clash_tol"])
    skip_kind = ("label", "opening")
    ca = [m for m in a["members"] if m.get("kind") not in skip_kind]
    cb = [m for m in b["members"] if m.get("kind") not in skip_kind]
    grid_a = a.get("axis_grid") or {}
    grid_b = b.get("axis_grid") or {}
    if grid_a and grid_b:
        counts, clashes, axmeta = scan_clashes_axis(
            ca, cb, grid_a, grid_b, a["clash_tol"])
        axis_mode, axis_missing = "axis-grid", False
    else:
        counts, clashes = scan_clashes(ca, cb, a["clash_tol"])
        axmeta = {"mode": "coordinate-fallback", "reason":
                  "一侧或两侧无可用轴格，退回 v0.2 坐标判定"}
        axis_mode, axis_missing = "coordinate-fallback", True
    dup_items, line_line = counts["dup"], counts["line_line"]
    groups = group_clashes(clashes)
    return {"side_a": a["spec"], "side_b": b["spec"],
            "source_a": a["source"], "source_b": b["source"],
            "cross_specialty": cross, "consistency": consistency,
            "opening_pass": len(opening_pass), "wall_pass": len(wall_pass),
            "opening_pass_samples": opening_pass[:10],
            "wall_pass_samples": wall_pass[:10],
            "dup_pairs": dup_items, "line_line_pairs": line_line,
            "labels_excluded": (len(a["members"]) - len(ca)
                                + len(b["members"]) - len(cb)),
            "axis_mode": axis_mode, "axis_missing": axis_missing,
            "axis_status_a": a.get("axis_status", "missing"),
            "axis_status_b": b.get("axis_status", "missing"),
            "axis_meta": axmeta,
            "clash_total": len(clashes), "clash_groups": groups,
            "clash_samples": clashes[:200]}


def _is_line_kind(m: dict) -> bool:
    """线段类构件（管线/道路线），区别于井/池/墙等实体。"""
    return m.get("kind") == "line" or str(m.get("category") or "").endswith("_geometry")


def to_md(report: dict) -> str:
    lines = ["# 跨专业碰撞校对报告", "",
             "> 2D 图面重叠/冲突**候选**提示（非 BIM 碰撞检测）；碰撞=不同专业构件"
             "在图面同位出现，须人工复核。final_quantity=false，图纸数据只落本机。", ""]
    lines.append(f"- schema：{report.get('schema', STATE_SCHEMA)}；state_v2="
                 + str(report.get("state_v2", True)) + "（旧 0.1.x 产物不冒充 pass）")
    lines.append(f"- 输入 {len(report['inputs'])} 份："
                 + "；".join(f"{i['file']}→{i['spec']}"
                             + (f"（{i['members']}构件）" if i.get("members") else "（未出清单）")
                             for i in report["inputs"]))
    for skipped in report.get("skipped", []):
        lines.append(f"- ⚠️ 跳过 {skipped['file']}：{skipped['reason']}")
    lines.append("")
    for pr in report["pairs"]:
        c = pr["consistency"]["counts"]
        lines.append(f"## {pr['side_a']}（{pr['source_a']}） × {pr['side_b']}（{pr['source_b']}）")
        lines.append("")
        lines.append(f"- **碰撞候选 {pr['clash_total']} 处**，归并为 {len(pr['clash_groups'])} 组位置"
                     + (f"（已剔除跨图重复表达 {pr.get('dup_pairs', 0)} 对）"
                        if pr.get("dup_pairs") else "")
                     + (f"（线×线平面交叉 {pr.get('line_line_pairs', 0)} 对——2D 无标高不可判，不计候选）"
                        if pr.get("line_line_pairs") else "")
                     + ("（同位置多构件已合并）" if pr["clash_total"] > len(pr["clash_groups"]) else ""))
        if pr.get("axis_mode") == "axis-grid":
            lines.append(f"- 判定模式：**轴格主判**（bbox→轴格区间，坐标降为佐证）；"
                         f"轴网 {pr.get('axis_status_a', '-')}/{pr.get('axis_status_b', '-')}"
                         + (f"，跨图坐标不主判（轴号配对 {pr.get('axis_meta', {}).get('mode')}）"
                            if pr.get('axis_meta', {}).get('mode') == 'axis-grid' else ''))
        elif pr.get("axis_missing"):
            lines.append("- **轴网缺失**：退回 v0.2 坐标判定，axis_missing=degraded（如实用态不冒充 pass）")
        if pr.get("opening_pass") or pr.get("wall_pass"):
            lines.append(f"- **洞口语义**：预留通道 {pr.get('opening_pass', 0)} "
                         f"/ 墙上门窗洞 {pr.get('wall_pass', 0)}（正常关系，不构成碰撞）")
        lines.append(f"- 一致性：pass {c['pass']} / warn {c['warn']} / conflict {c['conflict']}"
                     + ("（跨专业对只保留 conflict，占位差不算冲突）" if pr["cross_specialty"] else ""))
        if pr["clash_groups"]:
            lines.append("")
            lines.append("### 打架位置（按构件对数排序，取前 %d 组）" % MAX_MD_ITEMS)
            lines.append("")
            lines.append("| 位置 | A/B轴 | A/B层 | A/B类型 | 对数 | 最近间隙 | A侧构件 | B侧构件 |")
            lines.append("|---|---|---|---|---|---|---|---|")
            for g in pr["clash_groups"][:MAX_MD_ITEMS]:
                lines.append(
                    f"| ({g['x']:.0f}, {g['y']:.0f}) "
                    f"| {','.join(g.get('a_axis', [])[:2]) or '-'}/{','.join(g.get('b_axis', [])[:2]) or '-'} "
                    f"| {','.join(g.get('a_floor', [])[:2]) or '-'}/{','.join(g.get('b_floor', [])[:2]) or '-'} "
                    f"| {','.join(g.get('a_type', [])[:2]) or '-'}/{','.join(g.get('b_type', [])[:2]) or '-'} "
                    f"| {g['count']} | {g['min_gap']:.0f} "
                    f"| {', '.join(g['a_names'][:3]) or '-'} | {', '.join(g['b_names'][:3]) or '-'} |")
        if pr.get("clash_samples"):
            lines.append("")
            lines.append("### 候选明细（前 %d 条，sheet/坐标/类型已带）" % min(MAX_MD_ITEMS, len(pr["clash_samples"])))
            lines.append("")
            lines.append("| A构件 | B构件 | A位置(sheet/坐标) | B位置(sheet/坐标) | A类型/B类型 | 间隙 |")
            lines.append("|---|---|---|---|---|---|")
            for it in pr["clash_samples"][:MAX_MD_ITEMS]:
                lines.append(
                    f"| {it['a']} | {it['b']} "
                    f"| s{it.get('a_sheet')} ({it.get('a_coord', [0, 0])[0]:.0f},{it.get('a_coord', [0, 0])[1]:.0f}) "
                    f"| s{it.get('b_sheet')} ({it.get('b_coord', [0, 0])[0]:.0f},{it.get('b_coord', [0, 0])[1]:.0f}) "
                    f"| {it.get('a_type', '-')}/{it.get('b_type', '-')} | {it['gap']:.0f} |")
        items = [it for it in pr["consistency"]["items"] if it["severity"] == "conflict"]
        if items:
            lines.append("")
            lines.append(f"### 属性冲突（{len(items)} 条，展示前 {MAX_MD_ITEMS}）")
            lines.append("")
            for it in items[:MAX_MD_ITEMS]:
                lines.append(f"- **conflict** {it['key']}：{it['message']}")
        lines.append("")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- 施工计划模板
def build_construct_plan(report: dict) -> dict:
    """把碰撞候选整理成施工计划模板（= 图审/穿墙开洞/预留复核工作包草稿）。

    模板是「起始骨架」，不是正式施工计划：具体排期、责任人、施工顺序留空由项目经理填。
    """
    packages: list[dict] = []
    for pr in report.get("pairs", []):
        for i, g in enumerate(pr.get("clash_groups", [])[:200]):
            axes = list(dict.fromkeys(g.get("a_axis", []) + g.get("b_axis", [])))
            floors = list(dict.fromkeys(g.get("a_floor", []) + g.get("b_floor", [])))
            sheets = list(dict.fromkeys(g.get("a_sheet", []) + g.get("b_sheet", [])))
            packages.append({
                "work_package_id": f"{pr['side_a']}-{pr['side_b']}-{i+1:03d}",
                "title": f"{pr['side_a']} × {pr['side_b']} 图面同位区",
                "zone_axis": " / ".join(str(x) for x in axes),
                "floor": " / ".join(str(x) for x in floors),
                "sheet": " / ".join(str(x) for x in sheets),
                "count": g["count"],
                "min_gap": g["min_gap"],
                "coordinate": f"({g['x']:.0f}, {g['y']:.0f})",
                "side_a_types": g.get("a_type", []),
                "side_b_types": g.get("b_type", []),
                "task_type": "图审/穿墙开洞/预留孔洞复核",
                "priority": "高" if g["count"] >= 5 else ("中" if g["count"] >= 2 else "低"),
                "responsible": "", "due": "", "status": "open", "note": "施工计划模板草稿，请人工排期",
            })
    axes_hist = {}
    floors_hist = {}
    for s in packages:
        axes_hist[s["zone_axis"]] = axes_hist.get(s["zone_axis"], 0) + 1
        floors_hist[s["floor"]] = floors_hist.get(s["floor"], 0) + 1
    return {
        "schema": "cad-clash-construct-plan/v1", "final_quantity": False,
        "template": True,
        "boundary": "施工计划模板（起始骨架）：pending 分裂的计划项需工程例会定责任人/排期/验收；不作为正式施工依据。",
        "summary": {
            "packages": len(packages),
            "candidate_total": sum(p["clash_total"] for p in report.get("pairs", [])),
            "zone_axis": axes_hist, "floor": floors_hist,
        },
        "packages": packages,
        "opening_semantics": [{
            "preview_pass": sum(p.get("opening_pass", 0) for p in report.get("pairs", [])),
            "wall_pass": sum(p.get("wall_pass", 0) for p in report.get("pairs", [])),
        }],
    }


# ---------------------------------------------------------------- 主流程
def main() -> int:
    ap = argparse.ArgumentParser(
        description="跨专业碰撞校对一条龙：图纸进 → 碰撞/冲突标记出"
                    "（2D 候选提示，非 BIM 碰撞检测；final_quantity=false）")
    ap.add_argument("inputs", nargs="+",
                    help="DWG/DXF 图纸 或 识图产物 JSON（structural/municipal/mep/building）")
    ap.add_argument("-o", "--out-prefix", required=True, help="输出前缀（写 .json 与 .md）")
    ap.add_argument("--workdir", default=None, help="识图中间产物目录（默认 <out-prefix>_work）")
    ap.add_argument("--clash-tol", type=float, default=DEFAULT_CLASH_TOL,
                    help="空间碰撞距离上限，图面单位（默认 800）")
    ap.add_argument("--place-tol", type=float, default=None,
                    help="一致性位置核对容差（默认引擎内置 5000）")
    ap.add_argument("--state-file", default=None,
                    help="v0.2 状态文件路径（默认 <out-prefix>_work/state-v2.json）")
    args = ap.parse_args()

    cfr = find_cfr()
    workdir = Path(args.workdir or f"{args.out_prefix}_work")
    workdir.mkdir(parents=True, exist_ok=True)
    sides: list[dict] = []
    skipped: list[dict] = []
    input_metas: list[dict] = []

    for i, raw in enumerate(args.inputs, 1):
        p = Path(raw)
        if not p.exists():
            skipped.append({"file": p.name, "reason": "文件不存在"})
            continue
        try:
            if p.suffix.lower() in (".dwg", ".dxf"):
                detail = build_detail(p, workdir, cfr)
            else:
                detail = p
            data = json.loads(detail.read_text(encoding="utf-8"))
            spec = classify_detail(data)
            meta = {"file": p.name, "spec": spec}
            if spec not in SPEC_PIPELINE:
                skipped.append({"file": p.name,
                                "reason": f"专业判定为「{spec}」，暂无对应几何提取器"
                                          "（当前支持：结构/建筑/市政/MEP(电气/暖通/给排水)）"})
                input_metas.append(meta | {"members": 0})
                continue
            detail2 = detail
            if p.suffix.lower() in (".dwg", ".dxf"):
                detail2 = extract_specialty(detail, spec, workdir, cfr)
            src, members = load_members(detail2, spec)
            axis_nets, axis_summary = _axis_networks_from_data(data, cfr)
            sides.append({"spec": spec, "source": src, "members": members,
                          "clash_tol": args.clash_tol,
                          "axis_networks": axis_nets,
                          "axis_summary": axis_summary,
                          "axis_status": axis_summary.get("status", "missing"),
                          "axis_grid": axis_grid_from_networks(axis_nets)})
            meta.update({"members": len(members),
                         "kinds": _count_kinds(members),
                         "axis_status": axis_summary.get("status", "missing"),
                         "axis_networks": len(axis_nets),
                         "axis_usable": axis_summary.get("usable", 0),
                         "axis_degraded": axis_summary.get("degraded", 0)})
            input_metas.append(meta)
            print(f"[{i}/{len(args.inputs)}] {p.name} → 专业={spec}，{len(members)} 构件")
        except Exception as exc:  # 单张失败不拖垮整体
            skipped.append({"file": p.name, "reason": str(exc)[:300]})
            print(f"[{i}/{len(args.inputs)}] {p.name} 失败：{exc}", file=sys.stderr)

    pairs = []
    for i in range(len(sides)):
        for j in range(i + 1, len(sides)):
            pairs.append(compare_pair(sides[i], sides[j], args.place_tol))
            print(f"  {sides[i]['spec']} × {sides[j]['spec']}: "
                  f"碰撞候选 {pairs[-1]['clash_total']} / "
                  f"conflict {pairs[-1]['consistency']['counts']['conflict']}")

    report = {"schema": STATE_SCHEMA, "state_v2": True,
              "final_quantity": False,
              "old_flow_invalidated": True,
              "boundary": "2D 图面重叠/冲突候选提示，非 BIM 碰撞检测；"
                          "碰撞位置须人工复核，不是盖章结论。v0.3 轴格主判·坐标佐证；"
                          "无轴网自动降级 v0.2 坐标判定并标 degraded；旧 0.1.x 产物作废。",
              "inputs": input_metas, "skipped": skipped, "pairs": pairs}
    out = Path(args.out_prefix)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    out.with_suffix(".md").write_text(to_md(report), encoding="utf-8")

    plan = build_construct_plan(report)
    plan_out = out.with_name(out.name + "_construct_plan.json")
    plan_out.write_text(json.dumps(plan, ensure_ascii=False, indent=1, default=str),
                        encoding="utf-8")
    plan_md = "\n".join([
        "# 施工计划模板（clash v0.2）", "",
        "> 起始骨架：pending 工作包需工程例会定责任人/排期/验收；不作为正式施工依据。",
        "",
        f"- 工作包 {plan['summary']['packages']} 个；碰撞候选取自同一次 v0.2 报告。",
        "",
        "| 包号 | 标题 | 坐标 | 轴 | 层 | 类型A/B | 数量 | 优先级 |",
        "|---|---|---|---|---|---|---|---|",
        *[f"| {p['work_package_id']} | {p['title']} | {p['coordinate']} "
          f"| {p['zone_axis'] or '-'} | {p.get('floor') or '-'} "
          f"| {','.join(p['side_a_types']) or '-'}/{','.join(p['side_b_types']) or '-'} "
          f"| {p['count']} | {p['priority']} |" for p in plan["packages"][:100]],
        "",
    ])
    plan_md_out = out.with_name(out.name + "_construct_plan.md")
    plan_md_out.write_text(plan_md, encoding="utf-8")

    state = {"schema": STATE_SCHEMA, "version": "0.3.0", "status": "done",
             "old_flow_invalidated": True,
             "features": [
                 "SPEC_PIPELINE 含 MEP（电气/暖通/给排水）与 building（建筑墙/洞口）入口",
                 "报告字段带 sheet/floor/axis/专业A/B坐标/类型",
                 "洞口语义（预留通道/墙上门窗洞不计碰撞；穿墙无洞进候选）",
                 "axis_networks 轴格主判：bbox→轴格区间，坐标降为佐证",
                 "轴网缺失自动降级 v0.2 坐标判定并标 axis_missing=degraded",
                 "单元测试与施工计划模板",
                 "识图器未产墙/洞口时如实 degraded",
             ],
             "acceptance": [], "tests": []}
    state_path = Path(args.state_file or (workdir / STATE_FILE))
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")

    total = sum(p["clash_total"] for p in pairs)
    print(f"完成：{len(pairs)} 对专业组合，碰撞候选 {total} 处 → {out}.json / {out.with_suffix('.md')}")
    print(f"施工计划模板 → {plan_out} / {plan_md_out}")
    print(f"state-v2 → {state_path}")
    return 0


def _count_kinds(members: list[dict]) -> dict:
    from collections import Counter
    return dict(Counter(m.get("kind", "?") for m in members))


if __name__ == "__main__":
    raise SystemExit(main())
