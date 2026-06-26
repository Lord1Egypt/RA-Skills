#!/usr/bin/env python3
"""
list_audit.py — Per-list health: subscriber count, last campaign sent, opt-in source.

Identifies lists you can retire (no recent campaigns, low subscriber count).

Usage:
  python3 list_audit.py
  python3 list_audit.py --format json
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone

from _ac_client import ACClient, cli_main


def _days_since(iso_str: str | None) -> float | None:
    if not iso_str:
        return None
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - dt).total_seconds() / 86400
    except (ValueError, TypeError):
        return None


def fetch(client: ACClient, max_items: int = 50000) -> dict:
    lists = client.paginate("lists", "lists", max_items=2000)
    contact_lists = client.paginate("contactLists", "contactLists", max_items=max_items)
    campaigns = client.paginate("campaigns", "campaigns", max_items=2000)
    return {"lists": lists, "contact_lists": contact_lists, "campaigns": campaigns}


def analyze(data: dict) -> dict:
    by_list_active = Counter()  # status 1 = active
    by_list_unsub = Counter()
    by_list_bounce = Counter()
    for cl in data["contact_lists"]:
        lid = str(cl.get("list"))
        status = str(cl.get("status"))
        if status == "1":
            by_list_active[lid] += 1
        elif status == "2":
            by_list_unsub[lid] += 1
        elif status == "3":
            by_list_bounce[lid] += 1

    # last campaign per list (campaigns can target multiple lists via /campaignLists, but
    # `campaigns` resource often has list info inline as a list of ids)
    last_campaign = {}  # list_id -> (campaign_id, sdate)
    for c in data["campaigns"]:
        sdate = c.get("sdate") or c.get("ldate") or c.get("cdate")
        # campaign object may link to lists via various fields; many AC accounts surface "lists" array
        l_field = c.get("lists") or []
        if isinstance(l_field, list):
            target_lists = [str(x.get("list") if isinstance(x, dict) else x) for x in l_field]
        else:
            target_lists = []
        for lid in target_lists:
            cur = last_campaign.get(lid)
            if not cur or (sdate and sdate > cur[1]):
                last_campaign[lid] = (c.get("id"), sdate)

    rows = []
    for lst in data["lists"]:
        lid = str(lst["id"])
        active = by_list_active.get(lid, 0)
        unsub = by_list_unsub.get(lid, 0)
        bounce = by_list_bounce.get(lid, 0)
        total = active + unsub + bounce
        last = last_campaign.get(lid)
        last_sent = last[1] if last else None
        days = _days_since(last_sent) if last_sent else None
        rows.append({
            "id": lid,
            "name": lst.get("name", ""),
            "active": active,
            "unsubscribed": unsub,
            "bounced": bounce,
            "total": total,
            "last_campaign_sent": last_sent,
            "days_since_last_send": int(days) if days is not None else None,
            "stale": days is None or days > 90,
        })
    rows.sort(key=lambda x: -x["active"])
    return {"lists": rows, "stale_count": sum(1 for r in rows if r["stale"])}


def render_markdown(r: dict) -> str:
    lines = [
        "# List Audit",
        "",
        f"- Total lists: {len(r['lists'])}",
        f"- Stale (no campaign in 90+ days or never): **{r['stale_count']}**",
        "",
        "| List | Active | Unsub | Bounce | Total | Days since last send |",
        "|---|---|---|---|---|---|",
    ]
    for lst in r["lists"]:
        days = lst["days_since_last_send"]
        days_s = "never" if days is None else f"{days}"
        lines.append(
            f"| {lst['name']} | {lst['active']} | {lst['unsubscribed']} | "
            f"{lst['bounced']} | {lst['total']} | {days_s} |"
        )
    return "\n".join(lines)

def _add_args(parser):
    parser.add_argument("--max-items", type=int, default=50000,
                        help="Cap /contactLists stream (default 50000)")


def _fetch(client, args):
    return fetch(client, max_items=args.max_items)


def main():
    cli_main(
        description="Audit list health",
        fetch_data=_fetch,
        analyze=analyze,
        render_markdown=render_markdown,
        add_arguments=_add_args,
    )
if __name__ == "__main__":
    main()
