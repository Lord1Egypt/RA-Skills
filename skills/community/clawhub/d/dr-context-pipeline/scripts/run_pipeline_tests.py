#!/usr/bin/env python3
"""Run deterministic behavioral fixtures for dr-context-pipeline.

The harness intentionally avoids live model calls. Fixtures provide the
retrieval bundle, context pack, and lint result so the runner can verify the
pipeline contract: routing, stable snippet IDs, caps, artifacts, and per-mode
transcript exposure. Optional anti-fabrication fixtures deliberately tamper
with the simulated run so the harness can prove it catches unsupported claims.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import tempfile
from pathlib import Path


SNIPPET_ID_RE = re.compile(r"^S[0-9]+$")
ARTIFACT_STEPS = {
    "retrieval_bundle.json": "build_retrieval_bundle",
    "context_pack.json": "compress_context",
    "lint_result.json": "lint_context_pack",
    "reasoning_input_summary.json": "prepare_reasoning_input",
}
REQUIRED_RECEIPT_STEPS = [
    "load_always_on",
    "route_message",
    "retrieve_snippets",
    "build_retrieval_bundle",
    "compress_context",
    "lint_context_pack",
    "prepare_reasoning_input",
    "emit_audit_artifacts",
]


def normalize_text(value: str) -> str:
    normalized = value.lower().replace("'", "")
    normalized = re.sub(r"[^a-z0-9]+", " ", normalized)
    return re.sub(r"\s+", " ", normalized).strip()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def load_router_config(path: Path) -> dict[str, object]:
    """Parse the router config without requiring PyYAML."""
    rules: list[dict[str, object]] = []
    derived_rules: list[dict[str, object]] = []
    daily_log_match_any: list[str] = []
    current: dict[str, object] | None = None
    current_derived: dict[str, object] | None = None
    section: str | None = None
    current_list: str | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line == "router:":
            section = "router"
            current = None
            current_list = None
            continue
        if line == "derived_queries:":
            if current:
                rules.append(current)
                current = None
            section = "derived_queries"
            current_list = None
            continue
        if line == "retrieval_policy:":
            if current:
                rules.append(current)
                current = None
            if current_derived:
                derived_rules.append(current_derived)
                current_derived = None
            section = "retrieval_policy"
            current_list = None
            continue
        if line == "daily_log_trigger:":
            if current:
                rules.append(current)
                current = None
            if current_derived:
                derived_rules.append(current_derived)
                current_derived = None
            section = "daily_log_trigger"
            current_list = None
            continue

        if section == "router":
            if line.startswith("- task_type:"):
                if current:
                    rules.append(current)
                task_type = line.split(":", 1)[1].strip()
                current = {"task_type": task_type, "match_any": []}
                current_list = None
                continue
            if line == "match_any:":
                current_list = "match_any"
                continue
            if current_list == "match_any" and current is not None and line.startswith("- "):
                current["match_any"].append(parse_yaml_scalar(line[2:].strip()))
            continue

        if section == "derived_queries":
            if line == "when_contains:":
                continue
            if indent == 4 and line.endswith(":"):
                if current_derived:
                    derived_rules.append(current_derived)
                current_derived = {"name": line[:-1], "match_any": [], "add": []}
                current_list = None
                continue
            if any(line.startswith(prefix) for prefix in ("match_any:", "add:", "task_types:")) and "[" in line:
                key, raw_value = line.split(":", 1)
                current_list = key
                if current_derived is not None:
                    current_derived.setdefault(current_list, [])
                    current_derived[current_list].extend(parse_yaml_inline_list(raw_value))
                continue
            if line in {"match_any:", "add:", "task_types:"}:
                current_list = line[:-1]
                continue
            if indent >= 8 and line.startswith("- ") and current_derived is not None and current_list in {"match_any", "add", "task_types"}:
                current_derived.setdefault(current_list, [])
                current_derived[current_list].append(parse_yaml_scalar(line[2:].strip()))
            continue

        if section == "daily_log_trigger":
            if line.startswith("match_any:") and "[" in line:
                current_list = "match_any"
                daily_log_match_any.extend(parse_yaml_inline_list(line.split(":", 1)[1]))
                continue
            if line == "match_any:":
                current_list = "match_any"
                continue
            if current_list == "match_any" and line.startswith("- "):
                daily_log_match_any.append(parse_yaml_scalar(line[2:].strip()))

    if current_derived:
        derived_rules.append(current_derived)

    if current:
        rules.append(current)
    if not rules:
        raise ValueError(f"No router rules parsed from {path}")
    return {
        "router_rules": rules,
        "derived_query_rules": derived_rules,
        "daily_log_match_any": daily_log_match_any,
    }


def parse_yaml_scalar(value: str) -> str:
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    return value


def parse_yaml_inline_list(value: str) -> list[str]:
    stripped = value.strip()
    if not (stripped.startswith("[") and stripped.endswith("]")):
        return []
    inner = stripped[1:-1].strip()
    if not inner:
        return []
    return [parse_yaml_scalar(part.strip()) for part in inner.split(",")]


def route_message(message: str, rules: list[dict[str, object]]) -> str:
    text = f" {normalize_text(message)} "
    fallback = "other"
    for rule in rules:
        task_type = str(rule["task_type"])
        matches = [normalize_text(str(item)) for item in rule.get("match_any", [])]
        if not matches:
            fallback = task_type
            continue
        if any(match and f" {match} " in text for match in matches):
            return task_type
    return fallback


def derive_queries(message: str, task_type: str, rules: list[dict[str, object]]) -> list[str]:
    text = f" {normalize_text(message)} "
    queries: list[str] = []
    for rule in rules:
        allowed_task_types = {str(item) for item in rule.get("task_types", [])}
        if allowed_task_types and task_type not in allowed_task_types:
            continue
        matches = [normalize_text(str(item)) for item in rule.get("match_any", [])]
        if any(match and f" {match} " in text for match in matches):
            for query in rule.get("add", []):
                if query not in queries:
                    queries.append(str(query))
    return queries


def should_enable_daily_logs(message: str, match_any: list[str]) -> bool:
    text = f" {normalize_text(message)} "
    normalized_patterns = [normalize_text(pattern) for pattern in match_any]
    return any(pattern and f" {pattern} " in text for pattern in normalized_patterns)


def fail(errors: list[str], case_id: str, message: str) -> None:
    errors.append(f"{case_id}: {message}")


def assert_common_objects(case: dict, router_config: dict[str, object], errors: list[str]) -> None:
    case_id = case.get("id", "<unknown>")
    bundle = case.get("retrieval_bundle")
    pack = case.get("context_pack")
    lint_result = case.get("lint_result")
    expected_task_type = case.get("expected_task_type")
    expected_snippet_ids = case.get("expected_snippet_ids", [])

    if not isinstance(bundle, dict):
        fail(errors, case_id, "retrieval_bundle must be an object")
        return
    if not isinstance(pack, dict):
        fail(errors, case_id, "context_pack must be an object")
        return
    if not isinstance(lint_result, dict):
        fail(errors, case_id, "lint_result must be an object")
        return

    if bundle.get("retrieval_version") != "1.0":
        fail(errors, case_id, "retrieval_bundle.retrieval_version must be 1.0")
    if bundle.get("query_plan", {}).get("task_type") != expected_task_type:
        fail(errors, case_id, "retrieval_bundle query_plan.task_type mismatch")
    expected_derived_queries = derive_queries(
        case["user_message"],
        str(expected_task_type),
        router_config["derived_query_rules"],
    )
    if bundle.get("query_plan", {}).get("derived_queries", []) != expected_derived_queries:
        fail(
            errors,
            case_id,
            "retrieval_bundle query_plan.derived_queries mismatch",
        )
    if pack.get("version") != "1.0":
        fail(errors, case_id, "context_pack.version must be 1.0")
    if pack.get("task_type") != expected_task_type:
        fail(errors, case_id, "context_pack.task_type mismatch")

    if "expected_daily_log_trigger" in case:
        actual_daily_log_trigger = should_enable_daily_logs(case["user_message"], router_config["daily_log_match_any"])
        if actual_daily_log_trigger != case["expected_daily_log_trigger"]:
            fail(
                errors,
                case_id,
                f"daily_log_trigger mismatch: expected {case['expected_daily_log_trigger']}, found {actual_daily_log_trigger}",
            )

    snippets = bundle.get("snippets", [])
    actual_ids = [snippet.get("snippet_id") for snippet in snippets if isinstance(snippet, dict)]
    if actual_ids != expected_snippet_ids:
        fail(errors, case_id, f"snippet IDs mismatch: expected {expected_snippet_ids}, found {actual_ids}")
    if len(actual_ids) != len(set(actual_ids)):
        fail(errors, case_id, "snippet IDs must be unique")
    for snippet_id in actual_ids:
        if not isinstance(snippet_id, str) or not SNIPPET_ID_RE.match(snippet_id):
            fail(errors, case_id, f"invalid snippet ID: {snippet_id}")

    caps = bundle.get("query_plan", {}).get("caps", {})
    top_k = caps.get("top_k_snippets")
    if isinstance(top_k, int) and len(snippets) > top_k:
        fail(errors, case_id, f"retrieval bundle exceeds top_k_snippets cap {top_k}")

    included_sources = set(pack.get("retrieval_notes", {}).get("included_sources", []))
    if included_sources != set(expected_snippet_ids):
        fail(errors, case_id, "context_pack retrieval_notes included_sources mismatch")
    dropped_due_to_limits = pack.get("retrieval_notes", {}).get("dropped_due_to_limits", [])
    if not isinstance(dropped_due_to_limits, list):
        fail(errors, case_id, "context_pack retrieval_notes dropped_due_to_limits must be a list")

    for section in ["must_follow", "relevant_context", "conflicts_or_ambiguities", "exclude_as_irrelevant"]:
        for idx, item in enumerate(pack.get(section, [])):
            sources = item.get("sources", []) if isinstance(item, dict) else []
            for source in sources:
                if source not in expected_snippet_ids:
                    fail(errors, case_id, f"{section}[{idx}] references unknown source {source}")

    if not isinstance(bundle.get("dropped", []), list):
        fail(errors, case_id, "retrieval_bundle dropped must be a list")


def assert_compression_behavior(case: dict, errors: list[str]) -> None:
    case_id = case["id"]
    bundle = case["retrieval_bundle"]
    pack = case["context_pack"]
    lint_result = case["lint_result"]
    compression_expect = case.get("expect", {}).get("compression", {})
    if not isinstance(compression_expect, dict):
        fail(errors, case_id, "expect.compression must be an object when present")
        return

    expected_status = compression_expect.get("expected_status")
    actual_status = "fallback" if lint_result.get("fallback_used") else "succeeded"
    if expected_status and actual_status != expected_status:
        fail(errors, case_id, f"compression status mismatch: expected {expected_status}, found {actual_status}")

    expected_lint_status = compression_expect.get("expected_lint_status")
    if expected_lint_status and lint_result.get("status") != expected_lint_status:
        fail(errors, case_id, f"lint status mismatch: expected {expected_lint_status}, found {lint_result.get('status')}")

    expected_lint_errors = compression_expect.get("lint_errors_contains", [])
    for expected_error in expected_lint_errors:
        if expected_error not in lint_result.get("errors", []):
            fail(errors, case_id, f"missing lint error: {expected_error}")

    expected_dropped_paths = compression_expect.get("expected_dropped_paths", [])
    actual_dropped_paths = [item.get("path") for item in bundle.get("dropped", []) if isinstance(item, dict)]
    if expected_dropped_paths and actual_dropped_paths != expected_dropped_paths:
        fail(errors, case_id, f"dropped paths mismatch: expected {expected_dropped_paths}, found {actual_dropped_paths}")

    expected_dropped_sources = compression_expect.get("expected_dropped_due_to_limits", [])
    actual_dropped_sources = pack.get("retrieval_notes", {}).get("dropped_due_to_limits", [])
    if expected_dropped_sources and actual_dropped_sources != expected_dropped_sources:
        fail(
            errors,
            case_id,
            f"dropped_due_to_limits mismatch: expected {expected_dropped_sources}, found {actual_dropped_sources}",
        )

    if compression_expect.get("require_unknowns_to_confirm") and not pack.get("unknowns_to_confirm"):
        fail(errors, case_id, "expected unknowns_to_confirm to be non-empty")


def make_reasoning_input_summary(case: dict) -> dict:
    bundle = case["retrieval_bundle"]
    pack = case["context_pack"]
    lint_result = case["lint_result"]
    return {
        "mode": case["mode"],
        "task_type": case["expected_task_type"],
        "user_message_sha256": hashlib.sha256(case["user_message"].encode("utf-8")).hexdigest(),
        "snippet_ids": [snippet["snippet_id"] for snippet in bundle["snippets"]],
        "context_pack_sources": pack["retrieval_notes"]["included_sources"],
        "compression_status": "fallback" if lint_result.get("fallback_used") else "succeeded",
    }


def override_object(target: dict, overrides: dict) -> None:
    for key, value in overrides.items():
        target[key] = value


def write_artifacts(case: dict, run_dir: Path) -> dict[str, str]:
    artifacts = {
        "retrieval_bundle.json": case["retrieval_bundle"],
        "context_pack.json": case["context_pack"],
        "lint_result.json": case["lint_result"],
        "reasoning_input_summary.json": make_reasoning_input_summary(case),
    }
    written: dict[str, str] = {}
    for name, data in artifacts.items():
        path = run_dir / name
        write_json(path, data)
        written[name] = str(path)
    return written


def build_receipt_ledger(case: dict, artifact_paths: dict[str, str]) -> dict:
    run_id = f"{case['id']}-{case['mode']}"
    entries = []
    timestamp = "2026-06-23T00:00:00Z"

    summaries = {
        "load_always_on": "Loaded always_on fixture from retrieval bundle.",
        "route_message": f"Routed message to {case['expected_task_type']}.",
        "retrieve_snippets": f"Retrieved snippets {', '.join(case['expected_snippet_ids'])}.",
        "emit_audit_artifacts": "Prepared audit artifact set and receipt ledger.",
    }

    for step in REQUIRED_RECEIPT_STEPS:
        entry = {
            "step": step,
            "status": "succeeded",
            "started_at_utc": timestamp,
            "finished_at_utc": timestamp,
        }
        artifact_name = next((name for name, artifact_step in ARTIFACT_STEPS.items() if artifact_step == step), None)
        if artifact_name:
            path = Path(artifact_paths[artifact_name])
            entry["proof"] = {
                "artifact_path": str(path),
                "artifact_sha256": sha256(path),
                "summary": f"Wrote {artifact_name}.",
            }
        else:
            entry["proof"] = {"summary": summaries.get(step, f"Completed {step}.")}
        entries.append(entry)

    return {
        "version": "1.0",
        "mode": "audit",
        "run_id": run_id,
        "entries": entries,
    }


def make_transcript(case: dict, artifact_paths: dict[str, str], receipt_ledger: dict | None) -> dict:
    lint_result = case["lint_result"]
    transcript = {
        "mode": case["mode"],
        "task_type": case["expected_task_type"],
        "snippet_ids": case["expected_snippet_ids"],
        "compression_status": "fallback" if lint_result.get("fallback_used") else "succeeded",
        "answer_stub": "Fixture answer omitted; harness validates pipeline behavior, not reasoning quality.",
    }
    if case["mode"] in {"debug", "audit"}:
        transcript.update(
            {
                "artifact_paths": artifact_paths,
                "retrieval_bundle": case["retrieval_bundle"],
                "context_pack": case["context_pack"],
                "lint_result": case["lint_result"],
                "dropped_reasons": case["retrieval_bundle"]["dropped"],
            }
        )
    if case["mode"] == "audit":
        transcript["receipt_ledger"] = receipt_ledger
    return transcript


def apply_tamper(case: dict, artifact_paths: dict[str, str], receipt_ledger: dict | None, transcript: dict) -> None:
    tamper = case.get("tamper", {})
    if not isinstance(tamper, dict):
        return

    for name in tamper.get("delete_artifacts", []):
        path_str = artifact_paths.get(name)
        if not path_str:
            continue
        path = Path(path_str)
        if path.exists():
            path.unlink()

    for name, path_str in tamper.get("artifact_path_overrides", {}).items():
        artifact_paths[name] = path_str

    corrupt_receipt_hashes = set(tamper.get("corrupt_receipt_hashes_for", []))
    remove_receipt_steps = set(tamper.get("remove_receipt_steps", []))
    if isinstance(receipt_ledger, dict):
        entries = []
        for entry in receipt_ledger.get("entries", []):
            step = entry.get("step")
            if step in remove_receipt_steps:
                continue
            proof = entry.get("proof", {})
            artifact_path = Path(proof.get("artifact_path", "")).name if proof.get("artifact_path") else None
            if artifact_path in corrupt_receipt_hashes:
                proof["artifact_sha256"] = "0" * 64
            entries.append(entry)
        receipt_ledger["entries"] = entries

    transcript_overrides = tamper.get("transcript_overrides", {})
    if isinstance(transcript_overrides, dict):
        override_object(transcript, transcript_overrides)


def assert_transcript(case: dict, transcript: dict, errors: list[str]) -> None:
    case_id = case["id"]
    expect = case["expect"]
    for key in expect.get("transcript_keys", []):
        if key not in transcript:
            fail(errors, case_id, f"transcript missing required key {key}")
    for key in expect.get("forbidden_transcript_keys", []):
        if key in transcript:
            fail(errors, case_id, f"transcript exposed forbidden key {key}")


def assert_transcript_claims(
    case: dict,
    transcript: dict,
    artifact_paths: dict[str, str],
    receipt_ledger: dict | None,
    errors: list[str],
) -> None:
    case_id = case["id"]
    if case["mode"] == "normal" and "artifact_paths" in transcript:
        fail(errors, case_id, "normal mode transcript claimed artifact paths")

    transcript_artifact_paths = transcript.get("artifact_paths")
    if transcript_artifact_paths is not None and transcript_artifact_paths != artifact_paths:
        fail(errors, case_id, "transcript artifact_paths are not backed by written artifacts")

    transcript_receipt_ledger = transcript.get("receipt_ledger")
    if transcript_receipt_ledger is not None and transcript_receipt_ledger != receipt_ledger:
        fail(errors, case_id, "transcript receipt ledger does not match generated receipts")


def assert_artifacts(case: dict, run_dir: Path, artifact_paths: dict[str, str], errors: list[str]) -> None:
    case_id = case["id"]
    expected = case["expect"].get("artifacts", [])
    for name in expected:
        path = run_dir / name
        if not path.exists():
            fail(errors, case_id, f"missing artifact {name}")
        elif artifact_paths.get(name) != str(path):
            fail(errors, case_id, f"artifact_paths missing or wrong for {name}")
    unexpected = sorted(path.name for path in run_dir.glob("*.json") if path.name not in expected)
    if unexpected:
        fail(errors, case_id, f"unexpected artifacts written: {', '.join(unexpected)}")


def assert_receipts(case: dict, receipt_ledger: dict | None, errors: list[str]) -> None:
    case_id = case["id"]
    if case["mode"] != "audit":
        if receipt_ledger is not None:
            fail(errors, case_id, "non-audit mode produced receipt ledger")
        return
    if not isinstance(receipt_ledger, dict):
        fail(errors, case_id, "audit mode did not produce receipt ledger")
        return
    if receipt_ledger.get("version") != "1.0" or receipt_ledger.get("mode") != "audit":
        fail(errors, case_id, "receipt ledger header is invalid")
    steps = [entry.get("step") for entry in receipt_ledger.get("entries", [])]
    if steps != REQUIRED_RECEIPT_STEPS:
        fail(errors, case_id, f"receipt steps mismatch: {steps}")

    artifact_names = set(case["expect"].get("receipt_artifacts", []))
    for entry in receipt_ledger.get("entries", []):
        proof = entry.get("proof", {})
        artifact_path = proof.get("artifact_path")
        artifact_hash = proof.get("artifact_sha256")
        if not artifact_path:
            continue
        path = Path(artifact_path)
        if path.name not in artifact_names:
            fail(errors, case_id, f"receipt references unexpected artifact {path.name}")
            continue
        if not path.exists():
            fail(errors, case_id, f"receipt artifact path does not exist: {path}")
            continue
        if artifact_hash != sha256(path):
            fail(errors, case_id, f"receipt hash mismatch for {path.name}")


def run_case(case: dict, router_config: dict[str, object], output_root: Path) -> list[str]:
    errors: list[str] = []
    case_id = case.get("id", "<unknown>")
    for key in ["id", "mode", "user_message", "expected_task_type", "expected_snippet_ids", "expect"]:
        if key not in case:
            fail(errors, case_id, f"missing required case key {key}")
            return errors

    routed = route_message(case["user_message"], router_config["router_rules"])
    if routed != case["expected_task_type"]:
        fail(errors, case_id, f"router expected {case['expected_task_type']}, found {routed}")

    assert_common_objects(case, router_config, errors)
    assert_compression_behavior(case, errors)

    run_dir = output_root / ".openclaw" / "context-runs" / f"{case['id']}-{case['mode']}"
    artifact_paths: dict[str, str] = {}
    receipt_ledger = None

    if case["mode"] in {"debug", "audit"}:
        artifact_paths = write_artifacts(case, run_dir)
    if case["mode"] == "audit":
        receipt_ledger = build_receipt_ledger(case, artifact_paths)
        receipt_path = run_dir / "receipt_ledger.json"
        write_json(receipt_path, receipt_ledger)
        artifact_paths["receipt_ledger.json"] = str(receipt_path)

    transcript = make_transcript(case, artifact_paths, receipt_ledger)
    apply_tamper(case, artifact_paths, receipt_ledger, transcript)
    assert_transcript(case, transcript, errors)
    assert_transcript_claims(case, transcript, artifact_paths, receipt_ledger, errors)
    assert_artifacts(case, run_dir, artifact_paths, errors)
    assert_receipts(case, receipt_ledger, errors)
    return errors


def assert_negative_case(case: dict, case_errors: list[str], errors: list[str]) -> None:
    case_id = case.get("id", "<unknown>")
    expected_failure = case.get("expect_failure", {})
    if not isinstance(expected_failure, dict):
        fail(errors, case_id, "negative fixture must define expect_failure")
        return

    expected_messages = expected_failure.get("contains", [])
    if not isinstance(expected_messages, list) or not expected_messages:
        fail(errors, case_id, "negative fixture expect_failure.contains must be a non-empty list")
        return

    if not case_errors:
        fail(errors, case_id, "expected harness failure but case passed")
        return

    for expected_message in expected_messages:
        if not any(expected_message in message for message in case_errors):
            fail(errors, case_id, f"expected failure containing: {expected_message}")


def main() -> int:
    script_path = Path(__file__).resolve()
    skill_root = script_path.parents[1]

    parser = argparse.ArgumentParser(description="Run dr-context-pipeline behavioral fixtures")
    parser.add_argument("--router", default=str(skill_root / "references" / "router.yml"), help="Router YAML path")
    parser.add_argument("--fixtures", default=str(skill_root / "references" / "tests" / "harness_cases.json"), help="Harness cases JSON path")
    parser.add_argument(
        "--failure-fixtures",
        help="Optional anti-fabrication fixture path. These cases must fail for the expected reason.",
    )
    parser.add_argument("--output-root", help="Optional output root for simulated run artifacts")
    parser.add_argument("--keep-runs", action="store_true", help="Keep temporary run artifacts")
    args = parser.parse_args()

    router_config = load_router_config(Path(args.router).resolve())
    cases = read_json(Path(args.fixtures).resolve())
    if not isinstance(cases, list):
        print("HARNESS FAILED")
        print(" - fixtures root must be a list")
        return 1

    failure_cases = []
    if args.failure_fixtures:
        failure_cases = read_json(Path(args.failure_fixtures).resolve())
        if not isinstance(failure_cases, list):
            print("HARNESS FAILED")
            print(" - failure fixtures root must be a list")
            return 1

    errors: list[str] = []
    temp_dir = None
    if args.output_root:
        output_root = Path(args.output_root).resolve()
        output_root.mkdir(parents=True, exist_ok=True)
    else:
        temp_dir = tempfile.mkdtemp(prefix="dr-context-pipeline-tests-")
        output_root = Path(temp_dir)

    try:
        for case in cases:
            if not isinstance(case, dict):
                errors.append("fixture case must be an object")
                continue
            errors.extend(run_case(case, router_config, output_root))
        for case in failure_cases:
            if not isinstance(case, dict):
                errors.append("failure fixture case must be an object")
                continue
            case_errors = run_case(case, router_config, output_root)
            assert_negative_case(case, case_errors, errors)
    finally:
        if temp_dir and not args.keep_runs:
            shutil.rmtree(temp_dir, ignore_errors=True)

    if errors:
        print("HARNESS FAILED")
        for error in errors:
            print(f" - {error}")
        return 1

    print("HARNESS PASSED")
    print(f"Cases checked: {len(cases)}")
    print("Covered modes: " + ", ".join(sorted({case["mode"] for case in cases})))
    if failure_cases:
        print(f"Expected-failure cases checked: {len(failure_cases)}")
    if args.output_root or args.keep_runs:
        print(f"Artifact root: {output_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
