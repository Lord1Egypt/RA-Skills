#!/usr/bin/env python3
"""Run the kai-business-blueprint release verification chain."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Step:
    name: str
    command: list[str]
    cwd: str


@dataclass(frozen=True)
class StepResult:
    name: str
    command: str
    cwd: str
    ok: bool
    returncode: int
    stdout: str
    stderr: str


def command_string(command: list[str], root: Path | None = None) -> str:
    normalized = list(command)
    if normalized and Path(normalized[0]).resolve() == Path(sys.executable).resolve():
        normalized[0] = "python"
    if root is not None:
        repo_root = root.resolve()
        for index, token in enumerate(normalized[1:], start=1):
            try:
                token_path = Path(token).resolve()
            except OSError:
                continue
            try:
                normalized[index] = token_path.relative_to(repo_root).as_posix()
            except ValueError:
                continue
    return subprocess.list2cmdline(normalized)


def resolve(root: Path, relative_path: str) -> Path:
    return (root / relative_path).resolve()


def validate_skill_eval_args(args: argparse.Namespace) -> None:
    if args.skill_evals_runner == "fixture":
        return
    if args.skill_evals_runner == "trace" and args.skill_evals_normalized_trace and args.skill_evals_case_id:
        return
    raise SystemExit("--skill-evals-runner 'trace' requires --skill-evals-normalized-trace and --skill-evals-case-id")


def build_steps(root: Path, args: argparse.Namespace) -> list[Step]:
    python = sys.executable
    validate_skill_eval_args(args)
    steps: list[Step] = []

    if not args.skip_pytest:
        steps.append(
            Step(
                name="pytest",
                command=[python, "-m", "pytest", "scripts/tests", "-q"],
                cwd=str(root),
            )
        )

    skill_command = [
        python,
        str(resolve(root, "scripts/run-skill-evals.py")),
        "--root",
        str(root),
        "--runner",
        args.skill_evals_runner,
        "--format",
        "json",
        "--json-out",
        str(resolve(root, args.skill_evals_json_out)),
    ]
    if args.skill_evals_case_id:
        skill_command.extend(["--case-id", args.skill_evals_case_id])
    if args.skill_evals_normalized_trace:
        skill_command.extend(["--normalized-trace", str(resolve(root, args.skill_evals_normalized_trace))])
    steps.append(Step(name="skill-evals", command=skill_command, cwd=str(root)))

    return steps


def dry_run_payload(steps: list[Step]) -> dict[str, object]:
    return {
        "steps": [
            {
                "name": step.name,
                "command": command_string(step.command, Path(step.cwd)),
                "cwd": step.cwd,
            }
            for step in steps
        ]
    }


def run_steps(steps: list[Step]) -> list[StepResult]:
    results: list[StepResult] = []
    for step in steps:
        completed = subprocess.run(
            step.command,
            cwd=step.cwd,
            capture_output=True,
            text=True,
            timeout=900,
        )
        results.append(
            StepResult(
                name=step.name,
                command=command_string(step.command, Path(step.cwd)),
                cwd=step.cwd,
                ok=completed.returncode == 0,
                returncode=completed.returncode,
                stdout=completed.stdout,
                stderr=completed.stderr,
            )
        )
        if completed.returncode != 0:
            break
    return results


def print_text_results(results: list[StepResult]) -> int:
    failures = 0
    for result in results:
        status = "PASS" if result.ok else "FAIL"
        print(f"{status} {result.name}")
        print(f"  cwd: {result.cwd}")
        print(f"  cmd: {result.command}")
        if result.stdout.strip():
            print("  stdout:")
            for line in result.stdout.strip().splitlines():
                print(f"    {line}")
        if result.stderr.strip():
            print("  stderr:")
            for line in result.stderr.strip().splitlines():
                print(f"    {line}")
        if not result.ok:
            failures += 1
    print()
    print(f"Summary: {len(results) - failures} passed, {failures} failed.")
    return 0 if failures == 0 else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format.")
    parser.add_argument("--dry-run", action="store_true", help="Print the verification plan without running it.")
    parser.add_argument("--skip-pytest", action="store_true", help="Skip the pytest suite.")
    parser.add_argument("--skill-evals-runner", choices=["fixture", "trace"], default="fixture")
    parser.add_argument("--skill-evals-case-id", help="Run one captured-run skill eval case.")
    parser.add_argument("--skill-evals-normalized-trace", help="Use one agent-agnostic normalized trace for the selected case.")
    parser.add_argument(
        "--skill-evals-json-out",
        default=".tmp/verify-release/skill-evals.json",
        help="Output path for captured-run skill eval JSON, relative to repo root.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    steps = build_steps(root, args)

    if args.dry_run:
        payload = dry_run_payload(steps)
        if args.format == "json":
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            for step in payload["steps"]:
                print(f"PLAN {step['name']}")
                print(f"  cwd: {step['cwd']}")
                print(f"  cmd: {step['command']}")
        return 0

    results = run_steps(steps)
    payload = {
        "steps": [asdict(result) for result in results],
        "summary": {
            "total": len(steps),
            "executed": len(results),
            "failed": sum(1 for result in results if not result.ok),
        },
    }
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if payload["summary"]["failed"] == 0 and payload["summary"]["executed"] == payload["summary"]["total"] else 1
    return print_text_results(results)


if __name__ == "__main__":
    sys.exit(main())
