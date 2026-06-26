#!/usr/bin/env python3
"""
pipeline_audit.py — Per-pipeline / per-stage health for sales pipelines.

Reports deal count, total value, % of deals with required custom fields
populated, and stages with zero deals in 90 days. Excludes time-in-stage
(AC's v3 API does not expose stage-movement timestamps cleanly).

Requires the Deals feature on the AC account.

Usage:
  python3 pipeline_audit.py
  python3 pipeline_audit.py --format json
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from _ac_client import ACClient, ACClientError, render_feature_unavailable


def fetch(client: ACClient) -> dict:
    try:
        pipelines = client.paginate("dealGroups", "dealGroups", max_items=200)
        stages = client.paginate("dealStages", "dealStages", max_items=500)
        deals = client.paginate("deals", "deals", max_items=20000)
        deal_fields = client.get("dealCustomFieldMeta").get("dealCustomFieldMeta", [])
        deal_field_data = client.paginate("dealCustomFieldData", "dealCustomFieldData", max_items=50000)
    except ACClientError as e:
        if e.status_code == 403:
            return {"unavailable": True}
        raise
    return {
        "pipelines": pipelines,
        "stages": stages,
        "deals": deals,
        "fields": deal_fields,
        "field_data": deal_field_data,
    }


def _days_ago(iso_str):
    if not iso_str:
        return None
    try:
        dt = datetime.fromisoformat(str(iso_str).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - dt).total_seconds() / 86400
    except Exception:
        return None


def analyze(data: dict) -> dict:
    if data.get("unavailable"):
        return {"unavailable": True}
    deals_by_pipeline = defaultdict(list)
    deals_by_stage = defaultdict(list)
    for d in data["deals"]:
        deals_by_pipeline[str(d.get("group"))].append(d)
        deals_by_stage[str(d.get("stage"))].append(d)

    field_data_by_deal = defaultdict(dict)
    for fd in data["field_data"]:
        field_data_by_deal[str(fd.get("dealId"))][str(fd.get("customFieldId"))] = fd.get("fieldValue")

    pipeline_rows = []
    stage_rows = []
    for p in data["pipelines"]:
        pid = str(p["id"])
        p_deals = deals_by_pipeline.get(pid, [])
        total_value = sum(int(d.get("value") or 0) for d in p_deals)
        pipeline_rows.append({
            "id": pid,
            "name": p.get("title"),
            "deal_count": len(p_deals),
            "total_value_cents": total_value,
        })
        for s in data["stages"]:
            if str(s.get("group")) != pid:
                continue
            s_deals = deals_by_stage.get(str(s["id"]), [])
            recent_count = sum(1 for d in s_deals if _days_ago(d.get("cdate")) is not None and _days_ago(d.get("cdate")) <= 90)
            stage_rows.append({
                "pipeline": p.get("title"),
                "stage": s.get("title"),
                "stage_id": s["id"],
                "deal_count": len(s_deals),
                "recent_90d": recent_count,
                "stale": recent_count == 0,
            })

    # field completeness on deals
    field_completeness = []
    for f in data["fields"]:
        fid = str(f.get("id"))
        populated = sum(1 for v in field_data_by_deal.values() if v.get(fid))
        field_completeness.append({
            "field": f.get("fieldLabel"),
            "type": f.get("fieldType"),
            "populated_deals": populated,
            "pct": (populated / len(data["deals"]) * 100) if data["deals"] else 0,
        })

    return {
        "pipelines": pipeline_rows,
        "stages": stage_rows,
        "deal_field_completeness": field_completeness,
        "total_deals": len(data["deals"]),
    }


def render_markdown(r: dict) -> str:
    if r.get("unavailable"):
        return render_feature_unavailable(
            "Deals (CRM)", "Plus",
            "Pipeline audit needs /deals, /dealStages, /dealGroups.",
        )
    lines = [
        "# Pipeline Audit",
        "",
        f"Total deals: {r['total_deals']}",
        "",
        "## Pipelines",
        "| Pipeline | Deals | Total value (cents) |",
        "|---|---|---|",
    ]
    for p in r["pipelines"]:
        lines.append(f"| {p['name']} | {p['deal_count']} | {p['total_value_cents']} |")
    lines.append("")
    lines.append("## Stages")
    lines.append("| Pipeline | Stage | Deals | New in 90d | Stale? |")
    lines.append("|---|---|---|---|---|")
    for s in r["stages"]:
        lines.append(f"| {s['pipeline']} | {s['stage']} | {s['deal_count']} | {s['recent_90d']} | {'yes' if s['stale'] else 'no'} |")
    lines.append("")
    lines.append("## Deal custom field completeness")
    lines.append("| Field | Type | Populated | % |")
    lines.append("|---|---|---|---|")
    for f in r["deal_field_completeness"]:
        lines.append(f"| {f['field']} | {f['type']} | {f['populated_deals']} | {f['pct']:.1f}% |")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Audit deal pipelines")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    client = ACClient()
    data = fetch(client)
    r = analyze(data)
    out = json.dumps(r, indent=2) if args.format == "json" else render_markdown(r)
    if args.output:
        Path(args.output).write_text(out)
        print(f"Wrote {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()
