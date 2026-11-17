#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
export_editable.py — 把 content.json 导出成「可编辑版本」：Word(.docx) 与 Markdown(.md)。

build_draft.py 出的 HTML/PDF 是**版面稿**（mm 级定位，给设计师/印刷看）；
本脚本出的 docx/md 是**文字稿**（给编辑改稿、给领导批注、给 LLM 再加工）。

三者关系：
    content.json  ──build_draft──▶  draft.html / draft.pdf   （版面，不动这份）
                  ──export_editable──▶ draft.docx / draft.md  （可编辑）
    draft.docx 被编辑 ──import_docx──▶ content.edited.json    （回填）
                  ──build_draft──▶ draft.html                 （重新合版）

docx 里所有结构与机读元数据都写在「‖标记‖」段落上（样式 JD mark），
删掉标记后文档仍然可读，但 import_docx.py 就只能按样式尽力恢复。

用法：
  python export_editable.py --spec stylespec.json --content content.json --out out/
  python export_editable.py --content content.json --out out/ --only md
  python export_editable.py --content content.json --out out/ --no-marks --no-intro

依赖：仅标准库（--only md）；docx 需要 python-docx（python -m pip install python-docx）。

命令里的 `python`：Windows 用 `python`，macOS/Linux 用 `python3`。
"""
import argparse
import html
import json
import os
import re
import sys

# --------------------------------------------------------------------------
# 常量
# --------------------------------------------------------------------------
TPL_CN = {
    "cover": "封面", "quote": "引言", "masthead": "编委会", "toc": "目录",
    "divider": "分隔页", "unit_list": "栏目", "article": "文章", "backcover": "封底",
}
DEF_BODY_PT = 10.4
DEF_LEADING = 2.15
DEF_TOP_MM = {"unit_list": 42.0, "article": 20.0}
_DOCX = None
_IMG_ISSUES = [0]   # 没有可用图源的图位数（含坏图）


# --------------------------------------------------------------------------
# 版面信息（与 build_draft.py 同口径，但不 import，保证脚本可单独拷贝）
# --------------------------------------------------------------------------
def build_layout(spec):
    canvas = spec.get("canvas", {}) if spec else {}
    w_h = canvas.get("size_mm") or [210, 297]
    W, H = float(w_h[0]), float(w_h[1])
    roles = ((spec or {}).get("palette") or {}).get("roles") or {}
    pal = {
        "primary": roles.get("primary") or roles.get("accent") or "#A10F34",
        "text": roles.get("text") or "#000000",
        "secondary": roles.get("text-secondary") or "#3E3E3E",
        "meta": roles.get("meta") or "#7F7F7F",
    }
    typo = (spec or {}).get("typography") or {}
    body_pt = float(typo.get("body_size_pt") or DEF_BODY_PT)
    leading = float(typo.get("leading") or DEF_LEADING)
    families = typo.get("families") or ["PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", "sans-serif"]
    fam = families[0] if families else "PingFang SC"

    grids = dict((spec or {}).get("grids") or {})
    if not grids:
        temps = [t for t in ((spec or {}).get("page_templates") or [])
                 if t.get("grid", {}).get("left_mm") and t.get("grid", {}).get("right_mm")]
        temps.sort(key=lambda t: -t.get("count", 0))
        for t in temps:
            g = t["grid"]
            w = g["right_mm"] - g["left_mm"]
            key = "A" if w < 160 else "B"
            if key not in grids:
                grids[key] = {"left_mm": g["left_mm"], "right_mm": g["right_mm"]}
    if not grids:
        grids = {"A": {"left_mm": 31.7, "right_mm": 175.6},
                 "B": {"left_mm": 19.0, "right_mm": 191.0}}
    return {"W": W, "H": H, "pal": pal, "body_pt": body_pt, "leading": leading,
            "fam": fam, "grids": grids}


def grid_of(L, key):
    if isinstance(key, dict):
        return key
    g = L["grids"].get(key or "A")
    if g is None:
        g = list(L["grids"].values())[0]
    return g


def page_geom(L, p):
    """返回该页在 Word 里的 (左margin mm, 右margin mm, 上margin mm, 版心宽 mm)。"""
    gkey = p.get("grid")
    if gkey:
        g = grid_of(L, gkey)
        left = float(g["left_mm"])
        right = float(L["W"] - float(g["right_mm"]))
        width = float(g["right_mm"]) - float(g["left_mm"])
        top = float(p.get("top_mm", DEF_TOP_MM.get(p.get("template"), 20.0)))
    else:
        left = right = 15.0
        width = L["W"] - 30.0
        top = 15.0
    return left, right, top, width


# --------------------------------------------------------------------------
# 文本清洗（含量地简化了 build_draft.inline：**加粗** 与 <br>）
# --------------------------------------------------------------------------
def clean(s):
    s = str(s if s is not None else "")
    s = s.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
    s = re.sub(r"</?[a-zA-Z][^>]*>", "", s)
    return html.unescape(s)


_CAP_DECOR = re.compile(
    r"^\s*(?:[\[【⟨<]\s*(?:图位)?待补(?:图)?\s*[\]】⟩>]\s*[:：]?\s*|图位待补\s*[:：]\s*)"
    r"|\s*[（(]\s*(?:图位)?待补(?:图)?\s*[）)]\s*$"
)


def caption_core(caption):
    """剥掉图注里的「图位待补」占位装饰（前后缀两种写法都出现过）。

    `adopt_images.py` 只清理**回填那一刻**的图注；从没配过图的图位没人清，
    交付稿里就会同时出现「[ 待图 ]」和「（图位待补）」，重复且看着像没做完。
    """
    s = clean(caption)
    prev = None
    while prev != s:          # 前缀 + 后缀可能同时存在，循环剥
        prev = s
        s = _CAP_DECOR.sub("", s).strip()
    return s


def rich(para, text):
    """把 **加粗** 与换行写进段落。返回段落本身。"""
    text = clean(text)
    for i, line in enumerate(text.split("\n")):
        if i:
            para.add_run().add_break()
        for j, seg in enumerate(re.split(r"\*\*(.+?)\*\*", line)):
            if not seg:
                continue
            r = para.add_run(seg)
            r.bold = (j % 2 == 1)
    return para


# --------------------------------------------------------------------------
# Markdown 导出
# --------------------------------------------------------------------------
def md_line(prefix, s):
    s = clean(s)
    return prefix + s.replace("\n", "  \n") if s else ""


def to_md(L, content, marks=True):
    out = []
    issue = content.get("issue") or {}
    out.append("# %s" % clean(issue.get("title") or "期刊底稿"))
    meta = [x for x in [issue.get("no"), issue.get("yearmonth")] if x]
    if meta:
        out.append("> %s" % " · ".join(clean(x) for x in meta))
    out.append("")

    for i, p in enumerate(content.get("pages", [])):
        tpl = p.get("template", "article")
        f = p.get("fields") or {}
        if marks:
            out.append("<!-- page=%d template=%s folio=%s grid=%s -->"
                       % (i, tpl, clean(p.get("folio", "")), clean(p.get("grid", ""))))
        out.append("## P%02d · %s%s" % (i + 1, TPL_CN.get(tpl, tpl),
                                        " · " + clean(f.get("section") or f.get("title") or "")
                                        if (f.get("section") or f.get("title")) else ""))
        out.append("")

        if tpl == "cover":
            out.append("**%s**  \n%s  \n%s" % (clean(f.get("issue_no")), clean(f.get("yearmonth")),
                                               clean(f.get("year"))))
            bg = (p.get("images") or {}).get("bg")
            if bg:
                out.append("![封面底图](%s)" % bg)
        elif tpl == "quote":
            out.append("> %s  \n> %s" % (clean(f.get("quote")), clean(f.get("source"))))
        elif tpl == "masthead":
            out.append("### %s" % clean(f.get("title")))
            if f.get("names"):
                out.append(" / ".join(clean(n) for n in f["names"]))
            if f.get("note"):
                out.append(clean(f["note"]).replace("\n", "  \n"))
        elif tpl == "toc":
            out.append("### %s" % clean(f.get("title") or "CONTENTS"))
            for g in f.get("groups", []):
                out.append("**%s %s**" % (clean(g.get("no")), clean(g.get("title"))))
                for it in g.get("items", []):
                    # `page` 优先，没有就落 `ref`（锚点，页码由渲染器解析）。
                    # 早先只导出 page，用锚点的刊目录页码整列是空的。
                    out.append("- %s …… %s" % (clean(it.get("title")),
                                               clean(it.get("page") or it.get("ref"))))
        elif tpl == "divider":
            if f.get("label"):
                out.append("**%s**" % clean(f["label"]))
        elif tpl == "unit_list":
            if f.get("banner"):
                out.append("![栏目头图](%s)" % f["banner"])
            out.append("### %s" % clean(f.get("section")))
            for u in p.get("units", []):
                out.append("#### %s" % clean(u.get("title")))
                if u.get("meta"):
                    out.append("⟨META⟩ %s" % clean(u["meta"]))
                for para in clean(u.get("body", "")).split("\n\n"):
                    if para.strip():
                        out.append(para.strip())
                if u.get("cta"):
                    out.append("⟨CTA⟩ %s" % clean(u["cta"]))
                if u.get("image"):
                    out.append("![配图](%s)" % u["image"])
                out.append("")
        elif tpl == "article":
            if f.get("hero"):
                out.append("![主图](%s)" % f["hero"])
            out.append("### %s" % clean(f.get("title")))
            if f.get("byline"):
                out.append("*%s*" % clean(f["byline"]))
            if f.get("abstract"):
                out.append("> **摘要** %s" % clean(f["abstract"]))
            for b in p.get("blocks", []):
                t = b.get("type", "p")
                txt = clean(b.get("text", ""))
                if t == "h1":
                    out.append("#### " + txt)
                elif t == "h2":
                    out.append("##### " + txt)
                elif t == "li":
                    out.append("- " + txt)
                elif t == "quote":
                    out.append("> " + txt.replace("\n", "  \n> "))
                elif t == "figure":
                    if b.get("src"):
                        out.append("![%s](%s)" % (clean(b.get("caption") or ""), b["src"]))
                    else:
                        out.append("⟨待补图⟩ %s" % caption_core(b.get("caption") or "图位"))
                elif t == "note":
                    out.append("<!-- note --> " + txt)
                elif t == "disclaimer":
                    out.append("> ⚠ " + txt)
                else:
                    out.append(txt)
                out.append("")
        elif tpl == "backcover":
            for c in f.get("contacts", []):
                out.append("**%s**" % clean(c.get("name")))
                for ln in c.get("lines", []):
                    out.append(clean(ln) + "  ")
                out.append("")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


# --------------------------------------------------------------------------
# DOCX 导出
# --------------------------------------------------------------------------
def _docx_imports():
    try:
        from docx import Document
        from docx.enum.section import WD_SECTION
        from docx.enum.style import WD_STYLE_TYPE
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.oxml.ns import qn
        from docx.oxml import OxmlElement
        from docx.shared import Pt, Mm, RGBColor
    except ImportError:
        sys.exit("[ERR] 导出 docx 需要 python-docx：python -m pip install python-docx\n"
                 "      只要 Markdown 的话加 --only md")
    return Document, WD_SECTION, WD_STYLE_TYPE, WD_ALIGN_PARAGRAPH, qn, OxmlElement, Pt, Mm, RGBColor


def _mkstyle(doc, name, family, size_pt, color, bold=False, italic=False,
             align=None, leading=None, space_after_pt=None, space_before_pt=None,
             left_mm=None, hidden=False):
    (Document, WD_SECTION, WD_STYLE_TYPE, WD_ALIGN_PARAGRAPH, qn,
     OxmlElement, Pt, Mm, RGBColor) = _DOCX
    st = doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
    st.base_style = doc.styles["Normal"]
    st.quick_style = False
    st.font.name = family
    rpr = st.element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is not None:
        rf.set(qn("w:eastAsia"), family)
    st.font.size = Pt(size_pt)
    st.font.bold = bold
    st.font.italic = italic
    st.font.color.rgb = RGBColor.from_string(color.lstrip("#").upper())
    pf = st.paragraph_format
    if align == "right":
        pf.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    elif align == "center":
        pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if leading:
        pf.line_spacing = leading
    if space_after_pt is not None:
        pf.space_after = Pt(space_after_pt)
    if space_before_pt is not None:
        pf.space_before = Pt(space_before_pt)
    if left_mm is not None:
        pf.left_indent = Mm(left_mm)
    if hidden:
        st.hidden = True
    return st


def build_styles(doc, L):
    fam, bp, ld = L["fam"], L["body_pt"], L["leading"]
    pal = L["pal"]
    S = {}
    S["JD mark"] = _mkstyle(doc, "JD mark", fam, 7.5, "#909090", leading=1.0,
                            space_after_pt=0, italic=False)
    S["JD note"] = _mkstyle(doc, "JD note", fam, 8.5, "#909090", leading=1.4, space_after_pt=4)
    S["JD p"] = _mkstyle(doc, "JD p", fam, bp, pal["text"], leading=ld, space_after_pt=6)
    S["JD h1"] = _mkstyle(doc, "JD h1", fam, bp, pal["primary"], bold=True,
                          leading=ld, space_before_pt=6, space_after_pt=4)
    S["JD h2"] = _mkstyle(doc, "JD h2", fam, bp, pal["text"], bold=True,
                          leading=ld, space_before_pt=4, space_after_pt=3)
    S["JD li"] = _mkstyle(doc, "JD li", fam, bp, pal["text"], leading=ld,
                          space_after_pt=3, left_mm=4)
    S["JD quote"] = _mkstyle(doc, "JD quote", fam, bp, pal["secondary"],
                             leading=ld, space_after_pt=6, left_mm=5)
    S["JD note-block"] = _mkstyle(doc, "JD note-block", fam, 8.5, pal["meta"],
                                  leading=1.5, space_after_pt=4)
    # 摘要单独一种样式：先前与 note 块共用 JD note-block，回填时被当成 note 块
    # 塞进 blocks，与 base 里的 fields.abstract 重复一遍
    S["JD abstract"] = _mkstyle(doc, "JD abstract", fam, 8.5, pal["meta"],
                                leading=1.5, space_after_pt=4)
    S["JD disclaimer"] = _mkstyle(doc, "JD disclaimer", fam, 8.5, pal["secondary"],
                                  leading=1.7, space_after_pt=4)
    S["JD caption"] = _mkstyle(doc, "JD caption", fam, 8.5, pal["meta"],
                               leading=1.4, space_after_pt=6)
    S["JD title"] = _mkstyle(doc, "JD title", fam, 15.5, pal["primary"], bold=True,
                             leading=1.35, space_after_pt=6)
    S["JD byline"] = _mkstyle(doc, "JD byline", fam, bp, "#404040",
                              leading=ld, align="right", space_after_pt=8)
    S["JD section"] = _mkstyle(doc, "JD section", fam, 18.0, pal["primary"], bold=True,
                               leading=1.3, space_after_pt=10)
    S["JD unit-title"] = _mkstyle(doc, "JD unit-title", fam, bp, pal["text"], bold=True,
                                  leading=ld, space_before_pt=8, space_after_pt=3)
    S["JD unit-body"] = _mkstyle(doc, "JD unit-body", fam, bp, pal["text"],
                                 leading=ld, space_after_pt=5)
    S["JD unit-meta"] = _mkstyle(doc, "JD unit-meta", fam, max(8.0, bp - 2.0),
                                 pal.get("secondary") or "#7F7F7F",
                                 leading=1.5, space_after_pt=4)
    S["JD cta"] = _mkstyle(doc, "JD cta", fam, bp, pal["primary"], bold=True,
                           leading=ld, align="right", space_after_pt=8)
    S["JD toc-title"] = _mkstyle(doc, "JD toc-title", fam, 21.5, "#999999",
                                 leading=1.2, align="right", space_after_pt=8)
    S["JD toc-group"] = _mkstyle(doc, "JD toc-group", fam, 12.0, pal["primary"], bold=True,
                                 leading=1.4, space_before_pt=8, space_after_pt=4)
    S["JD toc-item"] = _mkstyle(doc, "JD toc-item", fam, bp, pal["text"],
                                leading=ld, space_after_pt=2)
    S["JD quote-text"] = _mkstyle(doc, "JD quote-text", fam, 14.1, pal["primary"], bold=True,
                                  leading=1.8, space_after_pt=8)
    S["JD quote-src"] = _mkstyle(doc, "JD quote-src", fam, 12.0, pal["primary"],
                                 leading=1.5, align="right", space_after_pt=4)
    S["JD cover-no"] = _mkstyle(doc, "JD cover-no", fam, bp, pal["text"], bold=True, leading=ld)
    S["JD cover-ym"] = _mkstyle(doc, "JD cover-ym", fam, bp, pal["text"], leading=ld,
                                space_before_pt=2)
    S["JD cover-year"] = _mkstyle(doc, "JD cover-year", fam, 21.5, pal["text"], bold=True,
                                  leading=1.2, space_before_pt=8)
    S["JD names"] = _mkstyle(doc, "JD names", fam, 9.0, pal["text"], leading=1.8)
    S["JD meta"] = _mkstyle(doc, "JD meta", fam, 9.0, pal["secondary"],
                            leading=1.6, space_after_pt=4)
    S["JD mh-title"] = _mkstyle(doc, "JD mh-title", fam, 12.0, pal["primary"], bold=True,
                                leading=1.4, space_after_pt=4)
    S["JD bc-title"] = _mkstyle(doc, "JD bc-title", fam, bp, pal["text"], bold=True,
                                leading=ld, space_before_pt=6, space_after_pt=2)
    S["JD bc-line"] = _mkstyle(doc, "JD bc-line", fam, 9.0, pal["secondary"],
                               leading=1.6, space_after_pt=0)
    S["JD figure"] = _mkstyle(doc, "JD figure", fam, bp, pal["text"], space_after_pt=2)
    S["JD running"] = _mkstyle(doc, "JD running", fam, 9.9, pal["primary"], leading=1.2,
                               align="right")
    return S


def add_para(doc, S, style, text, **kw):
    p = doc.add_paragraph(style=S.get(style))
    rich(p, text)
    return p


def add_mark(doc, S, text):
    p = doc.add_paragraph(style=S["JD mark"])
    r = p.add_run(text)
    return p


def mark_page(p, i, with_json=True):
    tpl = p.get("template", "article")
    f = p.get("fields") or {}
    human = "%s%s" % (TPL_CN.get(tpl, tpl),
                      " · " + clean(f.get("section") or f.get("title") or "")
                      if (f.get("section") or f.get("title")) else "")
    s = "‖页 %02d‖ %s" % (i + 1, human)
    if not with_json:
        return s
    meta = {k: v for k, v in p.items()
            if k not in ("template", "grid", "folio", "fields", "units", "blocks")}
    payload = {"i": i, "template": tpl, "grid": p.get("grid", ""),
               "folio": clean(p.get("folio", "")), "meta": meta}
    return s + " ‖" + json.dumps(payload, ensure_ascii=False, sort_keys=True) + "‖"


def mark_img(kind, **kw):
    """图位标记。

    空的 `src` 一律**不写进标记**：实测（2026-09-17）`{"src": ""}` 会被渲染端
    当成一个待加载的图片，拿空路径去解析、报「图片读取失败」并指向 content.json
    所在目录。省掉这个键，它就只当普通文字标记。import_docx.py 用
    `img.get("src") or ""` 读取，缺键不受影响。
    """
    kw = {k: v for k, v in kw.items()
          if not (k == "src" and not str(v or "").strip())}
    return "‖图位‖ " + json.dumps({"kind": kind, **kw}, ensure_ascii=False, sort_keys=True)


def add_picture(doc, S, src, width_mm, caption=None, base=None):
    """插入图片；没有可用图源时写一行 `[ 待图 ]` 占位，绝不尝试加载空路径。

    坑（实测 2026-09-17）：`os.path.join(base, "")` 返回的是 **base 目录本身**，
    而目录的 `os.path.exists()` 为真。所以 `src=""`（figure 块省略 src 键）会
    走进图片分支，把 content.json 所在**目录**当图片去嵌入 → 抛错被 except 吞掉 →
    正文里留下「[图片读取失败] (... 'D:\\...\\work\\')」。看起来像相对路径写错，
    实际是空图位。HTML / PDF / md 三条路本来都走占位，只有 docx 漏了。

    现在：空 src 直接走占位；路径判断用 `isfile`（不接受目录）。
    """
    (Document, WD_SECTION, WD_STYLE_TYPE, WD_ALIGN_PARAGRAPH, qn,
     OxmlElement, Pt, Mm, RGBColor) = _DOCX
    src = str(src or "").strip()   # figure 块省略 src 键时是 None，直接 isabs() 会中断整份导出
    path = ""
    if src:
        path = src if (not base or os.path.isabs(src)) else os.path.join(base, src)
    if path and os.path.isfile(path):
        p = doc.add_paragraph(style=S["JD figure"])
        try:
            p.add_run().add_picture(path, width=Mm(width_mm))
        except Exception as e:
            _IMG_ISSUES[0] += 1
            p.add_run("[图片读取失败] %s (%s)" % (path, e))
        if caption:
            add_para(doc, S, "JD caption", caption)
        return True
    _IMG_ISSUES[0] += 1
    ph = doc.add_paragraph(style=S["JD figure"])
    ph.add_run("[ 待图 ]%s  ── 建议 %dmm 宽 · ≥300dpi"
               % (("  <原稿:%s>" % src) if src else "", int(round(width_mm))))
    # 图注走独立的 JD caption 段：与「已配图」两条路结构一致，回填才认得。
    # 早先占位路把图注拼在 [ 待图 ] 那一行里，import_docx 读不到 →
    # 编辑在 Word 里写/改的图注回填时静默丢失。
    if caption:
        add_para(doc, S, "JD caption", caption)
    return False


def to_docx(L, content, spec, marks=True, intro=True, base_dir=None):
    (Document, WD_SECTION, WD_STYLE_TYPE, WD_ALIGN_PARAGRAPH, qn,
     OxmlElement, Pt, Mm, RGBColor) = _DOCX
    doc = Document()
    S = build_styles(doc, L)
    issue = content.get("issue") or {}
    doc.core_properties.title = clean(issue.get("title") or "期刊底稿（可编辑版）")

    norm = doc.styles["Normal"]
    norm.font.name = L["fam"]
    rpr = norm.element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is not None:
        rf.set(qn("w:eastAsia"), L["fam"])
    norm.font.size = Pt(L["body_pt"])
    norm.paragraph_format.line_spacing = L["leading"]

    pages = content.get("pages", [])
    for i, p in enumerate(pages):
        tpl = p.get("template", "article")
        f = p.get("fields") or {}
        left, right, top, width = page_geom(L, p)

        sec = doc.sections[0] if i == 0 else doc.add_section(WD_SECTION.NEW_PAGE)
        sec.page_width = Mm(L["W"])
        sec.page_height = Mm(L["H"])
        sec.left_margin = Mm(left)
        sec.right_margin = Mm(right)
        sec.top_margin = Mm(top)
        sec.bottom_margin = Mm(15)
        sec.header_distance = Mm(8)
        sec.footer_distance = Mm(8)

        running = clean(p.get("running_text") or issue.get("running_text") or "")
        if running and p.get("running") is not False and tpl not in ("cover", "divider", "masthead"):
            try:
                hd = sec.header
                hd.is_linked_to_previous = False
                hp = hd.paragraphs[0]
                hp.style = S["JD running"]
                hp.text = ""
                hp.add_run(running)
            except Exception:
                pass

        if i == 0 and intro:
            add_para(doc, S, "JD note",
                     "本文件是「可编辑文字稿」：版面由 draft.html / draft.pdf 表达，"
                     "此处只承载文字与结构。改完文字后用 import_docx.py 回填 content.json，"
                     "再跑 build_draft.py 重新合版即可。Word 的页码不与版面页码一一对应，"
                     "以每个 ‖页 NN‖ 标记为准。蓝色说明行交付前可整段删除。")

        if marks:
            add_mark(doc, S, mark_page(p, i))

        bg = (p.get("images") or {}).get("bg") or p.get("bg")
        if bg:
            add_mark(doc, S, mark_img("bg", src=bg))
            add_para(doc, S, "JD note", "[整版背景图，见版面稿] %s" % os.path.basename(str(bg)))

        if tpl == "cover":
            if f.get("issue_no"):
                add_para(doc, S, "JD cover-no", f["issue_no"])
            if f.get("yearmonth"):
                add_para(doc, S, "JD cover-ym", f["yearmonth"])
            if f.get("year"):
                add_para(doc, S, "JD cover-year", f["year"])
        elif tpl == "quote":
            if f.get("quote"):
                add_para(doc, S, "JD quote-text", f["quote"])
            if f.get("source"):
                add_para(doc, S, "JD quote-src", f["source"])
        elif tpl == "masthead":
            add_para(doc, S, "JD note",
                     "[编委会这一页在版面稿里压在整版底图上，此处只给纯文字对照]")
            if f.get("title"):
                add_para(doc, S, "JD mh-title", f["title"])
            if f.get("names"):
                add_para(doc, S, "JD names", " / ".join(clean(n) for n in f["names"]))
            if f.get("note"):
                add_para(doc, S, "JD meta", f["note"])
        elif tpl == "toc":
            add_para(doc, S, "JD toc-title", f.get("title") or "CONTENTS")
            for g in f.get("groups", []):
                add_para(doc, S, "JD toc-group",
                         "%s\t%s" % (clean(g.get("no")), clean(g.get("title"))))
                for it in g.get("items", []):
                    # 同 md：`ref` 锚点也要落进来，否则编辑看不到目录页码
                    add_para(doc, S, "JD toc-item",
                             "%s\t%s" % (clean(it.get("title")),
                                         clean(it.get("page") or it.get("ref"))))
        elif tpl == "divider":
            add_para(doc, S, "JD note", clean(f.get("label") or "[分隔页，无正文]"))
        elif tpl == "unit_list":
            if f.get("banner"):
                add_mark(doc, S, mark_img("banner", src=f["banner"]))
                add_picture(doc, S, f["banner"], width, base=base_dir)
            add_para(doc, S, "JD section", f.get("section", ""))
            for u in p.get("units", []):
                add_para(doc, S, "JD unit-title", u.get("title", ""))
                if u.get("meta"):
                    add_para(doc, S, "JD unit-meta", u["meta"])
                for seg in clean(u.get("body", "")).split("\n\n"):
                    if seg.strip():
                        add_para(doc, S, "JD unit-body", seg.strip())
                if u.get("image"):
                    add_mark(doc, S, mark_img("unit-image", src=u["image"]))
                    add_picture(doc, S, u["image"], width, base=base_dir)
                if u.get("cta"):
                    add_para(doc, S, "JD cta", u["cta"])
        elif tpl == "article":
            if f.get("hero"):
                add_mark(doc, S, mark_img("hero", src=f["hero"]))
                add_picture(doc, S, f["hero"], width, base=base_dir)
            add_para(doc, S, "JD title", f.get("title", ""))
            if f.get("byline"):
                add_para(doc, S, "JD byline", f["byline"])
            if f.get("abstract"):
                # 不带「摘要」前缀：前缀会跟着回填进 fields.abstract，
                # 重新合版就变成「摘要 摘要 ...」。状态由样式表达。
                add_para(doc, S, "JD abstract", f["abstract"])
            for j, b in enumerate(p.get("blocks", [])):
                t = b.get("type", "p")
                if t == "figure":
                    add_mark(doc, S, mark_img("figure", index=j, src=b.get("src") or ""))
                    add_picture(doc, S, b.get("src") or "", width, caption=b.get("caption"),
                                base=base_dir)
                elif t == "note":
                    add_para(doc, S, "JD note-block", b.get("text", ""))
                else:
                    m = {"h1": "JD h1", "h2": "JD h2", "li": "JD li",
                         "quote": "JD quote", "disclaimer": "JD disclaimer"}.get(t, "JD p")
                    add_para(doc, S, m, b.get("text", ""))
        elif tpl == "backcover":
            for c in f.get("contacts", []):
                add_para(doc, S, "JD bc-title", c.get("name", ""))
                for ln in c.get("lines", []):
                    add_para(doc, S, "JD bc-line", ln)
    return doc


# --------------------------------------------------------------------------
def main():
    global _DOCX
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", default=None)
    ap.add_argument("--content", required=True)
    ap.add_argument("--out", default="out")
    ap.add_argument("--only", default="all", choices=["all", "docx", "md"])
    ap.add_argument("--md-name", default="draft.md")
    ap.add_argument("--docx-name", default="draft.docx")
    ap.add_argument("--base-dir", default=None,
                    help="content.json 里相对图片路径的根目录，默认 content.json 所在目录")
    ap.add_argument("--no-marks", action="store_true", help="不写 ‖标记‖ 段（不可回读）")
    ap.add_argument("--no-intro", action="store_true", help="不加首页交付说明")
    args = ap.parse_args()

    spec = {}
    if args.spec and os.path.exists(args.spec):
        with open(args.spec, encoding="utf-8") as fp:
            spec = json.load(fp)
    elif args.spec:
        sys.stderr.write("[WARN] spec 不存在，使用内置默认网格\n")

    with open(args.content, encoding="utf-8") as fp:
        content = json.load(fp)

    L = build_layout(spec)
    os.makedirs(args.out, exist_ok=True)
    base_dir = args.base_dir or os.path.dirname(os.path.abspath(args.content))
    marks = not args.no_marks

    if args.only in ("all", "md"):
        p = os.path.join(args.out, args.md_name)
        with open(p, "w", encoding="utf-8") as fp:
            fp.write(to_md(L, content, marks=marks))
        print("md  : %s" % os.path.abspath(p))

    if args.only in ("all", "docx"):
        _DOCX = _docx_imports()
        doc = to_docx(L, content, spec, marks=marks, intro=not args.no_intro,
                      base_dir=base_dir)
        p = os.path.join(args.out, args.docx_name)
        doc.save(p)
        print("docx: %s" % os.path.abspath(p))
        print("      pages=%d %s" % (len(content.get("pages", [])),
                                     "（已写回读标记）" if marks else "（无标记，不可回填）"))
        if _IMG_ISSUES[0]:
            print("      [WARN] %d 处图位没有可用图源，已写成 [ 待图 ] 占位" % _IMG_ISSUES[0])


if __name__ == "__main__":
    main()
