#!/usr/bin/env python3
"""闪烁分析 v3（精确版）：用碎屑自己的像素当探针

v2 的缺陷：delta 按整块 bbox 统计不透明像素 → 腿/尾巴摆过该区域也会算成"闪"（假阳性）。
v3 判据：
  1. 取碎屑**自己的像素掩码**（残留未切的簇：从当前文件重算；已动过刀的帧：从包外备份重算）
  2. 拿这批像素当探针，逐帧去查：同一批坐标在该帧里有多少是不透明的
  3. on  = 它自己出现的帧里，探针像素的不透明数（≈ 碎屑面积）
     off = 其余帧里，同一批探针像素的不透明数（中位）
     delta = on - off  ← 播放时这处"有→无"的可见变化量
  delta ≥ 4px → 会闪；1~3 → 轻微；≤0 → 不闪（那批像素在别的帧被身体占着，看不出开关）
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
BACKUP = OUT / "backup_before_peninsula_cut"
CROPDIR = OUT / "peninsula_flicker"
if CROPDIR.exists():
    import shutil
    shutil.rmtree(CROPDIR)
CROPDIR.mkdir(parents=True, exist_ok=True)
LINK = 8

cfg = json.loads((pt.PACK / "pet.json").read_text(encoding="utf-8"))
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

# 已切过的帧（含在第1/2/3/4批里切过的）→ 探针要从备份取
CUT_TOUCHED = {("idle", 1), ("idle", 4), ("idle", 18), ("idle", 21), ("pat", 3), ("pat", 15),
               ("land_settle", 0), ("land_settle", 1), ("land_settle", 2), ("land_settle", 13),
               ("walk", 9), ("walk", 10), ("walk", 22), ("idle", 8), ("idle", 14),
               ("idle", 10), ("idle", 12), ("fall", 1), ("fall", 13), ("land", 0), ("land", 4),
               ("pat", 4), ("pat", 14), ("walk", 6), ("walk", 15), ("walk", 14), ("walk", 20),
               ("walk", 17), ("land_settle", 7)}
# 备份里存在的帧都要用备份（备份＝原始字节）
for a, i in [("idle", f) for f in (1, 4, 18, 21)] + [("pat", f) for f in (3, 15, 4, 14, 7, 11)] + \
             [("land_settle", f) for f in (0, 1, 2, 13, 7)] + [("walk", f) for f in (9, 10, 22, 6, 15, 14, 20, 17)] + \
             [("idle", f) for f in (8, 14, 10, 12)] + [("fall", f) for f in (1, 13)] + [("land", f) for f in (0, 4)]:
    if (BACKUP / a / f"{a}_{i}.png").exists():
        CUT_TOUCHED.add((a, i))


def mask_center(m):
    """轮廓 bbox 中心，用作运动配准点"""
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return (0.0, 0.0)
    return ((xs.min() + xs.max()) / 2.0, (ys.min() + ys.max()) / 2.0)


def load_mask(action, idx):
    """优先用备份（原始态）算探针 —— 这样能精确拿到被切掉的碎屑形状"""
    p = BACKUP / action / f"{action}_{idx}.png"
    if not p.exists():
        p = pt.PACK / "action" / f"{action}_{idx}.png"
    return (np.array(Image.open(p).convert("RGBA"))[:, :, 3] >= pt.ALPHA_FLOOR)


analysis = []
for action in cfg["actions"]:
    N = int(cfg["actions"][action]["frames"])
    curr, base = {}, {}
    for f in range(N):
        p = pt.PACK / "action" / f"{action}_{f}.png"
        if p.exists():
            curr[f] = (np.array(Image.open(p).convert("RGBA"))[:, :, 3] >= pt.ALPHA_FLOOR)
            base[f] = load_mask(action, f)

    for ci, c in enumerate(clusters):
        if c["action"] != action:
            continue
        # 判定该簇是否还有未切成员（在当前文件里严格匹配存在）
        live = []
        for g in c["group"]:
            f = g["idx"]
            if f in curr and curr[f][g["y"]:g["y"] + g["h"], g["x"]:g["x"] + g["w"]].any():
                live.append(g)
        if not live:
            continue

        # 探针像素：优先用 live 成员（残留的就是要判断的），从基线态重算它的 tip 掩码
        probe = np.zeros(curr[list(curr)[0]].shape, dtype=bool)
        g0 = live[0]
        src = base[g0["idx"]]
        cands = pt.find_candidates(src.astype(np.uint8))
        for tip, r_star, area, pd in cands:
            ys, xs = np.nonzero(tip)
            if abs(int(xs.min()) - g0["x"]) <= 2 and abs(int(ys.min()) - g0["y"]) <= 2:
                probe |= (tip > 0)
                break
        if not probe.any():
            continue

        own = sorted(set(g["idx"] for g in live))
        # 运动补偿：以轮廓中心为配准点，把探针平移到目标帧
        pys, pxs = np.nonzero(probe)
        cx0, cy0 = mask_center(curr[g0["idx"]])
        own_px, off_px = [], []
        for f, m in curr.items():
            cx, cy = mask_center(m)
            dx, dy = int(round(cx - cx0)), int(round(cy - cy0))
            xs2, ys2 = pxs + dx, pys + dy
            ok = (xs2 >= 0) & (xs2 < m.shape[1]) & (ys2 >= 0) & (ys2 < m.shape[0])
            n = int(m[ys2[ok], xs2[ok]].sum()) if ok.any() else 0
            (own_px if f in own else off_px).append(n)
        on_med = float(np.median(own_px))
        off_med = float(np.median(off_px)) if off_px else 0.0
        delta = on_med - off_med
        probe_area = int(probe.sum())
        ys, xs = np.nonzero(probe)
        bx0, by0, bx1, by1 = int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1

        if not off_px or len(own) >= N:
            kind, risk = "常驻（不闪）", 4
            delta = 0.0
        elif delta >= 4:
            contig = all(b - a == 1 for a, b in zip(own, own[1:]))
            if len(own) == 1:
                kind, risk = "单帧闪", 2
            elif contig:
                kind, risk = "短暂冒头", 3
            else:
                kind, risk = "闪烁（散点开关）", 1
        elif delta >= 1:
            kind, risk = "轻微（1~3px）", 5
        else:
            kind, risk = "不闪（被占住）", 6

        analysis.append(dict(id=ci, action=action, N=N, own=own, n_own=len(own),
                             on=round(on_med, 1), off=round(off_med, 1), delta=round(delta, 1),
                             probe=probe_area, kind=kind, risk=risk,
                             remain=len(live), total=len(c["group"]),
                             x0=bx0, y0=by0, x1=bx1, y1=by1))

analysis.sort(key=lambda a: (a["risk"], -a["delta"]))
from collections import Counter
print(f"剩余未清簇 {len(analysis)} 个")
print(dict(Counter(a["kind"] for a in analysis)))
print(f"\n会闪（delta≥4px）: {sum(1 for a in analysis if a['risk'] <= 3)} 簇")
print("按动作:", dict(Counter(a["action"] for a in analysis if a["risk"] <= 3)))


def checker(w, h, s=8):
    im = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(im)
    for yy in range(0, h, s):
        for xx in range(0, w, s):
            if (xx // s + yy // s) % 2 == 0:
                d.rectangle([xx, yy, xx + s - 1, yy + s - 1], fill=(212, 212, 212))
    return im


def panel_for(a, zoom=6, pad=20):
    f_on = a["own"][0]
    offs = [f for f in range(a["N"]) if f not in a["own"]]
    f_off = min(offs, key=lambda f: abs(f - f_on)) if offs else None
    tiles = []
    for f, tag in ((f_on, "有碎屑"), (f_off, "同位置空")):
        if f is None:
            continue
        rgba = np.array(Image.open(pt.PACK / "action" / f"{a['action']}_{f}.png").convert("RGBA"))
        cx0, cy0 = max(0, a["x0"] - pad), max(0, a["y0"] - pad)
        cx1, cy1 = min(rgba.shape[1], a["x1"] + pad), min(rgba.shape[0], a["y1"] + pad)
        crop = Image.fromarray(rgba[cy0:cy1, cx0:cx1]).resize(
            ((cx1 - cx0) * zoom, (cy1 - cy0) * zoom), Image.NEAREST)
        bg = checker(crop.width, crop.height)
        bg.paste(crop, (0, 0), crop)
        d = ImageDraw.Draw(bg)
        rx0, ry0 = (a["x0"] - cx0) * zoom, (a["y0"] - cy0) * zoom
        col = (255, 0, 0) if tag == "有碎屑" else (0, 110, 255)
        for wd in range(2):
            d.rectangle([rx0 - wd, ry0 - wd, (a["x1"] - cx0) * zoom + wd - 1,
                         (a["y1"] - cy0) * zoom + wd - 1], outline=col)
        d.text((4, 4), f"帧{f} {tag}", fill=col)
        tiles.append(bg)
    if not tiles:
        return None
    W = sum(t.width for t in tiles) + 20 * (len(tiles) - 1)
    H = max(t.height for t in tiles) + 26
    out = Image.new("RGB", (W, H), (255, 255, 255))
    xx = 0
    for t in tiles:
        out.paste(t, (xx, 24))
        xx += t.width + 20
    ImageDraw.Draw(out).text(
        (4, 4), f"#{a['id']} {a['kind']} · {a['action']} · 帧{a['own']} / 共{a['N']} · 差 {a['delta']}px",
        fill=(0, 0, 0))
    return out


name_map = {}
for a in analysis:
    p = panel_for(a)
    if p is None:
        continue
    nm = f"{a['id']:03d}_{a['action']}_d{a['delta']}.png"
    p.save(CROPDIR / nm)
    name_map[a["id"]] = nm

SEC = (("🔴 闪烁（散点开关）—— 优先切", 1),
       ("🟠 单帧闪 —— 只冒一帧", 2),
       ("🟡 短暂冒头 —— 连续几帧后消失", 3),
       ("⚪ 轻微（差 1~3px，基本看不出）", 5),
       ("⚪ 不闪（碎屑像素在别的帧被身体占住）", 6),
       ("⚪ 常驻（全程都在）", 4))
sections = ""
for label, risk in SEC:
    grp = [a for a in analysis if a["risk"] == risk and a["id"] in name_map]
    if not grp:
        continue
    cells = "".join(
        (f"<figure class='wide'><img src='peninsula_flicker/{name_map[a['id']]}'>"
         f"<figcaption>#{a['id']} · 出现帧 {a['own']} / 共 {a['N']} 帧 · 碎屑 {a['probe']}px，"
         f"同位置在其他帧还有 {a['off']}px → 差 {a['delta']}px · 剩余 {a['remain']}/{a['total']}</figcaption></figure>")
        for a in grp[:36])
    sections += f"<h2>{label} —— {len(grp)} 簇</h2><div class='row'>{cells}</div>\n"

tbl = "".join(
    f"<tr><td>#{a['id']}</td><td>{a['kind']}</td><td>{a['action']}</td><td>{a['own']} / {a['N']}</td>"
    f"<td>{a['probe']}</td><td>{a['off']}</td><td><b>{a['delta']}</b></td><td>{a['remain']}/{a['total']}</td></tr>"
    for a in analysis if a["risk"] <= 3)

html = f"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8"><title>半岛候选 · 哪些会闪</title>
<style>
 body{{font-family:"Microsoft YaHei",sans-serif;max-width:1280px;margin:20px auto;background:#fafafa;color:#222;line-height:1.6}}
 div.row{{display:flex;flex-wrap:wrap;gap:14px}} figure{{margin:0}} figure.wide img{{width:1150px}}
 img{{border:1px solid #ddd;background:#fff}} figcaption{{font-size:11px;color:#444}}
 table{{border-collapse:collapse;background:#fff;font-size:12px}} td,th{{border:1px solid #ccc;padding:3px 8px}} th{{background:#eee}}
 .hint{{background:#fff;border-left:4px solid #08c;padding:8px 12px}}
</style></head><body>
<h1>剩余半岛候选 · 哪些会闪（{len(analysis)} 簇）</h1>
<p class="hint"><b>怎么算的</b>：拿碎屑<b>自己的像素</b>当探针，逐帧去查同一批坐标在该帧里有多少是不透明的。<br>
它出现的帧记 on（≈碎屑面积），其余帧记 off —— <b>delta 就是播放时这处"有→无"的可见变化量</b>。<br>
delta ≥ 4px 才会被看出来；≤3px 基本看不出（那批像素在别的帧被别人占着）。<br>
⚠️ 只统计碎屑像素本身，所以"腿摆过此处"这种真实动画位移不会被算成闪。</p>
<p><b>结论：{len(analysis)} 个剩余簇里，{sum(1 for a in analysis if a['risk'] <= 3)} 个会闪</b>
（闪烁 {sum(1 for a in analysis if a['risk'] == 1)} · 单帧闪 {sum(1 for a in analysis if a['risk'] == 2)} · 短暂冒头 {sum(1 for a in analysis if a['risk'] == 3)}），
其余 {sum(1 for a in analysis if a['risk'] >= 4)} 个看不出。</p>
<h2>会闪的清单（按差值降序）</h2>
<table><tr><th>簇</th><th>类型</th><th>动作</th><th>出现帧/总帧</th><th>碎屑px</th><th>同位置其余帧px</th><th>差值</th><th>剩余</th></tr>
{tbl}</table>
{sections}
</body></html>"""
(OUT / "半岛闪烁风险.html").write_text(html, encoding="utf-8")
Path("flicker_analysis.json").write_text(json.dumps(analysis, ensure_ascii=False, indent=1), encoding="utf-8")
print("\n页面：半岛闪烁风险.html")
print("\n最显眼的 10 个：")
for a in sorted([x for x in analysis if x["risk"] <= 3], key=lambda y: -y["delta"])[:10]:
    print(f"  #{a['id']:<4}{a['kind']:<10}{a['action']:<12}帧{a['own']}/{a['N']} 探针{a['probe']}px 其余{a['off']}px 差{a['delta']}px")
