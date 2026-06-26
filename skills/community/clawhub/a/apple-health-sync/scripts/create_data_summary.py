#!/usr/bin/env python3
"""
Aggregate locally stored Apple Health snapshots into daily/weekly/monthly summaries.
"""

import argparse
import json
import sqlite3
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple
from config import load_effective_config, resolve_state_dir, resolve_user_paths


@dataclass
class Sample:
    user_id: str
    date: datetime
    updated_at: datetime
    payload: Any


def parse_iso(value: str) -> datetime:
    normalized = value.replace("Z", "+00:00")
    dt = datetime.fromisoformat(normalized)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def period_bounds(period: str, now: datetime) -> Tuple[datetime, datetime]:
    if period == "daily":
        start = now - timedelta(days=1)
    elif period == "weekly":
        start = now - timedelta(days=7)
    else:
        start = now - timedelta(days=30)
    return start, now


def flatten_numeric(data: Any, prefix: str = "") -> Dict[str, List[float]]:
    output: Dict[str, List[float]] = {}
    if isinstance(data, dict):
        for key, value in data.items():
            child_prefix = f"{prefix}.{key}" if prefix else key
            child = flatten_numeric(value, child_prefix)
            for c_key, c_values in child.items():
                output.setdefault(c_key, []).extend(c_values)
        return output
    if isinstance(data, list):
        for value in data:
            child_prefix = f"{prefix}[]" if prefix else "[]"
            child = flatten_numeric(value, child_prefix)
            for c_key, c_values in child.items():
                output.setdefault(c_key, []).extend(c_values)
        return output
    if isinstance(data, bool):
        return output
    if isinstance(data, (int, float)):
        output.setdefault(prefix or "value", []).append(float(data))
    return output


def load_sqlite_samples(sqlite_path: Path, start: datetime) -> List[Sample]:
    if not sqlite_path.exists():
        return []
    conn = sqlite3.connect(sqlite_path)
    try:
        rows = conn.execute(
            """
            select user_id, date, data, updated_at
            from health_data
            where date >= ?
            order by date asc
            """,
            (start.date().isoformat(),),
        ).fetchall()
    finally:
        conn.close()

    samples: List[Sample] = []
    for user_id, date_value, data_value, updated_at in rows:
        try:
            samples.append(
                Sample(
                    user_id=user_id,
                    date=parse_iso(date_value),
                    updated_at=parse_iso(updated_at),
                    payload=json.loads(data_value),
                )
            )
        except Exception:
            continue
    return samples


def load_json_samples(json_path: Path, start: datetime) -> List[Sample]:
    if not json_path.exists():
        return []
    samples: List[Sample] = []
    for line in json_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
            user_id = row.get("user_id") or row.get("record_id")
            fetched_at = parse_iso(row["fetched_at"])
            payload = row["payload"]
            if not user_id or not isinstance(payload, dict):
                continue
            for date_key, day_payload in payload.items():
                if not isinstance(date_key, str):
                    continue
                day_date = parse_iso(date_key)
                if day_date < start:
                    continue
                samples.append(
                    Sample(
                        user_id=user_id,
                        date=day_date,
                        updated_at=fetched_at,
                        payload=day_payload,
                    )
                )
        except Exception:
            continue
    return samples


def summarize(samples: Iterable[Sample]) -> Dict[str, Any]:
    sample_list = list(samples)
    metrics: Dict[str, List[float]] = {}
    for sample in sample_list:
        flattened = flatten_numeric(sample.payload)
        for metric_name, values in flattened.items():
            metrics.setdefault(metric_name, []).extend(values)

    summary_metrics: Dict[str, Dict[str, float]] = {}
    for metric_name, values in sorted(metrics.items()):
        if not values:
            continue
        summary_metrics[metric_name] = {
            "count": float(len(values)),
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
            "latest": values[-1],
        }

    by_record: Dict[str, int] = {}
    for sample in sample_list:
        by_record[sample.user_id] = by_record.get(sample.user_id, 0) + 1

    return {
        "sample_count": len(sample_list),
        "records": by_record,
        "metrics": summary_metrics,
    }


def format_text(period: str, start: datetime, end: datetime, summary: Dict[str, Any]) -> str:
    lines = [
        f"Apple Health Summary ({period})",
        f"Window: {start.isoformat()} -> {end.isoformat()}",
        f"Samples: {summary['sample_count']}",
    ]

    records = summary["records"]
    if records:
        lines.append("Samples per record:")
        for user_id, count in sorted(records.items()):
            lines.append(f"- {user_id}: {count}")
    else:
        lines.append("Samples per record: none")

    metrics = summary["metrics"]
    if metrics:
        lines.append("Numeric metrics:")
        for metric_name, values in metrics.items():
            lines.append(
                f"- {metric_name}: avg={values['avg']:.2f}, min={values['min']:.2f}, "
                f"max={values['max']:.2f}, latest={values['latest']:.2f}, n={int(values['count'])}"
            )
    else:
        lines.append("Numeric metrics: none")

    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Apple Health aggregate summaries.")
    parser.add_argument(
        "--state-dir",
        default="",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--period",
        choices=("daily", "weekly", "monthly"),
        default="weekly",
    )
    parser.add_argument(
        "--storage",
        choices=("auto", "sqlite", "json"),
        default="auto",
    )
    parser.add_argument("--sqlite-path", default="")
    parser.add_argument("--json-path", default="")
    parser.add_argument(
        "--output",
        choices=("text", "json"),
        default="text",
    )
    parser.add_argument("--save", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    state_dir = resolve_state_dir(args.state_dir)
    paths = resolve_user_paths(state_dir)
    try:
        _, config = load_effective_config(state_dir)
    except Exception as runtime_error:
        print(f"Error: {runtime_error}", file=sys.stderr)
        return 1

    storage = args.storage if args.storage != "auto" else config.get("storage", "sqlite")
    now = datetime.now(timezone.utc).replace(microsecond=0)
    start, end = period_bounds(args.period, now)

    if storage == "sqlite":
        sqlite_path = Path(args.sqlite_path or config.get("sqlite_path", state_dir / "health_data.db"))
        samples = load_sqlite_samples(sqlite_path.expanduser(), start)
    else:
        json_path = Path(args.json_path or config.get("json_path", paths["config_dir"] / "health_data.ndjson"))
        samples = load_json_samples(json_path.expanduser(), start)

    summary = summarize(samples)
    payload = {
        "period": args.period,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "storage": storage,
        "summary": summary,
    }

    if args.output == "json":
        rendered = json.dumps(payload, indent=2) + "\n"
    else:
        rendered = format_text(args.period, start, end, summary)

    if args.save:
        save_path = Path(args.save).expanduser().resolve()
        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_text(rendered, encoding="utf-8")
        print(f"Report written to: {save_path}")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
