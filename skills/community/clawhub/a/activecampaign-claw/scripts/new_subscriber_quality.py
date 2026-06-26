#!/usr/bin/env python3
"""
new_subscriber_quality.py — Engagement quality of contacts added in the trailing window.

Of contacts added in the last N days, what % opened, bounced, unsubscribed?

Usage:
  python3 new_subscriber_quality.py
  python3 new_subscriber_quality.py --days 30 --format json
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from _ac_client import ACClient, cli_main


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


def fetch(client: ACClient, max_events: int) -> dict:
    contacts = client.paginate("contacts", "contacts", max_items=20000)
    activities = client.fetch_engagement_events(max_items=max_events)
    return {"contacts": contacts, "activities": activities}


def analyze(data: dict, days: int) -> dict:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    new = []
    for c in data["contacts"]:
        d = _parse_iso(c.get("cdate"))
        if d and d >= cutoff:
            new.append(c)

    new_ids = {str(c["id"]) for c in new}
    opened = set()
    clicked = set()
    for a in data["activities"]:
        cid = a.get("contact")
        if not cid or cid not in new_ids:
            continue
        ev = a.get("event")
        if ev == "open":
            opened.add(cid)
        elif ev == "click":
            clicked.add(cid)

    unsub = sum(1 for c in new if str(c.get("status")) == "2")
    bounce = sum(1 for c in new if str(c.get("status")) == "3")
    total = len(new)
    return {
        "window_days": days,
        "new_contacts": total,
        "opened_at_least_once": len(opened),
        "clicked_at_least_once": len(clicked),
        "unsubscribed": unsub,
        "bounced": bounce,
        "open_rate_of_new": (len(opened) / total) if total else 0,
        "unsub_rate_of_new": (unsub / total) if total else 0,
        "bounce_rate_of_new": (bounce / total) if total else 0,
    }


def render_markdown(r: dict) -> str:
    lines = [
        f"# New Subscriber Quality (last {r['window_days']} days)",
        "",
        f"- New contacts: **{r['new_contacts']:,}**",
        f"- Opened any campaign: {r['opened_at_least_once']:,} ({r['open_rate_of_new']*100:.1f}%)",
        f"- Clicked any link: {r['clicked_at_least_once']:,}",
        f"- Unsubscribed: {r['unsubscribed']:,} ({r['unsub_rate_of_new']*100:.2f}%)",
        f"- Bounced: {r['bounced']:,} ({r['bounce_rate_of_new']*100:.2f}%)",
    ]
    if r["new_contacts"] == 0:
        lines.append("")
        lines.append("_No new contacts in window._")
    return "\n".join(lines)

def _add_args(parser):
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--max-events", type=int, default=30000)


def _fetch(client, args):
    return fetch(client, args.max_events)


def _analyze(data, args):
    return analyze(data, args.days)


def main():
    cli_main(
        description="New subscriber quality",
        fetch_data=_fetch,
        analyze=_analyze,
        render_markdown=render_markdown,
        add_arguments=_add_args,
    )
if __name__ == "__main__":
    main()
