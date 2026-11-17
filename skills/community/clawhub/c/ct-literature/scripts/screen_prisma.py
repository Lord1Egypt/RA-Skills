#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
screen_prisma.py — deterministic PRISMA title/abstract screening (no LLM).

Adds a rule-based screening layer *after* the U4 merge/dedupe stage. It reuses
the existing safety lexicon (SAFETY_LEXICON, originally defined in
fetch_openalex.py; imported here so the rule stays in sync — falls back to a
local copy if that module is unavailable) and the review_type signal. No LLM is
invoked; the screen is a machine first-pass only.

It writes a `prisma` block into .merged.json and annotates each work with
`prisma_stage` / `prisma_included` / `prisma_reason`.

PRISMA-2020 funnel produced:
  1. identified_records  — total works retrieved & de-duplicated
  2. screened_records    — title/abstract screened (here = all identified)
  3. excluded_records    — excluded at title/abstract by rule, with reasons
  4. included_records    — passed the screen
  5. duplicates_removed  — (NEW) records collapsed by upstream cross-source
                            de-duplication; surfaced so the downstream PRISMA
                            funnel can fill "duplicates removed (n=…)".
                            `None` when the merge step did not report it.

IMPORTANT: this is a *machine* screen. The report must declare
「机器初筛，非人工终审 / Machine screen — not a substitute for human final review」.
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Doc-type screening (ported from meta-analysis pdf_extractor empirical rules):
# used when the user asks for original research only — excludes
# review / guideline / protocol records at title/abstract level.
try:
    from doc_type_filter import classify_record
    _NON_ORIGINAL_TYPES = ("review", "guideline", "protocol")
    _VALID_TYPES = ("original", "review", "guideline", "protocol")
except Exception:  # pragma: no cover - keep screen working without the module
    classify_record = None
    _NON_ORIGINAL_TYPES = ()
    _VALID_TYPES = ()

# Reuse the existing safety lexicon (single source of truth).
try:
    from fetch_openalex import SAFETY_LEXICON  # type: ignore
except Exception:  # pragma: no cover - offline fallback
    # Mirrors fetch_openalex.SAFETY_LEXICON (English AE/PV term list).
    SAFETY_LEXICON = [
        "adverse event", "adverse reaction", "side effect", "safety", "toxicity",
        "toxic", "case report", "pharmacovigilance", "drug-induced", "drug reaction",
    ]

# Review-type -> expected study_type token (matches normalization logic).
_REVIEW_TYPE_STUDY = {
    "systematic-review": "systematic-review",
    "meta-analysis": "meta-analysis",
    "scoping-review": "scoping-review",
    "rct": "rct",
    "case-report": "case-report",
}


def _norm(s):
    if not s:
        return ""
    s = str(s).lower()
    s = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", s)
    return " ".join(s.split())


def _topic_tokens(topic):
    toks = [t for t in _norm(topic).split() if len(t) >= 3]
    return toks


def _is_safety(work):
    blob = _norm(" ".join([work.get("title") or "", work.get("abstract_snippet") or ""]))
    return any(k in blob for k in SAFETY_LEXICON)


def _passes_screen(work, topic_tokens, review_type, safety,
                   exclude_non_original=False, require_types=None):
    """Return (included:bool, reason:str|None)."""
    title = work.get("title") or ""
    abstract = work.get("abstract_snippet") or ""
    if not title and not abstract:
        return False, "no-title-abstract"

    # Doc-type gate (classify_record, ported empirical rules):
    #  - exclude_non_original: user wants original research only
    #    (excludes review/guideline/protocol; unknown passes).
    #  - require_types: inverse mode, user wants ONLY the listed types
    #    (unknown is excluded — when a type is explicitly requested,
    #     signal-less records must not slip in).
    if classify_record is not None and (exclude_non_original or require_types):
        cls = classify_record(title, abstract, work.get("pub_types"))
        if require_types:
            if cls["type"] not in require_types:
                return False, "type-not-required:%s" % cls["type"]
        elif cls["type"] in _NON_ORIGINAL_TYPES:
            return False, "non-original-type:%s" % cls["type"]

    blob = _norm(" ".join([title, abstract]))

    # Safety mode: any safety lexicon hit earns inclusion.
    if safety and _is_safety(work):
        return True, None

    # Topic relevance: at least one topic token (len>=3) appears.
    if topic_tokens:
        if any(t in blob for t in topic_tokens):
            # also honour explicit review_type match if requested
            if review_type not in (None, "all", ""):
                st = work.get("study_type") or work.get("type") or ""
                if st == _REVIEW_TYPE_STUDY.get(review_type):
                    return True, "topic+review_type"
                return True, "topic"
            return True, "topic"
        # topic given but no token matched -> exclude (low topical relevance)
        return False, "no-topic-match"

    # No topic filter: rely on review_type match if requested, else include.
    if review_type not in (None, "all", ""):
        st = work.get("study_type") or work.get("type") or ""
        if st == _REVIEW_TYPE_STUDY.get(review_type):
            return True, "review_type"
        return False, "review_type-mismatch"

    return True, None


def screen(works, topic="", review_type="all", safety=False,
            duplicates_removed=None, exclude_non_original=False,
            require_types=None):
    """Return {'works': annotated, 'prisma': {...}}.

    Incremental-compatible: original fields preserved; only prisma_* keys added.

    `duplicates_removed` (int|None): number of records collapsed by the upstream
    cross-source de-duplication (normalize.merge). Recorded in the prisma block so
    the downstream PRISMA-2020 funnel can fill its "duplicates removed (n=…)" box.
    """
    topic_tokens = _topic_tokens(topic)
    annotated = []
    reasons = {}
    included = 0
    for w in works:
        if not isinstance(w, dict):
            annotated.append(w)
            continue
        w = dict(w)
        ok, reason = _passes_screen(w, topic_tokens, review_type, safety,
                                    exclude_non_original=exclude_non_original,
                                    require_types=require_types)
        if ok:
            included += 1
            w["prisma_stage"] = "included"
            w["prisma_included"] = True
            w["prisma_reason"] = None
        else:
            w["prisma_stage"] = "excluded_tascreen"
            w["prisma_included"] = False
            w["prisma_reason"] = reason
            reasons[reason] = reasons.get(reason, 0) + 1
        annotated.append(w)

    identified = len(annotated)
    excluded = identified - included
    prisma = {
        "schema": "PRISMA-2020 (machine title/abstract screen, rule-based)",
        "duplicates_removed": duplicates_removed,
        "stages": [
            {"stage": "identified_records",
             "label": "Records identified (retrieved & de-duplicated)",
             "count": identified},
            {"stage": "screened_records",
             "label": "Records screened (title/abstract)",
             "count": identified},
            {"stage": "excluded_records",
             "label": "Records excluded (title/abstract, rule-based)",
             "count": excluded, "reasons": reasons},
            {"stage": "included_records",
             "label": "Records included (after screen)",
             "count": included},
        ],
        "note": ("机器初筛，非人工终审 / Machine screen — not a substitute for "
                 "human final review. Rules may miss relevant or wrongly exclude "
                 "records; verify before any formal synthesis."),
    }
    return {"works": annotated, "prisma": prisma}


def main():
    ap = argparse.ArgumentParser(description="PRISMA rule-based title/abstract screen.")
    ap.add_argument("--in", default=".merged.json", dest="inp", help=".merged.json path")
    ap.add_argument("--out", help="output .merged.json (default: overwrite --in)")
    ap.add_argument("--topic", default="", help="topic query (used for relevance rule)")
    ap.add_argument("--review-type", default="all")
    ap.add_argument("--safety", action="store_true", help="safety / CSM bias mode")
    ap.add_argument("--exclude-non-original", action="store_true",
                    help="只要原创研究：排除 review/guideline/protocol（unknown 放行）")
    ap.add_argument("--only-type", dest="only_type", default=None,
                    metavar="TYPES",
                    help="只保留指定类型（反向模式），逗号分隔："
                         "original/review/guideline/protocol，例：--only-type review")
    args = ap.parse_args()

    require_types = None
    if args.only_type:
        require_types = tuple(t.strip().lower() for t in args.only_type.split(",") if t.strip())
        bad = [t for t in require_types if t not in _VALID_TYPES]
        if bad:
            ap.error("unknown type(s): %s (valid: %s)" % (bad, ", ".join(_VALID_TYPES)))

    data = json.load(open(args.inp, encoding="utf-8"))
    works = data.get("works", [])
    res = screen(works, topic=args.topic, review_type=args.review_type,
                 safety=args.safety, exclude_non_original=args.exclude_non_original,
                 require_types=require_types)

    data = dict(data)
    data["works"] = res["works"]
    data["prisma"] = res["prisma"]
    if "count" in data:
        data["count"] = len(res["works"])

    out_path = args.out or args.inp
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    p = res["prisma"]
    print("[OK] PRISMA screen -> %s" % out_path)
    for s in p["stages"]:
        extra = ("  reasons=%s" % s["reasons"]) if s.get("reasons") else ""
        print("     %-22s %d%s" % (s["stage"], s["count"], extra))


if __name__ == "__main__":
    main()
