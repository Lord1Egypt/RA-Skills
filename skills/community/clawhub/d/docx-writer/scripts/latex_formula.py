#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""latex_formula.py — LaTeX 公式渲染为「紧裁 PNG」（XeLaTeX 真排版）。

依据 AGENTS.md「数学公式渲染（转图片）」：必须用 XeLaTeX + preview/tightpage 真排版，
禁止 matplotlib mathtext；PDF 用 PyMuPDF(fitz) 逐页转 PNG。

既可作 CLI，也可被 `docx_engine.py` import：

    from latex_formula import render_formulas
    items = render_formulas([r"E=mc^2", r"\\int_0^1 x\\,dx"], outdir="formula_png")

CLI
---
    python latex_formula.py --latex "E=mc^2" "\\alpha_0+\\alpha_1"
    python latex_formula.py --input formulas.txt --outdir ./formula_png --dpi 300
    python latex_formula.py --input formulas.json --inline --outdir ./png
    python latex_formula.py --latex "E=mc^2" --omml      # 输出 Word 原生公式（OMML）

stdout 为 JSON（{"status": "ok", ...}）；进度/错误写 stderr；失败非 0 退出。
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

# preview + tightpage：每个公式自动紧裁成一页（AGENTS.md 指定模板）
TEX_TEMPLATE = r"""\documentclass[12pt]{article}
\usepackage[active,tightpage]{preview}
\usepackage{amsmath,amssymb,bm}
\PreviewEnvironment{preview}
\setlength\PreviewBorder{%(border)s}
\begin{document}
%(body)s
\end{document}
"""


def find_xelatex(explicit=None):
    """定位 xelatex：显式参数 > 环境变量 OPENCODE_XELATEX > PATH。"""
    for cand in (explicit, os.environ.get("OPENCODE_XELATEX")):
        if cand:
            if os.path.exists(cand):
                return cand
            found = shutil.which(cand)
            if found:
                return found
    return shutil.which("xelatex")


def find_pandoc(explicit=None):
    """定位 pandoc：显式参数 > 环境变量 OPENCODE_PANDOC > PATH。"""
    for cand in (explicit, os.environ.get("OPENCODE_PANDOC")):
        if cand:
            if os.path.exists(cand):
                return cand
            found = shutil.which(cand)
            if found:
                return found
    return shutil.which("pandoc")


MATH_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"


def latex_to_omml(latex, display=False, pandoc=None, timeout=90):
    """LaTeX → OMML（Word 原生可编辑公式）的 XML 片段字符串。

    借助 pandoc：markdown 数学 → docx，再从 word/document.xml 抽取 m:oMath /
    m:oMathPara 元素。display=True 返回 m:oMathPara，否则返回 m:oMath。
    """
    import zipfile
    from lxml import etree

    pd = find_pandoc(pandoc)
    if not pd:
        raise RuntimeError("未找到 pandoc：请安装 pandoc，"
                           "或用 --pandoc / 环境变量 OPENCODE_PANDOC 指定路径")
    tex = ("$$%s$$" % latex) if display else ("$%s$" % latex)
    work = tempfile.mkdtemp(prefix="omml_")
    try:
        md = os.path.join(work, "in.md")
        with open(md, "w", encoding="utf-8") as f:
            f.write(tex + "\n")
        out = os.path.join(work, "o.docx")
        p = subprocess.run([pd, "-f", "markdown", "-t", "docx", "-o", out, md],
                           timeout=timeout, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
        if p.returncode != 0:
            raise RuntimeError("pandoc 转换失败:\n" +
                               p.stdout.decode("utf-8", "replace")[-800:])
        with zipfile.ZipFile(out) as z:
            xml = z.read("word/document.xml")
    finally:
        shutil.rmtree(work, ignore_errors=True)

    root = etree.fromstring(xml)
    tag = "{%s}%s" % (MATH_NS, "oMathPara" if display else "oMath")
    el = root.find(".//" + tag)
    if el is None:
        raise RuntimeError("未从 pandoc 输出中找到 OMML 元素（%s）" % tag)
    # 保留公式内的空格（如 "1.2 m"），否则 Word/LibreOffice 会吃掉
    for t in el.iter("{%s}t" % MATH_NS):
        if t.text and t.text != t.text.strip():
            t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    return etree.tostring(el, encoding="unicode")


def _norm(latex):
    """去掉用户可能带入的行内 $...$ / $$...$$ 定界符与首尾空白。"""
    t = (latex or "").strip()
    t = re.sub(r"^\$\$?", "", t)
    t = re.sub(r"\$\$?$", "", t)
    return t.strip()


def _cache_key(latex, display, dpi, border):
    raw = "%s|%d|%s|%s" % ("D" if display else "I", dpi, border, latex)
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def render_formulas(latex_list, outdir, dpi=300, display=True, xelatex=None,
                    timeout=180, border="3pt"):
    """把一组 LaTeX 公式渲染为紧裁 PNG。

    返回 [{"index", "latex", "png", "width_px", "height_px", "width_pt", "height_pt"}, ...]
    """
    import fitz  # PyMuPDF
    from PIL import Image

    outdir = os.path.abspath(outdir)
    os.makedirs(outdir, exist_ok=True)

    items, todo = [], []
    for i, raw in enumerate(latex_list):
        latex = _norm(raw)
        if not latex:
            raise ValueError("第 %d 个公式为空" % i)
        key = _cache_key(latex, display, dpi, border)
        png = os.path.join(outdir, key + ".png")
        it = {"index": i, "latex": latex, "png": png}
        items.append(it)
        if os.path.exists(png):
            w, h = Image.open(png).size
            it.update(width_px=w, height_px=h,
                      width_pt=w / dpi * 72.0, height_pt=h / dpi * 72.0)
        else:
            todo.append(it)

    if todo:
        xe = find_xelatex(xelatex)
        if not xe:
            raise RuntimeError("未找到 xelatex：请安装 TeX 发行版，"
                               "或用 --xelatex / 环境变量 OPENCODE_XELATEX 指定路径")
        style = r"\displaystyle" if display else r"\textstyle"
        body = "\n".join(r"\begin{preview}$%s %s$\end{preview}" % (style, it["latex"])
                         for it in todo)
        tex = TEX_TEMPLATE % {"border": border, "body": body}

        work = tempfile.mkdtemp(prefix="ltxform_", dir=outdir)
        try:
            texfile = os.path.join(work, "formula.tex")
            with open(texfile, "w", encoding="utf-8") as f:
                f.write(tex)
            cmd = [xe, "-interaction=nonstopmode", "-halt-on-error",
                   "-output-directory=" + work, texfile]
            for _ in range(2):  # preview 依靠 .aux 计算紧裁框，需第二遍
                p = subprocess.run(cmd, cwd=work, timeout=timeout,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                if p.returncode != 0:
                    log = p.stdout.decode("utf-8", "replace")
                    tail = "\n".join(log.splitlines()[-15:])
                    raise RuntimeError("xelatex 编译失败:\n" + tail)
            pdf = os.path.join(work, "formula.pdf")
            doc = fitz.open(pdf)
            if doc.page_count != len(todo):
                raise RuntimeError("页数不匹配：公式 %d 个，PDF %d 页"
                                   % (len(todo), doc.page_count))
            for it, page in zip(todo, doc):
                pix = page.get_pixmap(dpi=dpi, alpha=False)
                pix.save(it["png"])
                it.update(width_px=pix.width, height_px=pix.height,
                          width_pt=pix.width / dpi * 72.0,
                          height_pt=pix.height / dpi * 72.0)
            doc.close()
        finally:
            shutil.rmtree(work, ignore_errors=True)

    return items


# ───────────────────────── CLI ─────────────────────────
def _load_latex(args):
    out = list(args.latex or [])
    if args.input:
        if not os.path.exists(args.input):
            raise FileNotFoundError(args.input)
        if args.input.endswith(".json"):
            with open(args.input, encoding="utf-8") as f:
                data = json.load(f)
            out += [str(x) for x in (data if isinstance(data, list) else data.get("formulas", []))]
        else:
            with open(args.input, encoding="utf-8") as f:
                for line in f:
                    s = line.strip()
                    if s and not s.startswith("%"):
                        out.append(s)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="LaTeX 公式渲染为紧裁 PNG（XeLaTeX）")
    ap.add_argument("--latex", nargs="+", help="含 LaTeX 的公式字符串（可多个）")
    ap.add_argument("--input", help="公式文件：.txt（每行一个）或 .json（字符串数组）")
    ap.add_argument("--outdir", default="formula_png", help="输出 PNG 目录（默认 ./formula_png）")
    ap.add_argument("--dpi", type=int, default=300, help="渲染 DPI（默认 300）")
    ap.add_argument("--inline", action="store_true", help="行内公式（textstyle），默认行间 displaystyle")
    ap.add_argument("--xelatex", help="xelatex 可执行文件路径")
    ap.add_argument("--omml", action="store_true",
                    help="改为输出 Word 原生公式（OMML XML 片段，需 pandoc），不渲染 PNG")
    ap.add_argument("--pandoc", help="pandoc 可执行文件路径（--omml 时用）")
    ap.add_argument("--timeout", type=int, default=180, help="单次编译超时秒数")
    a = ap.parse_args(argv)

    try:
        latexes = _load_latex(a)
        if not latexes:
            raise ValueError("未提供公式：请用 --latex 或 --input")
        if a.omml:
            items = [{"index": i, "latex": _norm(t),
                      "omml": latex_to_omml(_norm(t), display=not a.inline,
                                            pandoc=a.pandoc, timeout=a.timeout)}
                     for i, t in enumerate(latexes)]
            print(json.dumps({"status": "ok", "count": len(items),
                              "format": "omml", "items": items}, ensure_ascii=False))
            return
        items = render_formulas(latexes, a.outdir, dpi=a.dpi,
                                display=not a.inline, xelatex=a.xelatex,
                                timeout=a.timeout)
        print(json.dumps({"status": "ok", "count": len(items),
                          "outdir": os.path.abspath(a.outdir),
                          "items": items}, ensure_ascii=False))
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
