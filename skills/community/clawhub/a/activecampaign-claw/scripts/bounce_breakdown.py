#!/usr/bin/env python3
"""
bounce_breakdown.py — Bounce decomposition by domain and reason for a campaign or globally.

Usage:
  python3 bounce_breakdown.py                # all bounces in account
  python3 bounce_breakdown.py --campaign 42  # campaign-scoped
  python3 bounce_breakdown.py --format json
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from _ac_client import ACClient


def fetch(client: ACClient, campaign_id: str | None, max_items: int = 20000) -> list:
    params = {}
    if campaign_id:
        params["filters[campaignid]"] = campaign_id
    return client.paginate("bounceLogs", "bounceLogs", params=params, max_items=max_items)


def analyze(bounces: list) -> dict:
    by_code = Counter()
    by_domain = Counter()
    detailed = []
    for b in bounces:
        code = (b.get("bounceCode") or b.get("error") or "unknown").split(":")[0]
        by_code[code] += 1
        # domain pulled from email if present in joined contact data; otherwise from email field
        email = (b.get("email") or "").lower()
        if "@" in email:
            by_domain[email.split("@", 1)[1]] += 1
        detailed.append({
            "contact": b.get("contact"),
            "campaign": b.get("campaignid"),
            "code": b.get("bounceCode"),
            "error": b.get("error"),
            "tstamp": b.get("tstamp"),
        })
    return {
        "total": len(bounces),
        "by_code": dict(by_code.most_common()),
        "by_domain": dict(by_domain.most_common(25)),
        "detail_sample": detailed[:50],
    }


def render_markdown(r: dict) -> str:
    lines = [
        "# Bounce Breakdown",
        "",
        f"Total bounces: **{r['total']}**",
        "",
        "## By bounce code",
    ]
    for code, n in r["by_code"].items():
        lines.append(f"- {code}: {n}")
    if r["by_domain"]:
        lines.append("")
        lines.append("## By recipient domain")
        for d, n in r["by_domain"].items():
            lines.append(f"- {d}: {n}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Bounce breakdown")
    parser.add_argument("--campaign", default=None)
    parser.add_argument("--max-items", type=int, default=20000,
                        help="Cap /bounceLogs stream (default 20000)")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    client = ACClient()
    bounces = fetch(client, args.campaign, max_items=args.max_items)
    r = analyze(bounces)
    out = json.dumps(r, indent=2) if args.format == "json" else render_markdown(r)
    if args.output:
        Path(args.output).write_text(out)
        print(f"Wrote {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()
