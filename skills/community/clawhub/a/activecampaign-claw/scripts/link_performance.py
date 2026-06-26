#!/usr/bin/env python3
"""
link_performance.py — Per-link performance for a campaign.

Usage:
  python3 link_performance.py <campaign_id>
  python3 link_performance.py 42 --format json
"""

from __future__ import annotations

from _ac_client import ACClient, cli_main
from _ac_client import safe_int as _safe_int


def fetch(client: ACClient, campaign_id: str) -> dict:
    campaign = client.get(f"campaigns/{campaign_id}").get("campaign", {})
    links = client.paginate(f"campaigns/{campaign_id}/links", "links", max_items=2000)
    return {"campaign": campaign, "links": links}


def analyze(data: dict) -> dict:
    c = data["campaign"]
    unique_opens = _safe_int(c.get("uniqueopens"))
    sent = _safe_int(c.get("send_amt"))

    rows = []
    total_unique_clicks = 0
    for link in data["links"]:
        uc = _safe_int(link.get("uniquelinkclicks"))
        rows.append({
            "link_id": link.get("id"),
            "url": link.get("link"),
            "name": link.get("name") or "",
            "tracked": link.get("tracked"),
            "clicks": _safe_int(link.get("linkclicks")),
            "unique_clicks": uc,
            "ctr_of_recipients": (uc / sent) if sent else 0,
            "ctr_of_opens": (uc / unique_opens) if unique_opens else 0,
        })
        total_unique_clicks += uc
    rows.sort(key=lambda x: -x["unique_clicks"])
    return {
        "campaign_id": c.get("id"),
        "campaign_name": c.get("name"),
        "total_links": len(rows),
        "total_unique_clicks": total_unique_clicks,
        "links": rows,
    }


def render_markdown(r: dict) -> str:
    lines = [
        f"# Link Performance: {r['campaign_name']} (id={r['campaign_id']})",
        "",
        f"- Total links: {r['total_links']}",
        f"- Total unique clicks: {r['total_unique_clicks']}",
        "",
        "| Link | Clicks | Unique | CTR (sent) | CTR (opens) |",
        "|---|---|---|---|---|",
    ]
    for link in r["links"]:
        url = (link["url"] or link["name"] or "")[:80]
        lines.append(
            f"| {url} | {link['clicks']} | {link['unique_clicks']} | "
            f"{link['ctr_of_recipients']*100:.2f}% | {link['ctr_of_opens']*100:.1f}% |"
        )
    return "\n".join(lines)

def _add_args(parser):
    parser.add_argument("campaign_id")


def _fetch(client, args):
    return fetch(client, args.campaign_id)


def main():
    cli_main(
        description="Per-link performance",
        fetch_data=_fetch,
        analyze=analyze,
        render_markdown=render_markdown,
        add_arguments=_add_args,
    )
if __name__ == "__main__":
    main()
