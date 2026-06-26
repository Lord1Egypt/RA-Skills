#!/usr/bin/env python3
"""
segment_performance.py — Aggregate campaign engagement for one audience cut.

Filters messageActivities to contacts in a given list, segment, or with a
given tag, then aggregates open/click rates.

Usage:
  python3 segment_performance.py --list <id>
  python3 segment_performance.py --tag <id>
  python3 segment_performance.py --segment <id>   # uses /contacts?segmentid=
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from _ac_client import ACClient, ACClientError


def fetch_audience(client: ACClient, list_id, tag_id, segment_id, max_contacts) -> set:
    if list_id:
        cls = client.paginate("contactLists", "contactLists", params={"filters[list]": list_id, "filters[status]": 1}, max_items=max_contacts)
        return {str(c.get("contact")) for c in cls}
    if tag_id:
        cts = client.paginate("contactTags", "contactTags", params={"filters[tag]": tag_id}, max_items=max_contacts)
        return {str(c.get("contact")) for c in cts}
    if segment_id:
        try:
            cs = client.paginate("contacts", "contacts", params={"segmentid": segment_id}, max_items=max_contacts)
            return {str(c["id"]) for c in cs}
        except ACClientError:
            return set()
    return set()


def fetch_activity(client: ACClient, max_events) -> list:
    return client.fetch_engagement_events(max_items=max_events)


def analyze(audience: set, activities: list) -> dict:
    sends = 0
    opens = 0
    clicks = 0
    contacts_open = set()
    contacts_click = set()
    for a in activities:
        cid = a.get("contact")
        if not cid or cid not in audience:
            continue
        ev = a.get("event")
        if ev == "send":
            sends += 1
        elif ev == "open":
            opens += 1
            contacts_open.add(cid)
        elif ev == "click":
            clicks += 1
            contacts_click.add(cid)
    return {
        "audience_size": len(audience),
        "send_events": sends,
        "open_events": opens,
        "click_events": clicks,
        "unique_openers": len(contacts_open),
        "unique_clickers": len(contacts_click),
    }


def render_markdown(r: dict, label: str) -> str:
    lines = [
        f"# Segment Performance: {label}",
        "",
        f"- Audience size: {r['audience_size']:,}",
        f"- Send events: {r['send_events']}",
        f"- Open events: {r['open_events']}",
        f"- Click events: {r['click_events']}",
        f"- Unique openers: {r['unique_openers']}",
        f"- Unique clickers: {r['unique_clickers']}",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Segment / audience performance")
    parser.add_argument("--list", dest="list_id")
    parser.add_argument("--tag", dest="tag_id")
    parser.add_argument("--segment", dest="segment_id")
    parser.add_argument("--max-contacts", type=int, default=20000)
    parser.add_argument("--max-events", type=int, default=30000)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    if not (args.list_id or args.tag_id or args.segment_id):
        print(
            "# Segment Performance\n\n"
            "This report needs an audience scope — pass exactly one of:\n\n"
            "- `--list <id>` to analyze a list's engagement\n"
            "- `--tag <id>` to analyze a tag's engagement\n"
            "- `--segment <id>` to analyze a saved segment's engagement\n\n"
            "Look up the id from `state.json` (run `calibrate.py` if needed) or "
            "from `scripts/list_audit.py` / `scripts/tag_audit.py` / "
            "`scripts/segment_audit.py`.\n"
        )
        return

    label = (
        f"list={args.list_id}" if args.list_id
        else f"tag={args.tag_id}" if args.tag_id
        else f"segment={args.segment_id}"
    )

    client = ACClient()
    audience = fetch_audience(client, args.list_id, args.tag_id, args.segment_id, args.max_contacts)
    activities = fetch_activity(client, args.max_events)
    r = analyze(audience, activities)
    out = json.dumps(r, indent=2) if args.format == "json" else render_markdown(r, label)
    if args.output:
        Path(args.output).write_text(out)
        print(f"Wrote {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()
