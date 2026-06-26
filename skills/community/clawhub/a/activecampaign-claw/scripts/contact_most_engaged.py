#!/usr/bin/env python3
"""
contact_most_engaged.py — Top N contacts by engagement signal.

Fast single-call lookup. Defaults to ranking by the contact's overall
score (the AC `score` field). Optional `--by recent` ranks by last
modification date (proxy for "recently active").

For deeper engagement analysis (composite scoring with tags + deals +
recent activity), use `scripts/find_hot_leads.py` instead — slower but
richer.

Usage:
  python3 contact_most_engaged.py                  # top 5 by score
  python3 contact_most_engaged.py --limit 10
  python3 contact_most_engaged.py --by recent      # top by mdate DESC
  python3 contact_most_engaged.py --format json
"""

from __future__ import annotations

from _ac_client import ACClient, cli_main, sanitize


def _add_args(parser):
    parser.add_argument("--limit", type=int, default=5,
                        help="How many contacts to return (default 5)")
    parser.add_argument("--by", choices=["score", "recent"], default="score",
                        help="Ranking signal: contact score (default) or "
                             "most-recently-modified")


def fetch_data(client: ACClient, args) -> dict:
    order_field = "score" if args.by == "score" else "mdate"
    res = client.get("contacts", params={
        f"orders[{order_field}]": "DESC",
        "limit": args.limit,
    })
    return {
        "contacts": res.get("contacts") or [],
        "by": args.by,
        "limit": args.limit,
    }


def analyze(data: dict) -> dict:
    return {
        "by": data["by"],
        "limit": data["limit"],
        "contacts": [
            {
                "id": c.get("id"),
                "email": sanitize(c.get("email", "")),
                "name": (
                    f"{sanitize(c.get('firstName', ''))} "
                    f"{sanitize(c.get('lastName', ''))}".strip()
                ),
                "orgname": sanitize(c.get("orgname", "")),
                "score": c.get("score"),
                "mdate": c.get("mdate"),
                "cdate": c.get("cdate"),
            }
            for c in data["contacts"]
        ],
    }


def render_markdown(r: dict) -> str:
    by_label = "score" if r["by"] == "score" else "last activity"
    lines = [
        f"# Top {r['limit']} contacts by {by_label}",
        "",
        "| Rank | Name | Email | Org | Score | Last activity |",
        "|---:|---|---|---|---:|---|",
    ]
    if not r["contacts"]:
        lines.append("| _no contacts_ | | | | | |")
        return "\n".join(lines) + "\n"
    for i, c in enumerate(r["contacts"], 1):
        lines.append(
            f"| {i} | {c['name'] or '—'} | {c['email']} | "
            f"{c['orgname'] or '—'} | {c['score'] or '—'} | {c['mdate']} |"
        )
    return "\n".join(lines) + "\n"


def main():
    cli_main(
        description="Top contacts by engagement signal (score or recency)",
        fetch_data=fetch_data,
        analyze=analyze,
        render_markdown=render_markdown,
        add_arguments=_add_args,
    )


if __name__ == "__main__":
    main()
