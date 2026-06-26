#!/usr/bin/env python3
"""
campaign_velocity.py — Send cadence and list-fatigue indicators.

Per list: campaigns sent in last N days, avg gap between sends, sends per
recipient over the window. Catches over-mailing and under-mailing.

Usage:
  python3 campaign_velocity.py
  python3 campaign_velocity.py --window-days 90 --format json
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta, timezone
from statistics import mean

from _ac_client import ACClient, cli_main
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
    campaigns = client.paginate("campaigns", "campaigns", max_items=5000)
    in_window = []
    for c in campaigns:
        d = _parse_iso(c.get("sdate") or c.get("ldate"))
        if d and d >= cutoff:
            in_window.append(c)
    lists = client.paginate("lists", "lists", max_items=2000)
    return {"campaigns": in_window, "lists": lists, "window_start": cutoff}


def analyze(data: dict, days: int) -> dict:
    list_name = {str(lst["id"]): lst.get("name", "") for lst in data["lists"]}
    sends_by_list = defaultdict(list)
    total_recipients = 0

    for c in data["campaigns"]:
        d = _parse_iso(c.get("sdate") or c.get("ldate"))
        sent = _safe_int(c.get("send_amt"))
        total_recipients += sent
        l_field = c.get("lists") or []
        if isinstance(l_field, list):
            for x in l_field:
                lid = str(x.get("list") if isinstance(x, dict) else x)
                sends_by_list[lid].append((d, sent))

    rows = []
    for lid, sends in sends_by_list.items():
        sends.sort()
        gaps = []
        for i in range(1, len(sends)):
            gaps.append((sends[i][0] - sends[i - 1][0]).total_seconds() / 86400)
        rows.append({
            "list_id": lid,
            "list_name": list_name.get(lid, lid),
            "sends": len(sends),
            "avg_gap_days": mean(gaps) if gaps else None,
            "total_recipient_events": sum(s[1] for s in sends),
        })
    rows.sort(key=lambda x: -x["sends"])
    return {
        "window_days": days,
        "total_campaigns": len(data["campaigns"]),
        "total_recipient_events": total_recipients,
        "by_list": rows,
    }


def render_markdown(r: dict) -> str:
    lines = [
        f"# Campaign Velocity (last {r['window_days']} days)",
        "",
        f"- Campaigns sent: {r['total_campaigns']}",
        f"- Total recipient-events: {r['total_recipient_events']:,}",
        "",
        "| List | Sends | Avg gap (days) | Recipient-events |",
        "|---|---|---|---|",
    ]
    for row in r["by_list"]:
        gap = f"{row['avg_gap_days']:.1f}" if row["avg_gap_days"] is not None else "—"
        lines.append(f"| {row['list_name']} | {row['sends']} | {gap} | {row['total_recipient_events']:,} |")
    if not r["by_list"]:
        lines.append("_No sends with list mapping in window._")
    return "\n".join(lines)

def _add_args(parser):
    parser.add_argument("--window-days", type=int, default=90)


def _fetch(client, args):
    return fetch(client, args.window_days)


def _analyze(data, args):
    return analyze(data, args.window_days)


def main():
    cli_main(
        description="Campaign send velocity per list",
        fetch_data=_fetch,
        analyze=_analyze,
        render_markdown=render_markdown,
        add_arguments=_add_args,
    )
if __name__ == "__main__":
    main()
