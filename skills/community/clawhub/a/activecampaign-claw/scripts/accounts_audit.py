#!/usr/bin/env python3
"""
accounts_audit.py — B2B Accounts (Plus+) health audit + ABM rollup.

Pulls /accounts (with `count_deals=true`) and /accountContacts to surface:

  - orphaned accounts (zero contacts AND zero deals)
  - "no-pipeline" accounts (contacts but no deals)
  - top accounts by deal count and contact count
  - stale accounts (no `updatedTimestamp` change in N days)
  - per-account-owner rollup

Plan gating: B2B Accounts is Plus+. On accounts without the feature,
`/accounts` returns 403 — the script exits cleanly.

Usage:
  python3 accounts_audit.py
  python3 accounts_audit.py --stale-days 90
  python3 accounts_audit.py --format json --output accounts_audit.json
"""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone

from _ac_client import (
    ACClient,
    ACClientError,
    cli_main,
    render_feature_unavailable,
)
from _ac_client import parse_date as _parse_date


def fetch_data(client: ACClient) -> dict:
    try:
        accounts = client.paginate(
            "accounts", "accounts",
            params={"count_deals": "true"},
            max_items=10000,
        )
    except ACClientError as e:
        if e.status_code == 403:
            return {"unavailable": True, "reason": "accounts_feature_not_enabled"}
        raise
    account_contacts = client.paginate(
        "accountContacts", "accountContacts", max_items=20000,
    )
    users = client.paginate("users", "users", max_items=500)
    return {
        "unavailable": False,
        "accounts": accounts,
        "account_contacts": account_contacts,
        "users": users,
    }


def analyze(data: dict, stale_days: int = 90, now: datetime | None = None) -> dict:
    if data.get("unavailable"):
        return {"unavailable": True, "reason": data.get("reason")}

    now = now or datetime.now(timezone.utc)
    accounts = data["accounts"]
    contacts = data["account_contacts"]
    users = data["users"]

    user_by_id = {str(u["id"]): u for u in users}
    contacts_per_account = Counter()
    for ac in contacts:
        contacts_per_account[str(ac.get("account"))] += 1

    rows = []
    for a in accounts:
        aid = str(a["id"])
        deal_count = int(a.get("dealCount", 0) or 0)
        contact_count = int(a.get("contactCount", 0) or contacts_per_account.get(aid, 0))
        last_update = _parse_date(a.get("updatedTimestamp") or a.get("createdTimestamp"))
        days_since = (now - last_update).days if last_update else None
        owner_id = str(a.get("owner") or "")
        owner_name = ""
        if owner_id in user_by_id:
            u = user_by_id[owner_id]
            owner_name = (
                f"{u.get('firstName', '')} {u.get('lastName', '')}".strip()
                or u.get("username", f"user-{owner_id}")
            )
        rows.append({
            "id": aid,
            "name": a.get("name", ""),
            "url": a.get("accountUrl", ""),
            "owner_id": owner_id,
            "owner_name": owner_name,
            "contact_count": contact_count,
            "deal_count": deal_count,
            "days_since_update": days_since,
        })

    orphaned = [r for r in rows if r["contact_count"] == 0 and r["deal_count"] == 0]
    no_pipeline = [r for r in rows if r["contact_count"] > 0 and r["deal_count"] == 0]
    stale = [
        r for r in rows
        if r["days_since_update"] is not None and r["days_since_update"] >= stale_days
    ]

    top_by_deals = sorted(rows, key=lambda r: -r["deal_count"])[:20]
    top_by_contacts = sorted(rows, key=lambda r: -r["contact_count"])[:20]

    by_owner = defaultdict(lambda: {
        "owner_name": "",
        "accounts": 0, "contacts": 0, "deals": 0,
    })
    for r in rows:
        bucket = by_owner[r["owner_id"]]
        bucket["owner_name"] = r["owner_name"] or f"user-{r['owner_id']}" or "(unowned)"
        bucket["accounts"] += 1
        bucket["contacts"] += r["contact_count"]
        bucket["deals"] += r["deal_count"]
    owner_rows = sorted(by_owner.values(), key=lambda r: -r["accounts"])

    return {
        "unavailable": False,
        "total_accounts": len(accounts),
        "total_account_contacts": len(contacts),
        "orphaned": orphaned,
        "no_pipeline": no_pipeline,
        "stale": stale,
        "top_by_deals": top_by_deals,
        "top_by_contacts": top_by_contacts,
        "owner_rollup": owner_rows,
        "stale_days_threshold": stale_days,
    }


def render_markdown(r: dict) -> str:
    if r.get("unavailable"):
        return render_feature_unavailable(
            "B2B Accounts", "Plus",
            "B2B accounts audit needs the /accounts endpoint.",
        )
    lines = [
        "# Accounts Audit",
        "",
        f"- Total accounts: **{r['total_accounts']}**",
        f"- Total account-contact links: {r['total_account_contacts']}",
        f"- Orphaned (no contacts and no deals): **{len(r['orphaned'])}**",
        f"- No-pipeline (contacts but no deals): **{len(r['no_pipeline'])}**",
        f"- Stale (no update in ≥{r['stale_days_threshold']}d): **{len(r['stale'])}**",
        "",
    ]
    if r["top_by_deals"]:
        lines.append("## Top accounts by deal count")
        lines.append("")
        lines.append("| Account | Owner | Contacts | Deals |")
        lines.append("|---|---|---:|---:|")
        for a in r["top_by_deals"][:10]:
            lines.append(
                f"| `{a['name']}` | {a['owner_name'] or '—'} | "
                f"{a['contact_count']} | {a['deal_count']} |"
            )
        lines.append("")
    if r["owner_rollup"]:
        lines.append("## Per-owner account rollup")
        lines.append("")
        lines.append("| Owner | Accounts | Contacts | Deals |")
        lines.append("|---|---:|---:|---:|")
        for o in r["owner_rollup"][:15]:
            lines.append(
                f"| {o['owner_name']} | {o['accounts']} | {o['contacts']} | {o['deals']} |"
            )
        lines.append("")
    if r["orphaned"]:
        lines.append("## Orphaned accounts (consider archive)")
        lines.append("")
        for a in r["orphaned"][:25]:
            lines.append(f"- `{a['name']}` (id={a['id']})")
        lines.append("")
    return "\n".join(lines)


def _add_args(parser):
    parser.add_argument("--stale-days", type=int, default=90)


def _analyze(data, args):
    return analyze(data, stale_days=args.stale_days)


def main():
    cli_main(
        description="Audit B2B accounts",
        fetch_data=fetch_data,
        analyze=_analyze,
        render_markdown=render_markdown,
        add_arguments=_add_args,
        feature_unavailable=(
            "B2B Accounts", "Plus",
            "B2B accounts audit needs the /accounts endpoint.",
        ),
    )


if __name__ == "__main__":
    main()
