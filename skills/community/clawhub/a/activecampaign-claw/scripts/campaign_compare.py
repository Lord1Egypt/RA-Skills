#!/usr/bin/env python3
"""
campaign_compare.py — Side-by-side performance for two campaigns.

Usage:
  python3 campaign_compare.py <id_a> <id_b>
  python3 campaign_compare.py 41 42 --format json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from _ac_client import ACClient
from _ac_client import safe_int as _safe_int


def fetch_campaign(client: ACClient, cid: str) -> dict:
    return client.get(f"campaigns/{cid}").get("campaign", {})


def metrics(c: dict) -> dict:
    sent = _safe_int(c.get("send_amt"))
    uo = _safe_int(c.get("uniqueopens"))
    uc = _safe_int(c.get("uniquelinkclicks"))
    return {
        "id": c.get("id"),
        "name": c.get("name"),
        "subject": c.get("subject"),
        "send_date": c.get("sdate") or c.get("ldate"),
        "sent": sent,
        "unique_opens": uo,
        "unique_clicks": uc,
        "unsubs": _safe_int(c.get("unsubscribes")),
        "bounces": _safe_int(c.get("bounces")),
        "open_rate": (uo / sent) if sent else 0,
        "click_rate": (uc / sent) if sent else 0,
        "click_to_open": (uc / uo) if uo else 0,
    }


def render_markdown(a: dict, b: dict) -> str:
    rows = [
        ("Name", a["name"], b["name"]),
        ("Subject", a["subject"], b["subject"]),
        ("Sent on", a["send_date"], b["send_date"]),
        ("Recipients", f"{a['sent']:,}", f"{b['sent']:,}"),
        ("Unique opens", a["unique_opens"], b["unique_opens"]),
        ("Unique clicks", a["unique_clicks"], b["unique_clicks"]),
        ("Unsubs", a["unsubs"], b["unsubs"]),
        ("Bounces", a["bounces"], b["bounces"]),
        ("Open rate", f"{a['open_rate']*100:.1f}%", f"{b['open_rate']*100:.1f}%"),
        ("Click rate", f"{a['click_rate']*100:.2f}%", f"{b['click_rate']*100:.2f}%"),
        ("Click-to-open", f"{a['click_to_open']*100:.1f}%", f"{b['click_to_open']*100:.1f}%"),
    ]
    lines = [
        f"# Campaign Compare: {a['id']} vs {b['id']}",
        "",
        "| Metric | Campaign A | Campaign B |",
        "|---|---|---|",
    ]
    for label, av, bv in rows:
        lines.append(f"| {label} | {av} | {bv} |")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Compare two campaigns")
    parser.add_argument("id_a")
    parser.add_argument("id_b")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    client = ACClient()
    ma = metrics(fetch_campaign(client, args.id_a))
    mb = metrics(fetch_campaign(client, args.id_b))
    if args.format == "json":
        out = json.dumps({"a": ma, "b": mb}, indent=2)
    else:
        out = render_markdown(ma, mb)
    if args.output:
        Path(args.output).write_text(out)
        print(f"Wrote {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()
