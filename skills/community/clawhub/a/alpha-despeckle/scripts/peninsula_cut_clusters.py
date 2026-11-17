#!/usr/bin/env python3
"""半岛碎块定点切除（可复用）：--ids "#67,#70,#72,#111"

用法：
  python peninsula_cut_clusters.py --ids 67,70,72,111 [--expect "67=7,11;70=6,15"]

要点（都是踩过的坑）：
- 簇编号来自**切除前**基线（peninsula_stats_full.json）生成的聚类页，所以编号永远以该基线为准，
  不能拿当前文件重算（切过的会消失、编号会错位）。
- 逐成员**严格匹配**：当前帧里要求 |dx|,|dy|≤2 且面积 ±2；找不到就跳过（视为已清过）。
  ⛔ 绝不用"最近候选"兜底 —— 那会误切邻近的不同特征（实测拦下过 5 处）。
- 切完必须清残余：主块被切后周围 alpha 12~25 低值像素会被切断，变成新的 1px 孤岛。
- 备份写在素材包外；切完打印残余清理明细，供复扫核对。
"""
import argparse
import importlib.util
import json
import shutil
from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

here = Path(__file__).resolve().parent
_trial = None
for cand in (here / "peninsula_cut_trial.py", here / "peninsula_trial.py",
             here / ".." / "peninsula_cut_trial.py", here / ".." / "peninsula_trial.py"):
    if cand.exists():
        _trial = cand
        break
if _trial is None:
    raise SystemExit("找不到 peninsula_cut_trial.py / peninsula_trial.py")
spec = importlib.util.spec_from_file_location("pt", _trial)
pt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pt)

ap = argparse.ArgumentParser()
ap.add_argument("--ids", required=True, help="簇编号，如 67,70,72,111")
ap.add_argument("--expect", default="", help='核对用，如 "67=7,11;70=6,15"')
ap.add_argument("--baseline", default="peninsula_stats_full.json", help="切除前基线候选表")
ap.add_argument("--out", default=".", help="输出目录（结果图与日志）")
ap.add_argument("--max-d", type=float, default=2.5,
                help="实体侵入守卫：候选像素到背景距离超过此值即拒切（薄片 d 小，实体内部 d 大；默认 2.5）")
args = ap.parse_args()

ids = [int(x) for x in args.ids.replace("#", "").split(",") if x.strip()]
expect = {}
for part in args.expect.split(";"):
    if "=" in part:
        k, v = part.split("=")
        expect[int(k.replace("#", ""))] = [int(t) for t in v.split(",")]

OUT = Path(args.out)
BACKUP = OUT / "lunapet_v26_素材目检" / "backup_before_peninsula_cut"
CROPDIR = OUT / "lunapet_v26_素材目检" / "peninsula_cut_结果"
CROPDIR.mkdir(parents=True, exist_ok=True)
LINK = 8
ZOOM, PAD = 5, 30

# ---- 复现基线聚类编号 ----
rows = json.loads((OUT / "lunapet_v26_素材目检" / args.baseline).read_text(encoding="utf-8")) \
    if (OUT / "lunapet_v26_素材目检" / args.baseline).exists() \
    else json.loads(Path(args.baseline).read_text(encoding="utf-8"))
by_action = defaultdict(list)
for r in rows:
    by_action[r["action"]].append(r)
clusters = []
for action, items in by_action.items():
    unvis = list(items)
    while unvis:
        seed = unvis.pop(0)
        group = [seed]
        changed = True
        while changed:
            changed = False
            for c in unvis[:]:
                for g in group:
                    if g["idx"] == c["idx"]:
                        continue
                    if ((g["x"] - c["x"]) ** 2 + (g["y"] - c["y"]) ** 2) ** 0.5 <= LINK:
                        group.append(c)
                        unvis.remove(c)
                        changed = True
                        break
        clusters.append(dict(action=action, group=group))
clusters.sort(key=lambda c: -len(set(g["idx"] for g in c["group"])))

print("=== 编号核对 ===")
for cid in ids:
    c = clusters[cid]
    frames = sorted(set(g["idx"] for g in c["group"]))
    areas = sorted(set(g["area"] for g in c["group"]))
    mark = ""
    if cid in expect:
        mark = "✔" if frames == expect[cid] else f"⛔ 期望帧 {expect[cid]}"
    print(f"  #{cid} {c['action']}: 帧{frames} 面积{areas} {mark}")

cut_log, skip_log = [], []
touched = set()
for cid in ids:
    c = clusters[cid]
    for g in c["group"]:
        action, idx = c["action"], g["idx"]
        path = pt.PACK / "action" / f"{action}_{idx}.png"
        rgba = np.array(Image.open(path).convert("RGBA"))
        mask = (rgba[:, :, 3] >= pt.ALPHA_FLOOR).astype(np.uint8)
        hit = None
        for tip, r_star, area, pd in pt.find_candidates(mask):
            ys, xs = np.nonzero(tip)
            if abs(int(xs.min()) - g["x"]) <= 2 and abs(int(ys.min()) - g["y"]) <= 2 \
                    and abs(area - g["area"]) <= 2:
                hit = (tip, r_star, area, pd, int(xs.min()), int(ys.min()))
                break
        if hit is None:
            skip_log.append(f"#{cid} {action}_{idx} ({g['x']},{g['y']}) a{g['area']} 目标不存在（已清过）")
            continue
        tip, r_star, area, pd, tx, ty = hit
        # ⛔⛔ 实体侵入守卫（2026-09-29 pat_3/15 事故后加）：
        #   候选若是"实心块"（其像素到背景距离 > max_d），说明它是角色实体的一部分
        #   （发丝接缝/衣服边缘），不是碎屑 —— 切了就是削角色。实测 pat 那处 17px 块
        #   有 2 个像素 d=3.2（实体内部），而 29 处正常切除 max d 全 ≤2.0。
        _d = cv2.distanceTransform(mask, cv2.DIST_L2, 5)
        solid = int((_d[tip > 0] > args.max_d).sum())
        if solid > 0:
            skip_log.append(f"#{cid} {action}_{idx} ({tx},{ty}) a{area} → ⛔ 疑似实体"
                            f"（{solid} px 到背景距离 >{args.max_d}），拒切")
            print(f"⛔ #{cid} {action}_{idx} ({tx},{ty}) {area}px 有 {solid} px 落在实体内部 → 拒切")
            continue
        bak = BACKUP / action
        bak.mkdir(parents=True, exist_ok=True)
        if not (bak / path.name).exists():
            shutil.copy2(path, bak / path.name)
        cut = rgba.copy()
        cut[tip > 0, 3] = 0
        Image.fromarray(cut).save(path, optimize=True)
        touched.add((action, idx))
        cut_log.append(dict(cluster=cid, action=action, idx=idx, x=tx, y=ty,
                            area=area, r=r_star, gap=round(pd, 1)))
        print(f"✔ #{cid} {action}_{idx} ({tx},{ty}) {area}px r*={r_star} 悬空={pd:.1f}px")

        ys, xs = np.nonzero(tip)
        x0, y0 = max(0, xs.min() - PAD), max(0, ys.min() - PAD)
        x1, y1 = min(rgba.shape[1], xs.max() + PAD), min(rgba.shape[0], ys.max() + PAD)
        panel = Image.new("RGB", ((x1 - x0) * ZOOM * 2 + 30, (y1 - y0) * ZOOM + 30), (255, 255, 255))
        for side, arr in ((0, rgba), (1, cut)):
            crop = Image.fromarray(arr[y0:y1, x0:x1]).resize(((x1 - x0) * ZOOM, (y1 - y0) * ZOOM), Image.NEAREST)
            bg = Image.new("RGB", crop.size, (255, 255, 255))
            d = ImageDraw.Draw(bg)
            for yy in range(0, bg.height, 8):
                for xx in range(0, bg.width, 8):
                    if (xx // 8 + yy // 8) % 2 == 0:
                        d.rectangle([xx, yy, xx + 7, yy + 7], fill=(212, 212, 212))
            bg.paste(crop, (0, 0), crop)
            panel.paste(bg, (side * ((x1 - x0) * ZOOM + 30), 20))
        ImageDraw.Draw(panel).text(
            (4, 4), f"#{cid} {action}_{idx} ({tx},{ty}) {area}px  L=原图 R=已切", fill=(0, 0, 0))
        panel.save(CROPDIR / f"cluster{cid:03d}_{action}_{idx:02d}_x{tx}_y{ty}_a{area}.png")

print(f"\n切除 {len(cut_log)} 处；跳过 {len(skip_log)} 处")
for s in skip_log:
    print("  " + s)

print("\n=== 残余清理（动过刀的帧，只清 alpha≥4 的 <4px 组件）===")
for action, idx in sorted(touched):
    path = pt.PACK / "action" / f"{action}_{idx}.png"
    rgba = np.array(Image.open(path).convert("RGBA"))
    alpha = rgba[:, :, 3]
    num, labels, stats, _ = cv2.connectedComponentsWithStats(
        (alpha >= pt.ALPHA_FLOOR).astype(np.uint8), connectivity=8)
    small = [(int(stats[i, cv2.CC_STAT_AREA]), int(stats[i, cv2.CC_STAT_LEFT]),
              int(stats[i, cv2.CC_STAT_TOP])) for i in range(1, num)
             if int(stats[i, cv2.CC_STAT_AREA]) < 4]
    if not small:
        print(f"  {action}_{idx}: 无残余")
        continue
    for i in range(1, num):
        if int(stats[i, cv2.CC_STAT_AREA]) < 4:
            alpha[labels == i] = 0
    Image.fromarray(rgba).save(path, optimize=True)
    print(f"  {action}_{idx}: 清 {len(small)} 处 {small}")

# ⭐ 追加写历史（别覆盖：每轮都写同一个文件名会把上一轮记录吃掉 —— 踩过一次）
import datetime
rec = dict(ts=datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
           ids=ids, cut=cut_log, skip=skip_log, touched=sorted(touched))
with open(OUT / "cluster_cut_history.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
Path(OUT / "cluster_cut_log_latest.json").write_text(
    json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"日志已追加到 cluster_cut_history.jsonl（本轮 {len(cut_log)} 处）")
print("\n完成")
