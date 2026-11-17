#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""badge-studio — ORCID 清新风格徽章生成器（20px 标准高、四色角度、细字）。
理论根基：LGD 徽章体系。Usage:
  python badge_studio.py --label LGD --score 90/100 [--color 2563eb] [--icon LGD] [--out out.svg]"""
import argparse, os, sys

H = 20; IW = 22; PAD = 7
COLORS = {"REG": "2563eb", "TRUST": "0d9488", "SAFE": "16a34a", "MACH": "7c3aed", "LGD": "2563eb", "VERIFIED": "2563eb"}

def make_badge(icon, fill, label, score):
    fs = 8.5 if len(icon) <= 4 else (7.0 if len(icon) == 5 else 6.0)
    lw = len(label) * 5.2 if label else 0
    sw = len(score) * 6.8
    total = IW + PAD + lw + (8 if label else 0) + sw + PAD
    s = f'<svg xmlns="http://www.w3.org/2000/svg" width="{total}" height="{H}" viewBox="0 0 {total} {H}" role="img" aria-label="{icon} {score}">'
    s += f'<rect x="0.5" y="0.5" width="{total-1}" height="{H-1}" rx="4" fill="#ffffff" stroke="#e2e8f0" stroke-width="1"/>'
    s += f'<rect x="1" y="1" width="{IW}" height="{H-2}" rx="3" fill="#{fill}"/>'
    s += f'<text x="{IW/2+1}" y="{13.8 if fs>=8 else 13.0}" fill="#ffffff" font-size="{fs}" font-weight="500" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif">{icon}</text>'
    if label:
        s += f'<text x="{IW+PAD}" y="13.8" fill="#0f172a" font-size="9" font-weight="300" font-family="Segoe UI,Arial,sans-serif">{label}</text>'
    x = IW + PAD + (lw + 8 if label else 0)
    s += f'<text x="{x}" y="13.9" fill="#0f172a" font-size="10" font-weight="500" font-family="Segoe UI,Arial,sans-serif">{score}</text>'
    return s + '</svg>'

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--label", default="VERIFIED", help="text label (omit = icon+score only)")
    p.add_argument("--score", default="90/100")
    p.add_argument("--icon", default="LGD")
    p.add_argument("--color", default=None, help="hex color for icon block")
    p.add_argument("--out", default="badge.svg")
    a = p.parse_args()
    fill = (a.color or COLORS.get(a.icon.upper()) or COLORS.get(a.label.upper()) or "2563eb")
    svg = make_badge(a.icon, fill, a.label, a.score)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(svg)
    print("badge written:", a.out)
    return 0

if __name__ == "__main__":
    sys.exit(main())
