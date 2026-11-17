#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown -> 印象笔记「超级笔记」原生 ENML

这个脚本封装了踩坑得到的全部格式规则。**格式细节不要改**，
否则印象笔记客户端同步时会「规范化」内容，把样式拍平。

核心规则（血泪教训）：
 1. 代码块必须是「一个 div + --en-codeblock + 真正的换行符」，
    绝不能每行一个 div（会产生巨大行距），
    也不能自己写 <span color> 上色（客户端会拍平丢色），
    更不能在自定义 div 上写 font-family: monospace（触发代码块拍平）。
    语法高亮由客户端依据 --en-meta 里的 lang 自己渲染。
 2. 标题用 other-props:base64({"blockId":...})，这样客户端才认为是原生标题。
 3. 内容开头不要写 <?xml?> 声明。
 4. 空行只加在「代码块之后」和「下一个标题之前」（即一节内容结束处）。

用法:
  python markdown_to_enml.py <input.md> -o out.enml [--lang C++]
      [--drop-first-title] [--promote 1] [--titles titles.json]
"""
import argparse
import base64
import json
import os
import random
import re
import string
import sys

# Windows 控制台默认 GBK，强制 UTF-8，避免输出中文/emoji 时崩溃
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ===== 来自 PDF 提取的 Atom One Light 代码配色（仅作文档参考，实际上色由客户端完成）=====
# #4078F2 预处理 # | #A626A4 关键字 | #50A14F 字符串/头文件 | #986801 类型/数字
# #C18401 函数名 | #336DF4 类名 | #0184BB 常量 | #A0A1A7 注释 | #2B2F36 默认

# ===== 正文强调样式（照印象笔记客户端原生写法）=====
C_CODE_BG = "#ECEAE6"   # 行内代码：灰底
C_TIP = "#FFDEBD"       # 小提示：橙底
C_WARN_BG = "#FFDCEB"   # 注意：粉底
C_WARN_FG = "#FF0000"   # 注意：红字
CELL = ("border-right:1px solid #d9d9d9;border-bottom:1px solid #d9d9d9;"
        "padding:10px;text-align:center;")
BLANK = "<div><br/></div>"

# 印象笔记原生代码块样式（照客户端生成的原样复制，勿改）
CB_STYLE = (
    "--en-codeblock:true;--en-blockId:{bid};--en-meta:{meta};"
    "box-sizing: border-box; padding: 8px; "
    "font-family: Monaco, Menlo, Consolas, &quot;Courier New&quot;, monospace; "
    "font-size: 12px; color: rgb(51, 51, 51); "
    "border-top-left-radius: 4px; border-top-right-radius: 4px; "
    "border-bottom-right-radius: 4px; border-bottom-left-radius: 4px; "
    "background-color: rgb(251, 250, 248); "
    "border: 1px solid rgba(0, 0, 0, 0.14902); "
    "background-position: initial initial; background-repeat: initial initial; "
    "margin-top: 6px;margin-bottom: 6px;"
)

EMOJI_RE = re.compile(r"[✅📌💡❗⚠️]")


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def attr_esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def rand_id(n=11):
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(n))


def block_id():
    return base64.urlsafe_b64encode(os.urandom(8)).decode().rstrip("=")


def hstyle():
    """标题的原生标记：other-props:base64({"blockId":...})"""
    j = json.dumps({"blockId": block_id()}, separators=(",", ":"))
    return "other-props:" + base64.b64encode(j.encode()).decode() + ";"


def meta_for(title, lang):
    """代码块元信息：title 是代码块标题，lang 决定客户端用哪套语法高亮"""
    j = json.dumps({"title": title, "lang": lang, "theme": "default",
                    "showLine": True, "lineWrap": False},
                   ensure_ascii=False, separators=(",", ":"))
    return attr_esc(j)


def inline(t):
    """行内元素：先转义，再处理 `代码` 与 **加粗**"""
    t = esc(t)
    t = re.sub(r"`([^`]+)`",
               lambda m: ('<span style="background-color: %s;">'
                          '<span style="font-weight: bold;">%s</span></span>'
                          % (C_CODE_BG, m.group(1))), t)
    t = re.sub(r"\*\*([^*]+)\*\*",
               lambda m: '<span style="font-weight: bold;">%s</span>' % m.group(1), t)
    return t


def render_codeblock(code_lines, title, lang):
    """整个代码块 = 一个 div + 真正的换行符；上色交给客户端"""
    parts = []
    for ln in code_lines:
        s = ln.lstrip(" ")
        parts.append("&nbsp;" * (len(ln) - len(s)) + esc(s))
    style = CB_STYLE.format(bid=rand_id(), meta=meta_for(title, lang))
    return '<div style="%s">%s</div>' % (style, "\n".join(parts))


def render_quote(raw):
    """引用块 -> 小提示（橙底）/ 注意（红字+粉底）/ 普通 div"""
    txts = [x.strip() for x in raw if x.strip()]
    if not txts:
        return ""
    head = txts[0]
    is_warn = ("注意" in head) or head.startswith("❗") or ("⚠" in head)
    is_tip = (("小提示" in head) or head.startswith("✅")
              or head.startswith("📌") or head.startswith("💡"))
    if not (is_warn or is_tip):
        return "".join("<div>%s</div>" % inline(t) for t in txts)

    bg = C_WARN_BG if is_warn else C_TIP
    out = []
    for t in txts:
        t = EMOJI_RE.sub("", t).strip()
        m = re.match(r"^[-*]\s+(.*)$", t)
        if m:
            t = "• " + m.group(1)
        t = inline(t)
        if is_warn:
            out.append('<div><span style="color: %s;">'
                       '<span style="background-color: %s;">%s</span></span></div>'
                       % (C_WARN_FG, bg, t))
        else:
            out.append('<div><span style="background-color: %s;">%s</span></div>' % (bg, t))
    return "".join(out)


def render_table(rows):
    """表格用印象笔记原生 smarttable 结构"""
    def cells(r):
        r = r.strip()
        r = r[1:] if r.startswith("|") else r
        r = r[:-1] if r.endswith("|") else r
        return [c.strip() for c in r.split("|")]

    header = cells(rows[0])
    body = [cells(r) for r in rows[2:]] if len(rows) > 2 else []
    n = max(1, len(header))
    w = 829 // n
    ts = ("--en-type:smarttable;border-left:1px solid #d9d9d9;"
          "border-top:1px solid #d9d9d9;border-collapse:collapse;width:829px;")

    o = ['<table style="%s" width="829px">' % ts]
    o.append("<colgroup>" + "".join('<col style="width: %dpx;"/>' % w for _ in range(n)) + "</colgroup>")
    o.append("<thead><tr>" + "".join("<td>%s</td>" % inline(h) for h in header) + "</tr></thead>")
    o.append("<tbody>")
    for r in body:
        r = (r + [""] * n)[:n]
        o.append("<tr>" + "".join('<td style="%s">%s</td>' % (CELL, inline(c)) for c in r) + "</tr>")
    o.append("</tbody></table>")
    return "".join(o)


def render_list(items):
    ordered = all(it[1] for it in items)
    tag = "ol" if ordered else "ul"
    o = ["<%s>" % tag]
    for indent, _, text in items:
        o.append("<li><div>%s%s</div></li>" % ("&nbsp;&nbsp;" * indent, inline(text)))
    o.append("</%s>" % tag)
    return "".join(o)


def convert(md_text, lang="C++", drop_first_title=False, promote=0, titles=None):
    lines = md_text.split("\n")
    body, i, cb_idx = [], 0, 0
    titles = titles or []
    pending_title = ""

    while i < len(lines):
        line = lines[i]
        st = line.strip()

        # 代码块标题注释：<!-- title: xxx -->
        m = re.match(r"^<!--\s*title\s*[:：]\s*(.*?)\s*-->$", st, re.I)
        if m:
            pending_title = m.group(1)
            i += 1
            continue

        # 代码块
        if st.startswith("```"):
            fence_info = st[3:].strip()
            i += 1
            code = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            title = pending_title
            pending_title = ""
            if not title and cb_idx < len(titles):
                title = titles[cb_idx]
            cb_idx += 1
            body.append(render_codeblock(code, title, lang))
            body.append(BLANK)          # 代码块后空行
            continue

        # 标题
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            lvl = len(m.group(1))
            if drop_first_title and lvl == 1:
                i += 1
                continue
            lvl = max(1, min(6, lvl + promote))
            # 新标题之前补空行 —— 即「上一节的内容」到此结束
            if body and body[-1] != BLANK:
                body.append(BLANK)
            body.append('<h%d style="%s">%s</h%d>' % (lvl, hstyle(), inline(m.group(2)), lvl))
            i += 1
            continue

        # 分隔线（丢弃）
        if re.match(r"^-{3,}$", st):
            i += 1
            continue

        # 表格
        if st.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            body.append(render_table(rows))
            continue

        # 引用
        if st.startswith(">"):
            raw = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                raw.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            body.append(render_quote(raw))
            continue

        # 列表
        if re.match(r"^\s*([-*]|\d+\.)\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]):
                raw = lines[i]
                ind = 1 if (len(raw) - len(raw.lstrip())) >= 2 else 0
                ordered = bool(re.match(r"^\s*\d+\.\s+", raw))
                items.append((ind, ordered, re.sub(r"^\s*([-*]|\d+\.)\s+", "", raw)))
                i += 1
            body.append(render_list(items))
            continue

        if not st:
            i += 1
            continue

        body.append("<div>%s</div>" % inline(line))
        i += 1

    return ('<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">\n'
            "<en-note>" + "".join(body) + "</en-note>"), cb_idx


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("md")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--lang", default="C++", help="代码块语言，决定客户端语法高亮（默认 C++）")
    ap.add_argument("--drop-first-title", action="store_true",
                    help="丢掉第一个一级标题（笔记标题栏已有，避免重复）")
    ap.add_argument("--promote", type=int, default=0,
                    help="标题层级整体上提 N 级（配合 --drop-first-title 用，通常 1）")
    ap.add_argument("--titles", help="代码块标题 JSON 数组，按出现顺序对应")
    a = ap.parse_args()

    titles = []
    if a.titles:
        if os.path.isfile(a.titles):
            titles = json.load(open(a.titles, encoding="utf-8"))
        else:
            titles = json.loads(a.titles)

    md = open(a.md, encoding="utf-8").read()
    enml, n = convert(md, a.lang, a.drop_first_title, a.promote, titles)
    open(a.out, "w", encoding="utf-8").write(enml)

    print(json.dumps({
        "success": True,
        "out": os.path.abspath(a.out),
        "code_blocks": n,
        "headings": len(re.findall(r"<h[1-6]", enml)),
        "tables": enml.count("<table"),
        "blank_lines": enml.count(BLANK),
        "bytes": len(enml.encode("utf-8")),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
