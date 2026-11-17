#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fetch_preprints.py — bioRxiv / medRxiv fetcher (clinical & biomedical preprints).

Two-stage retrieval:
  Stage 1: Europe PMC PPR (cursorMark pagination) — server-side keyword match.
  Stage 2: api.biorxiv.org — incremental window (last 3 days before the most
            recent Europe PMC result) to catch preprints not yet indexed by
            Europe PMC, with local keyword filtering.

Both stages merge by DOI (dedup). bioRxiv and medRxiv share the same official
API (server param differs), so the logic is symmetric.

No key required. Reuses http_utils.get_json (exponential backoff, Retry-After).
Zero confidential data or information input; reads only public literature.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.parse
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from adapters import http_utils  # shared GET+retry (exponential backoff, 429 Retry-After)

EPMC_BASE = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
API_BASE = "https://api.biorxiv.org"

SERVER_MAP = {
    "biorxiv": "bioRxiv",
    "medrxiv": "medRxiv",
}

# Europe PMC typically lags bioRxiv by 1–3 days. We pull this many days BEFORE
# the most recent Europe PMC result as the API catch-up window.
API_WINDOW_DAYS = 3

SAFETY_LEXICON = [
    "adverse event", "adverse reaction", "side effect", "safety", "toxicity",
    "toxic", "case report", "pharmacovigilance", "drug-induced", "drug reaction",
]


def _strip_html(s):
    if not s:
        return s
    return re.sub(r"<[^>]+>", "", s)


def _study_type_from(pub_types, title, abstract):
    blob = ((title or "") + " " + (abstract or "")).lower()
    pts = " ".join(pub_types).lower()
    if "systematic review" in blob or "meta-analysis" in blob:
        return "systematic-review"
    if "case report" in blob or "case series" in blob:
        return "case-report"
    if "randomized controlled trial" in blob or ("randomized" in blob and "trial" in blob):
        return "rct"
    if "review" in pts:
        return "review"
    return "preprint"


def _flag_safety(title, abstract):
    blob = ((title or "") + " " + (abstract or "")).lower()
    return any(k in blob for k in SAFETY_LEXICON)


def _extract(rec, source_label):
    """Extract a Europe PMC PPR record into our work schema."""
    ji = rec.get("journalInfo") or {}
    authors = []
    affiliations = []
    al = rec.get("authorList") or {}
    for a in (al.get("author") or [])[:6]:
        nm = a.get("fullName")
        if nm:
            authors.append(nm)
        aff_list = (a.get("authorAffiliationDetailsList") or {}).get("authorAffiliation") or []
        for aff in aff_list:
            if aff.get("affiliation") and aff["affiliation"] not in affiliations:
                affiliations.append(aff["affiliation"])
    n_auth = len(al.get("author") or [])
    if n_auth > 6:
        authors.append("et al.")
    mesh = []
    mh = rec.get("meshHeadingList") or {}
    for h in (mh.get("meshHeading") or [])[:8]:
        d = h.get("descriptorName")
        if d:
            mesh.append(d)
    title = _strip_html(rec.get("title") or "")
    abstract = _strip_html(rec.get("abstractText") or "")
    cited = rec.get("citedByCount")
    doi = (rec.get("doi") or "").strip()
    _host = "biorxiv" if source_label == "bioRxiv" else "medrxiv"
    pdf_direct = ("https://www.%s.org/content/%s.full.pdf" % (_host, doi)) if doi else None
    landing = ("https://doi.org/" + doi) if doi else None
    return {
        "source": source_label,
        "id": rec.get("id") or doi,
        "pmid": rec.get("pmid"),
        "pmcid": rec.get("pmcid"),
        "doi": doi,
        "title": title,
        "authors": authors or None,
        "affiliations": affiliations[:5] or None,
        "year": int(rec["pubYear"]) if rec.get("pubYear") and str(rec.get("pubYear")).isdigit() else None,
        "publication_date": (rec.get("printPublicationDate")
                            or rec.get("dateOfPublication")
                            or rec.get("firstPublicationDate")
                            or (str(rec["pubYear"]) if rec.get("pubYear") and str(rec.get("pubYear")).isdigit() else None)),
        "publication": source_label,
        "journal_iso": source_label,
        "type": "preprint",
        "study_type": _study_type_from(rec.get("pubTypeList", {}).get("pubType", []) or [], title, abstract),
        "cited_by_count": int(cited) if isinstance(cited, int) else 0,
        "url": landing,
        "open_access_url": pdf_direct,
        "abstract_snippet": abstract or "",
        "mesh": mesh or None,
        "is_safety": _flag_safety(title, abstract),
        "is_preprint": True,
        "volume": None,
        "issue": None,
        "page": rec.get("pageInfo"),
    }


def _extract_api(rec, source_label):
    """Extract an api.biorxiv.org record into our work schema."""
    doi = (rec.get("doi") or "").strip()
    _host = "biorxiv" if source_label == "bioRxiv" else "medrxiv"
    pdf_direct = ("https://www.%s.org/content/%s.full.pdf" % (_host, doi)) if doi else None
    landing = ("https://doi.org/" + doi) if doi else None
    title = _strip_html(rec.get("title") or "")
    abstract = _strip_html(rec.get("abstract") or "")
    authors_str = rec.get("authors") or ""
    authors = [a.strip() for a in authors_str.split(";") if a.strip()][:6]
    if authors_str.count(";") > 5:
        authors.append("et al.")
    date_str = rec.get("date") or ""
    year = int(date_str[:4]) if date_str and date_str[:4].isdigit() else None
    return {
        "source": source_label,
        "id": doi,
        "pmid": None,
        "pmcid": None,
        "doi": doi,
        "title": title,
        "authors": authors or None,
        "affiliations": None,
        "year": year,
        "publication_date": date_str or None,
        "publication": source_label,
        "journal_iso": source_label,
        "type": "preprint",
        "study_type": _study_type_from([], title, abstract),
        "cited_by_count": 0,
        "url": landing,
        "open_access_url": pdf_direct,
        "abstract_snippet": abstract or "",
        "mesh": None,
        "is_safety": _flag_safety(title, abstract),
        "is_preprint": True,
        "volume": None,
        "issue": None,
        "page": None,
    }


def _parse_api_date(rec):
    """Parse date from an api.biorxiv.org record (YYYY-MM-DD)."""
    d = rec.get("date") or ""
    try:
        return datetime.strptime(d[:10], "%Y-%m-%d")
    except Exception:
        return None


def _local_keyword_match(topic, rec):
    """Check if a record matches the topic keywords (local filter for API results).

    Supports OR groups like "(diabetes OR diabetes mellitus)treatment" by
    extracting each OR group and requiring at least one term per group.
    """
    title = (rec.get("title") or "").lower()
    abstract = (rec.get("abstract") or rec.get("abstract_snippet") or "").lower()
    blob = title + " " + abstract

    # Parse topic into OR-groups: e.g. "(A OR B)C" -> [["a","b"],["c"]]
    # We extract parenthesized OR-groups and bare tokens.
    topic_lower = topic.lower()
    groups = []
    i = 0
    while i < len(topic_lower):
        if topic_lower[i] == '(':
            j = topic_lower.find(')', i)
            if j == -1:
                break
            inner = topic_lower[i+1:j]
            terms = [t.strip() for t in inner.split(' or ') if t.strip()]
            if terms:
                groups.append(terms)
            i = j + 1
        elif topic_lower[i] == ' ':
            i += 1
        else:
            # bare token
            j = i
            while j < len(topic_lower) and topic_lower[j] not in (' ', '('):
                j += 1
            token = topic_lower[i:j].strip()
            if token:
                groups.append([token])
            i = j

    # Each group must match at least one term in the blob
    for group in groups:
        if not any(term in blob for term in group):
            return False
    return True


def _fetch_bioxiv_api(server, from_date, to_date, topic, max_results=200):
    """Fetch preprints from api.biorxiv.org within [from_date, to_date].

    Returns list of extracted works matching `topic` (local keyword filter).
    """
    source_label = SERVER_MAP.get(server, server)
    collected = []
    seen_dois = set()
    cursor = 0
    page_size = 100  # API returns 100 per page
    date_from = from_date.strftime("%Y-%m-%d")
    date_to = to_date.strftime("%Y-%m-%d")

    while len(collected) < max_results:
        url = "%s/details/%s/%s/%s/%d" % (API_BASE, server, date_from, date_to, cursor)
        try:
            j = http_utils.get_json(url, headers={"User-Agent": http_utils.UA},
                                    timeout=45, max_retries=4)
        except http_utils.HttpError as e:
            print("[WARN] api.biorxiv.org %s request failed: %s" % (source_label, e))
            break

        messages = j.get("messages") or []
        items = j.get("collection") or []
        if not items:
            break

        for rec in items:
            doi = (rec.get("doi") or "").strip()
            if doi and doi in seen_dois:
                continue
            if doi:
                seen_dois.add(doi)
            # Local keyword filter
            if not _local_keyword_match(topic, rec):
                continue
            collected.append(_extract_api(rec, source_label))

        if len(items) < page_size:
            break
        cursor += page_size
        time.sleep(0.3)

    return collected


def _fetch_epmc_ppr(topic, source_label, review_type, year_from, year_to,
                    safety, max_results, date_from=None, date_to=None):
    """Fetch from Europe PMC PPR with cursorMark pagination + DOI dedup."""
    q = topic
    if review_type == "systematic-review":
        q += " AND (systematic review OR meta-analysis)"
    elif review_type == "meta-analysis":
        q += " AND meta-analysis"
    elif review_type == "scoping-review":
        q += " AND scoping review"
    elif review_type == "rct":
        q += " AND randomized controlled trial"
    elif review_type == "case-report":
        q += " AND case report"
    if safety:
        q += " AND (adverse event OR safety OR toxicity OR case report)"
    q += " AND SRC:PPR AND publisher:%s" % source_label

    if date_from or date_to:
        lo = date_from if date_from else "1900-01-01"
        hi = date_to if date_to else datetime.now().strftime("%Y-%m-%d")
        q += " AND (FIRST_PDATE:[%s TO %s])" % (lo, hi)
    elif year_from or year_to:
        lo = str(year_from) if year_from else "1900"
        hi = str(year_to) if year_to else "3000"
        q += " AND (PUB_YEAR:[%s TO %s])" % (lo, hi)

    collected = []
    seen_dois = set()
    cursor = "*"
    per = 100
    while len(collected) < max_results:
        params = {
            "query": q,
            "format": "json",
            "resultType": "core",
            "pageSize": min(per, max_results - len(collected)),
        }
        if cursor and cursor != "*":
            params["cursorMark"] = cursor
        url = EPMC_BASE + "?" + urllib.parse.urlencode(params)
        try:
            j = http_utils.get_json(url, headers={"User-Agent": http_utils.UA},
                                    timeout=45, max_retries=4)
        except http_utils.HttpError as e:
            print("[WARN] %s (Europe PMC PPR) request failed: %s"
                  % (source_label, e))
            break

        results = (j.get("resultList") or {}).get("result", [])
        if not results:
            break
        for rec in results:
            pub = (rec.get("bookOrReportDetails") or {}).get("publisher")
            if pub and pub.lower() == source_label.lower():
                ext = _extract(rec, source_label)
                doi = ext.get("doi", "")
                if doi and doi in seen_dois:
                    continue
                if doi:
                    seen_dois.add(doi)
                collected.append(ext)

        cursor = j.get("nextCursorMark")
        if not cursor:
            break
        if len(results) < per:
            break
        time.sleep(0.3)

    return collected


def fetch(topic, review_type="all", year_from=None, year_to=None,
          safety=False, max_results=30, run=False, out=None, server="biorxiv",
          date_from=None, date_to=None):
    """Fetch preprints from one server (bioRxiv / medRxiv).

    Two-stage retrieval:
      Stage 1: Europe PMC PPR (cursorMark) — server-side keyword match.
      Stage 2: api.biorxiv.org — incremental window for recent preprints not
               yet indexed by Europe PMC (local keyword filter).
    """
    source_label = SERVER_MAP.get(server, server)
    if not run:
        print("[PREVIEW] would fetch %s for %r (Europe PMC PPR + api.biorxiv.org)"
              % (source_label, topic))
        return None

    # ── Stage 1: Europe PMC PPR ──────────────────────────────────────────────
    epmc_results = _fetch_epmc_ppr(topic, source_label, review_type,
                                   year_from, year_to, safety, max_results,
                                   date_from=date_from, date_to=date_to)

    # Build DOI set for dedup in Stage 2
    epmc_dois = {w.get("doi") for w in epmc_results if w.get("doi")}

    # ── Stage 2: api.biorxiv.org incremental window ──────────────────────────
    # 基础窗口：EPC 结果里最新日期 - API_WINDOW_DAYS 到今天；若指定 date_from/date_to，
    # 进一步收窄（date_from 更晚则取 date_from；date_to 更早则取 date_to）。
    # 即便 EPC 无命中，只要用户给了日期窗口也照常拉取（保证日期过滤生效）。
    api_results = []
    if epmc_results or date_from or date_to:
        latest_dates = []
        for w in epmc_results:
            d = w.get("publication_date") or ""
            if not d:
                continue
            try:
                if len(d) >= 10 and "-" in d[:10]:
                    latest_dates.append(datetime.strptime(d[:10], "%Y-%m-%d"))
                elif len(d) >= 4 and d[:4].isdigit():
                    latest_dates.append(datetime(int(d[:4]), 12, 31))
            except Exception:
                pass
        _base_from = (max(latest_dates) - timedelta(days=API_WINDOW_DAYS)) if latest_dates \
            else (datetime.now() - timedelta(days=API_WINDOW_DAYS))
        api_from_dt = _base_from
        if date_from:
            _df = datetime.strptime(date_from, "%Y-%m-%d")
            if _df > api_from_dt:
                api_from_dt = _df
        api_to_dt = datetime.now()
        if date_to:
            _dt = datetime.strptime(date_to, "%Y-%m-%d")
            if _dt < api_to_dt:
                api_to_dt = _dt
        print("[INFO] %s: pulling api.biorxiv.org incremental window %s → %s"
              % (source_label, api_from_dt.strftime("%Y-%m-%d"),
                 api_to_dt.strftime("%Y-%m-%d")))
        api_results = _fetch_bioxiv_api(server, api_from_dt, api_to_dt, topic,
                                        max_results=max_results)
        # Filter out DOIs already in EPC results
        api_results = [w for w in api_results if w.get("doi") not in epmc_dois]
        if api_results:
            print("[OK] %s: +%d from api.biorxiv.org (incremental)"
                  % (source_label, len(api_results)))

    # ── Merge ────────────────────────────────────────────────────────────────
    works = epmc_results + api_results

    payload = {
        "source": source_label,
        "query": topic,
        "review_type": review_type,
        "year_from": year_from,
        "year_to": year_to,
        "date_from": date_from,
        "date_to": date_to,
        "safety": safety,
        "count": len(works),
        "works": works,
    }
    if out:
        _write(out, payload)
    return payload


def _write(out, payload):
    try:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print("[OK] %s wrote %d works -> %s" % (payload["source"], payload["count"], out))
    except OSError as werr:
        print("[WARN] could not write %s payload: %s" % (payload["source"], werr))


def _empty(topic, source_label):
    return {"source": source_label, "query": topic, "count": 0, "works": []}


def main():
    ap = argparse.ArgumentParser(
        description="Fetch bioRxiv / medRxiv via Europe PMC PPR + api.biorxiv.org.")
    ap.add_argument("--topic", required=True)
    ap.add_argument("--server", default="biorxiv", choices=["biorxiv", "medrxiv"])
    ap.add_argument("--review-type", default="all",
                    choices=["all", "systematic-review", "scoping-review",
                             "meta-analysis", "rct", "case-report"])
    ap.add_argument("--year-from", type=int)
    ap.add_argument("--year-to", type=int)
    ap.add_argument("--date-from", default=None, metavar="YYYY-MM-DD",
                    help="精确发表日期下界（月份级过滤），优先于 --year-from")
    ap.add_argument("--date-to", default=None, metavar="YYYY-MM-DD",
                    help="精确发表日期上界（默认今天）")
    ap.add_argument("--safety", action="store_true")
    ap.add_argument("--max", type=int, default=30)
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--out")
    args = ap.parse_args()
    res = fetch(args.topic, args.review_type, args.year_from, args.year_to,
                args.safety, args.max, args.run, args.out, server=args.server,
                date_from=args.date_from, date_to=args.date_to)
    if res and not args.out:
        print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
