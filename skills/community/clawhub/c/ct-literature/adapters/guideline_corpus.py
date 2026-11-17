#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
guideline_corpus.py — LOCAL loader for the curated clinical-guideline corpus (G-upgrade).

The guideline corpus is built ONCE (or periodically) by adapters/build_guidelines.py,
which materializes guideline documents + metadata into references/guidelines/ and writes
guidelines_index.json. This module reads that LOCAL index at analysis time — ZERO network.

It returns the same payload shape as fetch_guidelines.fetch() so ct_literature consumes it
uniformly:
    {source, query, count, works, source_status, total_sources, api_sources, portal_sources}

Why local-first: clinical guidelines are a VERSIONED reference standard (NCCN 2024.v3,
ADA 2026 Standards). The value is stability + reproducibility, so at analysis time we read a
pinned local corpus instead of fetching "latest" on every run. This also honours ct-base's
local-first / data-不出域 principle. The only network path is build_guidelines.py, an explicit
author action.
"""
import argparse
import json
import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))
_SKILL_ROOT = os.path.dirname(_HERE)
_DEFAULT_CORPUS = os.path.join(_SKILL_ROOT, "references", "guidelines")
_TOTAL_SOURCES = 13  # mirrors fetch_guidelines.GUIDELINE_SOURCES at build time

# 中国监管 / 学会机构（升级项 I）：语料条目多数没有 region 字段（96 条实测全为 None），
# 若只认字段，china 车道会永远返回 0 条 —— 那不是「中国证据少」，而是功能空转。
# 因此按机构名兜底推断：显式 region 字段优先，缺失时看 guideline_org。
_CN_ORGS = {"CMA", "CDE", "NMPA", "NHC", "CACA", "CSCO", "CHINESE MEDICAL ASSOCIATION"}


def region_of(entry):
    """条目的证据车道区域：显式 region 字段优先，否则按机构名推断，默认 global。"""
    r = (entry.get("region") or "").strip().lower()
    if r:
        return "china" if r in ("china", "cn", "nmpa", "cde") else "global"
    org = str(entry.get("guideline_org") or entry.get("org") or "").strip().upper()
    if org in _CN_ORGS:
        return "china"
    return "global"


def _norm(s):
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", s)
    return " ".join(s.split())


def _match_entry(e, topic, enabled, region=None):
    if enabled and e.get("guideline_org") not in enabled and e.get("org") not in enabled:
        return False
    # 证据车道区域过滤（升级项 I，2026-11-02）：china / global / both(None)
    # 显式 region 字段优先；缺失时按机构名推断（CMA/CDE/NMPA… → china），
    # 其余按 global —— 既有语料零 region 字段，纯字段判断会让 china 车道空转。
    if region and region != "both":
        e_region = region_of(e)
        if region == "china" and e_region != "china":
            return False
        if region == "global" and e_region != "global":
            return False
    if not topic:
        return True
    t = _norm(topic)
    hay = " ".join([
        _norm(e.get("topic")),
        " ".join(_norm(x) for x in (e.get("topic_tags") or [])),
        _norm(e.get("title")),
        _norm(e.get("summary") or ""),
    ])
    return t in hay


def load(topic=None, review_type="all", sources=None, corpus_dir=None,
         max_results=20, out=None, region=None):
    """Load curated guideline records from the LOCAL corpus. Never hits the network.

    region: None/"both" = all; "global" = 非中国监管语料; "china" = CDE/NMPA 中国向语料
            （升级项 I：`--guidelines-region china` 提供中国监管证据视图）。
    Returns the same payload shape as fetch_guidelines.fetch(). If the corpus index is
    missing, returns an honest `corpus_missing` payload telling the author to run the builder.
    """
    corpus_dir = corpus_dir or _DEFAULT_CORPUS
    index_path = os.path.join(corpus_dir, "guidelines_index.json")

    if not os.path.isfile(index_path):
        return {
            "source": "Guidelines",
            "query": topic,
            "review_type": review_type,
            "count": 0,
            "works": [],
            "source_status": {"__corpus__": {
                "status": "missing",
                "note": "references/guidelines/guidelines_index.json not found; "
                        "run: python adapters/build_guidelines.py --topic <topic>"}},
            "total_sources": _TOTAL_SOURCES,
            "api_sources": 0,
            "portal_sources": 0,
            "corpus_missing": True,
        }

    with open(index_path, "r", encoding="utf-8") as f:
        idx = json.load(f)

    entries = idx.get("entries", [])
    enabled = [s.strip() for s in sources.split(",")] if sources else []

    works = [e for e in entries if _match_entry(e, topic, enabled, region)]
    # 回填推断后的车道归属（additive；报告/审计可直接看到 china / global）
    for _w in works:
        _w.setdefault("region", region_of(_w))
    works.sort(key=lambda w: (-(w.get("year") or 0), w.get("guideline_org") or w.get("org", "")))
    if max_results and max_results > 0:
        works = works[:max_results]

    source_status = {}
    for e in works:
        org = e.get("guideline_org") or e.get("org")
        st = source_status.setdefault(org, {"access": e.get("access"), "status": "loaded", "count": 0})
        st["count"] += 1

    payload = {
        "source": "Guidelines",
        "query": topic,
        "review_type": review_type,
        "count": len(works),
        "works": works,
        "source_status": source_status,
        "total_sources": idx.get("total_sources", _TOTAL_SOURCES),
        "api_sources": idx.get("api_sources", 0),
        "portal_sources": idx.get("portal_sources", 0),
        "corpus_built_at": idx.get("built_at"),
        "corpus_dir": corpus_dir,
        "region": region or "both",
    }

    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print("[OK] loaded guideline corpus -> %s (%d records)" % (out, len(works)))
    return payload


def main():
    ap = argparse.ArgumentParser(description="Load curated guideline corpus (local, zero network).")
    ap.add_argument("--topic", help="filter by topic (substring match on topic/tags/title)")
    ap.add_argument("--sources", help="comma-separated org subset (e.g. NCCN,WHO)")
    ap.add_argument("--max", type=int, default=20)
    ap.add_argument("--corpus-dir", help="override corpus directory")
    ap.add_argument("--out", help="write loaded payload to JSON")
    args = ap.parse_args()
    res = load(topic=args.topic, sources=args.sources, max_results=args.max,
               corpus_dir=args.corpus_dir, out=args.out)
    if not args.out:
        print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
