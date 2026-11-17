#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
obsidian_exporter.py — Obsidian / 文献管理软件集成（升级项 F）.

将 .merged.json 的每篇文献导出为 Obsidian 兼容的 Markdown 笔记：
  - 每篇文献一个独立 .md 文件，文件名即笔记名（去除文件系统非法字符）
  - 笔记内使用 Obsidian 内部链接语法 [[笔记名|作者 年份]] 互相引用
  - 自动生成一份 MOC（Map of Content）索引笔记，汇总全部文献
  - 基于共享 mesh / concepts / keywords 自动建立「相关文献」交叉链接，
    形成可图谱化的文献网络

纯本地、零联网、仅依赖标准库。可被 ct_literature.py 流水线直接调用，
也可作为独立 CLI 运行：

  python obsidian_exporter.py --in .merged.json --out-dir ./out [--no-related]

输出目录：<out-dir>/obsidian/
  ├── <论文标题>.md        每篇文献一篇
  └── Literature MOC.md    索引笔记（双击即可在 Obsidian 打开全部文献）
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

_ILLEGAL = re.compile(r'[\\/:*?"<>|#^\[\]]')


def _authors_list(work):
    a = work.get("authors")
    if isinstance(a, list):
        return [str(x) for x in a if x]
    if isinstance(a, str):
        return [x.strip() for x in re.split(r"\s*,\s*|\s+and\s+", a) if x.strip()]
    return []


def _split_name(name):
    name = (name or "").strip()
    if not name:
        return "", ""
    if "," in name:
        last, first = name.split(",", 1)
        return last.strip(), first.strip()
    if re.search(r"[\u4e00-\u9fff]", name):
        return name, ""
    parts = name.split()
    if len(parts) == 1:
        return parts[0], ""
    return parts[-1], " ".join(parts[:-1])


def _slug(text, max_len=60):
    """Filesystem / Obsidian-safe note name stem."""
    if not text:
        return "untitled"
    s = _ILLEGAL.sub(" ", str(text)).strip()
    s = re.sub(r"\s+", " ", s)
    if len(s) > max_len:
        s = s[:max_len].rstrip()
    return s or "untitled"


def _first_author_last(work):
    al = _authors_list(work)
    if not al:
        return "anon"
    last, _ = _split_name(al[0])
    return last or "anon"


def _display(work):
    """[[target|display]] 中的 display = '作者 年份'."""
    last = _first_author_last(work)
    year = work.get("year") or "nd"
    return "%s %s" % (last, year)


def _link_target(work, used):
    """Unique Obsidian note name = sanitized title (+year+idx on collision)."""
    base = _slug(work.get("title") or "untitled")
    cand = base
    if cand in used:
        cand = "%s %s" % (base, work.get("year") or "nd")
    i = 2
    while cand in used:
        cand = "%s %s %d" % (base, work.get("year") or "nd", i)
        i += 1
    used.add(cand)
    return cand


def _term_set(work):
    """Concepts / mesh / keywords 归一化集合，用于相关文献判断。"""
    terms = []
    for fld in ("concepts", "mesh", "keywords"):
        v = work.get(fld)
        if isinstance(v, list):
            terms.extend(str(x).lower().strip() for x in v if x)
        elif isinstance(v, str) and v:
            terms.append(v.lower().strip())
    return set(t.strip() for t in terms if t.strip())


def _frontmatter(work, lang):
    """YAML frontmatter with metadata + tags for Obsidian graph/tag pane."""
    tags = []
    for fld in ("mesh", "concepts", "keywords"):
        v = work.get(fld)
        if isinstance(v, list):
            for t in v[:8]:
                s = str(t).strip()
                if s:
                    tags.append("lit/" + _slug(s).replace(" ", "-").lower())
    lines = ["---"]
    if work.get("title"):
        lines.append("title: \"%s\"" % work["title"].replace('"', "'"))
    lines.append("authors: [%s]" % ", ".join(
        "\"%s\"" % a.replace('"', "'") for a in _authors_list(work)))
    if work.get("year"):
        lines.append("date: \"%s\"" % work["year"])
    if work.get("publication"):
        lines.append("journal: \"%s\"" % work["publication"].replace('"', "'"))
    if work.get("doi"):
        lines.append("doi: \"%s\"" % work["doi"])
    if work.get("url"):
        lines.append("url: \"%s\"" % work["url"])
    if work.get("pmid"):
        lines.append("pmid: \"%s\"" % work["pmid"])
    if work.get("pmcid"):
        lines.append("pmcid: \"%s\"" % work["pmcid"])
    if work.get("type"):
        lines.append("type: \"%s\"" % work["type"])
    if work.get("cited_by_count") is not None:
        lines.append("cited_by_count: %s" % work["cited_by_count"])
    if tags:
        lines.append("tags: [%s]" % ", ".join(tags))
    lines.append("---")
    return "\n".join(lines)


def _body(work, lang):
    L = {
        "zh": {"abs": "摘要", "src": "来源", "rel": "相关文献", "moc": "索引"},
        "en": {"abs": "Abstract", "src": "Sources", "rel": "Related", "moc": "Index"},
    }.get(lang, {"abs": "摘要", "src": "来源", "rel": "相关文献", "moc": "索引"})
    al = _authors_list(work)
    cite_authors = ", ".join(al) if al else "Unknown"
    lines = []
    lines.append("# %s" % (work.get("title") or "Untitled"))
    lines.append("")
    lines.append("> %s (%s). *%s*. %s." % (
        cite_authors, work.get("year") or "n.d.",
        work.get("publication") or "", work.get("doi") or ""))
    lines.append("")
    if work.get("abstract_snippet"):
        lines.append("## %s" % L["abs"])
        lines.append("")
        lines.append(work["abstract_snippet"].strip())
        lines.append("")
    lines.append("## %s" % L["src"])
    lines.append("")
    links = []
    if work.get("url"):
        links.append("- URL: %s" % work["url"])
    if work.get("open_access_url"):
        links.append("- Open Access: %s" % work["open_access_url"])
    if work.get("pmid"):
        links.append("- PubMed: https://pubmed.ncbi.nlm.nih.gov/%s/" % work["pmid"])
    if work.get("pmcid"):
        links.append("- PMC: https://www.ncbi.nlm.nih.gov/pmc/articles/%s/" % work["pmcid"])
    if work.get("doi"):
        links.append("- DOI: https://doi.org/%s" % work["doi"])
    if not links:
        links.append("- (no external links available)")
    lines.append("\n".join(links))
    lines.append("")
    return "\n".join(lines)


def export_obsidian(merged, out_dir=".", vault_rel="obsidian", build_related=True,
                    lang="auto"):
    """Write Obsidian notes for every work in `merged`.

    Returns dict {folder, notes:[...], moc, count}.
    """
    if lang == "auto":
        lang = "zh"
    works = [w for w in (merged.get("works") or []) if isinstance(w, dict)
             and w.get("title")]
    folder = os.path.join(out_dir, vault_rel)
    os.makedirs(folder, exist_ok=True)

    # assign unique note names
    used = set()
    targets = {}
    for w in works:
        targets[id(w)] = _link_target(w, used)

    # compute related links (shared terms)
    related_map = {}
    if build_related and len(works) > 1:
        term_index = {}  # term -> list of work indices
        for idx, w in enumerate(works):
            for t in _term_set(w):
                term_index.setdefault(t, []).append(idx)
        for idx, w in enumerate(works):
            rel = []
            seen = set()
            my_terms = _term_set(w)
            for t in my_terms:
                for j in term_index.get(t, []):
                    if j == idx or j in seen:
                        continue
                    seen.add(j)
                    rel.append(j)
            related_map[idx] = rel[:10]

    notes = []
    for idx, w in enumerate(works):
        target = targets[id(w)]
        note_path = os.path.join(folder, target + ".md")
        parts = [_frontmatter(w, lang), "", _body(w, lang)]
        # MOC backlink
        parts.append("## 📇 %s" % ("Literature MOC" if lang != "en" else "MOC"))
        parts.append("")
        parts.append("- [[Literature MOC]]")
        parts.append("")
        # related
        if build_related and idx in related_map and related_map[idx]:
            parts.append("## %s" % (
                "相关文献" if lang != "en" else "Related"))
            parts.append("")
            for j in related_map[idx]:
                oth = works[j]
                oth_target = targets[id(oth)]
                parts.append("- [[%s|%s]]" % (oth_target, _display(oth)))
            parts.append("")
        text = "\n".join(parts)
        with open(note_path, "w", encoding="utf-8") as f:
            f.write(text)
        notes.append(note_path)

    # MOC index note
    moc_lines = ["---", "tags: [lit/moc]", "---", "",
                 "# Literature MOC", "",
                 "> ct-literature 检索结果索引（共 %d 篇）。在 Obsidian 中打开本笔记即可跳转全部文献。" % len(works), ""]
    if lang != "en":
        moc_lines.append("## 全部文献")
    else:
        moc_lines.append("## All literature")
    moc_lines.append("")
    for w in works:
        target = targets[id(w)]
        moc_lines.append("- [[%s|%s]] — %s" % (target, _display(w),
                                                (w.get("title") or "")[:80]))
    moc_lines.append("")
    moc_path = os.path.join(folder, "Literature MOC.md")
    with open(moc_path, "w", encoding="utf-8") as f:
        f.write("\n".join(moc_lines))

    return {"folder": folder, "notes": notes, "moc": moc_path, "count": len(works)}


def main():
    ap = argparse.ArgumentParser(description="Export .merged.json to Obsidian notes.")
    ap.add_argument("--in", default=".merged.json", dest="inp", help=".merged.json path")
    ap.add_argument("--out-dir", default=".", help="output base directory")
    ap.add_argument("--vault-rel", default="obsidian",
                    help="sub-folder for notes (default: obsidian)")
    ap.add_argument("--no-related", action="store_true",
                    help="disable cross-reference / related-notes linking")
    ap.add_argument("--lang", default="zh", choices=["zh", "en", "auto"])
    args = ap.parse_args()
    data = json.load(open(args.inp, encoding="utf-8"))
    res = export_obsidian(data, out_dir=args.out_dir, vault_rel=args.vault_rel,
                          build_related=not args.no_related, lang=args.lang)
    print("[OK] obsidian notes=%d -> %s" % (res["count"], res["folder"]))
    print("     moc -> %s" % res["moc"])


if __name__ == "__main__":
    main()
