#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""市政管长汇总：管道标注 × 图面线段长度。

输入是 cad-file-reader `cad_municipal_geometry` 的产物 `*.municipal.json`
（schema cad-municipal-geometry/v1）。识图层只给证据（管道标注、管径、
图层线段），长度在此按以下口径汇总：

  长度   三档证据——
           ① 显式长度：管道标注文本里 L=12345 / 长度 12345（置信高）
           ② 桩号差：同文本里 K0+240.5~K0+412.3（市政管道纵断面主口径）
           ③ 图面线段：管道图层的 geometry 段长合计（图面口径，
              不含井段扣减/弯曲增长，只作缺显式长度时的估算证据）
  归属   图面线段只有图层——按该图层管道标注的系统多数派归属，
           管径记「未标注」；显式长度直接挂所属标注的系统×管径。

输出为估算口径（图面长度，非施工下料长度），final_quantity=false，
不替代测量放线、清单编制与结算。

用法
  python3 municipal_pipe_length.py --municipal 市政识图/xxx.municipal.json --out-prefix 市政管长
"""
from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from io import StringIO
from pathlib import Path

SCHEMA = "cad-municipal-pipe-length/v0.1"

LEN_RE = re.compile(r"(?:L\s*[=＝:]|长度)\s*(\d{2,6})(?:\.\d+)?", re.I)
STAKE_RE = re.compile(r"K(\d+)\s*[+＋]\s*(\d{3}(?:\.\d+)?)")


def _f(v) -> float:
    try:
        x = float(v)
    except (TypeError, ValueError):
        return 0.0
    return x if x > 0 else 0.0


def norm_size(size: str) -> str:
    """管径归一键：DN300/De300/dn300 → DN300（保留原文另存）。"""
    m = re.match(r"(?:DN|De|D|d|Φ|φ)\s*(\d{2,4})", str(size or ""), re.I)
    return f"DN{m.group(1)}" if m else ""


def explicit_pipe_lengths(pipes: list[dict]) -> list[dict]:
    """从管道标注取显式长度与桩号差（m）。每条证据行最多计一次。"""
    out: list[dict] = []
    for p in pipes or []:
        system = str(p.get("system") or "未分类")
        size_raw = str(p.get("pipe_size") or "")
        size = norm_size(size_raw)
        for ev in p.get("evidence") or []:
            text = str(ev.get("text") or "")
            length_m = 0.0
            basis = ""
            hit = LEN_RE.search(text)
            if hit:
                mm = _f(hit.group(1))
                if 1 <= mm <= 100000:
                    length_m = mm / 1000.0 if mm > 200 else mm
                    basis = "L="
            if not length_m:
                stakes = STAKE_RE.findall(text)
                if len(stakes) >= 2:
                    (k1, m1), (k2, m2) = stakes[0], stakes[-1]
                    d = (int(k2) * 1000 + float(m2)) - (int(k1) * 1000 + float(m1))
                    if 0 < d <= 100000:
                        length_m = d
                        basis = "桩号差"
            if length_m > 0:
                out.append({"system": system, "pipe_size": size,
                            "pipe_size_raw": size_raw, "length_m": round(length_m, 1),
                            "basis": basis, "text": text[:80]})
    return out


def layer_system_majority(pipes: list[dict]) -> dict[str, str]:
    """管道图层 → 系统多数派（图面线段归属用）。"""
    votes: dict[str, Counter] = defaultdict(Counter)
    for p in pipes or []:
        layer = str(p.get("layer") or "")
        system = str(p.get("system") or "")
        if layer and system:
            votes[layer][system] += 1
    return {layer: c.most_common(1)[0][0] for layer, c in votes.items()}


def drawn_lengths(municipal: dict, layer_system: dict[str, str]) -> list[dict]:
    """市政管道图层 geometry 段长合计 → (system, size)。

    管径优先取识图层就近挂接的 diameter（cad_municipal_geometry 的
    attach_diameters），取不到记「未标注」。
    """
    out: list[dict] = []
    agg: dict[tuple[str, str], float] = defaultdict(float)
    for item in municipal.get("municipal_geometry") or []:
        if not isinstance(item, dict):
            continue
        layer = str(item.get("layer") or "")
        if layer not in layer_system:
            continue  # 非管道图层的线段不计
        geom = item.get("geometry")
        length = 0.0
        if isinstance(geom, dict):
            length = _f(geom.get("length") or geom.get("length_mm"))
        elif isinstance(geom, (list, tuple)) and len(geom) >= 4:
            x0, y0, x1, y1 = (_f(geom[0]), _f(geom[1]), _f(geom[2]), _f(geom[3]))
            length = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
        if length > 0:
            size = norm_size(item.get("diameter")) or "未标注"
            agg[(layer_system[layer], size)] += length / 1000.0
    for (system, size), length_m in agg.items():
        out.append({"system": system, "pipe_size": size, "pipe_size_raw": "",
                    "length_m": round(length_m, 1), "basis": "图面线段", "text": ""})
    return out


def build(municipal_path: str, out_prefix: str) -> Path:
    municipal = json.load(open(municipal_path, encoding="utf-8"))
    pipes = municipal.get("pipe_network") or []
    if not pipes:
        raise SystemExit("❌ municipal.json 里没有管道候选"
                         "（确认输入是 cad_municipal_geometry 的 *.municipal.json）")

    explicit = explicit_pipe_lengths(pipes)
    layer_system = layer_system_majority(pipes)
    drawn = drawn_lengths(municipal, layer_system)

    # 汇总：显式长度优先；系统已有显式长度时其图面线段整体跳过（防重复计数）
    agg: dict[tuple[str, str], dict] = {}
    for r in explicit:
        key = (r["system"], r["pipe_size"])
        rec = agg.setdefault(key, {"length_m": 0.0, "basis": set(),
                                   "raw_sizes": set(), "texts": []})
        rec["length_m"] += r["length_m"]
        rec["basis"].add(r["basis"])
        if r["pipe_size_raw"]:
            rec["raw_sizes"].add(r["pipe_size_raw"])
        if r["text"]:
            rec["texts"].append(r["text"])
    explicit_systems = {r["system"] for r in explicit}
    drawn_used = 0.0
    for r in drawn:
        if r["system"] in explicit_systems:
            continue  # 该系统已有显式长度，图面线段不叠加（防重复计数）
        key = (r["system"], r["pipe_size"])
        rec = agg.setdefault(key, {"length_m": 0.0, "basis": set(),
                                   "raw_sizes": set(), "texts": []})
        rec["length_m"] += r["length_m"]
        rec["basis"].add(r["basis"])
        drawn_used += r["length_m"]

    rows = []
    grand_total = 0.0
    for (system, size), rec in sorted(agg.items(),
                                      key=lambda kv: (-kv[1]["length_m"], kv[0][0])):
        grand_total += rec["length_m"]
        rows.append({
            "系统": system, "管径": size or "未标注",
            "原文管径": "、".join(sorted(rec["raw_sizes"])) or "-",
            "管长m": round(rec["length_m"], 1),
            "长度口径": "+".join(sorted(rec["basis"])),
        })

    out = {
        "schema": SCHEMA,
        "final_quantity": False,
        "rows": rows,
        "explicit_rows": explicit,
        "drawn_total_m": round(drawn_used, 1),
        "layer_system_map": layer_system,
        "summary": {
            "管道标注数": len(pipes),
            "显式长度条数": len(explicit),
            "图面线段计入m": round(drawn_used, 1),
            "总管长m": round(grand_total, 1),
            "系统数": len({r["系统"] for r in rows}),
        },
    }
    _render(out, Path(municipal_path).stem, out_prefix)
    return Path(str(out_prefix) + ".csv")


def _render(out: dict, title: str, out_prefix: str) -> None:
    out_base = Path(out_prefix)
    out_base.parent.mkdir(parents=True, exist_ok=True)
    Path(str(out_base) + ".json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    md = StringIO()
    s = out["summary"]
    md.write(f"# {title}（市政管长汇总）\n\n")
    md.write("> **口径声明**：估算口径（final_quantity=false）；长度来自标注显式值/桩号差/"
             "图面线段（不含井段扣减与弯曲增长），非施工下料长度；不替代测量放线、清单编制与结算。\n\n")
    md.write(f"- 管道标注 {s['管道标注数']} 条；显式长度 {s['显式长度条数']} 条；"
             f"图面线段计入 {s['图面线段计入m']} m\n")
    if s["总管长m"] > 0:
        md.write(f"- **总管长：{s['总管长m']} m**（{s['系统数']} 个系统）\n\n")
        md.write("## 按系统 × 管径\n\n| 系统 | 管径 | 原文管径 | 管长m | 长度口径 |\n|---|---|---|---|---|\n")
        for r in out["rows"]:
            md.write(f"| {r['系统']} | {r['管径']} | {r['原文管径']} | {r['管长m']} | {r['长度口径']} |\n")
        md.write("\n")
    else:
        md.write("- ⚠️ 管道标注里没有显式长度/桩号差，管道图层也没有几何线段：只有标注清单\n\n")
    if out["explicit_rows"]:
        md.write("## 显式长度明细\n\n| 系统 | 管径 | 长度m | 口径 | 原文 |\n|---|---|---|---|---|\n")
        for r in out["explicit_rows"][:60]:
            md.write(f"| {r['system']} | {r['pipe_size'] or '未标注'} | {r['length_m']} "
                     f"| {r['basis']} | {r['text']} |\n")
        if len(out["explicit_rows"]) > 60:
            md.write(f"\n（其余 {len(out['explicit_rows']) - 60} 条见 JSON）\n")
    Path(str(out_base) + ".md").write_text(md.getvalue(), encoding="utf-8")

    with Path(str(out_base) + ".csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["系统", "管径", "管长m", "长度口径"])
        if s["总管长m"] > 0:
            w.writerow(["合计", "", s["总管长m"], ""])
            for r in out["rows"]:
                w.writerow([r["系统"], r["管径"], r["管长m"], r["长度口径"]])
        else:
            w.writerow(["", "", "", "无长度证据，只有管道标注清单"])


def main() -> None:
    raw = sys.argv[1:]
    ap = argparse.ArgumentParser(
        description="Municipal pipe length summary from cad_municipal_geometry output")
    ap.add_argument("--municipal", required=True,
                    help="cad_municipal_geometry 产物 *.municipal.json")
    ap.add_argument("--out-prefix", required=True)
    a = ap.parse_args(raw)
    build(a.municipal, a.out_prefix)


if __name__ == "__main__":
    main()
