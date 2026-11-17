#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""clash_adapt.py —— 识图产物 → 碰撞校对清单适配器（自 cad-suite/cross/adapt.py 移植）。

与原版的差异：
  ① municipal_geometry 等带 geometry 线段 [x0,y0,x1,y1] 的条目，
     bbox 直接取线段两端（原版按点 x/y 处理会丢线段）；
  ② 其余逻辑（就近轴号 / 坐标桶 / 属性透传）与 cad-suite 保持一致，
     两侧实现以 cad-suite 为准同步。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

DEFAULT_AXIS_TOL = 30000.0   # 轴号就近距离，图面单位
DEFAULT_BUCKET = 50000.0     # 坐标桶尺寸，图面单位


def _nearest_axis(x: float, y: float, sheet, axes: list[dict], tol: float) -> str:
    best, best_d = "", tol
    for a in axes:
        if sheet is not None and a.get("sheet") not in (sheet, None):
            continue
        try:
            ax, ay = float(a["x"]), float(a["y"])
        except (KeyError, TypeError, ValueError):
            continue
        d = ((x - ax) ** 2 + (y - ay) ** 2) ** 0.5
        if d <= best_d:
            best_d, best = d, str(a.get("value") or "")
    return best


def _bucket(x: float, y: float, size: float) -> str:
    return f"pos:x{int(x // size)}y{int(y // size)}"


def _floor_of(item: dict) -> str:
    for k in ("floor", "标高", "elevation", "level", "floor_name", "楼层"):
        if item.get(k):
            return str(item[k])
    return ""


def _kind_of(mtype: str, item: dict, name: str) -> str:
    """构件分类（v0.2）：洞口/墙/实体/线/标注。

    - opening：门窗洞口（建筑墙上的预留口）；
    - wall：墙体几何（结构/建筑整面层）；
    - entity：真几何实体（圆/块，bbox 为实体外接框）；
    - line：线段（管线/道路线/墙体线等几何段）；
    - label：图面文字标注（贴着被标注构件是正常图面行为）。
    """
    cat = str(item.get("category") or "")
    sys = str(item.get("system") or "")
    if cat in ("door", "window") or sys in ("door", "window"):
        return "opening"
    if cat == "wall":
        return "wall"
    if mtype in ("entities", "equipment", "risers"):
        return "entity"
    if mtype.endswith("_geometry"):
        return "line"
    return "label"


def _bbox_of(item: dict) -> tuple[float, float, float, float] | None:
    """bbox：优先 geometry 线段（保留两端），退化为点。"""
    g = item.get("geometry")
    if isinstance(g, (list, tuple)) and len(g) >= 4:
        try:
            x0, y0, x1, y1 = (float(g[0]), float(g[1]), float(g[2]), float(g[3]))
            return (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))
        except (TypeError, ValueError):
            pass
    try:
        x, y = float(item["x"]), float(item["y"])
        return (x, y, x, y)
    except (KeyError, TypeError, ValueError):
        return None


import re

# 说明句特征：图面「设计说明/施工要求」类文字不是构件标注。
# 保守组合（避免误杀短标注如「挡土墙」「电缆井（弱电用）」）：
# 长度>10 且含说明动词/施工术语。真图教训：一句「截水暗沟接小区雨水管网」
# 被 bbox 放大后罩住整片管网区，产生千级伪碰撞。
_NOTE_PAT = re.compile(r"见[:：]|做法|采用|覆土|详见|参照|接.+管网|深化")


def _is_annotation_text(name: str) -> bool:
    """长文本 + 说明特征 → 设计说明句，不进构件清单。"""
    if len(name) < 10:
        return False
    return bool(_NOTE_PAT.search(name))


def adapt(data: dict, project: str = "", member_types: list[str] | None = None,
          axis_tol: float = DEFAULT_AXIS_TOL,
          bucket: float = DEFAULT_BUCKET) -> dict:
    """识图产物 → {"source","members","relations"}。"""
    axes = [g for g in data.get("grids") or []
            if str(g.get("type")) == "axis" and g.get("value")]
    source = str(data.get("source_file") or data.get("source") or "")
    proj = project or source.rsplit(".", 1)[0]
    types = set(member_types or ["members", "components"])
    members: list[dict] = []
    for mtype in sorted(types):
        for it in data.get(mtype) or []:
            if not isinstance(it, dict):
                continue
            name = str(it.get("name") or it.get("raw") or "").strip()
            if mtype.endswith("_geometry") and not name:
                # 几何线段无标注名，用 系统/类别 构造（如 pipe/water_supply）
                name = str(it.get("system") or it.get("category") or mtype)
            if mtype == "entities" and not name:
                # 圆/块实体无文字名，用 类别+etype 构造（如 valve/circle）
                name = str(it.get("category") or "") + "/" + str(it.get("etype") or "entity")
            if not name:
                continue
            if mtype == "components" and _is_annotation_text(name):
                continue  # 设计说明句不是构件（真图教训：会产生大面积伪碰撞）
            bb = _bbox_of(it)
            if bb is None:
                continue
            sheet = it.get("sheet")
            grid = _nearest_axis(bb[0], bb[1], sheet, axes, axis_tol)
            if not grid:
                grid = _bucket(bb[0], bb[1], bucket)
            attrs = {}
            for k, out_k in (("system", "系统"), ("pipe_size", "管径"),
                             ("diameter", "管径"), ("category", "类别"),
                             ("material", "材质")):
                if it.get(k) and out_k not in attrs:
                    attrs[out_k] = str(it[k])
            members.append({
                "project": proj, "floor": _floor_of(it), "grid": grid,
                "name": name, "category": str(it.get("category") or mtype),
                "attrs": attrs,
                "bbox": list(bb),
                "sheet": sheet,
                "source_text": (f"sheet{sheet} " if sheet is not None else "")
                               + f"{it.get('layer', '')}",
                "kind": _kind_of(mtype, it, name),
            })
    return {"source": proj or source, "members": members, "relations": []}


def main() -> int:
    ap = argparse.ArgumentParser(description="识图产物 → 碰撞校对清单 JSON")
    ap.add_argument("inputs", nargs="+", help="识图产物 JSON（structural/municipal 等）")
    ap.add_argument("-o", "--out-prefix", required=True, help="输出前缀（多输入时写 <前缀>-1.json …）")
    ap.add_argument("--project", default="", help="项目名（缺省取源文件名）")
    ap.add_argument("--member-types", default="members,components",
                    help="要转的构件数组字段，逗号分隔（默认 members,components）")
    ap.add_argument("--axis-tol", type=float, default=DEFAULT_AXIS_TOL)
    ap.add_argument("--bucket", type=float, default=DEFAULT_BUCKET)
    args = ap.parse_args()

    types = [t.strip() for t in args.member_types.split(",") if t.strip()]
    for i, p in enumerate(args.inputs, 1):
        data = json.loads(Path(p).read_text(encoding="utf-8"))
        cl = adapt(data, args.project, types, args.axis_tol, args.bucket)
        out = Path(f"{args.out_prefix}-{i}.json") if len(args.inputs) > 1 else Path(f"{args.out_prefix}.json")
        out.write_text(json.dumps(cl, ensure_ascii=False, indent=1), encoding="utf-8")
        n_axis = sum(1 for m in cl["members"] if not m["grid"].startswith("pos:"))
        print(f"{p} → {out}：{len(cl['members'])} 构件（真轴号 {n_axis} / 坐标桶 {len(cl['members']) - n_axis}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
