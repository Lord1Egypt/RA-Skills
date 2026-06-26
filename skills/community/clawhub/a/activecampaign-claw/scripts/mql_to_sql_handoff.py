#!/usr/bin/env python3
"""
mql_to_sql_handoff.py — MQL→SQL handoff diagnostics.

Contacts whose lead score crossed a threshold in last N days, joined to
deals created for them. Surfaces which got a deal (handoff worked), which
didn't (sales miss), which deals were created without scoring (off-script).

Requires the Deals feature on the AC account.

Usage:
  python3 mql_to_sql_handoff.py --threshold 50 --days 7
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from _ac_client import ACClient, ACClientError, render_feature_unavailable
from _ac_client import safe_float as _safe_float


def _parse_iso(s):
    if not s:
        return None
    try:
        dt = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


def fetch(client: ACClient) -> dict:
    contacts = client.paginate("contacts", "contacts", max_items=20000)
    # AC v3: per-contact score values are at /scoreValues, not /contactScoreValues
    try:
        scores = client.paginate("scoreValues", "scoreValues", max_items=50000)
    except ACClientError as e:
        if e.status_code in (403, 404):
            scores = []
        else:
            raise
    try:
        deals = client.paginate("deals", "deals", max_items=20000)
    except ACClientError as e:
        if e.status_code == 403:
            return {"unavailable": True}
        raise
    return {"contacts": contacts, "scores": scores, "deals": deals}


def analyze(data: dict, threshold: float, days: int) -> dict:
    if data.get("unavailable"):
        return {"unavailable": True}
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    crossed = {}  # contact_id -> max_score in window
    for s in data["scores"]:
        ts = _parse_iso(s.get("mdate") or s.get("cdate"))
        if not ts or ts < cutoff:
            continue
        sc = _safe_float(s.get("scoreValue"))
        if sc < threshold:
            continue
        cid = str(s.get("contact"))
        if cid:
            crossed[cid] = max(crossed.get(cid, 0), sc)

    deal_by_contact = {}
    deals_in_window_no_score = []
    for d in data["deals"]:
        cd = _parse_iso(d.get("cdate"))
        if not cd or cd < cutoff:
            continue
        cid = str(d.get("contact"))
        deal_by_contact[cid] = d
        if cid not in crossed:
            deals_in_window_no_score.append({"deal_id": d.get("id"), "contact": cid, "value": d.get("value")})

    handoff_success = []
    handoff_miss = []
    for cid, score in crossed.items():
        if cid in deal_by_contact:
            handoff_success.append({"contact": cid, "score": score, "deal_id": deal_by_contact[cid].get("id")})
        else:
            handoff_miss.append({"contact": cid, "score": score})

    return {
        "threshold": threshold,
        "window_days": days,
        "contacts_crossed_threshold": len(crossed),
        "handoff_success": handoff_success,
        "handoff_miss": handoff_miss,
        "deals_no_scoring": deals_in_window_no_score,
    }


def render_markdown(r: dict) -> str:
    if r.get("unavailable"):
        return render_feature_unavailable(
            "Deals (CRM)", "Plus",
            "MQL→SQL handoff diagnostics need the /deals endpoint.",
        )
    lines = [
        f"# MQL→SQL Handoff (last {r['window_days']} days, score ≥ {r['threshold']})",
        "",
        f"- Contacts crossed threshold: {r['contacts_crossed_threshold']}",
        f"- Handoff success (got a deal): **{len(r['handoff_success'])}**",
        f"- Handoff miss (no deal): **{len(r['handoff_miss'])}**",
        f"- Deals created without scoring (rep off-script): **{len(r['deals_no_scoring'])}**",
        "",
    ]
    if r["handoff_miss"]:
        lines.append("## Handoff misses")
        for x in r["handoff_miss"][:50]:
            lines.append(f"- contact {x['contact']} — score {x['score']}")
        lines.append("")
    if r["deals_no_scoring"]:
        lines.append("## Deals without prior scoring")
        for x in r["deals_no_scoring"][:50]:
            lines.append(f"- deal {x['deal_id']} (contact {x['contact']}, value {x['value']})")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="MQL/SQL handoff")
    parser.add_argument("--threshold", type=float, default=50)
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    client = ACClient()
    data = fetch(client)
    r = analyze(data, args.threshold, args.days)
    out = json.dumps(r, indent=2) if args.format == "json" else render_markdown(r)
    if args.output:
        Path(args.output).write_text(out)
        print(f"Wrote {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()
