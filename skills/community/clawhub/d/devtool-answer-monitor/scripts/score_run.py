#!/usr/bin/env python3
import argparse
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

METRIC_MAP = {
    "mention_rate": ("mention_score", lambda r: True),
    "positive_mention_rate": ("sentiment_score", lambda r: (r.get("mention_score") or 0) > 0),
    "capability_accuracy": ("capability_score", lambda r: r.get("query_type") == "capability"),
    "ecosystem_accuracy": ("ecosystem_score", lambda r: r.get("query_type") == "ecosystem"),
}
FUNNEL_STAGE_ORDER = ["awareness", "selection", "integration", "activation", "agent"]


def load_jsonl(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def compute_metric(rows, score_field, predicate):
    vals = [r[score_field] / 2 for r in rows if predicate(r) and r.get(score_field) is not None]
    if not vals:
        return None
    return round(statistics.mean(vals) * 100, 2)


def strict_rate(rows, score_field, predicate):
    vals = [r[score_field] for r in rows if predicate(r) and r.get(score_field) is not None]
    if not vals:
        return None
    return round(sum(1 for v in vals if v == 2) / len(vals) * 100, 2)


def build_metric_entry(label_key, label_value, rows):
    entry = {
        label_key: label_value,
        "record_count": len(rows),
    }
    for metric, (score_field, predicate) in METRIC_MAP.items():
        entry[metric] = compute_metric(rows, score_field, predicate)
    return entry


def build_summary(rows):
    first = rows[0]
    summary = {
        "run_id": first["run_id"],
        "created_at": first.get("captured_at"),
        "project": first["project"],
        "record_count": len(rows),
        "metrics": {},
        "strict_rates": {},
        "by_model": [],
        "by_funnel_stage": [],
        "repair_candidates": [],
    }
    for metric, (score_field, predicate) in METRIC_MAP.items():
        summary["metrics"][metric] = compute_metric(rows, score_field, predicate)
        summary["strict_rates"][metric] = strict_rate(rows, score_field, predicate)

    by_model = defaultdict(list)
    for row in rows:
        by_model[row["model_id"]].append(row)
    for model_id, model_rows in sorted(by_model.items()):
        summary["by_model"].append(build_metric_entry("model_id", model_id, model_rows))

    by_funnel_stage = defaultdict(list)
    for row in rows:
        stage = row.get("funnel_stage")
        if stage:
            by_funnel_stage[stage].append(row)

    for stage in FUNNEL_STAGE_ORDER:
        stage_rows = by_funnel_stage.get(stage)
        if stage_rows:
            summary["by_funnel_stage"].append(build_metric_entry("funnel_stage", stage, stage_rows))

    for row in rows:
        if row.get("needs_repair"):
            summary["repair_candidates"].append(
                {
                    "query_id": row["query_id"],
                    "model_id": row["model_id"],
                    "repair_type": row.get("repair_type", "none"),
                }
            )
    return summary


def write_metrics_csv(summary, path):
    fields = ["scope", "name", "record_count", "mention_rate", "positive_mention_rate", "capability_accuracy", "ecosystem_accuracy"]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerow({"scope": "overall", "name": summary["project"], "record_count": summary["record_count"], **summary["metrics"]})
        for row in summary["by_model"]:
            writer.writerow({"scope": "model", "name": row["model_id"], **{k: row[k] for k in fields[2:]}})
        for row in summary.get("by_funnel_stage", []):
            writer.writerow({"scope": "funnel_stage", "name": row["funnel_stage"], **{k: row[k] for k in fields[2:]}})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output-dir", required=True)
    args = ap.parse_args()

    rows = load_jsonl(args.input)
    missing = [r for r in rows if any(r.get(k) is None for k in ["mention_score", "sentiment_score", "capability_score", "ecosystem_score"])]
    if missing:
        raise SystemExit(f"Found {len(missing)} rows with missing scores. Complete annotation first.")

    summary = build_summary(rows)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_metrics_csv(summary, out_dir / "metrics.csv")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
