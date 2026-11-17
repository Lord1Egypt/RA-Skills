#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_security_radar.py — 从 security_results.json 生成多维度雷达对比图（自包含 SVG，无 CDN）
对比三条线：我们实测 / 行业基线 / 企业级标准。
输出：verify/security-radar.svg
"""

import json
import math
import os

VERIFY = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(VERIFY)

CX, CY = 340, 300
R = 195
N = 6
W, H = 680, 600

DIM_LABELS = [
    "法规时效性",
    "覆盖完整性",
    "模板可用性",
    "风险分级准确性",
    "结构规范性",
    "安全净度",
]

SERIES = [
    ("我们实测", "#e63f3f", None),
    ("行业基线", "#f5b942", "dash"),
    ("企业级标准", "#3d7bfd", None),
]


def point(i, value):
    ang = -math.pi / 2 + i * 2 * math.pi / N
    rr = R * value / 5.0
    return (CX + rr * math.cos(ang), CY + rr * math.sin(ang))


def polygon(pts):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def main():
    with open(os.path.join(VERIFY, "security_results.json"), encoding="utf-8") as f:
        data = json.load(f)
    ours = {d["key"]: d["score"] for d in data["dimensions"]}
    base = data["benchmarks"]["industry_baseline"]
    ent = data["benchmarks"]["enterprise_standard"]

    keys = [d["key"] for d in data["dimensions"]]

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Microsoft YaHei, PingFang SC, sans-serif">')
    svg.append(f'<rect width="{W}" height="{H}" fill="#fafafa"/>')

    # 网格（5 圈）
    for g in range(1, 6):
        pts = [point(i, g) for i in range(N)]
        color = "#d9d9d9" if g % 2 else "#ececec"
        svg.append(f'<polygon points="{polygon(pts)}" fill="{color}" stroke="#cccccc" stroke-width="0.8"/>')
    # 辐条
    for i in range(N):
        x1, y1 = point(i, 0)
        x2, y2 = point(i, 5)
        svg.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#cccccc" stroke-width="0.8"/>')

    # 维度标签
    for i, label in enumerate(DIM_LABELS):
        ang = -math.pi / 2 + i * 2 * math.pi / N
        lx = CX + (R + 34) * math.cos(ang)
        ly = CY + (R + 34) * math.sin(ang)
        anchor = "middle"
        if abs(math.cos(ang)) < 0.3:
            anchor = "middle"
        elif math.cos(ang) > 0:
            anchor = "start"
        else:
            anchor = "end"
        svg.append(f'<text x="{lx:.1f}" y="{ly:.1f}" fill="#222222" font-size="15" font-weight="bold" text-anchor="{anchor}" dominant-baseline="middle">{label}</text>')

    # 刻度值（0/1/2/3/4/5 标注在 12 点方向）
    for g in [1, 2, 3, 4, 5]:
        x, y = point(0, g)
        svg.append(f'<text x="{x+8:.1f}" y="{y+4:.1f}" fill="#999999" font-size="11" text-anchor="start">{g}</text>')

    # 数据系列
    for name, color, style in SERIES:
        values = ours if name == "我们实测" else (base if name == "行业基线" else ent)
        vals = [values[k] for k in keys]
        pts = [point(i, v) for i, v in enumerate(vals)]
        fill = color + "33"
        dash = ' stroke-dasharray="6 4"' if style == "dash" else ""
        svg.append(f'<polygon points="{polygon(pts)}" fill="{fill}" stroke="{color}" stroke-width="2.2"{dash}/>')
        for x, y in pts:
            svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{color}"/>')

    # 标题与图例
    svg.append(f'<text x="{CX}" y="28" fill="#111111" font-size="20" font-weight="bold" text-anchor="middle">AI 内容标识实操 · 质量与安全稳定性实测（6 维度 0-5 分）</text>')
    ly = 32
    for name, color, style in SERIES:
        dash = ' stroke-dasharray="6 4"' if style == "dash" else ""
        svg.append(f'<line x1="180" y1="{ly}" x2="210" y2="{ly}" stroke="{color}" stroke-width="3"{dash}/>')
        svg.append(f'<text x="218" y="{ly+4}" fill="#333333" font-size="13">{name}</text>')
        ly += 24
    svg.append(f'<text x="{W-24}" y="{H-14}" fill="#999999" font-size="11" text-anchor="end">本地闭环验证 · 零网络零采集 · 可重复 · 基准日 2026-08-27</text>')
    svg.append("</svg>")

    out = os.path.join(VERIFY, "security-radar.svg")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"雷达图已生成：{out}")
    # 汇总对比数据
    print("\n维度对比（我们实测 / 行业基线 / 企业级标准）：")
    for i, d in enumerate(data["dimensions"]):
        print(f"  {DIM_LABELS[i]:<10s} {d['score']:.1f}  / {base[d['key']]:.1f}  / {ent[d['key']]:.1f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
