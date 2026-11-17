from __future__ import annotations

import argparse
import json
import re
import shutil
import statistics
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from _common import SkillError, load_json, utc_now, write_json
from build_first_candidate import build_first_candidate


COPY_IGNORES = (
    "history",
    "staging",
    "renders",
    "comparisons",
    "__pycache__",
)


def _case_id(value: Any, index: int) -> str:
    identifier = str(value or f"case-{index:03d}").strip()
    if not re.fullmatch(r"[A-Za-z0-9._-]+", identifier):
        raise SkillError(
            f"基准 case id 只能包含字母、数字、点、下划线和连字符: {identifier}"
        )
    return identifier


def _load_cases(manifest_path: Path) -> list[dict[str, Any]]:
    manifest_path = manifest_path.resolve()
    manifest = load_json(manifest_path)
    raw_cases = manifest.get("cases")
    if not isinstance(raw_cases, list) or not raw_cases:
        raise SkillError("基准清单必须包含非空 cases")
    cases: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw_case in enumerate(raw_cases, start=1):
        if not isinstance(raw_case, dict):
            raise SkillError(f"cases[{index - 1}] 必须是对象")
        identifier = _case_id(raw_case.get("id"), index)
        if identifier in seen:
            raise SkillError(f"基准 case id 重复: {identifier}")
        seen.add(identifier)
        job_value = raw_case.get("job_dir")
        if not isinstance(job_value, str) or not job_value.strip():
            raise SkillError(f"cases[{index - 1}] 缺少 job_dir")
        job_dir = Path(job_value).expanduser()
        if not job_dir.is_absolute():
            job_dir = manifest_path.parent / job_dir
        job_dir = job_dir.resolve()
        if not (job_dir / "job.json").is_file():
            raise SkillError(f"基准作业无效: {job_dir}")
        cases.append(
            {
                "id": identifier,
                "job_dir": job_dir,
                "tags": [
                    str(tag)
                    for tag in raw_case.get("tags", [])
                    if isinstance(tag, str)
                ],
            }
        )
    return cases


def _run_case(case: dict[str, Any], work_root: Path) -> dict[str, Any]:
    destination = work_root / str(case["id"])
    if destination.exists():
        raise SkillError(f"基准工作目录已存在: {destination}")
    shutil.copytree(
        case["job_dir"],
        destination,
        ignore=shutil.ignore_patterns(*COPY_IGNORES),
    )
    try:
        report = build_first_candidate(
            destination,
            attempt_label="benchmark-first",
        )
        return {
            "id": case["id"],
            "tags": case["tags"],
            "status": report.get("status"),
            "renderer_version": report.get("renderer_version"),
            "renderer_build_id": report.get("renderer_build_id"),
            "source_page_count": (report.get("build") or {}).get(
                "source_page_count"
            ),
            "candidate_page_count": (report.get("build") or {}).get(
                "candidate_page_count"
            ),
            "timing_seconds": report.get("timing_seconds", {}),
            "hard_failure_codes": [
                str(failure.get("code") or "UNKNOWN")
                for failure in report.get("hard_failures", [])
                if isinstance(failure, dict)
            ],
        }
    except Exception as exc:
        return {
            "id": case["id"],
            "tags": case["tags"],
            "status": "ERROR",
            "error": str(exc),
            "timing_seconds": {},
            "hard_failure_codes": [],
        }


def run_benchmark(
    manifest_path: Path,
    *,
    work_dir: Path | None = None,
    workers: int = 1,
) -> dict[str, Any]:
    if workers < 1:
        raise SkillError("workers 必须至少为 1")
    cases = _load_cases(manifest_path)
    temporary = None
    if work_dir is None:
        temporary = tempfile.TemporaryDirectory(
            prefix="academic-pdf-benchmark-"
        )
        work_root = Path(temporary.name)
    else:
        work_root = work_dir.resolve()
        work_root.mkdir(parents=True, exist_ok=True)

    results: list[dict[str, Any]] = []
    benchmark_started = time.monotonic()
    try:
        with ThreadPoolExecutor(
            max_workers=min(workers, len(cases))
        ) as executor:
            futures = {
                executor.submit(_run_case, case, work_root): case["id"]
                for case in cases
            }
            for future in as_completed(futures):
                results.append(future.result())
    finally:
        if temporary is not None:
            temporary.cleanup()

    results.sort(key=lambda item: str(item["id"]))
    passed = sum(
        result.get("status") == "READY_TO_REGISTER"
        for result in results
    )
    totals = [
        float(result["timing_seconds"]["total"])
        for result in results
        if isinstance(result.get("timing_seconds"), dict)
        and isinstance(
            result["timing_seconds"].get("total"),
            (int, float),
        )
    ]
    build_ids = sorted(
        {
            str(result["renderer_build_id"])
            for result in results
            if result.get("renderer_build_id")
        }
    )
    return {
        "schema_version": "1.0",
        "generated_at": utc_now(),
        "case_count": len(results),
        "automatic_first_pass_count": passed,
        "automatic_first_pass_rate": round(passed / len(results), 4),
        "median_total_seconds": (
            round(statistics.median(totals), 3) if totals else None
        ),
        "benchmark_wall_seconds": round(
            time.monotonic() - benchmark_started,
            3,
        ),
        "workers": workers,
        "renderer_build_ids": build_ids,
        "single_build": len(build_ids) == 1,
        "visual_review_required": True,
        "work_dir": str(work_root) if work_dir is not None else None,
        "cases": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="在隔离副本中批量测量首版自动通过率与耗时"
    )
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--work-dir", type=Path)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = run_benchmark(
            args.manifest,
            work_dir=args.work_dir,
            workers=args.workers,
        )
        if args.output:
            write_json(args.output.resolve(), report)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return (
            0
            if report["automatic_first_pass_count"]
            == report["case_count"]
            else 2
        )
    except SkillError as exc:
        print(f"错误: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
