#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
exam_format.py — 试卷选择题选项纵向对齐 + 全卷版式统一

用法：
    # 1) 先诊断（只读，不改文件）
    python3 exam_format.py 试卷.docx --inspect

    # 2) 对齐选项 + 统一版式（自动备份后原地覆盖）
    python3 exam_format.py 试卷.docx

    # 3) 只对齐选项，不动其它版式（最小干预）
    python3 exam_format.py 试卷.docx --align-only

    # 4) 输出到新文件、指定四列、正文 14pt
    python3 exam_format.py 试卷.docx -o 新卷.docx --letters ABCD --body-size 14

核心能力：
  * 把选项行（A./B./C./D.）之间的空格/制表符收敛为单个制表符，设置统一制表位 → 列对齐
  * 按内容自适应计算列位（避免题号前缀过长导致溢出到下一列）
  * 统一字号/字体/颜色（含表格、页眉页脚），消除 szCs 回退与 theme 字体继承
  * 自动按 OOXML schema 顺序重排 rPr/pPr，避免 Word 解析异常
  * 改前自动备份，改后输出内容校验报告（去空白逐段比对，确保零改动）

依赖：python-docx, lxml
"""

import argparse
import os
import re
import shutil
import sys
import zipfile
from datetime import datetime

try:
    import docx
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    from docx.shared import Pt
    from lxml import etree
except ImportError:
    sys.exit(
        "缺少依赖 python-docx / lxml。\n"
        "请用已安装依赖的解释器运行，例如：\n"
        "  /Users/heberlian/.workbuddy/binaries/python/envs/default/bin/python "
        f"{os.path.basename(__file__)} 试卷.docx\n"
        "或安装依赖：\n"
        f"  {sys.executable} -m pip install python-docx lxml"
    )

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

# ---------------- OOXML 元素顺序（顺序敏感，Word 会校验） ----------------
RPR_ORDER = ["rStyle", "rFonts", "b", "bCs", "i", "iCs", "caps", "smallCaps", "strike",
             "dstrike", "outline", "shadow", "emboss", "imprint", "noProof", "snapToGrid",
             "vanish", "webHidden", "color", "spacing", "w", "kern", "position", "sz", "szCs",
             "highlight", "u", "effect", "bdr", "shd", "fitText", "vertAlign", "rtl", "cs",
             "em", "lang", "eastAsianLayout", "specVanish", "oMath"]
PPR_ORDER = ["pStyle", "keepNext", "keepLines", "pageBreakBefore", "framePr", "widowControl",
             "numPr", "suppressLineNumbers", "pBdr", "shd", "tabs", "suppressAutoHyphens",
             "kinsoku", "wordWrap", "overflowPunct", "topLinePunct", "autoSpaceDE", "autoSpaceDN",
             "bidi", "adjustRightInd", "snapToGrid", "spacing", "ind", "contextualSpacing",
             "mirrorIndents", "suppressOverlap", "jc", "textDirection", "textAlignment",
             "textboxTightWrap", "outlineLvl", "divId", "cnfStyle", "rPr", "sectPr", "pPrChange"]

DEFAULT_LAT = "Times New Roman"
DEFAULT_EA = "宋体"


# ==================================================================== 工具函数
def para_text(p):
    return "".join(r.text for r in p.runs)


def text_width_pt(s, size_pt):
    """按 西文≈0.52em / 中文≈1.0em / 制表符≈1.0em 估算宽度（pt）。用于自适应列位。"""
    w = 0.0
    for ch in s:
        if ch == "\t":
            w += size_pt * 1.0          # 制表符按一个汉字宽保守估算
        else:
            w += size_pt * (1.0 if ord(ch) > 0x2E80 else 0.52)
    return w


def set_tab_stops(p, positions_tw):
    """设置段落制表位（左对齐）。positions_tw 为二十分之一磅(twips)列表。"""
    pPr = p._p.get_or_add_pPr()
    old = pPr.find(qn("w:tabs"))
    if old is not None:
        pPr.remove(old)
    tabs = OxmlElement("w:tabs")
    for pos in positions_tw:
        t = OxmlElement("w:tab")
        t.set(qn("w:val"), "left")
        t.set(qn("w:pos"), str(int(pos)))
        tabs.append(t)
    pPr.append(tabs)          # 顺序由 sort_docx_xml 统一修正


def clear_tab_stops(p):
    pPr = p._p.get_or_add_pPr()
    old = pPr.find(qn("w:tabs"))
    if old is not None:
        pPr.remove(old)


def unify_run(r, size_half, bold, lat=DEFAULT_LAT, ea=DEFAULT_EA,
              keep_underline=True, color="000000"):
    """把一个 run 的字体/字号/颜色写成确定值，杜绝继承与回退。"""
    rPr = r._element.get_or_add_rPr()
    rf = rPr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rPr.insert(0, rf)
    for a in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme",
              "w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        if rf.get(qn(a)) is not None:
            del rf.attrib[qn(a)]
    rf.set(qn("w:ascii"), lat)
    rf.set(qn("w:hAnsi"), lat)
    rf.set(qn("w:eastAsia"), ea)
    rf.set(qn("w:cs"), lat)
    rf.set(qn("w:hint"), "eastAsia")
    for tag in ("w:sz", "w:szCs"):          # szCs 必须与 sz 同步，否则部分字符用样式里的值
        e = rPr.find(qn(tag))
        if e is None:
            e = OxmlElement(tag)
            rPr.append(e)
        e.set(qn("w:val"), str(size_half))
    for tag in ("w:b", "w:bCs"):
        e = rPr.find(qn(tag))
        if bold:
            if e is None:
                e = OxmlElement(tag)
                rPr.append(e)
            e.set(qn("w:val"), "1")
        elif e is not None:
            rPr.remove(e)
    for tag in ("w:i", "w:iCs"):            # 去掉斜体，保证字体样式一致
        e = rPr.find(qn(tag))
        if e is not None:
            rPr.remove(e)
    c = rPr.find(qn("w:color"))
    if c is None:
        c = OxmlElement("w:color")
        rPr.append(c)
    c.set(qn("w:val"), color)
    if not keep_underline:
        u = rPr.find(qn("w:u"))
        if u is not None:
            rPr.remove(u)


def mark_para_empty(p, size_half=24):
    """空段落设置段落标记字号，防止继承 Normal 造成行高不一致。"""
    pPr = p._p.get_or_add_pPr()
    mrpr = pPr.find(qn("w:rPr"))
    if mrpr is None:
        mrpr = OxmlElement("w:rPr")
        pPr.append(mrpr)
    for tag in ("w:sz", "w:szCs"):
        e = mrpr.find(qn(tag))
        if e is None:
            e = OxmlElement(tag)
            mrpr.append(e)
        e.set(qn("w:val"), str(size_half))


def fix_style(style, size_half, lat=DEFAULT_LAT, ea=DEFAULT_EA):
    """修正样式定义，堵住 theme 字体与 szCs 的继承漏洞。"""
    rpr = style.element.find(qn("w:rPr"))
    if rpr is None:
        rpr = OxmlElement("w:rPr")
        style.element.append(rpr)
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rpr.insert(0, rf)
    for a in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme",
              "w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        if rf.get(qn(a)) is not None:
            del rf.attrib[qn(a)]
    rf.set(qn("w:ascii"), lat)
    rf.set(qn("w:hAnsi"), lat)
    rf.set(qn("w:eastAsia"), ea)
    rf.set(qn("w:cs"), lat)
    for tag in ("w:sz", "w:szCs"):
        e = rpr.find(qn(tag))
        if e is None:
            e = OxmlElement(tag)
            rpr.append(e)
        e.set(qn("w:val"), str(size_half))


def _sort_children(el, order):
    kids = list(el)
    if not kids:
        return 0
    def key(c):
        t = c.tag.split("}")[1]
        return order.index(t) if t in order else len(order)
    ordered = sorted(kids, key=key)
    if [c.tag for c in ordered] == [c.tag for c in kids]:
        return 0
    for c in kids:
        el.remove(c)
    for c in ordered:
        el.append(c)
    return 1


def sort_docx_xml(path):
    """按 OOXML schema 顺序重排 docx 内所有 w:rPr / w:pPr（document/styles/header/footer）。"""
    tmp = path + ".sorttmp"
    fixed = 0
    zin = zipfile.ZipFile(path, "r")
    zout = zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED)
    for item in zin.infolist():
        data = zin.read(item.filename)
        name = item.filename
        if name.endswith(".xml") and any(k in name for k in
                                         ("document", "styles", "header", "footer")):
            try:
                root = etree.fromstring(data)
            except Exception:
                zout.writestr(item, data)
                continue
            for tag, order in (("rPr", RPR_ORDER), ("pPr", PPR_ORDER)):
                for el in root.iter(qn("w:" + tag)):
                    fixed += _sort_children(el, order)
            data = etree.tostring(root, xml_declaration=True,
                                  encoding="UTF-8", standalone=True)
        zout.writestr(item, data)
    zout.close()
    zin.close()
    shutil.move(tmp, path)
    return fixed


# ==================================================================== 选项行识别
def parse_option_line(text, letters="ABCD"):
    """
    识别选项行。返回 dict(prefix, items=[(letter, content)], spans=[(mark_start, mark_end)])
    识别不到返回 None。
    """
    marks = []
    for m in re.finditer(r"([A-Za-z])\s*([.、．])", text):
        if m.group(1) not in letters:
            continue
        # 标记须位于行首或空白之后，避免匹配单词中的字母
        if m.start() > 0 and text[m.start() - 1] not in " \t\u3000\u00a0":
            continue
        marks.append((m.start(), m.end(), m.group(1)))
    if len(marks) < 2:
        return None
    # 字母必须按 letters 顺序严格递增
    seq = [mk[2] for mk in marks]
    idxs = [letters.index(c) for c in seq]
    if idxs != sorted(idxs) or len(set(idxs)) != len(idxs):
        return None
    # 每个标记后须有内容；记录内容在原文中的结束位置（供 gap 计算）
    items = []
    ends = []
    for i, (s, e, ch) in enumerate(marks):
        stop = marks[i + 1][0] if i + 1 < len(marks) else len(text)
        seg = text[e:stop]
        stripped = seg.rstrip(" \t\u3000")
        items.append((ch, stripped.strip(" \t\u3000")))
        ends.append(e + len(stripped))
    if any(not c for _, c in items):
        return None
    return {"prefix": text[:marks[0][0]], "items": items,
            "spans": [(mk[0], mk[1]) for mk in marks], "ends": ends}


def find_option_paragraphs(d, letters="ABCD"):
    """返回 [(paragraph_index, Paragraph, parsed)]"""
    out = []
    for i, p in enumerate(d.paragraphs):
        parsed = parse_option_line(para_text(p), letters)
        if parsed:
            out.append((i, p, parsed))
    return out


# ==================================================================== 对齐算法
def rewrite_gaps(p, gaps):
    """
    把全文坐标 gaps=[(start,end)] 的区间各自收敛为「一个制表符」。
    逐 run 改写以保留各 run 原有格式（下划线等）。tab 只放在区间起点所在的 run。
    """
    pos = 0
    for r in p.runs:
        t = r.text
        rs, re_ = pos, pos + len(t)
        if re_ == rs:
            continue
        new, cur = "", 0
        for gs, ge in gaps:
            # 用 ge < rs / gs > re_ 判定不相交，才能让长度为 0 的 gap（纯插入）生效
            if ge < rs or gs > re_:
                continue
            lgs, lge = max(gs, rs) - rs, min(ge, re_) - rs
            new += t[cur:lgs]
            # 只有「区间起点严格落在本 run 内」才产出制表符。
            # 用 rs <= gs < re_ 而非 gs >= rs，否则起点恰在 run 边界时会插入两个 tab，
            # 导致跳到下一个制表位、对齐失效。
            if rs <= gs < re_:
                new += "\t"
            cur = lge
        new += t[cur:]
        r.text = new                # python-docx 会把 \t 转成真正的 <w:tab/>
        pos += len(t)


def compute_columns(option_infos, size_pt, gap_chars=2.0, usable_pt=None,
                    first_line_pt=0.0):
    """
    自适应计算列位（pt）。返回 (cols_pt, warn)
    cols_pt[i] = 第 i 个选项字母的起始位置（相对左边距+左缩进）
    """
    n = max(len(info["items"]) for _, _, info in option_infos)
    maxw = [0.0] * n
    prefix_max = 0.0
    for _, _, info in option_infos:
        prefix_max = max(prefix_max,
                         text_width_pt(info["prefix"].rstrip(" \t\u3000"), size_pt))
        for k, (_, content) in enumerate(info["items"]):
            if k < n:
                # 内容宽度 + 字母标记本身（如 "A. "）
                maxw[k] = max(maxw[k], text_width_pt(content, size_pt) + 3.0 * 0.52 * size_pt)
    gap_pt = gap_chars * size_pt
    cols = [first_line_pt + prefix_max + gap_pt]
    for k in range(n - 1):
        cols.append(cols[-1] + maxw[k] + gap_pt)
    warn = None
    if usable_pt:
        need = cols[-1] + maxw[-1]
        if need > usable_pt:
            # ① 先尝试压缩列间隙
            slack = need - usable_pt
            per_gap = slack / max(1, n)
            if gap_pt - per_gap > 0.3 * size_pt:
                gap_pt -= per_gap
                cols = [first_line_pt + prefix_max + gap_pt]
                for k in range(n - 1):
                    cols.append(cols[-1] + maxw[k] + gap_pt)
                warn = f"列宽超出，已自动压缩列间隙至 {gap_pt / size_pt:.1f} 字符"
            # ② 仍不够：按可用宽度等分，避免制表符跳到 Word 默认制表位而彻底错位
            if cols[-1] + maxw[-1] > usable_pt:
                head = min(cols[0], usable_pt * 0.4)
                per = (usable_pt - head) / max(1, n - 1)
                cols = [head + per * k for k in range(n)]
                suggest = size_pt * usable_pt / need
                warn = (f"内容需 {need:.0f}pt > 可用 {usable_pt:.0f}pt，已按可用宽度等分列位"
                        f"（长选项可能重叠）。建议：①让选项单独成行（题干一行、选项一行）"
                        f" ②或 --body-size {suggest:.1f} ③或加大页边距可用宽度")
    return cols, warn


def align_options(d, letters, size_pt, cols_pt=None, gap_chars=2.0,
                  normalize=True):
    """对齐所有选项行。返回 (已处理行数, 列位pt, 警告列表)"""
    infos = find_option_paragraphs(d, letters)
    if not infos:
        return 0, [], ["未识别到任何选项行（检查 --letters 是否与卷面一致）"]

    warns = []
    sec = d.sections[0]
    usable = (sec.page_width - sec.left_margin - sec.right_margin) / 12700.0
    if cols_pt is None:
        cols_pt, w = compute_columns(infos, size_pt, gap_chars, usable)
        if w:
            warns.append(w)

    for i, p, info in infos:
        full = para_text(p)
        gaps = []
        # 1) 前缀（题号等）有效内容之后 → 一个制表符
        #    必须从前缀尾部算起，否则会把 "(    ) 1." 这样的题号一并删掉
        p_end = len(info["prefix"].rstrip(" \t\u3000"))
        gaps.append((p_end, info["spans"][0][0]))
        # 2) 上一选项「内容结束」到下一选项「标记开始」之间 → 一个制表符
        #    注意：必须到 content 结束为止，否则会把选项正文一并替换掉
        for end_pos, nxt in zip(info["ends"], info["spans"][1:]):
            gaps.append((end_pos, nxt[0]))
        gaps.sort()
        rewrite_gaps(p, gaps)

        # 3) 去掉段尾多余空白（只动最后一个 run，保留其余 run 的格式）
        if p.runs:
            tail = p.runs[-1]
            stripped = tail.text.rstrip(" \t\u3000")
            if stripped != tail.text:
                tail.text = stripped

        # 4) 规范标记后的空格：B.busy / A .busy -> B. busy
        #    逐 run 处理，不合并 run（否则会丢失下划线等格式，且重拼 text 会重复尾部字符）
        if normalize:
            for r in p.runs:
                if not r.text:
                    continue
                fixed = re.sub(rf"([{letters}])\s*([.、．])(?=[^\s])", r"\1\2 ", r.text)
                if fixed != r.text:
                    r.text = fixed

        # 4) 设置制表位（twips）；题干式选项行首行缩进归零，保证各行列位一致
        pf = p.paragraph_format
        pf.first_line_indent = Pt(0)
        set_tab_stops(p, [c * 20 for c in cols_pt])

    return len(infos), cols_pt, warns


# ==================================================================== 版式统一
def classify(doc_paras, body_half):
    """
    依据原始字号/加粗把段落分为 title1 / title2 / title3 / body。
    返回 {index: role}
    """
    roles = {}
    for i, p in enumerate(doc_paras):
        t = p.text.strip()
        if not t:
            roles[i] = "blank"
            continue
        sizes = [r.font.size.pt for r in p.runs if r.font.size]
        sz = max(sizes) if sizes else body_half / 2.0
        bold = any(r.font.bold for r in p.runs)
        if sz >= body_half / 2.0 + 5:
            roles[i] = "title1"
        elif sz >= body_half / 2.0 + 1.5:
            roles[i] = "title2"
        elif bold and len(t) <= 40:
            roles[i] = "title3"
        else:
            roles[i] = "body"
    return roles


def restyle(d, body_size=12.0, line_spacing=1.5, lat=DEFAULT_LAT, ea=DEFAULT_EA,
            margins_pt=(54, 54, 72, 54), indent_passage=True):
    """统一全卷版式：页面/字号/字体/行距/缩进。返回统计。"""
    body_half = int(round(body_size * 2))
    sec = d.sections[0]
    ml, mr, mt, mb = margins_pt
    sec.left_margin, sec.right_margin = Pt(ml), Pt(mr)
    sec.top_margin, sec.bottom_margin = Pt(mt), Pt(mb)

    roles = classify(d.paragraphs, body_half)
    size_map = {"title1": body_size + 4, "title2": body_size + 2,
                "title3": body_size, "body": body_size, "blank": body_size}
    bold_map = {"title1": True, "title2": True, "title3": True,
                "body": False, "blank": False}

    n = 0
    for i, p in enumerate(d.paragraphs):
        role = roles[i]
        sz = size_map[role]
        bold = bold_map[role]
        pf = p.paragraph_format
        pf.left_indent, pf.right_indent = Pt(0), Pt(0)
        if role != "blank":
            pf.line_spacing = 1.0 if role.startswith("title") else line_spacing
        # 长正文段落（完形/阅读短文）首行缩进 2 字符；题干、对话、标题顶格
        if role == "body" and indent_passage:
            t = p.text.strip()
            is_passage = (len(t) >= 60
                          and not re.match(r"^[\(（]?\s*\d", t)
                          and not re.match(r"^[A-Za-z]:", t)
                          and not re.match(r"^——", t))
            pf.first_line_indent = Pt(body_size * 2) if is_passage else Pt(0)
        pf.space_before = Pt(12 if role == "title1" else 6 if role.startswith("title") else 0)
        pf.space_after = Pt(6 if role == "title1" else 3 if role.startswith("title") else 0)
        if role == "title1":
            pf.alignment = 1          # 居中
        pf.keep_with_next = role.startswith("title")
        try:
            snap = p._p.get_or_add_pPr().find(qn("w:snapToGrid"))
            if snap is None:
                snap = OxmlElement("w:snapToGrid")
                p._p.get_or_add_pPr().append(snap)
            snap.set(qn("w:val"), "0")     # 关掉网格对齐，行距才可预期
        except Exception:
            pass

        if p.runs:
            for r in p.runs:
                unify_run(r, int(round(sz * 2)), bold, lat, ea, keep_underline=True)
                n += 1
        else:
            mark_para_empty(p, body_half)

    # 表格与正文同字号同字体
    for tb in d.tables:
        for row in tb.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    p.paragraph_format.line_spacing = 1.0
                    p.paragraph_format.space_before = Pt(0)
                    p.paragraph_format.space_after = Pt(0)
                    if p.runs:
                        for r in p.runs:
                            unify_run(r, body_half, False, lat, ea)
                            n += 1
                    else:
                        mark_para_empty(p, body_half)

    # 页眉页脚（隐藏占位 run 也统一，避免残留异字号）
    for s in d.sections:
        for part in (s.header, s.footer, s.first_page_header, s.first_page_footer,
                     s.even_page_header, s.even_page_footer):
            for p in part.paragraphs:
                for r in p.runs:
                    unify_run(r, 18, False, lat, ea, keep_underline=False)
                    n += 1

    # 修正样式定义，堵住继承漏洞
    for name in ("Normal",):
        try:
            fix_style(d.styles[name], body_half, lat, ea)
        except KeyError:
            pass
    for st in d.styles:
        try:
            if st.type is not None and st.name and st.name not in ("Normal",):
                rpr = st.element.find(qn("w:rPr"))
                if rpr is not None and rpr.find(qn("w:rFonts")) is not None:
                    fix_style(st, body_half, lat, ea)   # 有字体定义的自定义样式一并统一
        except Exception:
            pass
    return n, roles


# ==================================================================== 诊断
def inspect(path, letters, body_size):
    d = docx.Document(path)
    sec = d.sections[0]
    usable = (sec.page_width - sec.left_margin - sec.right_margin) / 12700.0
    print(f"文件: {path}")
    print(f"页面: 宽 {sec.page_width/12700:.0f}pt  可用正文宽 {usable:.0f}pt  "
          f"页边距 L{sec.left_margin/12700:.0f} R{sec.right_margin/12700:.0f} "
          f"T{sec.top_margin/12700:.0f} B{sec.bottom_margin/12700:.0f}")
    print(f"段落 {len(d.paragraphs)}  表格 {len(d.tables)}")

    # 字号/字体不一致清单
    sizes, fonts, eafonts = {}, {}, {}
    for p in d.paragraphs:
        for r in p.runs:
            if not r.text:
                continue
            sz = r.font.size.pt if r.font.size else "(继承)"
            sizes[sz] = sizes.get(sz, 0) + 1
            rf = r._element.rPr.find(qn("w:rFonts")) if r._element.rPr is not None else None
            asc = rf.get(qn("w:ascii")) if rf is not None else None
            ea = rf.get(qn("w:eastAsia")) if rf is not None else None
            fonts[asc] = fonts.get(asc, 0) + 1
            eafonts[ea] = eafonts.get(ea, 0) + 1
    print("\n[字号分布] (run 数)")
    for k, v in sorted(sizes.items(), key=lambda x: -x[1]):
        print(f"   {k}pt × {v}")
    print("[西文字体]", {k: v for k, v in sorted(fonts.items(), key=lambda x: -x[1])})
    print("[中文字体]", {k: v for k, v in sorted(eafonts.items(), key=lambda x: -x[1])})

    # szCs 检查
    bad = 0
    for p in d.paragraphs:
        for r in p.runs:
            rPr = r._element.rPr
            if rPr is None:
                continue
            sz = rPr.find(qn("w:sz"))
            szcs = rPr.find(qn("w:szCs"))
            a = sz.get(qn("w:val")) if sz is not None else None
            b = szcs.get(qn("w:val")) if szcs is not None else None
            if a is not None and b != a:
                bad += 1
    print(f"[sz≠szCs 的 run] {bad}  ← 不为 0 就会出现「看着字号不一致」")

    # 表格字号
    tsz = set()
    for tb in d.tables:
        for row in tb.rows:
            for c in row.cells:
                for p in c.paragraphs:
                    for r in p.runs:
                        tsz.add(r.font.size.pt if r.font.size else None)
    print(f"[表格字号] {sorted(str(x) for x in tsz)}  ← 应与正文 {body_size}pt 一致")

    # 行距
    ls = {}
    for p in d.paragraphs:
        if p.text.strip():
            ls[str(p.paragraph_format.line_spacing)] = ls.get(str(p.paragraph_format.line_spacing), 0) + 1
    print(f"[行距分布] {ls}")

    # 选项行
    infos = find_option_paragraphs(d, letters)
    print(f"\n[识别到的选项行] {len(infos)} 行（字母集合 {letters}）")
    for i, p, info in infos[:8]:
        print(f"   p{i}: 前缀={info['prefix']!r} 选项={[c for c, _ in info['items']]}")
    if infos:
        cols, w = compute_columns(infos, body_size, 2.0, usable)
        print(f"   自适应列位: {[round(c) for c in cols]} pt"
              + (f"   ⚠ {w}" if w else ""))
    print("\n（只读诊断，未修改文件）")


# ==================================================================== 校验
def verify(src_snapshot, out_path, letters):
    """去空白逐段比对，确保内容零改动。"""
    a = docx.Document(src_snapshot)
    b = docx.Document(out_path)
    norm = lambda s: re.sub(r"\s+", " ", s).strip()
    diffs = []
    for i, (x, y) in enumerate(zip(a.paragraphs, b.paragraphs)):
        if norm(x.text) != norm(y.text):
            diffs.append((i, x.text, y.text))
    if len(a.paragraphs) != len(b.paragraphs):
        diffs.append(("段落数", len(a.paragraphs), len(b.paragraphs)))
    return diffs


# ==================================================================== main
def main():
    ap = argparse.ArgumentParser(description="试卷选项对齐与版式统一")
    ap.add_argument("docx", help="输入 .docx")
    ap.add_argument("-o", "--out", help="输出路径（默认原地覆盖）")
    ap.add_argument("--inspect", action="store_true", help="只诊断，不修改")
    ap.add_argument("--align-only", action="store_true", help="只对齐选项，不动其它版式")
    ap.add_argument("--letters", default="ABCD", help="选项字母集合，如 ABCD（默认）或 ABC")
    ap.add_argument("--body-size", type=float, default=12.0, help="正文字号 pt（默认 12）")
    ap.add_argument("--line-spacing", type=float, default=1.5, help="正文行距（默认 1.5）")
    ap.add_argument("--cols", help="手动指定列位 pt，逗号分隔，如 80,220,360")
    ap.add_argument("--gap", type=float, default=2.0, help="列间隙（字符数，默认 2）")
    ap.add_argument("--lat-font", default=DEFAULT_LAT, help="西文字体（默认 Times New Roman）")
    ap.add_argument("--ea-font", default=DEFAULT_EA, help="中文字体（默认 宋体）")
    ap.add_argument("--no-indent", action="store_true", help="长正文段落不首行缩进")
    ap.add_argument("--no-backup", action="store_true", help="不生成备份")
    args = ap.parse_args()

    src = args.docx
    if not os.path.isfile(src):
        sys.exit(f"找不到文件：{src}")

    if args.inspect:
        inspect(src, args.letters, args.body_size)
        return

    out = args.out or src
    snapshot = src + ".snapshot.docx"
    shutil.copy2(src, snapshot)

    if not args.no_backup:
        bak = f"{os.path.splitext(out)[0]}.bak-{datetime.now():%Y%m%d%H%M}.docx"
        shutil.copy2(src, bak)
        print(f"备份 -> {bak}")

    d = docx.Document(src)

    # ---- 1. 版式统一（先做，列宽计算依赖最终字号）----
    if not args.align_only:
        n, roles = restyle(d, args.body_size, args.line_spacing,
                           args.lat_font, args.ea_font,
                           indent_passage=not args.no_indent)
        print(f"版式统一：处理 {n} 个 run；"
              f"标题分级 {sum(1 for v in roles.values() if v.startswith('title'))} 处")

    # ---- 2. 选项对齐 ----
    cols_pt = None
    if args.cols:
        cols_pt = [float(x) for x in args.cols.split(",")]
    cnt, cols_pt, warns = align_options(d, args.letters, args.body_size,
                                        cols_pt, args.gap)
    print(f"选项对齐：{cnt} 行；列位 {[round(c) for c in cols_pt]} pt")
    for w in warns:
        print(f"   ⚠ {w}")

    d.save(out)
    fixed = sort_docx_xml(out)
    print(f"OOXML 元素顺序修正：{fixed} 处")

    # ---- 3. 校验 ----
    diffs = verify(snapshot, out, args.letters)
    if diffs:
        print("\n[内容差异] （以下应为空白规范化，若出现字词变化请检查）")
        for i, a, b in diffs[:20]:
            print(f"   第{i}段\n      前: {a[:70]!r}\n      后: {b[:70]!r}")
    else:
        print("内容校验：逐段零改动 ✓")

    # 字号一致性抽查
    bad = 0
    dd = docx.Document(out)
    for p in dd.paragraphs:
        for r in p.runs:
            rPr = r._element.rPr
            if rPr is None:
                continue
            sz = rPr.find(qn("w:sz"))
            szcs = rPr.find(qn("w:szCs"))
            a = sz.get(qn("w:val")) if sz is not None else None
            b = szcs.get(qn("w:val")) if szcs is not None else None
            if a is not None and b != a:
                bad += 1
    if bad:
        note = "（--align-only 未做字号统一，属预期；如需统一请去掉该参数）" if args.align_only else ""
        print(f"sz≠szCs 残留：{bad} {note}")

    os.remove(snapshot)
    print(f"\n完成 -> {out}")


if __name__ == "__main__":
    main()
