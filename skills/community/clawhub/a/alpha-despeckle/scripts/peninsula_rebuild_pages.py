#!/usr/bin/env python3
"""重建两张页：① 聚类目检页（带实时剩余数）② 切除结果页（全部批次汇总）"""
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
LINK = 8

# ---- 1. 实时扫描当前状态 ----
cfg = json.loads((pt.PACK / "pet.json").read_text(encoding="utf-8"))
current = defaultdict(list)
for action in cfg["actions"]:
    frames = sorted(((int(p.stem[len(action) + 1:]), p) for p in (pt.PACK / "action").iterdir()
                     if p.stem.startswith(action + "_") and p.stem[len(action) + 1:].isdigit()))
    for idx, path in frames:
        mask = (np.array(Image.open(path).convert("RGBA"))[:, :, 3] >= pt.ALPHA_FLOOR).astype(np.uint8)
        for tip, r_star, area, pd in pt.find_candidates(mask):
            ys, xs = np.nonzero(tip)
            current[(action, idx)].append((int(xs.min()), int(ys.min()), area, r_star, round(pd, 1)))

# ---- 2. 基线聚类（编号与页面一致）----
rows = json.loads((OUT / "peninsula_stats_full.json").read_text(encoding="utf-8"))
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

def still_there(action, idx, x, y, area):
    for cx, cy, ca, _, _ in current.get((action, idx), []):
        if abs(cx - x) <= 2 and abs(cy - y) <= 2 and abs(ca - area) <= 2:
            return True
    return False

def checker(w, h, s=8):
    im = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(im)
    for yy in range(0, h, s):
        for xx in range(0, w, s):
            if (xx // s + yy // s) % 2 == 0:
                d.rectangle([xx, yy, xx + s - 1, yy + s - 1], fill=(212, 212, 212))
    return im

if CROPDIR.exists():
    import shutil
    shutil.rmtree(CROPDIR)
CROPDIR.mkdir(parents=True, exist_ok=True)

cards, cleared, pending = "", 0, 0
for ci, c in enumerate(clusters):
    action = c["action"]
    remain = [g for g in c["group"] if still_there(action, g["idx"], g["x"], g["y"], g["area"])]
    rep = max(remain or c["group"], key=lambda g: g["area"])
    path = pt.PACK / "action" / f"{action}_{rep['idx']}.png"
    rgba = np.array(Image.open(path).convert("RGBA"))
    x0, y0 = max(0, rep["x"] - 26), max(0, rep["y"] - 26)
    x1, y1 = min(rgba.shape[1], rep["x"] + rep["w"] + 26), min(rgba.shape[0], rep["y"] + rep["h"] + 26)
    crop = Image.fromarray(rgba[y0:y1, x0:x1]).resize(((x1 - x0) * 4, (y1 - y0) * 4), Image.NEAREST)
    bg = checker(crop.width, crop.height)
    bg.paste(crop, (0, 0), crop)
    d = ImageDraw.Draw(bg)
    if remain:      # 只给未清完的画红框
        rx0, ry0 = (rep["x"] - x0) * 4, (rep["y"] - y0) * 4
        for wd in range(2):
            d.rectangle([rx0 - wd, ry0 - wd, rx0 + rep["w"] * 4 - 1 + wd, ry0 + rep["h"] * 4 - 1 + wd],
                        outline=(255, 0, 0))
    name = f"c{ci:03d}_{action}_f{rep['idx']:02d}_rest{len(remain)}.png"
    bg.save(CROPDIR / name)
    frames = sorted(set(g["idx"] for g in c["group"]))
    areas = sorted(set(g["area"] for g in c["group"]))
    if not remain:
        cleared += 1
        cards += (f"<figure class='done'><img src='peninsula_clusters/{name}'>"
                  f"<figcaption><b>#{ci}</b> {action} · <span class='ok'>已清</span><br>"
                  f"面积{areas} · 帧{frames}</figcaption></figure>\n")
    else:
        pending += 1
        cards += (f"<figure><img src='peninsula_clusters/{name}'>"
                  f"<figcaption><b>#{ci}</b> {action} · 剩余 {len(remain)}/{len(c['group'])} 处<br>"
                  f"面积{areas} · 帧{frames[:14]}{'…' if len(frames) > 14 else ''}</figcaption></figure>\n")

html = f"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<title>半岛候选 · 跨帧聚类（带进度）</title><style>
 body{{font-family:"Microsoft YaHei",sans-serif;max-width:1220px;margin:20px auto;background:#fafafa;color:#222;line-height:1.6}}
 div.row{{display:flex;flex-wrap:wrap;gap:14px}}
 figure{{margin:0;text-align:center;width:230px}}
 img{{width:220px;border:1px solid #ddd;image-rendering:pixelated;background:#fff}}
 figure.done img{{border:2px solid #0a0;opacity:.55}}
 figcaption{{font-size:11px;color:#444;text-align:left}}
 .ok{{color:#070;font-weight:bold}} .hint{{background:#fff;border-left:4px solid #08c;padding:8px 12px}}
</style></head><body>
<h1>半岛候选 · 跨帧聚类（{len(clusters)} 簇，已清 {cleared} / 待裁决 {pending}）</h1>
<p class="hint">编号与首版页面<b>完全一致</b>（基于切除前的基线扫描），所以你手上的编号仍然有效。
绿框 + 半透明 = 该簇已全部清完；红框 = 该簇还有剩余（含剩余数量）。</p>
<p>已清的簇：#28 #40 #47 #52 #53 #55 #57 #63 #65 #67 #70 #72 #111 等（共 {cleared} 簇）。
红框细看仍是「细尖薄片」，判真假仍需你的眼睛 —— 几何判据已实测无效。</p>
<div class="row">
{cards}
</div></body></html>"""
(OUT / "半岛候选_跨帧聚类.html").write_text(html, encoding="utf-8")
print(f"聚类页重建完成：{len(clusters)} 簇，已清 {cleared}，剩余 {pending}")

# ---- 3. 结果页：全部批次汇总 ----
crops = sorted((OUT / "peninsula_cut_结果").glob("*.png"))
log2 = json.loads((OUT / "cluster_cut_log_latest.json").read_text(encoding="utf-8")) if (OUT / "cluster_cut_log_latest.json").exists() else {"cut": [], "skip": []}
log1 = json.loads((OUT / "cluster_cut_log.json").read_text(encoding="utf-8")) if (OUT / "cluster_cut_log.json").exists() else {"cut": [], "skip": []}
figs = "".join(f"<figure><img src='peninsula_cut_结果/{p.name}'><figcaption>{p.stem}</figcaption></figure>" for p in crops)
rows_html = ""
for rec in log1.get("cut", []) + log2.get("cut", []):
    if isinstance(rec, dict):
        cid = rec.get("cluster", rec.get("cid", "—"))
        rows_html += (f"<tr><td>#{cid}</td><td>{rec.get('action')}_{rec.get('idx')}</td>"
                      f"<td>({rec.get('x')},{rec.get('y')})</td><td>{rec.get('area')}px</td>"
                      f"<td>r*={rec.get('r')}</td><td>悬空 {rec.get('gap')}px</td></tr>")
    else:
        cid, action, idx, x, y, area, r, gap = rec
        rows_html += (f"<tr><td>#{cid}</td><td>{action}_{idx}</td><td>({x},{y})</td>"
                      f"<td>{area}px</td><td>r*={r}</td><td>悬空 {gap}px</td></tr>")

html2 = f"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8"><title>半岛切除 · 全部批次</title>
<style>
 body{{font-family:"Microsoft YaHei",sans-serif;max-width:1200px;margin:20px auto;background:#fafafa;color:#222;line-height:1.6}}
 img{{border:1px solid #ddd;background:#fff;width:250px}}
 div.row{{display:flex;flex-wrap:wrap;gap:10px}} figure{{margin:0;width:250px}}
 figcaption{{font-size:11px;color:#555;word-break:break-all}}
 table{{border-collapse:collapse;background:#fff;font-size:12px}} td,th{{border:1px solid #ccc;padding:3px 8px}} th{{background:#eee}}
</style></head><body>
<h1>半岛碎块切除 · 全部批次汇总</h1>
<p>共切除 <b>{len(crops)}</b> 处（含首批点名 4 处 + 对称帧副本 4 处 + 你点名的 13 个簇）。
每批切完都做了：字节级备份 → 严格匹配切除 → 残余清理 → 244 帧全量复扫（孤岛 0）。</p>
<table><tr><th>簇</th><th>帧</th><th>坐标</th><th>面积</th><th>断颈</th><th>悬空</th></tr>{rows_html}</table>
<h2>逐处前后对比（5× 放大，左原图 / 右已切）</h2>
<div class="row">{figs}</div>
</body></html>"""
(OUT / "半岛切除_结果.html").write_text(html2, encoding="utf-8")
print(f"结果页重建完成，收入 {len(crops)} 张对比图")
