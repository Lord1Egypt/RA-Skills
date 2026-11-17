#!/usr/bin/env python3
"""切除后必做：实体侵入审计（切完、残余清理完、复扫完之后跑）

removed = 备份mask(切除前) & ~当前mask；看被切掉的像素里有没有「实体内部」。
判据：到背景的距离 d。薄片/碎屑 d 小（1~2），实体内部 d 大（≥3）。
d≥3 → ⛔ 吃进了角色实体（头发/衣服），必须还原重来。

用法：python audit_cut_intrusion.py [--pack <素材包目录>] [--backup <备份目录>]
"""
import argparse
import importlib.util
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

# 定位同目录（或上级）的 peninsula 工具模块
here = Path(__file__).resolve().parent
_mod = None
for cand in (here / "peninsula_cut_trial.py", here / "peninsula_trial.py",
             here / ".." / "peninsula_cut_trial.py", here / ".." / "peninsula_trial.py"):
    if cand.exists():
        _mod = cand
        break
if _mod is None:
    raise SystemExit("找不到 peninsula_cut_trial.py / peninsula_trial.py")
spec = importlib.util.spec_from_file_location("pt", _mod)
pt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pt)

ap = argparse.ArgumentParser()
ap.add_argument("--backup", default=None, help="备份目录（默认 素材目检/backup_before_peninsula_cut）")
ap.add_argument("--deep", type=float, default=3.0, help="实体内部阈值（默认 3.0）")
args = ap.parse_args()

BACKUP = Path(args.backup) if args.backup else \
    Path("C:/Users/mercy/WorkBuddy/2026-09-28-20-59-35/lunapet_v26_素材目检/backup_before_peninsula_cut")

print(f"{'帧':<18}{'切掉px':>8}{'最大d':>7}{'d≥%.0f的px' % args.deep:>10}  判定")
rows = []
for a_dir in sorted(BACKUP.iterdir()):
    if not a_dir.is_dir():
        continue
    for bak in sorted(a_dir.glob("*.png")):
        cur = pt.PACK / "action" / bak.name
        if not cur.exists():
            continue
        b = np.array(Image.open(bak).convert("RGBA"))
        c = np.array(Image.open(cur).convert("RGBA"))
        bm = (b[:, :, 3] >= pt.ALPHA_FLOOR).astype(np.uint8)
        cm = (c[:, :, 3] >= pt.ALPHA_FLOOR).astype(np.uint8)
        removed = (bm > 0) & (cm == 0)
        n = int(removed.sum())
        if n == 0:
            continue
        d = cv2.distanceTransform(bm, cv2.DIST_L2, 5)
        dmax = float(d[removed].max())
        deep = int((d[removed] >= args.deep).sum())
        verdict = "⛔ 吃进实体 → 还原重来" if deep else \
                  ("· 贴边（max d=2）可接受" if dmax >= 2 else "✅ 只切薄片")
        rows.append((bak.name, n, dmax, deep, verdict))
        print(f"{bak.name:<18}{n:>8}{dmax:>7.1f}{deep:>10}  {verdict}")

bad = [r for r in rows if r[3] > 0]
print(f"\n审计 {len(rows)} 个被动过的帧 → 吃进实体 {len(bad)} 个")
if bad:
    print("⛔ 需还原：", ", ".join(r[0] for r in bad))
