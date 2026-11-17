#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""omni2docx — HTML 展示渲染器（展示场景：浏览器直接打开/分享，自包含单文件）

设计：复用 build_docx 的块解析（parse_blocks）与内联正则（INLINE_RE），
把同一份 Omni 解析结果渲染为 HTML；docx 引擎不做任何改动。
展示场景关注：可读排版、目录锚点跳转、源页标注、表格/脚注/引用还原、可打印（@page）。
"""
import argparse
import html
import json
import os
import re
import subprocess
import sys
import time
from html.parser import HTMLParser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_docx import (  # noqa: E402
    DOC_PROFILES, INLINE_RE, EMOJI_RE,
    build_outline_map, build_segment_index, classify_visual, clean_cjk_spaces,
    derive_outline_from_markdown, extract_footnotes, extract_title,
    match_outline_level, page_for_byte, parse_blocks, split_row, strip_emoji,
)


def esc(t):
    """文本节点专用：转 & < >，不动引号（引号在文本里不是危险字符）。
    属性值不走这一枚——那是另一枚出口 esc_attr()，两形的危险字符集不同。"""
    return html.escape(t or "", quote=False)


def esc_attr(t):
    """属性值专用出口：& < > " ' 全转（html.escape 的 quote=True 那一支），属性 breakout 由这一枚统一挡。

    件里所有写进 属性="…" 的值都必须经过本函数——包括 src／alt／href／id／class／data-page／style；
    散点 replace 或就地 html.escape 都不再是第二处真值。上游 Omni 返回的 description／alt／footnote key
    都是不可信数据，一枚引号就能把属性提前闭合（外部扫描器判这一形是可执行属性注入）。"""
    if t is None:
        return ""
    return html.escape(t if isinstance(t, str) else str(t), quote=True)


def slug(text, used):
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "-", (text or "").strip()).strip("-")[:40] or "s"
    base, i = s, 2
    while s in used:
        s = "%s-%d" % (base, i)
        i += 1
    used.add(s)
    return s


def inline(text, footnotes=None):
    """markdown 行内 → HTML（递归，支持粗体内嵌代码/链接/斜体）。"""
    out, pos = [], 0
    for m in INLINE_RE.finditer(text or ""):
        if m.start() > pos:
            out.append(esc(text[pos:m.start()]))
        tok = m.group(0)
        if tok.startswith("!["):
            mm = re.match(r"!\[([^\]]*)\]\(([^)]*)\)", tok)
            alt, src = (mm.group(1), mm.group(2)) if mm else ("", "")
            if src.startswith(("data:image", "http://", "https://")):
                out.append('<figure class="img"><img src="%s" alt="%s">'
                           '<figcaption>%s</figcaption></figure>'
                           % (esc_attr(src), esc_attr(alt), esc(alt or "图像")))
            else:
                out.append('<span class="img-note">［图像：%s］</span>' % esc(alt or "图像"))
        elif tok.startswith("[^"):
            key = tok[2:-1]
            n = len(footnotes) + 1 if footnotes is not None else 1
            idx = n
            if footnotes is not None and key not in footnotes:
                footnotes[key] = len(footnotes) + 1
                idx = footnotes[key]
            out.append('<sup class="fn"><a href="#fn-%s" id="fnref-%s">[%s]</a></sup>'
                       % (esc_attr(key), esc_attr(key), idx))
        elif tok.startswith("〔"):
            out.append('<span class="srcnote">%s</span>' % esc(tok))
        elif tok.startswith("**") or tok.startswith("__"):
            out.append("<strong>%s</strong>" % inline(tok[2:-2], footnotes))
        elif tok.startswith("`"):
            out.append("<code>%s</code>" % esc(tok[1:-1]))
        elif tok.startswith("["):
            mm = re.match(r"\[([^\]]+)\]\(([^)]+)\)", tok)
            if mm:
                out.append('<a href="%s" target="_blank" rel="noopener">%s</a>'
                           % (esc_attr(mm.group(2)), inline(mm.group(1), footnotes)))
            else:
                out.append(esc(tok))
        else:
            inner = tok[1:-1]
            # CJK 伪斜体：中文不用 <em>（渲染为机械倾斜），改用 <span class="cjk-em">
            if re.search(r"[\u4e00-\u9fff]", inner):
                out.append('<span class="cjk-em">%s</span>' % inline(inner, footnotes))
            else:
                out.append("<em>%s</em>" % inline(inner, footnotes))
        pos = m.end()
    if pos < len(text or ""):
        out.append(esc(text[pos:]))
    return "".join(out)


def spacing_css(ls):
    """行距容错：数值（≥12 视为磅值，否则倍数）/ 字符串（28pt、28磅、1.5倍、1.5x）。"""
    if ls is None:
        return "1.75"
    if isinstance(ls, (int, float)):
        return ("%gpt" % float(ls)) if float(ls) >= 12 else ("%g" % float(ls))
    s = str(ls).strip().lower()
    m = re.search(r"([0-9.]+)\s*(pt|磅|倍|x|em)?", s)
    if not m:
        return "1.75"
    val = float(m.group(1))
    unit = m.group(2)
    if unit in ("pt", "磅"):
        return "%gpt" % val
    if unit in ("倍", "x", "em"):
        return "%g" % val
    return ("%gpt" % val) if val >= 12 else ("%g" % val)


# 编辑式极简主题（与 PPTX/Word 同一套）：近单色 + 单一克制强调色 + 细灰 hairline；
# 本包制式：不铺色块、不用左 accent 竖条、不用表头填充——层级只靠留白、字重与细灰 hairline 表达。
HTML_THEMES = {
    "default":  {"primary": "#8C6A3F", "ink": "#1A1A1A", "accent": "#8C6A3F",
                 "hairline": "#DCDCDC", "panel": "#FAFAFA", "muted": "#6E6E6E"},
    "academic": {"primary": "#2E4A7A", "ink": "#1A1A1A", "accent": "#2E4A7A",
                 "hairline": "#DCDCDC", "panel": "#FAFAFA", "muted": "#6E6E6E"},
    "gov":      {"primary": "#8A2B2B", "ink": "#1A1A1A", "accent": "#8A2B2B",
                 "hairline": "#DCDCDC", "panel": "#FAFAFA", "muted": "#6E6E6E"},
    "legal":    {"primary": "#7A3B2E", "ink": "#1A1A1A", "accent": "#7A3B2E",
                 "hairline": "#DCDCDC", "panel": "#FAFAFA", "muted": "#6E6E6E"},
    "finance":  {"primary": "#1F6F6B", "ink": "#1A1A1A", "accent": "#1F6F6B",
                 "hairline": "#DCDCDC", "panel": "#FAFAFA", "muted": "#6E6E6E"},
}


def css_for(pcfg, page_marks, theme=None):
    east = pcfg.get("body_east", "宋体")
    latin = pcfg.get("body_latin")
    heast = pcfg.get("heading_east", "黑体")
    body = float(pcfg.get("body_size") or 10.5)
    hs = pcfg.get("heading_sizes") or [16, 14, 13, 12, 12, 12]
    title = float(pcfg.get("title_size") or 20)
    lh = spacing_css(pcfg.get("line_spacing"))
    ind = float(pcfg.get("first_line_indent") or 0)
    mg = pcfg.get("margins_cm") or {}
    mgc = "@page{size:A4;margin:%s}" % " ".join(
        "%gcm" % float(mg.get(k, 2.54)) for k in ("top", "right", "bottom", "left")
    ) if mg else "@page{size:A4;margin:2.54cm}"
    family = ('"%s",%s,"Microsoft YaHei","PingFang SC",sans-serif'
              % (east, ('"%s",' % latin) if latin else ""))
    hfamily = '"%s","Microsoft YaHei","PingFang SC",sans-serif' % heast
    th = theme or HTML_THEMES["default"]
    return """
%s
:root{--f:%s;--hf:%s;--body:%gpt;--lh:%s;--primary:%s;--ink:%s;--accent:%s;
 --hairline:%s;--muted:%s;--panel:%s}
*{box-sizing:border-box}
body{margin:0 auto;max-width:46rem;padding:0 1.6rem 2.5rem;font-family:var(--f);
 font-size:var(--body);line-height:var(--lh);color:#222;background:#fff}
.hero{margin:0 -1.6rem 2.2rem;padding:2.8rem 1.8rem 1.6rem;border-bottom:2px solid var(--accent)}
.hero h1{color:var(--ink);font-size:%gpt;margin:0 0 .35em;line-height:1.25;
 font-family:var(--hf);font-weight:700}
.hero .sub{color:var(--muted);font-size:1.02em;margin:.2em 0 0}
.hero .src{color:var(--muted);font-size:.85em;margin-top:1em}
h1,h2,h3,h4,h5,h6{font-family:var(--hf);color:var(--ink);font-weight:600;
 line-height:1.4;margin:1.6em 0 .6em}
h1{font-size:%gpt}h2{font-size:%gpt}h3{font-size:%gpt}h4{font-size:%gpt}
h5{font-size:%gpt}h6{font-size:%gpt}
h2{border-bottom:1px solid var(--hairline);padding-bottom:.2em}
h3{color:var(--muted)}
p{margin:.5em 0;text-align:justify%s}
ul,ol{margin:.5em 0 .5em 1.6em;padding:0}
li{margin:.25em 0}
table{border-collapse:collapse;width:100%%;margin:1em 0;font-size:.95em}
th,td{padding:.45em .65em;text-align:left;vertical-align:top}
th{border-bottom:2px solid var(--ink);font-family:var(--hf);font-weight:600;color:var(--ink)}
td{border-bottom:1px solid var(--hairline)}
tbody tr:last-child td{border-bottom:1px solid var(--hairline)}
blockquote{margin:1em 0;padding:.4em 0 .4em 1em;border-left:2px solid var(--hairline);
 font-family:%s;color:#444}
code{font-family:Consolas,Monaco,monospace;background:#f2f2f2;padding:.1em .3em;
 border-radius:0;font-size:.9em;color:#444}
.srcnote{color:#9aa0a6;font-size:.85em}
.cjk-em{font-weight:600;color:var(--ink)}
.fn a{text-decoration:none;color:var(--accent)}
.visual{border-left:2px solid var(--hairline);padding:.4em 0 .4em .9em;
 margin:.8em 0;color:#555;font-size:.92em}
.img-note{color:#9aa0a6;font-size:.85em}
figure.img{margin:1em 0}figure.img img{max-width:100%%}
figure.img figcaption{color:var(--muted);font-size:.85em;text-align:center;margin-top:.3em}
nav.toc{margin:0 0 2.2em;padding-bottom:.5em;border-bottom:1px solid var(--hairline)}
nav.toc summary{cursor:pointer;font-family:var(--hf);font-weight:600;color:var(--ink);
 font-size:1.05em;list-style:none}
nav.toc ul{list-style:none;padding:0;margin:.6em 0 0;display:grid;
 grid-template-columns:repeat(auto-fill,minmax(15rem,1fr));gap:.15em .8em}
nav.toc li{margin:0;padding:.12em 0}
nav.toc a{color:var(--ink);text-decoration:none}
nav.toc a:hover{text-decoration:underline;color:var(--accent)}
.pagemark{display:block;color:#b0b0b0;font-size:.78em;margin:1.1em 0 .2em;
 border-top:1px dashed var(--hairline);padding-top:.3em}
.meta{color:var(--muted);font-size:.85em;text-align:center;margin:.2em 0 1.6em}
hr{border:0;border-top:1px solid var(--hairline);margin:1.6em 0}
section.endnotes{margin-top:2.5em;border-top:1px solid var(--hairline);padding-top:1em;
 font-size:.9em;color:#444}
section.endnotes ol{margin-left:1.4em}
section.appendix{margin-top:2.5em}
@media print{nav.toc{display:none}body{padding:0;max-width:none}
 .hero{margin:0 0 2em;-webkit-print-color-adjust:exact;print-color-adjust:exact}
 a{color:#000;text-decoration:none}}
""" % (
        mgc, family, hfamily, body, lh,
        th["primary"], th["ink"], th["accent"], th["hairline"], th["muted"], th["panel"],
        title,
        float(hs[0] if len(hs) > 0 else 16), float(hs[1] if len(hs) > 1 else 14),
        float(hs[2] if len(hs) > 2 else 13), float(hs[3] if len(hs) > 3 else 12),
        float(hs[4] if len(hs) > 4 else 12), float(hs[5] if len(hs) > 5 else 12),
        (";text-indent:%gem" % ind) if ind else "",
        '"%s",serif' % pcfg.get("quote_east", "楷体"),
    )


def block_html(kind, payload, used_ids, footnotes, outline_map, level_offset=0):
    """返回 (html, toc_entry or None)。"""
    if kind == "heading":
        lvl, text = payload
        mr = match_outline_level(text, outline_map)
        if mr:
            lvl = mr[0]
        lvl = min(max(int(lvl) + level_offset, 1), 6)
        sid = slug(text, used_ids)
        return ('<h%d id="%s">%s</h%d>' % (lvl, esc_attr(sid), inline(text, footnotes), lvl),
                (lvl, text, sid))
    if kind == "para":
        return ("<p>%s</p>" % inline(payload, footnotes), None)
    if kind == "quote":
        return ("<blockquote>%s</blockquote>" % inline(payload, footnotes), None)
    if kind in ("ul", "ol"):
        tag = "ol" if kind == "ol" else "ul"
        items = "".join("<li>%s</li>" % inline(x, footnotes) for x in payload)
        return ("<%s>%s</%s>" % (tag, items, tag), None)
    if kind == "table":
        header, rows = payload
        th = "".join("<th>%s</th>" % inline(c, footnotes) for c in header)
        trs = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c, footnotes) for c in r)
                      for r in rows)
        return ("<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (th, trs), None)
    if kind == "hr":
        return ("<hr>", None)
    if kind == "visual":
        if isinstance(payload, (tuple, list)):
            label, text = payload[0], payload[1]
        else:
            label, text = "标注", str(payload)
        return ('<div class="visual"><strong>%s</strong>：%s</div>'
                % (esc(label), inline(text, footnotes)), None)
    return ("<p>%s</p>" % inline(str(payload), footnotes), None)


def render_source(md, outline, grounding, pcfg, used, page_marks=False, level_offset=0,
                  toc=True):
    md, foot = extract_footnotes(md)
    om = build_outline_map(outline) if outline else derive_outline_from_markdown(md)
    seg = build_segment_index(grounding) if grounding else []
    blocks = parse_blocks(md)
    body, toc_items = [], []
    footnotes = {}
    last_page = None
    for kind, payload, bstart in blocks:
        if seg:
            p = page_for_byte(seg, bstart)
            if p is not None and p != last_page:
                last_page = p
                cls = "pagemark"
                body.append('<span class="%s" data-page="%s">源第 %s 页</span>'
                            % (esc_attr(cls), esc_attr(p), esc(str(p))))
        h, toc_entry = block_html(kind, payload, used, footnotes, om, level_offset)
        body.append(h)
        if toc_entry:
            toc_items.append(toc_entry)
    return body, toc_items, footnotes, foot


def toc_html(items, depth=2):
    if not items:
        return ""
    li = []
    for lvl, text, sid in items:
        if lvl > depth:
            continue
        li.append('<li style="margin-left:%dem;list-style:none"><a href="#%s">%s</a></li>'
                  % (max(lvl - 1, 0) * 1.4, esc_attr(sid), esc(text)))
    if not li:
        return ""
    # 无序列表且去自动编号：标题多自带编号（"一、"/"3.1"），ol 的序号会叠加成双重编号
    return ('<nav class="toc"><details open><summary>目录</summary>'
            '<ul style="padding-left:0;margin:0">%s</ul></details></nav>'
            % "".join(li))


def endnotes_html(foot):
    if not foot:
        return ""
    items = []
    for key, text in foot:
        items.append('<li id="fn-%s">%s</li>' % (esc_attr(key), inline(text)))
    return '<section class="endnotes"><h2>注释</h2><ol>%s</ol></section>' % "".join(items)


def find_browser():
    cands = []
    if sys.platform.startswith("win"):
        for p in (r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                  r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                  r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                  r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"):
            cands.append(p)
    elif sys.platform == "darwin":
        cands += ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                  "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"]
    else:
        cands += ["google-chrome", "chromium", "chromium-browser", "microsoft-edge"]
    for c in cands:
        if os.path.exists(c):
            return c
    for c in cands:
        from shutil import which
        if which(c):
            return which(c)
    return None


def html_to_pdf(html_path, pdf_path):
    browser = find_browser()
    if not browser:
        return False, "未找到 headless 浏览器（Edge/Chrome/Chromium），跳过 PDF"
    url = "file:///" + os.path.abspath(html_path).replace("\\", "/")
    try:
        subprocess.run([browser, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                        "--print-to-pdf=%s" % os.path.abspath(pdf_path), url],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    except Exception as e:
        return False, "浏览器调用失败：%s" % e
    for _ in range(40):
        if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
            time.sleep(0.3)
            return True, os.path.abspath(pdf_path)
        time.sleep(0.25)
    return False, "浏览器未产出 PDF（超时）"


# --------------------------------------------------------------------------- #
#  微信 inline CSS 导出：把 <style> 规则解析后内联为 style 属性（粘贴公众号不重排）
# --------------------------------------------------------------------------- #
INHERITABLE = ("color", "font-family", "font-size", "line-height", "text-align")
_VOID = {"br", "img", "hr", "meta", "link", "input", "source", "wbr"}


def _parse_css_rules(css):
    """解析 <style>：剥注释/删 at-rules（@media print 绝不能内联）/解 :root 变量。

    返回 [(selector, [(prop, val)])]。带伪类/伪元素的选择器丢弃（无法静态内联）。
    """
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    root_vars = {}
    rules = []
    i, n = 0, len(css)

    def skip_at(s, i):
        depth = 0
        while i < len(s):
            if s[i] == "{":
                depth += 1
            elif s[i] == "}":
                depth -= 1
                if depth == 0:
                    return i + 1
            elif s[i] == ";" and depth == 0:
                return i + 1
            i += 1
        return i

    def resolve(val):
        for _ in range(3):
            if "var(" not in val:
                break
            val = re.sub(r"var\(\s*(--[\w-]+)\s*\)",
                         lambda m: root_vars.get(m.group(1).strip(), ""), val)
        return val.strip()

    while i < n:
        if css[i] == "@":
            i = skip_at(css, i)
            continue
        nxt = css.find("{", i)
        if nxt == -1:
            break
        sel = css[i:nxt].strip()
        depth, j = 1, nxt + 1
        while j < n and depth:
            if css[j] == "{":
                depth += 1
            elif css[j] == "}":
                depth -= 1
            j += 1
        body = css[nxt + 1:j - 1] if depth == 0 else css[nxt + 1:j]
        if sel.lower().startswith(":root"):
            for k, v in re.findall(r"(--[\w-]+)\s*:\s*([^;]+)", body):
                root_vars[k.strip()] = v.strip()
        else:
            decls = []
            for d in body.split(";"):
                if ":" not in d:
                    continue
                prop, val = d.split(":", 1)
                prop, val = prop.strip().lower(), resolve(val)
                if prop and val and val.lower() != "inherit":
                    decls.append((prop, val))
            for one in sel.split(","):
                one = one.strip()
                if one and ":" not in one and decls:
                    rules.append((one, decls))
        i = j
    return rules


_COMPOUND_RE = re.compile(r"^(?:([a-zA-Z][\w-]*))?((?:\.[\w-]+)*)?(?:#([\w-]+))?$")


def _compound_match(compound, tag, classes, el_id):
    m = _COMPOUND_RE.match(compound.strip())
    if not m:
        return False
    t, cls, idn = m.group(1), m.group(2), m.group(3)
    if t and t.lower() != tag:
        return False
    if cls:
        need = [c[1:] for c in cls.split(".") if c]
        if not all(c in classes for c in need):
            return False
    if idn and idn != el_id:
        return False
    return bool(t or cls or idn)


class _Inliner(HTMLParser):
    """重建 HTML：匹配规则声明 + 祖先可继承属性写入每个元素 style。

    <style> 块原样保留（悬停/斑马纹等伪类仍靠它，本地渲染不退化；
    微信粘贴时被剥离也无损——排版已内联）。
    """

    def __init__(self, rules):
        super().__init__(convert_charrefs=True)
        self.rules = rules
        self.out = []
        self.stack = []  # [(tag, classes, id, inherited{prop:val})]
        self.skip_depth = 0

    def _matched(self, tag, classes, el_id):
        got = []
        for sel, decls in self.rules:
            parts = sel.split()
            if not _compound_match(parts[-1], tag, classes, el_id):
                continue
            if len(parts) > 1:
                # 祖先链粗匹配：按序在栈里找各 compound
                ai = 0
                for (atag, acls, aid, _inh) in self.stack:
                    if ai < len(parts) - 1 and _compound_match(parts[ai], atag, acls, aid):
                        ai += 1
                if ai < len(parts) - 1:
                    continue
            got.append(decls)
        return got

    def _emit_tag(self, tag, attrs, self_closing=False):
        attrd = dict(attrs)
        classes = set((attrd.get("class") or "").split())
        el_id = attrd.get("id") or ""
        parent_inh = self.stack[-1][3] if self.stack else {}
        style_items = dict(parent_inh)
        for decls in self._matched(tag, classes, el_id):
            style_items.update(decls)
        inh = {k: v for k, v in style_items.items() if k in INHERITABLE}
        attrs_out = []
        existing_style = None
        for k, v in attrs:
            if k.lower() == "style":
                existing_style = v
                continue
            attrs_out.append((k, v))
        css = ";".join("%s:%s" % (k, v) for k, v in style_items.items() if v)
        if existing_style:
            css = (css + ";" + existing_style) if css else existing_style
        if css:
            attrs_out.append(("style", css))
        buf = ["<", tag]
        for k, v in attrs_out:
            buf.append(" %s" % k if v is None
                       else ' %s="%s"' % (k, esc_attr(v)))
        buf.append("/>" if self_closing else ">")
        self.out.append("".join(buf))
        if not self_closing and tag not in _VOID:
            self.stack.append((tag, classes, el_id, inh))

    def handle_starttag(self, tag, attrs):
        if tag == "style":
            self.skip_depth += 1
        self._emit_tag(tag, attrs)

    def handle_startendtag(self, tag, attrs):
        self._emit_tag(tag, attrs, self_closing=True)

    def handle_endtag(self, tag):
        if tag == "style":
            self.skip_depth = max(self.skip_depth - 1, 0)
            self.out.append("</style>")
            return
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
        self.out.append("</%s>" % tag)

    def handle_data(self, data):
        if self.skip_depth:
            self.out.append(data)
        else:
            self.out.append(html.escape(data, quote=False))

    def handle_decl(self, decl):
        self.out.append("<!%s>" % decl)

    def handle_comment(self, data):
        self.out.append("<!--%s-->" % data)

    def handle_entityref(self, name):
        self.out.append("&%s;" % name)

    def handle_charref(self, name):
        self.out.append("&#%s;" % name)


def inline_css(doc_html):
    """把文档 <style> 内联进各元素 style 属性，返回新 HTML。"""
    m = re.search(r"<style[^>]*>(.*?)</style>", doc_html, re.S)
    if not m:
        return doc_html
    rules = _parse_css_rules(m.group(1))
    p = _Inliner(rules)
    p.feed(doc_html)
    p.close()
    return "".join(p.out)


def main():
    ap = argparse.ArgumentParser(description="Omni 解析结果 → 展示用 HTML（自包含单文件）")
    ap.add_argument("--json", help="中间 JSON（markdown+grounding+outline）")
    ap.add_argument("--md", help="直接输入 markdown 文件（agent 产物/提纲）")
    ap.add_argument("--out", required=True, help="输出 .html")
    ap.add_argument("--profile", default="default",
                    help="场景制式：预设名（gov/legal/finance/academic/default）或内联 JSON / .json 文件")
    ap.add_argument("--no-toc", action="store_true", help="不生成目录")
    ap.add_argument("--toc-depth", type=int, default=2, help="目录收录的最大标题层级（默认 2）")
    ap.add_argument("--page-marks", action="store_true", help="标注源页码（需 grounding）")
    ap.add_argument("--strip-emoji", action="store_true", help="剥离 emoji/装饰符号")
    ap.add_argument("--pdf", action="store_true", help="同时用 headless 浏览器导出 PDF（打印保真）")
    ap.add_argument("--inline", action="store_true",
                    help="CSS 全部内联为 style 属性（微信/公众号粘贴不重排；伪类仍保留在 <style>）")
    ap.add_argument("--title", help="覆盖文档标题")
    ap.add_argument("--source-label", help="页首来源署名（默认不显示原始路径；需要溯源时显式给名）")
    args = ap.parse_args()
    if not args.json and not args.md:
        ap.error("--json 或 --md 必须提供一个")

    if args.profile.strip().startswith("{"):
        pcfg = json.loads(args.profile)
    elif args.profile.strip().endswith(".json"):
        with open(args.profile.strip(), encoding="utf-8") as f:
            pcfg = json.load(f)
    else:
        if args.profile not in DOC_PROFILES:
            ap.error("--profile 未知预设 %r" % args.profile)
        pcfg = DOC_PROFILES[args.profile]

    if args.md:
        with open(args.md, encoding="utf-8") as f:
            data = {"markdown": f.read(), "source": args.md}
    else:
        with open(args.json, encoding="utf-8") as f:
            data = json.load(f)

    want_strip = args.strip_emoji or bool(pcfg.get("strip_emoji"))

    # 主题解析（与 PPTX 同套配色，保证跨格式视觉一致）
    pk = args.profile.strip()
    theme = HTML_THEMES.get(pk if not (pk.startswith("{") or pk.endswith(".json")) else "",
                           HTML_THEMES["default"])

    def prep(md):
        if want_strip:
            md = strip_emoji(md)
        return md

    used = set()
    doc_title = args.title or data.get("title")
    parts_head, parts_body, all_toc = [], [], []

    if data.get("sources") or data.get("analysis"):
        sources = list(data.get("sources") or [])
        analysis = data.get("analysis")
        if analysis:
            ana = dict(analysis) if isinstance(analysis, dict) else {"markdown": str(analysis)}
            ana.setdefault("source", "整合分析")
            sources.insert(0, ana)
        for i, s in enumerate(sources):
            md = prep(s.get("markdown") or "")
            t_title, md = extract_title(md)
            chapter = (s.get("source") or "来源 %d" % (i + 1)).strip()
            body, toc_items, footnotes, foot = render_source(
                md, s.get("outline"), s.get("grounding"), pcfg, used,
                args.page_marks, level_offset=1)
            all_toc.append((1, chapter, slug(chapter, used)))
            all_toc.extend(toc_items)
            parts_body.append('<article><h1 id="%s">%s</h1>%s%s</article>'
                              % (esc_attr(all_toc[-len(toc_items) - 1][2] if toc_items else slug(chapter, used)),
                                 esc(chapter), "".join(body), endnotes_html(foot)))
        if data.get("sources"):
            rows = "".join(
                "<tr><td>%s</td><td>%s</td></tr>"
                % (esc((s.get("source") or "来源 %d" % (i + 1)).strip()),
                   esc(str(s.get("detail") or "")))
                for i, s in enumerate(data.get("sources") or []))
            parts_body.append('<section class="appendix"><h2>证据溯源附录</h2>'
                              '<table><thead><tr><th>来源</th><th>解析级别</th></tr>'
                              '</thead><tbody>%s</tbody></table></section>' % rows)
    else:
        md = prep(data.get("markdown") or "")
        t_title, md = extract_title(md)
        if not doc_title and t_title:
            doc_title = t_title
        body, toc_items, footnotes, foot = render_source(
            md, data.get("outline"), data.get("grounding"), pcfg, used, args.page_marks)
        parts_body.append("".join(body))
        parts_body.append(endnotes_html(foot))
        all_toc.extend(toc_items)

    # 封面 hero（主题色块 + 标题 + 来源/日期），替代旧居中 doc-title
    if doc_title:
        sub = ""
        if args.source_label:
            sub = ('<p class="sub">%s</p>' % esc(args.source_label))
        parts_head.append(
            '<header class="hero"><h1>%s</h1>%s'
            '<p class="src">Omni 解析重建 · 展示版</p></header>'
            % (esc(doc_title), sub))
    if not args.no_toc:
        parts_head.append(toc_html(all_toc, args.toc_depth))

    doc = ("<!DOCTYPE html>\n<html lang=\"zh-CN\"><head><meta charset=\"utf-8\">"
           "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
           "<title>%s</title><style>%s</style></head><body>%s%s</body></html>\n"
           % (esc(doc_title or "Omni 文档"), css_for(pcfg, args.page_marks, theme),
              "".join(parts_head), "".join(parts_body)))

    if args.inline:
        doc = inline_css(doc)

    out = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    print("HTML 已生成：%s（%d 字节%s）"
          % (out, os.path.getsize(out), "，CSS 已内联" if args.inline else ""))

    if args.pdf:
        pdf_path = os.path.splitext(out)[0] + ".pdf"
        ok, msg = html_to_pdf(out, pdf_path)
        print("PDF：%s" % (msg if ok else "跳过 —— " + msg))


if __name__ == "__main__":
    main()
