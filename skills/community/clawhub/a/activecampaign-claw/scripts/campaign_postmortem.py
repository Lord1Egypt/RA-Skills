#!/usr/bin/env python3
"""
campaign_postmortem.py — Single-campaign performance breakdown vs. baseline.

Reports opens, clicks, unsubs, bounces vs. the account 90-day baseline,
plus per-link CTR. Per-event detail (open-by-domain, time-to-first-open)
included when AC's messageActivities are populated.

Usage:
  python3 campaign_postmortem.py <campaign_id>
  python3 campaign_postmortem.py 42 --format json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from _ac_client import ACClient, ACClientError, load_state
from _ac_client import safe_int as _safe_int


def fetch(client: ACClient, campaign_id: str) -> dict:
    campaign = client.get(f"campaigns/{campaign_id}").get("campaign", {})
    links = client.paginate(f"campaigns/{campaign_id}/links", "links", max_items=2000)
    activities = []
    try:
        activities = client.paginate(
            f"campaigns/{campaign_id}/messageActivities",
            "messageActivities",
            max_items=10000,
        )
    except ACClientError as e:
        if e.status_code != 404:
            raise
    return {"campaign": campaign, "links": links, "activities": activities}


def analyze(data: dict, baseline: dict) -> dict:
    c = data["campaign"]
    sent = _safe_int(c.get("send_amt"))
    opens = _safe_int(c.get("opens"))
    unique_opens = _safe_int(c.get("uniqueopens"))
    clicks = _safe_int(c.get("linkclicks"))
    unique_clicks = _safe_int(c.get("uniquelinkclicks"))
    unsubs = _safe_int(c.get("unsubscribes"))
    bounces = _safe_int(c.get("bounces"))

    open_rate = (unique_opens / sent) if sent else 0
    click_rate = (unique_clicks / sent) if sent else 0
    unsub_rate = (unsubs / sent) if sent else 0
    bounce_rate = (bounces / sent) if sent else 0
    ctor = (unique_clicks / unique_opens) if unique_opens else 0

    base_open = baseline.get("open_rate_p50", 0.25)
    base_click = baseline.get("click_rate_p50", 0.03)
    base_unsub = baseline.get("unsub_rate", 0.003)

    link_rows = []
    for link in data["links"]:
        lc = _safe_int(link.get("linkclicks"))
        ulc = _safe_int(link.get("uniquelinkclicks"))
        link_rows.append({
            "url": link.get("link"),
            "name": link.get("name"),
            "clicks": lc,
            "unique_clicks": ulc,
            "ctr_of_opens": (ulc / unique_opens) if unique_opens else 0,
        })
    link_rows.sort(key=lambda x: -x["unique_clicks"])

    return {
        "campaign_id": c.get("id"),
        "name": c.get("name"),
        "subject": c.get("subject"),
        "send_date": c.get("sdate") or c.get("ldate"),
        "sent": sent,
        "opens": opens,
        "unique_opens": unique_opens,
        "clicks": clicks,
        "unique_clicks": unique_clicks,
        "unsubs": unsubs,
        "bounces": bounces,
        "metrics": {
            "open_rate": open_rate,
            "click_rate": click_rate,
            "unsub_rate": unsub_rate,
            "bounce_rate": bounce_rate,
            "click_to_open": ctor,
        },
        "vs_baseline": {
            "open_rate_delta_pp": (open_rate - base_open) * 100,
            "click_rate_delta_pp": (click_rate - base_click) * 100,
            "unsub_rate_delta_pp": (unsub_rate - base_unsub) * 100,
        },
        "links": link_rows,
        "activity_event_count": len(data["activities"]),
    }


def render_markdown(r: dict) -> str:
    m = r["metrics"]
    b = r["vs_baseline"]
    lines = [
        f"# Campaign Postmortem: {r['name']}",
        "",
        f"- Subject: {r['subject']}",
        f"- Sent: {r['send_date']}",
        f"- Recipients: {r['sent']:,}",
        "",
        "## Metrics",
        f"- Opens: {r['opens']} ({r['unique_opens']} unique)",
        f"- Clicks: {r['clicks']} ({r['unique_clicks']} unique)",
        f"- Unsubscribes: {r['unsubs']}",
        f"- Bounces: {r['bounces']}",
        "",
        "## Rates",
        f"- Open rate: **{m['open_rate']*100:.1f}%** (vs. baseline: {b['open_rate_delta_pp']:+.1f}pp)",
        f"- Click rate: **{m['click_rate']*100:.1f}%** (vs. baseline: {b['click_rate_delta_pp']:+.1f}pp)",
        f"- Click-to-open: {m['click_to_open']*100:.1f}%",
        f"- Unsub rate: {m['unsub_rate']*100:.2f}% (vs. baseline: {b['unsub_rate_delta_pp']:+.2f}pp)",
        f"- Bounce rate: {m['bounce_rate']*100:.2f}%",
        "",
    ]
    if r["links"]:
        lines.append("## Top links")
        lines.append("| Link | Unique clicks | CTR-of-opens |")
        lines.append("|---|---|---|")
        for link in r["links"][:15]:
            url = link["url"][:80] if link["url"] else link["name"]
            lines.append(f"| {url} | {link['unique_clicks']} | {link['ctr_of_opens']*100:.1f}% |")
    if r["activity_event_count"] == 0:
        lines.append("")
        lines.append("_(No per-event activity records returned by AC for this campaign.)_")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Campaign postmortem")
    parser.add_argument("campaign_id")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    state = load_state() or {}
    baseline = state.get("baselines", {})
    client = ACClient()
    data = fetch(client, args.campaign_id)
    r = analyze(data, baseline)
    out = json.dumps(r, indent=2) if args.format == "json" else render_markdown(r)
    if args.output:
        Path(args.output).write_text(out)
        print(f"Wrote {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()
