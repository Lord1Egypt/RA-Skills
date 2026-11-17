#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""crosscheck.py — 三件套一致性校验（html / md / pdf 是否都拿到了 content.json 的内容）。

为什么必须跑：三个渲染器是各自实现的，字段口径会漂移，而且丢了东西**不报错**。
实测抓到过的静默丢失：

  1. export_pdf 的封底只读 fields.groups，而 content-schema 规定用 contacts
     → 整页联系方式在 PDF 里消失，HTML 好好在那儿
  2. draw_divider 读 fields.sub，而 schema 与 HTML 用 subtitle
     → 4 个分隔页的英文副标题在 PDF 里消失
  3. draw_cover 拼 meta 时用了一个 schema 里没有的 issue_date
     → 封面只剩「第22期 | 2026」，年月凭空不见
  4. export_editable 不导出 article.fields.abstract
     → 编辑在 Word 里看不到摘要，自然也改不到

用法：

    python crosscheck.py --content content.json \
        --html build/draft.html --md editable/draft.md --pdf build/draft.pdf

省略哪个就跳过哪个。缺 pymupdf 时自动跳过 pdf。
退出码 0 = 一致，1 = 有缺失。

另外扫一遍 content.json 里的**过程标记**（`⟨待确认⟩` 这类）：三个渲染器都不清理它们，
写进字段值会**直接印进成品**，所以只报 WARN 不判失败（硬规则 28）。

命令里的 `python`：Windows 用 `python`，macOS/Linux 用 `python3`。
"""
import argparse
import io
import json
import os
import re
import sys

try:
    import unicodedata
except ImportError:                                    # pragma: no cover
    unicodedata = None

# 文字稿（md）按设计不承载纯版面字段，缺了不算漏
MD_SKIP = ("subtitle", "kicker", "dek", "org", "toc-item")


def norm(s):
    if unicodedata:
        # NFKC：把 PDF 里的连字 ﬁ/ﬀ 与全角标点折回常规字符
        s = unicodedata.normalize("NFKC", str(s))
    # 行内标记在 PDF/DOCX 里是渲染效果，不是字符，比对前必须剥掉，
    # 否则「**误判二**」永远在 PDF 里找不到（PDF 里只有「误判二」）。
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", str(s))
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"\1", s)
    s = re.sub(r"`([^`]*)`", r"\1", s)
    # 图位占位装饰：三个渲染器都会剥掉（`图位待补：X` / `X（图位待补）` /
    # `⟨待补图⟩ X` / 空图位的 `图位待补` 标签），比对前同步归一化，
    # 否则「图补上了、装饰还留着」这类已修好的差异会被反报成缺失。
    s = re.sub(
        r"[\[【⟨<]\s*(?:图位)?待补(?:图)?\s*[\]】⟩>]\s*[:：]?\s*"
        r"|图位待补\s*[:：]?\s*"
        r"|[（(]\s*(?:图位)?待补(?:图)?\s*[）)]\s*",
        "", s)
    return (re.sub(r"\s+", "", s)
            .replace("&amp;", "&")
            .replace("&nbsp;", "")
            .replace("&#39;", "'")
            .replace("&quot;", '"'))


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def _add(out, v, tag):
    v = strip_tags(re.sub(r"<br\s*/?>", " ", str(v or ""))).strip()
    if len(v) >= 6:
        out.append((tag, v))


def collect(content):
    """从 content.json 收集应当出现在每个成品里的文本片段。"""
    out = []
    for pi, pg in enumerate(content.get("pages", [])):
        f = pg.get("fields") or {}
        for k in ("title", "org", "subtitle", "issue_no", "yearmonth", "year",
                  "quote", "source", "note", "label", "section", "dek",
                  "kicker", "abstract", "byline"):
            _add(out, f.get(k), "P%d.%s" % (pi + 1, k))
        for nm in f.get("names", []) or []:
            _add(out, nm, "P%d.names" % (pi + 1))
        for gp in f.get("groups", []) or []:
            _add(out, gp.get("title"), "P%d.toc-group" % (pi + 1))
            for it in gp.get("items", []) or []:
                _add(out, it.get("title"), "P%d.toc-item" % (pi + 1))
        for ct in f.get("contacts", []) or []:
            _add(out, ct.get("name"), "P%d.bc-name" % (pi + 1))
            for ln in ct.get("lines", []) or []:
                _add(out, ln, "P%d.bc-line" % (pi + 1))
        for ui, u in enumerate(pg.get("units", []) or []):
            for k in ("title", "meta", "cta"):
                _add(out, u.get(k), "P%d.u%d.%s" % (pi + 1, ui, k))
            body = str(u.get("body", "")).split("\n\n")[0]
            _add(out, body, "P%d.u%d.body" % (pi + 1, ui))
        for bi, b in enumerate(pg.get("blocks", []) or []):
            if b.get("text"):
                _add(out, str(b["text"]).split("\n")[0], "P%d.b%d.text" % (pi + 1, bi))
            if b.get("caption"):
                _add(out, b["caption"], "P%d.b%d.caption" % (pi + 1, bi))
    return out


def load_text(path, is_html):
    raw = io.open(path, encoding="utf-8", errors="ignore").read()
    if not is_html:
        return norm(raw)
    return norm(strip_tags(raw).replace("&lt;", "<").replace("&gt;", ">"))


def load_pdf(path):
    try:
        import pymupdf
    except ImportError:
        return None, 0
    try:
        d = pymupdf.open(path)
        return norm("".join(p.get_text() for p in d)), d.page_count
    except Exception as e:
        print("  [警告] PDF 读取失败：%s" % e)
        return None, 0


MARK_CHARS = ("\u27e8", "\u27e9")   # 尖括号，过程标记统一用它


def scan_markers(content):
    """扫出所有残留的过程标记。返回 [(json 路径, 片段)]。

    为什么单独查这个：`\u27e8待确认\u27e9` / `\u27e8待补图\u27e9` 是给 agent 自己看的占位，
    渲染器**不会**清理它们（只有 plan_images.py 在图注里剥掉），
    所以一旦写进字段值就会原样印进 PDF / docx——版面不报错、下面的一致性比对也不报错。
    那是交到用户手上的刊物里出现「\u27e8待确认\u27e9」，属于当众出丑，必须拦。
    """
    hits = []

    def walk(o, path):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, "%s.%s" % (path, k))
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, "%s[%d]" % (path, i))
        elif isinstance(o, str):
            if any(c in o for c in MARK_CHARS):
                hits.append((path, o))

    walk(content, "")
    return hits


def main():
    ap = argparse.ArgumentParser(description="校验三件套是否都拿到了 content.json 的内容")
    ap.add_argument("--content", required=True)
    ap.add_argument("--html")
    ap.add_argument("--md")
    ap.add_argument("--pdf")
    a = ap.parse_args()

    content = json.load(io.open(a.content, encoding="utf-8"))

    marks = scan_markers(content)
    if marks:
        print("[WARN] content.json 有 %d 处过程标记，三个渲染器都不会清理它们，"
              "会原样印进成品：" % len(marks))
        for mp, mv in marks[:8]:
            print("       %-26s %s" % (mp.lstrip("."), mv[:44]))
        if len(marks) > 8:
            print("       …… 另有 %d 处" % (len(marks) - 8))
        print("       外推项请写进 pending.md，不要写进字段值（硬规则 28）")

    items = collect(content)
    print("待校文本片段 %d 条 / 来自 %s" % (len(items), a.content))

    texts = {}
    for name, path, is_html in (("html", a.html, True), ("md", a.md, False)):
        if path and os.path.exists(path):
            texts[name] = load_text(path, is_html)
        elif path:
            print("  [跳过] %s 不存在：%s" % (name, path))
    if a.pdf and os.path.exists(a.pdf):
        t, n = load_pdf(a.pdf)
        if t is not None:
            texts["pdf"] = t
            print("  pdf 已载入：%d 页" % n)
    elif a.pdf:
        print("  [跳过] pdf 不存在：%s" % a.pdf)

    if not texts:
        print("[ERR] 没有任何成品可校：至少给一个 --html / --md / --pdf")
        return 2

    bad = 0
    for name, t in texts.items():
        pool = [x for x in items
                if not (name == "md" and x[0].split(".")[-1] in MD_SKIP)]
        # 两侧都必须过同一套 norm，否则 NFKC/去空白只在 target 生效时会满屏误报
        miss = []
        for tag, v in pool:
            nv = norm(v)
            if nv not in t and nv.lstrip("—") not in t:
                miss.append((tag, v))
        if miss:
            bad += 1
            print("\n  x %s 缺 %d 条：" % (name.upper(), len(miss)))
            for tag, v in miss[:15]:
                print("      %-16s %s" % (tag, v[:46]))
            if len(miss) > 15:
                print("      …… 另有 %d 条" % (len(miss) - 15))
        else:
            print("  ok %s 全覆盖（%d 条）" % (name.upper(), len(pool)))

    print("\n结论：%s" % ("三件套一致" if bad == 0 else "%d 个版本有缺失" % bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
