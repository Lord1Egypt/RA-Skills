#!/usr/bin/env python3
"""
contact_full_profile.py — Everything about one contact in one report.

Pulls the contact record and its related sub-resources in parallel via
`fetch_many`: tags, lists, automations, deals, custom-field values, notes,
and recent activity. One report, ~5–6 API calls in flight at the rate limit,
instead of 5–6 serial scripts.

Usage:
  python3 contact_full_profile.py --email user@example.com
  python3 contact_full_profile.py --id 12345
  python3 contact_full_profile.py --email user@example.com --format json
"""

from __future__ import annotations

from _ac_client import ACClient, ACClientError, cli_main, load_state, sanitize


def _add_args(parser):
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--email", help="Contact email")
    g.add_argument("--id", dest="contact_id", help="Contact id")


def _resolve_contact(client: ACClient, args) -> dict:
    if args.contact_id:
        try:
            res = client.get(f"contacts/{args.contact_id}")
        except ACClientError as e:
            if e.status_code == 404:
                return {"not_found": True}
            raise
        return res.get("contact") or {"not_found": True}
    res = client.get("contacts", params={"email": args.email})
    contacts = res.get("contacts") or []
    return contacts[0] if contacts else {"not_found": True}


def fetch_data(client: ACClient, args) -> dict:
    args.progress("Resolving contact...")
    contact = _resolve_contact(client, args)
    if contact.get("not_found"):
        return {"contact": None}
    cid = contact["id"]
    filters = {"filters[contact]": cid}

    args.progress("Fetching tags, lists, automations, fields, notes, deals in parallel...")
    bulk = client.fetch_many([
        ("contactTags",        "contactTags",        filters, 200),
        ("contactLists",       "contactLists",       filters, 200),
        ("contactAutomations", "contactAutomations", filters, 200),
        ("fieldValues",        "fieldValues",        filters, 500),
        ("notes",              "notes",              filters, 200),
        ("deals",              "deals",              filters, 200),
    ])
    args.progress("Assembling report...")
    return {"contact": contact, "bulk": bulk}


def _name_lookups() -> dict:
    """Resolve foreign keys to human names via state.json (zero API calls)."""
    state = load_state() or {}
    tax = state.get("taxonomy", {})
    return {
        "tag_by_id": {str(t.get("id")): t.get("name") or t.get("tag")
                      for t in tax.get("tags", [])},
        "list_by_id": {str(_l.get("id")): _l.get("name")
                       for _l in tax.get("lists", [])},
        "auto_by_id": {str(a.get("id")): a.get("name")
                       for a in tax.get("automations", [])},
        "field_by_id": {
            str(f.get("id")): f.get("title")
            for f in tax.get("custom_fields", {}).get("contacts", [])
        },
    }


def analyze(data: dict) -> dict:
    c = data.get("contact")
    if c is None:
        return {"found": False}
    bulk = data["bulk"]
    names = _name_lookups()

    def _list_or_empty(label):
        v = bulk.get(label)
        return v if isinstance(v, list) else []

    tag_ids = [str(t.get("tag")) for t in _list_or_empty("contactTags")]
    list_ids = [str(_l.get("list")) for _l in _list_or_empty("contactLists")
                if str(_l.get("status")) == "1"]
    auto_rows = [
        {
            "automation_id": str(ca.get("automation")),
            "name": names["auto_by_id"].get(str(ca.get("automation")),
                                             ca.get("automation")),
            "status": ca.get("status"),
            "cdate": ca.get("cdate"),
        }
        for ca in _list_or_empty("contactAutomations")
    ]
    field_rows = [
        {
            "field_id": str(fv.get("field")),
            "name": names["field_by_id"].get(str(fv.get("field")),
                                              fv.get("field")),
            "value": sanitize(str(fv.get("value") or "")),
        }
        for fv in _list_or_empty("fieldValues")
        if fv.get("value")
    ]
    notes = _list_or_empty("notes")
    deals_value = bulk.get("deals")
    if isinstance(deals_value, dict) and deals_value.get("status_code") == 403:
        deal_rows = None
    else:
        deal_rows = [
            {
                "id": d.get("id"),
                "title": sanitize(d.get("title", "")),
                "value_cents": int(d.get("value", 0) or 0),
                "status": d.get("status"),
                "stage": d.get("stage"),
            }
            for d in (deals_value if isinstance(deals_value, list) else [])
        ]

    return {
        "found": True,
        "id": c.get("id"),
        "email": sanitize(c.get("email", "")),
        "name": (
            f"{sanitize(c.get('firstName', ''))} "
            f"{sanitize(c.get('lastName', ''))}".strip()
        ),
        "phone": sanitize(c.get("phone", "")),
        "orgname": sanitize(c.get("orgname", "")),
        "cdate": c.get("cdate"),
        "score": c.get("score"),
        "tags": [
            {"id": t, "name": names["tag_by_id"].get(t, t)}
            for t in tag_ids
        ],
        "lists": [
            {"id": _l, "name": names["list_by_id"].get(_l, _l)}
            for _l in list_ids
        ],
        "automations": auto_rows,
        "fields": field_rows,
        "notes": [
            {
                "id": n.get("id"),
                "text": sanitize(n.get("note", ""))[:300],
                "cdate": n.get("cdate"),
            }
            for n in notes
        ],
        "deals": deal_rows,
    }


def render_markdown(r: dict) -> str:
    if not r.get("found"):
        return "# Contact full profile\n\nNo contact found.\n"
    lines = [
        f"# {r['name']} ({r['email']})".strip(),
        "",
        f"- ID: **{r['id']}**",
        f"- Org: {r['orgname'] or '—'}",
        f"- Phone: {r['phone'] or '—'}",
        f"- Score: {r['score'] or '—'}",
        f"- Created: {r['cdate']}",
        "",
    ]
    if r["tags"]:
        lines.append("## Tags")
        for t in r["tags"]:
            lines.append(f"- `{t['name']}` (id={t['id']})")
        lines.append("")
    if r["lists"]:
        lines.append("## Subscribed lists")
        for _l in r["lists"]:
            lines.append(f"- {_l['name']} (id={_l['id']})")
        lines.append("")
    if r["automations"]:
        lines.append("## Automations")
        status_map = {"1": "active", "2": "completed"}
        for a in r["automations"]:
            lines.append(
                f"- `{a['name']}` (id={a['automation_id']}, "
                f"{status_map.get(str(a['status']), a['status'])}, "
                f"entered {a['cdate']})"
            )
        lines.append("")
    if r["fields"]:
        lines.append("## Custom fields")
        for f in r["fields"]:
            lines.append(f"- **{f['name']}**: {f['value']}")
        lines.append("")
    if r["deals"] is None:
        lines.append("## Deals\n\n_Deals feature not enabled on this AC plan._\n")
    elif r["deals"]:
        lines.append("## Deals")
        status_map = {"0": "open", "1": "won", "2": "lost", "3": "hot"}
        for d in r["deals"]:
            lines.append(
                f"- `{d['title']}` (id={d['id']}, "
                f"{status_map.get(str(d['status']), d['status'])}, "
                f"${d['value_cents']/100:,.2f})"
            )
        lines.append("")
    if r["notes"]:
        lines.append("## Notes")
        for n in r["notes"][:10]:
            lines.append(f"- ({n['cdate']}) {n['text']}")
        lines.append("")
    return "\n".join(lines) + "\n"


def main():
    cli_main(
        description="One-shot profile: contact + tags + lists + automations + fields + deals + notes",
        fetch_data=fetch_data,
        analyze=analyze,
        render_markdown=render_markdown,
        add_arguments=_add_args,
    )


if __name__ == "__main__":
    main()
