#!/usr/bin/env python3
"""清除半岛切除留下的 1px 低 alpha 残余（只处理本次动过刀的帧）

现象：切掉半岛主块后，其周围 alpha 12~25 的低值像素被切断 → 变成新的 1px 孤岛。
纪律：切一刀必须复扫，发现新残渣当场清掉，不留"改一处带出新问题"。
"""
import importlib.util
from pathlib import Path

import numpy as np
import cv2
from PIL import Image

spec = importlib.util.spec_from_file_location("pt", "peninsula_trial.py")
pt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pt)

OUT = Path("C:/Users/mercy/WorkBuddy/2026-09-28-20-59-35/lunapet_v26_素材目检")
BACKUP = OUT / "backup_before_peninsula_cut"
MIN_AREA = 4          # alpha>=4 连通域面积 <4 → 孤岛（与 alpha-despeckle 口径一致）

# 本次动过刀的帧（备份已存在，不再重复备份）
TOUCHED = [("idle", 1), ("idle", 4), ("idle", 18), ("idle", 21), ("pat", 3), ("pat", 15)]

for action, idx in TOUCHED:
    path = pt.PACK / "action" / f"{action}_{idx}.png"
    rgba = np.array(Image.open(path).convert("RGBA"))
    alpha = rgba[:, :, 3]
    num, labels, stats, cent = cv2.connectedComponentsWithStats(
        (alpha >= pt.ALPHA_FLOOR).astype(np.uint8), connectivity=8)
    removed = []
    for i in range(1, num):
        area = int(stats[i, cv2.CC_STAT_AREA])
        if area < MIN_AREA:
            x = int(stats[i, cv2.CC_STAT_LEFT]); y = int(stats[i, cv2.CC_STAT_TOP])
            ma = float(alpha[labels == i].mean())
            removed.append((area, x, y, round(ma, 1)))
    if not removed:
        print(f"{action}_{idx}: 无残余")
        continue
    for area, x, y, ma in removed:
        pass
    for i in range(1, num):
        if int(stats[i, cv2.CC_STAT_AREA]) < MIN_AREA:
            alpha[labels == i] = 0
    Image.fromarray(rgba).save(path, optimize=True)
    print(f"{action}_{idx}: 清除 {len(removed)} 处残余 " +
          ", ".join(f"({x},{y}) {a}px α{ma}" for a, x, y, ma in removed))

# 复扫确认
print("\n=== 复扫（应为 0 处孤岛）===")
bad = 0
for action, idx in TOUCHED:
    path = pt.PACK / "action" / f"{action}_{idx}.png"
    alpha = np.array(Image.open(path).convert("RGBA"))[:, :, 3]
    num, labels, stats, _ = cv2.connectedComponentsWithStats(
        (alpha >= pt.ALPHA_FLOOR).astype(np.uint8), connectivity=8)
    small = [int(stats[i, cv2.CC_STAT_AREA]) for i in range(1, num)
             if int(stats[i, cv2.CC_STAT_AREA]) < MIN_AREA]
    print(f"  {action}_{idx}: 组件 {num-1} 个，其中 <4px 的 {len(small)} 个 {small}")
    bad += len(small)
print("复扫结果:", "全清" if bad == 0 else f"仍有 {bad} 处")
