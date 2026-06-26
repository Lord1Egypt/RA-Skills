#!/usr/bin/env python3
"""
deal_by_id.py — Single deal lookup by AC id.

One API call. Exits cleanly on Lite (no Deals) accounts.

Usage:
  python3 deal_by_id.py <id>
  python3 deal_by_id.py 42 --format json
"""

from __future__ import annotations

from _ac_client import ACClient, ACClientError, cli_main, sanitize


def _add_args(parser):
    parser.add_argument("deal_id", help="ActiveCampaign deal id")


def fetch_data(client: ACClient, args) -> dict:
    try:
        res = client.get(f"deals/{args.deal_id}")
    except ACClientError as e:
        if e.status_code == 404:
            return {"not_found": True, "id": args.deal_id}
        raise
    return {"deal": res.get("deal"), "id": args.deal_id}


def analyze(data: dict) -> dict:
    if data.get("not_found"):
        return {"found": False, "id": data["id"]}
    d = data["deal"] or {}
    return {
        "found": True,
        "id": d.get("id"),
        "title": sanitize(d.get("title", "")),
        "value_cents": d.get("value"),
        "currency": d.get("currency"),
        "stage": d.get("stage"),
        "group": d.get("group"),
        "owner": d.get("owner"),
        "contact": d.get("contact"),
        "status": d.get("status"),
        "cdate": d.get("cdate"),
        "mdate": d.get("mdate"),
        "nextdate": d.get("nextdate"),
        "edate": d.get("edate"),
    }


def render_markdown(r: dict) -> str:
    if not r["found"]:
        return f"# Deal lookup\n\nNo deal found with id `{r['id']}`.\n"
    status_map = {"0": "open", "1": "won", "2": "lost", "3": "hot"}
    val_cents = r["value_cents"]
    val_str = (
        f"${int(val_cents) / 100:,.2f}" if val_cents not in (None, "", "0")
        else "—"
    )
    lines = [
        f"# Deal {r['id']}: {r['title']}".strip(),
        "",
        f"- Value: **{val_str}** {r['currency'] or ''}".rstrip(),
        f"- Status: {status_map.get(str(r['status']), r['status'])}",
        f"- Stage id: {r['stage']}",
        f"- Pipeline (group) id: {r['group']}",
        f"- Owner id: {r['owner']}",
        f"- Contact id: {r['contact']}",
        f"- Created: {r['cdate']}",
        f"- Last modified: {r['mdate']}",
        f"- Next activity date: {r['nextdate'] or '—'}",
        f"- Close date: {r['edate'] or '—'}",
    ]
    return "\n".join(lines) + "\n"


def main():
    cli_main(
        description="Look up a single deal by ID",
        fetch_data=fetch_data,
        analyze=analyze,
        render_markdown=render_markdown,
        add_arguments=_add_args,
        feature_unavailable=(
            "Deals (CRM)", "Plus",
            "Deal lookup needs the /deals endpoint.",
        ),
    )


if __name__ == "__main__":
    main()
