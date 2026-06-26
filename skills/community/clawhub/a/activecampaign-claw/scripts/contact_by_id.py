#!/usr/bin/env python3
"""
contact_by_id.py — Single contact lookup by AC id.

One API call.

Usage:
  python3 contact_by_id.py <id>
  python3 contact_by_id.py 123 --format json
"""

from __future__ import annotations

from _ac_client import ACClient, ACClientError, cli_main, sanitize


def _add_args(parser):
    parser.add_argument("contact_id", help="ActiveCampaign contact id")


def fetch_data(client: ACClient, args) -> dict:
    try:
        res = client.get(f"contacts/{args.contact_id}")
    except ACClientError as e:
        if e.status_code == 404:
            return {"not_found": True, "id": args.contact_id}
        raise
    return {"contact": res.get("contact"), "id": args.contact_id}


def analyze(data: dict) -> dict:
    if data.get("not_found"):
        return {"found": False, "id": data["id"]}
    c = data["contact"] or {}
    return {
        "found": True,
        "id": c.get("id"),
        "email": sanitize(c.get("email", "")),
        "first_name": sanitize(c.get("firstName", "")),
        "last_name": sanitize(c.get("lastName", "")),
        "phone": sanitize(c.get("phone", "")),
        "orgname": sanitize(c.get("orgname", "")),
        "score": c.get("score"),
        "cdate": c.get("cdate"),
        "mdate": c.get("mdate"),
        "bounced_hard": c.get("bounced_hard"),
        "bounced_soft": c.get("bounced_soft"),
    }


def render_markdown(r: dict) -> str:
    if not r["found"]:
        return f"# Contact lookup\n\nNo contact found with id `{r['id']}`.\n"
    lines = [
        f"# {r['first_name']} {r['last_name']} ({r['email']})".strip(),
        "",
        f"- ID: **{r['id']}**",
        f"- Phone: {r['phone'] or '—'}",
        f"- Organization: {r['orgname'] or '—'}",
        f"- Score: {r['score'] or '—'}",
        f"- Created: {r['cdate']}",
        f"- Last modified: {r['mdate']}",
        f"- Hard bounce: {'yes' if str(r['bounced_hard']) == '1' else 'no'}",
        f"- Soft bounce: {'yes' if str(r['bounced_soft']) == '1' else 'no'}",
    ]
    return "\n".join(lines) + "\n"


def main():
    cli_main(
        description="Look up a single contact by ID",
        fetch_data=fetch_data,
        analyze=analyze,
        render_markdown=render_markdown,
        add_arguments=_add_args,
    )


if __name__ == "__main__":
    main()
