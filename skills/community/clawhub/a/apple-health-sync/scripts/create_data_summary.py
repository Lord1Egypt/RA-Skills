#!/usr/bin/env python3
"""
Aggregate locally stored Apple Health snapshots into daily/weekly/monthly summaries.
"""

import argparse
import json
import os
import sqlite3
import stat
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
from config import (
    load_effective_config,
    resolve_state_dir,
    resolve_user_paths,
    secure_private_file,
    secure_state_directory,
)


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
    secure_private_file(sqlite_path)
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
    secure_private_file(json_path)
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

    record_count = len({sample.user_id for sample in sample_list})

    return {
        "sample_count": len(sample_list),
        "record_count": record_count,
        "metrics": summary_metrics,
    }


def format_text(period: str, start: datetime, end: datetime, summary: Dict[str, Any]) -> str:
    lines = [
        f"Apple Health Summary ({period})",
        f"Window: {start.isoformat()} -> {end.isoformat()}",
        f"Samples: {summary['sample_count']}",
    ]

    lines.append(f"Source records: {summary['record_count']}")

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


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
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
    parser.add_argument(
        "--save",
        default="",
        help="Write the sensitive report to a new file. Requires --confirm-sensitive-save.",
    )
    parser.add_argument(
        "--confirm-sensitive-save",
        action="store_true",
        help="Confirm that the destination is intended for private Apple Health data.",
    )
    return parser.parse_args(argv)


def resolve_save_path(raw_path: str) -> Path:
    return Path(os.path.abspath(os.path.expanduser(raw_path)))


def write_sensitive_report(save_path: Path, rendered: str) -> None:
    parent = save_path.parent
    if not parent.exists() or not parent.is_dir():
        raise RuntimeError(f"Report destination directory does not exist: {parent}")
    if save_path.is_symlink():
        raise RuntimeError(f"Report destination must not be a symbolic link: {save_path}")
    if save_path.exists():
        raise RuntimeError(f"Refusing to overwrite existing report: {save_path}")

    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    file_descriptor = None
    created = False
    try:
        file_descriptor = os.open(save_path, flags, 0o600)
        created = True
        if not stat.S_ISREG(os.fstat(file_descriptor).st_mode):
            raise RuntimeError(f"Report destination is not a regular file: {save_path}")
        os.fchmod(file_descriptor, 0o600)
        with os.fdopen(file_descriptor, "w", encoding="utf-8") as file_handle:
            file_descriptor = None
            file_handle.write(rendered)
            file_handle.flush()
            os.fsync(file_handle.fileno())
    except Exception:
        if file_descriptor is not None:
            os.close(file_descriptor)
        if created:
            save_path.unlink(missing_ok=True)
        raise


def main(argv: Optional[List[str]] = None) -> int:
    os.umask(0o077)
    args = parse_args(argv)
    if args.save and not args.confirm_sensitive_save:
        print(
            "Error: --save writes sensitive Apple Health data and requires --confirm-sensitive-save.",
            file=sys.stderr,
        )
        return 2
    if args.confirm_sensitive_save and not args.save:
        print("Error: --confirm-sensitive-save requires --save <path>.", file=sys.stderr)
        return 2

    state_dir = resolve_state_dir(args.state_dir)
    paths = resolve_user_paths(state_dir)
    for private_dir in (state_dir, paths["config_dir"], paths["secrets_dir"]):
        if private_dir.exists():
            secure_state_directory(private_dir)
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
        save_path = resolve_save_path(args.save)
        print(
            "Warning: this report contains sensitive Apple Health information. "
            "Keep the destination private and exclude it from shared backups.",
            file=sys.stderr,
        )
        try:
            write_sensitive_report(save_path, rendered)
        except Exception as runtime_error:
            print(f"Error: {runtime_error}", file=sys.stderr)
            return 1
        print(f"Report written to: {save_path}")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
