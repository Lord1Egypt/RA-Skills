#!/usr/bin/env python3
"""
forms_lead_quality.py — Per-form lead quality from list-membership proxy.

AC v3 does NOT expose a /formSubmissions endpoint, so this script
approximates per-form lead quality by:

  1. Pulling /forms (form definitions, including each form's
     subscribelist — the list contacts are added to on submit).
  2. For each form, sampling recent contacts on that subscribelist
     via /contacts?listid=<id>.
  3. Pulling each contact's score and recent campaign engagement
     (opens / clicks / bounces / unsubs from /linkData or
     /messageActivities), using the existing client helper.

Caveats (printed in the report):
  - Contacts can join a list from multiple sources, not just the form.
    If your subscribelist has a paid-import or another opt-in path,
    quality numbers will not isolate the form.
  - Bounce/unsub status reflects the contact's lifetime state, not the
    state at the moment of submission.
  - The sampling cap (--max-contacts-per-form, default 1000) keeps
    runtime reasonable on large lists.

Usage:
  python3 forms_lead_quality.py
  python3 forms_lead_quality.py --max-contacts-per-form 500 --window-days 90
  python3 forms_lead_quality.py --format json --output forms_lq.json
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

from _ac_client import ACClient, emit_files


def _form_subscribelists(form: dict) -> list[str]:
    """Form objects expose the target list in a few historical shapes."""
    raw = form.get("subscribelist") or form.get("subscribeList") or form.get("list")
    if not raw:
        return []
    if isinstance(raw, list):
        return [str(x) for x in raw if x]
    if isinstance(raw, dict):
        return [str(v) for v in raw.values() if v]
    return [str(raw)]


def fetch_data(client: ACClient, max_contacts_per_form: int = 1000,
               window_days: int = 90) -> dict:
    forms = client.paginate("forms", "forms", max_items=2000)

    contacts_by_form = {}
    cutoff = (datetime.now(timezone.utc) - timedelta(days=window_days)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    for f in forms:
        list_ids = _form_subscribelists(f)
        contacts = []
        for lid in list_ids:
            chunk = client.paginate(
                "contacts", "contacts",
                params={"listid": lid, "filters[created_after]": cutoff},
                max_items=max_contacts_per_form,
            )
            contacts.extend(chunk)
        # de-dupe by id
        seen = set()
        deduped = []
        for c in contacts:
            cid = str(c.get("id"))
            if cid and cid not in seen:
                seen.add(cid)
                deduped.append(c)
        contacts_by_form[str(f["id"])] = deduped

    # engagement signal across ALL contacts the script touched
    all_contact_ids = set()
    for cs in contacts_by_form.values():
        for c in cs:
            all_contact_ids.add(str(c.get("id")))

    events = client.fetch_engagement_events(max_items=30000, quiet=True)
    events_by_contact: dict[str, list] = defaultdict(list)
    for ev in events:
        cid = ev.get("contact")
        if cid in all_contact_ids:
            events_by_contact[cid].append(ev)

    return {
        "forms": forms,
        "contacts_by_form": contacts_by_form,
        "events_by_contact": dict(events_by_contact),
        "window_days": window_days,
    }


def analyze(data: dict, now: datetime | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    forms = data["forms"]
    by_form = data["contacts_by_form"]
    events_by_contact = data["events_by_contact"]

    rows = []
    for f in forms:
        fid = str(f["id"])
        contacts = by_form.get(fid, [])
        n_contacts = len(contacts)

        bounced = sum(1 for c in contacts if str(c.get("bounced_hard", "0")) == "1")
        unsubscribed = sum(1 for c in contacts if str(c.get("udate", "")) and str(c.get("status", "")) == "2")
        scores = []
        for c in contacts:
            try:
                v = float(c.get("score") or 0)
            except (ValueError, TypeError):
                v = 0
            scores.append(v)
        avg_score = sum(scores) / n_contacts if n_contacts else 0

        engaged = 0
        for c in contacts:
            evs = events_by_contact.get(str(c.get("id")), [])
            if any(e.get("event") in ("open", "click") for e in evs):
                engaged += 1

        engagement_rate = engaged / n_contacts if n_contacts else 0
        bounce_rate = bounced / n_contacts if n_contacts else 0
        unsub_rate = unsubscribed / n_contacts if n_contacts else 0

        rows.append({
            "id": fid,
            "name": f.get("name", ""),
            "subscribelists": _form_subscribelists(f),
            "contacts_sampled": n_contacts,
            "engagement_rate": engagement_rate,
            "avg_score": round(avg_score, 1),
            "bounce_rate": bounce_rate,
            "unsub_rate": unsub_rate,
        })

    rows.sort(key=lambda r: -r["engagement_rate"])

    return {
        "total_forms": len(forms),
        "window_days": data["window_days"],
        "forms": rows,
        "best": rows[:5],
        "worst": [r for r in rows if r["contacts_sampled"] >= 10][-5:][::-1],
    }


def render_markdown(r: dict) -> str:
    lines = [
        "# Forms — Lead Quality",
        "",
        f"- Window: last **{r['window_days']} days**",
        f"- Forms scanned: **{r['total_forms']}**",
        "",
        "*Quality is approximated from the form's subscribelist members. "
        "If a list has multiple opt-in sources, this is a list-quality reading, "
        "not strictly a per-form reading.*",
        "",
    ]
    if r["forms"]:
        lines.append("## Per-form lead quality")
        lines.append("")
        lines.append("| Form | Sampled | Engaged | Avg score | Bounce | Unsub |")
        lines.append("|---|---:|---:|---:|---:|---:|")
        for f in r["forms"][:30]:
            lines.append(
                f"| `{f['name']}` | {f['contacts_sampled']} | "
                f"{f['engagement_rate']*100:.1f}% | {f['avg_score']} | "
                f"{f['bounce_rate']*100:.1f}% | {f['unsub_rate']*100:.1f}% |"
            )
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Per-form lead quality (subscribelist-membership proxy)"
    )
    parser.add_argument("--max-contacts-per-form", type=int, default=1000)
    parser.add_argument("--window-days", type=int, default=90)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    client = ACClient()
    data = fetch_data(client, max_contacts_per_form=args.max_contacts_per_form,
                      window_days=args.window_days)
    report = analyze(data)
    out = json.dumps(report, indent=2) if args.format == "json" else render_markdown(report)

    if args.output:
        path = Path(args.output)
        path.write_text(out)
        print(f"Wrote {path}")
        emit_files(path)
    else:
        print(out)


if __name__ == "__main__":
    main()
