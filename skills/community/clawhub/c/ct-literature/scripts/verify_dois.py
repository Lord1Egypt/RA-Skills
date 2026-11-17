#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""verify_dois.py — DOI-focused citation audit for ct-literature.

Standalone DOI verification pass over an existing `.merged.json` (or any JSON with a
``works`` list). For every work carrying a DOI it:

  1. resolves the DOI (https://doi.org/<doi>, 2xx after redirects);
  2. fetches the DOI's canonical metadata from Crossref and fuzzy-matches the title +
     first-author surname against the work we hold;
  3. writes the additive ``doi_verified`` (bool) / ``doi_mismatch`` (bool) /
     ``doi_mismatch_note`` fields back onto each work.

It then emits ``doi_mismatch.md`` — a human-review list that isolates the
real-but-wrong / hallucinated-DOI case behind the ct-literature error-table entry
"DOI dedupe merged too aggressively / shared DOI typo".

SAFE PREVIEW: the pass is a NO-OP without ``--run`` (no network, no write) — it only
prints how many works carry a DOI. All outbound HTTP lives in
``adapters/verify_citations.py`` (ct-base §16.9 outbound-call confinement); this script
is a thin CLI + reporter and never issues a request itself.
"""
import argparse
import json
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adapters import verify_citations  # noqa: E402


def run_pass(works, timeout=15, progress=None):
    """Annotate every work in-place with the additive doi_* fields. Returns a summary.

    Parallelized with a bounded thread pool: each work is verified by exactly one
    thread (no shared work object), so in-place annotation is safe — only the shared
    ``summary`` accumulator is guarded by a lock. The upstream network layer already
    caps per-host concurrency, so this will not hammer Crossref / Europe PMC / OpenAlex.
    """
    summary = {"total": len(works), "with_doi": 0, "doi_verified": 0,
               "doi_mismatch": 0, "unresolved": 0, "no_doi": 0}
    n = len(works)
    if not n:
        return summary

    _lock = threading.Lock()
    _done = [0]

    def _verify_at(i, w):
        if not w.get("doi"):
            w.update({"doi": None, "doi_checked": False, "doi_verified": False,
                      "doi_mismatch": False, "doi_mismatch_note": "no DOI on this work"})
            return "no_doi"
        res = verify_citations.verify_doi_only(w, timeout=timeout)
        w.update(res)
        if res.get("doi_mismatch"):
            return "doi_mismatch"
        if res.get("doi_verified"):
            return "doi_verified"
        return "unresolved"

    with ThreadPoolExecutor(max_workers=min(8, n)) as _ex:
        _futs = {_ex.submit(_verify_at, i, w): i for i, w in enumerate(works)}
        for _f in as_completed(_futs):
            cat = _f.result()
            with _lock:
                if cat == "no_doi":
                    summary["no_doi"] += 1
                else:
                    summary["with_doi"] += 1
                    if cat == "doi_mismatch":
                        summary["doi_mismatch"] += 1
                    elif cat == "doi_verified":
                        summary["doi_verified"] += 1
                    else:
                        summary["unresolved"] += 1
                _done[0] += 1
                if progress:
                    progress(_done[0], n)
    return summary


def main():
    ap = argparse.ArgumentParser(
        description="DOI-focused citation audit (offline-safe preview; --run for network).")
    ap.add_argument("--in", default=".merged.json", dest="inp",
                    help="input JSON with a 'works' list (default .merged.json)")
    ap.add_argument("--run", action="store_true",
                    help="perform the live DOI pass (default: dry-run, no network/write)")
    ap.add_argument("--out-dir", default=None,
                    help="where to write doi_mismatch.md (default: the input's directory)")
    ap.add_argument("--timeout", type=int, default=15)
    args = ap.parse_args()

    if not os.path.isfile(args.inp):
        print("[ERR] input not found: %s" % args.inp)
        sys.exit(2)
    data = json.load(open(args.inp, encoding="utf-8"))
    works = data.get("works", [])
    n_doi = sum(1 for w in works if w.get("doi"))

    print("[doi] %d works; %d carry a DOI" % (len(works), n_doi))
    if not args.run:
        print("[SAFE PREVIEW] dry-run — no network, nothing written. "
              "Re-run with --run to perform the DOI audit.")
        return

    summary = run_pass(works, timeout=args.timeout)
    data["works"] = works
    with open(args.inp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("[OK] doi fields written back -> %s" % args.inp)

    out_dir = args.out_dir or os.path.dirname(os.path.abspath(args.inp))
    report = verify_citations.render_doi_mismatch_report(
        works, topic=(data.get("meta") or {}).get("topic"))
    rp = os.path.join(out_dir, "doi_mismatch.md")
    with open(rp, "w", encoding="utf-8") as f:
        f.write(report)
    print("[OK] doi mismatch report -> %s" % rp)
    print("[doi] summary: %s" % json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
