"""Command-line entrypoint for Founder Signal."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import run_once
from .report import write_failed_marker, write_report
from .runtime_paths import ensure_runtime_dirs, resolve_root_dir
from .setup import doctor_user_config, import_user_config, render_doctor_report


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:
        print(f"Founder Signal error: {exc}", file=sys.stderr)
        return 1


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python3 -m founder_signal")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor_parser = subparsers.add_parser("doctor", help="Validate a canonical Founder Signal config JSON.")
    doctor_parser.add_argument("--config", required=True, help="Path to founder-signal.config.json")
    doctor_parser.add_argument(
        "--root-dir",
        default=None,
        help="Runtime data directory. Defaults to $FOUNDER_SIGNAL_HOME or ~/.founder-signal.",
    )
    doctor_parser.set_defaults(func=_doctor_command)

    init_parser = subparsers.add_parser("init", help="Create the Founder Signal runtime data directories.")
    init_parser.add_argument(
        "--root-dir",
        default=None,
        help="Runtime data directory. Defaults to $FOUNDER_SIGNAL_HOME or ~/.founder-signal.",
    )
    init_parser.set_defaults(func=_init_command)

    config_parser = subparsers.add_parser("config", help="Config management helpers.")
    config_subparsers = config_parser.add_subparsers(dest="config_command", required=True)
    config_import = config_subparsers.add_parser(
        "import",
        help="Validate and save a canonical Founder Signal config into profiles/.",
    )
    config_import.add_argument("config_path", help="Path to founder-signal.config.json")
    config_import.add_argument(
        "--root-dir",
        default=None,
        help="Runtime data directory. Defaults to $FOUNDER_SIGNAL_HOME or ~/.founder-signal.",
    )
    config_import.set_defaults(func=_config_import_command)

    run_parser = subparsers.add_parser("run", help="Run Founder Signal once.")
    run_parser.add_argument("--profile", help="Run only the selected profile_id.")
    run_parser.add_argument("--config", help="Validate and import this config before running.")
    run_parser.add_argument("--require-action-card", action="store_true")
    run_parser.add_argument(
        "--require-publish-intent",
        action="store_true",
        help=(
            "Compatibility flag: require a human-reviewable Draft URL, plus local "
            "public-run-review.md and draft-publish-intent.json compliance."
        ),
    )
    run_parser.add_argument("--require-draft-review-url", action="store_true")
    run_parser.add_argument("--require-all-profiles", action="store_true")
    run_parser.add_argument(
        "--root-dir",
        default=None,
        help="Runtime data directory. Defaults to $FOUNDER_SIGNAL_HOME or ~/.founder-signal.",
    )
    run_parser.set_defaults(func=_run_command)
    return parser


def _doctor_command(args: argparse.Namespace) -> int:
    root_dir = resolve_root_dir(args.root_dir)
    config_path = Path(args.config).resolve()
    result = doctor_user_config(root_dir=root_dir, config_path=config_path)
    print(render_doctor_report(result, config_path=config_path), end="")
    return 0


def _init_command(args: argparse.Namespace) -> int:
    root_dir = resolve_root_dir(args.root_dir)
    ensure_runtime_dirs(root_dir)
    print(f"Founder Signal runtime home: {root_dir}")
    print("Created directories: profiles, runs, logs, state, config-imports")
    print("Next command: python3 -m founder_signal doctor --config founder-signal.config.json")
    return 0


def _config_import_command(args: argparse.Namespace) -> int:
    root_dir = resolve_root_dir(args.root_dir)
    ensure_runtime_dirs(root_dir)
    config_path = Path(args.config_path).resolve()
    imported = import_user_config(root_dir=root_dir, config_path=config_path)
    print(f"Imported profile: {imported.profile_id}")
    print(f"Runtime home: {root_dir}")
    print(f"Profile path: {imported.profile_path}")
    print(f"Saved canonical config copy: {imported.normalized_config_path}")
    print(f"Next command: python3 -m founder_signal run --profile {imported.profile_id}")
    return 0


def _run_command(args: argparse.Namespace) -> int:
    root_dir = resolve_root_dir(args.root_dir)
    ensure_runtime_dirs(root_dir)
    selected_profile_id = args.profile
    if args.config:
        imported = import_user_config(root_dir=root_dir, config_path=Path(args.config).resolve())
        if selected_profile_id and selected_profile_id != imported.profile_id:
            raise ValueError(
                f"--profile {selected_profile_id} does not match imported config profile_id {imported.profile_id}."
            )
        selected_profile_id = imported.profile_id

    run_dir = _next_run_dir(root_dir)
    run_dir.mkdir(parents=True, exist_ok=False)
    result = run_once(
        root_dir=root_dir,
        run_dir=run_dir,
        selected_profile_id=selected_profile_id,
    )
    failures = _required_failures(
        result=result,
        require_action_card=bool(args.require_action_card),
        require_publish_intent=bool(args.require_publish_intent or args.require_draft_review_url),
        require_all_profiles=bool(args.require_all_profiles),
    )
    if failures:
        result["status"] = "failed"
        result["next_step"] = "provide_verified_evidence_and_retry_e2e"
        result["failures"] = list(dict.fromkeys([str(item) for item in result.get("failures", [])] + failures))
        result["error"] = "; ".join(failures)
        (run_dir / "run.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        write_report(run_dir=run_dir, artifact=result)
        write_failed_marker(run_dir=run_dir, artifact=result)
    print(json.dumps(result, indent=2))
    return 1 if result.get("status") == "failed" else 0


def _required_failures(
    *,
    result: dict,
    require_action_card: bool,
    require_publish_intent: bool,
    require_all_profiles: bool,
) -> list[str]:
    failures: list[str] = []
    profile_results = result.get("profile_results") or []
    failures.extend(_review_artifact_failures(result, label="run"))
    if require_action_card and not result.get("action_card_generated"):
        failures.append("required Action Card was not generated")
    if require_publish_intent and not _has_draft_url(result):
        failures.append("required Draft public page URL was not generated")
    if require_all_profiles:
        if not profile_results:
            failures.append("required profile checks found no profile results")
        for item in profile_results:
            profile_id = item.get("profile_id") or "unknown"
            failures.extend(_review_artifact_failures(item, label=str(profile_id)))
            if require_action_card and not item.get("action_card_generated"):
                failures.append(f"{profile_id}: required Action Card was not generated")
            if require_publish_intent and not _has_draft_url(item):
                failures.append(f"{profile_id}: required Draft public page URL was not generated")
    return failures


def _has_draft_url(result: dict) -> bool:
    return bool(result.get("draft_public_publish_succeeded")) and bool(
        str(result.get("draft_public_url") or result.get("draft_url") or "").strip()
    )


def _review_artifact_failures(result: dict, *, label: str) -> list[str]:
    failures: list[str] = []
    public_review = str(result.get("public_run_review_path") or "").strip()
    if public_review and not Path(public_review).exists():
        failures.append(f"{label}: public-run-review.md path does not exist")
    if not public_review:
        failures.append(f"{label}: public-run-review.md was not generated")
    intent_path = str(result.get("draft_publish_intent_path") or "").strip()
    intent_paths = result.get("draft_publish_intent_paths")
    has_intent = bool(intent_path) or (
        isinstance(intent_paths, list) and any(str(item).strip() for item in intent_paths)
    )
    if result.get("draft_publish_attempted") and not has_intent:
        failures.append(f"{label}: draft-publish-intent.json was not generated")
    if result.get("draft_public_publish_succeeded") and not _has_draft_url(result):
        failures.append(f"{label}: Draft publish succeeded but review URL is missing")
    if (
        result.get("draft_publish_attempted")
        and not result.get("draft_public_publish_succeeded")
        and not str(result.get("draft_public_publish_error") or "").strip()
    ):
        failures.append(f"{label}: Draft publish failed but no publish error was recorded")
    return failures


def _next_run_dir(root_dir: Path) -> Path:
    runs_dir = root_dir / "runs"
    while True:
        candidate = runs_dir / _run_timestamp()
        if not candidate.exists():
            return candidate


def _run_timestamp() -> str:
    from datetime import datetime

    return datetime.now().strftime("%Y-%m-%d-%H%M%S")


if __name__ == "__main__":
    raise SystemExit(main())
