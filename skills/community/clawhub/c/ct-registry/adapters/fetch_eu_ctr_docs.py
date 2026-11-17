#!/usr/bin/env python3
"""fetch_eu_ctr_docs.py - Enrich EU-CTR records with downloadable document URLs.

Why (ct-registry 2026-07-28, v0.3.0)
-------------------------------------
The user wants "downloadable detailed documents" surfaced as links, and downloaded
only after explicit confirmation. Reality check (verified against cde_detail.json):
CDE's external-workflow detail returns **NO attachment URLs** (0 http(s) links, 0
附件/下载 fields) -- so CDE PDFs can only be fetched manually from the CDE site
(behind SafeDog WAF). EU CTR is the realistic automatable source: the EU CTIS
public retrieve API exposes a per-trial dossier that includes a documents list
with signed download URLs (protocol / IB / CSR synopsis / ...).

This script takes the EU-CTR search output (search_eu_ctr.py -> euctr.json; each
record carries `ctNumber`) and, for each record, queries the EU CTIS public
retrieve API to extract document URLs, attaching them as `documents` to the
record. Output keeps the SAME shape (source=EUCTR, records[...documents]) so it
can be fed straight into normalize.py.

CAVEAT (needs live validation): search_eu_ctr.py returns LEGACY EudraCT numbers
(YYYY-NNNNNN-NN). The CTIS retrieve API keys on CTIS numbers (EUCTIS...). If a
legacy number is not directly accepted, the call returns no documents -- we then
leave `documents` empty and surface a note. A EudraCT->CTIS mapping step may be
required; left as a follow-up. Treat this module as best-effort until validated
against the live CTIS API.

Safety: read-only public GET; --run required to actually fetch (default preview).
"""
import argparse
import json
import urllib.parse
import urllib.request

CTIS_RETRIEVE = "https://euclinicaltrials.eu/ctis-public-api/retrieve/{ctNumber}"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)", "Accept": "application/json"}

# Candidate locations of a document list inside the CTIS retrieve JSON.
_DOC_KEYS = ["documents", "documentList", "documentSummaryList", "results", "content"]
_URL_KEYS = ["documentUrl", "url", "downloadUrl", "documentURL"]
_TYPE_KEYS = ["documentType", "type", "documentKind"]
_TITLE_KEYS = ["documentTitle", "title", "name", "fileName"]


def _first(d, keys):
    for k in keys:
        if k in d and d[k]:
            return d[k]
    return None


def _extract_docs(obj, _seen=None):
    """Find a list of document dicts anywhere in the CTIS JSON (tolerant of nesting)."""
    if _seen is None:
        _seen = set()
    if isinstance(obj, dict):
        for k in _DOC_KEYS:
            v = obj.get(k)
            if isinstance(v, list) and v and isinstance(v[0], dict):
                return v
        for v in obj.values():
            if isinstance(v, (dict, list)):
                r = _extract_docs(v, _seen)
                if r:
                    return r
    return None


def _doc_entry(e):
    url = _first(e, _URL_KEYS)
    if not url:
        return None
    return {
        "title": _first(e, _TITLE_KEYS) or "document",
        "type": _first(e, _TYPE_KEYS) or "",
        "url": url,
    }


def fetch_docs(ct_number, timeout=40):
    url = CTIS_RETRIEVE.format(ctNumber=ct_number)
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8", "replace"))
    except Exception as e:  # noqa: BLE001 - best-effort; degrade gracefully
        return [], "request failed: %s" % e
    docs = _extract_docs(data)
    if not docs:
        return [], "no document list in CTIS response (legacy EudraCT number may need mapping)"
    out = []
    for e in docs:
        d = _doc_entry(e)
        if d:
            out.append(d)
    return out, None


def main():
    ap = argparse.ArgumentParser(
        description="Enrich EU-CTR records with document download URLs (best-effort).")
    ap.add_argument("--in", dest="inp", required=True, help="EU-CTR search output (euctr.json)")
    ap.add_argument("--out", default="euctr_docs.json")
    ap.add_argument("--max", type=int, default=0, help="max records to enrich (0=all)")
    ap.add_argument("--run", action="store_true", help="actually fetch (default preview)")
    args = ap.parse_args()

    with open(args.inp, encoding="utf-8") as f:
        data = json.load(f)
    records = data.get("records") or []

    if not args.run:
        print("[eu_ctr_docs][PREVIEW] would enrich %d EU-CTR records via CTIS retrieve "
              "API. Add --run to fetch." % len(records))
        return

    enriched = []
    total_docs = 0
    for i, rec in enumerate(records):
        ct = rec.get("ctNumber")
        docs = []
        if ct:
            docs, err = fetch_docs(ct)
            if err:
                print("[eu_ctr_docs] %s: %s" % (ct, err))
            else:
                total_docs += len(docs)
        r = dict(rec)
        r["documents"] = docs
        enriched.append(r)
        if args.max and i + 1 >= args.max:
            break

    out = dict(data)
    out["records"] = enriched
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("[eu_ctr_docs] enriched %d records, %d document links -> %s"
          % (len(enriched), total_docs, args.out))


if __name__ == "__main__":
    main()
