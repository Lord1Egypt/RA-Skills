#!/usr/bin/env python3
"""
last_campaign.py — Most recent campaign send.

One API call. Use for "when was my last email?" or "how did the last
send perform at a glance?"

Usage:
  python3 last_campaign.py
  python3 last_campaign.py --format json
"""

from __future__ import annotations

from _ac_client import ACClient, cli_main, sanitize


def fetch_data(client: ACClient) -> dict:
    res = client.get("campaigns", params={
        "orders[sdate]": "DESC",
        "limit": 1,
        "filters[status]": 5,  # 5 = sent
    })
    return {"campaigns": res.get("campaigns") or []}


def analyze(data: dict) -> dict:
    if not data["campaigns"]:
        return {"found": False}
    c = data["campaigns"][0]
    sends = int(c.get("send_amt", 0) or 0)
    uniq_opens = int(c.get("uniqueopens", 0) or 0)
    clicks = int(c.get("uniquelinkclicks", 0) or 0)
    bounces = int(c.get("bounces", 0) or 0)
    return {
        "found": True,
        "id": c.get("id"),
        "name": sanitize(c.get("name", "")),
        "subject": sanitize(c.get("subject", "")),
        "from_name": sanitize(c.get("fromname", "")),
        "from_email": sanitize(c.get("fromemail", "")),
        "sdate": c.get("sdate"),
        "send_amt": sends,
        "unique_opens": uniq_opens,
        "open_rate": (uniq_opens / sends) if sends else 0,
        "unique_clicks": clicks,
        "click_rate": (clicks / sends) if sends else 0,
        "bounces": bounces,
    }


def render_markdown(r: dict) -> str:
    if not r.get("found"):
        return "# Last campaign\n\nNo sent campaigns found.\n"
    return "\n".join([
        f"# Last campaign: `{r['name']}`",
        "",
        f"- Campaign id: **{r['id']}**",
        f"- Sent: {r['sdate']}",
        f"- Subject: {r['subject']}",
        f"- From: {r['from_name']} <{r['from_email']}>",
        f"- Recipients: **{r['send_amt']:,}**",
        f"- Unique opens: {r['unique_opens']:,} ({r['open_rate']*100:.1f}%)",
        f"- Unique clicks: {r['unique_clicks']:,} ({r['click_rate']*100:.1f}%)",
        f"- Bounces: {r['bounces']:,}",
    ]) + "\n"


def main():
    cli_main(
        description="Show the most recent campaign send",
        fetch_data=fetch_data,
        analyze=analyze,
        render_markdown=render_markdown,
    )


if __name__ == "__main__":
    main()
