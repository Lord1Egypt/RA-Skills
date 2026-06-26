#!/usr/bin/env python3
"""
win_loss_report.py — Closed-won vs. closed-lost by source.

Groups closed deals by contact's source list/tag, computes win-rate, avg deal
size, avg cycle length per source.

Requires the Deals feature on the AC account.

Usage:
  python3 win_loss_report.py --days 90
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean

from _ac_client import ACClient, ACClientError, render_feature_unavailable
from _ac_client import safe_int as _safe_int


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


def fetch(client: ACClient, days: int) -> dict:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    try:
        deals = client.paginate("deals", "deals", max_items=20000)
    except ACClientError as e:
        if e.status_code == 403:
            return {"unavailable": True}
        raise
    closed = []
    for d in deals:
        # status: 1=open, 2=won, 3=lost
        if str(d.get("status")) not in ("2", "3"):
            continue
        edate = _parse_iso(d.get("edate") or d.get("mdate"))
        if edate and edate >= cutoff:
            closed.append(d)
    contact_lists = client.paginate("contactLists", "contactLists", max_items=50000)
    return {"deals": closed, "contact_lists": contact_lists, "cutoff": cutoff}


def analyze(data: dict) -> dict:
    if data.get("unavailable"):
        return {"unavailable": True}
    contact_to_lists = defaultdict(list)
    for cl in data["contact_lists"]:
        if str(cl.get("status")) == "1":
            contact_to_lists[str(cl.get("contact"))].append(str(cl.get("list")))

    by_list = defaultdict(lambda: {"won": [], "lost": []})
    won_total = 0
    lost_total = 0
    won_value = 0
    lost_value = 0
    cycle_lengths = []
    for d in data["deals"]:
        cid = str(d.get("contact"))
        status = str(d.get("status"))
        value = _safe_int(d.get("value"))
        cdate = _parse_iso(d.get("cdate"))
        edate = _parse_iso(d.get("edate") or d.get("mdate"))
        cycle = (edate - cdate).total_seconds() / 86400 if (cdate and edate) else None
        if cycle is not None:
            cycle_lengths.append(cycle)
        for lid in contact_to_lists.get(cid, []) or ["(no list)"]:
            if status == "2":
                by_list[lid]["won"].append(value)
            else:
                by_list[lid]["lost"].append(value)
        if status == "2":
            won_total += 1
            won_value += value
        else:
            lost_total += 1
            lost_value += value

    rows = []
    for lid, b in by_list.items():
        w, lost_n = len(b["won"]), len(b["lost"])
        total = w + lost_n
        rows.append({
            "list": lid,
            "won": w,
            "lost": lost_n,
            "win_rate": (w / total) if total else 0,
            "avg_won_value": mean(b["won"]) if b["won"] else 0,
        })
    rows.sort(key=lambda x: -x["won"])

    return {
        "total_won": won_total,
        "total_lost": lost_total,
        "total_won_value_cents": won_value,
        "total_lost_value_cents": lost_value,
        "avg_cycle_days": mean(cycle_lengths) if cycle_lengths else None,
        "by_source_list": rows,
    }


def render_markdown(r: dict) -> str:
    if r.get("unavailable"):
        return render_feature_unavailable(
            "Deals (CRM)", "Plus",
            "Win/loss reporting needs the /deals endpoint.",
        )
    lines = [
        "# Win/Loss Report",
        "",
        f"- Won: {r['total_won']} (${r['total_won_value_cents']/100:,.2f})",
        f"- Lost: {r['total_lost']} (${r['total_lost_value_cents']/100:,.2f})",
        f"- Avg cycle (days): {r['avg_cycle_days']:.0f}" if r['avg_cycle_days'] is not None else "- Avg cycle: —",
        "",
        "## By source list",
        "| List ID | Won | Lost | Win rate | Avg won $ |",
        "|---|---|---|---|---|",
    ]
    for row in r["by_source_list"]:
        lines.append(
            f"| {row['list']} | {row['won']} | {row['lost']} | "
            f"{row['win_rate']*100:.1f}% | ${row['avg_won_value']/100:,.2f} |"
        )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Win/loss report")
    parser.add_argument("--days", type=int, default=90)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    client = ACClient()
    data = fetch(client, args.days)
    r = analyze(data)
    out = json.dumps(r, indent=2) if args.format == "json" else render_markdown(r)
    if args.output:
        Path(args.output).write_text(out)
        print(f"Wrote {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()
