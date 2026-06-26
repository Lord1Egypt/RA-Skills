#!/usr/bin/env python3
"""
contact_engagement_leaders.py — Top contacts by click / open / total engagement
in a recent window.

Aggregates `/messageActivities` (falls back to `/linkData` when the AC plan
doesn't expose messageActivities) by contact, counts events, returns the
top N. Designed as the fast path for questions like:

  - "Who are my contacts with the most clicks?"
  - "Who has opened the most emails recently?"
  - "Who are my most engaged contacts (clicks + opens)?"

Usage:
  python3 contact_engagement_leaders.py                       # top 10, last 30d, clicks+opens
  python3 contact_engagement_leaders.py --by clicks --limit 5
  python3 contact_engagement_leaders.py --by opens --window-days 90
  python3 contact_engagement_leaders.py --format json
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta, timezone

from _ac_client import ACClient, cli_main, sanitize


def _add_args(parser):
    parser.add_argument("--by", choices=["clicks", "opens", "both"], default="both",
                        help="Event type to rank by (default: both — sum of clicks + opens)")
    parser.add_argument("--limit", type=int, default=10,
                        help="How many top contacts to return (default 10)")
    parser.add_argument("--window-days", type=int, default=30,
                        help="Look back this many days (default 30)")
    parser.add_argument("--max-events", type=int, default=30000,
                        help="Cap the engagement-event scan (default 30000). "
                             "Raise on accounts with very high mail volume.")


def _parse_ts(s):
    if not s:
        return None
    try:
        dt = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (ValueError, TypeError):
        return None


def fetch_data(client: ACClient, args) -> dict:
    args.progress("Pulling engagement events...")
    events = client.fetch_engagement_events(max_items=args.max_events, quiet=True)
    args.progress(f"  ...{len(events):,} events found")
    return {
        "events": events,
        "by": args.by,
        "limit": args.limit,
        "window_days": args.window_days,
    }


def analyze(data: dict, args) -> dict:
    events = data["events"]
    cutoff = datetime.now(timezone.utc) - timedelta(days=args.window_days)

    # We want clicks or opens (or both).
    wanted = {"both": {"click", "open"},
              "clicks": {"click"},
              "opens": {"open"}}[args.by]

    clicks_by_contact: Counter = Counter()
    opens_by_contact: Counter = Counter()
    for e in events:
        cid = e.get("contact")
        ev = (e.get("event") or "").lower()
        ts = _parse_ts(e.get("tstamp"))
        if not cid or ev not in wanted:
            continue
        if ts and ts < cutoff:
            continue
        if ev == "click":
            clicks_by_contact[cid] += 1
        elif ev == "open":
            opens_by_contact[cid] += 1

    if args.by == "clicks":
        ranked = clicks_by_contact
    elif args.by == "opens":
        ranked = opens_by_contact
    else:
        ranked = clicks_by_contact + opens_by_contact

    top_ids = [cid for cid, _ in ranked.most_common(args.limit)]
    return {
        "by": args.by,
        "window_days": args.window_days,
        "limit": args.limit,
        "top": [
            {
                "contact_id": cid,
                "clicks": clicks_by_contact.get(cid, 0),
                "opens": opens_by_contact.get(cid, 0),
                "total": clicks_by_contact.get(cid, 0) + opens_by_contact.get(cid, 0),
            }
            for cid in top_ids
        ],
        "total_events_in_window": sum(ranked.values()),
        "unique_contacts_in_window": len(ranked),
    }


def _enrich_with_names(client: ACClient, report: dict) -> None:
    """Resolve contact ids in `report['top']` to email + name.

    AC v3 doesn't reliably support a multi-id `filters[id_in]` query on
    /contacts, so we just do one `GET /contacts/{id}` per top row. For a
    top-10 that's ~10 sub-200ms calls totaling ~2s wall-clock, which is
    acceptable for a script that's already 3–4s in event aggregation.
    """
    for row in report["top"]:
        cid = str(row.get("contact_id") or "")
        if not cid:
            row.setdefault("email", "")
            row.setdefault("name", "")
            continue
        try:
            c = client.get(f"contacts/{cid}").get("contact") or {}
        except Exception:  # noqa: BLE001 — enrichment is best-effort
            c = {}
        row["email"] = sanitize(c.get("email", ""))
        row["name"] = (
            f"{sanitize(c.get('firstName', ''))} "
            f"{sanitize(c.get('lastName', ''))}".strip()
        )


def _analyze_and_enrich(data, args):
    """Wraps analyze + a single batched name-resolution call. cli_main passes
    a client only into fetch_data, so we recreate one here (cheap) for the
    enrichment step. (`contact_engagement_leaders` is one of the few scripts
    that legitimately needs a client in analyze)."""
    report = analyze(data, args)
    try:
        client = ACClient()
        _enrich_with_names(client, report)
    except Exception:  # noqa: BLE001 — enrichment is best-effort
        for row in report["top"]:
            row.setdefault("email", "")
            row.setdefault("name", "")
    return report


def render_markdown(r: dict) -> str:
    label = {"clicks": "clicks", "opens": "opens",
             "both": "clicks + opens"}[r["by"]]
    lines = [
        f"# Top {r['limit']} contacts by {label} (last {r['window_days']} days)",
        "",
        f"_{r['total_events_in_window']:,} matching events across "
        f"{r['unique_contacts_in_window']:,} unique contacts in the window._",
        "",
        "| Rank | Name | Email | Clicks | Opens | Total |",
        "|---:|---|---|---:|---:|---:|",
    ]
    if not r["top"]:
        lines.append("| _no engagement events in window_ | | | | | |")
        return "\n".join(lines) + "\n"
    for i, row in enumerate(r["top"], 1):
        lines.append(
            f"| {i} | {row.get('name') or '—'} | "
            f"{row.get('email') or row['contact_id']} | "
            f"{row['clicks']} | {row['opens']} | **{row['total']}** |"
        )
    return "\n".join(lines) + "\n"


def main():
    cli_main(
        description="Top contacts by click / open / engagement event count",
        fetch_data=fetch_data,
        analyze=_analyze_and_enrich,
        render_markdown=render_markdown,
        add_arguments=_add_args,
    )


if __name__ == "__main__":
    main()
