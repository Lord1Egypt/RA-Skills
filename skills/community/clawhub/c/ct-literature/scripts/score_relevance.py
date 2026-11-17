#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
score_relevance.py — deterministic topical relevance scoring (0-1).

Computes a weighted relevance score for each merged work against a query
(topic + optional keywords). Title weighted 0.6, abstract 0.4. Uses rapidfuzz
if installed (faster / better fuzzy matching), otherwise falls back to the
stdlib `difflib` / a token-set overlap ratio. Pure local, no network.

Outputs: annotate each work with `relevance_score` (float 0-1) and a short
`relevance_basis` note. The merged evidence base is NOT mutated in place
unless you call `score_works` (which returns a new annotated list).

Known limitation: non-English (e.g. Chinese) abstracts have weaker fuzzy
scoring because tokenisation is romanisation-light; the score is therefore a
coarse machine signal, not a substitute for human judgement.
"""
import argparse
import json
import locale
import os
import re
import sys

# rapidfuzz is optional; difflib / token-overlap is the stdlib fallback.
try:
    from rapidfuzz import fuzz  # type: ignore
    _HAS_RAPIDFUZZ = True
except Exception:  # pragma: no cover - optional dependency
    from difflib import SequenceMatcher
    _HAS_RAPIDFUZZ = False

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _zc_locale():
    try:
        return (locale.getdefaultlocale()[0] or "zh").lower().startswith("zh")
    except Exception:
        return False


def _norm(s):
    if not s:
        return ""
    s = str(s).lower()
    # keep CJK + alnum; collapse separators
    s = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", s)
    return " ".join(s.split())


def _tokens(s):
    return _norm(s).split()


def _char_ratio(a, b):
    if _HAS_RAPIDFUZZ:
        return fuzz.ratio(a, b) / 100.0
    return SequenceMatcher(None, a, b).ratio()


def token_set_ratio(a, b):
    """Token-set similarity in [0,1]. rapidfuzz preferred; stdlib fallback."""
    if _HAS_RAPIDFUZZ:
        return fuzz.token_set_ratio(a, b) / 100.0
    ta = set(_tokens(a))
    tb = set(_tokens(b))
    if not ta or not tb:
        return 0.0
    inter = ta & tb
    if not inter:
        # no shared tokens -> fall back to character-level ratio (rarely high)
        return min(0.3, _char_ratio(a, b))
    # overlap scaled by the smaller set's size
    return min(1.0, len(inter) / min(len(ta), len(tb)))


def _build_query(topic, keywords):
    parts = []
    if topic:
        parts.append(_norm(topic))
    if keywords:
        # accept comma- or whitespace-separated keyword lists
        for kw in re.split(r"[,;]+", str(keywords)):
            kw = _norm(kw)
            if kw:
                parts.append(kw)
    return " ".join(parts).strip()


def score_work(work, query):
    """Return (score_0_1, basis_str)."""
    title = _norm(work.get("title") or "")
    abstract = _norm((work.get("abstract_snippet") or "")[:2000])
    if not query:
        # no query -> neutral 0.5 so ordering is stable but not misleading
        return 0.5, "no-query(neutral)"
    if not title and not abstract:
        return 0.0, "no-title-abstract"
    title_score = token_set_ratio(query, title) if title else 0.0
    abs_score = token_set_ratio(query, abstract) if abstract else 0.0
    score = 0.6 * title_score + 0.4 * abs_score
    basis = "title=%.2f,abs=%.2f" % (title_score, abs_score)
    return round(min(1.0, max(0.0, score)), 3), basis


def score_works(works, topic=None, keywords=None):
    """Return a new list of works annotated with relevance_score / relevance_basis.

    Incremental-compatible: original fields are preserved, only new keys added.
    """
    query = _build_query(topic, keywords)
    out = []
    for w in works:
        if not isinstance(w, dict):
            out.append(w)
            continue
        w = dict(w)
        sc, basis = score_work(w, query)
        w["relevance_score"] = sc
        w["relevance_basis"] = basis
        out.append(w)
    return out


def main():
    ap = argparse.ArgumentParser(
        description="Annotate .merged.json works with a 0-1 relevance_score.")
    ap.add_argument("--in", default=".merged.json", dest="inp", help=".merged.json path")
    ap.add_argument("--out", help="output .merged.json (default: overwrite --in)")
    ap.add_argument("--topic", default="", help="topic / drug / disease query")
    ap.add_argument("--keywords", default="", help="comma-separated extra keywords")
    ap.add_argument("--lang", default="auto", choices=["auto", "zh", "en"])
    args = ap.parse_args()

    data = json.load(open(args.inp, encoding="utf-8"))
    works = data.get("works", [])
    annotated = score_works(works, topic=args.topic, keywords=args.keywords)

    data = dict(data)
    data["works"] = annotated
    if "count" in data:
        data["count"] = len(annotated)

    out_path = args.out or args.inp
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("[OK] relevance scored %d works (query=%r) -> %s"
          % (len(annotated), args.topic or args.keywords, out_path))
    if _zc_locale() or args.lang == "zh":
        print("[提示] 非英文（如中文）摘要模糊打分偏弱，relevance_score 仅为机器粗筛信号，"
              "不替代人工判断。/ Non-English abstracts score weakly; relevance is a coarse "
              "machine signal, not a substitute for human review.")


if __name__ == "__main__":
    main()
