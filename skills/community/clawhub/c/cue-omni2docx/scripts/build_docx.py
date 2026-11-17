#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
omni2docx — 双层管线：Omni 解析（Agent 层）× 格式生成（用户层）
=================================================================================

定位：完整链路 = 多模态解析（Omni，给 agent）→ agent 整合分析 → 按需生成文档
（给用户）。生成阶段把解析侧已算出的元数据**再利用**回文档——这是超越普通转换
工具的核心：通用转换只吃 markdown，拿不到 grounding/outline/视觉理解/转写。

同一渲染引擎吃两种输入：A) Omni 解析重建（markdown+grounding，页级保真）；
B) agent 工作产物直出（--md file.md，含 [^n] 脚注/〔来源〕标注渲染）。

差异化定位：
  通用格式转换只吃 markdown，丢失 Omni 解析时已算出的结构化信息。本引擎
  **不重复造解析器**——解析全部交给 Omni 原生工具（parse）。我们只做 Omni
  不提供的那部分：**把解析侧能力映射回 Word 原生对象**：

  1. grounded grounding（detail="grounded" 的页锚点）
       -> 在 Word 中于正确的**源页边界插入分页符**（页级保真），保留阅读顺序。
          通用转换（pandoc/docx）对 PDF 源页结构**完全无知**，只能吐连续正文。
  2. 章节结构 / outline（真标题 + 可见目录）
       -> 优先用 read_outline 返回的确定性 H1–H6（官方权威；须与 parse 同会话
          调用——local_result_cache 绑定 bridge 进程）；
          outline 缺失或 coverage=none 时回退为从 Omni 输出的干净 markdown
          保守重建：中文序号"一、二、" → H1，指数型小节"N.XX指数" → H2。
          通用转换对 PDF 正文里无 `#` 的章节只能当成正文。
  3. content（markdown）
       -> 表格 / 列表 / 引用 / 行内 **粗体·斜体·代码·链接** 还原为 Word 原生对象。
  4. 溯源标注 + 图像引用（多模态源：视频/图片/音频/网页）
       -> Omni 多模态解析不返回图像/音频字节，但产出**文本形式的溯源标注**：
          视频帧 `[画面 00:48] 场景: …`（视觉理解描述）、音频转写
          `[说话人0 00:00-01:20] …`（说话人+时间戳）。引擎识别后渲染为区分明显的
          标注段：描述类=灰斜体+底纹（【画面】/【图说】），转写类=标签加粗蓝+正文色
          （可引用）——诉讼证据整合场景直接可用。
          `![alt](data:image;base64,…)` 剥离字节、保留说明（【图片：alt】）。
  5. 多源合并 + agent 整合分析（证据整合）：
       输入 {"title","analysis":{markdown},"sources":[{markdown,grounding,outline,source}]}
       -> analysis 渲染为首章（[^n] 引用照常），每源一章（H1 + 章间分页），
          总目录前置（章内层级自动 +1），页级分页照常。
       -> 文末自动生成「证据溯源附录」：把各源 grounding 页锚点（源第 N–M 页）、
          画面时间点、说话人转写段、章节 outline 回灌成表格——人拿最终文档可
          直接定位原件。`--no-appendix` 关闭。
  6. `--page-marks`：分页符处标注「源第 N 页」（scanned PDF 核对原件场景）。

坐标体系（实测）：
  - grounding.schema_version == "omni.grounding.v1"
  - segments[].content_range_utf8.{start,end} 为 UTF-8 **字节**偏移（引擎内部
    做字节→字符换算）。
  - segments[].grounding.anchors[] = [{kind:"page", value:<1-based 源页码>}]
  - layout（逐元素 bbox）：可用；本引擎当前消费页级锚点，
    元素级坐标保真为后续升级路径。遇解析侧报错时先排除调用侧问题（如
    跨进程作用域），不预设服务端故障，再失败则降级 grounded。

outline schema（来自 bridge dist result-contract.js:418，outlineNodeSchema）：
  { coverage: "complete"|"partial"|"none",
    nodes: [ { id:"node_xxxxxx", level:1-6, title:"...", preview:"..." }, ... ] }
  引擎同时兼容 outline 直接为 list、或包在 {outline:...} 内。

输入 JSON：
  { "markdown": "...", "grounding": {...}, "outline": {...}, "source":"", "detail":"" }

用法：
  python build_docx.py --json in.json --out out.docx
  python build_docx.py --json in.json --out out.docx --no-pagebreak --no-toc
依赖：python-docx（默认 venv 1.2.0）。
"""

import argparse
import json
import re
import sys
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_BREAK, WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import time


# --------------------------------------------------------------------------- #
# 0b. 主题色系统（与 render_pptx.py / render_html.py 完全一致的克制三色）
# --------------------------------------------------------------------------- #
# 全程统一一套色：primary 主 + accent 强调 + ink 墨；背景以白/极浅灰为主。
# 编辑式极简主题：近单色 + 单一克制强调色（仅用于微小标记：序号、短细线），
# 本包制式：不铺色块、不用左 accent 竖条、不用表头填充——层级只靠留白、字重与细灰 hairline 表达。
# hairline=细灰线；muted=灰字；primary 保留为强调色别名。正文与标题文字保持深墨色。
THEME = {
    "default":  {"primary": "#8C6A3F", "ink": "#1A1A1A", "accent": "#8C6A3F",
                 "hairline": "#DCDCDC", "muted": "#6E6E6E", "panel": "#FAFAFA"},
    "academic": {"primary": "#2E4A7A", "ink": "#1A1A1A", "accent": "#2E4A7A",
                 "hairline": "#DCDCDC", "muted": "#6E6E6E", "panel": "#FAFAFA"},
    "gov":      {"primary": "#8A2B2B", "ink": "#1A1A1A", "accent": "#8A2B2B",
                 "hairline": "#DCDCDC", "muted": "#6E6E6E", "panel": "#FAFAFA"},
    "legal":    {"primary": "#7A3B2E", "ink": "#1A1A1A", "accent": "#7A3B2E",
                 "hairline": "#DCDCDC", "muted": "#6E6E6E", "panel": "#FAFAFA"},
    "finance":  {"primary": "#1F6F6B", "ink": "#1A1A1A", "accent": "#1F6F6B",
                 "hairline": "#DCDCDC", "muted": "#6E6E6E", "panel": "#FAFAFA"},
}


def hex_to_rgb(h):
    h = (h or "#000000").lstrip("#")
    if len(h) != 6:
        h = "000000"
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def theme_for(profile):
    return THEME.get(profile, THEME["default"])


def add_para_border(paragraph, side, color_hex, sz=12, space=4):
    """给段落加单边边框（bottom/left/top/right），w:sz 单位 1/8 磅。
    用于封面下划、标题 accent 下划/左条、页脚细线——克制的装饰语言。"""
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = pPr.find(qn("w:pBdr"))
    if pBdr is None:
        pBdr = OxmlElement("w:pBdr")
        pPr.append(pBdr)
    e = OxmlElement("w:%s" % side)
    e.set(qn("w:val"), "single")
    e.set(qn("w:sz"), str(sz))
    e.set(qn("w:space"), str(space))
    e.set(qn("w:color"), color_hex.lstrip("#"))
    pBdr.append(e)


def set_cell_shading(cell, fill):
    """给表格单元格（tcPr）加底纹（幂等：先移除旧 shd，避免重复）。"""
    tcPr = cell._tc.get_or_add_tcPr()
    for ex in list(tcPr):
        if ex.tag == qn("w:shd"):
            tcPr.remove(ex)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill.lstrip("#"))
    tcPr.append(shd)


def style_table(t, theme=None):
    """编辑式极简表格：表头加粗墨色 + 表头底部墨色粗线；行间 hairline；
    无填充、无竖线、无外框——本包表格只留表头底部墨色粗线与行间 hairline，不做斑马纹、不做四边细框。"""
    theme = theme or THEME["default"]
    if not t.rows:
        return
    # 整表：仅底部外框 + 行间 hairline（无竖线、无顶框、无左/右边框）
    tblPr = t._tbl.tblPr
    old = tblPr.find(qn("w:tblBorders"))
    if old is not None:
        tblPr.remove(old)
    borders = OxmlElement("w:tblBorders")
    for edge, (col, sz) in {"bottom": (theme["hairline"], 8),
                            "insideH": (theme["hairline"], 4)}.items():
        e = OxmlElement("w:%s" % edge)
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), str(sz))
        e.set(qn("w:space"), "0")
        e.set(qn("w:color"), col.lstrip("#"))
        borders.append(e)
    tblPr.append(borders)
    for ri, row in enumerate(t.rows):
        for cell in row.cells:
            set_cell_shading(cell, "FFFFFF")
            for para in cell.paragraphs:
                for r in para.runs:
                    if ri == 0:
                        r.font.color.rgb = hex_to_rgb(theme["ink"])
                        r.bold = True
                    else:
                        r.font.color.rgb = hex_to_rgb("#2B2B2B")
            if ri == 0:  # 表头底部墨色粗线
                tcPr = cell._tc.get_or_add_tcPr()
                bdr = tcPr.find(qn("w:tcBorders"))
                if bdr is None:
                    bdr = OxmlElement("w:tcBorders")
                    tcPr.append(bdr)
                for ex in list(bdr):
                    if ex.tag == qn("w:bottom"):
                        bdr.remove(ex)
                e = OxmlElement("w:bottom")
                e.set(qn("w:val"), "single")
                e.set(qn("w:sz"), "12")
                e.set(qn("w:space"), "0")
                e.set(qn("w:color"), theme["ink"].lstrip("#"))
                bdr.append(e)


def accent_heading(p, level, theme=None):
    """编辑式标题装饰：仅 H1 底部一道细灰线（hairline），H2 及以下靠字号层级区分，
    不加左色条、不加粗色块——标题的分量只来自字号与字重。标题文字始终深墨色。"""
    theme = theme or THEME["default"]
    if level <= 1:
        add_para_border(p, "bottom", theme["hairline"], sz=12, space=6)
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(8)
    # H2+：不加任何边框，纯靠字号层级


def cover(doc, title_text, source="", theme=None, kicker="", date_str=None):
    """编辑式极简封面：Title 样式大标题（墨色）+ 标题下 accent 短细线（全格式唯一强调点，
    与 PPTX 封面/HTML hero 一致）+ 来源/日期灰副标；无 kicker 角标、无顶部线——封面只留这一个强调点。
    标题仍用 Title 样式（校验器要求）。kicker 参数保留仅为调用兼容，不再渲染。"""
    theme = theme or THEME["default"]
    t = doc.add_heading(level=0)
    t.add_run(title_text)
    t.paragraph_format.space_after = Pt(14)
    add_para_border(t, "bottom", theme["accent"], sz=16, space=8)
    sub = doc.add_paragraph()
    txt = source or ""
    if date_str:
        txt = (txt + "　·　" + date_str) if txt else date_str
    rs = sub.add_run(txt)
    rs.font.size = Pt(10.5)
    rs.font.color.rgb = hex_to_rgb(theme["muted"])
    sub.paragraph_format.space_after = Pt(20)


# --------------------------------------------------------------------------- #
# 1. 字节偏移
# --------------------------------------------------------------------------- #
def line_byte_offsets(md):
    offsets = []
    pos = 0
    for ln in md.split("\n"):
        offsets.append((ln, pos))
        pos += len(ln.encode("utf-8")) + 1
    return offsets


# --------------------------------------------------------------------------- #
# 2. grounding -> 字节区间到源页码
# --------------------------------------------------------------------------- #
def build_segment_index(grounding):
    if not grounding:
        return []
    index = []
    for s in (grounding.get("segments") or []):
        rng = s.get("content_range_utf8") or {}
        st, en = rng.get("start"), rng.get("end")
        if st is None or en is None:
            continue
        page = None
        for a in (s.get("grounding") or {}).get("anchors") or []:
            if a.get("kind") == "page":
                page = a.get("value")
                break
        index.append((st, en, page))
    index.sort(key=lambda t: t[0])
    return index


def page_for_byte(index, b):
    if not index:
        return None
    for st, en, page in index:
        if st <= b < en:
            return page
    return index[-1][2]


# --------------------------------------------------------------------------- #
# 3. outline -> 规范化（level, title）列表 + 标题→层级映射
# --------------------------------------------------------------------------- #
def build_outline_map(outline):
    """返回 [(level, title), ...]（已过滤非法 level）。"""
    nodes = []
    if not outline:
        return nodes
    if isinstance(outline, list):
        raw = outline
    elif isinstance(outline, dict):
        raw = outline.get("nodes") or outline.get("outline") or []
    else:
        return nodes
    for n in raw:
        if not isinstance(n, dict):
            continue
        lvl = n.get("level")
        title = (n.get("title") or n.get("text") or "").strip()
        if not title:
            continue
        try:
            lvl = int(lvl)
        except (TypeError, ValueError):
            lvl = 1
        if lvl < 1:
            lvl = 1
        if lvl > 6:
            lvl = 6
        nodes.append((lvl, title))
    return nodes


def norm(s):
    return re.sub(r"\s+", "", s or "")


# 章节前缀（中文数字序号 / 阿拉伯数字序号 / 括号）——用于把 "1.标普500指数" 这类
# outline 标题匹配到正文 "1.标普 500 指数：该指数..." 段落。
LEAD_TOKEN = re.compile(r"^[0-9]+[.、)）]|^[一二三四五六七八九十百千]+[.、]?|^[（(]")


# 当 JSON 未提供 outline 字段时（read_outline 返回 coverage=none、或调用侧
# 拿不到 result_id 等），从 Omni 输出的
# 干净 markdown 保守重建章节层级。仅捕获歧义极低的模式，避免误把列表项当标题：
#   H1：中文序号段 "一、美国" / "二、德国" ……（行首无缩进）
#   H2：数字序号 + 指数名 "1.标普 500 指数" / "2.纳斯达克 100 指数" ……
#       （以"指数"二字识别，排除含 ETF/基金代码的推荐列表项）
CN_SEC = re.compile(r"^[一二三四五六七八九十百千]+[、.．]")
SUBSEC = re.compile(r"^\s*\d+[.、)）]")


def derive_outline_from_markdown(md):
    """从 Omni markdown 保守重建章节层级（read_outline 不可用时）。

    捕获三类高置信度结构：
      H1：中文序号段 "一、美国" / "二、德国" …（行首无缩进）
      H2：数字序号 + 指数名 "1.标普 500 指数" / "2.纳斯达克 100 指数"
          （以"指数"识别，排除含 ETF/基金代码的推荐列表项）
      H1–H6：文档自带的 markdown 标题（### 证券研究报告 等）→ 也纳入目录
    """
    nodes = []
    seen = set()
    HM = re.compile(r"^(#{1,6})\s+(.*)$")
    for line in md.split("\n"):
        s = line.strip()
        if not s:
            continue
        mh = HM.match(s)
        if mh:
            lvl = min(int(len(mh.group(1))), 6)
            title = mh.group(2).strip()
            if title:
                key = (lvl, title)
                if key not in seen:
                    seen.add(key)
                    nodes.append((lvl, title))
            continue
        m = CN_SEC.match(s)
        if m:
            title = s.rstrip("。")
            key = (1, title)
            if key not in seen:
                seen.add(key)
                nodes.append((1, title))
            continue
        m2 = SUBSEC.match(s)
        if m2:
            cut = re.search(r"[：:]", s)
            head = s[: cut.start()] if cut else s
            if "指数" in head:
                title = head.rstrip("。")
                key = (2, title)
                if key not in seen:
                    seen.add(key)
                    nodes.append((2, title))
    return nodes


def match_outline_level(block_text, outline_map):
    """返回 (level, heading_text, body_text)；无匹配返回 None。

    body_text 为标题之后剩余的正文（用于避免把整段长描述提升为 heading）。
    """
    if not outline_map:
        return None
    bt = block_text.strip()
    bn = norm(bt)
    for lvl, title in outline_map:
        tn = norm(title)
        if not tn:
            continue
        # 情况 A：段落直接以 outline 标题开头（含序号前缀已对齐）
        if bn.startswith(tn):
            body = bt[len(title):].lstrip("：: ") if bt.startswith(title) else bt
            return (lvl, title, body)
        # 情况 B：段落开头有章节序号，去掉后再比对（官方 outline 标题不含序号时）
        m = LEAD_TOKEN.match(bt)
        if m:
            rest = bt[m.end():]
            if norm(rest).startswith(tn):
                body = rest[len(title):].lstrip("：: ") if rest.startswith(title) else rest
                return (lvl, title, body)
    return None


# --------------------------------------------------------------------------- #
# 3b. 溯源标注块（视觉理解描述 + 音视频转写，不含图像/音频字节）
# --------------------------------------------------------------------------- #
# Omni 解析多模态源时不返回图像/音频字节，但产出**文本形式的溯源标注**：
#   - 视频/图片：[画面 00:48] 场景: 这张图片展示了……  → 视觉理解描述
#   - 音频/视频：[说话人0 00:00-01:20] 就是时间非常长的……  → 说话人+时间戳转写
#   - 网页内图像：![Cue Logo](data:image;base64,…)  → 图像引用（剥离字节留说明）
# 这些是"Omni 看见/听见了什么"而非文档原文，渲染时必须与作者正文区分——
# 证据整合场景（诉讼文书等）尤其依赖说话人与时间戳的可引用性。
VISUAL_FRAME = re.compile(r"^\[画面\s*([\d:]+)\]\s*(.*)$")
AUDIO_TURN = re.compile(
    r"^\[(?:说话人\s*(\d+)\s+)?"       # 可选说话人编号
    r"(\d{1,2}:[0-5]?\d(?::[0-5]?\d)?"  # 起始时间 MM:SS / HH:MM:SS
    r"(?:\s*[-–—~]\s*\d{1,2}:[0-5]?\d(?::[0-5]?\d)?)?)"  # 可选结束时间
    r"\]\s*(.*)$"
)
VISUAL_LEAD = re.compile(r"^(场景[:：]|这张图片|图片展示|图中展示|图[：:]|【图片|字幕[:：])")


def classify_visual(text):
    """识别"溯源标注"块。返回 (label, body, kind)；非标注返回 None。
    kind: "desc"=视觉/场景描述（灰斜体+底纹）；"turn"=说话人/时间戳转写（正文色，
    可引用）。高置信前缀，正文里罕见以此开篇，误判风险低。"""
    t = (text or "").strip()
    if not t:
        return None
    m = VISUAL_FRAME.match(t)
    if m:
        return ("【画面 %s】" % m.group(1), m.group(2).strip(), "desc")
    m = AUDIO_TURN.match(t)
    if m:
        spk, ts, body = m.group(1), m.group(2), m.group(3).strip()
        label = ("说话人%s %s" % (spk, ts)) if spk is not None else ts
        return ("【%s】" % label, body, "turn")
    if VISUAL_LEAD.match(t):
        return ("【图说】", t, "desc")
    return None


# --------------------------------------------------------------------------- #
# 4. markdown -> 块（带字节偏移）
# --------------------------------------------------------------------------- #
BLOCK_RE = {
    "heading": re.compile(r"^(#{1,6})\s+(.*)$"),
    "hr": re.compile(r"^(\s*([-*_])\s*){3,}$"),
    "ul": re.compile(r"^\s*[-*+]\s+(.*)$"),
    "ol": re.compile(r"^\s*\d+[.)]\s+(.*)$"),
    "quote": re.compile(r"^\s*>\s?(.*)$"),
    "table_row": re.compile(r"^\s*\|(.+)\|\s*$"),
    "table_sep": re.compile(r"^\s*\|?[\s:|-]*-[\s:|-]*\|?\s*$"),
}


def parse_blocks(md):
    offsets = line_byte_offsets(md)
    blocks = []
    i, n = 0, len(offsets)
    while i < n:
        ln, bstart = offsets[i]
        raw = ln.strip()
        if raw == "":
            i += 1
            continue
        m = BLOCK_RE["heading"].match(ln)
        if m:
            blocks.append(("heading", (len(m.group(1)), m.group(2).strip()), bstart))
            i += 1
            continue
        if BLOCK_RE["hr"].match(ln):
            blocks.append(("hr", None, bstart))
            i += 1
            continue
        if BLOCK_RE["table_row"].match(ln) and i + 1 < n and BLOCK_RE["table_sep"].match(offsets[i + 1][0]):
            header = split_row(ln)
            i += 2
            rows = []
            while i < n and BLOCK_RE["table_row"].match(offsets[i][0].strip()) and offsets[i][0].strip() != "":
                rows.append(split_row(offsets[i][0]))
                i += 1
            blocks.append(("table", (header, rows), bstart))
            continue
        if BLOCK_RE["table_row"].match(ln):
            # 无分隔行的表格（xlsx/部分导出常见）：连续 | 行按表处理，首行作表头。
            # 至少 2 行且绝大多数行含 >=2 个单元格才判表；不达标的 | 行按普通段落
            # 消费（本分支必须至少消费 1 行，否则 para 空转死循环）。
            rows = []
            j = i
            while j < n and BLOCK_RE["table_row"].match(offsets[j][0].strip()) and offsets[j][0].strip() != "":
                rows.append(split_row(offsets[j][0]))
                j += 1
            if len(rows) >= 2 and sum(1 for r in rows if len(r) >= 2) >= len(rows) * 0.8:
                blocks.append(("table", (rows[0], rows[1:]), bstart))
            else:
                txt = clean_cjk_spaces(" ".join(offsets[k][0].strip() for k in range(i, j)))
                v = classify_visual(txt)
                blocks.append(("visual", v, bstart) if v else ("para", txt, bstart))
            i = j
            continue
        if BLOCK_RE["quote"].match(ln):
            buf = []
            while i < n and BLOCK_RE["quote"].match(offsets[i][0]):
                buf.append(BLOCK_RE["quote"].match(offsets[i][0]).group(1))
                i += 1
            blocks.append(("quote", " ".join(buf).strip(), bstart))
            continue
        if BLOCK_RE["ul"].match(ln) or BLOCK_RE["ol"].match(ln):
            is_ol = bool(BLOCK_RE["ol"].match(ln))
            buf = []
            while i < n:
                ml = BLOCK_RE["ul"].match(offsets[i][0])
                ol = BLOCK_RE["ol"].match(offsets[i][0])
                if is_ol and ol:
                    buf.append(ol.group(1).strip())
                    i += 1
                elif (not is_ol) and ml:
                    buf.append(ml.group(1).strip())
                    i += 1
                else:
                    break
            blocks.append(("ol" if is_ol else "ul", buf, bstart))
            continue
        buf = []
        while i < n:
            line = offsets[i][0]
            cur = line.strip()
            if cur == "" or any(r.match(line) for r in (BLOCK_RE["heading"], BLOCK_RE["hr"], BLOCK_RE["ul"], BLOCK_RE["ol"], BLOCK_RE["quote"], BLOCK_RE["table_row"])):
                break
            # 章节/小节边界：上一行已累计内容，当前行是新的章节/小节标题时断开，
            # 避免 "四、日本 目前跟踪… 1.东证指数：…" 被并成一段而吞掉小节标题。
            if buf and (CN_SEC.match(cur) or (SUBSEC.match(line) and "指数" in (cur.split("：")[0] if "：" in cur else cur))):
                break
            buf.append(cur)
            i += 1
        text = clean_cjk_spaces(" ".join(buf))
        v = classify_visual(text)
        if v:
            blocks.append(("visual", v, bstart))
        else:
            blocks.append(("para", text, bstart))
    return blocks


def split_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


# --------------------------------------------------------------------------- #
# 5. 行内 markdown
# --------------------------------------------------------------------------- #
INLINE_RE = re.compile(
    r"(\!\[[^\]]*\]\([^)]*\)"          # 图像引用 ![alt](src)（含 data:image base64）
    r"|\[\^[^\]]+\]"                    # 脚注引用 [^n]（渲染为上标）
    r"|〔[^〕]*〕"                       # 来源标注 〔来源：…〕（渲染为灰色小字）
    r"|\*\*.+?\*\*(?!\*)"               # 粗体（(?!\*)：***粗斜体*** 须闭合在最后，避免残留 *）
    r"|__.+?__(?!\_)"                   # 粗体（下划线）
    r"|`.+?`"                           # 行内代码
    r"|\[[^\]]+\]\([^)]+\)"             # 链接
    r"|\*[^\s*][^*\n]*\*"               # 斜体
    r"|_[^\s_][^_\n]*_)"                # 斜体（下划线）
)


def _chain(outer, inner):
    """组合两个 run 修饰函数（外层先、内层后），供嵌套行内解析用。"""
    def f(r):
        if outer:
            outer(r)
        inner(r)
    return f


def add_inline(paragraph, text, fmt=None):
    """行内 markdown → Word runs。fmt 为可选 run 修饰函数，嵌套时由外向内链式
    叠加（如粗体内套行内代码：递归解析内层，外层粗体 + 内层 Consolas 同时生效，
    反引号不残留——递交类文书一个字符都不该多出来）。"""
    pos = 0
    for m in INLINE_RE.finditer(text):
        if m.start() > pos:
            r = paragraph.add_run(text[pos:m.start()])
            if fmt:
                fmt(r)
        tok = m.group(0)
        if tok.startswith("!["):
            # 图像引用：剥离图像字节（base64 数据 URI 动辄数 MB），仅保留可读说明。
            # 注意 inner 保留右括号（tok[2:]），且必须推进 pos 再 continue，
            # 否则尾部 if pos < len(text) 会把整段原文重复输出。
            inner = tok[2:]
            m2 = re.match(r"^([^\]]*)\]\(([^)]*)\)$", inner)
            pos = m.end()
            if not m2:
                r = paragraph.add_run(tok)
                if fmt:
                    fmt(r)
                continue
            alt, src = m2.group(1).strip(), m2.group(2).strip()
            if src.startswith("data:image") and len(src) > 120:
                r = paragraph.add_run("【图片：%s】（图像数据已省略，仅保留说明）" % (alt or "无说明"))
                r.font.color.rgb = RGBColor(0x80, 0x80, 0x80)
            elif src.startswith("data:image"):
                r = paragraph.add_run("【图片：%s】" % (alt or "无说明"))
                r.font.color.rgb = RGBColor(0x80, 0x80, 0x80)
            elif alt:
                r = paragraph.add_run("【图】%s" % alt)
                r.font.color.rgb = RGBColor(0x80, 0x80, 0x80)
            if fmt:
                fmt(r)
            # 纯装饰图（无 alt 无说明）直接丢弃，不污染 docx
            continue
        if tok.startswith("[^"):
            # 脚注引用 [^n]：上标编号 + 深蓝，文末「注释」节给出定义
            r = paragraph.add_run(tok[2:-1])
            r.font.superscript = True
            r.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
            if fmt:
                fmt(r)
        elif tok.startswith("〔"):
            # 来源标注 〔来源：…〕：灰色小字，正文与证据可溯源的粘合标记
            r = paragraph.add_run(tok)
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(0x80, 0x80, 0x80)
            if fmt:
                fmt(r)
        elif tok.startswith("**") or tok.startswith("__"):
            # 粗体：递归解析内层（可能还套 code/link/脚注），样式链式叠加
            add_inline(paragraph, tok[2:-2],
                       _chain(fmt, lambda r: setattr(r, "bold", True)))
        elif tok.startswith("`"):
            r = paragraph.add_run(tok[1:-1])
            r.font.name = "Consolas"
            r.font.size = Pt(9)
            if fmt:
                fmt(r)
        elif tok.startswith("["):
            label = tok[1:tok.index("](")]
            r = paragraph.add_run(label)
            r.font.color.rgb = RGBColor(0x05, 0x63, 0xC1)
            if fmt:
                fmt(r)
        else:
            inner = tok[1:-1]
            r = paragraph.add_run(inner)
            # CJK 伪斜体渲染难看：含中文的强调用加粗，纯西文保留斜体
            if re.search(r"[\u4e00-\u9fff]", inner):
                r.bold = True
            else:
                r.italic = True
            if fmt:
                fmt(r)
        pos = m.end()
    if pos < len(text):
        r = paragraph.add_run(text[pos:])
        if fmt:
            fmt(r)


# --------------------------------------------------------------------------- #
# 6. 渲染 + 分页 + 标题提升 + 目录
# --------------------------------------------------------------------------- #
def insert_toc(doc, outline_map, theme=None):
    theme = theme or THEME["default"]
    h = doc.add_heading(level=1)
    add_inline(h, "目录")
    add_para_border(h, "bottom", theme["hairline"], sz=14, space=6)
    for lvl, title in outline_map:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Pt(18 * (lvl - 1) + 6)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(title)
        if lvl == 1:
            r.bold = True
            r.font.color.rgb = hex_to_rgb(theme["ink"])
        else:
            r.font.color.rgb = hex_to_rgb(theme["muted"])


def render(doc, blocks, seg_index, outline_map, use_pagebreak, use_toc, page_marks=False, level_offset=0, footnotes=None, indent_first=0, table_style="Light Grid Accent 1", quote_east=None, theme=None):
    theme = theme or THEME["default"]
    if use_toc and outline_map:
        insert_toc(doc, outline_map, theme)

    prev_page = None
    page_breaks = 0
    for btype, payload, bstart in blocks:
        page = page_for_byte(seg_index, bstart) if seg_index else None

        if use_pagebreak and seg_index and page is not None and prev_page is not None and page != prev_page:
            p = doc.add_paragraph()
            p.add_run().add_break(WD_BREAK.PAGE)
            page_breaks += 1
            if page_marks:
                # 场景2（scanned PDF→Word）：标注源页码，改稿/核对时可直接对照原件
                pm = doc.add_paragraph()
                pm.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                rm = pm.add_run("── 源第 %s 页 ──" % page)
                rm.font.size = Pt(9)
                rm.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
        if page is not None:
            prev_page = page

        # heading 提升：outline 优先级高于 markdown 猜测
        if btype == "para":
            hit = match_outline_level(payload, outline_map)
            if hit is not None:
                lvl, heading, body = hit
                h = doc.add_heading(level=min(lvl + level_offset, 6))
                add_inline(h, heading)
                accent_heading(h, min(lvl + level_offset, 6), theme)
                if body:
                    p = doc.add_paragraph()
                    add_inline(p, body)
                continue

        if btype == "heading":
            level, text = payload
            h = doc.add_heading(level=min(level + level_offset, 6))
            add_inline(h, text)
            accent_heading(h, min(level + level_offset, 6), theme)
        elif btype == "para":
            p = doc.add_paragraph(); add_inline(p, payload)
            if indent_first:
                # 场景制式：公文/法律/学术正文首行缩进 2 字符（视觉标注段不缩进）
                p.paragraph_format.first_line_indent = Pt(indent_first)
        elif btype == "hr":
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            add_para_border(p, "bottom", theme["hairline"], sz=8, space=2)
            p.paragraph_format.space_after = Pt(6)
        elif btype in ("ul", "ol"):
            # 每个列表条目也按 outline 匹配：命中则提升为标题（小节标题），
            # 未命中保持列表项（真列表不受影响）。
            style = "List Bullet" if btype == "ul" else "List Number"
            for it in payload:
                hit = match_outline_level(it, outline_map)
                if hit is not None:
                    lvl, heading, body = hit
                    h = doc.add_heading(level=min(lvl + level_offset, 6))
                    add_inline(h, heading)
                    accent_heading(h, min(lvl + level_offset, 6), theme)
                    if body:
                        p = doc.add_paragraph()
                        add_inline(p, body)
                else:
                    p = doc.add_paragraph(style=style)
                    add_inline(p, it)
        elif btype == "quote":
            p = doc.add_paragraph(); p.paragraph_format.left_indent = Pt(18)
            add_para_border(p, "left", theme["hairline"], sz=18, space=8)
            if quote_east:
                add_inline(p, payload, fmt=lambda r: set_run_east(r, quote_east))
            else:
                add_inline(p, payload)
            # CJK 伪斜体渲染难看：引用块用灰色 + 细灰左线区分，不用斜体、不用底纹
            for r in p.runs:
                r.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
        elif btype == "visual":
            label, body, kind = payload
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Pt(16)
            add_para_border(p, "left", theme["hairline"], sz=18, space=8)
            rl = p.add_run(label + ("  " if body else ""))
            rl.bold = True
            rl.font.color.rgb = hex_to_rgb(theme["ink"])
            if body:
                rb = p.add_run(body)
                if kind == "desc":
                    # 视觉/场景描述：灰色 + 细灰左线，表明是 Omni 看见的，非原文
                    # （不用斜体——CJK 伪斜体渲染难看；不铺底纹——编辑式极简）
                    rb.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
                # kind == "turn"：说话人/时间戳转写保持正文色，便于引用
        elif btype == "table":
            header, rows = payload
            # 护栏：列数不一致的"假表"（Omni 偶发锯齿布局表）降级为段落，避免破碎表格
            ncols = set([len(header)] + [len(r) for r in rows])
            if len(ncols) > 1 or len(header) == 0:
                for r in [header] + rows:
                    p = doc.add_paragraph()
                    add_inline(p, "　".join(c.strip() for c in r))
                continue
            ncol = len(header)
            t = doc.add_table(rows=1, cols=ncol)
            try:
                t.style = table_style
            except KeyError:
                t.style = "Table Grid"
            for c in range(ncol):
                cell = t.rows[0].cells[c]
                cell.text = ""
                add_inline(cell.paragraphs[0], header[c] if c < len(header) else "")
                for rr in cell.paragraphs[0].runs:
                    rr.bold = True
            for row in rows:
                cells = t.add_row().cells
                for c in range(ncol):
                    cells[c].text = ""
                    add_inline(cells[c].paragraphs[0], row[c] if c < len(row) else "")
            style_table(t, theme)  # 编辑式极简：表头墨色加粗+底线、行间 hairline、无填充
    # 文末「注释」节：脚注定义（agent 产物引用约定的落点）
    if footnotes:
        h = doc.add_heading(level=min(1 + level_offset, 6))
        add_inline(h, "注释")
        accent_heading(h, min(1 + level_offset, 6), theme)
        for label, text in footnotes:
            p = doc.add_paragraph()
            r = p.add_run("[%s] " % label)
            r.bold = True
            add_inline(p, text)
    return page_breaks


# --------------------------------------------------------------------------- #
# 6b. 中文渲染 + 保真工具
# --------------------------------------------------------------------------- #
_CJK = r"[\u3000-\u303f\u4e00-\u9fff\uff00-\uffef]"


def clean_cjk_spaces(text):
    """去掉软换行拼接引入的空格：紧贴 CJK 字符两侧的空白按中文排版习惯删除。
    既消除'核心 资产'这类行间多余空格，又保留英文词间空格。"""
    text = re.sub(r"\s+(?=" + _CJK + r")", "", text)
    text = re.sub(r"(?<=" + _CJK + r")\s+", "", text)
    return text


def set_shading(paragraph, fill):
    """给段落加底纹（w:shd），让视觉理解描述与正文一眼区分。"""
    pPr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    pPr.append(shd)


def set_run_east(run, eastasia):
    """run 级中文字体（w:eastAsia）——引用块/标注段的楷体等场景字体。"""
    rPr = run._element.get_or_add_rPr()
    rf = rPr.get_or_add_rFonts()
    rf.set(qn("w:eastAsia"), eastasia)


def add_page_number_footer(doc, source="", theme=None):
    """页脚：顶部 accent 细线 + 来源(左,灰) + PAGE 域页码(右)；域随分页自动更新。"""
    theme = theme or THEME["default"]
    sec = doc.sections[0]
    p = sec.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    add_para_border(p, "top", theme["hairline"], sz=6, space=2)
    if source:
        rs = p.add_run(source)
        rs.font.size = Pt(8)
        rs.font.color.rgb = hex_to_rgb(theme["muted"])
        p.add_run("\t")
        from docx.enum.text import WD_TAB_ALIGNMENT
        avail = sec.page_width - sec.left_margin - sec.right_margin
        p.paragraph_format.tab_stops.add_tab_stop(avail, WD_TAB_ALIGNMENT.RIGHT)
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), r"PAGE \* MERGEFORMAT")
    r = OxmlElement("w:r")
    t = OxmlElement("w:t")
    t.text = "1"
    r.append(t)
    fld.append(r)
    p._p.append(fld)


# emoji / 符号装饰：法院等正式文书不合适（部分字体显示为方框）。
# --strip-emoji 剥离；校验器对源文同样剥离，保证开关一致时不误报"丢失"。
EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF"
    "\u2B00-\u2BFF\uFE0F\u2705\u274C\u2757\u3030\u303D\u3297\u3299]"
)


def strip_emoji(text):
    return EMOJI_RE.sub("", text)


# --------------------------------------------------------------------------- #
# 6b-0. 场景制式预设（转换参数由"文档用在什么场景"决定，不由默认排版决定）
# --------------------------------------------------------------------------- #
# 用户在 agent 中用本 skill 转换时，产物会进入具体场景，各场景有成熟制式：
#   gov      公文（GB/T 9704-2012）：仿宋_GB2312 三号、固定行距 28 磅、首行缩进 2 字符、
#            页边距 上3.7/下3.5/左2.8/右2.6cm
#   legal    诉讼/法律文书：仿宋_GB2312 四号、行距 24 磅、首行缩进 2 字符；
#            证据溯源（页码标注/转写时间戳）是该场景的刚需 → agent 应主动建议 --page-marks
#   finance  金融研报/尽调：宋体五号、标题黑体、表格保真优先（本引擎默认即贴近此制式）
#   academic 论文/报告：宋体小四、1.5 倍行距、首行缩进 2 字符
# 字号对照：三号=16pt 四号=14pt 小四=12pt 五号=10.5pt
DOC_PROFILES = {
    "gov": {
        "body_east": "仿宋_GB2312", "body_latin": "Times New Roman", "body_size": 16,
        "heading_east": "黑体", "heading_sizes": [16, 16, 16, 16, 16, 16],
        "title_size": 22,  # 二号（公文文件标题）
        "line_spacing": 28, "first_line_indent": 2, "table_style": "Table Grid",
        "margins_cm": {"top": 3.7, "bottom": 3.5, "left": 2.8, "right": 2.6},
        "page_number": True, "quote_east": "楷体",
    },
    "legal": {
        "body_east": "仿宋_GB2312", "body_latin": "Times New Roman", "body_size": 14,
        "heading_east": "黑体", "heading_sizes": [16, 15, 14, 14, 14, 14],
        "title_size": 22, "line_spacing": 24, "first_line_indent": 2,
        "table_style": "Table Grid",
        "page_number": True, "quote_east": "楷体",
    },
    "finance": {
        "body_east": "宋体", "body_size": 10.5, "heading_east": "黑体",
        "heading_sizes": [16, 14, 13, 12, 12, 12], "title_size": 20,
        "table_style": "Light Grid Accent 1",
    },
    "academic": {
        "body_east": "宋体", "body_size": 12, "heading_east": "黑体",
        "heading_sizes": [15, 14, 13, 12, 12, 12], "title_size": 18,
        "line_spacing": 1.5, "first_line_indent": 2, "table_style": "Table Grid",
        "quote_east": "楷体",
    },
    "default": {
        "heading_east": "黑体",
        "heading_sizes": [16, 14, 13, 12, 12, 12], "title_size": 20,
        "table_style": "Light Grid Accent 1",
    },
}


def set_cjk_font(style, eastasia, latin=None):
    """给样式设置东亚字体，避免 Word 用西文字体渲染中文导致字体不一致/缺字。"""
    style.font.name = latin or eastasia
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.get_or_add_rFonts()
    rfonts.set(qn("w:eastAsia"), eastasia)
    rfonts.set(qn("w:ascii"), latin or eastasia)
    rfonts.set(qn("w:hAnsi"), latin or eastasia)


BLACK = RGBColor(0, 0, 0)


def apply_doc_fonts(doc, cfg=None):
    """按场景制式套字体/字号/行距/页边距。cfg 为 DOC_PROFILES 条目；缺省保持原行为。"""
    cfg = cfg or {}
    body_east = cfg.get("body_east", "宋体")
    heading_east = cfg.get("heading_east", "黑体")
    set_cjk_font(doc.styles["Normal"], body_east, cfg.get("body_latin"))
    if "body_size" in cfg:
        doc.styles["Normal"].font.size = Pt(cfg["body_size"])
    hsz = cfg.get("heading_sizes") or [None] * 6
    for i in range(1, 7):
        try:
            st = doc.styles["Heading %d" % i]
        except KeyError:
            continue
        set_cjk_font(st, heading_east)
        st.font.color.rgb = BLACK  # 覆盖 Office 模板默认蓝，避免"一眼模板货"
        if hsz[i - 1]:
            st.font.size = Pt(hsz[i - 1])
            st.font.bold = True
    try:
        st = doc.styles["Title"]
        set_cjk_font(st, heading_east)
        st.font.color.rgb = BLACK
        if cfg.get("title_size"):
            st.font.size = Pt(cfg["title_size"])
    except KeyError:
        pass
    if "line_spacing" in cfg:
        ls = cfg["line_spacing"]
        if isinstance(ls, str):
            # 容错 agent 自定义 profile 的字符串写法：'28pt'/'28磅'→固定磅值，
            # '1.5倍'/'1.5x'→倍数；裸数字字符串按 ≥12 磅 / <12 倍数启发式
            m = re.match(r"^([\d.]+)\s*(pt|磅|倍|x)?$", ls.strip().lower())
            if not m:
                raise ValueError("line_spacing 无法解析: %r（示例：28 / '28pt' / 1.5 / '1.5倍'）" % ls)
            val = float(m.group(1))
            unit = m.group(2)
            if unit in ("pt", "磅") or (unit is None and val >= 12):
                ls = Pt(val)
            else:
                ls = val
        else:
            ls = Pt(ls) if ls >= 12 else ls  # ≥12 视为固定磅值，否则倍数
        doc.styles["Normal"].paragraph_format.line_spacing = ls
    if "margins_cm" in cfg:
        from docx.shared import Cm
        sec = doc.sections[0]
        m = cfg["margins_cm"]
        sec.top_margin, sec.bottom_margin = Cm(m["top"]), Cm(m["bottom"])
        sec.left_margin, sec.right_margin = Cm(m["left"]), Cm(m["right"])


def extract_title(md):
    """从显式封面标记行提取标题；返回 (title, md_without_title)。

    支持三种显式标记：`标题：xxx` / `题目：xxx` / `Title: xxx`（大小写不敏感）。
    只认显式标记、不做"首行像标题就提"的启发式——误提正文首行会静默毁掉
    正文结构（该行会从正文消失）；需要封面标题时 agent/用户显式给标记，
    或用各渲染器的 --title 直接指定。
    """
    m = re.match(r"^\s*(?:标题|题目|title)\s*[:：]\s*(.+?)\s*(?:\n|$)", md, re.IGNORECASE)
    if not m:
        return None, md
    return m.group(1).strip(), re.sub(r"^\s*(?:标题|题目|title)\s*[:：].*(?:\n|$)", "", md,
                                      count=1, flags=re.IGNORECASE)


FOOTNOTE_DEF = re.compile(r"^\[\^([^\]]+)\]:\s*(.*)$")


def extract_footnotes(md):
    """剥离脚注定义行 `[^n]: text`；返回 (md_clean, footnotes)。
    agent 工作产物的引用约定：正文 `[^n]` 上标引用，文末由引擎渲染「注释」节。"""
    foot, lines = [], []
    for ln in md.split("\n"):
        m = FOOTNOTE_DEF.match(ln.strip())
        if m and m.group(2).strip():
            foot.append((m.group(1), m.group(2).strip()))
        else:
            lines.append(ln)
    return "\n".join(lines), foot


# --------------------------------------------------------------------------- #
# 6c. 证据溯源附录：把解析侧元数据（grounding/outline/画面/转写）再利用到转换
# --------------------------------------------------------------------------- #
# 完整链路：多模态解析 → agent 整合分析 → 按需生成文档。生成时把各源解析时
# 已算出的结构化信息（源页锚点、章节 outline、画面时间点、说话人时间段）回灌，
# 自动产出「证据溯源附录」——人拿最终文档可直接定位到每个源的页码/时间点。
# 通用转换工具没有解析元数据，做不到这一层。
def collect_provenance(md, grounding, outline_map):
    """从源 markdown + grounding 采集可溯源位置。返回 dict：
    pages      —— grounding 页锚点去重排序列表（可能为空）
    frames     —— [画面 HH:MM] 时间点列表
    turns      —— [(speaker, ts), ...] 说话人转写段
    headings   —— outline 章节数
    kind       —— 自动推断的源类型（视频/音频/文档/网页/文本）"""
    pages = sorted({p for _, _, p in build_segment_index(grounding)} - {None}) if grounding else []
    frames, turns = [], []
    for ln in (md or "").split("\n"):
        t = ln.strip()
        m = VISUAL_FRAME.match(t)
        if m:
            frames.append(m.group(1))
            continue
        m = AUDIO_TURN.match(t)
        if m:
            turns.append((m.group(1) or "", m.group(2)))
    if frames:
        kind = "视频/图片（画面描述）"
    elif turns:
        kind = "音视频（说话人转写）"
    elif pages:
        kind = "PDF/文档（页锚点）"
    else:
        kind = "网页/文本"
    return {
        "pages": pages,
        "frames": frames,
        "turns": turns,
        "headings": len(outline_map or []),
        "kind": kind,
    }


def fmt_pages(pages):
    """[1,2,3,7] -> '第 1–3、7 页'。"""
    if not pages:
        return ""
    runs, s, e = [], pages[0], pages[0]
    for p in pages[1:]:
        if p == e + 1:
            e = p
        else:
            runs.append((s, e)); s = e = p
    runs.append((s, e))
    return "第 " + "、".join(("%d" % a) if a == b else ("%d–%d" % (a, b)) for a, b in runs) + " 页"


def render_provenance_appendix(doc, prov_rows, table_style="Table Grid", theme=None):
    """文末「证据溯源附录」：每源一行（源 | 类型 | 可溯源位置）。"""
    theme = theme or THEME["default"]
    pb = doc.add_paragraph()
    pb.add_run().add_break(WD_BREAK.PAGE)
    h = doc.add_heading(level=1)
    add_inline(h, "证据溯源附录")
    accent_heading(h, 1, theme)
    note = doc.add_paragraph()
    rn = note.add_run("以下位置由 Omni 解析元数据（grounded 页锚点 / 画面时间点 / 说话人转写）自动生成，"
                      "可直接对照原件定位。")
    rn.font.size = Pt(9)
    rn.font.color.rgb = RGBColor(0x80, 0x80, 0x80)
    t = doc.add_table(rows=1, cols=3)
    try:
        t.style = table_style
    except KeyError:
        t.style = "Table Grid"
    for c, head in enumerate(("证据源", "类型", "可溯源位置")):
        cell = t.rows[0].cells[c]
        cell.text = ""
        r = cell.paragraphs[0].add_run(head)
        r.bold = True
    for name, kind, loc in prov_rows:
        cells = t.add_row().cells
        for c, val in enumerate((name, kind, loc)):
            cells[c].text = ""
            add_inline(cells[c].paragraphs[0], val)
    style_table(t, theme)  # 编辑式极简：表头墨色加粗+底线、行间 hairline、无填充


# --------------------------------------------------------------------------- #
# 7. 入口
# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(description="Omni grounded+outline -> Word 映射引擎")
    ap.add_argument("--json", help="中间 JSON（markdown+grounding+outline）")
    ap.add_argument("--out", required=True)
    ap.add_argument("--no-pagebreak", action="store_true")
    ap.add_argument("--no-toc", action="store_true", help="跳过 outline 目录/标题提升")
    ap.add_argument("--page-marks", action="store_true",
                    help="分页符处标注「源第 N 页」（scanned PDF 核对原件场景）")
    ap.add_argument("--no-appendix", action="store_true",
                    help="合并模式不生成文末「证据溯源附录」")
    ap.add_argument("--profile", default="default",
                    help="场景制式：预设名（gov/legal/finance/academic/default），"
                         "或内联 JSON / .json 文件路径——agent 可按场景知识自定义任意"
                         "排版参数（body_east/body_size/heading_east/line_spacing/"
                         "first_line_indent/margins_cm/table_style/heading_sizes 等）")
    ap.add_argument("--md", help="直接输入 markdown 文件（agent 工作产物→docx，免中间 JSON）")
    ap.add_argument("--page-numbers", action="store_true",
                    help="页脚居中插入 PAGE 域页码（递交/打印件；gov/legal 预设默认开）")
    ap.add_argument("--strip-emoji", action="store_true",
                    help="剥离 emoji/装饰符号（法院等正式文书不合适、部分字体显示为方框）；"
                         "校验器对源文同步剥离，不会误报丢失")
    args = ap.parse_args()
    if not args.json and not args.md:
        ap.error("--json 或 --md 必须提供一个")
    # --profile 三种形态：预设名 / 内联 JSON / .json 文件（agent 按场景知识自定义制式）
    if args.profile.strip().startswith("{"):
        pcfg = json.loads(args.profile)
        if not isinstance(pcfg, dict):
            ap.error("--profile 内联 JSON 必须是对象")
    elif args.profile.strip().endswith(".json"):
        with open(args.profile.strip(), encoding="utf-8") as f:
            pcfg = json.load(f)
        if not isinstance(pcfg, dict):
            ap.error("--profile JSON 文件根必须是对象")
    else:
        if args.profile not in DOC_PROFILES:
            ap.error("--profile 未知预设 %r（可选：%s，或传 JSON 自定义）"
                     % (args.profile, "/".join(sorted(DOC_PROFILES))))
        pcfg = DOC_PROFILES[args.profile]
    indent_pt = float(pcfg.get("first_line_indent") or 0) * float(pcfg.get("body_size") or 10.5)
    tstyle = pcfg.get("table_style", "Light Grid Accent 1")
    quote_east = pcfg.get("quote_east")
    want_pagenum = args.page_numbers or bool(pcfg.get("page_number"))
    want_strip = args.strip_emoji or bool(pcfg.get("strip_emoji"))

    if args.md:
        with open(args.md, encoding="utf-8") as f:
            data = {"markdown": f.read(), "source": args.md, "detail": "agent-markdown"}
    else:
        with open(args.json, encoding="utf-8") as f:
            data = json.load(f)
    if want_strip:
        data["markdown"] = strip_emoji(data.get("markdown") or "")

    source = data.get("source") or ""
    detail = data.get("detail") or "text"
    theme = theme_for(args.profile)
    today = time.strftime("%Y-%m-%d")

    doc = Document()
    apply_doc_fonts(doc, pcfg)  # 场景制式字体/字号/行距/页边距
    if want_pagenum:
        add_page_number_footer(doc, source, theme)  # 页脚：来源+accent 细线+PAGE 域

    # ---- 多源合并模式（证据整合场景）：{"title","analysis":{...},"sources":[...]} ---- #
    # analysis = agent 整合分析产物（渲染为首章，带 [^n] 引用）；
    # 文末自动生成「证据溯源附录」（把各源 grounding/画面/转写元数据回灌）。
    if data.get("sources") or data.get("analysis"):
        sources = list(data.get("sources") or [])
        analysis = data.get("analysis")
        if analysis:
            ana = dict(analysis) if isinstance(analysis, dict) else {"markdown": str(analysis)}
            ana.setdefault("source", "整合分析")
            sources.insert(0, ana)
        doc_title = data.get("title")
        doc.core_properties.title = (doc_title or "") + " | Omni 多源整合"
        doc.core_properties.author = "Omni2Docx"
        doc.core_properties.comments = "generated by omni2docx merge (%d sources)" % len(sources)

        # 第一遍：逐源预处理（章名 / 章内标题 / outline / seg），汇总总目录
        chapters = []
        combined_outline = []  # 章(来源)=H1，章内层级 +1
        for i, s in enumerate(sources):
            md = s.get("markdown") or ""
            if want_strip:
                md = strip_emoji(md)
            chapter = (s.get("source") or "来源 %d" % (i + 1)).strip()
            t_title, md = extract_title(md)  # 各源自带"标题："则提为章内副题
            md, foot = extract_footnotes(md)
            if not args.no_toc:
                om = build_outline_map(s.get("outline")) if s.get("outline") else derive_outline_from_markdown(md)
            else:
                om = []
            seg = build_segment_index(s.get("grounding")) if (s.get("grounding") and not args.no_pagebreak) else []
            chapters.append((chapter, t_title, md, om, seg, foot))
            combined_outline.append((1, chapter))
            combined_outline.extend((min(lvl + 1, 6), t) for lvl, t in om)

        # 前置：文档标题 + 总目录（附录恒在文末，目录可预置）
        if doc_title:
            cover(doc, doc_title, source, theme, date_str=today)
        if not args.no_appendix:
            combined_outline.append((1, "证据溯源附录"))
        if not args.no_toc and combined_outline:
            insert_toc(doc, combined_outline, theme)

        # 第二遍：逐章渲染（章间分页；章内分页/标题提升/溯源标注照常）
        for i, (chapter, t_title, md, om, seg, foot) in enumerate(chapters):
            if i > 0:
                pb = doc.add_paragraph()
                pb.add_run().add_break(WD_BREAK.PAGE)
            h = doc.add_heading(level=1)
            add_inline(h, chapter)
            accent_heading(h, 1, theme)
            if t_title:
                tp = doc.add_paragraph()
                r = tp.add_run(t_title)
                r.bold = True
            # 章内标题层级整体 +1：与总目录一致（章=H1，章内 H1→H2 …）
            blocks = parse_blocks(md)
            render(doc, blocks, seg, om, bool(seg), False, page_marks=args.page_marks, level_offset=1, footnotes=foot, indent_first=indent_pt, table_style=tstyle, quote_east=quote_east, theme=theme)

        # 证据溯源附录：把各源解析元数据（grounding 页锚点 / 画面时间点 / 说话人转写 /
        # outline 章节数）回灌到最终文档——人可按页码/时间点直接对照原件。
        if not args.no_appendix:
            prov_rows = []
            for i, s in enumerate(sources):
                name = (s.get("source") or "来源 %d" % (i + 1)).strip()
                pv = collect_provenance(s.get("markdown") or "", s.get("grounding"), s.get("outline"))
                locs = []
                fp = fmt_pages(pv["pages"])
                if fp:
                    locs.append(fp)
                if pv["frames"]:
                    rng = ("（首 %s … 末 %s）" % (pv["frames"][0], pv["frames"][-1])) if len(pv["frames"]) > 2 else ""
                    locs.append("%d 个画面时间点%s" % (len(pv["frames"]), rng))
                if pv["turns"]:
                    spk = sorted({sp for sp, _ in pv["turns"] if sp})
                    tss = [ts for _, ts in pv["turns"]]
                    rng = "%s 起" % tss[0] if tss else ""
                    locs.append("%d 段转写（说话人 %s，%s）" % (len(pv["turns"]), "、".join(spk) if spk else "—", rng))
                if pv["headings"]:
                    locs.append("%d 个章节" % pv["headings"])
                prov_rows.append((name, pv["kind"], "；".join(locs) if locs else "纯文本（无结构化锚点）"))
            render_provenance_appendix(doc, prov_rows, tstyle, theme)

        sys.stderr.write(
            "omni2docx merge: sources=%d outline_nodes=%d detail=%s\n"
            % (len(sources), len(combined_outline), detail)
        )
        doc.save(args.out)
        return

    # ---- 单源模式 ---- #
    md = data.get("markdown") or ""
    grounding = data.get("grounding")
    outline = data.get("outline")

    # 封面标题：从 "标题：xxx" 提取（研报/文章常见），并从正文去除避免重复
    title_text, md = extract_title(md)
    md, footnotes = extract_footnotes(md)  # 脚注定义剥出，正文 [^n] 渲染为上标，文末「注释」节

    # outline 优先用 Omni read_outline 官方结果（同会话取得后传入）；
    # 缺失或 coverage=none 则从 Omni 输出的 markdown 保守重建章节层级。
    if outline and not args.no_toc:
        outline_map = build_outline_map(outline)
    elif not args.no_toc:
        outline_map = derive_outline_from_markdown(md)
    else:
        outline_map = []
    use_toc = bool(outline_map)
    seg_index = build_segment_index(grounding) if (grounding and not args.no_pagebreak) else []
    use_pagebreak = bool(seg_index)

    if source:
        doc.core_properties.title = (title_text or "") + " | Omni 解析重建"
        doc.core_properties.author = "Omni2Docx"
        doc.core_properties.comments = "generated by omni2docx (detail=%s)" % detail

    blocks = parse_blocks(md)
    if title_text:
        cover(doc, title_text, source, theme, date_str=today)
    page_breaks = render(doc, blocks, seg_index, outline_map, use_pagebreak, use_toc, page_marks=args.page_marks, footnotes=footnotes, indent_first=indent_pt, table_style=tstyle, quote_east=quote_east, theme=theme)
    doc.save(args.out)

    sys.stderr.write(
        "omni2docx: blocks=%d outline_nodes=%d toc=%s segments=%d pagebreaks=%d detail=%s profile=%s\n"
        % (len(blocks), len(outline_map), use_toc, len(seg_index), page_breaks, detail, args.profile)
    )


if __name__ == "__main__":
    main()
