# Python review

Use the project's interpreter/environment and --lang python for its package.
Read patterns.md for redundancy, zombie code and gates.

## Behavior and cost

Trace real inputs, exception propagation and state changes. Confirm whether
imports create side effects before importing a project for inspection.
Profile list/string operations and repeated parsing on the actual workload;
a regex or an operator alone does not establish quadratic behavior.
Check interpreter/build and extension behavior before making concurrency/GIL claims.
Free-threaded CPython builds (3.13 and later) remove the GIL that some code relies
on as an implicit lock; check which build the project supports.

## Unused code

When already installed, Vulture can nominate unused functions, imports and
unreachable statements. Review its scope and confidence semantics. Check dynamic
getattr/importlib use, decorators, framework route discovery, pytest fixtures,
plugin entry points, serialization hooks and public package exports.

A function used only by a test may lack production integration, or be a supported
library API. Follow roots and external contracts before deletion. Examine mutually
dependent modules disconnected from all supported roots.

Keep any whitelist narrow, justified and current. An ignored name can hide
unrelated symbols; suppression is not evidence of use.

## Redundancy and gates

Compare duplicated validation/calculation at the same trust boundary and state.
Inspect broad except blocks, placeholder success returns, stale configuration,
empty test discovery and reports ignored by CI.
Test oracles should discriminate a deliberately wrong result. Mock counts and
lack of parametrization alone do not prove bad tests.

## Validation

Use existing pytest/unittest suites. Pytest exit code 5 means no tests collected;
exit 0 with only skipped tests still does not exercise behavior.
The helper reads a fresh JUnit report from pytest, counts executed cases and
keeps its reports/cache in a temporary directory. A failed run carries a
failure_kind: an ImportError or missing module during collection is environment,
not a reproduced defect. When the project has a virtual environment, the hint
suggests running its interpreter, for example
--command '.venv/bin/python -m pytest --junitxml {report}'.

For custom commands, write JUnit to {report}. If --scale is requested, the harness
must process that workload and write {"observed_scale": N} to the path in
CODESIFT_METRICS_PATH (PCR_METRICS_PATH is set to the same path for older
harnesses); the reviewer must inspect how the harness derives it. Exporting
TEST_SCALE alone is insufficient.

The dependency helper reads pyproject (PEP 621 groups, Poetry including legacy
dev-dependencies and custom sources, uv sources and indexes), requirements files
with -r includes, continuation lines and --hash pins, setup.cfg, Pipfile, and
literal setup.py declarations without executing setup.py. It reads setup.py even
when requirements files exist. Per-line errors name file:line and leave the other
lines parsed. Dynamic includes and private index resolution remain explicit
coverage limits.

Primary sources, checked 2026-11-03:
[Vulture](https://github.com/jendrikseipp/vulture),
[pytest exit codes](https://docs.pytest.org/en/stable/reference/exit-codes.html).
