#!/usr/bin/env python3
"""Phase 9B-9D live failure & recovery runner (opt-in, quota-consuming).

One command answers "does this workflow still recover when the real runtime
fails?" -- against the real Codex CLI, real separate processes, and the real
upstream assembly script.

    AGY_PPT_LIVE_RECOVERY=1 python3 skills/agy-ppt/scripts/run_live_recovery_tests.py

    # additionally run the process-interruption scenario (kills only the child
    # Codex process group this harness created and tracked)
    AGY_PPT_LIVE_RECOVERY=1 AGY_PPT_LIVE_RECOVERY_INTERRUPT=1 \
        python3 skills/agy-ppt/scripts/run_live_recovery_tests.py

Scenarios:

    partial resume        two real Python processes, 3 real render turns
    regenerate            real generation 1 -> qa_failed -> real generation 2
    process interruption  a real Codex generation killed mid-flight (double opt-in)
    assembly recovery     real upstream assembly failure -> fix -> complete (no Codex)

Every real Codex invocation is appended to ``codex_invocations.jsonl`` by the
process that makes it, so the counts printed at the end are file-based facts,
not in-memory bookkeeping.

Exit code is ``0`` only when no required scenario failed. A scenario that skips
because of a runtime capability blocker (no ``codex`` on PATH, built-in
``image_gen`` not exposed, no ``python-pptx`` for the assembly step, or the
interruption flag not set) is reported as ``SKIPPED`` and does not fail the run.
Nothing here uses an API key or the OpenAI Images API, and no dependency is
installed.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import shutil
import sys
import time
import unittest
from dataclasses import dataclass, field
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
TESTS_DIR = SKILL_DIR / "tests"
INTEGRATION_DIR = TESTS_DIR / "integration"
for _path in (str(INTEGRATION_DIR), str(TESTS_DIR), str(SKILL_DIR / "scripts")):
    if _path not in sys.path:
        sys.path.insert(0, _path)

HEADER = "Phase 9B-9D Live Failure & Recovery"

GATE_LIVE = "live"
GATE_INTERRUPT = "interrupt"

# module (in tests/integration) -> label, gate
SCENARIOS: tuple[tuple[str, str, str], ...] = (
    ("test_phase9_live_resume", "partial resume", GATE_LIVE),
    ("test_phase9_live_regenerate", "regenerate", GATE_LIVE),
    ("test_phase9_live_interruption", "process interruption", GATE_INTERRUPT),
    ("test_phase9_live_assembly_recovery", "assembly recovery", GATE_LIVE),
)

VERDICT_PASS = "PASS"
VERDICT_FAIL = "FAIL"
VERDICT_SKIPPED = "SKIPPED"


@dataclass
class ScenarioReport:
    module: str
    label: str
    verdict: str = VERDICT_SKIPPED
    tests: int = 0
    failures: int = 0
    errors: int = 0
    skipped: int = 0
    duration: float = 0.0
    reason: str = ""
    details: list[str] = field(default_factory=list)

    @property
    def failed(self) -> bool:
        return self.verdict == VERDICT_FAIL

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
            "reason": self.reason,
            "details": self.details,
        }


def _prepare_ledger(keep: bool) -> tuple["object", bool]:
    """Point every scenario at one shared ledger file and start it empty.

    Returns ``(ledger, owned)``. ``owned`` is False when the caller supplied the
    path through the environment, in which case the runner never deletes it.
    """
    from helpers import live_recovery as lr

    override = os.environ.get(lr.LEDGER_ENV_VAR)
    owned = not override
    if override:
        path = Path(override)
    else:
        path = lr.PROBE_ROOT / "live-recovery-run" / lr.LEDGER_FILENAME
        os.environ[lr.LEDGER_ENV_VAR] = str(path)
    if owned and not keep and path.exists():
        path.unlink()
    path.parent.mkdir(parents=True, exist_ok=True)
    return lr.InvocationLedger(path=path, scenario=""), owned


def run_scenario(module: str, label: str, verbosity: int) -> ScenarioReport:
    report = ScenarioReport(module=module, label=label)
    stream = sys.stderr if verbosity > 1 else io.StringIO()
    started = time.monotonic()
    try:
        suite = unittest.TestLoader().loadTestsFromName(module)
        result = unittest.TextTestRunner(stream=stream, verbosity=verbosity).run(suite)
    except Exception as exc:  # noqa: BLE001 - a load error must be reported, not raised
        report.duration = time.monotonic() - started
        report.verdict = VERDICT_FAIL
        report.errors = 1
        report.reason = f"could not load {module}: {exc}"
        report.details.append(report.reason)
        return report
    report.duration = time.monotonic() - started

    report.tests = result.testsRun
    report.failures = len(result.failures)
    report.errors = len(result.errors)
    report.skipped = len(result.skipped)
    for case, trace in list(result.failures) + list(result.errors):
        report.details.append(f"{case.id()}\n{trace.strip()}")

    if report.failures or report.errors:
        report.verdict = VERDICT_FAIL
    elif report.tests == 0 or report.skipped >= report.tests:
        report.verdict = VERDICT_SKIPPED
        if result.skipped:
            report.reason = str(result.skipped[0][1]).strip().splitlines()[0]
    else:
        report.verdict = VERDICT_PASS
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="show test names and timings (repeat for unittest verbosity)")
    parser.add_argument("--scenario", action="append", metavar="MODULE",
                        help="run only this scenario module or label (repeatable)")
    parser.add_argument("--json", metavar="PATH", help="write a machine-readable report here")
    parser.add_argument("--list", action="store_true", help="list scenarios and exit")
    parser.add_argument("--keep-ledger", action="store_true",
                        help="keep codex_invocations.jsonl after the run (debugging)")
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.list:
        for module, label, gate in SCENARIOS:
            print(f"{module}\t{label}\t{gate}")
        return 0

    if not INTEGRATION_DIR.is_dir():
        print(f"integration suite not found: {INTEGRATION_DIR}", file=sys.stderr)
        return 2

    from helpers import live_recovery as lr

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

    live = os.environ.get(lr.LIVE_ENV_FLAG) == "1"
    interrupt = os.environ.get(lr.INTERRUPT_ENV_FLAG) == "1"
    ledger, ledger_owned = _prepare_ledger(args.keep_ledger)

    print(HEADER)
    reports: list[ScenarioReport] = []
    for module, label, gate in selected:
        if not live:
            report = ScenarioReport(module=module, label=label, reason=lr.SKIP_REASON)
        elif gate == GATE_INTERRUPT and not interrupt:
            report = ScenarioReport(module=module, label=label, reason=lr.INTERRUPT_SKIP_REASON)
        else:
            report = run_scenario(module, label, verbosity=2 if args.verbose > 1 else 1)
        reports.append(report)
        line = f"{report.verdict} {label}"
        if report.verdict == VERDICT_SKIPPED and report.reason:
            line += f" ({report.reason})"
        elif args.verbose:
            line += f" ({report.tests} tests, {report.duration:.2f}s)"
        print(line, flush=True)

    invocations = ledger.total(None)
    duplicates = ledger.duplicate_count(None)
    fallbacks = ledger.api_fallback_count(None)

    print()
    print(f"codex real invocations: {invocations}")
    print(f"duplicate invocations: {duplicates}")
    print(f"api fallback count: {fallbacks}")

    failing = [r for r in reports if r.failed]
    passed = sum(1 for r in reports if r.verdict == VERDICT_PASS)
    skipped = sum(1 for r in reports if r.verdict == VERDICT_SKIPPED)
    print()
    print(f"{passed} PASS, {len(failing)} FAIL, {skipped} SKIPPED of {len(reports)} scenarios")

    if failing:
        print()
        for report in failing:
            print(f"--- {report.label} ({report.module}) ---")
            for detail in report.details:
                print(detail)
                print()

    if duplicates:
        print(f"duplicate Codex invocations detected: {duplicates}", file=sys.stderr)
    if fallbacks:
        print(f"API fallback was used {fallbacks} time(s): forbidden", file=sys.stderr)

    if args.json:
        payload = {
            "schema": "agy-ppt/live-recovery-test-report/1",
            "header": HEADER,
            "live_enabled": live,
            "interrupt_enabled": interrupt,
            "ledger_path": str(ledger.path),
            "codex_real_invocations": invocations,
            "duplicate_invocations": duplicates,
            "api_fallback_count": fallbacks,
            "passed": passed,
            "failed": len(failing),
            "skipped": skipped,
            "scenarios": [r.to_dict() for r in reports],
        }
        Path(args.json).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    if ledger_owned and not args.keep_ledger:
        shutil.rmtree(ledger.path.parent, ignore_errors=True)
        try:
            if lr.PROBE_ROOT.is_dir() and not any(lr.PROBE_ROOT.iterdir()):
                lr.PROBE_ROOT.rmdir()
        except OSError:  # pragma: no cover - defensive
            pass

    # Any required scenario failing, a duplicate invocation, or an API fallback
    # is a hard failure.
    if failing or duplicates or fallbacks:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
