#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fetch_arxiv.py — arXiv fetcher (physical/CS/preprint breadth source).

Reads the arXiv API (https://export.arxiv.org/api/query) — a free, keyless
Atom XML feed covering physics, mathematics, CS, quantitative biology,
statistics, etc. For clinical-trial evidence it is mostly *breadth* (methodology,
ML-for-health, biostatistics), not core RCT/safety literature — so it is wired as
an OPT-IN supplementary source (like Semantic Scholar), not default-on.

No key required. arXiv asks for <=1 request / 3 seconds; this fetcher issues a
single batched request per call, so polite-pool behaviour is preserved.

Zero confidential data or information input; reads only public literature.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from adapters import http_utils  # shared UA + key loaders (no key needed here, reused for consistency)

BASE = "https://export.arxiv.org/api/query"

ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV_NS = "{http://arxiv.org/schemas/atom}"

SAFETY_LEXICON = [
    "adverse event", "adverse reaction", "side effect", "safety", "toxicity",
    "toxic", "case report", "pharmacovigilance", "drug-induced", "drug reaction",
]

# arXiv categories that are clinically / biomedically relevant (used to flag
# relevance, not to restrict the search — we search broadly then tag).
BIOMED_CATS = {
    "q-bio", "stat", "cs.LG", "cs.AI", "cs.CV", "cs.CL", "eess", "math",
}


def _strip_ws(s):
    if not s:
        return ""
    return re.sub(r"\s+", " ", s).strip()


def _study_type_from(title, abstract):
    blob = ((title or "") + " " + (abstract or "")).lower()
    if "systematic review" in blob or "meta-analysis" in blob or "meta analysis" in blob:
        return "systematic-review"
    if "case report" in blob or "case series" in blob:
        return "case-report"
    if "randomized controlled trial" in blob or ("randomized" in blob and "trial" in blob):
        return "rct"
    return "preprint"


def _flag_safety(title, abstract):
    blob = ((title or "") + " " + (abstract or "")).lower()
    return any(k in blob for k in SAFETY_LEXICON)


def _get_xml(url, timeout=60, max_retries=4, backoff=2.0):
    """GET `url` and return parsed XML root, with the same backoff policy as
    http_utils.get_json (429/5xx/connection errors retry; 4xx non-retryable)."""
    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": http_utils.UA})
            r = urllib.request.urlopen(req, timeout=timeout)
            raw = r.read()
            return ET.fromstring(raw)
        except urllib.error.HTTPError as e:
            if e.code == 429 or 500 <= e.code < 600:
                wait = float(e.headers.get("Retry-After", backoff ** (attempt - 1)))
                print("[WARN] arXiv HTTP %s (attempt %d/%d) -> retry in %.1fs"
                      % (e.code, attempt, max_retries, wait))
                if attempt < max_retries:
                    time.sleep(wait)
                    continue
                raise http_utils.HttpError("HTTP %s after %d retries" % (e.code, max_retries),
                                           status=e.code, retryable=True)
            raise http_utils.HttpError("HTTP %s (non-retryable)" % e.code,
                                       status=e.code, retryable=False)
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            wait = backoff ** (attempt - 1)
            print("[WARN] arXiv request error (attempt %d/%d): %s -> retry in %.1fs"
                  % (attempt, max_retries, e, wait))
            if attempt < max_retries:
                time.sleep(wait)
                continue
            raise http_utils.HttpError("request failed after %d retries: %s" % (max_retries, e),
                                       retryable=True)
    raise http_utils.HttpError("unreachable retry loop", retryable=True)


def _extract_entry(entry):
    """Parse one <entry> Element into the unified work schema."""
    def txt(tag, ns=ATOM):
        el = entry.find(ns + tag)
        return el.text if el is not None else None

    def txt_arxiv(tag):
        el = entry.find(ARXIV_NS + tag)
        return el.text if el is not None else None

    arxiv_id_url = txt("id") or ""
    # id looks like "http://arxiv.org/abs/2606.11144v1"
    m = re.search(r"abs/([^ ]+)", arxiv_id_url)
    arxiv_id = m.group(1) if m else arxiv_id_url

    title = _strip_ws(txt("title"))
    abstract = _strip_ws(txt("summary"))

    authors = []
    for a in entry.findall(ATOM + "author"):
        nm = a.find(ATOM + "name")
        if nm is not None and nm.text:
            authors.append(nm.text.strip())
    if len(authors) > 6:
        authors = authors[:6] + ["et al."]

    # Links: alternate = abstract page; related (title=pdf) = PDF
    url = None
    pdf_url = None
    for link in entry.findall(ATOM + "link"):
        rel = link.get("rel")
        ltype = link.get("type")
        href = link.get("href")
        if rel == "alternate" and url is None:
            url = href
        if ltype == "application/pdf":
            pdf_url = href
    if not url:
        url = arxiv_id_url

    # Dates
    published = txt("published") or txt("updated") or ""
    year = None
    ym = re.match(r"(\d{4})", published or "")
    if ym:
        year = int(ym.group(1))

    # arXiv categories -> concepts (for relevance enrichment)
    cats = []
    for c in entry.findall(ATOM + "category"):
        term = c.get("term")
        if term:
            cats.append(term)
    primary = entry.find(ARXIV_NS + "primary_category")
    if primary is not None and primary.get("term"):
        pt = primary.get("term")
        if pt not in cats:
            cats.insert(0, pt)

    doi = txt_arxiv("doi")

    return {
        "source": "arXiv",
        "id": arxiv_id,
        "doi": doi,
        "pmid": None,
        "pmcid": None,
        "title": title,
        "authors": authors or None,
        "year": year,
        "publication_date": published or None,
        "publication": "arXiv",
        "journal_iso": "arXiv",
        "type": "preprint",
        "study_type": _study_type_from(title, abstract),
        "cited_by_count": 0,  # arXiv API has no citation count
        "url": url,
        "open_access_url": pdf_url,
        "abstract_snippet": abstract or "",
        "mesh": None,
        "concepts": cats[:6] or None,
        "keywords": None,
        "is_safety": _flag_safety(title, abstract),
        "is_preprint": True,
        "volume": None,
        "issue": None,
        "page": None,
    }


def fetch(topic, review_type="all", year_from=None, year_to=None,
          safety=False, max_results=30, run=False, out=None):
    if not run:
        print("[PREVIEW] would query arXiv for topic=%r (opt-in supplementary source)"
              % topic)
        return None

    q = "all:" + _quote_arxiv(topic)
    if review_type in ("systematic-review", "meta-analysis", "scoping-review"):
        q += " AND all:\"systematic review\""
    elif review_type == "rct":
        q += " AND all:\"randomized controlled trial\""
    elif review_type == "case-report":
        q += " AND all:\"case report\""
    if safety:
        q += " AND all:\"adverse event\""

    params = {
        "search_query": q,
        "start": 0,
        "max_results": min(max_results, 50),
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    if year_from or year_to:
        lo = str(year_from) if year_from else "1900"
        hi = str(year_to) if year_to else "3000"
        params["filter"] = "submittedDate:[%s0101 TO %s1231]" % (lo, hi)

    url = BASE + "?" + urllib.parse.urlencode(params)
    try:
        root = _get_xml(url, timeout=60, max_retries=4)
    except http_utils.HttpError as e:
        print("[WARN] arXiv request failed: %s" % e)
        empty = _empty(topic)
        if out:
            _write(out, empty)
        return empty

    collected = []
    for entry in root.findall(ATOM + "entry"):
        # arXiv API sometimes returns a <entry> with no title on error responses
        if entry.find(ATOM + "title") is None:
            continue
        collected.append(_extract_entry(entry))

    payload = {
        "source": "arXiv",
        "query": q,
        "review_type": review_type,
        "year_from": year_from,
        "year_to": year_to,
        "safety": safety,
        "count": len(collected),
        "works": collected,
    }
    if out:
        _write(out, payload)
    return payload


def _quote_arxiv(s):
    """Wrap a free-text phrase so arXiv treats it as a phrase (AND of words)."""
    s = (s or "").strip()
    # Remove characters that break the query; keep alphanumerics + spaces.
    s = re.sub(r"[^\w\s\-]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return '"%s"' % s if s else "all:electron"


def _write(out, payload):
    try:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print("[OK] arXiv wrote %d works -> %s" % (payload["count"], out))
    except OSError as werr:
        print("[WARN] could not write arXiv payload: %s" % werr)


def _empty(topic):
    return {"source": "arXiv", "query": topic, "count": 0, "works": []}


def main():
    ap = argparse.ArgumentParser(description="Fetch literature via arXiv (keyless, opt-in).")
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
