from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path

import perf_trace
from _common import (
    SkillError,
    internal_job_path,
    load_json,
    sha256_file,
    utc_now,
    write_json,
)
from audit_translation_completeness import build_completeness_audit
from candidate_analysis import (
    open_candidate_analysis,
    shared_candidate_analysis,
)
from qa_pdf import run_qa
from register_candidate import register_candidate
from renderer_identity import renderer_build_id as current_renderer_build_id
from validate_job import validate_job

IGNORED_SHADOW_PATHS = (
    "history",
    "renders",
    "comparisons",
    "staging",
    "__pycache__",
)


def _link_or_copy(source: str, destination: str) -> str:
    """预检副本优先使用硬链接，不支持时回退为普通复制。

    这条路径上的所有写入都走“临时文件加 os.replace”或 unlink，两者都只
    改动目录项，不会原地截断共享 inode。因此硬链接不会让预检修改正式作业。
    """

    try:
        os.link(source, destination)
        return destination
    except OSError:
        return shutil.copy2(source, destination)


def _technical_repair_tasks(
    hard_failures: list,
    validation_errors: list[str],
) -> list[dict]:
    tasks: list[dict] = []
    for index, failure in enumerate(hard_failures, 1):
        if isinstance(failure, dict):
            code = str(failure.get("code") or "TECHNICAL_QA_FAILURE")
            pages = failure.get("pages") or failure.get("page") or []
            if isinstance(pages, int):
                pages = [pages]
            evidence = failure
        else:
            code = "TECHNICAL_QA_FAILURE"
            pages = []
            evidence = {"message": str(failure)}
        lowered = code.lower()
        if any(token in lowered for token in ("overlap", "overflow", "clip", "bound")):
            action = (
                "重新流排受影响页面，消除重叠、裁切和越界；"
                "不得靠缩小正文或压低行距解决。"
            )
        elif any(token in lowered for token in ("font", "glyph", "character")):
            action = "修复字体嵌入、缺字或异常字符，并重新验证可复制检索。"
        elif any(token in lowered for token in ("blank", "whitespace", "width", "gap")):
            action = "重新计算版心、段距和分页，恢复正常阅读密度与正文宽度。"
        else:
            action = "依据自动 QA 证据修复候选 PDF，并重新运行注册前预检。"
        tasks.append(
            {
                "task_id": f"repair-technical-{index:04d}",
                "pages": pages,
                "priority": "high",
                "layers": ["layout-or-pdf"],
                "problem_codes": [code],
                "actions": [action],
                "evidence": evidence,
                "completion_check": (
                    "重新生成临时候选并运行 preflight_candidate.py，"
                    "确认该错误码消失。"
                ),
            }
        )
    for index, error in enumerate(validation_errors, 1):
        tasks.append(
            {
                "task_id": f"repair-validation-{index:04d}",
                "pages": [],
                "priority": "high",
                "layers": ["job-data"],
                "problem_codes": ["JOB_VALIDATION_ERROR"],
                "actions": [f"修复作业数据校验错误：{error}"],
                "evidence": {"message": error},
                "completion_check": "重新运行阶段校验，确认该错误消失。",
            }
        )
    return tasks


def _current_input_hashes(job_dir: Path, job: dict) -> dict[str, str]:
    files = job.get("files", {})
    paths = {
        "source_sha256": internal_job_path(
            job_dir,
            job["source"]["job_path"],
        ),
        "source_units_sha256": internal_job_path(
            job_dir,
            files.get("source_units", "source_units.json"),
        ),
        "translation_sha256": internal_job_path(
            job_dir,
            files["translation"],
        ),
        "complex_content_sha256": internal_job_path(
            job_dir,
            files.get("complex_content_payload", "complex_content.json"),
        ),
        "layout_overrides_sha256": internal_job_path(
            job_dir,
            files["layout_overrides"],
        ),
        "generator_layout_log_sha256": job_dir / "generator-layout-log.json",
    }
    result = {}
    for key, path in paths.items():
        if key == "source_units_sha256" and not path.is_file():
            translation_path = paths["translation_sha256"]
            payload = (
                "legacy-manual\n" + sha256_file(translation_path)
            ).encode("utf-8")
            result[key] = hashlib.sha256(payload).hexdigest()
        else:
            result[key] = sha256_file(path)
    return result


def _jsonable(value):
    if isinstance(value, bytes):
        return value.hex()
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {
            str(key): _jsonable(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
            if key not in {"xref", "number"}
        }
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def _timed__candidate_content_fingerprint(path: Path) -> str:
    analysis = open_candidate_analysis(path)
    document = analysis.document
    pages = []
    for page in document:
        text_blocks = []
        for block in page.get_text("dict").get("blocks", []):
            if block.get("type") != 0:
                continue
            text_blocks.append(
                {
                    "bbox": [
                        round(float(value), 3)
                        for value in block.get("bbox", [])
                    ],
                    "lines": [
                        {
                            "bbox": [
                                round(float(value), 3)
                                for value in line.get("bbox", [])
                            ],
                            "spans": [
                                {
                                    "text": str(span.get("text") or ""),
                                    "font": str(span.get("font") or ""),
                                    "size": round(
                                        float(span.get("size") or 0.0),
                                        3,
                                    ),
                                    "bbox": [
                                        round(float(value), 3)
                                        for value in span.get("bbox", [])
                                    ],
                                }
                                for span in line.get("spans", [])
                            ],
                        }
                        for line in block.get("lines", [])
                    ],
                }
            )
        pages.append(
            {
                "width": round(float(page.rect.width), 3),
                "height": round(float(page.rect.height), 3),
                "rotation": int(page.rotation),
                "text_blocks": text_blocks,
                "drawings": _jsonable(page.get_drawings()),
                "images": _jsonable(page.get_image_info(hashes=True)),
            }
        )
    analysis.release()
    payload = json.dumps(
        pages,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _render_readiness(
    job_dir: Path,
    job: dict,
) -> tuple[dict | None, list[str]]:
    files = job.get("files", {})
    path = internal_job_path(
        job_dir,
        files.get("render_readiness", "staging/render-readiness.json"),
    )
    if not path.is_file():
        return None, ["缺少导出前总检查结果，请先运行 pre_render_audit.py"]
    readiness = load_json(path)
    errors: list[str] = []
    if readiness.get("status") != "READY_TO_RENDER":
        errors.append("导出前总检查尚未通过")
    expected = _current_input_hashes(job_dir, job)
    actual = readiness.get("input_hashes")
    if not isinstance(actual, dict):
        errors.append("导出前总检查缺少输入哈希")
    else:
        for key, value in expected.items():
            if actual.get(key) != value:
                errors.append(f"导出前总检查已经过期: {key}")
    return readiness, errors


def _preflight_cycle(
    job_dir: Path,
    job: dict,
    renderer: str,
    renderer_version: str,
    renderer_build_id: str | None,
    candidate_hash: str,
    candidate_fingerprint: str,
) -> tuple[Path, dict, dict, int, bool]:
    files = job.get("files", {})
    ledger_path = internal_job_path(
        job_dir,
        files.get("preflight_ledger", "staging/preflight-ledger.json"),
    )
    if ledger_path.is_file():
        ledger = load_json(ledger_path)
    else:
        ledger = {"schema_version": "1.0", "cycles": []}
    cycles = ledger.setdefault("cycles", [])
    if not isinstance(cycles, list):
        raise SkillError("preflight-ledger.json 的 cycles 必须是数组")

    provenance_path = internal_job_path(
        job_dir,
        files["candidate_provenance"],
    )
    provenance = load_json(provenance_path)
    base_iteration = int(provenance.get("iteration") or 0)
    cycle = next(
        (
            item
            for item in cycles
            if isinstance(item, dict)
            and item.get("base_iteration") == base_iteration
            and item.get("renderer") == renderer
            and (
                item.get("renderer_build_id") == renderer_build_id
                if renderer_build_id
                else (
                    not item.get("renderer_build_id")
                    and item.get("renderer_version") == renderer_version
                )
            )
        ),
        None,
    )
    if cycle is None:
        cycle = {
            "base_iteration": base_iteration,
            "renderer": renderer,
            "renderer_version": renderer_version,
            "renderer_build_id": renderer_build_id,
            "runs": [],
        }
        cycles.append(cycle)
    elif renderer_version not in cycle.setdefault("renderer_versions", []):
        cycle["renderer_versions"].append(renderer_version)
    cycle.setdefault("renderer_versions", [renderer_version])
    runs = cycle.setdefault("runs", [])
    if not isinstance(runs, list):
        raise SkillError("preflight-ledger.json 的 runs 必须是数组")
    existing = next(
        (
            item
            for item in runs
            if isinstance(item, dict)
            and (
                item.get("candidate_fingerprint") == candidate_fingerprint
                or (
                    not item.get("candidate_fingerprint")
                    and item.get("candidate_sha256") == candidate_hash
                )
            )
        ),
        None,
    )
    if existing is not None:
        return ledger_path, ledger, cycle, int(existing["attempt"]), True
    return ledger_path, ledger, cycle, len(runs) + 1, False


def _timed_preflight_candidate(
    job_dir: Path,
    generated_pdf: Path,
    renderer: str,
    renderer_version: str | None = None,
    renderer_build_id: str | None = None,
) -> dict:
    """预检期间全程持有待检 PDF 的分析，指纹与注册共用同一次打开。"""

    if not Path(generated_pdf).resolve().is_file():
        raise SkillError(f"待预检 PDF 不存在: {generated_pdf}")
    with shared_candidate_analysis(Path(generated_pdf).resolve()):
        return _preflight_candidate(
            job_dir,
            generated_pdf,
            renderer,
            renderer_version,
            renderer_build_id,
        )


def _preflight_candidate(
    job_dir: Path,
    generated_pdf: Path,
    renderer: str,
    renderer_version: str | None = None,
    renderer_build_id: str | None = None,
) -> dict:
    job_dir = job_dir.resolve()
    generated_pdf = generated_pdf.resolve()
    if not (job_dir / "job.json").is_file():
        raise SkillError(f"作业目录无效: {job_dir}")
    if not generated_pdf.is_file():
        raise SkillError(f"待预检 PDF 不存在: {generated_pdf}")
    if not isinstance(renderer_version, str) or not renderer_version.strip():
        raise SkillError(
            "预检必须提供显示版本；统一生成器的次数按代码构建哈希计算"
        )
    if renderer.strip() == "academic-pdf-layout":
        expected_build_id = current_renderer_build_id()
        if (
            isinstance(renderer_build_id, str)
            and renderer_build_id.strip()
            and renderer_build_id.strip() != expected_build_id
        ):
            raise SkillError("renderer_build_id 与当前统一生成器代码不一致")
        renderer_build_id = expected_build_id
    elif isinstance(renderer_build_id, str):
        renderer_build_id = renderer_build_id.strip() or None
    job = load_json(job_dir / "job.json")
    readiness, readiness_errors = _render_readiness(job_dir, job)
    candidate_hash = sha256_file(generated_pdf)
    candidate_fingerprint = _candidate_content_fingerprint(generated_pdf)
    ledger_path, ledger, cycle, attempt, repeated_candidate = _preflight_cycle(
        job_dir,
        job,
        renderer,
        renderer_version,
        renderer_build_id,
        candidate_hash,
        candidate_fingerprint,
    )
    if readiness_errors:
        return {
            "valid": False,
            "status": "PRE_RENDER_AUDIT_REQUIRED",
            "next_action": "run-pre-render-audit-before-export",
            "candidate_sha256": candidate_hash,
            "automatic_decision": None,
            "hard_failures": [
                {
                    "code": "PRE_RENDER_AUDIT_REQUIRED",
                    "messages": readiness_errors,
                }
            ],
            "review_flags": [],
            "validation_errors": readiness_errors,
            "validation_warnings": [],
            "completeness_decision": None,
            "completeness_repair_pages": [],
            "completeness_review_pages": [],
            "completeness_flag_counts": {},
            "repair_plan": {
                "schema_version": "1.0",
                "action": "fix-inputs-before-render",
                "task_count": 1,
                "tasks": [
                    {
                        "task_id": "pre-render-audit",
                        "pages": [],
                        "priority": "high",
                        "layers": ["job-data", "renderer-inputs"],
                        "problem_codes": ["PRE_RENDER_AUDIT_REQUIRED"],
                        "actions": readiness_errors,
                        "completion_check": (
                            "运行 pre_render_audit.py，确认状态为 READY_TO_RENDER。"
                        ),
                    }
                ],
                "completion_condition": "导出前总检查通过后才允许生成候选。",
            },
            "preflight_attempt": attempt,
            "preflight_attempt_limit": 2,
            "formal_job_unchanged": True,
            "staging_ledger_updated": False,
        }
    if attempt > 2:
        return {
            "valid": False,
            "status": "GENERATOR_FIX_REQUIRED",
            "next_action": "fix-renderer-code",
            "candidate_sha256": candidate_hash,
            "automatic_decision": None,
            "hard_failures": [
                {
                    "code": "PREFLIGHT_ATTEMPT_LIMIT_REACHED",
                    "message": (
                        "同一排版器代码构建已经完成首检和一次集中返修。"
                        "继续生成前必须修复排版器，使代码构建哈希发生变化。"
                    ),
                }
            ],
            "review_flags": [],
            "validation_errors": [],
            "validation_warnings": [],
            "completeness_decision": None,
            "completeness_repair_pages": [],
            "completeness_review_pages": [],
            "completeness_flag_counts": {},
            "repair_plan": {
                "schema_version": "1.0",
                "action": "fix-renderer",
                "task_count": 1,
                "tasks": [],
                "completion_condition": (
                    "修复生成器共性问题并产生新的代码构建哈希；"
                    "不得继续对单篇 PDF 逐项打补丁。"
                ),
            },
            "preflight_attempt": 2,
            "preflight_attempt_limit": 2,
            "rejected_candidate_number": attempt,
            "formal_job_unchanged": True,
            "staging_ledger_updated": False,
        }

    with tempfile.TemporaryDirectory(prefix="academic-pdf-preflight-") as tmp:
        shadow = Path(tmp) / "job"
        shutil.copytree(
            job_dir,
            shadow,
            ignore=shutil.ignore_patterns(*IGNORED_SHADOW_PATHS),
            copy_function=_link_or_copy,
        )
        for relative in (
            "reviews",
            "renders/source",
            "renders/candidate",
            "comparisons",
        ):
            (shadow / relative).mkdir(parents=True, exist_ok=True)

        provenance = register_candidate(
            shadow,
            generated_pdf,
            renderer,
            renderer_version,
            "注册前临时预检，不写入正式作业历史",
            renderer_build_id=renderer_build_id,
            allow_additional_iteration=True,
        )
        # QA、作业校验和完整性审查读的是同一份影子候选。这里先把它打开一次，
        # 三步各自的 open 都会命中同一个分析对象，不再重复完整解析。
        shadow_candidate = internal_job_path(
            shadow,
            load_json(shadow / "job.json")["files"]["candidate"],
        )
        with shared_candidate_analysis(shadow_candidate):
            qa = run_qa(shadow)
            validation = validate_job(
                shadow,
                "candidate",
                advance=True,
                # QA 刚在本进程对同一份候选跑完，直接复用；
                # 哈希绑定检查照旧执行。
                qa_report=qa,
            )
            completeness = build_completeness_audit(shadow)
        completeness_needs_repair = (
            completeness["decision"] == "NEEDS_REPAIR"
        )
        hard_failures = list(qa.get("hard_failures", []))
        if completeness_needs_repair:
            hard_failures.append(
                {
                    "code": "TRANSLATION_COMPLETENESS_NEEDS_REPAIR",
                    "pages": completeness["repair_pages"],
                    "flag_counts": completeness["flag_counts"],
                }
            )
        validation_errors = list(validation.get("errors", []))
        repair_tasks = list(completeness["repair_plan"]["tasks"])
        repair_tasks.extend(
            _technical_repair_tasks(
                [
                    failure
                    for failure in hard_failures
                    if not (
                        isinstance(failure, dict)
                        and failure.get("code")
                        == "TRANSLATION_COMPLETENESS_NEEDS_REPAIR"
                    )
                ],
                validation_errors,
            )
        )
        repair_plan = {
            "schema_version": "1.0",
            "action": "repair-and-retry",
            "task_count": len(repair_tasks),
            "tasks": repair_tasks,
            "completion_condition": (
                "一次性完成全部任务并重新生成一次。第二次预检仍失败时，"
                "转为修复排版器，不再继续返修这篇 PDF。"
            ),
        }
        can_register = (
            bool(validation["valid"])
            and not hard_failures
            and not completeness_needs_repair
        )
        status = "READY_TO_REGISTER" if can_register else (
            "GENERATOR_FIX_REQUIRED" if attempt >= 2 else "NEEDS_REPAIR"
        )
        render_readiness_path = internal_job_path(
            job_dir,
            job.get("files", {}).get(
                "render_readiness",
                "staging/render-readiness.json",
            ),
        )
        figure_inventory_path = internal_job_path(
            job_dir,
            job["files"]["figure_inventory"],
        )
        render_readiness_sha256 = sha256_file(render_readiness_path)
        figure_inventory_sha256 = sha256_file(figure_inventory_path)
        run_record = {
            "attempt": attempt,
            "candidate_sha256": candidate_hash,
            "candidate_fingerprint": candidate_fingerprint,
            "renderer_build_id": renderer_build_id,
            "status": status,
            "hard_failure_codes": [
                str(failure.get("code") or "UNKNOWN")
                for failure in hard_failures
                if isinstance(failure, dict)
            ],
            "render_readiness_sha256": render_readiness_sha256,
            "figure_inventory_sha256": figure_inventory_sha256,
            "recorded_at": utc_now(),
        }
        if repeated_candidate:
            existing_run = next(
                (
                    item
                    for item in cycle["runs"]
                    if isinstance(item, dict)
                    and (
                        item.get("candidate_fingerprint")
                        == candidate_fingerprint
                        or (
                            not item.get("candidate_fingerprint")
                            and item.get("candidate_sha256") == candidate_hash
                        )
                    )
                ),
                None,
            )
            if existing_run is None:
                raise SkillError("重复候选缺少对应的预检记录")
            original_recorded_at = existing_run.get("recorded_at")
            existing_run.update(run_record)
            existing_run["first_recorded_at"] = (
                existing_run.get("first_recorded_at")
                or original_recorded_at
                or run_record["recorded_at"]
            )
            existing_run["rechecked_at"] = run_record["recorded_at"]
        else:
            cycle["runs"].append(run_record)
        write_json(ledger_path, ledger)
        return {
            "valid": can_register,
            "status": status,
            "next_action": (
                "register-candidate"
                if can_register
                else (
                    "fix-renderer-code"
                    if status == "GENERATOR_FIX_REQUIRED"
                    else "complete-one-concentrated-repair"
                )
            ),
            "candidate_sha256": provenance["candidate_sha256"],
            "candidate_fingerprint": candidate_fingerprint,
            "renderer_build_id": renderer_build_id,
            "automatic_decision": qa.get("automatic_decision"),
            "hard_failures": hard_failures,
            "review_flags": qa.get("review_flags", []),
            "validation_errors": validation_errors,
            "validation_warnings": validation.get("warnings", []),
            "completeness_decision": completeness["decision"],
            "completeness_repair_pages": completeness["repair_pages"],
            "completeness_review_pages": completeness["review_pages"],
            "completeness_flag_counts": completeness["flag_counts"],
            "repair_plan": repair_plan,
            "render_readiness_sha256": render_readiness_sha256,
            "preflight_attempt": attempt,
            "preflight_attempt_limit": 2,
            "repeated_candidate": repeated_candidate,
            "formal_job_unchanged": True,
            "staging_ledger_updated": True,
        }



def _candidate_content_fingerprint(*args, **kwargs):
    """计时包装：阶段耗时进入性能基线，行为与实现完全一致。"""

    with perf_trace.stage("candidate_fingerprint"):
        return _timed__candidate_content_fingerprint(*args, **kwargs)


def preflight_candidate(*args, **kwargs):
    """计时包装：阶段耗时进入性能基线，行为与实现完全一致。"""

    with perf_trace.stage("preflight"):
        return _timed_preflight_candidate(*args, **kwargs)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="在临时作业副本中预检候选，不增加正式候选版本"
    )
    parser.add_argument("job_dir", type=Path)
    parser.add_argument("generated_pdf", type=Path)
    parser.add_argument("--renderer", required=True)
    parser.add_argument("--renderer-version")
    parser.add_argument("--renderer-build-id")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--repair-plan", type=Path)
    args = parser.parse_args()
    try:
        report = preflight_candidate(
            args.job_dir,
            args.generated_pdf,
            args.renderer,
            args.renderer_version,
            args.renderer_build_id,
        )
        if args.output:
            write_json(args.output.resolve(), report)
        if report["status"] == "NEEDS_REPAIR" and args.repair_plan:
            write_json(args.repair_plan.resolve(), report["repair_plan"])
        print(json.dumps(report, ensure_ascii=False, indent=2))
        if report["status"] == "READY_TO_REGISTER":
            return 0
        if report["status"] == "NEEDS_REPAIR":
            return 2
        return 3
    except SkillError as exc:
        print(f"错误: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
