#!/usr/bin/env python3
"""Validate the installed context_pipeline bundle."""

from __future__ import annotations

import argparse
import json
import hashlib
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def iter_files(root: Path):
    for item in sorted(root.rglob("*")):
        if item.is_file():
            yield item


def validate_golden(golden, errors):
    if not isinstance(golden, list):
        errors.append("Golden tests file must be a list of cases")
        return
    for idx, case in enumerate(golden):
        if not isinstance(case, dict):
            errors.append(f"Golden case #{idx} is not an object")
            continue
        for key in ["id", "user_message", "expect"]:
            if key not in case:
                errors.append(f"Golden case #{idx} missing '{key}'")
        expect = case.get("expect", {})
        if not isinstance(expect, dict):
            errors.append(f"Golden case {case.get('id', idx)} expect must be object")
            continue
        # Soft checks on nested structures
        retrieval = expect.get("retrieval")
        if retrieval is not None and not isinstance(retrieval, dict):
            errors.append(f"Golden case {case.get('id', idx)} retrieval must be object")
        context_pack = expect.get("context_pack")
        if context_pack is not None and not isinstance(context_pack, dict):
            errors.append(f"Golden case {case.get('id', idx)} context_pack must be object")


def validate_harness_cases(cases, errors):
    if not isinstance(cases, list):
        errors.append("Harness cases file must be a list of cases")
        return
    required_modes = {"normal", "debug", "audit"}
    seen_modes = set()
    saw_fallback_case = False
    saw_dropped_case = False
    for idx, case in enumerate(cases):
        if not isinstance(case, dict):
            errors.append(f"Harness case #{idx} is not an object")
            continue
        for key in [
            "id",
            "mode",
            "user_message",
            "expected_task_type",
            "expected_snippet_ids",
            "retrieval_bundle",
            "context_pack",
            "lint_result",
            "expect",
        ]:
            if key not in case:
                errors.append(f"Harness case #{idx} missing '{key}'")
        mode = case.get("mode")
        if mode not in required_modes:
            errors.append(f"Harness case {case.get('id', idx)} has invalid mode: {mode}")
        else:
            seen_modes.add(mode)
        snippet_ids = case.get("expected_snippet_ids", [])
        if not isinstance(snippet_ids, list) or not all(isinstance(item, str) and item.startswith("S") for item in snippet_ids):
            errors.append(f"Harness case {case.get('id', idx)} expected_snippet_ids must be S* strings")
        expect = case.get("expect", {})
        if not isinstance(expect, dict):
            errors.append(f"Harness case {case.get('id', idx)} expect must be object")
        lint_result = case.get("lint_result", {})
        if isinstance(lint_result, dict) and lint_result.get("fallback_used") is True:
            saw_fallback_case = True
        retrieval_bundle = case.get("retrieval_bundle", {})
        if isinstance(retrieval_bundle, dict) and retrieval_bundle.get("dropped"):
            saw_dropped_case = True
    missing_modes = required_modes - seen_modes
    if missing_modes:
        errors.append("Harness cases missing modes: " + ", ".join(sorted(missing_modes)))
    if not saw_fallback_case:
        errors.append("Harness cases must include at least one lint fallback fixture")
    if not saw_dropped_case:
        errors.append("Harness cases must include at least one dropped-snippet fixture")


def validate_failure_cases(cases, errors):
    if not isinstance(cases, list):
        errors.append("Anti-fabrication cases file must be a list of cases")
        return
    for idx, case in enumerate(cases):
        if not isinstance(case, dict):
            errors.append(f"Anti-fabrication case #{idx} is not an object")
            continue
        for key in [
            "id",
            "mode",
            "user_message",
            "expected_task_type",
            "expected_snippet_ids",
            "retrieval_bundle",
            "context_pack",
            "lint_result",
            "expect",
            "tamper",
            "expect_failure",
        ]:
            if key not in case:
                errors.append(f"Anti-fabrication case #{idx} missing '{key}'")
        tamper = case.get("tamper", {})
        if not isinstance(tamper, dict):
            errors.append(f"Anti-fabrication case {case.get('id', idx)} tamper must be object")
        expect_failure = case.get("expect_failure", {})
        if not isinstance(expect_failure, dict):
            errors.append(f"Anti-fabrication case {case.get('id', idx)} expect_failure must be object")
            continue
        contains = expect_failure.get("contains")
        if not isinstance(contains, list) or not contains or not all(isinstance(item, str) for item in contains):
            errors.append(f"Anti-fabrication case {case.get('id', idx)} expect_failure.contains must be a non-empty string list")


def main() -> int:
    script_path = Path(__file__).resolve()
    workspace_root = script_path.parents[3]
    skill_root = script_path.parents[1]

    default_context = workspace_root / "context_pipeline"
    default_assets = skill_root / "assets" / "context_pipeline"

    parser = argparse.ArgumentParser(description="Validate context_pipeline installation")
    parser.add_argument("--context-root", default=str(default_context), help="Path to the installed context_pipeline folder")
    parser.add_argument("--assets-root", default=str(default_assets), help="Path to the source assets for comparison")
    args = parser.parse_args()

    context_root = Path(args.context_root).resolve()
    assets_root = Path(args.assets_root).resolve()

    errors = []

    if not context_root.exists():
        errors.append(f"Context root does not exist: {context_root}")
    if not assets_root.exists():
        errors.append(f"Assets root does not exist: {assets_root}")

    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        return 1

    # Compare hashes
    missing = []
    mismatched = []
    for asset_file in iter_files(assets_root):
        rel = asset_file.relative_to(assets_root)
        target_file = context_root / rel
        if not target_file.exists():
            missing.append(str(rel))
            continue
        asset_hash = sha256(asset_file)
        target_hash = sha256(target_file)
        if asset_hash != target_hash:
            mismatched.append((str(rel), asset_hash, target_hash))

    extra_files = []
    asset_paths = {str(f.relative_to(assets_root)) for f in iter_files(assets_root)}
    for target_file in iter_files(context_root):
        rel = str(target_file.relative_to(context_root))
        if rel not in asset_paths:
            extra_files.append(rel)

    for rel in missing:
        errors.append(f"Missing file in context root: {rel}")
    for rel, asset_hash, target_hash in mismatched:
        errors.append(f"Hash mismatch for {rel}: expected {asset_hash}, found {target_hash}")
    if extra_files:
        errors.append("Extra files present: " + ", ".join(extra_files))

    # JSON/schema sanity checks
    json_files = [
        context_root / "schemas" / "context_pack.schema.json",
        context_root / "schemas" / "receipt_ledger.schema.json",
        context_root / "schemas" / "retrieval_bundle.schema.json",
        context_root / "tests" / "golden.json",
        context_root / "tests" / "harness_cases.json",
        context_root / "tests" / "anti_fabrication_cases.json",
    ]
    for json_path in json_files:
        try:
            data = json.loads(json_path.read_text())
            if json_path.name == "golden.json":
                validate_golden(data, errors)
            if json_path.name == "harness_cases.json":
                validate_harness_cases(data, errors)
            if json_path.name == "anti_fabrication_cases.json":
                validate_failure_cases(data, errors)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"Failed to parse {json_path}: {exc}")

    if errors:
        print("VALIDATION FAILED")
        for err in errors:
            print(f" - {err}")
        return 1

    print("VALIDATION PASSED")
    print(f"Context root: {context_root}")
    print(f"Assets root:  {assets_root}")
    print(f"Total files checked: {len(list(iter_files(context_root)))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
