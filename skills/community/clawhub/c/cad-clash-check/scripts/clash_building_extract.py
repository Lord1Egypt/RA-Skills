#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""clash_building_extract.py —— 建筑（墙/洞口）识图产物合并器（cad-clash-check v0.2）。

输入：cad_scan 的 detail JSON（--with-geom --with-geom-layer）
处理：同时跑 cad-file-reader 的两个提取器：
  1. cad_structural_geometry.py    → wall 墙体几何（structural_geometry，category=wall）
  2. cad_deep_geometry.py --pack doors_windows_stairs_insulation_waterproof
                                   → door/window 洞口构件（components）
再合并为 clash 专用 building.json（members 含 wall/opening），
并从两者透传 grids 供轴号就近。若识图器没产出 wall/openings 会在
review 中如实标注，不当作 pass。
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], what: str, timeout: int = 1800) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(f"{what}失败 rc={r.returncode}: {(r.stderr or r.stdout or '')[-400:]}")


def main() -> int:
    ap = argparse.ArgumentParser(description="建筑墙/洞口识图产物合并")
    ap.add_argument("inputs", nargs="+", help="cad_scan detail JSON")
    ap.add_argument("--out-dir", default="建筑识图")
    ap.add_argument("--cfr", default="", help="cad-file-reader scripts 目录（缺省自动定位）")
    args = ap.parse_args()

    cfr = Path(args.cfr or "").resolve()
    if not cfr.is_dir():
        for base in (Path.home() / ".workbuddy" / "skills",
                     Path.home() / ".codex" / "skills"):
            p = base / "cad-file-reader" / "scripts"
            if p.is_dir():
                cfr = p
                break
        else:
            raise FileNotFoundError("找不到 cad-file-reader/scripts；请 --cfr 指定")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    outputs = []
    for src in args.inputs:
        src = Path(src)
        data = json.loads(src.read_text(encoding="utf-8"))
        tmp = out_dir / f"{src.stem}_buildup"
        tmp.mkdir(parents=True, exist_ok=True)

        # 1) 结构提取器 → walls
        run([sys.executable, str(cfr / "cad_structural_geometry.py"), str(src),
             "--out-dir", str(tmp)], "结构提取")
        struct_path = tmp / f"{src.stem}.structural.json"
        struct = json.loads(struct_path.read_text(encoding="utf-8")) if struct_path.exists() else {}

        # 2) 深化提取器（门窗） → openings
        run([sys.executable, str(cfr / "cad_deep_geometry.py"), str(src),
             "--pack", "doors_windows_stairs_insulation_waterproof",
             "--out-dir", str(tmp)], "门窗提取")
        dw_path = tmp / f"{src.stem}.doors_windows_stairs_insulation_waterproof.json"
        doorwin = json.loads(dw_path.read_text(encoding="utf-8")) if dw_path.exists() else {}

        walls = [g for g in (struct.get("structural_geometry") or [])
                 if str(g.get("category") or "") == "wall"]
        openings = [c for c in (doorwin.get("components") or [])
                    if str(c.get("category") or "") in ("door", "window")]
        grids = [g for g in (struct.get("grids") or doorwin.get("grids") or [])]

        review = []
        if not walls:
            review.append({"type": "wall", "reason": "识图器未产出墙体几何（结构层无 category=wall 线段），墙不可用，不带入碰撞实体", "evidence": []})
        else:
            review.append({"type": "wall", "reason": f"识别到墙体几何 {len(walls)} 段", "evidence": [{"count": len(walls)}]})
        if not openings:
            review.append({"type": "opening", "reason": "识图器未产出门窗洞口（deep geometry 无 door/window 构件），洞口不可用，MEP穿墙将退回无洞候选口径", "evidence": []})
        else:
            review.append({"type": "opening", "reason": f"识别到门窗洞口 {len(openings)} 个（含门/窗标注）", "evidence": [{"count": len(openings)}]})

        members = []
        # 墙体（线段几何）
        for it in walls:
            members.append({"type": "wall", "category": "wall", "system": "wall",
                            "name": "wall/" + (it.get("layer") or "wall").strip(),
                            "raw": (it.get("layer") or "wall"), "layer": it.get("layer"),
                            "file": it.get("file"), "sheet": it.get("sheet"),
                            "x": None, "y": None, "geometry": it.get("geometry"),
                            "floor": _floor_of(struct, it)})
        # 洞口（门窗文字构件 + 门窗几何段）
        for it in openings:
            members.append({"type": "opening", "category": it.get("category"),
                            "system": it.get("system") or it.get("category"),
                            "name": it.get("raw") or (str(it.get("category")) + "/opening"),
                            "raw": it.get("raw"), "layer": it.get("layer"),
                            "file": it.get("file"), "sheet": it.get("sheet"),
                            "x": it.get("x"), "y": it.get("y"),
                            "geometry": it.get("geometry"),
                            "floor": _floor_of(doorwin, it)})

        payload = {
            "schema": "cad-clash-building/v1",
            "source_file": src.name,
            "source_paths": data.get("source_paths") or [],
            "grids": grids,
            "members": members,
            "walls": walls,
            "openings": openings,
            "review": review,
            "boundary": "建筑墙/洞口的碰撞校对候选；识图器未产出的墙/洞口如实标注 degraded，不冒充 pass。",
        }
        jp = out_dir / f"{src.stem}.building.json"
        jp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        outputs.append(str(jp))
        print(json.dumps({"source": str(src), "walls": len(walls),
                          "openings": len(openings), "review": review, "outputs": outputs},
                         ensure_ascii=False))
    return 0


def _floor_of(container: dict, item: dict) -> str:
    for k in ("floor", "标高", "elevation", "level", "floor_name", "楼层"):
        v = item.get(k)
        if v:
            return str(v)
    # 从父级 drawing_types/systems 里找楼层线索（简化：优先 item）
    return ""


if __name__ == "__main__":
    raise SystemExit(main())
