# Safety Net — pin behavior down before you move it

A refactor, rewrite, or port is only as trustworthy as the evidence that behavior did not change. This file covers how much evidence you need, how to get it for code that has none, and how to compare two implementations.

## Contents
1. Size the net to the blast radius · 2. Characterization tests · 3. Golden master / approval tests · 4. Differential testing · 5. Property-based and fuzz parity · 6. Seams for untestable code · 7. What to record as baseline · 8. Tools by language

## 1. Size the net to the blast radius

Measure coverage of the code you will actually touch, not the project average — a 90%-covered repo can have the function you are moving at 0%.

| Touched-code coverage | Strategy | Allowed moves before more tests exist |
|---|---|---|
| High (most branches exercised by meaningful assertions) | Refactor with tools, run the suite after each step | Any structural move, one at a time |
| Medium | Add targeted tests for exactly the paths you will touch, confirm they pass on the current code, confirm with a coverage run that they reach those lines | Same as high, once the new tests demonstrably hit the touched lines |
| Low / none | Characterize first (section 2); introduce the smallest seam needed (section 6) | Only tool-verified renames/moves; add new behavior in new, tested functions (sprout/wrap) rather than editing in place |

Caveats worth remembering:
- Line coverage is not branch coverage. A covered `if` line says nothing about the untested `else`. Read the branches you are about to touch.
- Some runners silently omit untested packages/files from the coverage total. Force-include them (`--cov=` the package root, `-coverpkg=./...`, `collectCoverageFrom`, etc.).
- A test that passes for both the old and a deliberately broken new version protects nothing. When in doubt, mutate one line and watch it fail.

## 2. Characterization tests

A characterization test records what the code **does**, not what it should do. It is the definition of "unchanged" for this task.

Recipe:
1. Pick the entry points the refactor touches (public functions, CLI commands, handlers).
2. Enumerate input classes: typical values, boundaries (`0`, empty, max size), invalid input, error paths, unusual-but-legal input (unicode, duplicates, negative numbers, NaN, time zones).
3. Run the current code and capture outputs, raised errors (type + message), and side effects (files written, calls made, log lines callers parse).
4. Assert exactly that, including surprising results. Name surprising cases clearly (`test_negative_quantity_currently_returns_discount`) so later readers see they are recorded quirks, not endorsements.
5. Run the new tests against the untouched code: they must pass before any edit.

If a recorded behavior looks like a bug, keep the test as is and list the bug under "Found, not fixed". Fixing it is a separate, approved change.

## 3. Golden master / approval tests

For code with large or structured outputs (reports, rendered HTML, generated code, CLI output, serialized data), snapshot the whole output:
- Generate a corpus of inputs (hand-picked + recorded production samples if the user can provide them + generated combinations).
- Store outputs as files next to the tests; diff on every run.
- Normalize only what is truly irrelevant (timestamps, random IDs, absolute paths) and write each normalization down — over-normalizing hides real differences.
- Review snapshot updates as code: an "update all snapshots" during a refactor means the refactor changed behavior.

## 4. Differential testing (rewrite and port)

Run the old and the new implementation on the same inputs and compare. This is the strongest evidence a rewrite or port can have.

- **Shared fixtures.** Keep inputs and expected outputs in language-neutral files (JSON/YAML/text) so both implementations run the same cases; this also gives you test parity for free.
- **Process-level harness.** For CLIs and services, invoke both binaries with identical argv/stdin/env (or HTTP requests) and compare stdout, stderr class, exit code, and produced files.
- **Shadow/parallel run.** For services, send a copy of real traffic to the new implementation, compare responses, but serve only the old one until differences are triaged.
- **Report the denominator.** "0 differences" means nothing without "over N inputs covering these classes". Say which input classes were not covered.
- **Triage every difference** into: new-code bug (fix), old-code bug that the user agrees to change (record in the contract), or irrelevant (add an explicit, documented normalization).

## 5. Property-based and fuzz parity

When inputs are large or combinatorial (parsers, encoders, numeric code), generate inputs instead of listing them:
- Property: `new(x) == old(x)` for generated `x` (via FFI, subprocess, or a recorded oracle).
- Round-trip properties: `decode(encode(x)) == x` in both implementations.
- Fuzz both with the same corpus; a crash or difference becomes a new fixture.

## 6. Seams for untestable code

A seam is a place where you can substitute behavior without editing the code under test. Introduce the smallest one that lets a test run:
- **Parameter/constructor injection:** pass the clock, filesystem, HTTP client, random source, or DB handle in instead of creating it inside.
- **Interface at the point of use:** declare a narrow interface (often one method) in the consumer; the existing concrete type already satisfies it in structurally typed languages (Go, TS) or via a thin adapter elsewhere.
- **Wrap/sprout:** put new logic in a new tested function and call it from the old code, instead of editing untested code in place.
- **Process boundary:** if nothing else works, test the program from outside (CLI/HTTP) — slower but needs no code change.

Keep seam-introducing edits tiny and mechanical; they are the only edits made before a net exists.

## 7. What to record as baseline

Before the first edit, capture and keep for the report:
- Test command(s) and results (pass/fail/skip counts, known failures).
- Type checker, linter, and build warnings — so new warnings are attributable.
- Coverage of the touched code (if available).
- Performance numbers if the code is on a hot path or the user mentioned speed — a refactor that regresses performance noticeably is a behavior change.
- For ports: the source toolchain version and how fixtures were produced.

## 8. Tools by language

| Language | Characterization / snapshots | Property / fuzz | Coverage |
|---|---|---|---|
| Python | pytest, syrupy or pytest-snapshot, approvaltests | hypothesis, atheris | coverage.py / pytest-cov |
| JS/TS | vitest or jest snapshots, approvals | fast-check | c8 / istanbul |
| Go | table tests, golden files (`-update` flag pattern), go-cmp | `testing.F` fuzzing, rapid | `go test -cover -coverpkg=./...` |
| Rust | insta snapshots | proptest, cargo-fuzz | cargo-llvm-cov / tarpaulin |
| Java/Kotlin | JUnit 5, ApprovalTests, AssertJ | jqwik, Kotest property | JaCoCo / Kover |
| C/C++ | GoogleTest, Catch2, golden files | libFuzzer, AFL++ (+ sanitizers) | gcov / llvm-cov |
| C# | xUnit/NUnit, Verify | FsCheck | coverlet |
