#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_security_radar.py — 由 security_results.json 生成安全实测雷达图(SVG)

输出多维度雷达对比图：本工具实测 / 行业基线(参考) / 企业级标准(参考)。
用法：
  python tools/gen_security_radar.py                 # 写 references/panorama-security-radar.svg
  python tools/gen_security_radar.py --out out.svg   # 指定输出
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "security_results.json"
OUT = HERE.parent / "references" / "panorama-security-radar.svg"

# 参考基线（行业常见水平估计，仅用于对比展示，非实测）
BASELINE = {
    "抗暴力破解": 4.0, "防篡改审计": 3.5, "授权时效": 4.0, "抗重放": 3.5,
    "零知识边界": 3.0, "解绑完整性": 3.5, "并发稳定性": 4.0, "边界容错": 3.5,
}
ENTERPRISE = {
    "抗暴力破解": 4.5, "防篡改审计": 4.5, "授权时效": 4.5, "抗重放": 4.5,
    "零知识边界": 4.0, "解绑完整性": 4.5, "并发稳定性": 4.5, "边界容错": 4.0,
}


def _polar(cx, cy, r, ang):
    import math
    return (cx + r * math.cos(ang), cy + r * math.sin(ang))


def build(results: dict, out: Path):
    dims = results["dimensions"]
    n = len(dims)
    W, H = 680, 520
    cx, cy, R = 340, 270, 190
    import math
    step = 2 * math.pi / n

    # 网格圈
    grid = ""
    for lvl in range(1, 6):
        pts = []
        for i in range(n):
            x, y = _polar(cx, cy, R * lvl / 5, -math.pi / 2 + i * step)
            pts.append(f"{x:.1f},{y:.1f}")
        grid += f'<polygon points="{" ".join(pts)}" fill="none" stroke="#d0d7e2" stroke-width="1"/>'

    # 轴线 + 标签
    axes = ""
    labels = []
    for i, d in enumerate(dims):
        ang = -math.pi / 2 + i * step
        x, y = _polar(cx, cy, R, ang)
        axes += f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="#d0d7e2" stroke-width="1"/>'
        lx, ly = _polar(cx, cy, R + 26, ang)
        anchor = "middle"
        if lx < cx - 5:
            anchor = "end"
        elif lx > cx + 5:
            anchor = "start"
        labels.append(f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="13" fill="#1f2d3d" '
                      f'text-anchor="{anchor}" dominant-baseline="middle">{d["name"]}</text>')

    # 多边形
    def polygon(vals, color, fill, width, dash=""):
        pts = []
        for i, v in enumerate(vals):
            ang = -math.pi / 2 + i * step
            x, y = _polar(cx, cy, R * v / 5, ang)
            pts.append(f"{x:.1f},{y:.1f}")
        return (f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{color}" '
                f'stroke-width="{width}" {"stroke-dasharray=\""+dash+"\"" if dash else ""}/>')

    base_vals = [BASELINE.get(d["name"], 3.5) for d in dims]
    ent_vals = [ENTERPRISE.get(d["name"], 4.5) for d in dims]
    meas_vals = [d["score"] for d in dims]

    polys = polygon(base_vals, "#9aa7b8", "rgba(154,167,184,0.15)", 1.5, "5 4")
    polys += polygon(ent_vals, "#3b82f6", "rgba(59,130,246,0.12)", 1.5, "5 4")
    polys += polygon(meas_vals, "#16a34a", "rgba(22,163,74,0.28)", 2.5)

    overall = results.get("overall", 0)
    legend = (
        '<rect x="40" y="470" width="14" height="14" fill="rgba(22,163,74,0.5)" stroke="#16a34a"/>'
        '<text x="60" y="482" font-size="13" fill="#1f2d3d">本工具实测</text>'
        '<rect x="170" y="470" width="14" height="14" fill="rgba(59,130,246,0.25)" stroke="#3b82f6"/>'
        '<text x="190" y="482" font-size="13" fill="#1f2d3d">企业级标准(参考)</text>'
        '<rect x="340" y="470" width="14" height="14" fill="rgba(154,167,184,0.3)" stroke="#9aa7b8"/>'
        '<text x="360" y="482" font-size="13" fill="#1f2d3d">行业基线(参考)</text>'
    )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="-apple-system,Segoe UI,Roboto,Microsoft YaHei,sans-serif">
  <rect width="{W}" height="{H}" fill="#ffffff"/>
  <text x="{cx}" y="34" font-size="18" font-weight="700" fill="#111827" text-anchor="middle">统一凭据保险库 · 安全稳定性实测</text>
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
    if not RESULTS.exists():
        print("先跑 test_vault.py 生成 security_results.json", file=sys.stderr)
        return 1
    out = OUT if "--out" not in sys.argv else Path(sys.argv[sys.argv.index("--out") + 1])
    res = json.loads(RESULTS.read_text("utf-8"))
    p = build(res, out)
    print(f"✔ 雷达图已生成：{p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
