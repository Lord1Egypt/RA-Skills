#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_security_radar.py — 由 8 维安全实测生成 security_results.json 与雷达 SVG
============================================================================
输出（tools/ 下）：
  - security_results.json      8 维评分数据（我们实测 vs 企业级标准 vs 行业基线）
  - security_radar.svg         8 轴雷达图（三系列对比）

用法：python gen_security_radar.py
依赖：credential_broker_security_test.run_security_checks
"""
import json
import os
import math

from credential_broker_security_test import run_security_checks

# 对比基线（行为级评分 0–5，仅作对照，不披露实现）
ENTERPRISE = [5, 5, 5, 4, 4, 5, 5, 4]   # 成熟商业凭据库典型档位
INDUSTRY = [3, 3, 3, 2, 3, 2, 3, 3]     # 自管/遗留脚本典型档位


def _axis_points(cx, cy, R, n, scores):
    pts = []
    for i, s in enumerate(scores):
        ang = -math.pi / 2 + 2 * math.pi * i / n
        r = R * (s / 5.0)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def _poly(points):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def build_svg(results):
    n = len(results)
    W, H = 680, 460
    cx, cy, R = 340, 230, 150
    labels = [d["dim"] for d in results]
    ours = [d["score"] for d in results]

    # 网格环
    rings = ""
    for k in range(1, 6):
        ring_scores = [k] * n
        p = _poly(_axis_points(cx, cy, R, n, ring_scores))
        rings += f'<polygon points="{p}" fill="none" stroke="#e2e8f0" stroke-width="1"/>'

    # 轴线 + 标签
    axes = ""
    for i, lab in enumerate(labels):
        ang = -math.pi / 2 + 2 * math.pi * i / n
        x2 = cx + R * math.cos(ang)
        y2 = cy + R * math.sin(ang)
        axes += f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#cbd5e1" stroke-width="1"/>'
        lx = cx + (R + 26) * math.cos(ang)
        ly = cy + (R + 26) * math.sin(ang)
        anchor = "middle"
        if math.cos(ang) > 0.3:
            anchor = "start"
        elif math.cos(ang) < -0.3:
            anchor = "end"
        axes += f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="10" fill="#33414f" text-anchor="{anchor}" dominant-baseline="middle">{lab}</text>'

    ours_p = _poly(_axis_points(cx, cy, R, n, ours))
    ent_p = _poly(_axis_points(cx, cy, R, n, ENTERPRISE))
    ind_p = _poly(_axis_points(cx, cy, R, n, INDUSTRY))

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="-apple-system,Segoe UI,Microsoft YaHei,sans-serif">
  <rect width="{W}" height="{H}" fill="#ffffff"/>
  <text x="24" y="28" font-size="15" font-weight="700" fill="#185FA5">统一凭据 Broker · 安全稳定性实测雷达（8 维）</text>
  <text x="24" y="46" font-size="10" fill="#5b6b7c">我们实测(红) vs 企业级标准(蓝) vs 行业基线(灰) · 零真实凭据本地闭环</text>
  {rings}
  {axes}
  <polygon points="{ind_p}" fill="rgba(148,163,184,0.18)" stroke="#94a3b8" stroke-width="1.2"/>
  <polygon points="{ent_p}" fill="rgba(59,130,246,0.15)" stroke="#3b82f6" stroke-width="1.2"/>
  <polygon points="{ours_p}" fill="rgba(220,38,38,0.22)" stroke="#dc2626" stroke-width="2"/>
  <g font-size="10" fill="#33414f">
    <rect x="430" y="400" width="12" height="12" fill="#dc2626"/><text x="448" y="410">我们实测 {ours[0]:.0f}–{max(ours):.0f}/5</text>
    <rect x="430" y="418" width="12" height="12" fill="#3b82f6"/><text x="448" y="428">企业级标准</text>
    <rect x="540" y="400" width="12" height="12" fill="#94a3b8"/><text x="558" y="410">行业基线</text>
  </g>
</svg>'''
    return svg


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    results = run_security_checks()
    ours = [d["score"] for d in results]

    data = {
        "title": "统一凭据 Broker 安全稳定性实测",
        "method": "本地闭环 · 零真实凭据 · 可重复",
        "overall": round(sum(ours) / len(ours), 2),
        "dimensions": [
            {
                "dim": d["dim"],
                "we_measured": d["score"],
                "enterprise_baseline": ENTERPRISE[i],
                "industry_baseline": INDUSTRY[i],
                "metric": d["metric"],
                "detail": d["detail"],
            }
            for i, d in enumerate(results)
        ],
    }
    with open(os.path.join(here, "security_results.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    svg = build_svg(results)
    with open(os.path.join(here, "security_radar.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print("已生成 security_results.json 与 security_radar.svg")
    print(f"综合分：{data['overall']:.2f} / 5.00")
    for d in data["dimensions"]:
        print(f"  {d['dim']:<8} 实测 {d['we_measured']:.1f} | 企业 {d['enterprise_baseline']} | 基线 {d['industry_baseline']}")


if __name__ == "__main__":
    main()
