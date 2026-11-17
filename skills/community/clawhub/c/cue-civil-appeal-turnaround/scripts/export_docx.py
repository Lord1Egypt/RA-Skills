#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
export_docx.py — 把本技能产出的 Markdown 案件材料转成可递交 / 可打印的 Word（.docx）。

用法:
    python export_docx.py <input.md> [-o out.docx] [--style court|brief] [--check]
    python export_docx.py --dir <目录> [--pattern "*.md"] [-o <输出目录>] [--style court] [--check]

设计前提（与 journal-draft 的「文字稿」同一条经验）：
  Word 版是**用来改文字和递交打印的**，不是用来看版面的；不强求 mm 级定位，
  否则会退化成一堆互相打架的文本框。

与期刊那条链最大的不同：**本件用于递交法院的文书，内容必须逐字保真。**
所以本脚本不重写、不润色、不「优化措辞」——只做格式投影，并用 --check
做文本覆盖校验（转出来的 Word 少了哪一行，直接报出来）。

样式（--style）：
  court  公文体：A4 + 上3.7/下3.5/左2.8/右2.6cm；正文仿宋三号、行距固定 28pt、
         首行缩进 2 字符；文种标题黑体二号居中；表格宋体小四。递交法院用这个。
  brief  诉状体：正文宋体小四、1.5 倍行距。给律师核、自己看，行数少一点。

依赖：python-docx（可选）。未安装时脚本会明确报出安装命令，不做静默降级。
零网络请求。
"""

from __future__ import annotations

import argparse
import glob
import os
import re
import sys
from pathlib import Path

try:
    from docx import Document
    from docx.enum.section import WD_SECTION
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt, RGBColor
except ImportError:  # pragma: no cover
    sys.exit(
        "缺少依赖 python-docx。安装：\n"
        "  python -m pip install python-docx -i https://pypi.tuna.tsinghua.edu.cn/simple\n"
        "（本脚本不做静默降级：没有依赖就不产出半成品文件。）"
    )

# ---------------------------------------------------------------- 样式参数

# 中文字号 → pt
PT = {"二号": 22, "小二": 18, "三号": 16, "小三": 15, "四号": 14, "小四": 12, "五号": 10.5}

STYLES = {
    "court": {
        "page": (Cm(21), Cm(29.7)),           # A4
        "margin": (Cm(3.7), Cm(3.5), Cm(2.8), Cm(2.6)),  # 上 下 左 右
        "body_font": "仿宋",
        "body_size": PT["三号"],
        "body_leading": Pt(28),
        "body_indent": Pt(32),                # 三号 × 2 字符
        "h1_font": "黑体", "h1_size": PT["二号"],
        "h2_font": "黑体", "h2_size": PT["三号"],
        "h3_font": "楷体", "h3_size": PT["小三"],
        "quote_font": "楷体", "quote_size": PT["小四"],
        "table_font": "宋体", "table_size": PT["小四"],
        "exact_leading": True,
    },
    "brief": {
        "page": (Cm(21), Cm(29.7)),
        "margin": (Cm(2.54), Cm(2.54), Cm(3.17), Cm(3.17)),
        "body_font": "宋体",
        "body_size": PT["小四"],
        "body_leading": 1.5,
        "body_indent": Pt(24),
        "h1_font": "黑体", "h1_size": PT["三号"],
        "h2_font": "黑体", "h2_size": PT["小四"],
        "h3_font": "黑体", "h3_size": PT["小四"],
        "quote_font": "楷体", "quote_size": PT["小四"],
        "table_font": "宋体", "table_size": PT["五号"],
        "exact_leading": False,
    },
}

EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\u2600-\u27BF\uFE0F\u2B00-\u2BFF\u2705\u274C\u2757\u203C\u2049]"
)


# ---------------------------------------------------------------- 基础工具

def set_run(run, font_name: str, size_pt: float, bold=False, color=None):
    """设字体。**中文必须写 eastAsia**，否则 Word 里中文掉回宋体。"""
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    if color is not None:
        run.font.color.rgb = color
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:ascii"), font_name)
    rfonts.set(qn("w:hAnsi"), font_name)
    rfonts.set(qn("w:eastAsia"), font_name)


def add_page_number(paragraph, font="宋体", size=PT["小四"]):
    """页脚插入 PAGE 域。递交件要页码。"""
    run = paragraph.add_run()
    set_run(run, font, size)
    f1 = OxmlElement("w:fldChar")
    f1.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText")
    it.set(qn("xml:space"), "preserve")
    it.text = "PAGE"
    f2 = OxmlElement("w:fldChar")
    f2.set(qn("w:fldCharType"), "end")
    run._r.append(f1)
    run._r.append(it)
    run._r.append(f2)


INLINE_RE = re.compile(r"(\*\*.+?\*\*|`[^`]+`|\[[^\]]+\]\([^)]+\))")


def strip_inline(text: str) -> str:
    """去掉行内 markdown 标记，返回纯文本（用于保真校验与表格单元格）。"""
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    t = re.sub(r"`([^`]+)`", r"\1", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    return t


def write_runs(paragraph, text: str, font: str, size: float, base_bold=False):
    """按 **粗体** / `代码` / [链接](url) 切段写入，保留粗体语义。"""
    if not text:
        return
    pos = 0
    for m in INLINE_RE.finditer(text):
        if m.start() > pos:
            seg = text[pos:m.start()]
            if seg:
                set_run(paragraph.add_run(seg), font, size, base_bold)
        tok = m.group(0)
        if tok.startswith("**"):
            # 递归：粗体内部还可能套 `代码` 或 [链接](url)。
            # 不递归的话整段会按粗体原样写入，反引号会留在 Word 里——
            # 递交件出现 `xxx.md` 这种残留标记很难看，校验也会因此误报缺失。
            write_runs(paragraph, tok[2:-2], font, size, True)
        elif tok.startswith("`"):
            set_run(paragraph.add_run(tok[1:-1]), "Consolas", size, base_bold)
        else:
            label = re.match(r"\[([^\]]+)\]\(([^)]+)\)", tok)
            set_run(paragraph.add_run(f"{label.group(1)}（{label.group(2)}）"), font, size, base_bold)
        pos = m.end()
    tail = text[pos:]
    if tail:
        set_run(paragraph.add_run(tail), font, size, base_bold)


# ---------------------------------------------------------------- 分块解析

def split_row(line: str) -> list[str]:
    """拆表格行，处理单元格内的 \\| 转义。"""
    cells, buf, i = [], [], 0
    while i < len(line):
        c = line[i]
        if c == "\\" and i + 1 < len(line) and line[i + 1] == "|":
            buf.append("|")
            i += 2
            continue
        if c == "|":
            cells.append("".join(buf).strip())
            buf = []
            i += 1
            continue
        buf.append(c)
        i += 1
    cells.append("".join(buf).strip())
    # 去掉首尾由 | 产生的空单元格
    if cells and cells[0] == "":
        cells = cells[1:]
    if cells and cells[-1] == "":
        cells = cells[:-1]
    return cells


def parse_blocks(lines: list[str]) -> list[dict]:
    """把 markdown 行切成块：heading / para / quote / table / code / list / hr。"""
    blocks: list[dict] = []
    i = 0
    n = len(lines)
    while i < n:
        raw = lines[i].rstrip("\n")
        line = raw.rstrip()
        stripped = line.strip()

        if not stripped:
            blocks.append({"type": "blank"})
            i += 1
            continue

        # 代码块
        if stripped.startswith("```"):
            i += 1
            buf = []
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i].rstrip("\n"))
                i += 1
            i += 1  # 收尾 ```
            blocks.append({"type": "code", "lines": buf})
            continue

        # 标题
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            blocks.append({"type": "heading", "level": len(m.group(1)), "text": m.group(2).strip()})
            i += 1
            continue

        # 分隔线
        if re.match(r"^(\-{3,}|\*{3,}|_{3,})$", stripped):
            blocks.append({"type": "hr"})
            i += 1
            continue

        # 表格：当前行 | 开头，且下一行是分隔行
        if stripped.startswith("|") and i + 1 < n and re.match(r"^\|?\s*:?-{2,}", lines[i + 1].strip()):
            header = split_row(stripped)
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i].strip()))
                i += 1
            blocks.append({"type": "table", "header": header, "rows": rows})
            continue

        # 引用（连续行合并为一段）
        if stripped.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^>\s?", "", lines[i].strip()))
                i += 1
            blocks.append({"type": "quote", "text": " ".join(x for x in buf if x)})
            continue

        # 列表（连续行合并为一个列表块，保留层级）
        m = re.match(r"^(\s*)([-*+])\s+(.*)$", raw)
        m2 = re.match(r"^(\s*)(\d+)[.)]\s+(.*)$", stripped)
        if m or m2:
            items = []
            ordered = bool(m2)
            while i < n:
                s = lines[i].rstrip("\n")
                mm = re.match(r"^(\s*)([-*+])\s+(.*)$", s)
                mn = re.match(r"^(\s*)(\d+)[.)]\s+(.*)$", s.strip())
                if mm and not ordered:
                    indent = len(mm.group(1)) // 2
                    txt = mm.group(3)
                    txt = re.sub(r"^\[[ xX]\]\s*", "☐ " if re.match(r"^\[\s\]", txt) else "☑ ", txt)
                    items.append((indent, txt))
                    i += 1
                elif mn and ordered:
                    indent = len(mn.group(1)) // 2
                    items.append((indent, mn.group(3)))
                    i += 1
                else:
                    break
            blocks.append({"type": "list", "ordered": ordered, "items": items})
            continue

        # 普通段落（软换行并入同段）
        buf = [stripped]
        i += 1
        while i < n:
            s = lines[i].strip()
            if (not s or s.startswith(("#", ">", "|", "```", "-", "*", "+"))
                    or re.match(r"^\d+[.)]\s", s)
                    or re.match(r"^(\-{3,}|\*{3,}|_{3,})$", s)):
                break
            buf.append(s)
            i += 1
        blocks.append({"type": "para", "text": " ".join(buf)})
    return blocks


# ---------------------------------------------------------------- 渲染

def render(doc, blocks: list[dict], S: dict, strip_emoji: bool):
    sec = doc.sections[0]
    sec.page_width, sec.page_height = S["page"]
    sec.top_margin, sec.bottom_margin, sec.left_margin, sec.right_margin = S["margin"]

    def clean(t: str) -> str:
        return EMOJI_RE.sub("", t) if strip_emoji else t

    for b in blocks:
        t = b["type"]

        if t == "blank":
            continue

        if t == "hr":
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
            continue

        if t == "heading":
            level = b["level"]
            text = clean(strip_inline(b["text"]))
            p = doc.add_paragraph()
            pf = p.paragraph_format
            if level == 1:
                pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
                pf.space_before = Pt(0)
                pf.space_after = Pt(18)
                set_run(p.add_run(text), S["h1_font"], S["h1_size"], True)
            elif level == 2:
                pf.space_before = Pt(12)
                pf.space_after = Pt(6)
                set_run(p.add_run(text), S["h2_font"], S["h2_size"], True)
            else:
                pf.space_before = Pt(8)
                pf.space_after = Pt(4)
                set_run(p.add_run(text), S["h3_font"], S["h3_size"], True)
            continue

        if t == "para":
            text = clean(b["text"])
            p = doc.add_paragraph()
            pf = p.paragraph_format
            pf.first_line_indent = S["body_indent"]
            pf.line_spacing = S["body_leading"]
            if S["exact_leading"]:
                pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            pf.space_after = Pt(0)
            write_runs(p, text, S["body_font"], S["body_size"])
            continue

        if t == "quote":
            text = clean(b["text"])
            p = doc.add_paragraph()
            pf = p.paragraph_format
            pf.left_indent = S["body_indent"]
            pf.first_line_indent = S["body_indent"]
            pf.line_spacing = S["body_leading"]
            if S["exact_leading"]:
                pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            pf.space_before = Pt(4)
            pf.space_after = Pt(4)
            write_runs(p, text, S["quote_font"], S["quote_size"])
            continue

        if t == "list":
            for indent, item in b["items"]:
                text = clean(item)
                p = doc.add_paragraph(style="List Bullet" if not b["ordered"] else "List Number")
                pf = p.paragraph_format
                pf.left_indent = Pt(21 + 21 * indent)
                pf.line_spacing = S["body_leading"]
                if S["exact_leading"]:
                    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
                pf.space_after = Pt(0)
                write_runs(p, text, S["body_font"], S["body_size"])
            continue

        if t == "code":
            for ln in b["lines"] or [""]:
                p = doc.add_paragraph()
                pf = p.paragraph_format
                pf.left_indent = Pt(21)
                pf.line_spacing = Pt(14)
                pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
                set_run(p.add_run(ln if ln else " "), "Consolas", PT["五号"])
            continue

        if t == "table":
            header = [clean(strip_inline(c)) for c in b["header"]]
            rows = [[clean(strip_inline(c)) for c in r] for r in b["rows"]]
            ncols = len(header)
            tbl = doc.add_table(rows=1, cols=ncols)
            tbl.style = "Table Grid"
            tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            hdr = tbl.rows[0].cells
            for j, h in enumerate(header):
                hdr[j].text = ""
                p = hdr[j].paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                set_run(p.add_run(h), S["table_font"], S["table_size"], True)
            for r in rows:
                cells = tbl.add_row().cells
                for j in range(ncols):
                    v = r[j] if j < len(r) else ""
                    cells[j].text = ""
                    p = cells[j].paragraphs[0]
                    p.paragraph_format.space_after = Pt(0)
                    set_run(p.add_run(v), S["table_font"], S["table_size"])
            doc.add_paragraph().paragraph_format.space_after = Pt(0)
            continue


def build(md_path: Path, out_path: Path, style: str, strip_emoji: bool, page_number: bool):
    lines = md_path.read_text(encoding="utf-8").splitlines(keepends=True)
    blocks = parse_blocks(lines)
    S = STYLES[style]
    doc = Document()
    # 正文默认样式：避免 Word 用 Normal 的西文字体渲染中文
    normal = doc.styles["Normal"]
    normal.font.name = S["body_font"]
    normal.font.size = Pt(S["body_size"])
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), S["body_font"])

    render(doc, blocks, S, strip_emoji)

    if page_number:
        footer = doc.sections[0].footer
        p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_page_number(p)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_path))
    return blocks


# ---------------------------------------------------------------- 保真校验

def norm(s: str) -> str:
    """归一化：去空白、去常见标点差异，便于包含匹配。"""
    s = re.sub(r"\s+", "", s)
    return s


def check_fidelity(md_path: Path, docx_path: Path, strip_emoji: bool = False) -> tuple[int, int, list[str]]:
    """转出的 Word 是否覆盖了源 md 的每一行实质文本。

    思路取自 journal-draft 的 crosscheck：不比对格式，只比对「文字有没有少」。
    少内容这类失败不会报错，只会静静少一段——递交法院的文书尤其不能接受。

    strip_emoji 必须与导出时一致：源文本若不去 emoji，就会拿带 emoji 的源去
    比对已去 emoji 的 Word，把「按要求去掉的符号」误报成「丢失的内容」。
    """
    src_lines = []
    for ln in md_path.read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if not s:
            continue
        if s.startswith(("```", "---", "***", "___")):
            continue
        if s.startswith(">"):
            s = re.sub(r"^>\s?", "", s)
        if s.startswith("|"):
            # 表格行：拆成单元格分别校验
            for c in split_row(s):
                c = strip_inline(c).strip()
                if c and not re.match(r"^:?-{2,}", c):
                    src_lines.append(c)
            continue
        s = re.sub(r"^#{1,6}\s+", "", s)
        s = re.sub(r"^\s*([-*+]|\d+[.)])\s+", "", s)
        s = re.sub(r"^\[[ xX]\]\s*", "", s)
        s = strip_inline(s)
        if s:
            src_lines.append(s)
    if strip_emoji:
        src_lines = [EMOJI_RE.sub("", s) for s in src_lines]

    doc = Document(str(docx_path))
    got = []
    for p in doc.paragraphs:
        if p.text.strip():
            got.append(p.text)
    for tbl in doc.tables:
        for row in tbl.rows:
            for cell in row.cells:
                if cell.text.strip():
                    got.append(cell.text)
    blob = norm("".join(got))

    missing = [s for s in src_lines if norm(s) and norm(s) not in blob]
    return len(src_lines), len(missing), missing[:8]


# ---------------------------------------------------------------- CLI

def main():
    ap = argparse.ArgumentParser(
        description="把 Markdown 案件材料转成可递交 / 可打印的 Word（逐字保真，不重写内容）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例：\n"
               "  python export_docx.py 上诉状.md -o 递交/上诉状.docx --check\n"
               "  python export_docx.py --dir . --pattern '上诉状*.md' -o 递交/\n",
    )
    ap.add_argument("input", nargs="?", help="输入 .md 文件")
    ap.add_argument("-o", "--out", help="输出 .docx 路径；配合 --dir 时为输出目录")
    ap.add_argument("--dir", help="批量：输入目录")
    ap.add_argument("--pattern", default="*.md", help="批量：文件名通配（默认 *.md）")
    ap.add_argument("--style", choices=sorted(STYLES), default="court",
                    help="court=公文体（递交用，默认）；brief=诉状体（自用）")
    ap.add_argument("--strip-emoji", action="store_true",
                    help="去掉 emoji（递交法院的正式文书建议开）")
    ap.add_argument("--no-page-number", action="store_true", help="不加页脚页码")
    ap.add_argument("--check", action="store_true",
                    help="转后做文本覆盖校验，报出 Word 里缺失的源文本行")
    args = ap.parse_args()

    if not args.input and not args.dir:
        ap.error("需要 <input.md> 或 --dir <目录>")

    if args.dir:
        indir = Path(args.dir)
        outdir = Path(args.out) if args.out else indir / "Word"
        files = sorted(indir.glob(args.pattern))
        if not files:
            sys.exit(f"目录里没有匹配 {args.pattern} 的文件：{indir}")
        for f in files:
            out = outdir / (f.stem + ".docx")
            build(f, out, args.style, args.strip_emoji, not args.no_page_number)
            msg = f"✅ {f.name} → {out}"
            if args.check:
                total, miss, samples = check_fidelity(f, out, args.strip_emoji)
                flag = "OK" if miss == 0 else f"⚠ 缺 {miss}/{total}"
                msg += f"　[校验 {flag}]"
                for s in samples:
                    msg += f"\n     缺：{s[:60]}"
            print(msg)
        print(f"\n共 {len(files)} 个文件 → {outdir}")
        return

    src = Path(args.input)
    if not src.exists():
        sys.exit(f"输入文件不存在：{src}（给一个 .md 文件路径；批量请用 --dir <目录>）")
    if src.is_dir():
        sys.exit(f"输入是目录、不是文件：{src}（批量请用 --dir {src} --pattern \"*.md\"）")
    out = Path(args.out) if args.out else src.with_suffix(".docx")
    build(src, out, args.style, args.strip_emoji, not args.no_page_number)
    print(f"✅ {src.name} → {out}　[样式 {args.style}]")
    if args.check:
        total, miss, samples = check_fidelity(src, out, args.strip_emoji)
        if miss == 0:
            print(f"校验通过：{total} 行源文本全部出现在 Word 中")
        else:
            print(f"⚠ 校验：{total} 行中有 {miss} 行未出现在 Word 中，例：")
            for s in samples:
                print(f"     {s[:70]}")


if __name__ == "__main__":
    main()
