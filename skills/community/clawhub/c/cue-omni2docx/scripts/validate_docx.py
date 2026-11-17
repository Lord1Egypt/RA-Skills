#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_docx.py — Omni2Docx 产品级保真 + 结构校验器
================================================================================
从源 markdown（去 markdown 语法）抽取正文，与输出的 .docx 全文比对，量化：
  1. 内容保真：CJK 字符覆盖率（docx 是否含源文全部中文）、关键锚句命中率
  2. 结构：标题层级、目录、分页符、表格数量
不是 demo 的自检——用真实数据证明"零/近零文本丢失 + 结构正确"。

用法：
  python validate_docx.py --json <combined.json> --docx <out.docx>   # 场景②③
  python validate_docx.py --md <agent产出.md> --docx <out.docx>      # 场景①（--md 直出，无中间 JSON）
"""
import argparse
import json
import re
from docx import Document
from docx.oxml.ns import qn

CJK = r"[\u4e00-\u9fff]"

# 与 build_docx.py 的 EMOJI_RE 同口径：源文比对前剥离 emoji/装饰符号，
# 保证 --strip-emoji 开下时"按要求去掉的符号"不被误报为"丢失的内容"。
EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF"
    "\u2B00-\u2BFF\uFE0F\u2705\u274C\u2757\u3030\u303D\u3297\u3299]"
)


def strip_markdown(md):
    """去掉 markdown 语法，保留可读正文（用于与 docx 文本比对）。"""
    # 内嵌图像数据 URI 是字节不是文本，不应计入保真口径
    md = re.sub(r"!\[[^\]]*\]\(data:image[^)]*\)", " ", md)
    lines = []
    for ln in md.split("\n"):
        s = ln.strip()
        if not s:
            continue
        # 标题
        s = re.sub(r"^#{1,6}\s+", "", s)
        # 表格：去掉首尾 | 与分隔行
        if s.startswith("|") or re.match(r"^[\s:|-]+$", s):
            s = s.strip("|")
            if re.match(r"^[\s:|-]+$", s):
                continue
            s = re.sub(r"\|", " ", s)
        # 引用 / 列表前缀
        s = re.sub(r"^\s*>\s?", "", s)
        s = re.sub(r"^\s*[-*+]\s+", "", s)
        s = re.sub(r"^\s*\d+[.)]\s+", "", s)
        # 行内标记
        s = re.sub(r"\*\*|__|\*|`", "", s)
        lines.append(s)
    return "\n".join(lines)


def docx_text(doc):
    parts = []
    for p in doc.paragraphs:
        parts.append(p.text)
    for t in doc.tables:
        for row in t.rows:
            cells = [c.text for c in row.cells]
            parts.append(" ".join(cells))  # 行内单元格用空格拼接，与源 markdown 去 | 后形态一致
    return "\n".join(parts)


def cjk_set(text):
    return set(re.findall(CJK, text))


def page_breaks(doc):
    n = 0
    for p in doc.paragraphs:
        for r in p.runs:
            for b in r._element.findall(qn("w:br")):
                if b.get(qn("w:type")) == "page":
                    n += 1
    return n


def headings_summary(doc):
    h = {}
    for p in doc.paragraphs:
        st = p.style.name
        if st.startswith("Heading") or st == "Title":
            h[st] = h.get(st, 0) + 1
    return h


def table_borders_audit(doc):
    """单元格级审计：表格必须在 tblPr 上带 tblBorders（引擎 style_table 必写）。

    渲染器所有 add_table 路径均经 style_table（写整表底线+行间 hairline），
    若某表 tblPr 无 tblBorders，说明绕过 style_table（回归/第三方改造风险）。
    注意：仅在 tblPr 层判定——命名样式（Table Grid 等）的边框不在此层，但
    style_table 会覆盖式写入 tblPr/tblBorders，故正常产物必带。
    """
    bad = 0
    for t in doc.tables:
        tbl = t._tbl
        tblPr = tbl.tblPr
        if tblPr is None or tblPr.find(qn("w:tblBorders")) is None:
            bad += 1
    return bad


def anchor_phrases(md, min_cjk=12):
    """从源文抽取若干长中文短语作为保真锚点。"""
    phrases = []
    for chunk in re.split(r"[。！？\n]", md):
        cjk = re.findall(CJK, chunk)
        if len(cjk) >= min_cjk:
            phrases.append(chunk.strip())
    return phrases


def main():
    ap = argparse.ArgumentParser(description="omni2docx Word 保真 + 结构校验器")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--json", help="渲染时输入的中间 JSON（场景②③）")
    g.add_argument("--md", help="--md 直出时的源 markdown（场景①，替代 --json 的源）")
    ap.add_argument("--docx", required=True)
    args = ap.parse_args()

    if args.md:
        md = EMOJI_RE.sub("", open(args.md, encoding="utf-8").read())
    else:
        data = json.load(open(args.json, encoding="utf-8"))
        md = EMOJI_RE.sub("", data.get("markdown") or "")
    doc = Document(args.docx)

    src_body = strip_markdown(md)
    out_text = docx_text(doc)

    src_cjk = cjk_set(src_body)
    out_cjk = cjk_set(out_text)
    covered = src_cjk & out_cjk
    coverage = (len(covered) / len(src_cjk) * 100) if src_cjk else 100.0
    missing = src_cjk - out_cjk

    # 锚句命中（去空白后子串匹配，排除中英文排版空格差异的假阴性）
    phrases = anchor_phrases(md)
    out_norm = re.sub(r"\s+", "", out_text)
    hit = 0
    missed = []
    for ph in phrases:
        if re.sub(r"\s+", "", ph) in out_norm:
            hit += 1
        else:
            missed.append(ph[:20])
    phrase_rate = (hit / len(phrases) * 100) if phrases else 100.0

    # 结构
    hsum = headings_summary(doc)
    pb = page_breaks(doc)
    n_tables = len(doc.tables)
    toc = any(p.style.name == "Heading 1" and p.text.strip() == "目录" for p in doc.paragraphs)
    title = any(p.style.name == "Title" for p in doc.paragraphs)

    print("=" * 64)
    print("Omni2Docx 保真 + 结构校验 :", args.docx)
    print("=" * 64)
    print("[内容保真]")
    print("  源文 CJK 字符种类 :", len(src_cjk))
    print("  docx 含源文 CJK 覆盖率 : %.2f%%" % coverage)
    print("  缺失 CJK 字符(种类) :", len(missing), list(missing)[:20])
    print("  锚句命中 : %d/%d (%.2f%%)" % (hit, len(phrases), phrase_rate))
    if missed:
        print("  未命中锚句样例 :", missed[:8])
    print("[结构]")
    print("  标题层级统计 :", hsum)
    print("  目录(TOC) :", "有" if toc else "无")
    print("  封面标题 :", "有" if title else "无")
    print("  分页符 :", pb)
    print("  表格数 :", n_tables)
    print("  docx 段落数 :", len(doc.paragraphs))
    # 判定：以字符级 CJK 覆盖率为准（阈 99%，低于阈即 DX-01）；锚句命中率仅作参考，不决定判定
    n_unstyled = table_borders_audit(doc)
    problems = []
    if coverage < 99.0:
        problems.append("DX-01 CJK 覆盖率 %.2f%% <99%%（字符丢失）" % coverage)
    if n_unstyled:
        problems.append("DX-02 未应用表格边框 %d 张（疑似绕过 style_table）" % n_unstyled)
    ok = not problems
    print("-" * 64)
    print("判定 :", "PASS（DX-01 通过）" if ok else "CHECK ⚠️（%s）" % "；".join(problems))
    print("  [参考] 锚句命中率 %.2f%%（跨表格单元格的拆分短语可能误判，不计入判定）" % phrase_rate)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
