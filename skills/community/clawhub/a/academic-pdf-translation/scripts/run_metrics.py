from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Any

from _common import (
    SCHEMA_VERSION,
    SkillError,
    internal_job_path,
    load_json,
    utc_now,
    write_json,
)


def _metrics_path(job_dir: Path, job: dict[str, Any]) -> Path:
    return internal_job_path(
        job_dir,
        job.get("files", {}).get("run_metrics", "run-metrics.json"),
    )


def record_run_metric(
    job_dir: Path,
    *,
    stage: str,
    status: str,
    elapsed_seconds: float | None = None,
    model: str | None = None,
    input_tokens: int | None = None,
    output_tokens: int | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    job_dir = job_dir.resolve()
    job = load_json(job_dir / "job.json")
    if not stage.strip() or not status.strip():
        raise SkillError("stage 和 status 不能为空")
    for label, value in (
        ("elapsed_seconds", elapsed_seconds),
        ("input_tokens", input_tokens),
        ("output_tokens", output_tokens),
    ):
        if value is not None and (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or value < 0
        ):
            raise SkillError(f"{label} 必须是非负数")

    path = _metrics_path(job_dir, job)
    ledger = (
        load_json(path)
        if path.is_file()
        else {
            "schema_version": SCHEMA_VERSION,
            "job_id": job.get("job_id"),
            "events": [],
        }
    )
    events = ledger.setdefault("events", [])
    if not isinstance(events, list):
        raise SkillError("run-metrics.json 的 events 必须是数组")
    event = {
        "event_id": len(events) + 1,
        "recorded_at": utc_now(),
        "stage": stage.strip(),
        "status": status.strip(),
        "review_mode": job.get("review", {}).get("mode"),
        "elapsed_seconds": (
            round(float(elapsed_seconds), 3)
            if elapsed_seconds is not None
            else None
        ),
        "model": model.strip() if isinstance(model, str) and model.strip() else None,
        "input_tokens": int(input_tokens) if input_tokens is not None else None,
        "output_tokens": int(output_tokens) if output_tokens is not None else None,
        "metadata": metadata or {},
    }
    events.append(event)
    write_json(path, ledger)
    return event


def summarize_metric_ledgers(paths: list[Path]) -> dict[str, Any]:
    events: list[dict[str, Any]] = []
    jobs: set[str] = set()
    for path in paths:
        try:
            ledger = load_json(path)
        except SkillError:
            continue
        jobs.add(str(ledger.get("job_id") or path.parent))
        events.extend(
            event
            for event in ledger.get("events", [])
            if isinstance(event, dict)
        )

    modes: dict[str, dict[str, Any]] = {}
    for mode in ("none", "independent", "precise", "unknown"):
        mode_events = [
            event
            for event in events
            if str(event.get("review_mode") or "unknown") == mode
        ]
        pipeline = [
            event
            for event in mode_events
            if event.get("stage") == "candidate-pipeline"
            and (
                event.get("metadata", {}).get("attempt_kind") == "first"
                or (
                    "attempt_kind" not in event.get("metadata", {})
                    and event.get("metadata", {}).get("attempt_label")
                    in {"first", "benchmark-first"}
                )
            )
        ]
        elapsed = [
            float(event["elapsed_seconds"])
            for event in pipeline
            if isinstance(event.get("elapsed_seconds"), (int, float))
        ]
        passed = sum(
            event.get("status") == "READY_TO_REGISTER"
            for event in pipeline
        )
        input_tokens = sum(
            int(event.get("input_tokens") or 0)
            for event in mode_events
        )
        output_tokens = sum(
            int(event.get("output_tokens") or 0)
            for event in mode_events
        )
        modes[mode] = {
            "first_candidate_runs": len(pipeline),
            "first_candidate_passes": passed,
            "first_candidate_pass_rate": (
                round(passed / len(pipeline), 4) if pipeline else None
            ),
            "median_pipeline_seconds": (
                round(statistics.median(elapsed), 3) if elapsed else None
            ),
            "recorded_input_tokens": input_tokens,
            "recorded_output_tokens": output_tokens,
        }
    return {
        "schema_version": SCHEMA_VERSION,
        "job_count": len(jobs),
        "event_count": len(events),
        "modes": modes,
        "measurement_note": (
            "通过率只统计 attempt_kind=first 的候选流水线事件；"
            "没有记录的数据保持 null，不作估算。"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="记录或汇总学术 PDF 译制的时间与 token 消耗"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    record = subparsers.add_parser("record")
    record.add_argument("job_dir", type=Path)
    record.add_argument("--stage", required=True)
    record.add_argument("--status", required=True)
    record.add_argument("--elapsed-seconds", type=float)
    record.add_argument("--model")
    record.add_argument("--input-tokens", type=int)
    record.add_argument("--output-tokens", type=int)
    record.add_argument("--metadata-json")

    summarize = subparsers.add_parser("summarize")
    summarize.add_argument("root", type=Path)
    summarize.add_argument("--output", type=Path)

    args = parser.parse_args()
    try:
        if args.command == "record":
            metadata = (
                json.loads(args.metadata_json)
                if args.metadata_json
                else {}
            )
            event = record_run_metric(
                args.job_dir,
                stage=args.stage,
                status=args.status,
                elapsed_seconds=args.elapsed_seconds,
                model=args.model,
                input_tokens=args.input_tokens,
                output_tokens=args.output_tokens,
                metadata=metadata,
            )
            print(json.dumps(event, ensure_ascii=False, indent=2))
            return 0

        paths = [
            path
            for path in args.root.resolve().rglob("run-metrics.json")
            if "history" not in path.parts
        ]
        report = summarize_metric_ledgers(paths)
        if args.output:
            write_json(args.output.resolve(), report)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    except (SkillError, json.JSONDecodeError) as exc:
        print(f"错误: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
