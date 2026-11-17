#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_skill_security_radar.py — 由 security_results.json 生成安全稳定性实测雷达图(SVG)

通用版：标题 / 输出路径 / 基线均可参数化，适配任意 Skill（文档型 / 工具型 / 专家型）。
本地闭环、零网络、零真实凭据依赖。

用法：
  python gen_skill_security_radar.py --results security_results.json \
      --out security-radar.svg --title "内容发布全流程 · 安全稳定性实测"
"""
from __future__ import annotations
import json
import math
import sys
from pathlib import Path

BASELINE = 3.5      # 行业基线(参考估计)
ENTERPRISE = 4.5    # 企业级标准(参考估计)


def _polar(cx, cy, r, ang):
    return (cx + r * math.cos(ang), cy + r * math.sin(ang))


def build(results: dict, title: str, out: Path):
    dims = results["dimensions"]
    n = len(dims)
    W, H = 680, 540
    cx, cy, R = 340, 270, 190
    step = 2 * math.pi / n

    grid = ""
    for lvl in range(1, 6):
        pts = []
        for i in range(n):
            x, y = _polar(cx, cy, R * lvl / 5, -math.pi / 2 + i * step)
            pts.append(f"{x:.1f},{y:.1f}")
        grid += f'<polygon points="{" ".join(pts)}" fill="none" stroke="#d0d7e2" stroke-width="1"/>'

    axes = ""
    labels = []
    for i, d in enumerate(dims):
        ang = -math.pi / 2 + i * step
        x, y = _polar(cx, cy, R, ang)
        axes += f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="#d0d7e2" stroke-width="1"/>'
        lx, ly = _polar(cx, cy, R + 28, ang)
        anchor = "middle"
        if lx < cx - 5:
            anchor = "end"
        elif lx > cx + 5:
            anchor = "start"
        labels.append(f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="13" fill="#1f2d3d" '
                      f'text-anchor="{anchor}" dominant-baseline="middle">{d["name"]}</text>')

    def polygon(vals, color, fill, width, dash=""):
        pts = []
        for i, v in enumerate(vals):
            ang = -math.pi / 2 + i * step
            x, y = _polar(cx, cy, R * v / 5, ang)
            pts.append(f"{x:.1f},{y:.1f}")
        return (f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{color}" '
                f'stroke-width="{width}" {"stroke-dasharray=\""+dash+"\"" if dash else ""}/>')

    base_vals = [BASELINE for _ in dims]
    ent_vals = [ENTERPRISE for _ in dims]
    meas_vals = [d["score"] for d in dims]

    polys = polygon(base_vals, "#9aa7b8", "rgba(154,167,184,0.15)", 1.5, "5 4")
    polys += polygon(ent_vals, "#3b82f6", "rgba(59,130,246,0.12)", 1.5, "5 4")
    polys += polygon(meas_vals, "#16a34a", "rgba(22,163,74,0.28)", 2.5)

    overall = results.get("overall", 0)
    legend = (
        '<rect x="40" y="492" width="14" height="14" fill="rgba(22,163,74,0.5)" stroke="#16a34a"/>'
        '<text x="60" y="504" font-size="13" fill="#1f2d3d">本工具实测</text>'
        '<rect x="190" y="492" width="14" height="14" fill="rgba(59,130,246,0.25)" stroke="#3b82f6"/>'
        '<text x="210" y="504" font-size="13" fill="#1f2d3d">企业级标准(参考)</text>'
        '<rect x="380" y="492" width="14" height="14" fill="rgba(154,167,184,0.3)" stroke="#9aa7b8"/>'
        '<text x="400" y="504" font-size="13" fill="#1f2d3d">行业基线(参考)</text>'
    )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="-apple-system,Segoe UI,Roboto,Microsoft YaHei,sans-serif">
  <rect width="{W}" height="{H}" fill="#ffffff"/>
  <text x="{cx}" y="34" font-size="18" font-weight="700" fill="#111827" text-anchor="middle">{title}</text>
  <text x="{cx}" y="56" font-size="13" fill="#6b7280" text-anchor="middle">综合 {overall:.2f}/5 · 本地闭环 · 零真实凭据 · 可重跑</text>
  {grid}
  {axes}
  {polys}
  {"".join(labels)}
  {legend}
</svg>'''
    out.write_text(svg, "utf-8")
    return out


def main():
    args = sys.argv[1:]
    results_path = None
    out_path = Path("security-radar.svg")
    title = "Skill 安全稳定性实测"
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--results":
            results_path = Path(args[i + 1]); i += 2
        elif a == "--out":
            out_path = Path(args[i + 1]); i += 2
        elif a == "--title":
            title = args[i + 1]; i += 2
        else:
            i += 1
    if results_path is None or not results_path.exists():
        print("缺少 --results <security_results.json>", file=sys.stderr)
        return 1
    res = json.loads(results_path.read_text("utf-8"))
    p = build(res, title, out_path)
    print(f"✔ 雷达图已生成：{p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
