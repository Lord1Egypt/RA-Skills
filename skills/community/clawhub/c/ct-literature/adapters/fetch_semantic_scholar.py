#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fetch_semantic_scholar.py — Semantic Scholar fetcher (optional citation-enhancement source).

Reads the Semantic Scholar Graph API (https://api.semanticscholar.org/graph/v1/paper/search)
for citation-aware relevance ranking. OPTIONAL API KEY via SEMANTIC_SCHOLAR_API_KEY (.env): the
keyed pool lifts the harsh ~1 req/s keyless limit and avoids most 429s.
LOW-PRIORITY supplementary source: the S2 key requires a manual form review (not auto-issued,
waits after applying), so it is usually absent short-term. When no key is configured the
source is SKIPPED entirely (no network request) rather than attempting-and-degrading.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from adapters import http_utils  # shared GET+retry (exponential backoff, 429 Retry-After)

BASE = "https://api.semanticscholar.org/graph/v1/paper/search"

SAFETY_LEXICON = [
    "adverse event", "adverse reaction", "side effect", "safety", "toxicity",
    "toxic", "case report", "pharmacovigilance", "drug-induced", "drug reaction",
]


def _study_type_from(title, abstract):
    blob = ((title or "") + " " + (abstract or "")).lower()
    if "systematic review" in blob or "meta-analysis" in blob:
        return "systematic-review"
    if "case report" in blob or "case series" in blob:
        return "case-report"
    if "randomized controlled trial" in blob or ("randomized" in blob and "trial" in blob):
        return "rct"
    return "article"


def _flag_safety(title, abstract):
    blob = ((title or "") + " " + (abstract or "")).lower()
    return any(k in blob for k in SAFETY_LEXICON)


def fetch(topic, review_type="all", year_from=None, year_to=None,
          safety=False, max_results=30, run=False, out=None):
    if not run:
        print("[PREVIEW] would query Semantic Scholar for topic=%r (optional; degrades on 429)"
              % topic)
        return None

    q = topic
    if review_type in ("systematic-review", "meta-analysis", "scoping-review"):
        q += " systematic review"
    elif review_type == "rct":
        q += " randomized controlled trial"
    elif review_type == "case-report":
        q += " case report"
    if safety:
        q += " adverse event"

    params = {
        "query": q,
        "limit": min(max_results, 100),
        "fields": "title,year,citationCount,venue,externalIds,abstract,publicationTypes,authors,publicationDate,openAccessPdf",
    }
    url = BASE + "?" + urllib.parse.urlencode(params)
    s2_key = http_utils.load_s2_key()
    http_utils.notify_s2_key_if_missing(s2_key)
    # S2 priority demoted: its key requires a manual form review (not auto-issued),
    # so a key is usually absent short-term. When absent, skip this source outright
    # (no doomed 429 request) to avoid wasted calls and slowing the primary flow;
    # only query for real when a key is present (much looser rate limit).
    if not s2_key:
        from i18n import t
        print(t("semantic_scholar.skip_no_key"))
        empty = _empty(topic)
        if out:
            try:
                with open(out, "w", encoding="utf-8") as f:
                    json.dump(empty, f, ensure_ascii=False, indent=2)
                print("[OK] Semantic Scholar wrote 0 works (skipped, no key) -> %s" % out)
            except OSError as werr:
                print("[WARN] could not write skipped S2 payload: %s" % werr)
        return empty
    max_retries = 2
    try:
        j = http_utils.get_json(url, headers=http_utils.build_s2_headers(s2_key),
                                timeout=45, max_retries=max_retries)
    except http_utils.HttpError as e:
        # Optional enhancement source: retries exhausted (incl. 429) -> graceful
        # degradation to empty; never abort the pipeline.
        print("[WARN] Semantic Scholar failed (%s) -> skipped (optional source)" % e)
        empty = _empty(topic)
        # Still materialise the file when --out was requested: downstream
        # normalize/merge steps and orchestration scripts expect the artifact
        # to exist even for a degraded (empty) optional source.
        if out:
            try:
                with open(out, "w", encoding="utf-8") as f:
                    json.dump(empty, f, ensure_ascii=False, indent=2)
                print("[OK] Semantic Scholar wrote 0 works (degraded) -> %s" % out)
            except OSError as werr:
                print("[WARN] could not write degraded S2 payload: %s" % werr)
        return empty

    data = j.get("data", [])
    collected = []
    for d in data:
        title = d.get("title") or ""
        abstract = d.get("abstract") or ""
        ext = d.get("externalIds") or {}
        # Authors
        authors = []
        for a in (d.get("authors") or [])[:6]:
            nm = a.get("name")
            if nm:
                authors.append(nm)
        if len(d.get("authors") or []) > 6:
            authors.append("et al.")
        collected.append({
            "source": "SemanticScholar",
            "id": ext.get("DOI") or d.get("paperId"),
            "doi": ext.get("DOI"),
            "pmid": ext.get("PubMed"),
            "pmcid": ext.get("PubMedCentral"),
            "title": title,
            "authors": authors,
            "year": d.get("year"),
            "publication_date": d.get("publicationDate"),
            "publication": d.get("venue"),
            "journal_iso": d.get("venue"),
            "type": "article",
            # pub_types: S2 publicationTypes 原样透传（CamelCase，如 "Review" /
            # "JournalArticle"），供 doc_type_filter 的 pubType 强通道使用——
            # 2026-09-09 起 doc-type 甄别依赖该字段（此前请求了字段但未落地）。
            "pub_types": [_camel_to_words(t) for t in (d.get("publicationTypes") or [])],
            "study_type": _study_type_from(title, abstract),
            "cited_by_count": d.get("citationCount") or 0,
            "url": ext.get("DOI") or ("https://www.semanticscholar.org/paper/%s" % d.get("paperId") if d.get("paperId") else None),
            "open_access_url": d.get("openAccessPdf", {}).get("url") if d.get("openAccessPdf") else None,
            "abstract_snippet": abstract or "",
            "mesh": None,
            "is_safety": _flag_safety(title, abstract),
        })
    payload = {
        "source": "SemanticScholar",
        "query": q,
        "review_type": review_type,
        "year_from": year_from,
        "year_to": year_to,
        "safety": safety,
        "count": len(collected),
        "works": collected,
    }
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print("[OK] Semantic Scholar wrote %d works -> %s" % (len(collected), out))
    return payload


def _camel_to_words(s):
    """S2 类型标签 CamelCase → 分词（"JournalArticle"→"Journal Article"）。

    使 doc_type_filter._PUBTYPE_MAP 的空格形态正则（journal article /
    systematic review / clinical trial）能命中；纯小写/含空格标签原样返回。
    """
    s = str(s or "")
    return re.sub(r"(?<=[a-z])(?=[A-Z])", " ", s).strip()


def _empty(topic):
    return {"source": "SemanticScholar", "query": topic, "count": 0, "works": []}


def main():
    ap = argparse.ArgumentParser(description="Fetch literature via Semantic Scholar (optional).")
    ap.add_argument("--topic", required=True)
    ap.add_argument("--review-type", default="all")
    ap.add_argument("--year-from", type=int)
    ap.add_argument("--year-to", type=int)
    ap.add_argument("--safety", action="store_true")
    ap.add_argument("--max", type=int, default=30)
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--out")
    args = ap.parse_args()
    res = fetch(args.topic, args.review_type, args.year_from, args.year_to,
                args.safety, args.max, args.run, args.out)
    if res and not args.out:
        print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
