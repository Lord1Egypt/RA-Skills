#!/usr/bin/env python3
"""Run agent-agnostic captured-run skill evals for kai-business-blueprint."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class NormalizedTraceMetrics:
    runner: str
    trace_format_version: str
    tool_calls: list[dict[str, Any]]
    shell_commands: list[str]
    failed_shell_commands: list[str]
    read_paths: list[str]
    write_paths: list[str]
    artifact_paths: list[str]
    input_tokens: int | None
    output_tokens: int | None
    wall_ms: int
    run_completed: bool
    skill_evidence: dict[str, bool]
    runner_warnings: list[str]


@dataclass(frozen=True)
class SkillEvalCase:
    case_id: str
    total_score: int
    passed: bool
    eval_complete: bool
    scores: dict[str, int]
    failures: list[str]
    style_rubric: dict[str, Any] | None
    metrics: dict[str, Any]
    artifact_dir: str


def load_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def bool_field(row: dict[str, str], key: str) -> bool:
    return row[key].strip().lower() == "true"


def int_field(row: dict[str, str], key: str, default: int) -> int:
    value = row.get(key, "").strip()
    return int(value) if value else default


def _suffix_match(paths: list[str], suffix: str) -> bool:
    normalized_suffix = suffix.replace("\\", "/").lstrip("./")
    return any(path.replace("\\", "/").lstrip("./").endswith(normalized_suffix) for path in paths)


def _contains_any(values: list[str], needles: list[str]) -> bool:
    haystack = "\n".join(values)
    return any(needle in haystack for needle in needles)


def _infer_skill_evidence(
    read_paths: list[str],
    write_paths: list[str],
    artifact_paths: list[str],
    commands: list[str],
) -> dict[str, bool]:
    all_paths = read_paths + write_paths + artifact_paths
    skill_contract_read = _suffix_match(read_paths, "SKILL.md") or _contains_any(commands, ["SKILL.md"])
    validate_observed = _contains_any(commands, ["--validate", " validate.py"])
    export_observed = _contains_any(commands, ["--export", "--export-auto", " export_svg.py"]) or any(
        path.endswith(".svg") or path.endswith(".html") for path in all_paths
    )
    projection_observed = _contains_any(commands, ["--project", " projection.py"]) or any(
        path.endswith(".projection.json") for path in all_paths
    )
    blueprint_flow_observed = (
        _contains_any(commands, ["scripts/business_blueprint/cli.py", "business_blueprint.cli", "--plan"])
        or any(path.endswith(".blueprint.json") for path in all_paths)
        or export_observed
        or projection_observed
        or validate_observed
    )
    return {
        "skill_contract_read": skill_contract_read,
        "blueprint_flow_observed": blueprint_flow_observed,
        "validate_observed": validate_observed,
        "export_observed": export_observed,
        "projection_observed": projection_observed,
    }


def load_normalized_trace(path: Path) -> NormalizedTraceMetrics:
    payload = json.loads(path.read_text(encoding="utf-8"))
    shell_commands = list(payload.get("shell_commands") or [])
    read_paths = list(payload.get("read_paths") or [])
    write_paths = list(payload.get("write_paths") or [])
    artifact_paths = list(payload.get("artifact_paths") or [])
    skill_evidence = dict(payload.get("skill_evidence") or {})
    if not skill_evidence:
        skill_evidence = _infer_skill_evidence(read_paths, write_paths, artifact_paths, shell_commands)
    return NormalizedTraceMetrics(
        runner=str(payload.get("runner") or "normalized-trace"),
        trace_format_version=str(payload.get("trace_format_version") or "normalized-v1"),
        tool_calls=list(payload.get("tool_calls") or []),
        shell_commands=shell_commands,
        failed_shell_commands=list(payload.get("failed_shell_commands") or []),
        read_paths=read_paths,
        write_paths=write_paths,
        artifact_paths=artifact_paths,
        input_tokens=payload.get("input_tokens"),
        output_tokens=payload.get("output_tokens"),
        wall_ms=int(payload.get("wall_ms") or 0),
        run_completed=bool(payload.get("run_completed", True)),
        skill_evidence=skill_evidence,
        runner_warnings=list(payload.get("runner_warnings") or []),
    )


def _resolve_existing_path(root: Path, path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else root / path


def files_for_case(root: Path, metrics: NormalizedTraceMetrics, artifact_dir: Path, suffixes: tuple[str, ...]) -> list[Path]:
    candidates: list[Path] = []
    if artifact_dir.exists():
        for suffix in suffixes:
            candidates.extend(sorted(artifact_dir.rglob(f"*{suffix}")))
    for path_text in metrics.artifact_paths + metrics.write_paths:
        if not path_text.endswith(suffixes):
            continue
        path = _resolve_existing_path(root, path_text)
        if path.exists() and path not in candidates:
            candidates.append(path)
    return candidates


def blueprint_files_for_case(root: Path, metrics: NormalizedTraceMetrics, artifact_dir: Path) -> list[Path]:
    return files_for_case(root, metrics, artifact_dir, (".blueprint.json",))


def projection_files_for_case(root: Path, metrics: NormalizedTraceMetrics, artifact_dir: Path) -> list[Path]:
    return files_for_case(root, metrics, artifact_dir, (".projection.json",))


def svg_files_for_case(root: Path, metrics: NormalizedTraceMetrics, artifact_dir: Path) -> list[Path]:
    return files_for_case(root, metrics, artifact_dir, (".svg",))


def html_files_for_case(root: Path, metrics: NormalizedTraceMetrics, artifact_dir: Path) -> list[Path]:
    return files_for_case(root, metrics, artifact_dir, (".html",))


def _display_path(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def _blueprint_payload(root: Path, metrics: NormalizedTraceMetrics, artifact_dir: Path) -> dict[str, Any]:
    files = blueprint_files_for_case(root, metrics, artifact_dir)
    if not files:
        return {}
    try:
        return _read_json(files[0])
    except json.JSONDecodeError:
        return {}


def _artifact_mentions(metrics: NormalizedTraceMetrics, suffix: str) -> bool:
    return any(path.endswith(suffix) for path in metrics.artifact_paths + metrics.write_paths)


def _expected_artifacts_satisfied(
    root: Path,
    row: dict[str, str],
    metrics: NormalizedTraceMetrics,
    artifact_dir: Path,
) -> bool:
    expected = row.get("expected_artifact", "")
    if "svg" in expected and not (svg_files_for_case(root, metrics, artifact_dir) or _artifact_mentions(metrics, ".svg")):
        return False
    if "html" in expected and not (html_files_for_case(root, metrics, artifact_dir) or _artifact_mentions(metrics, ".html")):
        return False
    if "projection" in expected and not (
        projection_files_for_case(root, metrics, artifact_dir) or _artifact_mentions(metrics, ".projection.json")
    ):
        return False
    return True


def default_style_rubric_fixture(root: Path, case_id: str) -> Path:
    return root / "scripts" / "tests" / "fixtures" / "skill-evals" / f"{case_id}-style-rubric.json"


def _validate_style_rubric(rubric: dict[str, Any], case_id: str) -> list[str]:
    failures: list[str] = []
    required = ["case_id", "overall_pass", "score", "checks", "summary"]
    for key in required:
        if key not in rubric:
            failures.append(f"style.rubric_missing_{key}")

    if rubric.get("case_id") != case_id:
        failures.append("style.rubric_case_mismatch")
    score = rubric.get("score")
    if not isinstance(score, int) or score < 0 or score > 100:
        failures.append("style.rubric_score_invalid")
    if not isinstance(rubric.get("overall_pass"), bool):
        failures.append("style.rubric_overall_pass_invalid")
    checks = rubric.get("checks")
    if not isinstance(checks, list) or len(checks) < 4:
        failures.append("style.rubric_checks_invalid")
    elif any(
        not isinstance(check, dict)
        or not isinstance(check.get("id"), str)
        or not isinstance(check.get("pass"), bool)
        or not isinstance(check.get("score"), int)
        or not 1 <= check.get("score", 0) <= 5
        or not isinstance(check.get("notes"), str)
        or not check.get("notes", "").strip()
        for check in checks
    ):
        failures.append("style.rubric_check_invalid")
    if not isinstance(rubric.get("summary"), str) or not rubric.get("summary", "").strip():
        failures.append("style.rubric_summary_invalid")
    return failures


def style_rubric_path_for_case(
    root: Path,
    case_id: str,
    artifact_dir: Path,
    allow_fixture_style_rubric: bool,
) -> tuple[Path | None, str | None]:
    artifact_path = artifact_dir / "style-rubric.json"
    if artifact_path.exists():
        return artifact_path, "artifact"
    fixture_path = default_style_rubric_fixture(root, case_id)
    if allow_fixture_style_rubric and fixture_path.exists():
        return fixture_path, "fixture"
    return None, None


def _blueprint_entity_count(payload: dict[str, Any]) -> int:
    entities = payload.get("entities")
    if isinstance(entities, dict):
        return sum(len(value) for value in entities.values() if isinstance(value, list))
    library = payload.get("library")
    if isinstance(library, dict):
        knowledge = library.get("knowledge")
        if isinstance(knowledge, dict):
            return sum(len(value) for value in knowledge.values() if isinstance(value, list))
    return 0


def _blueprint_relation_count(payload: dict[str, Any]) -> int:
    relations = payload.get("relations")
    return len(relations) if isinstance(relations, list) else 0


def _expected_blueprint_type(payload: dict[str, Any], expected: str) -> bool:
    meta = payload.get("meta")
    if not isinstance(meta, dict):
        return False
    actual = str(meta.get("blueprintType") or "architecture")
    return actual == expected


def score_outcome(
    root: Path,
    row: dict[str, str],
    metrics: NormalizedTraceMetrics,
    artifact_dir: Path,
) -> tuple[int, list[str]]:
    should_trigger = bool_field(row, "should_trigger")
    blueprint_files = blueprint_files_for_case(root, metrics, artifact_dir)

    if not should_trigger:
        generated = (
            blueprint_files
            or projection_files_for_case(root, metrics, artifact_dir)
            or svg_files_for_case(root, metrics, artifact_dir)
            or html_files_for_case(root, metrics, artifact_dir)
            or any(path.endswith((".blueprint.json", ".projection.json", ".svg", ".html")) for path in metrics.write_paths)
        )
        if generated:
            return 0, ["outcome.negative_case_generated_blueprint"]
        return 25, []

    if not blueprint_files:
        return 0, ["outcome.missing_blueprint_artifact"]

    failures: list[str] = []
    score = 10
    payload = _blueprint_payload(root, metrics, artifact_dir)
    if payload.get("version") and isinstance(payload.get("meta"), dict):
        score += 5
    else:
        failures.append("outcome.blueprint_json_invalid")
    if metrics.skill_evidence.get("validate_observed"):
        score += 5
    else:
        failures.append("outcome.validate_not_observed")
    if _expected_artifacts_satisfied(root, row, metrics, artifact_dir):
        score += 5
    else:
        failures.append("outcome.expected_exports_missing")
    return score, failures


def score_process(row: dict[str, str], metrics: NormalizedTraceMetrics) -> tuple[int, list[str]]:
    should_trigger = bool_field(row, "should_trigger")
    if not should_trigger:
        used_blueprint_flow = (
            metrics.skill_evidence.get("blueprint_flow_observed")
            or metrics.skill_evidence.get("validate_observed")
            or metrics.skill_evidence.get("export_observed")
            or metrics.skill_evidence.get("projection_observed")
        )
        if used_blueprint_flow:
            return 0, ["process.negative_case_used_blueprint_flow"]
        return 25, []

    failures: list[str] = []
    score = 0
    if metrics.skill_evidence.get("skill_contract_read") or _suffix_match(metrics.read_paths, "SKILL.md"):
        score += 5
    else:
        failures.append("process.skill_contract_not_observed")

    route_refs = [
        "references/blueprint-schema.md",
        "references/entities-schema.md",
        "references/systems-schema.md",
        "references/domain-knowledge-extraction.md",
        "references/route-eligibility.md",
    ]
    if any(_suffix_match(metrics.read_paths, ref) for ref in route_refs):
        score += 5
    else:
        failures.append("process.blueprint_references_not_observed")

    if metrics.skill_evidence.get("blueprint_flow_observed"):
        score += 5
    else:
        failures.append("process.blueprint_flow_not_observed")

    if metrics.skill_evidence.get("validate_observed"):
        score += 5
    else:
        failures.append("process.validate_not_observed")

    needs_projection = "projection" in row.get("expected_artifact", "")
    final_step_observed = metrics.skill_evidence.get("projection_observed") if needs_projection else metrics.skill_evidence.get("export_observed")
    if final_step_observed:
        score += 5
    elif needs_projection:
        failures.append("process.projection_not_observed")
    else:
        failures.append("process.export_not_observed")

    return score, failures


def score_style(
    root: Path,
    row: dict[str, str],
    metrics: NormalizedTraceMetrics,
    artifact_dir: Path,
    allow_fixture_style_rubric: bool,
) -> tuple[int, list[str], dict[str, Any] | None]:
    if not bool_field(row, "should_trigger"):
        return 25, [], None

    payload = _blueprint_payload(root, metrics, artifact_dir)
    if not payload:
        return 0, ["style.missing_blueprint_artifact"], None

    failures: list[str] = []
    score = 0
    meta = payload.get("meta") if isinstance(payload.get("meta"), dict) else {}
    expected_industry = row.get("expected_industry", "").strip()
    if expected_industry and meta.get("industry") == expected_industry:
        score += 5
    elif expected_industry:
        failures.append("style.expected_industry_not_found")

    expected_type = row.get("expected_blueprint_type", "").strip()
    if expected_type and _expected_blueprint_type(payload, expected_type):
        score += 5
    elif expected_type:
        failures.append("style.expected_blueprint_type_not_found")

    serialized = json.dumps(payload, ensure_ascii=False)
    generic_markers = ["Lorem ipsum", "TODO", "Untitled", "Your title here", "示例标题"]
    if _blueprint_entity_count(payload) >= 6 and _blueprint_relation_count(payload) >= 4 and not any(
        marker in serialized for marker in generic_markers
    ):
        score += 5
    else:
        failures.append("style.semantic_density_or_placeholder_failed")

    style_rubric = None
    rubric_path, rubric_source = style_rubric_path_for_case(root, row["id"], artifact_dir, allow_fixture_style_rubric)
    if rubric_path is not None and rubric_source is not None:
        rubric = json.loads(rubric_path.read_text(encoding="utf-8"))
        rubric_failures = _validate_style_rubric(rubric, row["id"])
        if rubric_failures:
            failures.extend(rubric_failures)
            failures.append("eval.style_rubric_invalid")
        else:
            score += round(int(rubric.get("score", 0)) * 10 / 100)
        style_rubric = {
            "source": rubric_source,
            "path": _display_path(root, rubric_path),
            "score": int(rubric.get("score", 0)) if isinstance(rubric.get("score"), int) else None,
            "overall_pass": bool(rubric.get("overall_pass")),
        }
        if not rubric.get("overall_pass"):
            failures.append("style.rubric_needs_work")
    else:
        failures.append("style.rubric_missing")
        failures.append("eval.style_rubric_missing")

    return min(score, 25), failures, style_rubric


def score_efficiency(row: dict[str, str], metrics: NormalizedTraceMetrics) -> tuple[int, list[str]]:
    failures: list[str] = []
    score = 25
    max_shell_commands = int_field(row, "max_shell_commands", 12)
    max_input_tokens = int_field(row, "max_input_tokens", 90000)
    max_output_tokens = int_field(row, "max_output_tokens", 25000)
    max_wall_ms = int_field(row, "max_wall_ms", 240000)

    if len(metrics.shell_commands) > max_shell_commands:
        score -= 5
        failures.append("efficiency.shell_command_count_over_budget")

    failed_counts = Counter(metrics.failed_shell_commands)
    repeated_failed = sum(count - 1 for count in failed_counts.values() if count > 1)
    if metrics.failed_shell_commands:
        score -= 5
        failures.append("efficiency.failed_shell_command")
    if repeated_failed:
        score -= 10
        failures.append("efficiency.repeated_failed_command")

    if metrics.input_tokens is not None and metrics.input_tokens > max_input_tokens:
        score -= 5
        failures.append("efficiency.input_tokens_over_budget")
    if metrics.output_tokens is not None and metrics.output_tokens > max_output_tokens:
        score -= 5
        failures.append("efficiency.output_tokens_over_budget")
    if metrics.wall_ms > max_wall_ms:
        score -= 3
        failures.append("efficiency.wall_time_over_budget")

    return max(score, 0), failures


def default_normalized_fixture(root: Path, case_id: str) -> Path:
    return root / "scripts" / "tests" / "fixtures" / "skill-evals" / f"{case_id}-normalized.json"


def metrics_for_case(
    root: Path,
    row: dict[str, str],
    runner: str,
    normalized_trace: Path | None,
) -> NormalizedTraceMetrics:
    if normalized_trace is not None:
        return load_normalized_trace(normalized_trace)
    if runner == "fixture":
        return load_normalized_trace(default_normalized_fixture(root, row["id"]))
    raise ValueError("--runner trace requires --normalized-trace")


def evaluate_case(
    root: Path,
    row: dict[str, str],
    runner: str,
    artifact_root: Path,
    normalized_trace: Path | None,
    allow_fixture_style_rubric: bool,
) -> SkillEvalCase:
    case_id = row["id"]
    case_artifact_dir = artifact_root / case_id
    case_artifact_dir.mkdir(parents=True, exist_ok=True)
    metrics = metrics_for_case(root, row, runner, normalized_trace)

    normalized_path = case_artifact_dir / "trace.normalized.json"
    normalized_path.write_text(json.dumps(asdict(metrics), ensure_ascii=False, indent=2), encoding="utf-8")

    outcome, outcome_failures = score_outcome(root, row, metrics, case_artifact_dir)
    process, process_failures = score_process(row, metrics)
    style, style_failures, style_rubric = score_style(root, row, metrics, case_artifact_dir, allow_fixture_style_rubric)
    efficiency, efficiency_failures = score_efficiency(row, metrics)
    scores = {
        "outcome": outcome,
        "process": process,
        "style": style,
        "efficiency": efficiency,
    }
    runner_failures = [] if metrics.run_completed else ["runner.run_incomplete"]
    failures = runner_failures + outcome_failures + process_failures + style_failures + efficiency_failures
    total_score = sum(scores.values())
    should_trigger = bool_field(row, "should_trigger")
    outcome_gate = outcome >= 20 if should_trigger else outcome == 25
    eval_complete = metrics.run_completed and not any(failure.startswith("eval.") for failure in failures)
    passed = eval_complete and outcome_gate and total_score >= 75 and not any(
        failure in {
            "outcome.negative_case_generated_blueprint",
            "process.negative_case_used_blueprint_flow",
        }
        for failure in failures
    )

    return SkillEvalCase(
        case_id=case_id,
        total_score=total_score,
        passed=passed,
        eval_complete=eval_complete,
        scores=scores,
        failures=failures,
        style_rubric=style_rubric,
        metrics=asdict(metrics),
        artifact_dir=_display_path(root, case_artifact_dir),
    )


def selected_rows(rows: list[dict[str, str]], case_id: str | None) -> list[dict[str, str]]:
    if case_id is None:
        return rows
    selected = [row for row in rows if row["id"] == case_id]
    if not selected:
        raise SystemExit(f"No eval case found for {case_id!r}")
    return selected


def build_payload(cases: list[SkillEvalCase]) -> dict[str, Any]:
    categories = ["outcome", "process", "style", "efficiency"]
    return {
        "cases": [asdict(case) for case in cases],
        "summary": {
            "total": len(cases),
            "passed": sum(1 for case in cases if case.passed),
            "failed": sum(1 for case in cases if not case.passed),
            "incomplete": sum(1 for case in cases if not case.eval_complete),
            "average_score": round(sum(case.total_score for case in cases) / len(cases), 2) if cases else 0,
            "average_category_scores": {
                category: round(sum(case.scores[category] for case in cases) / len(cases), 2) if cases else 0
                for category in categories
            },
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--manifest", default="evals/blueprint-skill-prompts.csv")
    parser.add_argument("--runner", choices=["fixture", "trace"], default="fixture")
    parser.add_argument("--case-id", help="Run one case id.")
    parser.add_argument("--normalized-trace", help="Use one normalized trace for selected case.")
    parser.add_argument("--artifact-dir", default="evals/artifacts/current/skill-runs")
    parser.add_argument(
        "--disable-fixture-style-rubric",
        action="store_true",
        help="Do not use checked-in style rubric fixtures when scoring fixture runs.",
    )
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--json-out", help="Optional JSON output path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    manifest = (root / args.manifest).resolve()
    artifact_root = (
        (root / args.artifact_dir).resolve() if not Path(args.artifact_dir).is_absolute() else Path(args.artifact_dir)
    )
    normalized_trace = Path(args.normalized_trace).resolve() if args.normalized_trace else None

    rows = selected_rows(load_manifest(manifest), args.case_id)
    if normalized_trace and len(rows) != 1:
        raise SystemExit("--normalized-trace requires --case-id to select exactly one case")

    cases = [
        evaluate_case(
            root,
            row,
            args.runner,
            artifact_root,
            normalized_trace,
            args.runner == "fixture" and not args.disable_fixture_style_rubric,
        )
        for row in rows
    ]
    payload = build_payload(cases)

    if args.json_out:
        target = Path(args.json_out)
        target = target if target.is_absolute() else root / target
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for case in cases:
            status = "PASS" if case.passed else "FAIL"
            print(f"{status} {case.case_id}: {case.total_score}/100 {case.scores}")
            for failure in case.failures:
                print(f"  - {failure}")
        print(f"Summary: {payload['summary']['passed']} passed, {payload['summary']['failed']} failed.")
    return 0 if payload["summary"]["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
