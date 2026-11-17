#!/usr/bin/env python3
"""半岛碎块探测（只读，不改任何素材）

原理：腐蚀半径 r 会断开宽度 <2r 的"脖子"。碎块从主体分离出来所需的最小半径 = 脖子粗细的度量。
- r*=1 断开：脖子 ≤2px（发丝级桥接），大概率是脏
- r*=2 断开：脖子 ≤4px，需目检
- r*≥3 才断开：基本是真实结构（呆毛/耳尖/尾巴），保留

输出：分档统计 + 放大标注裁切图 + HTML 目检页。
"""
import json
import re
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

PACK = Path("C:/Users/mercy/Desktop/LunaPet_v26-转身接线/_internal/packs/luna")
OUT = Path("C:/Users/mercy/WorkBuddy/2026-09-28-20-59-35/lunapet_v26_素材目检")
CROPDIR = OUT / "peninsula_crops"
if CROPDIR.exists():
    import shutil
    shutil.rmtree(CROPDIR)
CROPDIR.mkdir(parents=True, exist_ok=True)

ALPHA_FLOOR = 4
MAX_R = 4          # 探测到腐蚀半径 4
MAX_TIP_AREA = 400  # 只关心小碎块
ZOOM, PAD = 4, 26

cfg = json.loads((PACK / "pet.json").read_text(encoding="utf-8"))


def disk(r):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def frames_of(action):
    out = []
    for p in (PACK / "action").iterdir():
        if p.stem.startswith(action + "_") and p.stem[len(action) + 1:].isdigit():
            out.append((int(p.stem[len(action) + 1:]), p))
    out.sort()
    return out


def label_others(er):
    """返回 (主连通域 label, [(area, centroid, labels, stats, id), ...])"""
    num, labels, stats, cent = cv2.connectedComponentsWithStats(er, connectivity=8)
    if num <= 1:
        return labels, stats, cent, []
    areas = stats[1:, cv2.CC_STAT_AREA]
    main_id = int(np.argmax(areas)) + 1
    others = [(int(stats[i, cv2.CC_STAT_AREA]), (float(cent[i][0]), float(cent[i][1])), i)
              for i in range(1, num) if i != main_id]
    return labels, stats, cent, others


records = []
for action in cfg["actions"]:
    for idx, path in frames_of(action):
        rgba = np.array(Image.open(path).convert("RGBA"))
        mask = (rgba[:, :, 3] >= ALPHA_FLOOR).astype(np.uint8)

        levels = {}
        for r in range(1, MAX_R + 1):
            er = cv2.erode(mask, disk(r))
            levels[r] = (er,) + label_others(er)

        # 以最细半径 r=1 的分离块为种子，往上找它最早在哪一级出现（= 断颈半径 r*）
        seeds = levels[1][4]
        for area1, (cx, cy), _ in seeds:
            if area1 > MAX_TIP_AREA:
                continue
            r_star = 1
            for r in range(2, MAX_R + 1):
                hit = False
                for a, (x, y), _ in levels[r][4]:
                    if abs(x - cx) < 10 and abs(y - cy) < 10:
                        hit = True
                        break
                if not hit:
                    break
                r_star = r
            # 重建碎块在原始 mask 里的像素
            # 只保留与种子质心相近的那个连通域作为种子
            _, sl, ss, sc = cv2.connectedComponentsWithStats(
                levels[r_star][0], connectivity=8)
            best, bd = None, 1e9
            for i in range(1, int(ss.shape[0])):
                d = (sc[i][0] - cx) ** 2 + (sc[i][1] - cy) ** 2
                if d < bd:
                    bd, best = d, i
            if best is None:
                continue
            seed = (sl == best)
            grown = cv2.dilate(seed.astype(np.uint8), disk(r_star)) & mask
            n2, l2, s2, _ = cv2.connectedComponentsWithStats(grown, connectivity=8)
            tip = np.zeros_like(mask)
            for i in range(1, n2):
                if np.any((l2 == i) & seed):
                    tip |= (l2 == i).astype(np.uint8)
            tip_area = int(tip.sum())
            if tip_area > MAX_TIP_AREA:
                continue
            ys, xs = np.nonzero(tip)
            x, y = int(xs.min()), int(ys.min())
            w, h = int(xs.max() - x + 1), int(ys.max() - y + 1)
            records.append(dict(action=action, idx=idx, file=path.name, r_star=r_star,
                                tip_area=tip_area, x=x, y=y, w=w, h=h,
                                cx=float(cx), cy=float(cy)))
    print(f"{action} 扫描完成，累计候选 {len(records)}")

tiers = {1: [], 2: [], 3: [], 4: []}
for rec in records:
    tiers[rec["r_star"]].append(rec)
print("\n=== 分档统计（断颈半径 r* = 脖子粗细） ===")
for k in sorted(tiers):
    print(f"  r*={k}（脖子 ≤{2*k}px）: {len(tiers[k])} 处")
print(f"  合计 {len(records)} 处")

# ---- 标注图（每档最多 24 张）----
def checker(w, h, s=8):
    im = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(im)
    for yy in range(0, h, s):
        for xx in range(0, w, s):
            if (xx // s + yy // s) % 2 == 0:
                d.rectangle([xx, yy, xx + s - 1, yy + s - 1], fill=(210, 210, 210))
    return im

shown = []
for k in sorted(tiers):
    for rec in tiers[k][:24]:
        rgba = np.array(Image.open(PACK / "action" / rec["file"]).convert("RGBA"))
        x0 = max(0, rec["x"] - PAD); y0 = max(0, rec["y"] - PAD)
        x1 = min(rgba.shape[1], rec["x"] + rec["w"] + PAD)
        y1 = min(rgba.shape[0], rec["y"] + rec["h"] + PAD)
        crop = Image.fromarray(rgba[y0:y1, x0:x1]).resize(
            ((x1 - x0) * ZOOM, (y1 - y0) * ZOOM), Image.NEAREST)
        bg = checker(crop.width, crop.height)
        bg.paste(crop, (0, 0), crop)
        d = ImageDraw.Draw(bg)
        rx0, ry0 = (rec["x"] - x0) * ZOOM, (rec["y"] - y0) * ZOOM
        rx1, ry1 = rx0 + rec["w"] * ZOOM - 1, ry0 + rec["h"] * ZOOM - 1
        for wd in range(2):
            d.rectangle([rx0 - wd, ry0 - wd, rx1 + wd, ry1 + wd], outline=(255, 0, 0))
        name = f"r{k}_{rec['action']}_{rec['idx']:02d}_x{rec['x']}_y{rec['y']}_a{rec['tip_area']}.png"
        bg.save(CROPDIR / name)
        shown.append((rec, name))

sections = ""
for k in sorted(tiers):
    items = [(r, n) for r, n in shown if r["r_star"] == k]
    grouped = {}
    for rec, name in items:
        grouped.setdefault(rec["action"], []).append((rec, name))
    cells = ""
    for action, lst in grouped.items():
        frms = sorted(set(r["idx"] for r, _ in lst))
        cells += f"<h3>{action} <small>{len(lst)} 处 / 帧 {frms}</small></h3><div>"
        for rec, name in lst:
            cells += (f"<figure><img src='peninsula_crops/{name}'><figcaption>"
                      f"#{rec['idx']} ({rec['x']},{rec['y']}) {rec['tip_area']}px "
                      f"{rec['w']}×{rec['h']}</figcaption></figure>")
        cells += "</div>"
    verdict = {1: "脖子 ≤2px —— 发丝级桥接，几乎必然是脏，可自动切",
               2: "脖子 ≤4px —— 需逐处目检",
               3: "脖子 ≤6px —— 大概率是真实结构（呆毛/耳尖），建议保留",
               4: "脖子 ≤8px —— 基本是真实结构，保留"}[k]
    sections += (f"<h2>档位 r*={k}：{len(tiers[k])} 处 <small>{verdict}</small></h2>{cells}")

html = f"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<title>半岛碎块探测</title><style>
 body{{font-family:"Microsoft YaHei",sans-serif;max-width:1200px;margin:20px auto;background:#fafafa;color:#222}}
 div{{display:flex;flex-wrap:wrap;gap:10px}}
 figure{{margin:0;text-align:center}}
 img{{width:170px;border:1px solid #ddd;image-rendering:pixelated}}
 figcaption{{font-size:11px;color:#555}}
 h2 small,h3 small{{color:#777;font-weight:normal}}
</style></head><body>
<h1>半岛碎块探测（只读扫描，未改动任何素材）</h1>
<p>判据：腐蚀半径 r 会断开宽度 &lt;2r 的脖子；碎块分离所需最小半径 r* = 脖子粗细。
红框=候选碎块的包围盒（4× 放大，棋盘格=透明）。</p>
<table border=1 cellspacing=0 cellpadding=6>
<tr><th>档位</th><th>脖子宽度</th><th>数量</th><th>处置建议</th></tr>
{''.join(f"<tr><td>r*={k}</td><td>≤{2*k}px</td><td>{len(tiers[k])}</td><td>{['自动切（脏）','逐处目检','大概率真结构，保留','真结构，保留'][k-1]}</td></tr>" for k in sorted(tiers))}
</table>
{sections}</body></html>"""
(OUT / "peninsula_探测.html").write_text(html, encoding="utf-8")
print("\n目检页已生成")

# ⭐ 2026-09-29 补：导出候选表 JSON（cluster / flicker / rebuild_pages 都依赖它，
#    原脚本只出 HTML —— 缺这一步整条链会断在 FileNotFoundError）
import json as _json
# ⭐ 2026-09-29 补：cut_clusters 读的是 r["area"]，而 scan 内部字段叫 tip_area
#   → 直接加别名，否则下游 KeyError: 'area'
for _r in records:
    _r.setdefault("area", _r.get("tip_area"))
_js = _json.dumps(records, ensure_ascii=False, indent=1, default=str)
(OUT / "peninsula_stats_full.json").write_text(_js, encoding="utf-8")
(OUT.parent / "peninsula_stats_full.json").write_text(_js, encoding="utf-8")
print(f"候选表 JSON 已导出：{len(records)} 条")
