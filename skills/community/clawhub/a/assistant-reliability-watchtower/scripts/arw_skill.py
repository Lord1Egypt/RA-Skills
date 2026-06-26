#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = SKILL_DIR / "assets" / "example-config.json"
REPO_ROOT_ENV = "ARW_REPO_ROOT"
DEFAULT_EXPECTED_RECIPIENT = "dry-run:recipient"


def _looks_like_repo_root(path: Path) -> bool:
    return (path / "arw" / "run.py").is_file() and (path / "Makefile").is_file()


def _resolve_repo_root(explicit: str = "") -> Path:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit))
    env_repo_root = os.environ.get(REPO_ROOT_ENV, "")
    if env_repo_root:
        candidates.append(Path(env_repo_root))
    candidates.append(SKILL_DIR.parents[1])

    seen: set[Path] = set()
    for candidate in candidates:
        resolved = (candidate if candidate.is_absolute() else (Path.cwd() / candidate)).resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        if _looks_like_repo_root(resolved):
            return resolved

    raise FileNotFoundError(
        "Could not locate an ARW repo root. Pass --repo-root or set ARW_REPO_ROOT "
        "to a checkout containing arw/run.py and Makefile."
    )


def _load_config(path: str, repo_root: Path) -> dict[str, Any]:
    if not path:
        return {}

    config_path = Path(path)
    candidates = [config_path]
    if not config_path.is_absolute():
        candidates = [(Path.cwd() / config_path).resolve(), (repo_root / config_path).resolve()]

    for candidate in candidates:
        if candidate.is_file():
            return json.loads(candidate.read_text(encoding="utf-8"))
    return {}


def _env(repo_root: Path) -> dict[str, str]:
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(repo_root) if not existing else f"{repo_root}:{existing}"
    return env


def _run(command: list[str], repo_root: Path) -> int:
    result = subprocess.run(command, cwd=repo_root, env=_env(repo_root))
    return result.returncode


def _run_capture(command: list[str], repo_root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=repo_root,
        env=_env(repo_root),
        text=True,
        capture_output=True,
    )


def _cfg_value(config: dict[str, Any], key: str, fallback: Any) -> Any:
    value = config.get(key, fallback)
    return fallback if value in (None, "") else value


def _append_if(command: list[str], flag: str, value: Any) -> None:
    if value not in (None, ""):
        command.extend([flag, str(value)])


def _add_repo_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--repo-root", default="", help="Path to the ARW repo root (or set ARW_REPO_ROOT)")


def _add_common_digest_args(parser: argparse.ArgumentParser) -> None:
    _add_repo_arg(parser)
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Optional JSON config path")
    parser.add_argument("--out-dir", default="", help="Override artifact output dir")
    parser.add_argument("--window-hours", type=int, default=None)
    parser.add_argument("--trend-window", type=int, default=None)
    parser.add_argument("--trend-flip-threshold", type=int, default=None)
    parser.add_argument("--freshness-max-age-seconds", type=int, default=None)
    parser.add_argument("--probe-runtime-threshold-ms", type=int, default=None)
    parser.add_argument("--max-delivery-latency-seconds", type=int, default=None)
    parser.add_argument("--max-probe-evidence-age-seconds", type=int, default=None)
    parser.add_argument("--max-alignment-gap-seconds", type=int, default=None)
    parser.add_argument("--digest-as-of", default="")


def _add_common_validation_args(parser: argparse.ArgumentParser) -> None:
    _add_repo_arg(parser)
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Optional JSON config path")
    parser.add_argument("--out-dir", default="", help="Override artifact output dir")
    parser.add_argument("--window-hours", type=int, default=None)
    parser.add_argument("--trend-window", type=int, default=None)
    parser.add_argument("--trend-flip-threshold", type=int, default=None)
    parser.add_argument("--freshness-max-age-seconds", type=int, default=None)
    parser.add_argument("--probe-runtime-threshold-ms", type=int, default=None)
    parser.add_argument("--max-delivery-latency-seconds", type=int, default=None)
    parser.add_argument("--max-probe-evidence-age-seconds", type=int, default=None)
    parser.add_argument("--max-alignment-gap-seconds", type=int, default=None)
    parser.add_argument("--digest-as-of", default="")
    parser.add_argument("--expected-recipient", default="", help="Expected scorecard recipient")
    parser.add_argument("--actual-recipient", default="", help="Actual scorecard recipient")
    parser.add_argument("--send-ref", default="", help="Send evidence reference")
    parser.add_argument("--send-started-at", default="", help="Optional ISO-8601 send start time")
    parser.add_argument("--confirmation-ref", default="", help="Channel confirmation reference")
    parser.add_argument("--confirmation-at", default="", help="Optional ISO-8601 confirmation time")


def _build_digest_command(args: argparse.Namespace, config: dict[str, Any], out_dir: str) -> list[str]:
    command = [sys.executable, "-m", "arw.run", "--daily-digest", "--out-dir", str(out_dir)]
    _append_if(command, "--window-hours", args.window_hours if args.window_hours is not None else config.get("window_hours"))
    _append_if(command, "--trend-window", args.trend_window if args.trend_window is not None else config.get("trend_window"))
    _append_if(
        command,
        "--trend-flip-threshold",
        args.trend_flip_threshold if args.trend_flip_threshold is not None else config.get("trend_flip_threshold"),
    )
    _append_if(
        command,
        "--freshness-max-age-seconds",
        args.freshness_max_age_seconds if args.freshness_max_age_seconds is not None else config.get("freshness_max_age_seconds"),
    )
    _append_if(
        command,
        "--probe-runtime-threshold-ms",
        args.probe_runtime_threshold_ms if args.probe_runtime_threshold_ms is not None else config.get("probe_runtime_threshold_ms"),
    )
    _append_if(
        command,
        "--max-delivery-latency-seconds",
        args.max_delivery_latency_seconds
        if args.max_delivery_latency_seconds is not None
        else config.get("max_delivery_latency_seconds"),
    )
    _append_if(
        command,
        "--max-probe-evidence-age-seconds",
        args.max_probe_evidence_age_seconds
        if args.max_probe_evidence_age_seconds is not None
        else config.get("max_probe_evidence_age_seconds"),
    )
    _append_if(
        command,
        "--max-alignment-gap-seconds",
        args.max_alignment_gap_seconds if args.max_alignment_gap_seconds is not None else config.get("max_alignment_gap_seconds"),
    )
    _append_if(command, "--digest-as-of", args.digest_as_of)
    return command


def _resolve_out_dir_path(repo_root: Path, out_dir: str) -> Path:
    out_path = Path(out_dir)
    return out_path if out_path.is_absolute() else (repo_root / out_path).resolve()


def _parse_last_line_paths(output: str, expected_parts: int) -> list[str]:
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    if not lines:
        return []
    parts = lines[-1].split()
    return parts if len(parts) == expected_parts else []


def _load_latest_alert_paths(repo_root: Path, out_dir: str) -> dict[str, str]:
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    from arw.alert import load_latest_severe_alert_artifacts

    return load_latest_severe_alert_artifacts(_resolve_out_dir_path(repo_root, out_dir))


def _delivery_value(cli_value: str, config: dict[str, Any], key: str, fallback: str) -> str:
    return str(cli_value or _cfg_value(config, key, fallback))


def _run_verify_scorecard_evidence(args: argparse.Namespace) -> int:
    repo_root = _resolve_repo_root(args.repo_root)
    config = _load_config(args.config, repo_root)
    out_dir = args.out_dir or _cfg_value(config, "out_dir", "artifacts/arw")

    digest_result = _run_capture(_build_digest_command(args, config, out_dir), repo_root)
    if digest_result.returncode != 0:
        if digest_result.stdout:
            print(digest_result.stdout, end="")
        if digest_result.stderr:
            print(digest_result.stderr, end="", file=sys.stderr)
        return digest_result.returncode

    digest_paths = _parse_last_line_paths(digest_result.stdout, expected_parts=2)
    if len(digest_paths) != 2:
        return 2

    expected_recipient = _delivery_value(args.expected_recipient, config, "expected_recipient", DEFAULT_EXPECTED_RECIPIENT)
    actual_recipient = _delivery_value(args.actual_recipient, config, "actual_recipient", expected_recipient)
    send_ref = _delivery_value(args.send_ref, config, "send_ref", "dry-run:scorecard-evidence")
    confirmation_ref = _delivery_value(
        args.confirmation_ref,
        config,
        "confirmation_ref",
        "dry-run:scorecard-evidence",
    )
    send_started_at = _delivery_value(args.send_started_at, config, "send_started_at", "")
    confirmation_at = _delivery_value(args.confirmation_at, config, "confirmation_at", "")
    alert_paths = _load_latest_alert_paths(repo_root, out_dir)

    command = [
        sys.executable,
        "-m",
        "arw.run",
        "--validate-scorecard",
        "--out-dir",
        str(out_dir),
        "--artifact-json-path",
        digest_paths[0],
        "--artifact-markdown-path",
        digest_paths[1],
        "--expected-recipient",
        expected_recipient,
        "--actual-recipient",
        actual_recipient,
        "--send-ref",
        send_ref,
        "--confirmation-ref",
        confirmation_ref,
    ]
    _append_if(command, "--send-started-at", send_started_at)
    _append_if(command, "--confirmation-at", confirmation_at)
    _append_if(command, "--alert-json-path", alert_paths.get("json_path", ""))
    _append_if(command, "--alert-markdown-path", alert_paths.get("markdown_path", ""))

    validation_result = _run_capture(command, repo_root)
    if validation_result.returncode != 0:
        if validation_result.stdout:
            print(validation_result.stdout, end="")
        if validation_result.stderr:
            print(validation_result.stderr, end="", file=sys.stderr)
        return validation_result.returncode

    validation_paths = _parse_last_line_paths(validation_result.stdout, expected_parts=1)
    if len(validation_paths) != 1:
        return 2

    print(validation_paths[0])
    return 0


def _run_verify_scorecard_preamble(args: argparse.Namespace) -> int:
    repo_root = _resolve_repo_root(args.repo_root)
    config = _load_config(args.config, repo_root)
    out_dir = args.out_dir or _cfg_value(config, "out_dir", "artifacts/arw")

    digest_result = _run_capture(_build_digest_command(args, config, out_dir), repo_root)
    if digest_result.returncode != 0:
        if digest_result.stdout:
            print(digest_result.stdout, end="")
        if digest_result.stderr:
            print(digest_result.stderr, end="", file=sys.stderr)
        return digest_result.returncode

    digest_paths = _parse_last_line_paths(digest_result.stdout, expected_parts=2)
    if len(digest_paths) != 2:
        return 2

    expected_recipient = _delivery_value(args.expected_recipient, config, "expected_recipient", DEFAULT_EXPECTED_RECIPIENT)
    actual_recipient = _delivery_value(args.actual_recipient, config, "actual_recipient", expected_recipient)
    send_ref = _delivery_value(args.send_ref, config, "send_ref", "dry-run:scorecard-preamble")
    confirmation_ref = _delivery_value(
        args.confirmation_ref,
        config,
        "confirmation_ref",
        "dry-run:scorecard-preamble",
    )
    send_started_at = _delivery_value(args.send_started_at, config, "send_started_at", "")
    confirmation_at = _delivery_value(args.confirmation_at, config, "confirmation_at", "")
    alert_paths = _load_latest_alert_paths(repo_root, out_dir)

    validation_command = [
        sys.executable,
        "-m",
        "arw.run",
        "--validate-scorecard",
        "--out-dir",
        str(out_dir),
        "--artifact-json-path",
        digest_paths[0],
        "--artifact-markdown-path",
        digest_paths[1],
        "--expected-recipient",
        expected_recipient,
        "--actual-recipient",
        actual_recipient,
        "--send-ref",
        send_ref,
        "--confirmation-ref",
        confirmation_ref,
    ]
    _append_if(validation_command, "--send-started-at", send_started_at)
    _append_if(validation_command, "--confirmation-at", confirmation_at)
    _append_if(validation_command, "--alert-json-path", alert_paths.get("json_path", ""))
    _append_if(validation_command, "--alert-markdown-path", alert_paths.get("markdown_path", ""))

    validation_result = _run_capture(validation_command, repo_root)
    if validation_result.returncode != 0:
        if validation_result.stdout:
            print(validation_result.stdout, end="")
        if validation_result.stderr:
            print(validation_result.stderr, end="", file=sys.stderr)
        return validation_result.returncode

    validation_paths = _parse_last_line_paths(validation_result.stdout, expected_parts=1)
    if len(validation_paths) != 1:
        return 2

    render_result = _run_capture(
        [
            sys.executable,
            "-m",
            "arw.run",
            "--render-validation-preamble",
            "--validation-json-path",
            validation_paths[0],
            "--out-dir",
            str(out_dir),
        ],
        repo_root,
    )
    if render_result.stdout:
        print(render_result.stdout, end="")
    if render_result.stderr:
        print(render_result.stderr, end="", file=sys.stderr)
    return render_result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Repo-backed ARW skill wrapper")
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    smoke = subparsers.add_parser("smoke", help="Run ARW smoke probes")
    _add_repo_arg(smoke)
    smoke.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Optional JSON config path")
    smoke.add_argument("--out-dir", default="", help="Override artifact output dir")
    smoke.add_argument("--suite", default="", help="Override probe suite name")
    smoke.add_argument("--immediate-alert", action="store_true", help="Emit immediate alert artifacts when severe")
    smoke.add_argument("--alert-cooldown-seconds", type=int, default=None)

    digest = subparsers.add_parser("digest", help="Generate ARW daily digest")
    _add_common_digest_args(digest)

    verify = subparsers.add_parser("verify-scorecard-evidence", help="Generate a digest pair and validate the scorecard")
    _add_common_validation_args(verify)

    preamble = subparsers.add_parser("verify-scorecard-preamble", help="Generate a digest pair, validate it, and render the delivery preamble")
    _add_common_validation_args(preamble)

    render = subparsers.add_parser("render-validation-preamble", help="Render preamble from a validation artifact")
    _add_repo_arg(render)
    render.add_argument("validation_json_path")
    render.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Optional JSON config path")
    render.add_argument("--out-dir", default="", help="Override artifact output dir")

    args = parser.parse_args()

    if args.cmd == "verify-scorecard-evidence":
        return _run_verify_scorecard_evidence(args)

    if args.cmd == "verify-scorecard-preamble":
        return _run_verify_scorecard_preamble(args)

    repo_root = _resolve_repo_root(getattr(args, "repo_root", ""))
    config = _load_config(getattr(args, "config", str(DEFAULT_CONFIG_PATH)), repo_root)
    out_dir = getattr(args, "out_dir", "") or _cfg_value(config, "out_dir", "artifacts/arw")

    if args.cmd == "smoke":
        command = [sys.executable, "-m", "arw.run", "--suite", _cfg_value(config, "suite", args.suite or "smoke"), "--out-dir", str(out_dir)]
        cooldown = args.alert_cooldown_seconds if args.alert_cooldown_seconds is not None else config.get("alert_cooldown_seconds")
        if args.immediate_alert:
            command.append("--immediate-alert")
        _append_if(command, "--alert-cooldown-seconds", cooldown)
        return _run(command, repo_root)

    if args.cmd == "digest":
        return _run(_build_digest_command(args, config, out_dir), repo_root)

    if args.cmd == "render-validation-preamble":
        command = [
            sys.executable,
            "-m",
            "arw.run",
            "--render-validation-preamble",
            "--validation-json-path",
            args.validation_json_path,
            "--out-dir",
            str(out_dir),
        ]
        return _run(command, repo_root)

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
