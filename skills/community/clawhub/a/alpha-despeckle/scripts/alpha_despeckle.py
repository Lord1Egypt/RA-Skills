#!/usr/bin/env python3
"""alpha_despeckle.py -- 清除抠像后 PNG 中残留的细小像素块。

针对已完成抠像（透明底）的 RGBA PNG：
  A. 半透明残渣：alpha < alpha-thresh 的像素直接归零（雾状残留）。
  B. 孤岛残渣：alpha 连通域面积 < min-area 的整块归零（飞溅的小点/碎块）。
  C. 安全阀：无论参数如何，面积排名前 keep-largest 的连通域永不删除。

默认 dry-run（只报告不动文件）；--apply 才落盘，落盘前默认生成字节级备份。
"""

import argparse
import glob
import os
import shutil
import sys

import cv2
import numpy as np

try:
    from PIL import Image
except ImportError:
    print("ERROR: 需要 Pillow（pip install pillow）", file=sys.stderr)
    sys.exit(1)


def analyze_and_clean(rgba: np.ndarray, alpha_thresh: int, min_area: int,
                      connectivity: int, keep_largest: int, force: bool):
    """返回 (cleaned_rgba, report_dict)。不修改输入数组。"""
    h, w = rgba.shape[:2]
    alpha = rgba[:, :, 3]

    report = {
        "size": (w, h),
        "opaque_before": int((alpha > 0).sum()),
        "haze_px": 0,
        "islands_removed": 0,
        "island_px": 0,
        "removed_list": [],   # [(area, x, y, w, h, mean_alpha), ...] 按 area 降序
        "kept_top": [],
        "refused": False,
    }

    # --- A. 半透明残渣 ---
    haze_mask = (alpha > 0) & (alpha < alpha_thresh)
    report["haze_px"] = int(haze_mask.sum())
    cleaned_alpha = alpha.copy()
    cleaned_alpha[haze_mask] = 0

    # --- B. 连通域分析（只看 alpha，不碰 RGB，避免通道顺序坑） ---
    bin_mask = (cleaned_alpha >= alpha_thresh).astype(np.uint8)
    num, labels, stats, _ = cv2.connectedComponentsWithStats(
        bin_mask, connectivity=connectivity)
    if num <= 1:
        report["opaque_after"] = report["opaque_before"] - report["haze_px"]
        report["opaque_final"] = report["opaque_after"]
        out = rgba.copy()
        out[:, :, 3] = cleaned_alpha
        return out, report

    areas = stats[1:, cv2.CC_STAT_AREA]
    order = np.argsort(areas)[::-1]  # 降序
    keep_ids = set(int(order[i]) + 1 for i in range(min(keep_largest, len(order))))

    remove_ids = []
    for i in range(1, num):
        area = int(stats[i, cv2.CC_STAT_AREA])
        if i in keep_ids or area >= min_area:
            if i in keep_ids:
                x, y = int(stats[i, cv2.CC_STAT_LEFT]), int(stats[i, cv2.CC_STAT_TOP])
                report["kept_top"].append((area, x, y,
                                           int(stats[i, cv2.CC_STAT_WIDTH]),
                                           int(stats[i, cv2.CC_STAT_HEIGHT])))
            continue
        remove_ids.append(i)

    island_px = 0
    removed_list = []
    for i in remove_ids:
        area = int(stats[i, cv2.CC_STAT_AREA])
        x, y = int(stats[i, cv2.CC_STAT_LEFT]), int(stats[i, cv2.CC_STAT_TOP])
        cw, ch = int(stats[i, cv2.CC_STAT_WIDTH]), int(stats[i, cv2.CC_STAT_HEIGHT])
        comp_mask = labels == i
        mean_a = float(cleaned_alpha[comp_mask].mean())
        removed_list.append((area, x, y, cw, ch, round(mean_a, 1)))
        island_px += area

    # --- 安全阀：删除量异常大时拒绝执行 ---
    opaque_after = report["opaque_before"] - report["haze_px"]
    report["islands_removed"] = len(remove_ids)
    report["island_px"] = island_px
    report["removed_list"] = sorted(removed_list, reverse=True)
    report["opaque_after"] = opaque_after
    if opaque_after > 0 and island_px / opaque_after > 0.30 and not force:
        report["refused"] = True
        report["opaque_final"] = opaque_after
        return rgba.copy(), report  # 拒绝时完全不动

    for i in remove_ids:
        cleaned_alpha[labels == i] = 0

    report["opaque_final"] = int((cleaned_alpha > 0).sum())

    out = rgba.copy()
    out[:, :, 3] = cleaned_alpha
    return out, report


def print_report(path, rep, verbose):
    w, h = rep["size"]
    print(f"\n=== {path} ({w}x{h}) ===")
    print(f"  非透明像素: {rep['opaque_before']} -> 清理后 {rep['opaque_final']}"
          f"  (雾状残渣 {rep['haze_px']} px, 孤岛 {rep['islands_removed']} 块 / {rep['island_px']} px)")
    if rep["refused"]:
        print("  !! 拒绝执行：删除量超过非透明像素的 30%，参数可能过于激进。确认后加 --force。")
    if rep["removed_list"]:
        show = rep["removed_list"] if verbose else rep["removed_list"][:10]
        print(f"  删除明细（area, bbox=x,y,w,h, 平均alpha）前 {len(show)} 条:")
        for area, x, y, cw, ch, ma in show:
            print(f"    area={area:<6} bbox=({x},{y},{cw},{ch})  mean_alpha={ma}")
        if len(rep["removed_list"]) > len(show):
            print(f"    ... 其余 {len(rep['removed_list']) - len(show)} 块省略（--verbose 查看全部）")
    if rep["kept_top"]:
        top = rep["kept_top"][0]
        print(f"  保留最大连通域: area={top[0]} bbox=({top[1]},{top[2]},{top[3]},{top[4]})")


def main():
    ap = argparse.ArgumentParser(
        description="清除抠像 PNG 中残留的细小像素块（默认 dry-run，只报告）")
    ap.add_argument("inputs", nargs="+", help="PNG 路径，支持通配符")
    ap.add_argument("--apply", action="store_true",
                    help="实际写回（默认仅 dry-run 报告）")
    ap.add_argument("--out", help="另存目录或文件路径（与 --apply 二选一时用它则不覆盖原图）")
    ap.add_argument("--alpha-thresh", type=int, default=8,
                    help="alpha 低于该值的像素视为半透明残渣归零（默认 8）")
    ap.add_argument("--min-area", type=int, default=12,
                    help="连通域面积小于该值则整块删除（默认 12 px）")
    ap.add_argument("--connectivity", type=int, choices=(4, 8), default=8)
    ap.add_argument("--keep-largest", type=int, default=1,
                    help="无论参数如何都保留面积前 N 的连通域（默认 1）")
    ap.add_argument("--force", action="store_true",
                    help="删除量超过 30% 时仍然执行")
    ap.add_argument("--no-backup", action="store_true",
                    help="原地写回时不生成 .bak 备份（不建议）")
    ap.add_argument("--verbose", action="store_true", help="打印全部删除明细")
    args = ap.parse_args()

    files = []
    for pat in args.inputs:
        hit = sorted(glob.glob(pat)) if any(c in pat for c in "*?[") else [pat]
        files.extend(hit)
    if not files:
        print("ERROR: 未匹配到文件", file=sys.stderr)
        sys.exit(1)

    out_dir = None
    out_file = None
    if args.out:
        if args.apply:
            print("ERROR: --apply 与 --out 不能同时使用", file=sys.stderr)
            sys.exit(1)
        has_img_ext = os.path.splitext(args.out)[1].lower() in (".png",)
        if os.path.isdir(args.out) or not has_img_ext:
            out_dir = args.out
            os.makedirs(out_dir, exist_ok=True)
        else:
            out_file = args.out

    exit_code = 0
    for path in files:
        if not os.path.isfile(path):
            print(f"SKIP（不存在）: {path}", file=sys.stderr)
            exit_code = 1
            continue
        img = Image.open(path)
        if img.mode != "RGBA":
            print(f"SKIP（非 RGBA，mode={img.mode}）: {path}", file=sys.stderr)
            exit_code = 1
            continue
        rgba = np.array(img)
        cleaned, rep = analyze_and_clean(
            rgba, args.alpha_thresh, args.min_area,
            args.connectivity, args.keep_largest, args.force)
        print_report(path, rep, args.verbose)

        if rep["refused"]:
            exit_code = 2
            continue
        if not (args.apply or args.out):
            continue  # dry-run 到此为止

        if args.apply:
            if not args.no_backup:
                bak = path + ".despeckle.bak.png"
                shutil.copy2(path, bak)
                print(f"  备份: {bak}")
            Image.fromarray(cleaned).save(path, optimize=True)
            print(f"  已写回: {path}")
        else:
            dst = (os.path.join(out_dir, os.path.basename(path))
                   if out_dir else out_file)
            Image.fromarray(cleaned).save(dst, optimize=True)
            print(f"  已另存: {dst}")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
