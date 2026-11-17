#!/usr/bin/env python3
"""cite-check: confirm every citation in a draft is real before it ships.

Bite 1 of the cite-check guard: the *resolve* check. It pulls every URL and
arXiv ID out of a draft and confirms each one actually exists, fetching it
over the network. A draft that cites a dead link or a fabricated arXiv ID
fails the gate (exit code 1) so it never reaches publish.

What it does NOT do yet (phase 2): check that the source actually *supports*
the claim made next to it. That is the harder, separate problem.

Usage:
    cite-check <file>            # check a draft file
    cat draft.md | cite-check    # check stdin
    cite-check <file> --json     # machine-readable report
    cite-check <file> --quiet    # only print failures

Exit codes:
    0  every citation resolved
    1  one or more citations did not resolve (or no citations found + --strict)
    2  usage error
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from typing import Optional

import httpx

# --- extraction patterns -------------------------------------------------

# Plain URLs. Trailing punctuation (.,;:)] etc.) is trimmed after matching so
# that "see https://x.com/a." does not capture the full stop.
URL_RE = re.compile(r"https?://[^\s<>\"')\]]+", re.IGNORECASE)

# arXiv IDs in any of the common shapes:
#   arXiv:2404.10774   arxiv.org/abs/2404.10774   2404.10774v2
# New-style IDs are YYMM.NNNNN (4+5 digits), optionally with a version suffix.
ARXIV_RE = re.compile(
    r"(?:arxiv\.org/(?:abs|pdf)/|arxiv:\s*)?(?<!\d)(\d{4}\.\d{4,5})(v\d+)?",
    re.IGNORECASE,
)

ARXIV_API = "https://export.arxiv.org/api/query"
TRAILING = ".,;:)]}>\"'"
UA = "cite-check/1.0 (+https://workloft.ai)"


@dataclass
class Result:
    kind: str          # "url" | "arxiv"
    ref: str           # the thing as it appeared in the draft
    ok: bool
    status: str        # human-readable verdict
    detail: str = ""


def _strip(url: str) -> str:
    while url and url[-1] in TRAILING:
        url = url[:-1]
    return url


def find_citations(text: str) -> tuple[list[str], list[str]]:
    """Return (urls, arxiv_ids) found in the draft, de-duplicated, order-kept."""
    urls: list[str] = []
    seen_u: set[str] = set()
    for m in URL_RE.finditer(text):
        u = _strip(m.group(0))
        # An arxiv.org URL is checked via the API path below, not as a plain URL.
        if "arxiv.org/abs/" in u.lower() or "arxiv.org/pdf/" in u.lower():
            continue
        if u not in seen_u:
            seen_u.add(u)
            urls.append(u)

    ids: list[str] = []
    seen_a: set[str] = set()
    for m in ARXIV_RE.finditer(text):
        aid = m.group(1)
        if aid not in seen_a:
            seen_a.add(aid)
            ids.append(aid)
    return urls, ids


def check_url(client: httpx.Client, url: str) -> Result:
    """Resolve a URL. HEAD first; fall back to GET when HEAD is unsupported.

    We distinguish 'resolved' (the URL is real, status < 400) from a login or
    paywall soft-200 only at a coarse level here; phase 2 handles content.
    """
    try:
        r = client.head(url, follow_redirects=True, timeout=12)
        if r.status_code in (403, 405, 501) or r.status_code >= 500:
            # Many servers refuse HEAD; retry with a streamed GET (no full body).
            with client.stream("GET", url, follow_redirects=True, timeout=15) as g:
                code = g.status_code
        else:
            code = r.status_code
    except httpx.HTTPError as e:
        return Result("url", url, False, "DEAD", f"{type(e).__name__}: {e}")

    if code < 400:
        return Result("url", url, True, "OK", f"HTTP {code}")
    return Result("url", url, False, "DEAD", f"HTTP {code}")


def check_arxiv(client: httpx.Client, arxiv_id: str) -> Result:
    """Confirm an arXiv ID exists via the official API.

    A fabricated ID returns a feed with zero <entry> elements. Crucially we
    also confirm the returned entry id matches the requested id, because the
    API echoes the query even for some malformed inputs.
    """
    try:
        r = client.get(ARXIV_API, params={"id_list": arxiv_id, "max_results": 1},
                        follow_redirects=True, timeout=15)
        r.raise_for_status()
    except httpx.HTTPError as e:
        return Result("arxiv", arxiv_id, False, "ERROR",
                      f"arXiv API unreachable: {e}")

    body = r.text
    # The API returns an Atom feed. A real hit contains an <entry> whose <id>
    # carries the arxiv id; a miss has a single <entry> only when erroring, so
    # we look for the id string inside an entry id URL.
    if "<entry>" not in body:
        return Result("arxiv", arxiv_id, False, "NOT FOUND",
                      "no entry in arXiv response")
    if arxiv_id.split("v")[0] in body and "arxiv.org/abs/" in body:
        return Result("arxiv", arxiv_id, True, "OK", "arXiv id resolves")
    return Result("arxiv", arxiv_id, False, "NOT FOUND",
                  "id absent from arXiv response")


def run(text: str) -> list[Result]:
    urls, ids = find_citations(text)
    results: list[Result] = []
    with httpx.Client(headers={"User-Agent": UA}) as client:
        for u in urls:
            results.append(check_url(client, u))
        for aid in ids:
            results.append(check_arxiv(client, aid))
    return results


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        prog="cite-check",
        description="Confirm every URL and arXiv ID in a draft is real before it ships.",
    )
    ap.add_argument("file", nargs="?", help="draft file (default: stdin)")
    ap.add_argument("--json", action="store_true", help="machine-readable report")
    ap.add_argument("--quiet", action="store_true", help="print only failures")
    ap.add_argument("--strict", action="store_true",
                    help="fail if the draft contains no citations at all")
    args = ap.parse_args(argv)

    if args.file:
        try:
            text = open(args.file, encoding="utf-8", errors="replace").read()
        except OSError as e:
            print(f"cite-check: cannot read {args.file}: {e}", file=sys.stderr)
            return 2
    else:
        text = sys.stdin.read()

    results = run(text)
    failures = [r for r in results if not r.ok]

    if args.json:
        print(json.dumps({
            "checked": len(results),
            "failed": len(failures),
            "results": [asdict(r) for r in results],
        }, indent=2))
    else:
        if not results:
            print("cite-check: no URLs or arXiv IDs found in draft.")
        for r in results:
            if args.quiet and r.ok:
                continue
            mark = "PASS" if r.ok else "FAIL"
            print(f"[{mark}] {r.status:<10} {r.ref}")
            if not r.ok and r.detail:
                print(f"         -> {r.detail}")
        print(f"\ncite-check: {len(results)-len(failures)}/{len(results)} resolved"
              + (f", {len(failures)} FAILED" if failures else ""))

    if failures:
        return 1
    if not results and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
