#!/usr/bin/env python3
"""按 Ronny 点名的坐标精确切除半岛碎块（不是规则批量，是定点手术）

目标签名：(动作, 帧号, bbox 左上角 x, y, 面积)
动刀前字节级备份到素材包外；切后复扫确认目标已消失；产出 4× 前后标注对比。
"""
import importlib.util
import json
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

spec = importlib.util.spec_from_file_location("pt", "peninsula_trial.py")
pt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pt)

OUT = Path("C:/Users/mercy/WorkBuddy/2026-09-28-20-59-35/lunapet_v26_素材目检")
BACKUP = OUT / "backup_before_peninsula_cut"
CROPDIR = OUT / "peninsula_cut_结果"
CROPDIR.mkdir(parents=True, exist_ok=True)

TARGETS = [
    ("idle", 1, 333, 174, 5),
    ("idle", 4, 332, 173, 5),
    ("idle", 4, 291, 202, 5),
    ("pat", 3, 299, 236, 17),
]

ZOOM, PAD = 5, 34


def checker(w, h, s=8):
    im = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(im)
    for yy in range(0, h, s):
        for xx in range(0, w, s):
            if (xx // s + yy // s) % 2 == 0:
                d.rectangle([xx, yy, xx + s - 1, yy + s - 1], fill=(212, 212, 212))
    return im


done = []
for action, idx, tx, ty, tarea in TARGETS:
    path = pt.PACK / "action" / f"{action}_{idx}.png"
    rgba = np.array(Image.open(path).convert("RGBA"))
    mask = (rgba[:, :, 3] >= pt.ALPHA_FLOOR).astype(np.uint8)
    cands = pt.find_candidates(mask)

    hit = None
    for tip, r_star, area, pd in cands:
        ys, xs = np.nonzero(tip)
        if int(xs.min()) == tx and int(ys.min()) == ty and area == tarea:
            hit = (tip, r_star, area, pd)
            break
    if hit is None:
        print(f"⛔ 未命中：{action}_{idx} ({tx},{ty}) a{tarea}")
        continue

    tip, r_star, area, pd = hit
    # 备份原字节
    bak = BACKUP / action
    bak.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, bak / path.name)

    cut = rgba.copy()
    cut[tip > 0, 3] = 0
    Image.fromarray(cut).save(path, optimize=True)

    # 复扫验证
    mask2 = (cut[:, :, 3] >= pt.ALPHA_FLOOR).astype(np.uint8)
    cands2 = pt.find_candidates(mask2)
    still = any(int(np.nonzero(t)[1].min()) == tx and int(np.nonzero(t)[0].min()) == ty
                and a == tarea for t, _, a, _ in cands2)
    print(f"{action}_{idx} ({tx},{ty}) a{area} r*={r_star} 悬空={pd:.1f}px → "
          f"已切 {int(tip.sum())}px，复扫仍在={still}")

    ys, xs = np.nonzero(tip)
    x0 = max(0, xs.min() - PAD); y0 = max(0, ys.min() - PAD)
    x1 = min(rgba.shape[1], xs.max() + PAD); y1 = min(rgba.shape[0], ys.max() + PAD)
    panel = Image.new("RGB", ((x1 - x0) * ZOOM * 2 + 30, (y1 - y0) * ZOOM + 30), (255, 255, 255))
    for side, arr in ((0, rgba), (1, cut)):
        crop = Image.fromarray(arr[y0:y1, x0:x1]).resize(
            ((x1 - x0) * ZOOM, (y1 - y0) * ZOOM), Image.NEAREST)
        bg = checker(crop.width, crop.height)
        bg.paste(crop, (0, 0), crop)
        panel.paste(bg, (side * ((x1 - x0) * ZOOM + 30), 20))
    d = ImageDraw.Draw(panel)
    d.text((4, 4), f"{action}_{idx} ({tx},{ty}) {area}px r*={r_star}  L=原图 R=已切后", fill=(0, 0, 0))
    name = f"{action}_{idx:02d}_x{tx}_y{ty}_a{area}.png"
    panel.save(CROPDIR / name)
    done.append((action, idx, tx, ty, area, still, name))

print(f"\n完成 {len(done)}/4，备份在 {BACKUP}")
