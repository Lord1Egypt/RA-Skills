#!/usr/bin/env python3
"""
deal_full_context.py — Everything about one deal in one report.

Pulls the deal record and its related sub-resources in parallel:
contact, tasks, notes, custom-field values, and the stage history we can
derive from /deals. Falls back gracefully on Lite plans.

Usage:
  python3 deal_full_context.py <deal_id>
  python3 deal_full_context.py 42 --format json
"""

from __future__ import annotations

from _ac_client import ACClient, ACClientError, cli_main, load_state, sanitize


def _add_args(parser):
    parser.add_argument("deal_id", help="ActiveCampaign deal id")


def fetch_data(client: ACClient, args) -> dict:
    cid = args.deal_id
    try:
        deal_res = client.get(f"deals/{cid}")
    except ACClientError as e:
        if e.status_code == 403:
            raise
        if e.status_code == 404:
            return {"not_found": True, "id": cid}
        raise
    deal = deal_res.get("deal") or {}
    contact_id = str(deal.get("contact") or "")

    # The three collection endpoints fan out in parallel.
    bulk = client.fetch_many([
        ("dealCustomFieldData", "dealCustomFieldData",
         {"filters[dealId]": cid}, 200),
        ("dealTasks",           "dealTasks",
         {"filters[relid]": cid, "filters[reltype]": "Deal"}, 200),
        ("notes",               "notes",
         {"filters[relid]": cid, "filters[reltype]": "Deal"}, 200),
    ])

    # Contact is a single-record endpoint; fetch directly. Cheap relative
    # to the other calls and avoids mixing paginate semantics with item-get.
    contact = None
    if contact_id:
        try:
            contact_res = client.get(f"contacts/{contact_id}")
            contact = contact_res.get("contact")
        except ACClientError:
            contact = None

    return {
        "deal": deal,
        "contact": contact,
        "bulk": bulk,
    }


def _name_lookups() -> dict:
    state = load_state() or {}
    tax = state.get("taxonomy", {})
    stages = {}
    for p in tax.get("pipelines", []):
        for s in p.get("stages", []):
            stages[str(s.get("id"))] = {
                "title": s.get("title"),
                "pipeline": p.get("name"),
            }
    pipelines = {str(p.get("id")): p.get("name") for p in tax.get("pipelines", [])}
    deal_fields = {
        str(f.get("id")): f.get("fieldLabel") or f.get("title")
        for f in tax.get("custom_fields", {}).get("deals", [])
    }
    return {"stages": stages, "pipelines": pipelines, "deal_fields": deal_fields}


def analyze(data: dict) -> dict:
    if data.get("not_found"):
        return {"found": False, "id": data["id"]}
    d = data["deal"]
    c = data.get("contact") or {}
    bulk = data["bulk"]
    names = _name_lookups()

    def _list_or_empty(label):
        v = bulk.get(label)
        return v if isinstance(v, list) else []

    stage = names["stages"].get(str(d.get("stage")), {})
    field_rows = [
        {
            "field_id": str(fv.get("customFieldId")),
            "name": names["deal_fields"].get(str(fv.get("customFieldId")),
                                              fv.get("customFieldId")),
            "value": sanitize(str(fv.get("fieldValue") or "")),
        }
        for fv in _list_or_empty("dealCustomFieldData")
        if fv.get("fieldValue")
    ]
    tasks = [
        {
            "id": t.get("id"),
            "title": sanitize(t.get("title", "")),
            "duedate": t.get("duedate"),
            "status": t.get("status"),
        }
        for t in _list_or_empty("dealTasks")
    ]
    notes = [
        {
            "id": n.get("id"),
            "text": sanitize(n.get("note", ""))[:300],
            "cdate": n.get("cdate"),
        }
        for n in _list_or_empty("notes")
    ]

    return {
        "found": True,
        "id": d.get("id"),
        "title": sanitize(d.get("title", "")),
        "value_cents": int(d.get("value", 0) or 0),
        "currency": d.get("currency"),
        "status": d.get("status"),
        "stage_id": d.get("stage"),
        "stage_title": stage.get("title", "—"),
        "pipeline": stage.get("pipeline") or
                    names["pipelines"].get(str(d.get("group")), "—"),
        "owner_id": d.get("owner"),
        "cdate": d.get("cdate"),
        "mdate": d.get("mdate"),
        "nextdate": d.get("nextdate"),
        "edate": d.get("edate"),
        "contact": {
            "id": c.get("id"),
            "email": sanitize(c.get("email", "")),
            "name": (
                f"{sanitize(c.get('firstName', ''))} "
                f"{sanitize(c.get('lastName', ''))}".strip()
            ),
        } if c else None,
        "fields": field_rows,
        "tasks": tasks,
        "notes": notes,
    }


def render_markdown(r: dict) -> str:
    if not r["found"]:
        return f"# Deal full context\n\nNo deal found with id `{r['id']}`.\n"
    status_map = {"0": "open", "1": "won", "2": "lost", "3": "hot"}
    val_str = f"${r['value_cents']/100:,.2f}" if r["value_cents"] else "—"
    lines = [
        f"# Deal {r['id']}: {r['title']}".rstrip(": "),
        "",
        f"- Pipeline: **{r['pipeline']}** / stage **{r['stage_title']}**",
        f"- Value: **{val_str}** {r['currency'] or ''}".rstrip(),
        f"- Status: {status_map.get(str(r['status']), r['status'])}",
        f"- Owner id: {r['owner_id']}",
        f"- Created: {r['cdate']}",
        f"- Last modified: {r['mdate']}",
        f"- Next activity: {r['nextdate'] or '—'}",
        f"- Close date: {r['edate'] or '—'}",
        "",
    ]
    if r["contact"]:
        c = r["contact"]
        lines.append("## Contact")
        lines.append(f"- {c['name']} ({c['email']}) — id={c['id']}")
        lines.append("")
    if r["fields"]:
        lines.append("## Custom fields")
        for f in r["fields"]:
            lines.append(f"- **{f['name']}**: {f['value']}")
        lines.append("")
    if r["tasks"]:
        lines.append("## Open tasks")
        for t in r["tasks"]:
            done = "✓" if str(t["status"]) == "1" else "○"
            lines.append(f"- {done} `{t['title']}` (due {t['duedate'] or '—'})")
        lines.append("")
    if r["notes"]:
        lines.append("## Notes")
        for n in r["notes"][:10]:
            lines.append(f"- ({n['cdate']}) {n['text']}")
        lines.append("")
    return "\n".join(lines) + "\n"


def main():
    cli_main(
        description="One-shot context: deal + contact + tasks + notes + fields",
        fetch_data=fetch_data,
        analyze=analyze,
        render_markdown=render_markdown,
        add_arguments=_add_args,
        feature_unavailable=(
            "Deals (CRM)", "Plus",
            "Deal full context needs the /deals endpoint.",
        ),
    )


if __name__ == "__main__":
    main()
