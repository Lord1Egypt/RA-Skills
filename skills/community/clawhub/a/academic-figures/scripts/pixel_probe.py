#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pixel_probe：多面板交付图的逐面板像素密度探针（v7.8.0 批次2 · B2）。

对每个网格面板统计「非背景像素占比」，机械暴露两类排版事故：
- <1.5%  WARN（空白/不可见面板——渲染失败、数据为空、面板被裁）
- >50%   WARN（过绘——元素铺满无留白，字号/信息密度必然崩坏）

设计要点：
- 背景判定 = 近白色（RGB 三通道均 ≥245 的像素为背景），与引擎白底约定一致；
- 面板网格用 --grid 行x列 均分（如 2x2）；面板间天然留白会被均分边界吃进
  邻格，属可接受的近似——探针的职责是抓「整格空白/整格过绘」这类宏观事故，
  不做精确版面测量；
- 结构化输出：人类可读行 + --json <path> 侧车（逐面板占比与 WARN 明细）；
- 报告型工具：默认 WARN 不改变退出码（exit 0），--fail-on-warn 供流水线
  把 WARN 升级为 exit 1；输入/依赖错误沿用我方语义（1=输入类，2=依赖缺失）。

Usage:
  python pixel_probe.py figure.png --grid 2x2
  python pixel_probe.py figure.png --grid 2x2 --json probe.json --fail-on-warn
  python pixel_probe.py --selftest
"""
import argparse
import json
import os
import sys

WARN_BLANK = 0.015   # 非背景像素占比下限（1.5%）
WARN_OVERDRAW = 0.50  # 上限（50%）
BACKDROP = 245        # 背景=近白阈值（三通道均 ≥ 此值）


def probe(image_path, grid_rows, grid_cols):
    """逐面板统计非背景像素占比。返回 (panels, w, h)。"""
    try:
        import numpy as np
    except ImportError:
        print("ERROR: pixel_probe 需要 numpy（pip install numpy）", file=sys.stderr)
        sys.exit(2)
    try:
        from PIL import Image
    except ImportError:
        print("ERROR: pixel_probe 需要 Pillow（pip install pillow）", file=sys.stderr)
        sys.exit(2)
    im = Image.open(image_path).convert("RGB")
    w, h = im.size
    arr = np.asarray(im).astype(int)
    fg = ~((arr[:, :, 0] >= BACKDROP) & (arr[:, :, 1] >= BACKDROP)
           & (arr[:, :, 2] >= BACKDROP))
    panels = []
    for r in range(grid_rows):
        for c in range(grid_cols):
            y0 = h * r // grid_rows
            y1 = h * (r + 1) // grid_rows
            x0 = w * c // grid_cols
            x1 = w * (c + 1) // grid_cols
            cell = fg[y0:y1, x0:x1]
            ratio = float(cell.mean()) if cell.size else 0.0
            warns = []
            if ratio < WARN_BLANK:
                warns.append(f"blank-ish（{ratio * 100:.2f}% < {WARN_BLANK * 100:.1f}%——"
                             "空白/不可见面板？）")
            if ratio > WARN_OVERDRAW:
                warns.append(f"overdraw（{ratio * 100:.2f}% > {WARN_OVERDRAW * 100:.0f}%——"
                             "过绘，留白不足）")
            panels.append({"panel": f"r{r + 1}c{c + 1}", "fg_ratio": round(ratio, 4),
                           "warns": warns})
    return panels, w, h


def selftest():
    """合成 2x2 图：一格空白/一格过绘/两格正常——四格判定必须全部命中。"""
    try:
        import numpy as np
        from PIL import Image
    except ImportError:
        print("ERROR: selftest 需要 numpy+Pillow", file=sys.stderr)
        sys.exit(2)
    import tempfile
    W = H = 800
    im = np.full((H, W, 3), 255, dtype=np.uint8)
    im[0:H // 2, 0:W // 2] = 250                      # r1c1 空白（无任何前景）
    im[0:H // 2, W // 2:] = (30, 30, 30)              # r1c2 过绘（整格深色）
    for y in range(H // 2 + 40, H - 40, 24):          # r2c1/r2c2 正常（细线条）
        im[y:y + 6, W // 4:W - W // 4] = (60, 60, 60)
    fp = os.path.join(tempfile.mkdtemp(), "st.png")
    Image.fromarray(im).save(fp)
    panels, _, _ = probe(fp, 2, 2)
    by = {p["panel"]: p for p in panels}
    ok = True
    checks = [("r1c1", "blank-ish"), ("r1c2", "overdraw"), ("r2c1", None), ("r2c2", None)]
    for name, want in checks:
        p = by[name]
        got = p["warns"][0].split("（")[0] if p["warns"] else None
        good = (got == want)
        ok = ok and good
        print(f"  selftest {name}: ratio={p['fg_ratio'] * 100:.2f}% warn={got} "
              f"期望={want} 判定={'PASS' if good else 'FAIL'}")
    print("pixel_probe --selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="Per-panel pixel-density probe for delivery figures")
    ap.add_argument("image", nargs="?", default=None, help="交付图（PNG）")
    ap.add_argument("--grid", default="1x1", help="面板网格 行x列（如 2x2；默认 1x1）")
    ap.add_argument("--json", default=None, metavar="PATH", help="结构化结果侧车 JSON")
    ap.add_argument("--fail-on-warn", action="store_true",
                    help="任一面板 WARN → exit 1（流水线闸模式；默认报告型 rc=0）")
    ap.add_argument("--selftest", action="store_true", help="内置自测（无需输入）")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(selftest())
    if not args.image or not os.path.isfile(args.image):
        print("ERROR: 需要 --image 交付图路径（或 --selftest）", file=sys.stderr)
        sys.exit(1)
    try:
        gr, gc = (int(x) for x in args.grid.lower().split("x"))
    except ValueError:
        print(f"ERROR: --grid 形如 2x2，收到 '{args.grid}'", file=sys.stderr)
        sys.exit(1)
    if not (1 <= gr <= 8 and 1 <= gc <= 8):
        print("ERROR: --grid 行列须在 1-8", file=sys.stderr)
        sys.exit(1)

    panels, w, h = probe(args.image, gr, gc)
    n_warn = sum(1 for p in panels if p["warns"])
    print(f"== pixel_probe: {args.image}（{w}x{h}px，网格 {gr}x{gc}）==")
    for p in panels:
        tag = " ⚠️ " + "；".join(p["warns"]) if p["warns"] else " OK"
        print(f"  {p['panel']}: 前景占比 {p['fg_ratio'] * 100:6.2f}%{tag}")
    print(f"汇总: {len(panels)} 面板，WARN {n_warn}（blank<{WARN_BLANK * 100:.1f}% / "
          f"overdraw>{WARN_OVERDRAW * 100:.0f}%）")
    if args.json:
        json.dump({"image": os.path.abspath(args.image), "grid": [gr, gc],
                   "thresholds": {"blank": WARN_BLANK, "overdraw": WARN_OVERDRAW},
                   "panels": panels}, open(args.json, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print(f"结构化结果 → {args.json}")
    if n_warn and args.fail_on_warn:
        print("FAIL-ON-WARN: 存在 WARN 面板（流水线闸触发）")
        sys.exit(1)


if __name__ == "__main__":
    main()
