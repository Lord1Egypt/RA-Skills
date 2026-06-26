#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def fmt(v):
    return "NA" if v is None else f"{v:.2f}"


def render_stage_table(stage_rows):
    stage_lines = ["| Funnel Stage | Records | Mention | Positive | Capability | Ecosystem |", "|---|---:|---:|---:|---:|---:|"]
    for row in stage_rows:
        stage_lines.append(
            f"| {row['funnel_stage']} | {row['record_count']} | {fmt(row['mention_rate'])} | {fmt(row['positive_mention_rate'])} | {fmt(row['capability_accuracy'])} | {fmt(row['ecosystem_accuracy'])} |"
        )
    if len(stage_lines) == 2:
        stage_lines.append("| no funnel metadata | 0 | NA | NA | NA | NA |")
    return "\n".join(stage_lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", required=True)
    ap.add_argument("--template", default="templates/weekly-report.md")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    summary = json.loads(Path(args.summary).read_text(encoding="utf-8"))
    template = Path(args.template).read_text(encoding="utf-8")

    by_model_lines = ["| Model | Mention | Positive | Capability | Ecosystem |", "|---|---:|---:|---:|---:|"]
    for row in summary.get("by_model", []):
        by_model_lines.append(
            f"| {row['model_id']} | {fmt(row['mention_rate'])} | {fmt(row['positive_mention_rate'])} | {fmt(row['capability_accuracy'])} | {fmt(row['ecosystem_accuracy'])} |"
        )

    repair_lines = ["| Query ID | Model | Repair Type |", "|---|---|---|"]
    for row in summary.get("repair_candidates", []):
        repair_lines.append(f"| {row['query_id']} | {row['model_id']} | {row['repair_type']} |")
    if len(repair_lines) == 2:
        repair_lines.append("| none | none | none |")

    rendered = template.format(
        run_id=summary["run_id"],
        project=summary["project"],
        created_at=summary["created_at"],
        record_count=summary["record_count"],
        mention_rate=fmt(summary["metrics"].get("mention_rate")),
        positive_mention_rate=fmt(summary["metrics"].get("positive_mention_rate")),
        capability_accuracy=fmt(summary["metrics"].get("capability_accuracy")),
        ecosystem_accuracy=fmt(summary["metrics"].get("ecosystem_accuracy")),
        by_model_table="\n".join(by_model_lines),
        by_funnel_stage_table=render_stage_table(summary.get("by_funnel_stage", [])),
        repair_table="\n".join(repair_lines),
    )
    Path(args.output).write_text(rendered, encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
