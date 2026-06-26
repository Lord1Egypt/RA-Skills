#!/usr/bin/env python3
"""
domain_engagement_report.py — Open / click / bounce rates by recipient domain.

Joins messageActivity events to contacts, groups by email domain.
Catches one mailbox provider rate-limiting or filtering you.

Usage:
  python3 domain_engagement_report.py
  python3 domain_engagement_report.py --top 25 --format json
"""

from __future__ import annotations

from collections import defaultdict

from _ac_client import ACClient, cli_main


def fetch(client: ACClient, max_events: int, max_items: int = 20000) -> dict:
    activities = client.fetch_engagement_events(max_items=max_events)
    contacts = client.paginate("contacts", "contacts", max_items=max_items)
    bounces = client.paginate("bounceLogs", "bounceLogs", max_items=20000)
    return {"activities": activities, "contacts": contacts, "bounces": bounces}


def analyze(data: dict, top: int) -> dict:
    email_by_id = {str(c["id"]): (c.get("email") or "").lower() for c in data["contacts"]}

    def _domain(cid):
        e = email_by_id.get(str(cid)) or ""
        return e.split("@", 1)[1] if "@" in e else None

    open_by_domain = defaultdict(int)
    click_by_domain = defaultdict(int)
    send_by_domain = defaultdict(int)
    contacts_by_domain = defaultdict(int)
    for c in data["contacts"]:
        e = (c.get("email") or "").lower()
        if "@" in e:
            contacts_by_domain[e.split("@", 1)[1]] += 1

    for a in data["activities"]:
        d = _domain(a.get("contact"))
        if not d:
            continue
        ev = a.get("event")
        if ev == "open":
            open_by_domain[d] += 1
        elif ev == "click":
            click_by_domain[d] += 1
        elif ev == "send":
            send_by_domain[d] += 1

    bounce_by_domain = defaultdict(int)
    for b in data["bounces"]:
        d = _domain(b.get("contact"))
        if d:
            bounce_by_domain[d] += 1

    rows = []
    for d, count in sorted(contacts_by_domain.items(), key=lambda x: -x[1])[:top]:
        rows.append({
            "domain": d,
            "contacts": count,
            "opens": open_by_domain.get(d, 0),
            "clicks": click_by_domain.get(d, 0),
            "bounces": bounce_by_domain.get(d, 0),
        })
    return {"domains": rows, "total_open_events": sum(open_by_domain.values())}


def render_markdown(r: dict) -> str:
    lines = [
        "# Domain Engagement Report",
        "",
        f"Total open events analyzed: {r['total_open_events']}",
        "",
        "| Domain | Contacts | Opens | Clicks | Bounces |",
        "|---|---|---|---|---|",
    ]
    for d in r["domains"]:
        lines.append(f"| {d['domain']} | {d['contacts']} | {d['opens']} | {d['clicks']} | {d['bounces']} |")
    if not r["domains"]:
        lines.append("_(No data.)_")
    return "\n".join(lines)

def _add_args(parser):
    parser.add_argument("--top", type=int, default=25)
    parser.add_argument("--max-events", type=int, default=20000)
    parser.add_argument("--max-items", type=int, default=20000)


def _fetch(client, args):
    return fetch(client, args.max_events, max_items=args.max_items)


def _analyze(data, args):
    return analyze(data, args.top)


def main():
    cli_main(
        description="Engagement by recipient domain",
        fetch_data=_fetch,
        analyze=_analyze,
        render_markdown=render_markdown,
        add_arguments=_add_args,
    )
if __name__ == "__main__":
    main()
