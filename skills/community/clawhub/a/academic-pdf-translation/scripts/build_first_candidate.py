from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from _common import SkillError, write_json
from build_candidate import (
    RENDERER_NAME,
    RENDERER_VERSION,
    build_candidate,
)
from font_preparation import prepare_job_fonts
from pre_render_audit import (
    build_input_readiness_audit,
    build_pre_render_audit,
)
from preflight_candidate import preflight_candidate
from renderer_identity import renderer_build_id
from run_metrics import record_run_metric


def build_first_candidate(
    job_dir: Path,
    output_pdf: Path | None = None,
    *,
    attempt_label: str = "first",
    max_page_expansion_ratio: float | None = None,
) -> dict:
    pipeline_started = time.monotonic()
    job_dir = job_dir.resolve()
    label = attempt_label.strip()
    if not label or any(char in label for char in "/\\"):
        raise SkillError("--attempt-label 必须是非空文件名片段")
    attempt_kind = (
        "repair"
        if label.casefold().startswith("repair")
        else "first"
    )
    if output_pdf is None:
        output_pdf = (
            job_dir
            / "staging"
            / f"candidate-{label}.pdf"
        )
    else:
        output_pdf = output_pdf.resolve()

    input_started = time.monotonic()
    # 先解析字体，再做输入就绪检查。顺序反过来，全新作业永远进不来。
    font_report = prepare_job_fonts(job_dir)
    input_readiness = build_input_readiness_audit(job_dir)
    input_readiness["font_preparation"] = font_report
    input_seconds = time.monotonic() - input_started
    input_readiness_path = (
        job_dir
        / "staging"
        / f"input-readiness-{label}.json"
    )
    write_json(input_readiness_path, input_readiness)
    if input_readiness["status"] != "READY_TO_RENDER":
        total_seconds = time.monotonic() - pipeline_started
        report = {
            "status": "BLOCKED_BEFORE_PREFLIGHT",
            "blocked_stage": "input-readiness",
            "renderer": RENDERER_NAME,
            "renderer_version": RENDERER_VERSION,
            "renderer_build_id": renderer_build_id(),
            "candidate_pdf": None,
            # 保持字段类型稳定：这里没有发生排版，用空对象而不是 None，
            # 否则下游 report.get("build", {}).get(...) 会拿到 None 并崩溃。
            "build": {},
            "input_readiness": str(input_readiness_path),
            "issues": input_readiness.get("issues", []),
            "timing_seconds": {
                "input_readiness": round(input_seconds, 3),
                "build": 0.0,
                "pre_render_audit": 0.0,
                "preflight": 0.0,
                "total": round(total_seconds, 3),
            },
        }
        record_run_metric(
            job_dir,
            stage="candidate-pipeline",
            status=report["status"],
            elapsed_seconds=total_seconds,
            metadata={
                "attempt_label": label,
                "attempt_kind": attempt_kind,
                "blocked_stage": "input-readiness",
                "timing_seconds": report["timing_seconds"],
            },
        )
        return report

    build_started = time.monotonic()
    build = build_candidate(
        job_dir,
        output_pdf,
        max_page_expansion_ratio=max_page_expansion_ratio,
    )
    build_seconds = time.monotonic() - build_started
    build_id = renderer_build_id()
    audit_started = time.monotonic()
    readiness = build_pre_render_audit(job_dir)
    audit_seconds = time.monotonic() - audit_started
    readiness_path = (
        job_dir
        / "staging"
        / f"render-readiness-{label}.json"
    )
    write_json(readiness_path, readiness)
    if readiness["status"] != "READY_TO_RENDER":
        total_seconds = time.monotonic() - pipeline_started
        report = {
            "status": "BLOCKED_BEFORE_PREFLIGHT",
            "blocked_stage": "render-contract",
            "renderer": RENDERER_NAME,
            "renderer_version": RENDERER_VERSION,
            "renderer_build_id": build_id,
            "candidate_pdf": str(output_pdf),
            "build": build,
            "input_readiness": str(input_readiness_path),
            "render_readiness": str(readiness_path),
            "issues": readiness.get("issues", []),
            "timing_seconds": {
                "input_readiness": round(input_seconds, 3),
                "build": round(build_seconds, 3),
                "pre_render_audit": round(audit_seconds, 3),
                "preflight": 0.0,
                "total": round(total_seconds, 3),
            },
        }
        record_run_metric(
            job_dir,
            stage="candidate-pipeline",
            status=report["status"],
            elapsed_seconds=total_seconds,
            metadata={
                "attempt_label": label,
                "attempt_kind": attempt_kind,
                "renderer_build_id": build_id,
                "timing_seconds": report["timing_seconds"],
            },
        )
        return report

    preflight_started = time.monotonic()
    preflight = preflight_candidate(
        job_dir,
        output_pdf,
        RENDERER_NAME,
        RENDERER_VERSION,
        build_id,
    )
    preflight_seconds = time.monotonic() - preflight_started
    preflight_path = (
        job_dir
        / "staging"
        / f"preflight-{label}.json"
    )
    write_json(preflight_path, preflight)
    if preflight["status"] == "NEEDS_REPAIR":
        write_json(
            job_dir
            / "staging"
            / f"repair-plan-{label}.json",
            preflight["repair_plan"],
        )
    total_seconds = time.monotonic() - pipeline_started
    report = {
        "status": preflight["status"],
        "renderer": RENDERER_NAME,
        "renderer_version": RENDERER_VERSION,
        "renderer_build_id": build_id,
        "candidate_pdf": str(output_pdf),
        "build": build,
        "input_readiness": str(input_readiness_path),
        "render_readiness": str(readiness_path),
        "preflight": str(preflight_path),
        "preflight_attempt": preflight.get("preflight_attempt"),
        "hard_failures": preflight.get("hard_failures", []),
        "validation_warnings": preflight.get("validation_warnings", []),
        "completeness_decision": preflight.get("completeness_decision"),
        "timing_seconds": {
            "input_readiness": round(input_seconds, 3),
            "build": round(build_seconds, 3),
            "pre_render_audit": round(audit_seconds, 3),
            "preflight": round(preflight_seconds, 3),
            "total": round(total_seconds, 3),
        },
    }
    record_run_metric(
        job_dir,
        stage="candidate-pipeline",
        status=report["status"],
        elapsed_seconds=total_seconds,
        metadata={
            "attempt_label": label,
            "attempt_kind": attempt_kind,
            "renderer_build_id": build_id,
            "preflight_attempt": report["preflight_attempt"],
            "source_page_count": build.get("source_page_count"),
            "candidate_page_count": build.get("candidate_page_count"),
            "timing_seconds": report["timing_seconds"],
        },
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="一次完成候选生成、总检查和注册前预检"
    )
    parser.add_argument("job_dir", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--attempt-label", default="first")
    parser.add_argument(
        "--max-page-expansion-ratio",
        type=float,
        default=None,
        help="可选的异常页数保护上限；默认按参考文献占比自动计算",
    )
    args = parser.parse_args()
    try:
        if (
            args.max_page_expansion_ratio is not None
            and not 1.0 <= args.max_page_expansion_ratio <= 3.0
        ):
            raise SkillError("--max-page-expansion-ratio 必须位于 1.0..3.0")
        report = build_first_candidate(
            args.job_dir,
            args.output,
            attempt_label=args.attempt_label,
            max_page_expansion_ratio=args.max_page_expansion_ratio,
        )
        print(json.dumps(report, ensure_ascii=False, indent=2))
        if report["status"] == "READY_TO_REGISTER":
            return 0
        if report["status"] in {"NEEDS_REPAIR", "BLOCKED_BEFORE_PREFLIGHT"}:
            return 2
        return 3
    except SkillError as exc:
        print(f"错误: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
