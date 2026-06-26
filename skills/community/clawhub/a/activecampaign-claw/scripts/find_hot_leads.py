#!/usr/bin/env python3
"""
find_hot_leads.py — Rank contacts by lead heat using scores, deal activity, and tags.

Produces a ranked list of the hottest leads with reasons and recommended actions.

Usage:
  python3 find_hot_leads.py              # top 10, markdown
  python3 find_hot_leads.py --top 5      # top 5
  python3 find_hot_leads.py --format json
  python3 find_hot_leads.py --min-score 50

Required: ~/.activecampaign-skill/state.json (run calibrate.py first)
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from _ac_client import (
    ACClient,
    ACClientError,
    compare_to_previous,
    detect_patterns,
    emit_files,
    ensure_state,
    load_history,
    log_outcome,
    sanitize,
    write_insight,
    write_report,
)
from _ac_client import (
    safe_float as _safe_float,
)


def _days_ago(iso_str: str | None) -> float | None:
    if not iso_str:
        return None
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - dt).total_seconds() / 86400
    except (ValueError, TypeError):
        return None


def fetch_contacts_with_scores(client: ACClient, max_contacts: int = 500,
                               max_aux: int = 50000) -> list[dict]:
    """Enrich contacts with their best score + tag ids.

    Uses bulk endpoints (`/scoreValues`, `/contactTags`) and joins client-side,
    instead of fetching per-contact subresources. This collapses 2N+1 calls
    into ~3 — critical for accounts with thousands of contacts.

    `max_aux` caps the auxiliary collection pulls so a very large account
    doesn't OOM. Default 50k covers the typical Plus-tier scoring library;
    raise via `--max-aux` on the CLI if you've calibrated and need more.
    """
    contacts = client.paginate("contacts", "contacts", max_items=max_contacts)

    try:
        all_scores = client.paginate("scoreValues", "scoreValues", max_items=max_aux)
    except Exception:
        all_scores = []
    try:
        all_tags = client.paginate("contactTags", "contactTags", max_items=max_aux)
    except Exception:
        all_tags = []

    best_by_contact: dict[str, float] = {}
    for sv in all_scores:
        cid = str(sv.get("contact") or "")
        if not cid:
            continue
        val = _safe_float(sv.get("score_value"))
        if val > best_by_contact.get(cid, 0):
            best_by_contact[cid] = val

    tags_by_contact: dict[str, list] = {}
    for ct in all_tags:
        cid = str(ct.get("contact") or "")
        if cid:
            tags_by_contact.setdefault(cid, []).append(ct.get("tag"))

    enriched = []
    for c in contacts:
        cid = str(c.get("id", ""))
        enriched.append({
            "id": cid,
            "email": sanitize(c.get("email", "")),
            "first_name": sanitize(c.get("firstName", "")),
            "last_name": sanitize(c.get("lastName", "")),
            "score": best_by_contact.get(cid, 0),
            "cdate": c.get("cdate"),
            "mdate": c.get("mdate"),
            "tag_ids": tags_by_contact.get(cid, []),
        })
    return enriched


def fetch_open_deals_by_contact(client: ACClient) -> dict[str, list[dict]]:
    try:
        deals = client.paginate("deals", "deals", params={"filters[status]": "0"}, max_items=500)
    except ACClientError as e:
        if e.status_code == 403:
            # Deals feature not on plan — return empty mapping; scoring still works
            # off the contact-score + tag signals.
            return {}
        raise
    by_contact: dict[str, list[dict]] = {}
    for d in deals:
        contact = d.get("contact")
        if contact:
            by_contact.setdefault(contact, []).append({
                "id": d.get("id"),
                "title": d.get("title"),
                "value": int(_safe_float(d.get("value"))),
                "stage": d.get("stage"),
                "mdate": d.get("mdate"),
            })
    return by_contact


def score_leads(contacts: list[dict], deals_by_contact: dict,
                state: dict, min_score: float = 0) -> list[dict]:
    tag_taxonomy = {t["id"]: t["name"] for t in state.get("taxonomy", {}).get("tags", [])}
    valuable_tags = {"vip", "customer", "hot lead", "enterprise", "paid"}

    scored = []
    for c in contacts:
        signals = []
        heat = c["score"]

        # Boost for recent modification
        days_since_mod = _days_ago(c.get("mdate"))
        if days_since_mod is not None and days_since_mod < 7:
            heat += 20
            signals.append("Active in last 7 days")
        elif days_since_mod is not None and days_since_mod < 30:
            heat += 10
            signals.append("Active in last 30 days")

        # Boost for valuable tags
        for tid in c.get("tag_ids", []):
            tag_name = tag_taxonomy.get(tid, "").lower()
            if tag_name in valuable_tags:
                heat += 15
                signals.append(f"Tag: {tag_taxonomy.get(tid, tid)}")

        # Boost for open deals
        contact_deals = deals_by_contact.get(c["id"], [])
        if contact_deals:
            total_deal_value = sum(d["value"] for d in contact_deals)
            heat += min(30, total_deal_value // 10000)
            signals.append(f"{len(contact_deals)} open deal(s), ${total_deal_value/100:,.0f}")

            for d in contact_deals:
                deal_days = _days_ago(d.get("mdate"))
                if deal_days is not None and deal_days < 3:
                    heat += 10
                    signals.append(f"Deal '{d['title']}' updated recently")

        # Boost for newness (recent signup)
        days_since_create = _days_ago(c.get("cdate"))
        if days_since_create is not None and days_since_create < 14:
            heat += 10
            signals.append("New contact (< 14 days)")

        if heat < min_score:
            continue

        action = "Review and assess"
        if heat >= 80 and contact_deals:
            action = "Call today — high-value active lead"
        elif heat >= 80:
            action = "Reach out — high engagement, no deal yet"
        elif heat >= 50 and contact_deals:
            action = "Follow up on open deal"
        elif heat >= 50:
            action = "Send targeted content"

        scored.append({
            "id": c["id"],
            "email": c["email"],
            "name": f"{c['first_name']} {c['last_name']}".strip(),
            "score": c["score"],
            "heat": round(heat),
            "signals": signals,
            "action": action,
            "deals": contact_deals,
        })

    scored.sort(key=lambda x: -x["heat"])
    return scored


def format_markdown(leads: list[dict], top: int) -> str:
    lines = []
    display = leads[:top]

    if not display:
        lines.append("No leads found matching the criteria.")
        return "\n".join(lines)

    lines.append("## Top leads by heat score\n")
    lines.append("| Rank | Name | Email | AC Score | Heat | Top signal | Action |")
    lines.append("|---|---|---|---|---|---|---|")
    for i, lead in enumerate(display, 1):
        top_signal = lead["signals"][0] if lead["signals"] else "—"
        lines.append(
            f"| {i} | {lead['name'] or '—'} | {lead['email']} | "
            f"{lead['score']:.0f} | **{lead['heat']}** | {top_signal} | {lead['action']} |"
        )

    lines.append("\n## Signal details\n")
    for i, lead in enumerate(display, 1):
        lines.append(f"### {i}. {lead['name'] or lead['email']}")
        for s in lead["signals"]:
            lines.append(f"  - {s}")
        if lead["deals"]:
            for d in lead["deals"]:
                lines.append(f"  - Deal: {d['title']} (${d['value']/100:,.0f})")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Find hot leads")
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--min-score", type=float, default=0)
    parser.add_argument("--max-contacts", type=int, default=5000,
                        help="Cap the contact-scan size (default: 5000)")
    parser.add_argument("--max-aux", type=int, default=50000,
                        help="Cap the /scoreValues + /contactTags bulk pulls (default: 50000)")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()

    state = ensure_state()
    client = ACClient()

    print("→ Fetching contacts with scores...", file=sys.stderr)
    contacts = fetch_contacts_with_scores(
        client, max_contacts=args.max_contacts, max_aux=args.max_aux,
    )

    print("→ Fetching open deals...", file=sys.stderr)
    deals_by_contact = fetch_open_deals_by_contact(client)

    print("→ Scoring leads...", file=sys.stderr)
    leads = score_leads(contacts, deals_by_contact, state, min_score=args.min_score)

    current_metrics = {
        "total_scored": len(leads),
        "top_heat": leads[0]["heat"] if leads else 0,
        "displayed": min(args.top, len(leads)),
    }

    if args.format == "json":
        output = json.dumps(leads[:args.top], indent=2)
    else:
        content = format_markdown(leads, args.top)
        trends = compare_to_previous(
            "find-hot-leads", current_metrics, ["total_scored", "top_heat"],
        )
        if trends:
            content += "\n\n" + trends
        patterns = detect_patterns()
        if patterns:
            content += "\n\n## Proactive suggestions\n"
            for p in patterns:
                content += f"\n- {p}"
            content += "\n"
        output = write_report("Hot Leads Report", content)

    if args.output:
        Path(args.output).write_text(output)
        print(f"✓ Report written to {args.output}", file=sys.stderr)
        emit_files(args.output)
    else:
        print(output)

    history = load_history(recipe="find-hot-leads", limit=3)
    if len(history) >= 3:
        heat_vals = [h.get("top_heat", 0) for h in history[:3]]
        if all(isinstance(v, (int, float)) for v in heat_vals):
            if heat_vals[0] > heat_vals[1] > heat_vals[2]:
                write_insight(
                    f"Top lead heat score has declined 3 consecutive runs: "
                    f"{heat_vals[2]} → {heat_vals[1]} → {heat_vals[0]}. "
                    f"Lead engagement may be cooling across the account.",
                    category="trend",
                )

    log_outcome(
        "hot_leads_generated",
        recipe="find-hot-leads",
        total_scored=len(leads),
        top_heat=leads[0]["heat"] if leads else 0,
        displayed=min(args.top, len(leads)),
    )


if __name__ == "__main__":
    main()
