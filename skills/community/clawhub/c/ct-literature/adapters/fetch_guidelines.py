#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fetch_guidelines.py — clinical guideline multi-source aggregator (ct-literature G-upgrade).

Aggregates clinical-practice guidelines from 12+ authoritative sources into one
de-duplicated, normalized list. Two access tiers, honestly labelled:

  * api    — fetched live via the shared http_utils GET+retry (OpenAlex guideline search,
             Europe PMC, GIN, WHO IRIS; NICE / MAGICapp / TRIP are key-gated best-effort).
  * portal — no free keyword-search API exists for these orgs; emit an honest
             navigational pointer (org portal + the topic) so the user knows where to
             look. These records carry `retrieved:false` — they are NOT fabricated
             fetches.

Pure local computation + read-only public endpoints; zero confidential data. SAFE
PREVIEW: returns None (preview) unless run=True. Every live source is wrapped so a
failure degrades to a `source_status` note — never aborts the whole retrieval.

Contract (mirrors fetch_openalex.fetch so ct_literature can call it uniformly):
    fetch(topic, review_type="all", year_from=None, year_to=None, safety=False,
          max_results=30, run=False, out=None, sources=None, http_get=None,
          mailto="dev@example.com") -> {source, query, count, works, source_status} | None
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.parse

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                      # sibling imports within adapters/
sys.path.insert(0, os.path.dirname(_HERE))     # skill root -> `from adapters import http_utils`
from adapters import http_utils  # shared GET+retry (429 Retry-After, backoff, Bearer key)

# ── 12+ guideline source registry ──────────────────────────────────────────────
# access : "api"   -> live fetch (or key-gated best-effort)
#          "portal" -> navigational pointer only (no free API)
# key_env: env var carrying the API key for key-gated api sources; None otherwise
GUIDELINE_SOURCES = {
    "OpenAlex":  {"access": "api",    "key_env": None,            "org_url": "https://openalex.org"},
    "EuropePMC": {"access": "api",    "key_env": None,            "org_url": "https://europepmc.org"},
    "GIN":       {"access": "api",    "key_env": None,            "org_url": "https://guidelines.ebm.torum.be"},
    "WHO":       {"access": "api",    "key_env": None,            "org_url": "https://www.who.int/publications/guidelines"},
    "NICE":      {"access": "api",    "key_env": "NICE_API_KEY",  "org_url": "https://www.nice.org.uk/guidance"},
    "MAGICapp":  {"access": "api",    "key_env": None,            "org_url": "https://app.magicapp.org"},
    "TRIP":      {"access": "api",    "key_env": "TRIP_API_KEY",  "org_url": "https://www.tripdatabase.com"},
    # ---- portal-only (no free keyword API) ----
    "NCCN":      {"access": "portal", "key_env": None,            "org_url": "https://www.nccn.org/professionals/physician_gls"},
    "ADA":       {"access": "portal", "key_env": None,            "org_url": "https://diabetesjournals.org/clinicalcare"},
    "AHA":       {"access": "portal", "key_env": None,            "org_url": "https://www.ahajournals.org"},
    "SIGN":      {"access": "portal", "key_env": None,            "org_url": "https://www.sign.ac.uk/our-guidelines"},
    "CMA":       {"access": "portal", "key_env": None,            "org_url": "https://www.cma.org.cn"},
    "CPIC":      {"access": "portal", "key_env": None,            "org_url": "https://cpicpgx.org/guidelines"},
}

_GUIDELINE_TERMS = ["guideline", "guidelines", "recommendation", "recommendations",
                    "consensus", "guidance", "standard of care", "指南", "共识", "规范"]


def _looks_like_guideline(title, abstract=""):
    """Light precision filter: keep only items whose title/abstract signals a guideline."""
    blob = ("%s %s" % (title or "", abstract or "")).lower()
    return any(t in blob for t in _GUIDELINE_TERMS)


def _norm_title(t):
    if not t:
        return ""
    t = (t or "").lower()
    t = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", t)
    return " ".join(t.split())


def _default_get(url, headers=None, timeout=45):
    """Default live fetcher -> JSON via shared http_utils (retry/backoff built in)."""
    return http_utils.get_json(url, headers=headers, timeout=timeout, max_retries=4)


def _normalize(org, access, title, year=None, url=None, org_url=None,
               summary=None, update_date=None, retrieved=True, topic=None, extra=None):
    return {
        "source": "Guidelines",
        "guideline_org": org,
        "access": access,             # "api" | "portal"
        "retrieved": retrieved,       # False for portal pointers
        "title": (title or "").strip(),
        "year": _as_int(year),        # always int or None (sources return str/int inconsistently)
        "url": url,
        "org_url": org_url,
        "summary": (summary or "").strip() or None,
        "update_date": update_date,
        "topic": topic,
        "extra": extra or {},
    }


# ── per-source api fetchers (each returns a list of normalized records) ─────────
def _oa_guidelines(topic, max_results, http_get, year_from=None, year_to=None, mailto="dev@example.com"):
    filt = ["has_doi:true"]
    if year_from:
        filt.append("from_publication_date:%d-01-01" % year_from)
    if year_to:
        filt.append("to_publication_date:%d-12-31" % year_to)
    params = {
        "search": "%s guideline" % topic,
        "filter": ",".join(filt),
        "per-page": min(50, max(1, max_results)),
        "page": 1,
        "mailto": mailto,
        "select": "id,doi,title,display_name,publication_year,publication_date,primary_location,best_oa_location,abstract_inverted_index,ids",
    }
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
    headers = http_utils.build_openalex_headers(mailto=mailto)
    j = http_get(url, headers=headers)
    out = []
    for r in j.get("results", []):
        title = (r.get("title") or r.get("display_name") or "").strip()
        abstract = ""
        inv = r.get("abstract_inverted_index")
        if inv:
            try:
                mp = max(max(p) for p in inv.values() if p)
                slots = [None] * (mp + 1)
                for w, idxs in inv.items():
                    for i in idxs:
                        if i <= mp:
                            slots[i] = w
                abstract = " ".join(x for x in slots if x)
            except Exception:
                abstract = ""
        if not _looks_like_guideline(title, abstract):
            continue
        loc = r.get("primary_location") or {}
        src = loc.get("source") or {} if loc else {}
        oa = r.get("best_oa_location") or {}
        oa_url = oa.get("pdf_url") or oa.get("landing_page_url") or r.get("doi")
        out.append(_normalize(
            "OpenAlex", "api", title,
            year=r.get("publication_year"),
            url=oa_url or r.get("doi"),
            org_url="https://openalex.org",
            summary=abstract[:400] if abstract else None,
            update_date=r.get("publication_date"),
            retrieved=True, topic=topic,
            extra={"publication": src.get("display_name"), "doi": r.get("doi"),
                   "pdf_url": oa.get("pdf_url")}))
    return out


def _epmc_guidelines(topic, max_results, http_get, year_from=None, year_to=None):
    q = "(%s) AND (guideline OR recommendations OR consensus)" % topic
    params = {
        "query": q,
        "format": "json",
        "pageSize": min(50, max(1, max_results)),
        "resultType": "core",
    }
    if year_from:
        params["query"] += " AND (PUBYEAR:%s)" % year_from
    if year_to:
        params["query"] += " AND (PUBYEAR:%s)" % year_to
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urllib.parse.urlencode(params)
    j = http_get(url)
    out = []
    for r in (j.get("resultList") or {}).get("result", []):
        title = (r.get("title") or "").strip()
        abstract = r.get("abstractText") or ""
        if not _looks_like_guideline(title, abstract):
            continue
        pmid = r.get("pmid")
        out.append(_normalize(
            "EuropePMC", "api", title,
            year=r.get("pubYear"),
            url=("https://europepmc.org/article/MED/%s" % pmid) if pmid else None,
            org_url="https://europepmc.org",
            summary=(abstract[:400] if abstract else None),
            update_date=r.get("firstPublicationDate") or r.get("lastUpdate"),
            retrieved=True, topic=topic,
            extra={"pmid": pmid, "pmcid": r.get("pmcid"), "doi": r.get("doi"),
                   "publication": r.get("journalInfo", {}).get("journal", {}).get("title")}))
    return out


def _gin_guidelines(topic, max_results, http_get):
    url = "https://guidelines.ebm.torum.be/api/v1/guidelines?" + urllib.parse.urlencode(
        {"query": topic, "page": 1, "per_page": min(50, max(1, max_results))})
    j = http_get(url)
    results = j.get("results") or j.get("data") or (j.get("guidelines") or [])
    if isinstance(results, dict):
        results = results.get("results") or results.get("data") or []
    out = []
    for r in results[:max_results]:
        if not isinstance(r, dict):
            continue
        title = (r.get("title") or r.get("name") or "").strip()
        if not title or not _looks_like_guideline(title):
            continue
        out.append(_normalize(
            "GIN", "api", title,
            year=_as_int(r.get("year") or r.get("publication_year")),
            url=r.get("url") or r.get("link"),
            org_url="https://guidelines.ebm.torum.be",
            summary=(r.get("summary") or r.get("description") or "")[:400] or None,
            update_date=r.get("updated_at") or r.get("date"),
            retrieved=True, topic=topic,
            extra={"organization": r.get("organization") or r.get("developer")}))
    return out


def _who_guidelines(topic, max_results, http_get):
    url = "https://iris.who.int/rest/search?" + urllib.parse.urlencode(
        {"q": "%s guideline" % topic, "wt": "json", "rows": min(50, max(1, max_results)),
         "fl": "title,url,date,description"})
    j = http_get(url)
    docs = (j.get("response") or {}).get("docs", [])
    out = []
    for r in docs[:max_results]:
        if not isinstance(r, dict):
            continue
        title = (r.get("title") or "").strip()
        if not title or not _looks_like_guideline(title, r.get("description", "")):
            continue
        out.append(_normalize(
            "WHO", "api", title,
            year=_as_int(str(r.get("date") or "")[:4]),
            url=r.get("url"),
            org_url="https://www.who.int/publications/guidelines",
            summary=(r.get("description") or "")[:400] or None,
            update_date=r.get("date"),
            retrieved=True, topic=topic))
    return out


def _nice_guidelines(topic, max_results, http_get, key):
    if not key:
        return None  # signal caller to mark key-gated skip
    url = "https://api.nice.org.uk/v1/guidance?" + urllib.parse.urlencode(
        {"search": topic, "pageSize": min(50, max(1, max_results))})
    headers = {"Authorization": "Bearer %s" % key}
    j = http_get(url, headers=headers)
    results = j.get("guidance") or j.get("results") or j.get("data") or []
    out = []
    for r in results[:max_results]:
        if not isinstance(r, dict):
            continue
        title = (r.get("title") or "").strip()
        if not title or not _looks_like_guideline(title):
            continue
        out.append(_normalize(
            "NICE", "api", title,
            year=_as_int(r.get("published") or r.get("datePublished")),
            url=r.get("webAddress") or r.get("url") or r.get("href"),
            org_url="https://www.nice.org.uk/guidance",
            summary=(r.get("summary") or r.get("description") or "")[:400] or None,
            update_date=r.get("updated") or r.get("lastUpdated"),
            retrieved=True, topic=topic,
            extra={"status": r.get("status")}))
    return out


def _magicapp_guidelines(topic, max_results, http_get):
    url = "https://app.magicapp.org/api/v1/guidelines?" + urllib.parse.urlencode(
        {"query": topic, "limit": min(50, max(1, max_results))})
    j = http_get(url)
    results = j.get("results") or j.get("data") or j.get("guidelines") or []
    out = []
    for r in results[:max_results]:
        if not isinstance(r, dict):
            continue
        title = (r.get("title") or r.get("name") or "").strip()
        if not title or not _looks_like_guideline(title):
            continue
        out.append(_normalize(
            "MAGICapp", "api", title,
            year=_as_int(r.get("year")),
            url=r.get("url") or r.get("link"),
            org_url="https://app.magicapp.org",
            summary=(r.get("summary") or r.get("abstract") or "")[:400] or None,
            update_date=r.get("updated"),
            retrieved=True, topic=topic))
    return out


def _trip_guidelines(topic, max_results, http_get, key):
    if not key:
        return None
    url = "https://api.tripdatabase.com/v1/articles?" + urllib.parse.urlencode(
        {"query": topic, "limit": min(50, max(1, max_results)), "category": "guidelines"})
    headers = {"Authorization": "Bearer %s" % key}
    j = http_get(url, headers=headers)
    results = j.get("results") or j.get("data") or j.get("articles") or []
    out = []
    for r in results[:max_results]:
        if not isinstance(r, dict):
            continue
        title = (r.get("title") or "").strip()
        if not title or not _looks_like_guideline(title, r.get("abstract", "")):
            continue
        out.append(_normalize(
            "TRIP", "api", title,
            year=_as_int(r.get("year") or r.get("publicationDate")),
            url=r.get("url") or r.get("link"),
            org_url="https://www.tripdatabase.com",
            summary=(r.get("abstract") or r.get("snippet") or "")[:400] or None,
            update_date=r.get("date"),
            retrieved=True, topic=topic,
            extra={"source_name": r.get("source") or r.get("sourceName")}))
    return out


def _portal_pointers(topic, orgs):
    """Honest navigational pointers for orgs without a free keyword API.

    NOT a fetch — retrieved=False, url is the canonical portal. The user sees where
    to look; nothing is fabricated.
    """
    out = []
    for org in orgs:
        meta = GUIDELINE_SOURCES.get(org)
        if not meta:
            continue
        out.append(_normalize(
            org, "portal", "%s — 在 %s 官方门户检索「%s」" % (org, org, topic),
            url=meta["org_url"], org_url=meta["org_url"],
            retrieved=False, topic=topic,
            extra={"note": "portal-only: no free keyword API; navigate the org portal to retrieve"}))
    return out


def _as_int(v):
    try:
        return int(str(v)[:4]) if v else None
    except Exception:
        return None


# ── orchestrator ───────────────────────────────────────────────────────────────
def fetch(topic, review_type="all", year_from=None, year_to=None, safety=False,
          max_results=30, run=False, out=None, sources=None, http_get=None,
          mailto="dev@example.com"):
    """Aggregate clinical guidelines across 12+ sources.

    Returns {source, query, count, works, source_status} or None (preview / no run).
    `http_get(url, headers=None)` is injectable so tests run offline (mock responses).
    """
    if not run:
        print("[PREVIEW] would aggregate clinical guidelines for topic=%r across %d sources "
              "(use --run to execute)" % (topic, len(GUIDELINE_SOURCES)))
        return None

    get = http_get or _default_get
    enabled = [s for s in (sources or list(GUIDELINE_SOURCES.keys())) if s in GUIDELINE_SOURCES]
    source_status = {}
    collected = []

    # key-gated sources resolve their key once
    keys = {}
    for org in enabled:
        ke = GUIDELINE_SOURCES[org].get("key_env")
        if ke and ke not in keys:
            keys[ke] = os.environ.get(ke)

    for org in enabled:
        meta = GUIDELINE_SOURCES[org]
        try:
            if meta["access"] == "portal":
                recs = _portal_pointers(topic, [org])
                source_status[org] = {"access": "portal", "status": "pointer", "count": len(recs)}
            else:
                ke = meta.get("key_env")
                key = keys.get(ke) if ke else None
                if ke and not key:
                    # key-gated but no key configured -> graceful skip (never fake)
                    recs = []
                    source_status[org] = {"access": "api", "status": "skipped_no_key",
                                          "count": 0, "key_env": ke}
                else:
                    if org == "OpenAlex":
                        recs = _oa_guidelines(topic, max_results, get, year_from, year_to, mailto)
                    elif org == "EuropePMC":
                        recs = _epmc_guidelines(topic, max_results, get, year_from, year_to)
                    elif org == "GIN":
                        recs = _gin_guidelines(topic, max_results, get)
                    elif org == "WHO":
                        recs = _who_guidelines(topic, max_results, get)
                    elif org == "NICE":
                        recs = _nice_guidelines(topic, max_results, get, key)
                    elif org == "MAGICapp":
                        recs = _magicapp_guidelines(topic, max_results, get)
                    elif org == "TRIP":
                        recs = _trip_guidelines(topic, max_results, get, key)
                    else:
                        recs = []
                    source_status[org] = {"access": "api", "status": "ok", "count": len(recs)}
            collected.extend(recs)
        except Exception as e:  # one source failing must not abort the aggregation
            source_status[org] = {"access": meta["access"], "status": "error",
                                   "error": str(e)[:200], "count": 0}

    # dedupe by (org, normalized title)
    seen, works = set(), []
    for w in collected:
        k = (w["guideline_org"], _norm_title(w["title"]))
        if not k[1] or k in seen:
            continue
        seen.add(k)
        works.append(w)

    works.sort(key=lambda w: (-(w.get("year") or 0), w["guideline_org"]))
    payload = {
        "source": "Guidelines",
        "query": topic,
        "review_type": review_type,
        "year_from": year_from,
        "year_to": year_to,
        "count": len(works),
        "works": works,
        "source_status": source_status,
        "total_sources": len(GUIDELINE_SOURCES),
        "api_sources": sum(1 for m in GUIDELINE_SOURCES.values() if m["access"] == "api"),
        "portal_sources": sum(1 for m in GUIDELINE_SOURCES.values() if m["access"] == "portal"),
    }
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print("[OK] guideline aggregation wrote %d records -> %s" % (len(works), out))
    print("[OK] guideline aggregation: %d records from %d sources (api=%d portal=%d)"
          % (len(works), len(enabled),
             sum(1 for s in source_status.values() if s["access"] == "api"),
             sum(1 for s in source_status.values() if s["access"] == "portal")))
    return payload


def main():
    ap = argparse.ArgumentParser(description="Aggregate clinical guidelines across 12+ sources.")
    ap.add_argument("--topic", required=True, help="disease / drug / topic")
    ap.add_argument("--year-from", type=int, help="lower bound year")
    ap.add_argument("--year-to", type=int, help="upper bound year")
    ap.add_argument("--max", type=int, default=30, help="max records per api source")
    ap.add_argument("--sources", help="comma-separated subset of sources (default: all)")
    ap.add_argument("--run", action="store_true", help="execute network requests")
    ap.add_argument("--out", help="output JSON path")
    args = ap.parse_args()
    srcs = [s.strip() for s in args.sources.split(",")] if args.sources else None
    res = fetch(args.topic, year_from=args.year_from, year_to=args.year_to,
                max_results=args.max, run=args.run, out=args.out, sources=srcs)
    if res and not args.out:
        print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
