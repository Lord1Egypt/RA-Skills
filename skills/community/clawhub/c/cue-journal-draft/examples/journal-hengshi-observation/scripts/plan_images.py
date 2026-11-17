#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""plan_images.py —— 由 StyleSpec + content.json 生成「配图计划」 image-plan.json。

配图是期刊底稿里最容易翻车的一环：AI 生成的图一旦出现人脸、错字、假 logo，
整本刊的可用性直接归零。所以这个脚本的第一职责不是「把所有空位填满」，
而是**判定哪些空位根本不该由 AI 生成**。

四类决策：
  skip   —— 不该配图（装饰线、色块、留白本身就是设计）
  reuse  —— 有真实素材（企业 logo、实拍、产品图、既有图表），必须优先用真的
  manual —— 需要图，但「这期要画什么」未知（样刊槽位天生属于这一类：
            样刊的图是它自己的内容，不能直接推导出新刊的主题）。
            这一类要打包去问用户，补到 manual 转成 gen 才动手。
  gen    —— 主题已明确且 AI 能安全生成（抽象意象、场景氛围、几何陪衬）

并且把 gen 条目按 consistency_group 分组：同组共用一张参考图做图生图，
这是保证「整本刊看起来是一套」的唯一可靠手段——逐张独立出图必然风格漂移。

用法：
  python plan_images.py --spec stylespec.json --content content.json \
      --out ./images --imagery imagery.json --dpi 300

输出：
  image-plan.json   配图计划（人可读、可改、可复核）
  image-plan.md     人类复核稿

命令里的 `python`：Windows 用 `python`，macOS/Linux 用 `python3`。
"""

import argparse
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict

# --------------------------------------------------------------------------
# 常量
# --------------------------------------------------------------------------

# 这些槽位角色不是「图片内容」，是版面疾患——用代码/CSS 画出来，不该去生成
NON_IMAGE_ROLES = ("decoration", "rule", "divider", "bullet")

# AI 配图的安全红线：这些内容一律不得出现在生成图里
HARD_NEGATIVE = (
    "text, letters, words, captions, watermark, signature, "
    "human faces, portraits, identifiable people, "
    "brand logo, company logo, trademark, QR code"
)

# 按用途给的默认负向提示
NEGATIVE_BY_ROLE = {
    "hero": HARD_NEGATIVE + ", cluttered background, low contrast",
    "cover": HARD_NEGATIVE + ", cluttered composition, busy background",
    "figure": HARD_NEGATIVE + ", decorative frame, drop shadow, 3d render artifact",
    "inline": HARD_NEGATIVE + ", busy background, heavy texture",
    "backcover": HARD_NEGATIVE + ", busy detail",
}

# 常见出图像素档位（长边优先）。用于把 mm 换算后的理想尺寸吸附到可提交档位。
# 本表只是吸附参考；不吸附也能出图，只是有些服务对非标准尺寸不友好。
SIZE_LADDER = [
    (512, 512), (768, 768), (1024, 1024),
    (1024, 1536), (1536, 1024),
    (1280, 720), (720, 1280),
    (1024, 768), (768, 1024),
    (2048, 2048),
]

DEFAULT_IMAGERY = {
    "style_anchor": "minimal, flat vector illustration, restrained palette, "
                    "generous negative space, editorial tone",
    "medium": "abstract editorial illustration",
    "palette": [],
    "avoid": [],
    "reference_image": "",
}


# --------------------------------------------------------------------------
# 工具
# --------------------------------------------------------------------------

def mm_to_px(mm, dpi):
    return int(round(mm * dpi / 25.4))


def to_mm(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def snap_size(w_px, h_px, max_px=2048):
    """把理想像素尺寸吸附到常见档位，保持长宽比方向不乱。

    不追求精确——配图是给排版用的，只要比例方向对、分辨率够，
    具体像素由排版时的 object-fit 兜底。
    """
    if w_px <= 0 or h_px <= 0:
        return 1024, 1024
    ratio = w_px / float(h_px)
    # 找最接近的候选
    best = None
    for cw, ch in SIZE_LADDER:
        c_ratio = cw / float(ch)
        cost = abs(math.log(ratio / c_ratio)) + abs(math.log((cw * ch) / float(w_px * h_px))) * 0.15
        if best is None or cost < best[0]:
            best = (cost, cw, ch)
    rw, rh = best[1], best[2]
    # 整体裁额度，别超出 provider 上限
    scale = min(1.0, max_px / float(max(rw, rh)))
    return max(256, int(rw * scale)), max(256, int(rh * scale))


def classify_slot(slot):
    """判定一个图片槽位的用途。返回 (role, decision, reason)。"""
    role = (slot.get("role_guess") or slot.get("role") or "unknown").lower()
    w = to_mm(slot.get("w_mm")) or 0
    h = to_mm(slot.get("h_mm")) or 0
    ratio = slot.get("page_ratio") or 0
    area = w * h
    recurring = bool(slot.get("recurring"))

    if role in NON_IMAGE_ROLES:
        return role, "skip", "装饰性元素，用矢量/CSS 绘制，不得生成"

    # 极小面积的元素多为 logo / 图标 / 二维码位——这些必须由真实素材提供，
    # 生成出来的假 logo 会让整本刊作废
    if area < 900:
        return role, "skip", "面积过小（<900mm²），属 logo/图标位，须用真实素材，禁止生成"

    # 满版：封面或整版分隔页 -> 通常是品牌底纹，优先复用真素材
    if ratio >= 0.95 and area > 20000:
        return "cover", "reuse", "满版整页：优先用既有品牌底纹/实拍；确无素材才转 gen"

    if role == "hero" or ratio >= 0.4:
        return "hero", "manual", "主视觉位：需本期主题，由人工指派后转 gen"
    return "inline", "manual", "文内配图：需本期主题，由人工指派后转 gen"


def read_json(path, default=None):
    if not path or not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# --------------------------------------------------------------------------
# 收集任务
# --------------------------------------------------------------------------

def collect_slot_tasks(spec, dpi, imagery, asset_index):
    """从 StyleSpec 的页面模板里收集复用频次高的槽位（去掉一次性的噪声）。"""
    tasks = []
    for tpl in spec.get("page_templates", []) or []:
        for slot in tpl.get("image_slots", []) or []:
            role, decision, reason = classify_slot(slot)
            w_mm, h_mm = to_mm(slot.get("w_mm")), to_mm(slot.get("h_mm"))
            if not w_mm or not h_mm:
                continue
            key = "%s|%s" % (role, snap_size(mm_to_px(w_mm, dpi), mm_to_px(h_mm, dpi))[0])
            tasks.append({
                "source": "slot",
                "slot_id": slot.get("id"),
                "template_id": tpl.get("id"),
                "role": role,
                "decision": decision,
                "reason": reason,
                "w_mm": round(w_mm, 1),
                "h_mm": round(h_mm, 1),
                "aspect": round(w_mm / h_mm, 3) if h_mm else 1.0,
                "recurring": bool(slot.get("recurring")),
                "group_key": key,
                "_asset": asset_index.get(role),
            })

    # 同一个 (role, 尺寸档) 只保留一条代表性任务，其余标为同组
    grouped = defaultdict(list)
    for t in tasks:
        grouped[t["group_key"]].append(t)
    out = []
    for i, (key, items) in enumerate(sorted(grouped.items(), key=lambda kv: -len(kv[1]))):
        rep = max(items, key=lambda x: (x["recurring"], x["w_mm"] * x["h_mm"]))
        rep["consistency_group"] = "G%d" % (i + 1)
        rep["occurrences"] = len(items)
        rep["representative_of"] = [x["slot_id"] for x in items][:12]
        out.append(rep)
    return out


def typical_column_mm(spec):
    """从 StyleSpec 的页面模板里取出现次数最多的正文栏宽。

    宁可用样刊自己的网格，也不要写死 160mm —— 双栏刊物写死会把图撑出栏外。
    """
    widths = Counter()
    for tpl in spec.get("page_templates", []) or []:
        g = tpl.get("grid") or {}
        l, r = to_mm(g.get("left_mm")), to_mm(g.get("right_mm"))
        if l and r and 60 <= (r - l) <= 210:
            widths[int(round(r - l))] += tpl.get("count", 1)
    if widths:
        return float(widths.most_common(1)[0][0])
    return 160.0


def page_heading(page):
    """取页面里第一个 h1/h2 作为该页主题，用于给缺图位拟题。"""
    for b in page.get("blocks", []) or []:
        if b.get("type") in ("h1", "h2"):
            t = (b.get("text") or "").strip()
            if t:
                return t
    return ""


def collect_block_tasks(content, imagery, dpi, col_mm):
    """遍历 content.json 的 pages，找出所有「空图位」。

    实测 content.json 的顶层是 pages（不是 articles），图位分布在三处：
      pages[i].blocks[j]  type="figure" 且 src 为空   —— 明确的文内配图
      pages[i].fields.hero / .banner 为空字符串       —— 主视觉位
      pages[i].images.bg 为空字符串                   —— 整版背景
    只 walks blocks 会漏掉后两类，而它们恰恰是最显眼的封面与分隔页。
    """
    tasks = []
    pages = content.get("pages") or []

    def add(slot_id, role, decision, reason, w_mm, h_mm, subject_hint="", page_no=0):
        h = h_mm if h_mm else round(w_mm / 1.6, 1)
        tasks.append({
            "source": "block",
            "slot_id": slot_id,
            "role": role,
            "decision": decision,
            "reason": reason,
            "w_mm": round(w_mm, 1),
            "h_mm": round(h, 1),
            "aspect": round(w_mm / h, 3) if h else 1.0,
            "page_no": page_no,
            "unit_title": subject_hint,
            "caption": "",
            "consistency_group": "GF",
            "occurrences": 1,
        })

    for i, page in enumerate(pages):
        tpl = page.get("template") or ""
        heading = page_heading(page)

        # 1) 整版背景
        bg = (page.get("images") or {}).get("bg")
        if isinstance(bg, str) and bg.strip() == "":
            if tpl in ("cover", "backcover") or "cover" in tpl:
                add("bg_p%d" % i, "cover", "manual",
                    "整版背景：需本期视觉主题，由人工指派后转 gen", 210.0, 297.0, heading, i)
            else:
                add("bg_p%d" % i, "hero", "manual",
                    "整版背景：需本期视觉主题，由人工指派后转 gen", 210.0, 297.0, heading, i)

        # 2) fields 里的主视觉 / 横幅
        fields = page.get("fields") or {}
        for key, role in (("hero", "hero"), ("banner", "hero")):
            v = fields.get(key)
            if isinstance(v, str) and v.strip() == "":
                add("%s_p%d" % (key, i), role, "manual",
                    "%s 位：需本期视觉主题，由人工指派后转 gen" % key,
                    col_mm, col_mm / 1.9, heading, i)

        # 3) 文内 figure 块
        for j, b in enumerate(page.get("blocks", []) or []):
            if b.get("type") != "figure":
                continue
            if (b.get("src") or "").strip():
                continue
            cap = (b.get("caption") or "").strip()
            n = len([t for t in tasks if t["slot_id"].startswith("fig")])
            # 有图注 -> 主题已知 -> 可直接生成；无图注 -> 退回页面标题做主题，仍标 gen 但置信低
            if cap:
                tasks.append({
                    "source": "block", "slot_id": "fig_%d" % n, "block_index": j, "role": "figure",
                    "decision": "gen", "reason": "正文 figure 块缺图，有图注可提炼主题",
                    "w_mm": round(col_mm, 1), "h_mm": round(col_mm / 1.6, 1),
                    "aspect": 1.6, "page_no": i, "caption": cap,
                    "unit_title": heading, "consistency_group": "GF", "occurrences": 1,
                })
            else:
                tasks.append({
                    "source": "block", "slot_id": "fig_%d" % n, "block_index": j, "role": "figure",
                    "decision": "gen", "reason": "正文 figure 块缺图且无图注，已用页面标题兜底（低置信，须复核）",
                    "w_mm": round(col_mm, 1), "h_mm": round(col_mm / 1.6, 1),
                    "aspect": 1.6, "page_no": i, "caption": "",
                    "unit_title": heading, "consistency_group": "GF", "occurrences": 1,
                })
    return tasks


def topic_from_text(text, max_len=24):
    """从图注/标题里提炼主题词。做得很保守——提炼失败就返回空，让人工补。"""
    t = (text or "").strip()
    t = re.sub(r"^图\s*\d+[:：]\s*", "", t)
    # 占位前缀不是主题，必须剥掉——实测漏剥会让 prompt 主体变成
    # 「图位待补：香港数字资产监管框架示意」这种脏串，直接喂给出图模型
    t = re.sub(r"^(图位待补|待补图|待补|占位|待确认)\s*[:：]\s*", "", t)
    t = t.replace("⟨待确认⟩", "").replace("⟨待补图⟩", "").strip()
    t = re.sub(r"[（(].*?[)）]", "", t)
    if not t:
        return ""
    return t[:max_len]


AMBIENT_HINTS = ("封面", "题花", "版头", "氛围", "分隔", "装饰", "跨页")


def classify_render(caption, title=""):
    """判定这一图位该走**矢量绘制**还是**文生图**。

    默认判为语义图（diagram）：期刊文内图位绝大多数承载具体信息——流程、框架、
    分工、并列、分层、路径。这类图的信息全在标签文字与拓扑关系上，扩散模型既写
    不对中文，也维持不住「三框并列」「四线汇聚」这类精确关系；为了回避画错而把
    具象元素抽掉，成品就是无信息的抽象色块（实测第 22 期 6 张里 5 张如此）。
    所以这类图必须用 gen_diagram.py 画。

    只有两种情形走文生图：图注命中氛围词（封面 / 题花 / 分隔页），或**图注为空**
    ——没有文字信息要承载，才适合做纯装饰的氛围图，且这类图不配技术性图注。

    早先版本用「示意 / 框架 / 流程…」正向匹配，结果「海南封关四条政策主线」因不含
    这些词被判成 imagegen，而它恰恰就是「四根红杠 + 空心几何形」那张废图的来源。
    **反向兜底（默认 diagram）才不会漏。**
    """
    text = ("%s %s" % (caption or "", title or "")).strip()
    if not text:
        return "imagegen"
    if any(k in text for k in AMBIENT_HINTS):
        return "imagegen"
    return "diagram"


def build_prompt(task, imagery):
    """拼出 prompt。结构是固定的：主体 + 媒介 + 风格锚 + 构图 + 安全约束。

    刻意不写「 photorealistic 」这类词：企业期刊配图一旦追求写实，
    很容易露出 AI 痕迹（手指、透视、错字）。抽象/矢量/编辑插图容错率高得多。
    """
    topic = topic_from_text(task.get("caption") or task.get("unit_title") or "")
    medium = imagery.get("medium") or DEFAULT_IMAGERY["medium"]
    anchor = imagery.get("style_anchor") or DEFAULT_IMAGERY["style_anchor"]

    subject = topic if topic else "BLOCK_SUBJECT"  # 留占位，逼人来补
    parts = [subject, medium, anchor]

    if task["role"] == "cover":
        parts.append("full-bleed composition, margins left empty for title overlay")
    elif task["role"] == "hero":
        parts.append("wide horizontal composition, calm, editorial")
    elif task["role"] == "figure":
        parts.append("diagrammatic clarity, simple shapes, clear visual hierarchy")
    else:
        parts.append("compact composition, works at small size")

    pal = imagery.get("palette") or []
    if pal:
        parts.append("palette limited to %s" % "、".join(pal[:4]))

    if task["role"] in ("cover", "hero"):
        parts.append("leave clean area for headline")

    # 右下角必须留空。理由不是审美，是**可裁性**：内置出图会在右下角打一枚
    # 半透明「AI生成」水印，去掉它只能沿底边或右边裁掉一条窄带。实测 6 张里
    # 就有 1 张（漏斗构图）底留白仅 6.7%、另 1 张（通栏横条）右留白仅 7.9%，
    # 导致「裁底」和「裁右」都不可行，只能重出。prompt 里先把这块留出来，
    # adopt_images 就能稳定按「先量后裁」处理。
    parts.append("keep the bottom-right corner clear of content, "
                 "leave at least 10% empty margin along the bottom edge, "
                 "content centered with generous margins on all sides")
    parts.append("no text, no letters, no logos, no human faces")
    return ", ".join(parts)


def build_negative(task, imagery):
    neg = NEGATIVE_BY_ROLE.get(task["role"], HARD_NEGATIVE)
    avoid = imagery.get("avoid") or []
    if avoid:
        neg += ", " + ", ".join(avoid[:6])
    return neg


# --------------------------------------------------------------------------
# 主流程
# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="生成期刊配图计划")
    ap.add_argument("--spec", help="stylespec.json")
    ap.add_argument("--content", help="content.json")
    ap.add_argument("--imagery", help="imagery.json：人工确认的视觉风格设定")
    ap.add_argument("--out", required=True, help="输出目录")
    ap.add_argument("--dpi", type=int, default=300, help="目标印刷分辨率，默认 300")
    ap.add_argument("--max-px", type=int, default=2048, help="像素上限，默认 2048")
    ap.add_argument("--assets", help="既有素材目录：命中则决策为 reuse")
    args = ap.parse_args()

    spec = read_json(args.spec, {}) or {}
    content = read_json(args.content, {}) or {}
    imagery = dict(DEFAULT_IMAGERY)
    imagery.update(read_json(args.imagery, {}) or {})

    # 素材索引：目录里按角色命名的文件（hero.*/cover.*/logo.*）
    asset_index = {}
    if args.assets and os.path.isdir(args.assets):
        for fn in os.listdir(args.assets):
            base = os.path.splitext(fn)[0].lower()
            if base in ("cover", "hero", "logo", "backcover", "figure", "inline"):
                asset_index[base] = os.path.join(args.assets, fn)

    col_mm = typical_column_mm(spec)
    tasks = collect_slot_tasks(spec, args.dpi, imagery, asset_index)
    tasks += collect_block_tasks(content, imagery, args.dpi, col_mm)

    # 有真实素材 -> 强制 reuse
    for t in tasks:
        if t.get("_asset"):
            t["decision"] = "reuse"
            t["asset_path"] = t["_asset"]
            t["reason"] = "已有真实素材，优先于 AI 生成"
        if t["decision"] in ("gen", "manual"):
            t["prompt_ready"] = ("BLOCK_SUBJECT" not in build_prompt(t, imagery))
        if t["decision"] == "gen":
            w_px = mm_to_px(t["w_mm"], args.dpi)
            h_px = mm_to_px(t["h_mm"], args.dpi)
            t["target_px"] = list(snap_size(w_px, h_px, args.max_px))
            t["ideal_px"] = [w_px, h_px]
            t["render"] = classify_render(t.get("caption"), t.get("unit_title"))
            t["prompt"] = build_prompt(t, imagery)
            t["negative_prompt"] = build_negative(t, imagery)
            t["reference_image"] = imagery.get("reference_image") or ""
            if t["render"] == "diagram":
                t["render_note"] = ("语义图：改用 scripts/gen_diagram.py 矢量绘制，"
                                    "不要用文生图（硬规则 25）；上面的文生图 prompt 作废")
        t.pop("_asset", None)

    gen = [t for t in tasks if t["decision"] == "gen"]
    reuse = [t for t in tasks if t["decision"] == "reuse"]
    skip = [t for t in tasks if t["decision"] == "skip"]
    manual = [t for t in tasks if t["decision"] == "manual"]

    # 占位符未替换 = 必须人工介入
    blocked = [t for t in gen if "BLOCK_SUBJECT" in t.get("prompt", "")]
    manual_blocked = [t for t in manual if not t.get("caption")]

    os.makedirs(args.out, exist_ok=True)
    plan = {
        "generated_from": {"spec": args.spec, "content": args.content, "imagery": args.imagery},
        "dpi": args.dpi,
        "summary": {
            "total": len(tasks), "gen": len(gen), "reuse": len(reuse), "skip": len(skip),
            "manual": len(manual), "column_width_mm": col_mm,
            "blocked_by_missing_subject": len(blocked),
            "diagram": len([t for t in gen if t.get("render") == "diagram"]),
            "imagegen": len([t for t in gen if t.get("render") == "imagegen"]),
            "consistency_groups": len(set(t.get("consistency_group") for t in gen)),
        },
        "imagery_profile": imagery,
        "hard_negative": HARD_NEGATIVE,
        "tasks": tasks,
    }
    pj = os.path.join(args.out, "image-plan.json")
    with open(pj, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

    # 人类复核稿
    L = []
    L.append("# 配图计划复核稿\n")
    L.append("- 总槽位 **%d**：直接生成 **%d** / 待定主题 **%d** / 复用素材 **%d** / 不配图 **%d**\n" % (
        len(tasks), len(gen), len(manual), len(reuse), len(skip)))
    L.append("- 正文栏宽取 **%.1f mm**（来自样刊网格众数，非拍脑袋）\n" % col_mm)
    L.append("- 一致性分组 **%d** 组（同组共用参考图做图生图，避免风格漂移）\n" % (
        plan["summary"]["consistency_groups"]))
    if manual_blocked:
        L.append("- ⚠️ **%d 个图位缺本期主题**（样刊的图不等于新刊要画的图），须人工指派后转 gen\n"
                 % len(manual_blocked))
    if blocked:
        L.append("- ⚠️ **%d 条 prompt 含 `BLOCK_SUBJECT` 占位**，必须人工补主题才能生成\n"
                 % len(blocked))
    L.append("\n## 一、需要生成的图\n")
    for t in gen:
        L.append("### %s —— %s\n" % (t["slot_id"], t["role"]))
        L.append("- 尺寸：%.1f×%.1f mm → %d×%d px（理想 %d×%d @%ddpi）\n" % (
            t["w_mm"], t["h_mm"], t["target_px"][0], t["target_px"][1],
            t["ideal_px"][0], t["ideal_px"][1], args.dpi))
        L.append("- 组：%s ｜ 出现 %d 次 ｜ 来源：%s\n" % (
            t.get("consistency_group"), t.get("occurrences", 1), t["source"]))
        if t.get("caption"):
            L.append("- 图注：%s\n" % t["caption"])
        if t.get("render") == "diagram":
            L.append("- **画法：矢量绘制**（`gen_diagram.py`）—— 语义图不走文生图，"
                     "下面不再给 prompt。图的信息在标签文字与拓扑关系上，"
                     "扩散模型写不对中文也维持不住连线。\n")
            L.append("- 版式建议：`columns`（并列）/ `flow`（流程）/ `rows`（逐行）"
                     "/ `stack`（分层）/ `converge`（汇聚）\n")
            L.append("- 要点一律从本期正文取，每条都要能在正文里找到出处\n")
        else:
            L.append("- 画法：文生图（氛围图；**不要配技术性图注**）\n")
            L.append("- **prompt**：`%s`\n" % t["prompt"])
            L.append("- negative：`%s`\n" % t["negative_prompt"])
        L.append("\n")
    if manual:
        L.append("## 二、待定主题（需向用户确认后再生成）\n")
        for t in manual:
            L.append("- **%s** ｜ %s ｜ %.1f×%.1fmm ｜ 组 %s ｜ 出现 %d 次\n" % (
                t["slot_id"], t["role"], t["w_mm"], t["h_mm"],
                t.get("consistency_group"), t.get("occurrences", 1)))
        L.append("\n> 把这一节打包成一次提问，逐条给出默认主题建议即可。\n\n")
    if reuse:
        L.append("## 三、复用真实素材（不要生成）\n")
        for t in reuse:
            L.append("- %s ｜ %s ｜ %s\n" % (t["slot_id"], t["role"], t.get("reason", "")))
        L.append("\n")
    if skip:
        L.append("## 四、判定为不配图\n")
        cnt = Counter((t["role"], t["reason"]) for t in skip)
        for (role, reason), n in cnt.most_common():
            L.append("- %s ×%d —— %s\n" % (role, n, reason))
    pm = os.path.join(args.out, "image-plan.md")
    with open(pm, "w", encoding="utf-8") as f:
        f.write("".join(L))

    s = plan["summary"]
    print("OK total=%d gen=%d manual=%d reuse=%d skip=%d groups=%d colmm=%.1f" % (
        s["total"], s["gen"], s["manual"], s["reuse"], s["skip"],
        s["consistency_groups"], s["column_width_mm"]))
    print("plan  ->", pj)
    print("brief ->", pm)
    if blocked:
        print("[WARN] %d 条 prompt 含占位符 BLOCK_SUBJECT，须人工补主题后再生成" % len(blocked))
    if not (imagery.get("avoid") or []):
        print("[WARN] imagery.json 没给 avoid 清单——本行业的敏感题材不会被排除。"
              "实测：律所刊漏传时，出图把「天平 + 握手」画了进来")


if __name__ == "__main__":
    main()
