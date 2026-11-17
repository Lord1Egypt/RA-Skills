#!/usr/bin/env python3
"""跨帧聚类：把 519 处半岛候选归并成"同一处在不同帧的重复出现"

几何判据证明无法区分碎屑/发丝（同签名），所以流程改为：
  聚类 → 每簇看一次（附"出现在 N/M 帧"）→ 点名 → 整簇一起切（保证帧间一致）
"""
import importlib.util
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

spec = importlib.util.spec_from_file_location("pt", "peninsula_trial.py")
pt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pt)

OUT = Path("C:/Users/mercy/WorkBuddy/2026-09-28-20-59-35/lunapet_v26_素材目检")
CROPDIR = OUT / "peninsula_clusters"
if CROPDIR.exists():
    import shutil
    shutil.rmtree(CROPDIR)
CROPDIR.mkdir(parents=True, exist_ok=True)

LINK = 8          # 跨帧聚类半径（px）
ZOOM, PAD = 4, 26

_sf = OUT.parent / peninsula_stats_full.json
if not _sf.exists():
    _sf = OUT / peninsula_stats_full.json      # ⭐ 兜底：scan 也可能写在 OUT 下
rows = json.loads(_sf.read_text(encoding=utf-8))
cfg = json.loads((pt.PACK / "pet.json").read_text(encoding="utf-8"))

by_action = defaultdict(list)
for r in rows:
    by_action[r["action"]].append(r)

clusters = []
for action, items in by_action.items():
    unvisited = list(items)
    while unvisited:
        seed = unvisited.pop(0)
        group = [seed]
        changed = True
        while changed:
            changed = False
            for cand in unvisited[:]:
                for g in group:
                    if g["idx"] == cand["idx"]:
                        continue      # 同一帧里的不同碎块不并簇
                    d = ((g["x"] - cand["x"]) ** 2 + (g["y"] - cand["y"]) ** 2) ** 0.5
                    if d <= LINK:
                        group.append(cand)
                        unvisited.remove(cand)
                        changed = True
                        break
        nframes = len(set(g["idx"] for g in group))
        clusters.append(dict(action=action, group=group, nframes=nframes,
                             total=pt  and len(group)))

clusters.sort(key=lambda c: -c["nframes"])
print(f"候选 {len(rows)} 处 → 归并成 {len(clusters)} 簇")
bucket = defaultdict(int)
for c in clusters:
    bucket[c["nframes"]] += 1
print("每簇跨帧数分布（出现帧数: 簇数）:", dict(sorted(bucket.items())))


def checker(w, h, s=8):
    im = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(im)
    for yy in range(0, h, s):
        for xx in range(0, w, s):
            if (xx // s + yy // s) % 2 == 0:
                d.rectangle([xx, yy, xx + s - 1, yy + s - 1], fill=(212, 212, 212))
    return im


cards = ""
for ci, c in enumerate(clusters):
    action = c["action"]
    rep = max(c["group"], key=lambda g: g["area"])
    path = pt.PACK / "action" / f"{action}_{rep['idx']}.png"
    rgba = np.array(Image.open(path).convert("RGBA"))
    x0 = max(0, rep["x"] - PAD); y0 = max(0, rep["y"] - PAD)
    x1 = min(rgba.shape[1], rep["x"] + rep["w"] + PAD)
    y1 = min(rgba.shape[0], rep["y"] + rep["h"] + PAD)
    crop = Image.fromarray(rgba[y0:y1, x0:x1]).resize(
        ((x1 - x0) * ZOOM, (y1 - y0) * ZOOM), Image.NEAREST)
    bg = checker(crop.width, crop.height)
    bg.paste(crop, (0, 0), crop)
    d = ImageDraw.Draw(bg)
    rx0, ry0 = (rep["x"] - x0) * ZOOM, (rep["y"] - y0) * ZOOM
    for wd in range(2):
        d.rectangle([rx0 - wd, ry0 - wd,
                     rx0 + rep["w"] * ZOOM - 1 + wd, ry0 + rep["h"] * ZOOM - 1 + wd],
                    outline=(255, 0, 0))
    name = f"c{ci:03d}_{action}_f{rep['idx']:02d}_n{c['nframes']}.png"
    bg.save(CROPDIR / name)
    frames = sorted(set(g["idx"] for g in c["group"]))
    areas = sorted(set(g["area"] for g in c["group"]))
    cards += (f"<figure><img src='peninsula_clusters/{name}'><figcaption>"
              f"<b>#{ci}</b> {action} · 出现 {c['nframes']} 帧 / 共 {c['total']} 处<br>"
              f"面积 {areas} · 帧 {frames[:14]}{'…' if len(frames) > 14 else ''}</figcaption></figure>\n")

html = f"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<title>半岛候选 · 跨帧聚类目检</title><style>
 body{{font-family:"Microsoft YaHei",sans-serif;max-width:1200px;margin:20px auto;background:#fafafa;color:#222;line-height:1.6}}
 div.row{{display:flex;flex-wrap:wrap;gap:14px}}
 figure{{margin:0;text-align:center;width:230px}}
 img{{width:220px;border:1px solid #ddd;image-rendering:pixelated;background:#fff}}
 figcaption{{font-size:11px;color:#444;text-align:left}}
</style></head><body>
<h1>半岛候选 · 跨帧聚类（{len(clusters)} 簇 / 原 {len(rows)} 处）</h1>
<p>几何判据已实测无效（碎屑与发丝细尖签名完全相同：3×3、填充 0.56、接触 5px）。
所以改成：<b>聚类 → 每簇看一次 → 点名 → 整簇一起切</b>。整簇切的好处是帧间一致，
不会切了这帧漏了那帧造成闪动。</p>
<p>红框=该簇代表帧的碎块位置（4× 放大）。标注里的「出现 N 帧」= 这一处在该动作的 N 个帧里重复出现。</p>
<div class="row">
{cards}
</div></body></html>"""
(OUT / "半岛候选_跨帧聚类.html").write_text(html, encoding="utf-8")
print("目检页已生成：半岛候选_跨帧聚类.html")
