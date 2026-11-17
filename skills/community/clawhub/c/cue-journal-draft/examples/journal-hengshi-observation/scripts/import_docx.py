#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
import_docx.py — 把编辑在 Word 里改过的 draft.docx 回填成 content.json。

它是 export_editable.py 的逆操作，用来关闭这一圈：

    content.json
      ├─ build_draft.py      → draft.html / draft.pdf  （版面稿）
      ├─ export_editable.py  → draft.docx / draft.md    （可编辑稿）
      └─ import_docx.py      ← draft.docx（编辑改完）   → content.edited.json
           └─ build_draft.py → 新的 draft.html

**回填范围（说清楚，别吹）**
- 能回：全部文字（正文/标题/名单/目录/联系方式/图说）、单元的新增与删除、
       图位原路径（`src` 由 ‖图位‖ 标记携带，Word 里替换过的图不回读）、页码 `folio`。
- 不回：毫米定位（`x_mm` / `top_mm` 等）、背景图图像本身、脚注/批注/修订、
        Word 里新插入的图片文件——这些只在 `--base` 的原始 content.json 里保留，
        所以**一定要带 --base**，否则只能按标记重建空骨架。

用法：
  python import_docx.py --docx out/draft.docx --base content.json --out content.edited.json
  python import_docx.py --docx out/draft.docx --out content.rebuilt.json   # 无 baseline，会警告丢字段

依赖：python-docx（python -m pip install python-docx）

命令里的 `python`：Windows 用 `python`，macOS/Linux 用 `python3`。
"""
import argparse
import json
import os
import re
import sys
from copy import deepcopy

PAGE_MARK = re.compile(r"^‖页\s*(\d+)‖")
IMG_MARK = re.compile(r"^\s*‖图位‖\s*(\{.*\})\s*$")

# 段落样式 → (作用对象, 角色)
STYLE_MAP = {
    "JD p": ("block", "p"), "JD h1": ("block", "h1"), "JD h2": ("block", "h2"),
    "JD li": ("block", "li"), "JD quote": ("block", "quote"),
    "JD disclaimer": ("block", "disclaimer"), "JD note-block": ("block", "note"),
    "JD abstract": ("article", "abstract"),
    "JD caption": ("caption", ""),
    "JD title": ("article", "title"), "JD byline": ("article", "byline"),
    "JD section": ("unit_list", "section"),
    "JD unit-title": ("unit", "title"), "JD unit-body": ("unit", "body"),
    "JD unit-meta": ("unit", "meta"), "JD cta": ("unit", "cta"),
    "JD toc-title": ("toc", "title"), "JD toc-group": ("toc", "group"),
    "JD toc-item": ("toc", "item"),
    "JD quote-text": ("quote", "text"), "JD quote-src": ("quote", "source"),
    "JD cover-no": ("cover", "issue_no"), "JD cover-ym": ("cover", "yearmonth"),
    "JD cover-year": ("cover", "year"),
    "JD names": ("masthead", "name"), "JD meta": ("masthead", "note"),
    "JD mh-title": ("masthead", "title"),
    "JD bc-title": ("backcover", "name"), "JD bc-line": ("backcover", "line"),
    "JD figure": ("figure", ""), "JD note": ("note", ""),
    "JD running": ("skip", ""), "JD mark": ("mark", ""),
}


def _read_docx(path):
    try:
        from docx import Document
        from docx.oxml.ns import qn
    except ImportError:
        sys.exit("[ERR] 需要 python-docx：python -m pip install python-docx")
    return Document(path), qn


def walk_text(p_el, qn, out):
    for c in list(p_el):
        t = c.tag
        if t == qn("w:r"):
            seg = []
            for d in list(c):
                if d.tag == qn("w:t"):
                    seg.append(d.text or "")
                elif d.tag in (qn("w:br"), qn("w:cr")):
                    seg.append("\n")
                elif d.tag == qn("w:tab"):
                    seg.append("\t")
            s = "".join(seg)
            # 行内加粗在 Word 里是 run 属性、不是字符，而 content.json 用 `**…**` 表达。
            # 不回写这对星号，编辑在 Word 里看到的加粗改一次稿就没了（实测 issue-22
            # 有 20+ 处 `**…**` 会被静默抹掉）。只认 run 级 w:b —— 样式级加粗
            # （JD h1/标题之类的整段加粗）不算，否则标题会被包上星号。
            if s and s.strip() and _run_bold(c, qn):
                s = "**" + s + "**"
            out.append(s)
        elif t in (qn("w:hyperlink"), qn("w:ins"), qn("w:sdtContent")):
            walk_text(c, qn, out)
    return out


def _run_bold(r_el, qn):
    """run 是否**显式**加粗（只看直接格式，不看段落样式继承）。"""
    for rpr in r_el.findall(qn("w:rPr")):
        for b in rpr.findall(qn("w:b")):
            v = b.get(qn("w:val"))
            if v is None or str(v).lower() not in ("0", "false", "off"):
                return True
    return False


def has_drawing(p_el, qn):
    return p_el.find(".//" + qn("w:drawing")) is not None or p_el.find(".//" + qn("w:pict")) is not None


def iter_paragraphs(doc, qn):
    """正文段落（跳过页眉页脚）→ [(style_name, text, has_picture)]"""
    for p in doc.paragraphs:
        buf = []
        walk_text(p._p, qn, buf)
        yield p.style.name if p.style else "Normal", "".join(buf), has_drawing(p._p, qn)


def parse_mark(text):
    """从 ‖页 NN‖ ... ‖{json}‖ 里取 payload（不能 rfind「‖」——JSON 自己就是被 ‖ 包着的）。"""
    a = text.find("{")
    b = text.rfind("}")
    if a >= 0 and b > a:
        try:
            return json.loads(text[a:b + 1])
        except Exception:
            return None
    return None


# --------------------------------------------------------------------------
# 解析：把 Word 段落流还原成 page 结构
# --------------------------------------------------------------------------
def parse_docx(path):
    doc, qn = _read_docx(path)
    pages = []
    cur = None
    pending_img = None
    units = None
    contacts = None
    last_caption_target = None

    def new_page(payload):
        f = dict(payload.get("meta") or {})
        return {"template": payload.get("template", "article"),
                "grid": payload.get("grid") or "",
                "folio": payload.get("folio") or "",
                "meta": f, "fields": {}, "units": [], "blocks": [],
                "index": payload.get("i", len(pages))}

    for style, text, pic in iter_paragraphs(doc, qn):
        if style == "JD mark":
            if PAGE_MARK.match(text):
                payload = parse_mark(text) or {}
                if cur is not None:
                    pages.append(cur)
                cur = new_page(payload)
                units, contacts = cur["units"], None
                last_caption_target = None
                pending_img = None
            else:
                m = IMG_MARK.match(text)
                if m:
                    try:
                        pending_img = json.loads(m.group(1))
                    except Exception:
                        pending_img = None
            continue

        if cur is None:
            continue  # 标记前的说明段，丢弃

        kind, role = STYLE_MAP.get(style, ("skip", ""))
        if kind in ("skip", "mark"):
            continue
        if pending_img is not None:
            if kind == "figure" or pic:
                apply_img(cur, pending_img, text, units)
                last_caption_target = pending_img
                pending_img = None
                continue
            # 图缺 normative 承载段（占位被删了），先把_pending 挂上去
            apply_img(cur, pending_img, None, units)
            pending_img = None
        if kind == "figure":
            continue  # 图片承载段本身
        if kind == "caption":
            set_caption(cur, text, last_caption_target)
            continue
        route(cur, kind, role, text, units, contacts)

    if cur is not None:
        pages.append(cur)
    return pages, doc


def _units_of(page):
    return page["units"]


def apply_img(page, img, _text, units):
    kind = img.get("kind")
    src = img.get("src") or ""
    if kind == "bg":
        page.setdefault("images", {})["bg"] = src
    elif kind == "banner":
        page["fields"]["banner"] = src
    elif kind == "hero":
        page["fields"]["hero"] = src
    elif kind == "unit-image":
        if units:
            units[-1]["image"] = src
    elif kind == "figure":
        page["blocks"].append(fig_block(src))


def set_caption(page, text, target):
    if not text.strip():
        return
    if target and target.get("kind") in ("banner", "hero", "unit-image"):
        return
    for b in reversed(page["blocks"]):
        if b.get("type") == "figure":
            b["caption"] = text.strip()
            return
    if target and target.get("kind") == "figure":
        page["blocks"].append(fig_block(target.get("src"), text.strip()))


def fig_block(src, caption=""):
    """figure 块：`src` 为空时**不写这个键**。

    schema 的约定是「`src` 有值则出图，无值出占位框」，空串与缺键等价；
    但写成空串会让回填 diff 每次都报一条「src 新增：（空）」的假改动。
    """
    b = {"type": "figure", "caption": caption}
    if str(src or "").strip():
        b["src"] = src
    return b


def route(page, kind, role, text, units, contacts):
    t = text.strip()
    tpl = page["template"]
    f = page["fields"]
    if kind == "cover":
        f[role] = text.strip()
    elif kind == "quote":
        f["quote" if role == "text" else "source"] = text.strip()
    elif kind == "masthead":
        if role == "title":
            f["title"] = t
        elif role == "name":
            page.setdefault("_names", [])
            page["_names"].extend([x.strip() for x in re.split(r"\s*/\s*", t) if x.strip()])
        else:
            f["note"] = text.strip()
    elif kind == "toc":
        if role == "title":
            f["title"] = t
        elif role == "group":
            no, _, title = t.partition("\t")
            page.setdefault("_toc", []).append({"no": no.strip(), "title": title.strip(), "items": []})
        elif role == "item":
            title, _, pg = t.partition("\t")
            if page.get("_toc"):
                page["_toc"][-1]["items"].append(toc_item(title, pg))
    elif kind == "unit_list":
        f["section"] = text.strip()
    elif kind == "unit":
        if role == "title":
            units.append({"title": t, "body": "", "cta": ""})
        elif role == "body":
            if not units:
                units.append({"title": "", "body": "", "cta": ""})
            u = units[-1]
            u["body"] = (u["body"] + "\n\n" + t) if u.get("body") else t
        elif role == "meta":
            if not units:
                units.append({"title": "", "body": "", "cta": ""})
            units[-1]["meta"] = t
        elif role == "cta":
            if units:
                units[-1]["cta"] = t
    elif kind == "article":
        if role == "title":
            f["title"] = text.strip()
        elif role == "abstract":
            f["abstract"] = text.strip()
        else:
            f["byline"] = text.strip()
    elif kind == "block":
        page["blocks"].append({"type": role, "text": text.strip()})
    elif kind == "note":
        # 「[分隔页，无正文]」是导出时给编辑看的占位说明，不当正文回填
        if tpl == "divider" and t and not t.startswith("["):
            f["label"] = t
    elif kind == "backcover":
        page.setdefault("_contacts", [])
        if role == "name":
            page["_contacts"].append({"name": t, "lines": []})
        elif role == "line" and page["_contacts"]:
            page["_contacts"][-1]["lines"].append(t)


# --------------------------------------------------------------------------
# 组装：合并 base（保住 mm 定位与非文字字段）
# --------------------------------------------------------------------------
def finalize(page):
    tpl = page["template"]
    out = {}
    base_fields = dict(page.get("_base_fields") or {})
    base_units = base_fields.pop("_units", [])
    meta = dict(page.get("meta") or {})

    # 页面级：template / grid / folio / 其余原样（含 x_mm 等若被放进 meta）
    out["template"] = tpl
    if page.get("grid"):
        out["grid"] = page["grid"]
    if page.get("folio"):
        out["folio"] = page["folio"]
    for k, v in meta.items():
        out.setdefault(k, v)
    if page.get("images"):
        out["images"] = page["images"]

    f = {}
    for k, v in base_fields.items():
        f[k] = v
    for k, v in page["fields"].items():
        f[k] = v
    if "_names" in page:
        f["names"] = page["_names"]
    if "_toc" in page:
        f["groups"] = page["_toc"]
    if "_contacts" in page:
        f["contacts"] = page["_contacts"]
    out["fields"] = f

    if page["units"]:
        # 用 base_units（已从 base_fields 里 pop 出来）——早先这里又写
        # `base_fields.get("_units", [])`，pop 之后恒为空列表，于是 clean_unit
        # 的 base 永远是 {}，所有「照抄 base」的分支都是死代码。
        out["units"] = [clean_unit(u, b) for u, b in zip_all(page["units"], base_units)]
    if page["blocks"]:
        out["blocks"] = page["blocks"]
    return out


def zip_all(a, b):
    for i, u in enumerate(a):
        yield u, (b[i] if i < len(b) else {})


_PAGE_LIKE = re.compile(r"^[\d\s\-–—~至/、,，.]+$")


def toc_item(title, rhs):
    """目录项：右侧是页码还是锚点，按形态判断。

    实测 issue-22 用 `ref` 锚点（页码交给渲染器从 anchor_map 解析）。若回填时
    一律写成 `page`，锚点就没了 —— 重新合版目录页码整列消失，而且是静默的。
    """
    it = {"title": title.strip()}
    v = rhs.strip()
    if v:
        it["page" if _PAGE_LIKE.match(v) else "ref"] = v
    return it


def clean_unit(u, base):
    """单元回填。

    可选字段（image / cta / meta）的**空值**处理是这里唯一有坑的地方：解析端对每个
    单元都会给出 `cta: ""`（没有 CTA 也是空串），因此无法与「编辑把 CTA 删了」区分。
    规则：空值以 base 的**键是否存在**为准 —— base 有键（哪怕空串）就照抄，base 没有
    就不写键。否则回填 diff 会冒出纯键存在性噪声（实测 issue-22 P19 报 4 条
    「cta 新增：」、改成不写键后又把 P17 的 8 条报成「cta 被删除」）。

    已知限界：编辑在 Word 里**清空**一个原本有值的 CTA，无法表达为删除，会被恢复。
    """
    out = {"title": u.get("title", "")}
    if u.get("body"):
        out["body"] = u["body"]
    for key in ("image", "cta", "meta"):
        v = u.get(key) or base.get(key)
        if v or key in base:
            out[key] = v or ""
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--docx", required=True)
    ap.add_argument("--base", default=None, help="原始 content.json，用于保住 mm 定位等不可回读字段")
    ap.add_argument("--out", default="content.edited.json")
    ap.add_argument("--issue", default=None, help="覆盖 issue 块（JSON 字符串）")
    args = ap.parse_args()

    pages, doc = parse_docx(args.docx)

    base = None
    base_pages = []
    if args.base and not os.path.isfile(args.base):
        # 目录也会 exists() 为真，用户很容易把 --base 写成目录（名字里有 base），
        # 然后拿到一个看不出所以然的 PermissionError 堆栈
        sys.exit("[ERR] --base 要的是**原始 content.json 文件**，不是目录：%s\n"
                 "      （传目录是 export_editable.py 的 --base-dir，两个参数别混）"
                 % args.base)
    if args.base:
        with open(args.base, encoding="utf-8") as f:
            base = json.load(f)
        base_pages = base.get("pages", [])
    else:
        sys.stderr.write("[WARN] 未给 --base：无法保住 x_mm / top_mm 等毫米定位，"
                         "Word 里替换过的图片也回不来\n")

    for p in pages:
        i = p["index"]
        bp = base_pages[i] if i < len(base_pages) else None
        if bp and bp.get("template") == p["template"]:
            p["_has_base"] = True
            p["_base_fields"] = deepcopy(bp.get("fields") or {})
            p["_base_fields"]["_units"] = deepcopy(bp.get("units") or [])
            kept = (bp.get("images") or {})
            if kept.get("bg") and not p.get("images", {}).get("bg"):
                p.setdefault("images", {})["bg"] = kept["bg"]
            for k, v in bp.items():
                if k not in ("template", "grid", "folio", "fields", "units", "blocks", "images"):
                    p["meta"].setdefault(k, v)
        else:
            p["_base_fields"] = {}

    issue = base.get("issue") if base else {}
    if args.issue:
        try:
            issue = json.loads(args.issue)
        except Exception as e:
            sys.stderr.write("[WARN] --issue 不是合法 JSON，忽略：%s\n" % e)

    # 顶层除 issue/pages 外还有承重块（`meta.freshness_exceptions` / `issue_date` /
    # `window_months`，check_freshness.py 直接读它们）。早先只写 issue+pages，
    # 一趟「改稿 → 回填」就把时效豁免清单和收录窗口静默清空。
    out = dict(base) if base else {}
    out["issue"] = issue or {}
    out["pages"] = [finalize(p) for p in pages]
    if base:
        n = restore_equivalent(out, base)
        if n:
            print("  已回抄 %d 处「写法不同、内容等价」的字段（<br>/空白，非编辑改动）" % n)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    def n(x):
        return len(x) if x is not None else 0

    print("OK pages=%d units=%d blocks=%d" % (
        len(pages), sum(n(p.get("units")) for p in pages),
        sum(n(p.get("blocks")) for p in pages)))
    print("out : %s" % os.path.abspath(args.out))
    if base_pages and len(base_pages) != len(pages):
        print("  [!] 页数变了：原 %d 页 → 现 %d 页（Word 里增/删了整页）"
              % (len(base_pages), len(pages)))
    miss = [i for i, p in enumerate(pages) if not p.get("_has_base")]
    if miss:
        print("  [!] 第 %s 页找不到原始对照（新增页/模板改动），这些页只有 Word 里的字段"
              % ",".join(str(i + 1) for i in miss))
    changed = diff_summary(base_pages, out["pages"]) if base_pages else []
    if changed:
        print("改动清单（相对 %s）共 %d 处：" % (os.path.basename(args.base), len(changed)))
        for line in changed[:12]:
            print("  · " + line)
        if len(changed) > 12:
            print("  … 其余 %d 处省略" % (len(changed) - 12))
    else:
        print("改动清单：与原始 content.json 一致（未发现文字改动）")


def page_text(p):
    """把一页摊平成 [(路径, 文本)]，用来比对改动。"""
    out = []
    f = p.get("fields") or {}
    for k in sorted(f):
        v = f[k]
        if isinstance(v, str):
            out.append(("fields.%s" % k, v))
        elif isinstance(v, list):
            out.append(("fields.%s" % k, json.dumps(v, ensure_ascii=False)))
    for j, u in enumerate(p.get("units") or []):
        for k in sorted(u):
            if isinstance(u[k], str):
                out.append(("units[%d].%s" % (j, k), u[k]))
    for j, b in enumerate(p.get("blocks") or []):
        for k in sorted(b):
            if isinstance(b[k], str):
                out.append(("blocks[%d].%s" % (j, k), b[k]))
    return out


def norm_cmp(s):
    """比对用的归一化：`<br>` / `**` / 空白在 docx 里是渲染效果，不是字符差异。"""
    s = re.sub(r"<br\s*/?>", "", str(s), flags=re.I)
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    return re.sub(r"\s+", "", s.replace("\u00a0", " "))


def equivalent(a, b):
    """两串「写法不同、内容等价」——不是编辑改动。"""
    return (isinstance(a, str) and isinstance(b, str) and a != b
            and norm_cmp(a) == norm_cmp(b))


def restore_equivalent(out, base):
    """结构对齐且归一化后等价的字段，回抄 base 的原文。

    文字稿经 Word 走一趟，`<br>` 会变真换行、空白会被重排——这些不是编辑改的字。
    不回抄有两个后果：①改动清单里满屏假改动，真改动被埋掉；②编辑没碰过的字段
    被悄悄换了写法。只在「归一化后完全等价」时回抄，所以不会掩盖真改动。
    """
    hits = [0]

    def walk(o, b):
        if isinstance(o, dict) and isinstance(b, dict):
            for k in list(o):
                if k not in b:
                    continue
                if equivalent(o[k], b[k]):
                    o[k] = b[k]
                    hits[0] += 1
                else:
                    walk(o[k], b[k])
            # base 有、回填结果没有的键，值为 None/空串时补回来 —— 让「没改过稿」
            # 的回填与原文**逐字节一致**（例：figure 的 `"src": null`）。
            for k, v in b.items():
                if k not in o and (v is None or v == ""):
                    o[k] = v
                    hits[0] += 1
        elif isinstance(o, list) and isinstance(b, list) and len(o) == len(b):
            for i in range(len(o)):
                if equivalent(o[i], b[i]):
                    o[i] = b[i]
                    hits[0] += 1
                else:
                    walk(o[i], b[i])

    walk(out, base)
    return hits[0]


def diff_summary(base_pages, out_pages):
    lines = []
    for i, op in enumerate(out_pages):
        bp = base_pages[i] if i < len(base_pages) else None
        if bp is None:
            lines.append("P%02d 为新增页（%s）" % (i + 1, op.get("template")))
            continue
        a = dict(page_text(bp))
        b = dict(page_text(op))
        for k in sorted(set(a) | set(b)):
            va, vb = a.get(k), b.get(k)
            if va == vb or equivalent(va, vb):
                continue
            if vb is None:
                lines.append("P%02d %s 被删除" % (i + 1, k))
            elif va is None:
                lines.append("P%02d %s 新增：%s" % (i + 1, k, short(vb)))
            else:
                lines.append("P%02d %s：%s → %s" % (i + 1, k, short(va), short(vb)))
    return lines


def short(s, n=26):
    s = " ".join(str(s).split())
    return s[:n] + ("…" if len(s) > n else "")


if __name__ == "__main__":
    main()
