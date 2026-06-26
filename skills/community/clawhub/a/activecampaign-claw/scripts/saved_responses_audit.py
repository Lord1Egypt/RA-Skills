#!/usr/bin/env python3
"""
saved_responses_audit.py — Inventory of sales-rep saved-response templates.

Pulls /savedResponses (Plus+ feature) and reports on the library:

  - total saved responses, last-modified distribution
  - stale entries (last touched > N days ago)
  - very short / very long entries (likely placeholders or runaway HTML)
  - near-duplicate detection (token-overlap on the body) — pairs whose
    word sets overlap >= --duplicate-threshold (default 0.85)

Note: AC v3 does NOT expose per-rep usage of saved responses, so this
script audits the library content but cannot tell you who's using what.
That signal lives in the UI/inbox only.

Usage:
  python3 saved_responses_audit.py
  python3 saved_responses_audit.py --stale-days 365
  python3 saved_responses_audit.py --format json --output sr_audit.json
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from _ac_client import ACClient, ACClientError, emit_files, render_feature_unavailable
from _ac_client import parse_date as _parse_date

_HTML_TAG = re.compile(r"<[^>]+>")
_WORD = re.compile(r"[a-zA-Z][a-zA-Z'-]{2,}")


def _body_text(html: str | None) -> str:
    if not html:
        return ""
    return _HTML_TAG.sub(" ", html)


def _wordset(text: str) -> set[str]:
    return {w.lower() for w in _WORD.findall(text)}


def fetch_data(client: ACClient) -> dict:
    try:
        responses = client.paginate("savedResponses", "savedResponses", max_items=2000)
        return {"responses": responses, "unavailable": False}
    except ACClientError as e:
        if e.status_code == 403:
            return {"responses": [], "unavailable": True}
        raise


def analyze(data: dict, stale_days: int = 365, duplicate_threshold: float = 0.85,
            now: datetime | None = None) -> dict:
    if data.get("unavailable"):
        return {"unavailable": True}
    now = now or datetime.now(timezone.utc)
    rows = []
    for r in data["responses"]:
        body = r.get("body") or ""
        text = _body_text(body)
        last_mod = _parse_date(r.get("mdate") or r.get("cdate"))
        days_since = (now - last_mod).days if last_mod else None
        rows.append({
            "id": r["id"],
            "title": r.get("title", ""),
            "body_len": len(text),
            "html_len": len(body),
            "days_since_modified": days_since,
            "wordset": _wordset(text),
        })

    stale = [r for r in rows if r["days_since_modified"] is not None and r["days_since_modified"] >= stale_days]
    too_short = [r for r in rows if 0 < r["body_len"] < 50]
    too_long = [r for r in rows if r["body_len"] > 8000]

    # near-duplicate detection: jaccard >= threshold
    duplicates = []
    n = len(rows)
    for i in range(n):
        for j in range(i + 1, n):
            a, b = rows[i]["wordset"], rows[j]["wordset"]
            if not a or not b:
                continue
            inter = len(a & b)
            union = len(a | b)
            if union == 0:
                continue
            jac = inter / union
            if jac >= duplicate_threshold:
                duplicates.append({
                    "a_id": rows[i]["id"], "a_title": rows[i]["title"],
                    "b_id": rows[j]["id"], "b_title": rows[j]["title"],
                    "jaccard": round(jac, 3),
                })
    duplicates.sort(key=lambda x: -x["jaccard"])

    # strip wordset before returning (not JSON serializable as a set)
    for r in rows:
        r.pop("wordset", None)

    return {
        "unavailable": False,
        "total": len(rows),
        "stale": stale,
        "too_short": too_short,
        "too_long": too_long,
        "duplicates": duplicates[:25],
        "responses": rows,
        "stale_days_threshold": stale_days,
    }


def render_markdown(r: dict) -> str:
    if r.get("unavailable"):
        return render_feature_unavailable(
            "Saved Responses (CRM)", "Plus",
            "Saved-responses audit needs the /savedResponses endpoint.",
        )
    lines = [
        "# Saved Responses Audit",
        "",
        f"- Total: **{r['total']}**",
        f"- Stale (>={r['stale_days_threshold']}d since last edit): **{len(r['stale'])}**",
        f"- Suspiciously short (<50 chars body): **{len(r['too_short'])}**",
        f"- Very long (>8000 chars body): **{len(r['too_long'])}**",
        f"- Near-duplicate pairs (jaccard ≥ threshold): **{len(r['duplicates'])}**",
        "",
    ]
    if r["stale"]:
        lines.append("## Stale entries")
        lines.append("")
        for s in r["stale"][:20]:
            lines.append(f"- `{s['title']}` (id={s['id']}) — last edit {s['days_since_modified']}d ago")
        lines.append("")
    if r["duplicates"]:
        lines.append("## Likely duplicates")
        lines.append("")
        for d in r["duplicates"][:15]:
            lines.append(
                f"- `{d['a_title']}` ⇔ `{d['b_title']}` — jaccard={d['jaccard']}"
            )
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Audit saved responses library")
    parser.add_argument("--stale-days", type=int, default=365)
    parser.add_argument("--duplicate-threshold", type=float, default=0.85)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    client = ACClient()
    data = fetch_data(client)
    report = analyze(data, stale_days=args.stale_days,
                     duplicate_threshold=args.duplicate_threshold)
    out = json.dumps(report, indent=2, default=str) if args.format == "json" else render_markdown(report)

    if args.output:
        path = Path(args.output)
        path.write_text(out)
        print(f"Wrote {path}")
        emit_files(path)
    else:
        print(out)


if __name__ == "__main__":
    main()
