#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
build_guidelines.py — CORPUS BUILDER for the clinical-guideline corpus (G-upgrade).

Run by the skill AUTHOR (build-time; network ALLOWED) to materialize guidelines into the
curated corpus. IMPORTANT division of labour (data-protection design):

  * The skill tree (references/guidelines/) holds ONLY the POINTER INDEX — org / title /
    URL / version metadata. Low-sensitivity, publish-safe.
  * FULL-TEXT documents are NEVER written into the skill. When --download is used they go
    to a LOCAL CACHE OUTSIDE the skill (default ~/.workbuddy/ct-guideline-docs) — a personal
    convenience only. The CANONICAL controlled home for full text is the user's own Coze KB
    (self-controlled; it does NOT travel with the shareable/publishable skill).

    python adapters/build_guidelines.py --topic diabetes --sources OpenAlex,EuropePMC --run
    python adapters/build_guidelines.py --topic "breast cancer" --sources OpenAlex,EuropePMC --run --download

Design:
  * Reuses fetch_guidelines.fetch() (the 13-source adapter library) for api sources.
  * For every portal-only org (NCCN/ADA/AHA/SIGN/CMA/CPIC) it first tries a BUILD-TIME
    lightweight fetch (adapters/portal_fetch.py: CPIC via its real free API; the rest via
    best-effort public-portal scraping). Fetched records are stored as real `api` entries;
    on any failure it falls back to the honest `portal` pointer. Analysis time stays offline.
  * Merges into guidelines_index.json (dedupe by id), pinned with built_at timestamp.

SAFE PREVIEW: --dry-run returns the would-be payload WITHOUT writing files / downloading.
--download is OFF by default: full text is out-of-scope for the skill (use Coze for that).
"""
import argparse
import json
import os
import re
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.dirname(_HERE))
from adapters import fetch_guidelines
from adapters import portal_fetch  # G: BUILD-TIME lightweight fetchers for portal-only orgs

_SKILL_ROOT = os.path.dirname(_HERE)
_DEFAULT_CORPUS = os.path.join(_SKILL_ROOT, "references", "guidelines")
_TOTAL_SOURCES = len(fetch_guidelines.GUIDELINE_SOURCES)
_API_SOURCES = sum(1 for m in fetch_guidelines.GUIDELINE_SOURCES.values() if m["access"] == "api")
_PORTAL_SOURCES = sum(1 for m in fetch_guidelines.GUIDELINE_SOURCES.values() if m["access"] == "portal")
_SCHEMA_VERSION = 1
_MAX_DOC_BYTES = 8_000_000
_MAX_DOCS_PER_BUILD = 40  # safety cap on downloaded documents per build invocation


def _slug(s, maxlen=60):
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "_", s)
    s = s.strip("_")
    return (s[:maxlen] or "item").strip("_")


def _http_text(url, timeout=60, retries=3):
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ct-literature-guideline-builder/0.1"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            last = e
            time.sleep(1.5 * (i + 1))
    return None


def _download_doc(rec, doc_cache_dir, max_bytes=5_000_000):
    """Best-effort OA full-text download into a LOCAL CACHE that lives OUTSIDE this skill.

    Returns absolute file path or None. Full-text documents are the user's curated IP — they
    must NOT ship with the (shareable/publishable) skill, so we never write them under
    references/guidelines/. The canonical controlled home for full text is the user's Coze KB;
    this cache is only a personal convenience on the author's machine. Never aborts the build.
    """
    org = rec.get("guideline_org")
    extra = rec.get("extra") or {}
    url = extra.get("pdf_url") or extra.get("oa_pdf")
    if org != "OpenAlex" or not url:
        return None
    try:
        # use requests (not urllib): this Anaconda/Windows env has no CA bundle for
        # urllib, so urllib raises CERTIFICATE_VERIFY_FAILED; requests works (http_utils
        # already depends on it).
        import requests
        r = requests.get(url, timeout=(10, 40),
                         headers={"User-Agent": "Mozilla/5.0 (ct-literature-guideline-builder)"})
        if r.status_code != 200:
            return None
        data = r.content
        ctype = (r.headers.get("Content-Type") or "").lower()
        if not data or len(data) > max_bytes:
            return None
        # a tiny html body is almost certainly an error/redirect page, not a PDF
        if "html" in ctype and len(data) < 8000:
            return None
        os.makedirs(doc_cache_dir, exist_ok=True)
        sub = os.path.join(doc_cache_dir, _slug(org))
        os.makedirs(sub, exist_ok=True)
        fid = _slug(rec.get("title"))[:60] or _slug(extra.get("doi", ""))
        path = os.path.join(sub, "%s.pdf" % fid)
        with open(path, "wb") as f:
            f.write(data)
        return os.path.abspath(path)
    except Exception:
        return None


def _derive_id(rec):
    extra = rec.get("extra") or {}
    org = rec.get("guideline_org")
    if rec.get("access") == "portal":
        # portal pointers share org_url across topics -> include topic for uniqueness
        return "%s:%s:%s" % (org, _slug(rec.get("topic") or ""), _slug(rec.get("title")))
    for k in ("doi", "pmid", "pmcid", "url"):
        v = extra.get(k) or rec.get(k)
        if v:
            return "%s:%s" % (org, _slug(str(v)))
    return "%s:%s" % (org, _slug(rec.get("title")))


def build(topic, sources=None, corpus_dir=None, max_results=30, run=False,
          download=False, doc_cache_dir=None, dry_run=False, year_from=None, year_to=None):
    """Build / refresh the guideline corpus for `topic`.

    Returns the payload that would be written (dict). With dry_run=True nothing is written
    and no network/download happens (SAFE PREVIEW). Full-text download (--download) is OFF
    by default: documents go to a LOCAL CACHE OUTSIDE the skill, never into references/
    guidelines/, so the skill tree stays pointer-only and publish-safe.
    """
    corpus_dir = corpus_dir or _DEFAULT_CORPUS

    if not run:
        print("[PREVIEW] would build guideline corpus for topic=%r (use --run to execute network + write)"
              % topic)
        return None

    if download:
        print("[WARN] Full-text documents will be written to a LOCAL CACHE OUTSIDE this skill "
              "(default %s). These docs are NOT part of ct-literature and MUST NOT be published. "
              "Preferred controlled home for full text: your Coze KB."
              % os.path.expanduser("~/.workbuddy/ct-guideline-docs"))

    # 1) api records from the source library
    api_srcs = [s for s in (sources or list(fetch_guidelines.GUIDELINE_SOURCES.keys()))
                if fetch_guidelines.GUIDELINE_SOURCES.get(s, {}).get("access") == "api"]
    payload = fetch_guidelines.fetch(topic, review_type="all", year_from=year_from, year_to=year_to,
                                     max_results=max_results, run=True, sources=api_srcs)
    records = list(payload.get("works", [])) if payload else []

    # 2) portal orgs: BUILD-TIME lightweight fetch; graceful fall back to honest pointer
    portal_orgs = [o for o, m in fetch_guidelines.GUIDELINE_SOURCES.items() if m["access"] == "portal"]
    portal_status = {}
    for org in portal_orgs:
        try:
            fetched = portal_fetch.fetch_portal(org, topic, max_results=min(10, max_results))
        except Exception:
            fetched = []
        if fetched:
            records += fetched
            portal_status[org] = {"access": "portal", "status": "fetched", "count": len(fetched)}
        else:
            records += fetch_guidelines._portal_pointers(topic, [org])
            portal_status[org] = {"access": "portal", "status": "pointer", "count": 1}

    # 3) assemble entries (id, file download, topic_tags)
    entries = []
    docs_downloaded = 0
    for rec in records:
        org = rec.get("guideline_org")
        entry = dict(rec)  # keep _normalize shape (source/guideline_org/access/retrieved/...)
        entry["id"] = _derive_id(rec)
        entry["version"] = None
        entry["date"] = rec.get("update_date")
        entry["topic_tags"] = [_slug(topic)]
        entry["file"] = None
        if download and docs_downloaded < _MAX_DOCS_PER_BUILD:
            cache = doc_cache_dir or os.path.expanduser("~/.workbuddy/ct-guideline-docs")
            rel = _download_doc(rec, cache)
            if rel:
                entry["file"] = rel
                entry["retrieved"] = True
                docs_downloaded += 1
        entries.append(entry)

    # merge portal build-time status into the aggregate source_status
    source_status = {}
    if payload:
        source_status.update(payload.get("source_status", {}))
    source_status.update(portal_status)

    if dry_run:
        print("[DRY-RUN] %d entries would be written (no files / no network side-effects)" % len(entries))
        return {"source": "Guidelines", "query": topic, "count": len(entries),
                "works": entries, "source_status": source_status,
                "docs_downloaded": docs_downloaded, "dry_run": True}

    # 4) merge with existing index (dedupe by id)
    os.makedirs(corpus_dir, exist_ok=True)
    index_path = os.path.join(corpus_dir, "guidelines_index.json")
    existing = []
    if os.path.isfile(index_path):
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                existing = json.load(f).get("entries", [])
        except Exception:
            existing = []
    seen = set(e.get("id") for e in existing)
    added = 0
    for e in entries:
        if e["id"] in seen:
            continue
        existing.append(e)
        seen.add(e["id"])
        added += 1

    index = {
        "schema_version": _SCHEMA_VERSION,
        "built_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "built_by": "build_guidelines.py",
        "corpus_dir": os.path.relpath(corpus_dir, _SKILL_ROOT),
        "total_sources": _TOTAL_SOURCES,
        "api_sources": _API_SOURCES,
        "portal_sources": _PORTAL_SOURCES,
        "entries": existing,
    }
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print("[OK] guideline corpus built: %d entries total (%d added this run, %d docs downloaded) -> %s"
          % (len(existing), added, docs_downloaded, index_path))
    return {"source": "Guidelines", "query": topic, "count": len(existing),
            "added": added, "docs_downloaded": docs_downloaded,
            "source_status": source_status,
            "index": index_path}


def main():
    ap = argparse.ArgumentParser(description="Build the curated clinical-guideline corpus (network, build-time).")
    ap.add_argument("--topic", required=True, help="disease / drug / topic")
    ap.add_argument("--sources", help="comma-separated api-source subset (default: all api sources)")
    ap.add_argument("--max", type=int, default=30, help="max records per api source")
    ap.add_argument("--year-from", type=int)
    ap.add_argument("--year-to", type=int)
    ap.add_argument("--corpus-dir", help="override corpus (pointer index) directory")
    ap.add_argument("--download", action="store_true",
                    help="download OA full texts into a LOCAL CACHE OUTSIDE the skill (opt-in; "
                         "off by default). Full text is NOT part of the skill — use your Coze KB "
                         "as the controlled home.")
    ap.add_argument("--doc-cache-dir", help="override the local full-text cache directory "
                                            "(default: ~/.workbuddy/ct-guideline-docs)")
    ap.add_argument("--dry-run", action="store_true", help="SAFE PREVIEW: no write, no download")
    ap.add_argument("--run", action="store_true", help="execute network requests + write index")
    args = ap.parse_args()
    srcs = [s.strip() for s in args.sources.split(",")] if args.sources else None
    build(args.topic, sources=srcs, corpus_dir=args.corpus_dir, max_results=args.max,
          run=args.run, download=args.download, doc_cache_dir=args.doc_cache_dir,
          dry_run=args.dry_run, year_from=args.year_from, year_to=args.year_to)


if __name__ == "__main__":
    main()
