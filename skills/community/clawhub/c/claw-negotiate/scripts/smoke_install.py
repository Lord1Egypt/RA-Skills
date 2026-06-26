#!/usr/bin/env python3
"""Smoke-check an installed or checked-out negotiate_safe skill.

This script is intentionally read-only by default. It validates the manifest,
checks that all deployable files exist, verifies required local commands are
discoverable, and can optionally invoke `run_safe.py doctor`.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SKILL_DIR = REPO_ROOT


def _runtime_dir(skill_dir: Path) -> Path:
    """Return the directory containing run_safe.py and skill_manifest.json.

    Public installs can clone this repo as the skill root, where SKILL.md lives
    at the top level and runtime files live under negotiate_safe/. Legacy/demo
    installs may point directly at negotiate_safe/.
    """
    if (skill_dir / "skill_manifest.json").exists():
        return skill_dir
    return skill_dir / "negotiate_safe"


def _load_manifest(runtime_dir: Path) -> dict:
    manifest_path = runtime_dir / "skill_manifest.json"
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def _check_files(runtime_dir: Path, manifest: dict) -> list[str]:
    errors: list[str] = []
    for rel in manifest.get("files", []):
        if not (runtime_dir / rel).exists():
            errors.append(f"missing file: {rel}")
    return errors


def _check_bins(manifest: dict, *, skip_openclaw: bool = False) -> list[str]:
    errors: list[str] = []
    for name in manifest.get("required_bins", []):
        if skip_openclaw and name == "openclaw":
            continue
        if shutil.which(name) is None:
            errors.append(f"missing command: {name}")
    return errors


def _run_manifest(runtime_dir: Path) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, str(runtime_dir / "run_safe.py"), "manifest"],
        capture_output=True,
        text=True,
        timeout=20,
    )
    return result.returncode, result.stdout or result.stderr


def _run_doctor(runtime_dir: Path) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, str(runtime_dir / "run_safe.py"), "doctor"],
        capture_output=True,
        text=True,
        timeout=60,
    )
    return result.returncode, result.stdout or result.stderr


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Smoke-check claw-negotiate install")
    parser.add_argument(
        "--skill-dir",
        default=str(DEFAULT_SKILL_DIR),
        help="Path to installed skill root or negotiate_safe runtime directory.",
    )
    parser.add_argument(
        "--skip-openclaw",
        action="store_true",
        help="Do not require the openclaw binary on this machine.",
    )
    parser.add_argument(
        "--run-doctor",
        action="store_true",
        help="Also invoke run_safe.py doctor. This may contact sshsign/OpenClaw.",
    )
    args = parser.parse_args(argv)

    skill_dir = Path(args.skill_dir).resolve()
    errors: list[str] = []

    if not skill_dir.exists():
        errors.append(f"skill dir missing: {skill_dir}")
    else:
        runtime_dir = _runtime_dir(skill_dir)
        if not (skill_dir / "SKILL.md").exists() and not (runtime_dir / "SKILL.md").exists():
            errors.append("missing SKILL.md")
        try:
            manifest = _load_manifest(runtime_dir)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"manifest invalid: {exc}")
            manifest = {}
        if manifest:
            errors.extend(_check_files(runtime_dir, manifest))
            errors.extend(_check_bins(manifest, skip_openclaw=args.skip_openclaw))
            rc, output = _run_manifest(runtime_dir)
            if rc != 0:
                errors.append(f"manifest command failed: {output.strip()}")
            else:
                try:
                    cli_manifest = json.loads(output)
                except json.JSONDecodeError as exc:
                    errors.append(f"manifest command returned non-json: {exc}")
                else:
                    if cli_manifest.get("name") != manifest.get("name"):
                        errors.append("manifest command name mismatch")

    if args.run_doctor and not errors:
        runtime_dir = _runtime_dir(skill_dir)
        rc, output = _run_doctor(runtime_dir)
        sys.stdout.write(output)
        if rc != 0:
            errors.append("doctor reported install/config failures")

    if errors:
        for error in errors:
            sys.stderr.write(f"fail  {error}\n")
        return 1

    sys.stdout.write(f"ok    negotiate_safe smoke check passed: {skill_dir}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
