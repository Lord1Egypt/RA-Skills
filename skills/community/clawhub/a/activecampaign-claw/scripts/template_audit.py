#!/usr/bin/env python3
"""
template_audit.py — Audit campaign email templates and their usage.

Cross-references /templates against /campaigns to find:

  - templates referenced in recent campaigns vs. never used
  - stale templates (last modified > N days ago)
  - longest / shortest templates (length distribution sanity check)
  - templates whose linked campaigns underperform (open rate vs. baseline)

Note: v3 `/templates` covers campaign/email-designer templates only.
Transactional Email templates use a separate Postmark-based API outside
v3 and are NOT exposed by this endpoint.

Usage:
  python3 template_audit.py
  python3 template_audit.py --stale-days 180
  python3 template_audit.py --format json --output template_audit.json
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone

from _ac_client import ACClient, cli_main
from _ac_client import parse_date as _parse_date


def fetch_data(client: ACClient) -> dict:
    templates = client.paginate("templates", "templates", max_items=2000)
    campaigns = client.paginate("campaigns", "campaigns", max_items=2000)
    return {"templates": templates, "campaigns": campaigns}


def _detect_template_id(campaign: dict) -> str | None:
    # Campaigns reference template id under several historical field names
    # depending on plan + campaign type. Cover the common ones.
    for key in ("templateid", "template", "messageTemplate", "designid"):
        v = campaign.get(key)
        if v:
            return str(v)
    return None


def analyze(data: dict, stale_days: int = 180, now: datetime | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    templates = data["templates"]
    campaigns = data["campaigns"]

    template_by_id = {str(t["id"]): t for t in templates}

    usage = defaultdict(list)  # template_id -> [campaign dicts]
    name_hits = defaultdict(int)  # fallback match by name

    for c in campaigns:
        tid = _detect_template_id(c)
        if tid and tid in template_by_id:
            usage[tid].append(c)
        elif c.get("name"):
            for t in templates:
                tname = (t.get("name") or "").strip()
                if tname and tname.lower() in c["name"].lower():
                    name_hits[str(t["id"])] += 1

    rows = []
    for t in templates:
        tid = str(t["id"])
        used_in = usage.get(tid, [])
        last_mod = _parse_date(t.get("mdate") or t.get("cdate"))
        days_since_modified = (now - last_mod).days if last_mod else None
        content_len = len(t.get("content") or "") or 0

        # average open rate across linked campaigns (when present)
        open_rates = []
        for c in used_in:
            try:
                sends = int(c.get("send_amt", 0) or 0)
                uo = int(c.get("uniqueopens", 0) or 0)
                if sends:
                    open_rates.append(uo / sends)
            except (ValueError, TypeError):
                continue
        avg_open = sum(open_rates) / len(open_rates) if open_rates else None

        rows.append({
            "id": tid,
            "name": t.get("name", ""),
            "subject": t.get("subject", ""),
            "content_len": content_len,
            "days_since_modified": days_since_modified,
            "campaign_uses": len(used_in),
            "name_match_uses": name_hits.get(tid, 0),
            "avg_open_rate": avg_open,
        })

    rows.sort(key=lambda r: -r["campaign_uses"])

    unused = [r for r in rows if r["campaign_uses"] == 0 and r["name_match_uses"] == 0]
    stale = [
        r for r in rows
        if r["days_since_modified"] is not None and r["days_since_modified"] >= stale_days
    ]
    too_short = [r for r in rows if 0 < r["content_len"] < 200]
    too_long = sorted(
        [r for r in rows if r["content_len"] > 50000],
        key=lambda r: -r["content_len"],
    )

    return {
        "total_templates": len(templates),
        "total_campaigns_scanned": len(campaigns),
        "unused": unused,
        "stale": stale,
        "too_short": too_short,
        "too_long": too_long[:10],
        "stale_days_threshold": stale_days,
        "templates": rows,
    }


def render_markdown(r: dict) -> str:
    lines = [
        "# Template Audit",
        "",
        f"- Total campaign templates: **{r['total_templates']}**",
        f"- Campaigns scanned for usage references: {r['total_campaigns_scanned']}",
        f"- Unused templates (no campaign reference, no name match): **{len(r['unused'])}**",
        f"- Stale templates (last modified ≥{r['stale_days_threshold']}d ago): **{len(r['stale'])}**",
        f"- Suspiciously short (<200 chars): **{len(r['too_short'])}**",
        f"- Very long (>50KB): **{len(r['too_long'])}**",
        "",
    ]
    if r["templates"]:
        lines.append("## Top templates by campaign use")
        lines.append("")
        lines.append("| Template | Subject | Uses | Avg open rate | Last modified |")
        lines.append("|---|---|---:|---:|---:|")
        for t in r["templates"][:15]:
            open_rate = (
                f"{t['avg_open_rate']*100:.1f}%"
                if t["avg_open_rate"] is not None else "—"
            )
            mod = (
                f"{t['days_since_modified']}d ago"
                if t["days_since_modified"] is not None else "—"
            )
            lines.append(
                f"| `{t['name']}` | {t['subject']} | {t['campaign_uses']} | {open_rate} | {mod} |"
            )
        lines.append("")
    if r["unused"]:
        lines.append("## Unused templates (candidates for archive)")
        lines.append("")
        for t in r["unused"][:50]:
            lines.append(f"- `{t['name']}` (id={t['id']})")
        lines.append("")
    return "\n".join(lines)


def _add_args(parser):
    parser.add_argument("--stale-days", type=int, default=180)


def _analyze(data, args):
    return analyze(data, stale_days=args.stale_days)


def main():
    cli_main(
        description="Audit campaign templates",
        fetch_data=fetch_data,
        analyze=_analyze,
        render_markdown=render_markdown,
        add_arguments=_add_args,
    )


if __name__ == "__main__":
    main()
