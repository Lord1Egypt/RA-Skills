#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""adopt_images.py —— 收录图源并做印前校验，回填 content.json。

本脚本**不发任何网络请求、不需要任何 API key**。出图由 agent 自带的多模态能力
完成（见 references/imagery.md），本脚本只管拿到图之后的三件事：

  1. 裁切到图位的目标比例、缩放到理想像素、写入 300dpi 元数据
  2. 印前校验：亮度（过暗/近乎空白）、主色到品牌色板的距离
  3. 按 plan 里记录的 page_no / block_index 精确回填 content.json

Pillow 缺失时明写 checked:false 并跳过校验——宁可少做，也不假装做过。

用法：
  python adopt_images.py --plan ./images/image-plan.json --out ./images/gen \
      --adopt fig_0=/abs/path/a.png,fig_3=/abs/path/b.png \
      --patch-content ./content.json

  # 图源带右下角「AI生成」水印时的处理：先量内容边界，再挑留白够的那一条窄带裁
  # （底边优先——不动宽度；底边不够改裁右边；两条都不够则**拒绝裁**并报警，交人工重出）
  python adopt_images.py --plan ./images/image-plan.json --out ./images/gen \
      --adopt fig_0=/abs/path/a.png --crop-watermark

输出：
  <out>/<slot_id>.png
  <out>/manifest.json   每项的实际尺寸、主色距离、亮度、裁切记录、校验结论
  <content>.patched.json（给了 --patch-content 时）

命令里的 `python`：Windows 用 `python`，macOS/Linux 用 `python3`。
"""

import argparse
import json
import os
import re
import sys


# --------------------------------------------------------------------------
# 图像后处理（Pillow 可选）
# --------------------------------------------------------------------------

def _pil():
    try:
        from PIL import Image
        return Image
    except ImportError:
        return None


def hex_to_rgb(h):
    h = (h or "").lstrip("#")
    if len(h) != 6:
        return None
    try:
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return None


def content_bbox(im, tol=60, step=2):
    """量出内容（与左上角背景色差异明显的像素）的外接矩形。

    只用来回答一个问题：右下角的水印带能不能安全裁掉。
    采样式扫描（step=2）是为速度——1536×1024 全量扫描在慢机器上要好几秒。
    整幅近乎纯色时返回 None（无内容可测），调用方必须拒绝盲裁。
    """
    w, h = im.size
    px = im.convert("RGB").load()
    bg = px[3, 3]
    l, t, r, b = w, h, -1, -1
    for y in range(0, h, step):
        for x in range(0, w, step):
            c = px[x, y]
            if abs(c[0] - bg[0]) + abs(c[1] - bg[1]) + abs(c[2] - bg[2]) > tol:
                if x < l:
                    l = x
                if x > r:
                    r = x
                if y < t:
                    t = y
                if y > b:
                    b = y
    if r < 0:
        return None
    return (l, t, r, b)


def choose_watermark_crop(im, min_bottom=0.08, min_right=0.10, tol=60):
    """挑一条「盖得住右下角水印、又不切到内容」的窄带。

    实测：内置出图的「AI生成」水印固定在**右下角**，占高 ≤6%、占宽 ≤8%
    （1536×1024 实测 x 92.1%–99.3%、y 94.0%–98.9%）。所以裁底边或裁右边
    都能去掉它，关键是挑留白够的那一条：

      底部留白 ≥ min_bottom → 裁底边（首选：不动宽度，宽幅图更安全）
      否则右边留白 ≥ min_right → 裁右边
      两条都不够 → 不裁，明确报警，交人工重出或修图

    早期版本写死「右 10% + 底 9%」两条一起裁。实测这会把横向铺满的图切掉
    一截（四条通栏横条右边留白仅 7.9%，右裁 10% 必然切到横条端头），
    而竖幅图底部留白又经常不足（实测圆锥构图底留白 6.7%）。
    所以现在一律**先量后裁**，并在 manifest 里留下量到的四个边界值。
    """
    w, h = im.size
    bb = content_bbox(im, tol=tol)
    if bb is None:
        return im, {"chosen": None,
                    "note": "整幅近乎纯色，无法测量内容边界，拒绝盲裁水印"}
    l, t, r, b = bb
    bottom_margin = (h - 1 - b) / float(h)
    right_margin = (w - 1 - r) / float(w)
    info = {
        "content_bbox_pct": [round(l / w * 100, 1), round(t / h * 100, 1),
                             round(r / w * 100, 1), round(b / h * 100, 1)],
        "bottom_margin_pct": round(bottom_margin * 100, 1),
        "right_margin_pct": round(right_margin * 100, 1),
    }
    if bottom_margin >= min_bottom:
        info["chosen"] = "bottom"
        info["band_pct"] = round(min_bottom * 100, 1)
        return im.crop((0, 0, w, int(round(h * (1 - min_bottom))))), info
    if right_margin >= min_right:
        info["chosen"] = "right"
        info["band_pct"] = round(min_right * 100, 1)
        return im.crop((0, 0, int(round(w * (1 - min_right))), h)), info
    info["chosen"] = None
    info["note"] = ("右下角水印无法安全裁除：底部留白 %.1f%%（需 ≥%.0f%%）、"
                    "右边留白 %.1f%%（需 ≥%.0f%%），裁哪一条都会切到画面内容。"
                    "必须重出图（prompt 里要求右下角留空）或人工修图。"
                    % (bottom_margin * 100, min_bottom * 100,
                       right_margin * 100, min_right * 100))
    return im, info


def process_image(src_path, dst_path, task, dpi=300, crop_wm=False):
    """裁切到目标比例 → 落到理想像素 → 写 dpi 元数据 → 算主色与亮度。

    返回 dict；Pillow 缺失时返回 checked=False，绝不假装做过检查。
    """
    Image = _pil()
    rec = {"processed": False, "checked": False}
    if Image is None:
        rec["note"] = "未安装 Pillow，跳过后处理与校验（pip install pillow）"
        return rec

    im = Image.open(src_path)
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGBA" if im.mode == "P" and "transparency" in im.info else "RGB")
    im = im.convert("RGB")
    w0, h0 = im.size
    rec["source_px"] = [w0, h0]

    if crop_wm:
        before = im.size
        im, wm = choose_watermark_crop(im)
        rec["watermark_crop"] = wm
        if wm.get("chosen"):
            rec["watermark_cropped"] = "%dx%d -> %dx%d（裁%s边 %s%%，底留白 %s%% / 右留白 %s%%）" % (
                before[0], before[1], im.size[0], im.size[1],
                "底" if wm["chosen"] == "bottom" else "右", wm["band_pct"],
                wm["bottom_margin_pct"], wm["right_margin_pct"])
        else:
            rec.setdefault("warnings", []).append(wm.get("note", ""))
        w0, h0 = im.size

    target_aspect = task.get("aspect") or 1.0
    ideal = task.get("ideal_px") or [w0, h0]

    # 居中裁切到目标比例
    cur = w0 / float(h0)
    if abs(cur - target_aspect) > 0.01:
        if cur > target_aspect:
            nw = int(round(h0 * target_aspect))
            box = ((w0 - nw) // 2, 0, (w0 - nw) // 2 + nw, h0)
        else:
            nh = int(round(w0 / target_aspect))
            box = (0, (h0 - nh) // 2, w0, (h0 - nh) // 2 + nh)
        im = im.crop(box)
        rec["cropped_to_aspect"] = round(target_aspect, 3)

    tw, th = int(ideal[0]), int(ideal[1])
    if tw > 0 and th > 0:
        im = im.resize((tw, th), Image.LANCZOS)
    os.makedirs(os.path.dirname(dst_path) or ".", exist_ok=True)
    im.save(dst_path, dpi=(dpi, dpi))
    rec["processed"] = True
    rec["out_px"] = [im.size[0], im.size[1]]

    # --- 校验 ---
    # 1) 亮度：过低印出来发闷，过高则丢层次
    # 用 histogram 而不是 getdata：后者在 Pillow 14 会移除，前者也快得多
    hist = im.convert("L").histogram()
    total = float(sum(hist)) or 1.0
    mean_l = sum(i * c for i, c in enumerate(hist)) / total
    rec["luma_mean"] = round(mean_l, 1)
    # setdefault 而不是直接赋 []：裁水印阶段可能已经写过 warning，别把它抹掉
    rec.setdefault("warnings", [])
    if mean_l < 45:
        rec["warnings"].append("画面过暗（%.0f/255），印刷后易糊成一团黑" % mean_l)
    if mean_l > 232:
        rec["warnings"].append("画面接近纯白（%.0f/255），可能几乎是空白" % mean_l)

    # 2) 主色 vs 品牌色板：量化取主色，算到色板的最近距离
    small = im.resize((64, 64), Image.LANCZOS).quantize(colors=8, method=Image.MEDIANCUT)
    counts = sorted(small.convert("RGB").getcolors(64 * 64) or [], key=lambda x: -x[0])
    # 纸白/浅底不是「主色」。占比最大的量桶在矢量信息图（gen_diagram.py 输出，
    # bg=#FFFFFF）和带 tint 通栏的版式里永远是纸面本身，拿它去比品牌色板，距离
    # 必然 200+，于是每张图都报「不像一套的」——实测 2026-09-18 第 27 期六张图
    # 六张全警（图面用的明明就是 #A10F34 主色）。改为在**非纸面**量桶里取主色。
    # 「纸面」判据分两类，缺一不可：
    #   ① 极亮：三通道都 ≥240 —— 纸白本身；
    #   ② 近中性且亮：色差 ≤24 且均亮 ≥200 —— tint 底、分隔线这类浅灰调。
    #      这一条是为缩图副作用准备的：64×64 LANCZOS 会把 #F5F4F1 横带与纸白
    #      混成 #ECEAE8（min 232 已跌破 240，只靠①拦不住，实测 fig_4 因此漏网）。
    # 全被排除时（近乎空白的图）退回 counts[0]，那种图由 luma>232 告警负责。
    def _is_paper(rgb):
        mx, mn = max(rgb), min(rgb)
        return mn >= 240 or ((mx - mn) <= 24 and sum(rgb) / 3.0 >= 200)

    ink = [(n, c) for n, c in counts if not _is_paper(c)]
    dom = ink or counts
    if dom:
        rec["dominant_rgb"] = list(dom[0][1])
        rec["dominant_share"] = round(dom[0][0] / float(64 * 64), 3)
        if ink and ink[0][1] != counts[0][1]:
            rec["dominant_note"] = ("主色取自非纸面像素；纸白/浅底占比 %.3f 未计入"
                                    % (counts[0][0] / float(64 * 64)))

    spec_pal = [hex_to_rgb(c) for c in (task.get("palette") or [])]
    spec_pal = [c for c in spec_pal if c]
    if spec_pal and dom:
        tr = dom[0][1]
        dists = [sum((a - b) ** 2 for a, b in zip(tr, c)) ** 0.5 for c in spec_pal]
        rec["color_distance"] = round(min(dists), 1)
        # >100 说明这张图的调子和品牌色板基本无关
        if min(dists) > 100:
            rec["warnings"].append(
                "主色与品牌色板距离 %.0f（>100），视觉上不像一套的" % min(dists))

    rec["checked"] = True
    return rec


# --------------------------------------------------------------------------

def adopt_mode(args, plan):
    """收录 agent 出好的图，只做验收与回填。

    这一步的存在理由是：图如果绕开验收直接进底稿，尺寸不对、亮度过低、
    主色跑偏这三件事就只能等打样才发现。
    """
    pairs = []
    for item in args.adopt.split(","):
        item = item.strip()
        if not item or "=" not in item:
            continue
        sid, path = item.split("=", 1)
        pairs.append((sid.strip(), path.strip().strip('"').strip("'")))

    if not pairs:
        print("[ERROR] --adopt 格式应为 slot_id=/abs/path.png（多个用逗号分隔）",
              file=sys.stderr)
        return 2

    tasks = plan.get("tasks", [])
    by_id = {t["slot_id"]: t for t in tasks}
    dpi = plan.get("dpi", 300)
    palette = (plan.get("imagery_profile") or {}).get("palette") or []
    os.makedirs(args.out, exist_ok=True)

    manifest = []
    for sid, src in pairs:
        rec = {"slot_id": sid, "source_path": src, "adopted": True}
        if sid not in by_id:
            rec["error"] = "plan 里没有这个 slot_id（只允许 plan 已列出的图位）"
            rec["ok"] = False
            print("[FAIL] %s" % rec["error"])
            manifest.append(rec)
            continue
        if not os.path.exists(src):
            rec["error"] = "文件不存在：%s" % src
            rec["ok"] = False
            print("[FAIL] %s" % rec["error"])
            manifest.append(rec)
            continue
        t = dict(by_id[sid])
        t["palette"] = palette
        dst = os.path.join(args.out, sid + ".png")
        rec.update(process_image(src, dst, t, dpi=dpi, crop_wm=args.crop_watermark))
        rec["ok"] = rec.get("processed", False)
        rec["dst"] = dst
        rec["role"] = t.get("role")
        for w in rec.get("warnings", []):
            print("  [WARN] %s" % w)
        print("[ADOPT] %s -> %s px=%s luma=%s dist=%s" % (
            sid, dst, rec.get("out_px"), rec.get("luma_mean"), rec.get("color_distance")))
        manifest.append(rec)

    mp = os.path.join(args.out, "manifest.json")
    old = []
    if os.path.exists(mp):
        with open(mp, "r", encoding="utf-8") as f:
            old = json.load(f).get("items", [])
    with open(mp, "w", encoding="utf-8") as f:
        json.dump({"plan": args.plan, "dpi": dpi,
                   "items": [o for o in old if o["slot_id"] not in by_id] + manifest},
                  f, ensure_ascii=False, indent=2)

    ok = [m for m in manifest if m.get("ok")]
    fail = [m for m in manifest if m.get("error")]
    print("\nADOPT OK=%d FAIL=%d -> %s" % (len(ok), len(fail), mp))
    if args.patch_content and ok:
        n, n_caption = patch_content(args.patch_content, ok, tasks)
        print("patched %d 处（其中 %d 处同时剥掉了图注的「图位待补：」占位前缀）-> %s" % (
            n, n_caption, args.patch_content.replace(".json", ".patched.json")))
    return 0 if not fail else 1


# 「图位待补：」这类前缀是起草期写给自己的标记（表示此处缺图，待补）。
# 图一旦补上，标记就必须跟着消失——否则它会一路印到成品里。
# 实测：只回填 src 不清理图注时，成品 PDF 的图注是
# 「图位待补：香港数字资产监管框架示意（…三线分工）」，占位符直接付印。
# 前缀清单与 plan_images.topic_from_text() 保持一致，两边不得各写一套。
PLACEHOLDER_PREFIX = re.compile(r"^(图位待补|待补图|待补|占位|待确认)\s*[:：]\s*")


def patch_content(content_path, ok_items, tasks):
    """把图按精确索引回填进 content.json，产出 *.patched.json。

    回填靠 plan 里记录的 block_index / page_no 定位 —— 早期版本靠「第几个
    figure 块」重数匹配，因编号起点不一致而回填了 0 处，所以现在一律用索引。

    回填 figure 的 src 时**同时剥掉图注的「图位待补：」占位前缀**：这个前缀
    的含义正是「此处缺图」，图补上后它就成了过期标记，留着会印进成品。
    返回 (回填处数, 清理图注处数)。
    """
    patch = {m["slot_id"]: m["dst"] for m in ok_items}
    with open(content_path, "r", encoding="utf-8") as f:
        content = json.load(f)
    n = 0
    n_caption = 0
    for t in tasks:
        sid = t["slot_id"]
        if sid not in patch:
            continue
        page_no = t.get("page_no")
        bi = t.get("block_index")
        if page_no is None:
            continue
        pages = content.get("pages", [])
        if page_no >= len(pages):
            continue
        if sid.startswith("fig_") and bi is not None:
            blocks = pages[page_no].get("blocks", []) or []
            if bi < len(blocks) and blocks[bi].get("type") == "figure":
                blocks[bi]["src"] = patch[sid]
                n += 1
                cap = blocks[bi].get("caption") or ""
                if PLACEHOLDER_PREFIX.match(cap):
                    blocks[bi]["caption"] = PLACEHOLDER_PREFIX.sub("", cap).strip()
                    n_caption += 1
        elif sid.startswith("bg_p"):
            pages[page_no].setdefault("images", {})["bg"] = patch[sid]
            n += 1
        else:
            key = sid.split("_p")[0]
            if key in ("hero", "banner"):
                pages[page_no].setdefault("fields", {})[key] = patch[sid]
                n += 1
    out = content_path.replace(".json", ".patched.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    return n, n_caption


def main():
    ap = argparse.ArgumentParser(
        description="收录图源并做印前校验（不发请求、不需 API key）")
    ap.add_argument("--plan", required=True, help="image-plan.json")
    ap.add_argument("--adopt", required=True,
                    help="收录图片：slot_id=/abs/path.png，多个用逗号分隔")
    ap.add_argument("--out", required=True, help="输出目录")
    ap.add_argument("--crop-watermark", action="store_true",
                    help="去除右下角水印：先量内容边界，再裁留白够的那一条窄带"
                         "（底边 8%% 优先，其次右边 10%%；两条都不够则拒绝裁并报警）")
    ap.add_argument("--patch-content", help="把结果回填到 content.json")
    args = ap.parse_args()

    with open(args.plan, "r", encoding="utf-8") as f:
        plan = json.load(f)

    return adopt_mode(args, plan)


if __name__ == "__main__":
    sys.exit(main())
