#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可数特征核验 count_features.py —— 用颜色分割**客观计数**重复元素（尾尖 / 头 / 角 / 灯 等）

背景：图像模型**不会计数**，只会采样"很多个"这个分布；而人眼在缩略图上也**数不准**
（实测：同一张图，肉眼记 9 条、放大后实为 10 条）。
所以对"典籍硬特征"（九尾 / 三头 / 六足 / 千手）必须**程序化核验**。

原理：给重复元素一个**独特的高饱和标识色**（如朱砂尾尖），
      按色相+饱和度分割 → 形态学清理 → 连通域计数 → 按面积过滤小噪点。

⚠️ 两个必需的人工环节：
  1. **--roi 限定区域**：背景里同色系的元素（鎏金立柱、眼周纹路）会造成假阳性，必须用 ROI 排除。
  2. **--dump-mask 目视复核**：计数结果**必须**看一眼掩膜叠加图，确认色块确实落在目标元素上。

依赖：opencv-python、numpy（本机已具备）。

用法：
  # 数朱砂尾尖（默认参数），限定尾扇 ROI，并存掩膜叠加图复核
  python3 scripts/count_features.py 图.png --roi 0,0,1050,900 --dump-mask /tmp/mask.png
  # 批量数一个目录，输出 CSV 便于挑 best-of-N
  python3 scripts/count_features.py --dir 图片目录 --roi 0,0,1050,900 --csv 结果.csv
  # 换标识色（如金色 / 青色）：--hue-lo 170 --hue-hi 14 是红橙；金色约 --hue-lo 160 --hue-hi 30
"""
import argparse
import csv
import glob
import os
import sys

import cv2
import numpy as np

IMG_EXTS = (".png", ".jpg", ".jpeg", ".webp")


def build_mask(img, hue_lo, hue_hi, sat, val, close, open_):
    """按 HSV 阈值取掩膜：色相落在 [hue_lo,179]∪[0,hue_hi]，且饱和度/明度达标。"""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    H, S, V = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    m = (((H <= hue_hi) | (H >= hue_lo)) & (S >= sat) & (V >= val)).astype(np.uint8) * 255
    if close > 0:
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((close, close), np.uint8))
    if open_ > 0:
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((open_, open_), np.uint8))
    return m


def count_blobs(mask, min_area, roi=None):
    """连通域计数；返回 (面积降序列表, 全部面积)。roi=(x,y,w,h) 时只计 ROI 内的连通域。"""
    n, lab, stats, cent = cv2.connectedComponentsWithStats(mask, 8)
    areas = []
    for i in range(1, n):
        x, y, w, h, a = stats[i]
        if a < min_area:
            continue
        if roi:
            rx, ry, rw, rh = roi
            cx, cy = cent[i]
            # 以质心判定是否落在 ROI 内（避免大色块跨边界被误算）
            if not (rx <= cx <= rx + rw and ry <= cy <= ry + rh):
                continue
        areas.append(int(a))
    areas.sort(reverse=True)
    return areas


def parse_roi(s):
    if not s:
        return None
    parts = [int(float(x)) for x in s.replace(" ", "").split(",")]
    if len(parts) != 4:
        sys.exit("[FAIL] --roi 需为 x,y,w,h")
    return tuple(parts)


def collect(paths, args, roi):
    out = []
    for p in paths:
        img = cv2.imread(p)
        if img is None:
            print(f"[skip] 读不了：{p}", file=sys.stderr)
            continue
        m = build_mask(img, args.hue_lo, args.hue_hi, args.sat, args.val,
                       args.close, args.open)
        areas = count_blobs(m, args.min_area, roi)
        out.append((p, len(areas), areas))
        flag = "✅" if (args.expect and len(areas) == args.expect) else "  "
        exp = f" (期望 {args.expect})" if args.expect else ""
        print(f"{flag} {len(areas):2d} 个{exp}  {os.path.basename(p)}")
        if args.verbose:
            print(f"      面积: {areas}")
        if args.dump_mask:
            base = os.path.splitext(os.path.basename(p))[0]
            root, ext = os.path.splitext(args.dump_mask)
            vis = img.copy()
            vis[m > 0] = (0, 0, 255)
            if roi:
                x, y, w, h = roi
                cv2.rectangle(vis, (x, y), (x + w, y + h), (0, 255, 0), 3)
            dst = f"{root}-{base}{ext or '.png'}"
            cv2.imwrite(dst, vis)
            print(f"      掩膜叠加 → {dst}")
    return out


def main():
    ap = argparse.ArgumentParser(description="可数特征核验：颜色分割 + 连通域计数")
    ap.add_argument("images", nargs="*", help="图片路径（可多个）")
    ap.add_argument("--dir", default="", help="图片目录（与位置参数二选一）")
    ap.add_argument("--hue-lo", type=int, default=170, help="红色相下界（默认 170）")
    ap.add_argument("--hue-hi", type=int, default=14, help="红色相上界（默认 14）")
    ap.add_argument("--sat", type=int, default=100, help="饱和度下界（默认 100）")
    ap.add_argument("--val", type=int, default=90, help="明度下界（默认 90）")
    ap.add_argument("--min-area", type=int, default=1200, help="最小连通域面积（默认 1200）")
    ap.add_argument("--close", type=int, default=9, help="闭运算核（默认 9，0=不做）")
    ap.add_argument("--open", dest="open", type=int, default=5, help="开运算核（默认 5，0=不做）")
    ap.add_argument("--roi", default="", help="限定区域 x,y,w,h（强烈建议：排除背景同色元素）")
    ap.add_argument("--expect", type=int, default=0, help="期望个数；命中打 ✅（如 9）")
    ap.add_argument("--dump-mask", default="", help="掩膜叠加图输出路径前缀（用于目视复核）")
    ap.add_argument("--csv", default="", help="结果写 CSV")
    ap.add_argument("--verbose", action="store_true", help="打印面积列表")
    args = ap.parse_args()

    paths = list(args.images)
    if args.dir:
        for e in IMG_EXTS:
            paths += sorted(glob.glob(os.path.join(args.dir, f"*{e}")))
    if not paths:
        sys.exit("[FAIL] 未给图片（位置参数或 --dir）")
    roi = parse_roi(args.roi)

    print(f"[参数] 色相 {args.hue_lo}-179 / 0-{args.hue_hi}  S>={args.sat} V>={args.val} "
          f"面积>={args.min_area}  ROI={roi or '全图（注意假阳性）'}\n")
    res = collect(paths, args, roi)

    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(["文件", "个数", "面积(降序)"])
            for p, n, a in res:
                w.writerow([os.path.basename(p), n, " ".join(map(str, a))])
        print(f"\n[CSV] {args.csv}")

    if args.expect:
        hit = [p for p, n, _ in res if n == args.expect]
        print(f"\n[汇总] {len(hit)}/{len(res)} 张命中 {args.expect} 个")
        for p in hit:
            print(f"  ✅ {os.path.basename(p)}")
        print("\n⚠️ 必须目视复核掩膜叠加图（--dump-mask），确认色块落在目标元素上；"
              "计数仅供参考，最终以放大目视为准。")


if __name__ == "__main__":
    main()
