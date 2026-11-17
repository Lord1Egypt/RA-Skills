#!/usr/bin/env python3
"""半岛碎块：量化 + 零风险试验（只处理副本，不动装机包）

- 对每个候选碎块测「悬空距离」= 碎块像素到主体连通域的最小距离
- 在副本上执行切颈，产出 4× 放大前后对比 + 128px 实际显示尺度对比
- 默认 dry-run，--apply 才写副本；装机包永远不动（改包须显式 --pack）
"""
import argparse
import json
import shutil
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

PACK = Path("C:/Users/mercy/Desktop/LunaPet_v26-转身接线/_internal/packs/luna")
OUT = Path("C:/Users/mercy/WorkBuddy/2026-09-28-20-59-35/lunapet_v26_素材目检/peninsula_trial")
DISPLAY = 128          # 桌宠实际显示尺度（512 画布按 1/4 显示）
ALPHA_FLOOR = 4
MAX_R = 4
MAX_TIP_AREA = 400
ZOOM, PAD = 4, 30


def disk(r):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def find_candidates(mask):
    """返回 [(tip_mask, r_star, tip_area, protrude_dist)]"""
    levels = {}
    for r in range(1, MAX_R + 1):
        er = cv2.erode(mask, disk(r))
        num, labels, stats, cent = cv2.connectedComponentsWithStats(er, connectivity=8)
        if num <= 1:
            levels[r] = (er, labels, stats, cent, [], None)
            continue
        areas = stats[1:, cv2.CC_STAT_AREA]
        main_id = int(np.argmax(areas)) + 1
        others = [(int(stats[i, cv2.CC_STAT_AREA]), (float(cent[i][0]), float(cent[i][1])), i)
                  for i in range(1, num) if i != main_id]
        levels[r] = (er, labels, stats, cent, others, main_id)

    # 主体（用于算悬空距离）
    _, _, _, _, _, main_id = levels[1]
    main_mask = (levels[1][1] == main_id).astype(np.uint8) if main_id else None

    out = []
    for area1, (cx, cy), _ in levels[1][4]:
        if area1 > MAX_TIP_AREA:
            continue
        r_star = 1
        for r in range(2, MAX_R + 1):
            if not any(abs(x - cx) < 10 and abs(y - cy) < 10 for _, (x, y), _ in levels[r][4]):
                break
            r_star = r
        er, labels, _, cent, _, _ = levels[r_star]
        best, bd = None, 1e9
        for i in range(1, int(labels.max()) + 1):
            d = (cent[i][0] - cx) ** 2 + (cent[i][1] - cy) ** 2
            if d < bd:
                bd, best = d, i
        if best is None:
            continue
        seed = (labels == best).astype(np.uint8)
        grown = cv2.dilate(seed, disk(r_star)) & mask
        n2, l2, _, _ = cv2.connectedComponentsWithStats(grown, connectivity=8)
        tip = np.zeros_like(mask)
        for i in range(1, n2):
            if np.any((l2 == i) & seed):
                tip |= (l2 == i).astype(np.uint8)
        tip_area = int(tip.sum())
        if tip_area == 0 or tip_area > MAX_TIP_AREA:
            continue
        # 悬空距离：碎块像素到主体连通域的最小距离
        if main_mask is not None:
            dist_map = cv2.distanceTransform(1 - main_mask, cv2.DIST_L2, 3)
            pd = float(dist_map[tip > 0].min())
        else:
            pd = 0.0
        out.append((tip, r_star, tip_area, pd))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--actions", default="idle", help="逗号分隔，默认只试 idle")
    ap.add_argument("--apply", action="store_true", help="写入副本（默认只出预览）")
    ap.add_argument("--pack", action="store_true",
                    help="⛔ 直接改装机包（需 --apply，谨慎）")
    args = ap.parse_args()

    cfg = json.loads((PACK / "pet.json").read_text(encoding="utf-8"))
    actions = [a.strip() for a in args.actions.split(",") if a.strip()]

    if args.apply:
        if args.pack:
            target_root = PACK / "action"
            print("⚠️ 目标 = 装机包本体")
        else:
            target_root = OUT / "staging" / "action"
            target_root.mkdir(parents=True, exist_ok=True)
            print(f"目标 = 副本 {target_root}")
    else:
        target_root = None
        print("dry-run：只出预览，不写任何文件")

    stats_rows = []
    for action in actions:
        frames = sorted(((int(p.stem[len(action) + 1:]), p)
                         for p in (PACK / "action").iterdir()
                         if p.stem.startswith(action + "_") and p.stem[len(action) + 1:].isdigit()))
        for idx, path in frames:
            rgba = np.array(Image.open(path).convert("RGBA"))
            mask = (rgba[:, :, 3] >= ALPHA_FLOOR).astype(np.uint8)
            cands = find_candidates(mask)
            if not cands:
                continue

            cut = rgba.copy()
            for tip, r_star, area, pd in cands:
                cut[tip > 0, 3] = 0            # 切颈：整块碎块归零

            stats_rows.append(dict(action=action, idx=idx, n=len(cands),
                                   area=sum(c[2] for c in cands),
                                   maxpd=max(c[3] for c in cands),
                                   maxr=max(c[1] for c in cands)))

            # 预览：每个碎块一张 4× 前后对比
            for k, (tip, r_star, area, pd) in enumerate(sorted(cands, key=lambda c: -c[2])[:6]):
                ys, xs = np.nonzero(tip)
                x0 = max(0, xs.min() - PAD); y0 = max(0, ys.min() - PAD)
                x1 = min(rgba.shape[1], xs.max() + PAD); y1 = min(rgba.shape[0], ys.max() + PAD)
                panel = Image.new("RGB", ((x1 - x0) * 2 * ZOOM + 30, (y1 - y0) * ZOOM + 30), (255, 255, 255))
                for side, arr in ((0, rgba), (1, cut)):
                    crop = Image.fromarray(arr[y0:y1, x0:x1]).resize(
                        ((x1 - x0) * ZOOM, (y1 - y0) * ZOOM), Image.NEAREST)
                    bg = Image.new("RGB", crop.size, (255, 255, 255))
                    d = ImageDraw.Draw(bg)
                    for yy in range(0, bg.height, 8):
                        for xx in range(0, bg.width, 8):
                            if (xx // 8 + yy // 8) % 2 == 0:
                                d.rectangle([xx, yy, xx + 7, yy + 7], fill=(215, 215, 215))
                    bg.paste(crop, (0, 0), crop)
                    panel.paste(bg, (side * ((x1 - x0) * ZOOM + 30), 20))
                d = ImageDraw.Draw(panel)
                d.text((4, 4), f"{path.name} #{k} area={area} neck<={2*r_star}px gap={pd:.1f}px   L=原图 R=切后",
                       fill=(0, 0, 0))
                (OUT / "crops").mkdir(parents=True, exist_ok=True)
                panel.save(OUT / "crops" / f"{action}_{idx:02d}_c{k}_a{area}_gap{pd:.0f}.png")

            # 显示尺度对比（128px）
            small = Image.new("RGB", (DISPLAY * 2 + 20, DISPLAY + 24), (255, 255, 255))
            for side, arr in ((0, rgba), (1, cut)):
                im = Image.fromarray(arr).resize((DISPLAY, DISPLAY), Image.LANCZOS)
                tile = Image.new("RGB", (DISPLAY, DISPLAY), (128, 128, 128))
                tile.paste(im, (0, 0), im)
                small.paste(tile, (side * (DISPLAY + 20), 20))
            d = ImageDraw.Draw(small)
            d.text((4, 4), f"{path.name}  实际显示尺度(128px)  L=原图 R=切后", fill=(0, 0, 0))
            (OUT / "display").mkdir(parents=True, exist_ok=True)
            small.save(OUT / "display" / f"{action}_{idx:02d}.png")

            if args.apply and target_root is not None:
                if args.pack:
                    bak = OUT / "backup_pack" / action
                    bak.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(path, bak / path.name)
                Image.fromarray(cut).save(target_root / path.name, optimize=True)

    print(f"\n{'帧':<18}{'碎块数':>6}{'总面积':>8}{'最大悬空':>9}{'最大脖子':>9}")
    for r in stats_rows:
        print(f"{r['action']+'_'+str(r['idx']):<18}{r['n']:>6}{r['area']:>8}{r['maxpd']:>9.1f}{2*r['maxr']:>8}px")
    tot = sum(r["n"] for r in stats_rows)
    print(f"\n合计 {len(stats_rows)} 帧 / {tot} 处")
    gaps = [r["maxpd"] for r in stats_rows]
    if gaps:
        print(f"悬空距离分布：min {min(gaps):.1f}px / 中位 {float(np.median(gaps)):.1f}px / max {max(gaps):.1f}px")


if __name__ == "__main__":
    main()
