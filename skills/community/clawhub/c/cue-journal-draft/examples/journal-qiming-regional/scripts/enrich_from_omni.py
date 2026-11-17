#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
enrich_from_omni.py —— 把 Omni Reader 的富文本解析结果转成 StyleSpec 的「语义层」补丁。

分工（两者不可互相替代）：
  extract_style.py  -> 几何层：页、网格、字号、颜色、图片槽位、物理页 vs 印刷页 offset
  本脚本            -> 语义层：栏目树、文章边界、单元字数分布、题头元信息模板、
                       固定件（CTA / 免责声明 / 分所名录）、术语种子

为什么必须两层：Omni 富文本保留标题树、列表、HTML 表格，但**丢图片**；
几何层保留图片矩形，但**认不出栏目/文章边界**。判据见 references/style-extraction.md。

输入：
  --md         Omni `save_result` 落盘的 Markdown（必须）
  --outline    可选，`read_outline` 的 JSON 原文
  --geo        可选，`extract_style.py` 产出的 stylespec.json
  --out        输出目录

输出：
  semantic.json           语义层结构化结果
  unit-patterns.draft.md  可直接喂给 UnitPattern 模板的草稿
  stylespec.merged.json   几何层 + 语义层合成的 StyleSpec（给了 --geo 才产出）
"""
import argparse
import io
import json
import os
import re
import sys
from collections import Counter, OrderedDict

HEAD_RE = re.compile(r"^(#{1,6})\s+(.*)$")
DATE_RE = re.compile(r"(20\d{2})[.\-/年]\s?(\d{1,2})[.\-/月]\s?(\d{1,2})")
LAW_RE = re.compile(r"《([^》《]{2,60})》")
QUOTE_RE = re.compile(r"[“\"]([^“”\"\n]{3,40})[”\"]")
PART_RE = re.compile(r"^\s*(\d{2})\s*[、.\s]?\s*(.{2,24})$")
OFFICE_RE = re.compile(r"^.{0,4}(总部|分所|分公司|办公室|代表处)$")
CJK = r"\u4e00-\u9fff"
PUNCT = r"\s\u3000-\u303f\uff00-\uffef"


def read_text(path):
    with io.open(path, encoding="utf-8") as f:
        return f.read()


def norm_space(s):
    """把 Omni 对加宽字距输出的散字合回去：'王 维 巍' -> '韦思远'。

    只合并「汉字<空格>汉字」。汉字与数字/西文之间的空格必须保留 ——
    目录条目「XXX 19」的页码靠这个空格才能剥离。
    """
    s = s.replace("\u00a0", " ")
    for _ in range(4):
        s = re.sub(r"(?<=[" + CJK + r"])\s+(?=[" + CJK + r"])", "", s)
    return s


def fingerprint(s):
    """标题指纹：去所有空白与标点，用于和目录条目比对。"""
    return re.sub(r"[" + PUNCT + r"]", "", s)


def blocks_from_md(md):
    lines = md.split("\n")
    heads = []
    for i, ln in enumerate(lines):
        m = HEAD_RE.match(ln)
        if m:
            heads.append({"line": i, "level": len(m.group(1)), "title": norm_space(m.group(2)).strip()})
    uniq = []
    for h in heads:
        if uniq and uniq[-1]["title"] == h["title"] and h["line"] - uniq[-1]["line"] <= 3:
            continue
        uniq.append(h)
    out = []
    for idx, h in enumerate(uniq):
        end = uniq[idx + 1]["line"] if idx + 1 < len(uniq) else len(lines)
        body = norm_space("\n".join(lines[h["line"] + 1:end])).strip()
        out.append({
            "level": h["level"],
            "title": h["title"],
            "line": h["line"],
            "body": body,
            "body_raw": "\n".join(lines[h["line"] + 1:end])[:400],
            "chars": len(re.sub(r"\s+", "", body)),
        })
    return out


# ---------------------------------------------------------------- 目录解析

def _tail_page(s):
    """剥掉尾部的印刷页码，返回 (纯标题, 页码 or None)。"""
    m = re.match(r"^(.*?)\s+(\d{1,3})$", s.strip())
    if m and len(m.group(1)) >= 3:
        return m.group(1).strip(), int(m.group(2))
    return s.strip(), None


def extract_contents(md):
    r"""从 CONTENTS 目录页抽权威清单：栏目 -> 单元标题 -> 印刷页码。

    目录是本刊「自我声明」的结构，比 Omni 给出的 Markdown 标题层级可靠得多。
    难点：目录条目有的带页码、有的不带（多为跨行续出的长标题），
    处理办法按优先级判定：
      1. `^\d{2}\s+\S`  -> 栏目头（即使它带页码也要先当栏目）
      2. 以 `空格+页码` 结尾 -> 完结一条目
      3. 长度 >= 10 -> 一条不带页码的新条目
      4. 短碎片(<10) -> 续接到上一条无页码条目的标题尾部
    """
    lines = md.split("\n")
    start = None
    for i, ln in enumerate(lines):
        if re.match(r"^#{1,6}\s*CONTENTS", ln, re.I):
            start = i + 1
            break
    if start is None:
        return None

    parts, entries = [], []
    cur_part = None
    seen_part_ids = set()
    for i in range(start, min(start + 400, len(lines))):
        ln = lines[i].strip()
        if not ln:
            continue
        m_head = HEAD_RE.match(ln)
        title_line = norm_space(m_head.group(2)).strip() if m_head else norm_space(ln)
        if m_head and m_head.group(1) != "#" and len(title_line) > 40:
            break  # 进入正文的长标题
        if len(title_line) > 120:
            break  # 进入正文段落

        pm = PART_RE.match(title_line)
        if pm and len(pm.group(2)) >= 2:
            # 目录里每个栏目编号只出现一次；正文各栏目页会重复出现 -> 越界信号
            if pm.group(1) in seen_part_ids:
                break
            seen_part_ids.add(pm.group(1))
            name, _pg = _tail_page(pm.group(2))
            cur_part = {"id": pm.group(1), "name": name}
            parts.append(cur_part)
            continue

        bare, page = _tail_page(title_line)
        if page is not None:
            _push(entries, bare, page, cur_part)
            continue
        if len(bare) >= 10:
            _push(entries, bare, None, cur_part)
            continue
        # 短碎片：续接上一条无页码条目（跨行长标题的第二行）
        if entries and entries[-1]["page"] is None:
            entries[-1]["title"] += bare
        elif entries:
            entries[-1]["title"] += bare

    if not entries:
        return None
    return {"parts": parts, "entries": entries}


def _push(entries, bare, page, cur_part):
    title = bare.strip()
    # 目录里常见「同一标题重复印一次」（中英双列），去重
    if not title:
        return
    for e in entries:
        if e["title"] == title:
            if page and not e["page"]:
                e["page"] = page
            return
    entries.append({"title": title, "page": page, "part_id": cur_part["id"] if cur_part else None})


# ---------------------------------------------------------------- 元信息

def split_names(chunk):
    """把连写的中文姓名串切成候选姓名（2-3 字）。结果为候选，须人工复核。"""
    c = chunk.replace(" ", "")
    if not (3 <= len(c) <= 18):
        return []
    if len(c) % 3 == 0 and len(c) >= 6:
        step = 3
    elif len(c) % 2 == 0:
        step = 2
    else:
        step = 2
    out = [c[i:i + step] for i in range(0, len(c), step)]
    return [x for x in out if x]


def header_metas(blocks):
    metas = []
    for b in blocks:
        head = b["body"][:160]
        d = DATE_RE.search(head)
        if not d:
            continue
        raw_head = b.get("body_raw", "")[:160]
        authors = []
        for tok in re.findall(r"[" + CJK + r"](?:\s?[" + CJK + r"]){1,17}", raw_head[:60]):
            if any(w in tok for w in ("我们", "本文", "公司", "有限", "律师", "事务")):
                continue
            authors.extend(split_names(tok))
        metas.append({
            "title": b["title"],
            "date_raw": d.group(0),
            "date_iso": "%s-%02d-%02d" % (d.group(1), int(d.group(2)), int(d.group(3))),
            "dateline_template": DATE_RE.sub("<DATE>", head[:48]).strip(),
            "authors_candidates": authors[:8],
            "authors_confidence": "guessed",
            "chars": b["chars"],
        })
    return metas


SUBHEAD_RE = re.compile(r"^([一二三四五六七八九十]+[、.]|\d+[、.]|（[一二三四五六七八九十\d]+）|背景|前言|引言|结语|小结|结语[:：])")
ARTICLE_MIN = 6


def _is_unit(b, contents_fp, metas_map, fallback_mode):
    fp = fingerprint(b["title"])
    for e in contents_fp:
        if fp == e or (len(fp) >= 8 and (fp in e or e in fp)):
            return True, "contents"
    # 章节型标题不作单元：单独的 dateline 不足以证明它是新文章
    if b["title"] in metas_map and len(b["title"]) >= ARTICLE_MIN \
            and not SUBHEAD_RE.match(b["title"]) and not b["title"].endswith("。"):
        return True, "dateline"
    if fallback_mode and b["level"] <= 2 and len(b["title"]) >= 8 and b["chars"] >= 600:
        return True, "heuristic"
    return False, None


def build_tree(blocks, contents, metas):
    metas_map = {}
    for m in metas:
        metas_map[m["title"]] = m
    contents_fp = []
    part_name = {}
    entry_fp = {}
    if contents:
        for p in contents["parts"]:
            part_name[p["id"]] = p["name"]
        for e in contents["entries"]:
            f = fingerprint(e["title"])
            if f:
                contents_fp.append(f)
                entry_fp[f] = e

    # 先按栏目顺序列出权威单元表（保持目录顺序，便于与印页对齐）
    ordered_parts = OrderedDict()
    if contents:
        for p in contents["parts"]:
            ordered_parts[p["id"]] = {"id": p["id"], "name": p["name"], "units": [],
                                      "toc_pages": [e["page"] for e in contents["entries"]
                                                    if e["part_id"] == p["id"] and e["page"]]}
    frame = {"front_matter": [], "back_matter": [], "parts": ordered_parts, "parts_seen": False}

    fallback_mode = not bool(contents_fp)
    assigned = {}
    for b in blocks:
        ok, how = _is_unit(b, contents_fp, metas_map, fallback_mode)
        if not ok:
            continue
        fp = fingerprint(b["title"])
        e = entry_fp.get(fp)
        # 找不到精确指纹时做一次包含匹配
        if e is None:
            for f, ent in entry_fp.items():
                if len(fp) >= 8 and (fp in f or f in fp):
                    e = ent
                    break
        pid = e["part_id"] if e else None
        assigned[b["line"]] = {"block": b, "part_id": pid, "toc_page": e["page"] if e else None,
                               "how": how}

    if not assigned:
        return {"front_matter": [b["title"] for b in blocks],
                "back_matter": [], "parts": {}, "tree_confidence": "low",
                "note": "既无可用目录也无日期题头，单元边界不可信，必须人工划定"}

    # 未命中的块按行号挂到最近的后续/前序 unit
    unit_lines = sorted(assigned.keys())
    for idx, b in enumerate(blocks):
        if b["line"] in assigned:
            continue
        prev = [x for x in unit_lines if x <= b["line"]]
        owner = assigned[prev[-1]] if prev else None
        target = owner["block"] if owner else None
        if target is None:
            frame["front_matter"].append(b)
            continue
        if OFFICE_RE.match(b["title"]) and "电话" in b["body"][:40]:
            frame["back_matter"].append(b)
            continue
        target.setdefault("subs", []).append(b)

    for ln in unit_lines:
        info = assigned[ln]
        b = info["block"]
        pid = info["part_id"]
        if pid is None:
            key = None
        else:
            key = pid
        if key is None:
            # 目录外单元：放进第一个栏目的兜底桶
            if not frame["parts"]:
                frame["parts"]["--"] = {"id": None, "name": "(未分栏)", "units": [], "toc_pages": []}
            key = list(frame["parts"].keys())[0]
        if key not in frame["parts"]:
            frame["parts"][key] = {"id": key, "name": part_name.get(key, "(未命名栏目)"),
                                   "units": [], "toc_pages": []}
        bucket = frame["parts"][key]
        subs = b.get("subs", [])
        total = b["chars"] + sum(x["chars"] for x in subs)
        # role：有分节且篇幅大 = article；无分节且以日期导语起 = entry
        role = "article" if len(subs) >= 3 or total >= 2500 else "entry"
        bucket["units"].append({
            "title": b["title"],
            "chars_own": b["chars"],
            "chars_total": total,
            "role": role,
            "toc_page": info["toc_page"],
            "matched_by": info["how"],
            "meta": metas_map.get(b["title"]),
            "subheads": [{"title": s["title"], "chars": s["chars"], "level": s["level"]}
                         for s in subs],
        })

    return {
        "front_matter": [{"title": x["title"], "chars": x["chars"]} for x in frame["front_matter"]],
        "back_matter": [{"title": x["title"], "chars": x["chars"]} for x in frame["back_matter"]],
        "parts": frame["parts"],
        "tree_confidence": "high" if not fallback_mode else "media",
    }


def stats(vals):
    vals = sorted(v for v in vals if v)
    if not vals:
        return None
    n = len(vals)

    def pct(p):
        return vals[min(n - 1, max(0, int(round((n - 1) * p))))]

    return {"n": n, "min": vals[0], "p25": pct(0.25), "median": pct(0.5), "p75": pct(0.75), "max": vals[-1]}


LEAD_DATE_RE = re.compile(r"^\s*(20\d{2})[年.\-/]\s?(\d{1,2})[月.\-/]\s?(\d{1,2})")
LEAD_TAG_RE = re.compile(r"^\s*([\u4e00-\u9fff]{2,8})[:：]")     # 「香港：」「澳门：」式地区前缀
LEAD_ORG_RE = re.compile(r"^\s*(20\d{2})[年.\-/]\s?(\d{1,2})[月.\-/]\s?(\d{1,2})[日]?[，,]\s?([\u4e00-\u9fff]{2,12})")


def paragraph_units(md):
    """识别「段落型单元」——不在目录、也不是 Markdown 标题，但成批重复出现的条目。

    律所期刊的法规动态几乎都是这种：每条既无独立页码也不进 markdown 标题树，
    只表现为「同一 leading pattern + 相近篇幅」反复出现。返回候选与切分正则。
    """
    paras = []
    for block in re.split(r"\n\s*\n+", md):
        t = norm_space(block).strip()
        if not t or HEAD_RE.match(t):
            continue
        core = re.sub(r"\s+", "", t)
        if not (80 <= len(core) <= 1200):
            continue
        paras.append((t, core))

    date_units, tag_units = [], []
    for t, core in paras:
        if LEAD_ORG_RE.match(t) or LEAD_DATE_RE.match(t):
            date_units.append(core)
            continue
        m = LEAD_TAG_RE.match(t)
        if m and 2 <= len(m.group(1)) <= 8:
            tag_units.append(core)

    def summarize(items, name, regex):
        if len(items) < 3:
            return None
        lens = sorted(len(x) for x in items)
        n = len(lens)

        def pct(p):
            return lens[min(n - 1, max(0, int(round((n - 1) * p))))]

        return {"kind": name, "count": len(items), "split_regex": regex,
                "chars": {"n": n, "min": lens[0], "p25": pct(0.25), "median": pct(0.5),
                          "p75": pct(0.75), "max": lens[-1]},
                "samples": [x[:90] for x in items[:3]]}

    out = []
    for cand in (summarize(date_units, "lead_date_entry", r"^20\d{2}年\d{1,2}月\d{1,2}日[,，]"),
                 summarize(tag_units, "lead_tag_entry", r"^[\u4e00-\u9fff]{2,8}[:：]")):
        if cand:
            out.append(cand)
    return out


def fixed_pieces(md, tree):
    lines = [norm_space(x).strip() for x in md.split("\n")]
    cta = Counter()
    for ln in lines:
        if not ln or HEAD_RE.match(ln):
            continue
        core = re.sub(r"\s+", "", ln)
        if 2 <= len(core) <= 12:
            cta[core] += 1
    running = [{"text": t, "count": n} for t, n in cta.most_common(30) if n >= 15]
    ctas = [{"text": t, "count": n} for t, n in cta.most_common(12) if 3 <= n < 15]

    disclaimer, seen = [], set()
    for ln in lines:
        core = re.sub(r"\s+", "", ln)
        if len(core) < 40:
            continue
        if re.search(r"不构成|不代表|仅供参考|不承担|不应被视为", core):
            if core[:24] in seen:
                continue
            seen.add(core[:24])
            disclaimer.append({"text": core[:300]})

    offices = [x["title"] for x in tree.get("back_matter", [])]
    return {"running_head_candidates": running, "cta_candidates": ctas,
            "disclaimer_candidates": disclaimer[:5], "contact_list": offices}


def terms(md):
    ns = norm_space(md)
    laws = Counter(LAW_RE.findall(ns))
    quoted = Counter()
    for q in QUOTE_RE.findall(ns):
        q = q.strip()
        if 3 <= len(q) <= 24 and not re.search(r"[。；]", q):
            quoted[q] += 1
    return {"statutes_top": [{"name": k, "n": v} for k, v in laws.most_common(30)],
            "terms_top": [{"name": k, "n": v} for k, v in quoted.most_common(20)]}


def draft_markdown(sem, metas):
    tree = sem["section_tree"]
    L = ["# UnitPattern 草稿（Omni 富文本自动生成，须人工复核）\n",
         "> 字数按去空白字符计；`匹配方式`= contents 表示目录命中，dateline 表示题头日期命中。\n",
         "\n## 一、栏目结构\n"]
    for pid, part in tree.get("parts", {}).items():
        L.append("- `%s` %s —— %d 个单元\n" % (part["id"] or "--", part["name"], len(part["units"])))
    if tree.get("front_matter"):
        L.append("- 前置件（封面/扉页/目录）：%d 块\n" % len(tree["front_matter"]))
    if tree.get("back_matter"):
        L.append("- 后置件（分所名录等固定件）：%s\n" % "、".join(x["title"] for x in tree["back_matter"]))
    L.append("\n## 二、单元度量（按栏目）\n")
    L.append("| 栏目 | 单元数 | 中位字数 | 字数区间 | 平均分节数 |\n|---|---|---|---|---|\n")
    for pid, part in tree.get("parts", {}).items():
        if not part["units"]:
            continue
        cs = [u["chars_total"] for u in part["units"] if u["chars_total"] > 0] or [0]
        sh = [len(u["subheads"]) for u in part["units"]]
        st = stats(cs)
        L.append("| %s | %d | %d | %d–%d | %.1f |\n" % (
            part["name"], st["n"], st["median"], st["min"], st["max"], sum(sh) / float(len(sh))))
    L.append("\n## 三、题头元信息（日期 + 作者）\n")
    L.append("> 作者由连写汉字串切分得到，一律视为候选，须人工核对。\n")
    for m in metas[:24]:
        L.append("- **%s** —— `%s` 作者：%s（%d 字）\n" % (
            m["title"], m["date_raw"], "、".join(m.get("authors_candidates", [])) or "未识别", m["chars"]))
    L.append("\n## 三点五、段落型单元（不进标题树的重复条目）\n")
    if not sem.get("paragraph_units"):
        L.append("- 未识别到成批重复段落（本刊可能全部单元都带标题）\n")
    for pu in sem.get("paragraph_units", []):
        c = pu["chars"]
        L.append("- **%s** × %d —— 字数 %d–%d（中位 %d）；切分 ` %s `\n" % (
            pu["kind"], pu["count"], c["min"], c["max"], c["median"], pu["split_regex"]))
        for x in pu["samples"]:
            L.append("    - %s…\n" % x)
    L.append("\n## 四、固定件候选\n")
    for c in sem["fixed_pieces"]["running_head_candidates"][:4]:
        L.append("- 页眉/页脚「%s」× %d（几乎每页重复）\n" % (c["text"], c["count"]))
    for c in sem["fixed_pieces"]["cta_candidates"][:8]:
        L.append("- CTA「%s」× %d\n" % (c["text"], c["count"]))
    for d in sem["fixed_pieces"]["disclaimer_candidates"]:
        L.append("- 免责声明：%s…\n" % d["text"][:80])
    if sem["fixed_pieces"]["contact_list"]:
        L.append("- 名录件：%s\n" % "、".join(sem["fixed_pieces"]["contact_list"]))
    L.append("\n## 五、术语/法规种子\n")
    for t in sem["terms"]["statutes_top"][:15]:
        L.append("- 《%s》× %d\n" % (t["name"], t["n"]))
    L.append("\n## 六、人工必须补齐\n")
    L.append("- [ ] 图与装饰件（富文本层丢失图片，一律以 `image_slots` 为准）\n")
    L.append("- [ ] UnitPattern 的「必有句式」是否真为硬要求（至少看 3 期是否稳定）\n")
    L.append("- [ ] 免责声明是全刊套用还是条件触发\n")
    L.append("- [ ] 目录页码 → 物理页 offset（用几何层的 `page_offset` 对齐）\n")
    return "".join(L)


def main():
    ap = argparse.ArgumentParser(description="Omni 富文本 -> StyleSpec 语义层")
    ap.add_argument("--md", required=True, help="Omni save_result 落盘的 Markdown")
    ap.add_argument("--outline", help="read_outline 的 JSON（可选）")
    ap.add_argument("--geo", help="extract_style.py 产出的 stylespec.json（可选）")
    ap.add_argument("--out", required=True, help="输出目录")
    a = ap.parse_args()

    md = read_text(a.md)
    blocks = blocks_from_md(md)
    metas = header_metas(blocks)
    contents = extract_contents(md)
    tree = build_tree(blocks, contents, metas)

    per_part = {}
    for pid, part in tree.get("parts", {}).items():
        cs = [u["chars_total"] for u in part["units"] if u["chars_total"] > 0]
        if cs:
            per_part[part["name"]] = stats(cs)

    sem = {
        "source": {"md": os.path.basename(a.md), "characters_raw": len(md)},
        "headings": len(blocks),
        "contents": contents,
        "section_tree": tree,
        "unit_metrics": {
            "all_units": stats([u["chars_total"] for p in tree.get("parts", {}).values()
                                for u in p["units"] if u["chars_total"] > 0]),
            "per_part": per_part,
        },
        "header_metas": metas,
        "fixed_pieces": fixed_pieces(md, tree),
        "paragraph_units": paragraph_units(md),
        "terms": terms(md),
        "capability_notes": {
            "has_images_in_text": bool(re.search(r"!\[", md)),
            "has_html_table": "<table" in md,
            "has_gfm_table": bool(re.search(r"^\|.*\|$", md, re.M)),
        },
    }
    if a.outline:
        # 上游返货坏了就停下，不产出一份看起来正常的草稿：这句 outline 只在语义层里做补强，
        # 缺它或不合式都该由取数方补回，而不是让下游拿一份没有大纲锚的成稿当正常件用。
        # 给了 --outline 却读不到＝取数错误，不退化成「当作没给」：后者照样产出两件同名产物，
        # 与 outline 在场时的产物形完全同，读者无从分辨少了一层语义。
        if not os.path.exists(a.outline):
            sys.stderr.write("enrich_from_omni: --outline 指向的文件不存在（%s），取数错误——不产出任何文件\n"
                             "      → 可选参数整个省掉才对；既然给了就得把那份 read_outline 落盘再重跑\n" % a.outline)
            sys.exit(1)
        try:
            oj = json.loads(read_text(a.outline))
        except json.JSONDecodeError as e:
            sys.stderr.write("enrich_from_omni: --outline 不是合法 JSON（%s），取数错误——不产出任何文件\n" % e.msg)
            sys.exit(1)
        if not isinstance(oj, dict):
            sys.stderr.write("enrich_from_omni: --outline 是 JSON %s，本件只收对象（形如 {\"nodes\": [], \"coverage\": ...}），"
                             "取数错误——不产出任何文件\n" % type(oj).__name__)
            sys.exit(1)
        sem["outline_nodes"] = oj.get("nodes", [])
        sem["outline_coverage"] = oj.get("coverage")

    if not os.path.isdir(a.out):
        os.makedirs(a.out)
    with io.open(os.path.join(a.out, "semantic.json"), "w", encoding="utf-8") as f:
        json.dump(sem, f, ensure_ascii=False, indent=1)
    with io.open(os.path.join(a.out, "unit-patterns.draft.md"), "w", encoding="utf-8") as f:
        f.write(draft_markdown(sem, metas))

    if a.geo and os.path.exists(a.geo):
        geo = json.loads(read_text(a.geo))
        geo["semantic"] = {k: sem[k] for k in
                           ("source", "headings", "contents", "section_tree", "unit_metrics",
                            "fixed_pieces", "paragraph_units", "terms", "capability_notes")}
        if sem.get("outline_nodes"):
            geo["semantic"]["outline_nodes"] = sem["outline_nodes"]
        with io.open(os.path.join(a.out, "stylespec.merged.json"), "w", encoding="utf-8") as f:
            json.dump(geo, f, ensure_ascii=False, indent=1)

    n = sum(len(p["units"]) for p in tree.get("parts", {}).values())
    print("written -> %s" % a.out)
    print("headings=%d units=%d parts=%d ctas=%d confidence=%s" % (
        len(blocks), n, len(tree.get("parts", {})),
        len(sem["fixed_pieces"]["cta_candidates"]), tree.get("tree_confidence")))


if __name__ == "__main__":
    main()
