---
name: ci-flake-triage
description: Detect flaky tests from JUnit XML retries and emit a triage report with top unstable cases.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---

# CI Flake Triage

Use this skill to turn noisy JUnit retry artifacts into a focused flaky-test report.

## What this skill does
- Reads one or more JUnit XML files (for example: first run + rerun artifacts)
- Aggregates status per test case (`passed`, `failed`, `skipped`, `error`)
- Flags flaky candidates when a test has both fail-like and pass outcomes
- Separates persistent failures from flaky failures
- Prints top flaky tests to prioritize stabilization work

## Inputs
Optional:
- `JUNIT_GLOB` (default: `test-results/**/*.xml`)
- `TRIAGE_TOP` (default: `20`)
- `OUTPUT_FORMAT` (`text` or `json`, default: `text`)
- `FAIL_ON_PERSISTENT` (`0` or `1`, default: `0`) — exit non-zero when persistent failures exist
- `FAIL_ON_FLAKE` (`0` or `1`, default: `0`) — exit non-zero when flaky candidates exist

## Run

Text report:

```bash
JUNIT_GLOB='artifacts/junit/**/*.xml' \
TRIAGE_TOP=15 \
bash skills/ci-flake-triage/scripts/triage-flakes.sh
```

JSON output for CI ingestion:

```bash
JUNIT_GLOB='artifacts/junit/**/*.xml' \
OUTPUT_FORMAT=json \
FAIL_ON_PERSISTENT=1 \
bash skills/ci-flake-triage/scripts/triage-flakes.sh
```

Run with bundled fixtures:

```bash
JUNIT_GLOB='skills/ci-flake-triage/fixtures/*.xml' \
bash skills/ci-flake-triage/scripts/triage-flakes.sh
```

## Output contract
- Exit `0` when no fail gates are enabled (default)
- Exit `1` if `FAIL_ON_PERSISTENT=1` and persistent failures are found
- Exit `1` if `FAIL_ON_FLAKE=1` and flaky candidates are found
- In `text` mode, prints summary + top flaky + persistent failures
- In `json` mode, prints machine-readable summary and testcase details
