#!/usr/bin/env python3
"""
stale_contact_report.py — Contacts with no message engagement in the trailing window.

Uses messageActivities (reliable) instead of full contactActivities (incomplete
per AC's API).

Usage:
  python3 stale_contact_report.py
  python3 stale_contact_report.py --window-days 365 --format json
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


def fetch(client: ACClient, max_events: int, max_contacts: int = 20000) -> dict:
    contacts = client.stream("contacts", "contacts", max_items=max_contacts)
    activities = client.fetch_engagement_events(max_items=max_events)
    return {"contacts": contacts, "activities": activities}


def analyze(data: dict, window_days: int, sample_size: int = 50) -> dict:
    cutoff = datetime.now(timezone.utc) - timedelta(days=window_days)
    last_engage = {}
    for a in data["activities"]:
        ev = a.get("event")
        if ev not in ("open", "click"):
            continue
        ts = _parse_iso(a.get("tstamp"))
        if not ts:
            continue
        cid = a.get("contact")
        if not cid:
            continue
        cur = last_engage.get(cid)
        if not cur or ts > cur:
            last_engage[cid] = ts

    # Stream-friendly: counters + bounded samples instead of full per-contact lists.
    # AC's /contacts.status is null per-contact (status lives on /contactLists membership).
    # We treat all contacts as in-scope; users can filter by list separately.
    active_contacts = 0
    fresh_count = 0
    stale_count = 0
    no_engagement_count = 0
    stale_sample = []
    no_engagement_sample = []

    for c in data["contacts"]:
        active_contacts += 1
        cid = str(c["id"])
        last = last_engage.get(cid)
        if last is None:
            no_engagement_count += 1
            if len(no_engagement_sample) < sample_size:
                no_engagement_sample.append({
                    "id": cid, "email": c.get("email"), "cdate": c.get("cdate"),
                })
        elif last < cutoff:
            stale_count += 1
            if len(stale_sample) < sample_size:
                stale_sample.append({
                    "id": cid, "email": c.get("email"), "last_engaged": last.isoformat(),
                })
        else:
            fresh_count += 1

    return {
        "window_days": window_days,
        "active_contacts": active_contacts,
        "fresh_count": fresh_count,
        "stale_count": stale_count,
        "no_engagement_count": no_engagement_count,
        "stale": stale_sample,
        "no_engagement": no_engagement_sample,
    }


def render_markdown(r: dict) -> str:
    lines = [
        f"# Stale Contact Report (engagement in last {r['window_days']} days)",
        "",
        f"- Active contacts: **{r['active_contacts']:,}**",
        f"- Engaged in window: {r['fresh_count']:,}",
        f"- Stale (engaged outside window): {r['stale_count']:,}",
        f"- Never engaged: {r['no_engagement_count']:,}",
        "",
    ]
    if r["stale"]:
        lines.append("## Stale (showing first 50)")
        for s in r["stale"][:50]:
            lines.append(f"- {s['email']} — last engaged {s['last_engaged']}")
        lines.append("")
    if r["no_engagement"]:
        lines.append(f"## Never engaged (showing first 50 of {r['no_engagement_count']})")
        for s in r["no_engagement"][:50]:
            lines.append(f"- {s['email']} (created {s['cdate']})")
    return "\n".join(lines)

def _add_args(parser):
    parser.add_argument("--window-days", type=int, default=365)
    parser.add_argument("--max-events", type=int, default=30000)


def _fetch(client, args):
    return fetch(client, args.max_events)


def _analyze(data, args):
    return analyze(data, args.window_days)


def main():
    cli_main(
        description="Stale contact report",
        fetch_data=_fetch,
        analyze=_analyze,
        render_markdown=render_markdown,
        add_arguments=_add_args,
    )
if __name__ == "__main__":
    main()
