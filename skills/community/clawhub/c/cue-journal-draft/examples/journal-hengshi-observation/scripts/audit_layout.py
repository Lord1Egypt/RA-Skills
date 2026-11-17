#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""audit_layout.py — 版面质量门禁（效果侧）

`crosscheck.py` 只保证「三个渲染器内容一致」，`build_draft.py --stats` 只保证
「篇幅量级达标」。两者都**不保证成品好看、好读**。实测（2026-09-18）一本
门禁全绿的稿子仍然：正文字号比样刊小一档、字号层级碎成八档、行距 2.3 倍、
页脚固定件带着 73 处中文空格、品牌字体（苹方）被 PyMuPDF 静默换成兜底字体。
这些都是**不报错**的，只能量出来。

本脚本把「美观 / 易读」变成七条可校验的指标，跑在 `+check` 之前：

    python audit_layout.py --pdf out/draft.pdf --spec stylespec.json
    python audit_layout.py --pdf out/draft.pdf --spec stylespec.json --sample 样刊.pdf
    python audit_layout.py --pdf out/draft.pdf --spec stylespec.json --json
    python audit_layout.py --pdf out/draft.pdf --spec stylespec.json --strict   # WARN 也算失败

退出码：0 = 通过 / 1 = 门禁失败（FAIL，或 --strict 下有 WARN）/ 2 = 环境或参数不可用。
**缺 pymupdf 时明确报 exit 2，绝不假装检查过。**

七条指标
  1 body_pt      成品正文主峰字号 vs 样刊实测正文字号（比值 <0.85 判 FAIL）
  2 fragmentation 正文字号是否碎裂（主峰占比 <50% 判 WARN）
  3 leading      行距倍数（中文正文宜 1.5–2.0，>2.05 判 WARN）
  4 measure      每行字数（中文宜 20–45，超出判 WARN）
  5 font         品牌字体是否生效（成品为 Droid/Charis 等兜底字体判 WARN）
  6 zh_space     中文数字间残留空格（>0 判 FAIL，硬规则 13）
  7 density      每页字数 vs 样刊密度（偏差 >25% 判 WARN）
"""
from __future__ import print_function

import argparse
import collections
import json
import os
import re
import sys

MM = 0.3528
ZH_SPACE = re.compile(r"\d[ ]+[年月日]|年[ ]+\d|\d[ ]+月")
# PyMuPDF / ReportLab 一类渲染器在没有指定字体文件时的兜底字体
FALLBACK_FONTS = (
    "droid", "charis", "noto sans symbols", "dejavu", "liberation",
    "urw", "nimbus", "texgyre", "arial", "helvetica", "times",
)


def _load_spec(path):
    if not path or not os.path.isfile(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        sys.stderr.write("[WARN] spec 读不出来（%s），字体与字号基线将全部降级为「未知」\n" % e)
        return {}


def spec_body_pt(spec):
    """样刊实测正文字号。

    优先 `typography.body_size_pt`（目前 extract_style.py 并不写这个键）；
    退回 `typography.type_scale` 里 count 最大的一档——type_scale 的 count 是**行数**，
    正文那一档必然是行数量级最大的（实测：启明样刊 10.4pt / 1655 行，
    而 14.1pt 只有 25 行，那是栏目标题不是正文）。
    """
    typo = spec.get("typography") or {}
    v = typo.get("body_size_pt")
    if v:
        return float(v), "typography.body_size_pt"
    ts = typo.get("type_scale") or []
    if ts:
        best = max(ts, key=lambda z: z.get("count") or 0)
        if best.get("size_pt"):
            return float(best["size_pt"]), "type_scale 中 count 最大的一档"
    return None, None


def measure_pdf(path):
    """量成品：字号（char 加权）/ 行距 / 行宽 / 字体 / 每页字数。"""
    import pymupdf  # noqa: F401  (import 失败由调用方处理)

    doc = pymupdf.open(path)
    sizes = collections.Counter()
    fonts = collections.Counter()
    gaps = collections.Counter()
    widths = collections.Counter()
    per_page = []
    for pno in range(len(doc)):
        page = doc[pno]
        d = page.get_text("dict")
        lines = []
        n_chars = 0
        for b in d.get("blocks", []):
            if b.get("type") != 0:
                continue
            for l in b["lines"]:
                txt = "".join(s["text"] for s in l["spans"]).strip()
                if not txt:
                    continue
                for s in l["spans"]:
                    c = len(s["text"].strip())
                    if c:
                        sizes[round(s["size"], 1)] += c
                        fonts[s["font"]] += c
                x0, y0, x1, y1 = l["bbox"]
                lines.append((y0, x1 - x0))
                n_chars += len(re.sub(r"\s", "", txt))
        lines.sort()
        for (y0, _), (y1, _) in zip(lines, lines[1:]):
            g = y1 - y0
            if 5 < g < 40:
                gaps[round(g, 1)] += 1
        for _, w in lines:
            if w > 60:
                widths[round(w, 1)] += 1
        per_page.append(n_chars)
    pw = doc[0].rect.width * MM
    doc.close()

    body = sizes.most_common(1)[0][0] if sizes else None
    # 正文字号档位占比：只看 6–13pt 这一区（正文区），排除标题与图注
    plain = {k: v for k, v in sizes.items() if 6.0 <= k <= 13.0}
    tot_plain = sum(plain.values()) or 1
    share = (plain.get(body, 0) / float(tot_plain)) if body else 0.0
    # 行距取「合理区带内的众数」。区带是 [0.9×字号, 2.8×字号]：
    # 小于下界的是图注/页脚等小字行，大于上界的是段间距与块间距。
    # 直接取全局众数会把段间距当成行距、把倍数算高；
    # 直接取最小值则会撞上小字行（实测一本样刊因此算出 0.42 倍这种荒谬值）。
    lead = None
    if body:
        lo, hi = 0.9 * body, 2.8 * body
        band = [(k, v) for k, v in gaps.items() if lo <= k <= hi]
        if band:
            lead = max(band, key=lambda kv: kv[1])[0]
    if lead is None and gaps:
        lead = gaps.most_common(1)[0][0]
    # 正文栏宽 = 出现 ≥3 次的最宽行。取众数会撞上图注、页脚这类短行
    # （实测一份 80 页的稿子因此算出「8 字/行」这种荒谬值）。
    wide = None
    ranked = [k for k, v in widths.items() if v >= 3]
    if ranked:
        wide = max(ranked)
    elif widths:
        wide = max(widths.keys())
    per_page_sorted = sorted(per_page)
    med = per_page_sorted[len(per_page_sorted) // 2] if per_page_sorted else 0
    return {
        "pages": len(per_page),
        "body_pt": body,
        "body_share": round(share, 3),
        "plain_chars": tot_plain,
        "plain_sizes": sorted(plain.keys()),
        "leading_pt": lead,
        "leading_ratio": (round(lead / body, 2) if (lead and body) else None),
        "max_line_mm": round(wide * MM, 1) if wide else None,
        "chars_per_page_median": med,
        "chars_per_page": (sum(per_page) / float(len(per_page))) if per_page else 0,
        "chars_total": sum(per_page),
        "fonts": [f for f, _ in fonts.most_common(6)],
    }


def main():
    ap = argparse.ArgumentParser(
        description="版面质量门禁：把「美观 / 易读」量化成七条指标")
    ap.add_argument("--pdf", required=True, help="成品 PDF（draft.pdf）")
    ap.add_argument("--spec", help="stylespec.json（提供样刊实测字号与密度基线）")
    ap.add_argument("--sample", help="样刊 PDF（可选，直接量样刊做基准，比 spec 更可信）")
    ap.add_argument("--json", action="store_true", help="机器可读输出")
    ap.add_argument("--strict", action="store_true", help="WARN 也判失败")
    a = ap.parse_args()

    try:
        import pymupdf  # noqa: F401
    except ImportError:
        sys.stderr.write("[ERR] 缺 pymupdf，量不了成品 PDF："
                         "python -m pip install pymupdf\n")
        return 2
    if not os.path.isfile(a.pdf):
        sys.stderr.write("[ERR] 找不到成品 PDF：%s\n" % a.pdf)
        return 2

    out = measure_pdf(a.pdf)
    spec = _load_spec(a.spec)

    # ---- 基准：优先直接量样刊，其次 spec ----
    base_pt, base_src = None, None
    base_density = None
    if a.sample and os.path.isfile(a.sample):
        try:
            s = measure_pdf(a.sample)
            base_pt, base_src = s["body_pt"], "样刊 PDF 实测"
            sb = spec.get("scale_baseline") or {}
            if s["pages"]:
                base_density = s["chars_total"] / float(s["pages"])
        except Exception as e:
            sys.stderr.write("[WARN] 样刊量不出来（%s），退回 spec\n" % e)
    if base_pt is None:
        base_pt, base_src = spec_body_pt(spec)
    if base_density is None:
        sb = spec.get("scale_baseline") or {}
        if sb.get("chars") and sb.get("pages"):
            base_density = float(sb["chars"]) / float(sb["pages"])

    checks = []

    def add(name, level, msg, detail=""):
        checks.append({"name": name, "level": level, "msg": msg, "detail": detail})

    # 1 正文字号
    if base_pt and out["body_pt"]:
        r = out["body_pt"] / base_pt
        if r < 0.85:
            add("body_pt", "FAIL",
                "成品正文 %.1fpt，样刊 %.1fpt，只占 %.0f%%——明显偏小"
                % (out["body_pt"], base_pt, r * 100),
                "渲染器没吃到 type_scale 时最常出这条")
        elif r > 1.18:
            add("body_pt", "WARN",
                "成品正文 %.1fpt，样刊 %.1fpt，大了 %.0f%%——会撑破版心"
                % (out["body_pt"], base_pt, (r - 1) * 100), "")
        else:
            add("body_pt", "OK",
                "成品正文 %.1fpt / 样刊 %.1fpt（%.0f%%）" % (out["body_pt"], base_pt, r * 100),
                "基准来源：%s" % (base_src or "未知"))
    else:
        add("body_pt", "WARN", "没有可用基准（缺样刊 PDF 且 spec 无 type_scale），跳过",
            "给 --sample 最省事")

    # 2 字号碎裂
    if out["body_pt"] and out.get("plain_chars", 0) >= 3000:
        if out["body_share"] < 0.50:
            add("fragmentation", "WARN",
                "正文字号碎成 %d 档，主峰 %.1fpt 只占 %.0f%%——同一本刊里字号在漂移"
                % (len(out["plain_sizes"]), out["body_pt"], out["body_share"] * 100),
                "档位：%s" % ", ".join("%.1f" % x for x in out["plain_sizes"]))
        else:
            add("fragmentation", "OK",
                "正文字号收敛，主峰 %.1fpt 占 %.0f%%" % (out["body_pt"], out["body_share"] * 100), "")
    elif out["body_pt"]:
        add("fragmentation", "OK",
            "样本太小（正文区仅 %d 字），碎裂度不判" % out.get("plain_chars", 0), "")

    # 3 行距倍数
    if out["leading_ratio"]:
        lr = out["leading_ratio"]
        if lr > 2.05:
            add("leading", "WARN", "行距 %.2f 倍，偏松（中文正文宜 1.5–2.0），页面会显得散"
                % lr, "字越小、行距倍数越大，是最难看的一种组合")
        elif lr < 1.35:
            add("leading", "WARN", "行距 %.2f 倍，偏挤（中文正文宜 1.5–2.0）" % lr, "")
        else:
            add("leading", "OK", "行距 %.2f 倍" % lr, "")

    # 4 每行字数
    if out["max_line_mm"] and out["body_pt"]:
        cpl = out["max_line_mm"] / (out["body_pt"] * MM)
        if cpl > 45:
            add("measure", "WARN",
                "最宽行 %.0fmm ≈ %.0f 字/行，超出中文舒适区（20–45），易串行"
                % (out["max_line_mm"], cpl),
                "单栏全宽是已知缺口；补偿办法是收窄版心到 100–115mm，不是把字调小")
        elif cpl < 18:
            add("measure", "WARN", "最宽行仅 %.0f 字/行，版心过窄或字号过大" % cpl, "")
        else:
            add("measure", "OK", "最宽行 %.0fmm ≈ %.0f 字/行" % (out["max_line_mm"], cpl), "")

    # 5 字体
    joined = " ".join(out["fonts"]).lower()
    hits = [f for f in FALLBACK_FONTS if f in joined]
    fam = (spec.get("typography") or {}).get("families") or []
    if hits and fam:
        add("font", "WARN",
            "成品用的是兜底字体（%s），spec 里写的 %s 没生效" % ("/".join(hits[:3]), "/".join(fam[:3])),
            "PyMuPDF 的 insert_htmlbox 只认内置字体与显式注册的字体文件；"
            "要保住品牌字体得走 insert_textbox(fontfile=…) 或出 PDF 后另行套版")
    elif hits:
        add("font", "WARN", "成品用兜底字体（%s），spec 也没指定字族" % "/".join(hits[:3]), "")
    else:
        add("font", "OK", "字体 %s" % (out["fonts"][0] if out["fonts"] else "未知"), "")

    # 6 中文空格（硬规则 13）
    import pymupdf as _p
    doc = _p.open(a.pdf)
    bad = 0
    for i in range(len(doc)):
        bad += len(ZH_SPACE.findall(doc[i].get_text("text") or ""))
    doc.close()
    if bad:
        add("zh_space", "FAIL", "成品里还有 %d 处中文数字/日期间空格（硬规则 13）" % bad,
            "页脚固定件「2026 年第 8 期」是最常见的来源，逐页都印")
    else:
        add("zh_space", "OK", "无中文空格残留", "")

    # 7 页面密度
    if base_density and out["chars_per_page_median"]:
        r = out["chars_per_page"] / base_density
        if r < 0.75 or r > 1.35:
            add("density", "WARN",
                "页面密度 %.0f 字/页，样刊 %.0f 字/页，比值 %.2f——松紧与样刊不像"
                % (out["chars_per_page"], base_density, r), "")
        else:
            add("density", "OK", "密度 %.0f 字/页 / 样刊 %.0f（%.2f）"
                % (out["chars_per_page"], base_density, r), "")
    else:
        add("density", "WARN", "没有密度基线（spec 缺 scale_baseline），跳过", "")

    n_fail = sum(1 for c in checks if c["level"] == "FAIL")
    n_warn = sum(1 for c in checks if c["level"] == "WARN")

    if a.json:
        print(json.dumps({"pdf": a.pdf, "metrics": out, "checks": checks,
                          "fail": n_fail, "warn": n_warn}, ensure_ascii=False, indent=1))
    else:
        print("版面质量门禁 — %s" % os.path.basename(a.pdf))
        print("  页数 %d / 总字 %d / 每页中位 %d 字"
              % (out["pages"], out["chars_total"], out["chars_per_page_median"]))
        for c in checks:
            tag = {"OK": "[ OK ]", "WARN": "[WARN]", "FAIL": "[FAIL]"}[c["level"]]
            print("  %s %-14s %s" % (tag, c["name"], c["msg"]))
            if c["detail"] and c["level"] != "OK":
                print("         └─ %s" % c["detail"])
        print("  ── FAIL %d / WARN %d" % (n_fail, n_warn))
        if n_fail == 0 and n_warn == 0:
            print("  版面质量门禁通过。")
        elif n_fail == 0:
            print("  无阻塞项；WARN 建议逐条看一眼再交付。")

    return 1 if (n_fail or (a.strict and n_warn)) else 0


if __name__ == "__main__":
    sys.exit(main())
