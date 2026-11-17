#!/usr/bin/env python3
"""Run the deterministic acceptance checks for design-guide's three product journeys."""

from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys
import tempfile
import argparse

try:
    from i18n import add_locale_argument, t
except ModuleNotFoundError:  # Imported by the repository test suite.
    from scripts.i18n import add_locale_argument, t


ROOT = pathlib.Path(__file__).resolve().parents[1]


def run(label: str, command: list[str], env: dict[str, str] | None = None) -> tuple[bool, str]:
    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
        env=env,
        check=False,
    )
    output = (result.stdout + result.stderr).strip()
    return result.returncode == 0, f"{label}: {'PASS' if result.returncode == 0 else 'FAIL'}\n{output}"


def main() -> int:
    parser = argparse.ArgumentParser(description=t("Run deterministic design-guide product journey checks."))
    add_locale_argument(parser)
    args = parser.parse_args()
    results: list[tuple[bool, str]] = []

    results.append(
        run(
            "Journey 1 contract",
            [
                sys.executable,
                "scripts/design-contract.py",
                "validate",
                "tests/fixtures/quality/design-contract.json",
                "--project-root",
                ".",
                "--require-approved",
            ],
        )
    )
    results.append(
        run(
            "Journey 1 artifact presentation",
            [
                sys.executable,
                "scripts/present-design.py",
                "open",
                "tests/fixtures/quality/review-artifact.html",
                "--browser",
                "never",
            ],
        )
    )
    results.append(
        run(
            "Journey 2 isolated desktop review",
            [
                sys.executable,
                "scripts/evaluate-review-output.py",
                "tests/fixtures/review-behavior/desktop-url-isolated.json",
                "tests/fixtures/review-behavior/desktop-url-isolated-pass.md",
            ],
        )
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        env = os.environ.copy()
        env["F_DESIGN_SRC"] = str(ROOT)
        env["F_DESIGN_TARGET_HOME"] = temp_dir
        results.append(run("Journey 3 cross-AIDE sync", ["bash", "scripts/sync-aide.sh"], env=env))
        doctor_ok, doctor_output = run(
            "Journey 3 doctor",
            [
                sys.executable,
                "scripts/design-guide-doctor.py",
                "--source",
                str(ROOT),
                "--target-home",
                temp_dir,
                "--strict",
                "--json",
            ],
        )
        if doctor_ok:
            try:
                payload = json.loads(doctor_output.split("\n", 1)[1])
                doctor_ok = payload["healthy"] and len(payload["targets"]) == 4
            except (KeyError, json.JSONDecodeError):
                doctor_ok = False
        results.append((doctor_ok, doctor_output))

    for _, output in results:
        print(output)
    passed = sum(1 for ok, _ in results if ok)
    print(t("Product journeys: {passed}/{total} passed", args.locale, passed=passed, total=len(results)))
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
