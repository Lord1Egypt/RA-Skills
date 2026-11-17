#!/usr/bin/env python3
"""Phase 9 recovery-suite runner.

Runs every deterministic fault-injection / recovery scenario in
``tests/recovery/`` and prints one line per scenario, so a single command answers
"can this workflow still recover?".

    python3 skills/agy-ppt/scripts/run_recovery_tests.py
    python3 skills/agy-ppt/scripts/run_recovery_tests.py -v
    python3 skills/agy-ppt/scripts/run_recovery_tests.py --json report.json

Exit code is ``0`` only when every scenario passes; any failure or error exits
non-zero.

No real Codex, Kiro or ``image_gen`` call is made and no subscription quota is
consumed: the scenarios use fake workers and each test forbids process spawning.
Live, quota-consuming recovery checks are opt-in and live in
``tests/integration/test_recovery_live.py`` (``AGY_PPT_LIVE_RECOVERY=1``).
"""

from __future__ import annotations

import argparse
import io
import json
import sys
import time
import unittest
from dataclasses import dataclass, field
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
TESTS_DIR = SKILL_DIR / "tests"
RECOVERY_DIR = TESTS_DIR / "recovery"
for _path in (str(TESTS_DIR), str(SKILL_DIR / "scripts")):
    if _path not in sys.path:
        sys.path.insert(0, _path)

# scenario module (in tests/recovery) -> human label for the summary
SCENARIOS: tuple[tuple[str, str], ...] = (
    ("test_generation_failure", "generation failure"),
    ("test_backend_unavailable", "backend unavailable"),
    ("test_artifact_ambiguous", "artifact ambiguous"),
    ("test_invalid_output", "invalid artifact"),
    ("test_interrupted_generation", "interrupted generation"),
    ("test_qa_regeneration", "QA regeneration"),
    ("test_assembly_failure", "assembly failure"),
    ("test_resume_idempotency", "resume/idempotency"),
    ("test_consecutive_generic_failure", "consecutive generic failure retry policy"),
    ("test_operator_quota_stops_dispatch", "operator-confirmed quota stops dispatch"),
)

HEADER = "Phase 9 Recovery Test"


@dataclass
class ScenarioReport:
    module: str
    label: str
    tests: int = 0
    failures: int = 0
    errors: int = 0
    skipped: int = 0
    duration: float = 0.0
    details: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.failures == 0 and self.errors == 0

    @property
    def verdict(self) -> str:
        return "PASS" if self.ok else "FAIL"

    def to_dict(self) -> dict:
        return {
            "module": self.module,
            "label": self.label,
            "verdict": self.verdict,
            "tests": self.tests,
            "failures": self.failures,
            "errors": self.errors,
            "skipped": self.skipped,
            "duration_seconds": round(self.duration, 3),
            "details": self.details,
        }


def _load_suite(module: str) -> unittest.TestSuite:
    return unittest.TestLoader().loadTestsFromName(f"recovery.{module}")


def run_scenario(module: str, label: str, verbosity: int) -> ScenarioReport:
    report = ScenarioReport(module=module, label=label)
    stream = sys.stderr if verbosity > 1 else io.StringIO()
    started = time.monotonic()
    try:
        suite = _load_suite(module)
        result = unittest.TextTestRunner(stream=stream, verbosity=verbosity).run(suite)
    finally:
        report.duration = time.monotonic() - started

    report.tests = result.testsRun
    report.failures = len(result.failures)
    report.errors = len(result.errors)
    report.skipped = len(result.skipped)
    for case, trace in list(result.failures) + list(result.errors):
        report.details.append(f"{case.id()}\n{trace.strip()}")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="show individual test names (repeat for unittest verbosity)")
    parser.add_argument("--scenario", action="append", metavar="MODULE",
                        help="run only this scenario module (repeatable)")
    parser.add_argument("--json", metavar="PATH", help="write a machine-readable report here")
    parser.add_argument("--list", action="store_true", help="list scenarios and exit")
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.list:
        for module, label in SCENARIOS:
            print(f"{module}\t{label}")
        return 0

    selected = SCENARIOS
    if args.scenario:
        wanted = set(args.scenario)
        selected = tuple(s for s in SCENARIOS if s[0] in wanted or s[1] in wanted)
        unknown = wanted - {s[0] for s in SCENARIOS} - {s[1] for s in SCENARIOS}
        if unknown:
            print(f"unknown scenario(s): {', '.join(sorted(unknown))}", file=sys.stderr)
            return 2
    if not selected:
        print("no scenarios selected", file=sys.stderr)
        return 2

    if not RECOVERY_DIR.is_dir():
        print(f"recovery suite not found: {RECOVERY_DIR}", file=sys.stderr)
        return 2

    print(HEADER)
    reports: list[ScenarioReport] = []
    for module, label in selected:
        report = run_scenario(module, label, verbosity=2 if args.verbose > 1 else 1)
        reports.append(report)
        suffix = ""
        if args.verbose:
            suffix = f" ({report.tests} tests"
            if report.skipped:
                suffix += f", {report.skipped} skipped"
            suffix += f", {report.duration:.2f}s)"
        print(f"{report.verdict} {label}{suffix}", flush=True)

    passed = sum(1 for r in reports if r.ok)
    total = len(reports)
    total_tests = sum(r.tests for r in reports)
    print()
    print(f"{passed}/{total} PASS")
    if args.verbose:
        print(f"{total_tests} tests total")

    failing = [r for r in reports if not r.ok]
    if failing:
        print()
        for report in failing:
            print(f"--- {report.label} ({report.module}) ---")
            for detail in report.details:
                print(detail)
                print()

    if args.json:
        payload = {
            "schema": "agy-ppt/recovery-test-report/1",
            "header": HEADER,
            "passed": passed,
            "total": total,
            "tests": total_tests,
            "scenarios": [r.to_dict() for r in reports],
        }
        Path(args.json).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    return 0 if not failing else 1


if __name__ == "__main__":
    raise SystemExit(main())
