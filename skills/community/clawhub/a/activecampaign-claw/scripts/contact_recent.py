#!/usr/bin/env python3
"""
contact_recent.py — Most recent N contacts, ordered by creation date.

One API call. Use for "who signed up most recently" or "what's our newest lead."

Usage:
  python3 contact_recent.py                       # 5 most recent
  python3 contact_recent.py --limit 10
  python3 contact_recent.py --limit 20 --format json
"""

from __future__ import annotations

from _ac_client import ACClient, cli_main, sanitize


def _add_args(parser):
    parser.add_argument("--limit", type=int, default=5,
                        help="How many recent contacts to return (default 5)")


def fetch_data(client: ACClient, args) -> dict:
    res = client.get("contacts", params={
        "orders[cdate]": "DESC",
        "limit": args.limit,
    })
    return {"contacts": res.get("contacts") or [], "limit": args.limit}


def analyze(data: dict) -> dict:
    contacts = [
        {
            "id": c.get("id"),
            "email": sanitize(c.get("email", "")),
            "name": (
                f"{sanitize(c.get('firstName', ''))} "
                f"{sanitize(c.get('lastName', ''))}"
            ).strip(),
            "cdate": c.get("cdate"),
            "score": c.get("score"),
            "orgname": sanitize(c.get("orgname", "")),
        }
        for c in data["contacts"]
    ]
    return {"contacts": contacts, "limit": data["limit"]}


def render_markdown(r: dict) -> str:
    lines = [
        f"# Most recent {r['limit']} contacts",
        "",
        "| ID | Email | Name | Org | Score | Created |",
        "|---|---|---|---|---:|---|",
    ]
    for c in r["contacts"]:
        lines.append(
            f"| {c['id']} | {c['email']} | {c['name'] or '—'} | "
            f"{c['orgname'] or '—'} | {c['score'] or '—'} | {c['cdate']} |"
        )
    if not r["contacts"]:
        lines.append("| _no contacts_ | | | | | |")
    return "\n".join(lines) + "\n"


def main():
    cli_main(
        description="Most recent contacts by creation date",
        fetch_data=fetch_data,
        analyze=analyze,
        render_markdown=render_markdown,
        add_arguments=_add_args,
    )


if __name__ == "__main__":
    main()
