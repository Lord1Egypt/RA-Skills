#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
visualize.py — 把缠论结构画在K线上 (自包含HTML/SVG, 零依赖, 供人工核对与展示)
用法: python visualize.py --symbol 600519.SH --csv k.csv [--out chart.html] [--bars 250]
画: 蜡烛图 + 笔(折线) + 中枢(矩形带ZG/ZD) + 买卖点(标记) + 标题带操作判定
"""
import argparse
import html
import json
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chan_engine import load_csv, run  # noqa: E402

W, H, PAD_T, PAD_B, PAD_L, PAD_R = 1180, 560, 56, 28, 10, 64


def build_svg(symbol, rows, out):
    n = len(rows)
    x_of = {r["date"]: PAD_L + (W - PAD_L - PAD_R) * (i + 0.5) / n for i, r in enumerate(rows)}
    lo = min(r["low"] for r in rows)
    hi = max(r["high"] for r in rows)
    span = (hi - lo) or 1

    def y_of(p):
        return PAD_T + (H - PAD_T - PAD_B) * (hi - p) / span

    bw = max(1.2, (W - PAD_L - PAD_R) / n * 0.62)
    s = []
    # 中枢矩形(先画在底层)
    for z in out["day"]["zs"]:
        if z["e"] < rows[0]["date"]:
            continue
        x1 = x_of.get(z["b"], PAD_L)
        x2 = x_of.get(z["e"], W - PAD_R)
        y1, y2 = y_of(z["zg"]), y_of(z["zd"])
        dash = "" if z["sure"] else ' stroke-dasharray="5 4"'
        s.append(f'<rect x="{x1:.1f}" y="{y1:.1f}" width="{x2-x1:.1f}" height="{y2-y1:.1f}" '
                 f'fill="#1e3a8a12" stroke="#1e3a8a" stroke-width="1.2"{dash}/>')
        s.append(f'<text x="{x2+4:.1f}" y="{y1+4:.1f}" font-size="10" fill="#1e3a8a">ZG {z["zg"]}</text>')
        s.append(f'<text x="{x2+4:.1f}" y="{y2+4:.1f}" font-size="10" fill="#1e3a8a">ZD {z["zd"]}</text>')
    # 蜡烛
    for r in rows:
        x = x_of[r["date"]]
        up = r["close"] >= r["open"]
        c = "#c0392b" if up else "#16794c"          # A股红涨绿跌
        s.append(f'<line x1="{x:.1f}" y1="{y_of(r["high"]):.1f}" x2="{x:.1f}" '
                 f'y2="{y_of(r["low"]):.1f}" stroke="{c}" stroke-width="1"/>')
        yo, yc = y_of(r["open"]), y_of(r["close"])
        y1, hgt = min(yo, yc), max(abs(yc - yo), 0.8)
        fill = c if not up else "#fff"
        s.append(f'<rect x="{x-bw/2:.1f}" y="{y1:.1f}" width="{bw:.1f}" height="{hgt:.1f}" '
                 f'fill="{fill}" stroke="{c}" stroke-width="1"/>')
    # 笔折线
    pts = []
    for b in out["day"]["bi"]:
        if b["b"] in x_of and not pts:
            pts.append((x_of[b["b"]], y_of(b["bv"])))
        if b["e"] in x_of:
            pts.append((x_of[b["e"]], y_of(b["ev"])))
    if len(pts) > 1:
        d = " ".join(f'{x:.1f},{y:.1f}' for x, y in pts)
        s.append(f'<polyline points="{d}" fill="none" stroke="#0b0f1a" stroke-width="2" opacity=".85"/>')
    # 买卖点标记
    for p in out["day"]["bsp"]:
        if p["d"] not in x_of:
            continue
        x, y = x_of[p["d"]], y_of(p["px"])
        buy = p["bs"] == "B"
        col = "#c0392b" if buy else "#16794c"
        dy = 16 if buy else -10
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{col}"/>')
        s.append(f'<text x="{x:.1f}" y="{y+dy:.1f}" font-size="11" font-weight="700" '
                 f'text-anchor="middle" fill="{col}">{"B" if buy else "S"}{p["type"]}'
                 f'{"" if p["sure"] else "?"}</text>')
    verdict = html.escape(out["verdict"]["action"])
    title = (f'{html.escape(symbol)} · 缠论结构 · {out["meta"]["asof"]} · 判定: {verdict}'
             f'（虚线中枢/带?买卖点=未确认）')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'style="max-width:100%;background:#fafbfc">'
            f'<text x="{PAD_L}" y="24" font-size="15" font-weight="700" fill="#0b0f1a">{title}</text>'
            + "".join(s) + "</svg>")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbol", required=True)
    ap.add_argument("--csv", required=True)
    ap.add_argument("--out")
    ap.add_argument("--bars", type=int, default=250)
    a = ap.parse_args()
    rows_all = load_csv(a.csv)
    out = run(a.symbol, rows_all)
    rows = rows_all[-a.bars:]
    svg = build_svg(a.symbol, rows, out)
    page = (f'<!doctype html><meta charset="utf-8"><title>{html.escape(a.symbol)} 缠论结构</title>'
            f'<body style="margin:16px;font-family:sans-serif">{svg}'
            f'<p style="font-size:13px;color:#626b7d;max-width:1100px">{html.escape(out["summary"]["verdict"])}</p></body>')
    path = a.out or f'chan_{a.symbol.replace(".", "_")}.html'
    open(path, "w", encoding="utf-8").write(page)
    print(json.dumps({"written": path, "bars": len(rows)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
