#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
format_citations.py — formatted citations + BibTeX / RIS export.

Reads `.merged.json` and renders each work as a formatted citation under one of
five styles (apa / nature / vancouver / ieee / gb7714), then writes:
  - references.bib   (BibTeX, all works)
  - references.ris   (RIS, all works)
  - references_<style>.md  (human-readable citation list in the chosen style)

Pure local; reuses existing .merged.json schema fields (title / authors / year /
publication / volume / issue / page / doi / url). No fetch-layer change needed.

GB/T 7714 is the Chinese national standard: when style == 'gb7714' we branch to
Chinese punctuation / labelling so it does not get mangled when mixed with the
English styles in the same export run.
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

STYLES = ["apa", "nature", "vancouver", "ieee", "gb7714"]

# DOI can arrive in two shapes: OpenAlex stores the full resolver URL
# (https://doi.org/10.x/...), Europe PMC stores the bare DOI (10.x/...).
# Normalise to the canonical bare suffix so every consumer (text citation,
# BibTeX, RIS) builds at most ONE resolver prefix — never "https://doi.org/https://...".
_DOI_RE = re.compile(r"10\.\d{4,9}/[^\s]+")


def _bare_doi(doi):
    """Return the canonical bare DOI (10.x/...) regardless of input shape.

    Accepts a full URL (https://doi.org/10.x/...) or a bare DOI (10.x/...) and
    always returns the bare suffix; non-DOI / malformed input is returned as-is.
    """
    if not doi:
        return ""
    m = _DOI_RE.search(str(doi))
    return m.group(0) if m else str(doi).strip()


# ---- field helpers (tolerant of missing / mixed types) ----

def _authors_list(work):
    a = work.get("authors")
    if isinstance(a, list):
        return [str(x) for x in a if x]
    if isinstance(a, str):
        return [x.strip() for x in re.split(r"\s*,\s*|\s+and\s+", a) if x.strip()]
    return []


def _split_name(name):
    """Return (last, first) from a name string, CJK-aware."""
    name = (name or "").strip()
    if not name:
        return "", ""
    if "," in name:  # "Smith, John"
        last, first = name.split(",", 1)
        return last.strip(), first.strip()
    if re.search(r"[\u4e00-\u9fff]", name):  # Chinese name, keep as-is
        return name, ""
    parts = name.split()
    if len(parts) == 1:
        return parts[0], ""
    return parts[-1], " ".join(parts[:-1])


def _initials(first):
    first = (first or "").strip()
    if not first:
        return ""
    # keep CJK characters whole; take leading letter of each latin token
    out = []
    for tok in re.split(r"\s+", first):
        if re.search(r"[\u4e00-\u9fff]", tok):
            out.append(tok)
        else:
            out.append(tok[0].upper() + ".")
    return " ".join(out)


def _pages(work):
    p = work.get("page") or ""
    p = str(p).strip()
    return p.replace(" ", "")


# ---- per-style citation rendering ----

def _apa_authors(authors):
    names = [_split_name(n) for n in authors]
    parts = []
    for last, first in names:
        ini = _initials(first)
        parts.append(("%s, %s" % (last, ini)).strip(", "))
    if not parts:
        return ""
    if len(parts) == 1:
        return parts[0]
    return ", ".join(parts[:-1]) + ", & " + parts[-1]


def _nat_ieee_authors(authors):
    # "Smith J, Jones A" style (initials after surname, comma separated)
    out = []
    for n in authors:
        last, first = _split_name(n)
        ini = _initials(first).replace(" ", "")
        out.append(("%s %s" % (last, ini)).strip())
    return ", ".join(out)


def _van_authors(authors):
    return ", ".join(_nat_ieee_authors(authors).split(", "))


def _gb_authors(authors):
    # Chinese standard: surname + given name, no comma, "and" -> "，"
    out = []
    for n in authors:
        last, first = _split_name(n)
        out.append(("".join([last, first])).strip())
    return "，".join(out)


def _local_pdf_label(work):
    """Return the absolute local-PDF path string, or "" if none.

    文件实际落盘在本地（out_dir/pdfs 下），因此题录数据直接写**绝对路径**，
    便于用户复制到资源管理器 / 文献管理器直接定位，而不是只剩一个无上下文的文件名。
    （历史上曾写 os.path.basename，用户 2026-09-21 明确改为绝对路径。）
    """
    p = work.get("local_pdf_path") or ""
    if not p:
        return ""
    return os.path.normpath(os.path.abspath(str(p)))


def cite(work, style):
    authors = _authors_list(work)
    year = work.get("year") or "n.d."
    title = (work.get("title") or "").strip()
    journal = work.get("publication") or ""
    vol = work.get("volume") or ""
    iss = work.get("issue") or ""
    pages = _pages(work)
    doi = work.get("doi") or ""
    bare_doi = _bare_doi(doi)
    url = work.get("url") or (("https://doi.org/" + bare_doi) if bare_doi else "")
    pdf_fn = _local_pdf_label(work)

    if style == "apa":
        a = _apa_authors(authors)
        s = "%s (%s). %s. " % (a + "." if a else "", year, title)
        if journal:
            s += "*%s*" % journal
            if vol:
                s += ", %s" % vol
                if iss:
                    s += "(%s)" % iss
            if pages:
                s += ", %s" % pages
            s += "."
        if doi:
            s += " https://doi.org/%s" % bare_doi
        if pdf_fn:
            s += " [本地PDF: %s]" % pdf_fn
        return s.strip()

    if style == "nature":
        a = _nat_ieee_authors(authors)
        s = "%s. %s. " % (a, title) if a else "%s. " % title
        if journal:
            s += "%s " % journal
            if vol:
                s += "%s, " % vol
            if pages:
                s += "%s" % pages
            s += " (%s)." % year
        elif year:
            s += "(%s)." % year
        if doi:
            s += " https://doi.org/%s" % bare_doi
        if pdf_fn:
            s += " [本地PDF: %s]" % pdf_fn
        return s.strip()

    if style == "vancouver":
        a = _van_authors(authors)
        s = "%s. %s. " % (a, title) if a else "%s. " % title
        if journal:
            s += "%s. " % journal
            s += "%s" % year
            if vol:
                s += ";%s" % vol
                if iss:
                    s += "(%s)" % iss
            if pages:
                s += ":%s" % pages
            s += "."
        if doi:
            s += " doi:%s" % bare_doi
        if pdf_fn:
            s += " [本地PDF: %s]" % pdf_fn
        return s.strip()

    if style == "ieee":
        a = _nat_ieee_authors(authors)
        s = "%s, " % a if a else ""
        s += '"%s," ' % title
        if journal:
            s += "%s" % journal
            if vol:
                s += ", vol. %s" % vol
            if iss:
                s += ", no. %s" % iss
            if pages:
                s += ", pp. %s" % pages
            s += ", %s." % year
        elif year:
            s += "%s." % year
        if doi:
            s += " doi: %s." % bare_doi
        if pdf_fn:
            s += " [本地PDF: %s]" % pdf_fn
        return s.strip()

    if style == "gb7714":
        a = _gb_authors(authors)
        s = "%s. " % a if a else ""
        s += "%s[J]. " % title
        if journal:
            s += "%s, " % journal
            s += "%s" % year
            if vol:
                s += ", %s" % vol
                if iss:
                    s += "(%s)" % iss
            if pages:
                s += ":%s" % pages
            s += "."
        if doi:
            s += " DOI:%s." % bare_doi
        if pdf_fn:
            s += " [本地PDF: %s]" % pdf_fn
        return s.strip()

    # fallback to apa
    return cite(work, "apa")


# ---- BibTeX / RIS ----

def _bibtex_key(work, i):
    authors = _authors_list(work)
    if authors:
        last, _ = _split_name(authors[0])
        key_author = re.sub(r"[^a-zA-Z]", "", last) or "anon"
    else:
        key_author = "anon"
    year = work.get("year") or "nd"
    tw = _norm_first(word=(work.get("title") or "untitled"))
    return "%s%s%s" % (key_author, year, tw)


def _norm_first(word):
    word = re.sub(r"[^a-zA-Z]", "", str(word))
    return word.lower()[:8] or "work"


def to_bibtex(works):
    blocks = []
    seen = {}
    for i, w in enumerate(works):
        key = _bibtex_key(w, i)
        seen[key] = seen.get(key, 0) + 1
        if seen[key] > 1:
            key = "%s%d" % (key, seen[key])
        lines = ["@article{%s," % key]
        authors = _authors_list(w)
        if authors:
            lines.append("  author = {%s}," % " and ".join(authors))
        if w.get("title"):
            lines.append("  title = {%s}," % w["title"])
        if w.get("publication"):
            lines.append("  journal = {%s}," % w["publication"])
        if w.get("year"):
            lines.append("  year = {%s}," % w["year"])
        if w.get("volume"):
            lines.append("  volume = {%s}," % w["volume"])
        if w.get("issue"):
            lines.append("  number = {%s}," % w["issue"])
        if _pages(w):
            lines.append("  pages = {%s}," % _pages(w))
        if w.get("doi"):
            lines.append("  doi = {%s}," % _bare_doi(w["doi"]))
        if w.get("url"):
            lines.append("  url = {%s}," % w["url"])
        pdf_fn = _local_pdf_label(w)
        if pdf_fn:
            lines.append("  note = {本地PDF: %s}," % pdf_fn)
        lines.append("}")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks) + ("\n" if blocks else "")


def to_ris(works):
    blocks = []
    for w in works:
        lines = ["TY  - JOUR"]
        for a in _authors_list(w):
            lines.append("AU  - %s" % a)
        if w.get("title"):
            lines.append("TI  - %s" % w["title"])
        if w.get("publication"):
            lines.append("JO  - %s" % w["publication"])
        if w.get("year"):
            lines.append("PY  - %s" % w["year"])
        if w.get("volume"):
            lines.append("VL  - %s" % w["volume"])
        if w.get("issue"):
            lines.append("IS  - %s" % w["issue"])
        pg = _pages(w)
        if pg:
            if "-" in pg:
                sp, ep = pg.split("-", 1)
                lines.append("SP  - %s" % sp)
                lines.append("EP  - %s" % ep)
            else:
                lines.append("SP  - %s" % pg)
        if w.get("doi"):
            lines.append("DO  - %s" % _bare_doi(w["doi"]))
        if w.get("url"):
            lines.append("UR  - %s" % w["url"])
        pdf_fn = _local_pdf_label(w)
        if pdf_fn:
            lines.append("L1  - %s" % pdf_fn)
        lines.append("ER  - ")
        blocks.append("\n".join(lines))
    return "\n".join(blocks) + ("\n" if blocks else "")


def export_citations(merged, style="apa", out_dir=".", lang="auto"):
    """Write references.bib, references.ris, and a style citation .md.

    Returns a dict {bib, ris, md, citations:[...]} for pipeline integration.
    """
    works = [w for w in (merged.get("works") or []) if isinstance(w, dict)]
    citations = [cite(w, style) for w in works]
    bib = to_bibtex(works)
    ris = to_ris(works)

    os.makedirs(out_dir, exist_ok=True)
    bib_path = os.path.join(out_dir, "references.bib")
    ris_path = os.path.join(out_dir, "references.ris")
    md_path = os.path.join(out_dir, "references_%s.md" % style)

    with open(bib_path, "w", encoding="utf-8") as f:
        f.write(bib)
    with open(ris_path, "w", encoding="utf-8") as f:
        f.write(ris)

    md_lines = []
    md_lines.append("# References / 参考文献 (%s 样式)\n" % style)
    md_lines.append("> 引文样式 / Citation style: **%s**\n" % style)
    for i, c in enumerate(citations, 1):
        md_lines.append("%d. %s" % (i, c))
    md_text = "\n".join(md_lines) + "\n"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_text)

    return {"bib": bib, "ris": ris, "md": md_text, "citations": citations,
            "bib_path": bib_path, "ris_path": ris_path, "md_path": md_path}


def main():
    ap = argparse.ArgumentParser(description="Format citations + export BibTeX/RIS.")
    ap.add_argument("--in", default=".merged.json", dest="inp", help=".merged.json path")
    ap.add_argument("--out-dir", default=".", help="output directory")
    ap.add_argument("--citation-style", default="apa", choices=STYLES,
                    help="citation style (default: apa)")
    ap.add_argument("--export-bib", action="store_true", default=True,
                    help="write references.bib + references.ris (default: on)")
    ap.add_argument("--lang", default="auto", choices=["auto", "zh", "en"])
    args = ap.parse_args()

    data = json.load(open(args.inp, encoding="utf-8"))
    res = export_citations(data, style=args.citation_style, out_dir=args.out_dir,
                           lang=args.lang)
    print("[OK] style=%s citations=%d" % (args.citation_style, len(res["citations"])))
    print("     bib -> %s" % res["bib_path"])
    print("     ris -> %s" % res["ris_path"])
    print("     md  -> %s" % res["md_path"])
    # preview first citation
    if res["citations"]:
        print("     e.g. %s" % res["citations"][0][:160])


if __name__ == "__main__":
    main()
