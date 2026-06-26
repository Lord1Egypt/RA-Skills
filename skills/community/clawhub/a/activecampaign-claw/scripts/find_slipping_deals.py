#!/usr/bin/env python3
"""
find_slipping_deals.py — Surface deals that are stale or past expected close.

Produces a prioritized list of deals needing attention, ranked by
(days overdue × value) for maximum revenue-impact visibility.

Usage:
  python3 find_slipping_deals.py                  # markdown, 14-day stale threshold
  python3 find_slipping_deals.py --stale-days 7   # tighter threshold
  python3 find_slipping_deals.py --pipeline 1     # specific pipeline only
  python3 find_slipping_deals.py --top 5          # top 5 only
  python3 find_slipping_deals.py --format json

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
    ensure_state,
    load_history,
    log_outcome,
    render_feature_unavailable,
    sanitize,
    write_insight,
    write_report,
)
from _ac_client import (
    safe_int as _safe_int,
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


def fetch_open_deals(client: ACClient, pipeline_id: str | None = None) -> list[dict] | dict:
    params: dict = {"filters[status]": "0"}
    if pipeline_id:
        params["filters[d_groupid]"] = pipeline_id
    try:
        return client.paginate("deals", "deals", params=params, max_items=1000)
    except ACClientError as e:
        if e.status_code == 403:
            return {"unavailable": True}
        raise


def analyze_deals(deals: list[dict], state: dict,
                  stale_days: int = 14) -> dict:
    stage_map = {}
    for p in state.get("taxonomy", {}).get("pipelines", []):
        for s in p.get("stages", []):
            stage_map[s["id"]] = {"title": s["title"], "pipeline": p["name"]}

    slipping = []
    stale = []
    data_issues = []
    stage_counts: dict[str, dict] = {}

    for d in deals:
        deal_id = d.get("id", "")
        title = sanitize(d.get("title", "Untitled"))
        value = _safe_int(d.get("value"))
        stage_id = d.get("stage", "")
        stage_info = stage_map.get(stage_id, {"title": "Unknown", "pipeline": "Unknown"})
        owner = d.get("owner", "")

        days_since_mod = _days_ago(d.get("mdate"))
        days_overdue = _days_ago(d.get("nextdate"))

        deal_record = {
            "id": deal_id,
            "title": title,
            "value_cents": value,
            "value_display": f"${value/100:,.0f}" if value else "$0",
            "stage": stage_info["title"],
            "pipeline": stage_info["pipeline"],
            "owner": owner,
            "days_since_activity": round(days_since_mod, 1) if days_since_mod else None,
            "days_overdue": round(days_overdue, 1) if days_overdue and days_overdue > 0 else None,
            "urgency_score": 0,
        }

        # Slipping: past expected close date
        if days_overdue is not None and days_overdue > 0:
            deal_record["urgency_score"] = days_overdue * (value / 100)
            slipping.append(deal_record)

        # Stale: no activity in threshold days
        if days_since_mod is not None and days_since_mod > stale_days:
            if deal_record["urgency_score"] == 0:
                deal_record["urgency_score"] = days_since_mod * (value / 100)
            stale.append(deal_record)

        # Data quality issues
        issues = []
        if not d.get("nextdate"):
            issues.append("missing close date")
        if value == 0:
            issues.append("$0 value")
        if not owner or owner == "0":
            issues.append("no owner")
        if issues:
            deal_record["issues"] = issues
            data_issues.append(deal_record)

        # Stage distribution
        stage_name = stage_info["title"]
        if stage_name not in stage_counts:
            stage_counts[stage_name] = {"count": 0, "value": 0}
        stage_counts[stage_name]["count"] += 1
        stage_counts[stage_name]["value"] += value

    slipping.sort(key=lambda x: -x["urgency_score"])
    stale.sort(key=lambda x: -x["urgency_score"])

    total_open = len(deals)
    total_value = sum(_safe_int(d.get("value")) for d in deals)

    return {
        "summary": {
            "total_open": total_open,
            "total_value_cents": total_value,
            "total_value_display": f"${total_value/100:,.0f}",
        },
        "slipping": slipping,
        "stale": stale,
        "data_issues": data_issues,
        "stage_distribution": stage_counts,
    }


def generate_actions(analysis: dict) -> list[str]:
    actions = []
    for d in analysis["slipping"][:3]:
        actions.append(
            f"{d['title']}: {d.get('days_overdue', 0):.0f} days overdue "
            f"({d['value_display']}). Call today or move to Lost."
        )
    for d in analysis["stale"][:3]:
        if d not in analysis["slipping"][:3]:
            actions.append(
                f"{d['title']}: {d.get('days_since_activity', 0):.0f} days stale "
                f"({d['value_display']}). Follow up or reassign."
            )
    if analysis["data_issues"]:
        count = len(analysis["data_issues"])
        actions.append(f"{count} deal(s) with data quality issues — review and fix.")
    return actions


def format_markdown(analysis: dict, top: int) -> str:
    lines = []
    s = analysis["summary"]

    lines.append("## Pipeline summary\n")
    lines.append(f"**{s['total_open']} open deals** | **{s['total_value_display']}** total value\n")

    if analysis["stage_distribution"]:
        lines.append("| Stage | Deals | Value |")
        lines.append("|---|---|---|")
        for stage, data in analysis["stage_distribution"].items():
            lines.append(
                f"| {stage} | {data['count']} | ${data['value']/100:,.0f} |"
            )

    if analysis["slipping"]:
        lines.append(f"\n## Slipping deals ({len(analysis['slipping'])})\n")
        lines.append("| Deal | Value | Days overdue | Last activity |")
        lines.append("|---|---|---|---|")
        for d in analysis["slipping"][:top]:
            lines.append(
                f"| {d['title']} | {d['value_display']} | "
                f"{d.get('days_overdue', 0):.0f} days | "
                f"{d.get('days_since_activity', '?'):.0f} days ago |"
            )
    else:
        lines.append("\n## Slipping deals\n\nNone — all deals are within expected close dates. ✅")

    if analysis["stale"]:
        lines.append(f"\n## Stale deals — no recent activity ({len(analysis['stale'])})\n")
        lines.append("| Deal | Value | Stage | Days since activity |")
        lines.append("|---|---|---|---|")
        for d in analysis["stale"][:top]:
            lines.append(
                f"| {d['title']} | {d['value_display']} | "
                f"{d['stage']} | {d.get('days_since_activity', '?'):.0f} days |"
            )
    else:
        lines.append("\n## Stale deals\n\nNone — all deals have recent activity. ✅")

    if analysis["data_issues"]:
        lines.append(f"\n## Data quality issues ({len(analysis['data_issues'])})\n")
        for d in analysis["data_issues"][:top]:
            issues_str = ", ".join(d.get("issues", []))
            lines.append(f"- **{d['title']}** ({d['value_display']}): {issues_str}")
    else:
        lines.append("\n## Data quality\n\nAll deals have complete data. ✅")

    actions = generate_actions(analysis)
    if actions:
        lines.append("\n## Recommended actions\n")
        for i, a in enumerate(actions, 1):
            lines.append(f"{i}. {a}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Find slipping deals")
    parser.add_argument("--stale-days", type=int, default=14)
    parser.add_argument("--pipeline", type=str, default=None)
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()

    state = ensure_state()
    client = ACClient()

    print("→ Fetching open deals...", file=sys.stderr)
    deals = fetch_open_deals(client, pipeline_id=args.pipeline)

    if isinstance(deals, dict) and deals.get("unavailable"):
        print(render_feature_unavailable(
            "Deals (CRM)", "Plus",
            "Slipping-deals analysis needs the /deals endpoint.",
        ))
        return

    print("→ Analyzing pipeline...", file=sys.stderr)
    analysis = analyze_deals(deals, state, stale_days=args.stale_days)

    current_metrics = {
        "total_open": analysis["summary"]["total_open"],
        "total_value": analysis["summary"]["total_value_cents"],
        "slipping": len(analysis["slipping"]),
        "stale": len(analysis["stale"]),
        "data_issues": len(analysis["data_issues"]),
    }

    if args.format == "json":
        output = json.dumps(analysis, indent=2, default=str)
    else:
        content = format_markdown(analysis, args.top)
        trends = compare_to_previous(
            "deal-hygiene", current_metrics,
            ["total_open", "slipping", "stale", "data_issues"],
        )
        if trends:
            content += "\n\n" + trends
        patterns = detect_patterns()
        if patterns:
            content += "\n\n## Proactive suggestions\n"
            for p in patterns:
                content += f"\n- {p}"
            content += "\n"
        output = write_report("Deal Hygiene Report", content)

    if args.output:
        Path(args.output).write_text(output)
        print(f"✓ Report written to {args.output}", file=sys.stderr)
    else:
        print(output)

    history = load_history(recipe="deal-hygiene", limit=3)
    if len(history) >= 3:
        slipping_counts = [h.get("slipping", 0) for h in history[:3]]
        if all(isinstance(v, (int, float)) for v in slipping_counts):
            if slipping_counts[0] > slipping_counts[1] > slipping_counts[2]:
                write_insight(
                    f"Slipping deals count increasing 3 runs in a row: "
                    f"{slipping_counts[2]} → {slipping_counts[1]} → {slipping_counts[0]}. "
                    f"Pipeline velocity may be degrading.",
                    category="risk",
                )

    log_outcome(
        "deal_hygiene_executed",
        recipe="deal-hygiene",
        total_open=analysis["summary"]["total_open"],
        total_value=analysis["summary"]["total_value_cents"],
        slipping=len(analysis["slipping"]),
        stale=len(analysis["stale"]),
        data_issues=len(analysis["data_issues"]),
    )


if __name__ == "__main__":
    main()
