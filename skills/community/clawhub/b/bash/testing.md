# Testing — Lint Gates, bats, Stubs, Fixtures

Shell bugs are cheap to prevent and expensive to discover in production, because the failing path is usually the one nobody ran. Order the gates by cost: parse, lint, format, then real tests.

## The Three-Second Gate (run before any test suite)

```bash
bash -n script.sh                    # parse only
shellcheck -S warning script.sh      # -S at lint_gate; -x follows sourced files
shfmt -d -i 2 -ci script.sh          # -d shows the diff, -w applies it (-i = indent_style)
```

- `shellcheck` reads `.shellcheckrc` in the repo root: put project-wide `disable=` there with a comment, never scattered ad hoc
- Sourced libraries are invisible to shellcheck by default: `# shellcheck source=lib/common.sh` above the `source` line, or run with `-x`
- Files without a `.sh` extension need `# shellcheck shell=bash` on line 2 or `-s bash`
- Fail CI on the gate, not on a human noticing: one job, three commands, exit nonzero

## Make The Script Testable

```bash
main() {
  parse_args "$@"
  do_work
}
# only run when executed, not when sourced by a test
[[ ${BASH_SOURCE[0]} == "$0" ]] && main "$@"
```

- The source guard is what lets a test file `source ./script.sh` and call individual functions
- Inject every external dependency as an overridable variable: `: "${CURL:=curl}"` then `"$CURL" -sS …`. The test sets `CURL=./tests/fake-curl`
- Same for paths: `: "${CONFIG_DIR:=$HOME/.config/app}"`. A script with hardcoded absolute paths can only be tested by root on the real machine
- Keep pure logic (parsing, formatting, decisions) in functions that take arguments and print to stdout; those are testable without any fixture

## bats-core

```bash
# tests/deploy.bats
setup() {
  load '../script.sh'                     # source with the guard above
  TEST_DIR=$(mktemp -d); export TEST_DIR
}
teardown() { rm -rf "$TEST_DIR"; }

@test "version parser accepts a v-prefix" {
  run parse_version "v1.2.3"
  [ "$status" -eq 0 ]
  [ "$output" = "1.2.3" ]
}

@test "missing config exits 2 with a message on stderr" {
  run --separate-stderr main --config /nonexistent
  [ "$status" -eq 2 ]
  [[ $stderr == *"config not found"* ]]
}
```

- `run` captures status in `$status` and combined output in `$output`; it NEVER fails the test itself, so a test without a `$status` assertion asserts nothing
- `run --separate-stderr` (bats >=1.5) is how you assert that errors go to stderr — the property SKILL.md Core Rules demand of `die`
- `$lines[@]` holds the output split by line; `${lines[0]}` for the first
- One temp dir per test via `mktemp -d` in `setup` (or `$BATS_TEST_TMPDIR`), removed in `teardown` — tests that share a directory pass in isolation and fail in a suite
- `bats --jobs 4` parallelizes; any test writing to a fixed path breaks immediately under it, which is a useful design check

## Stubbing External Commands

Two mechanisms, chosen by what you are testing:

- **PATH shim** — the honest one, works even when the script `exec`s or subshells:
  ```bash
  setup() {
    STUB=$(mktemp -d); PATH="$STUB:$PATH"
    printf '#!/usr/bin/env bash\necho "$@" >> "$STUB/calls"\nexit 0\n' > "$STUB/aws"
    chmod +x "$STUB/aws"
  }
  ```
  Then assert on `$STUB/calls` — the arguments the script REALLY passed, which is what regressions change
- **Function override** — only works for code running in the same shell (sourced functions), and only if the script calls the command by bare name; `command curl` or `/usr/bin/curl` bypasses it
- Make stubs assert too: a stub that exits 1 when it receives an unexpected argument turns a silent wrong call into a failing test
- Never stub by editing the script under test; the version you tested must be the version you ship

## Testing The Failure Paths

- SKILL.md Core Rule 7 as a test: replace a dependency stub with one that exits 1, assert the script exits nonzero AND that the temp file is gone (`[ ! -e "$TEST_DIR/work.tmp" ]`) — that is how you prove the trap fired
- Signals: `timeout -s TERM 1 ./script.sh; [ $? -eq 143 ]` proves SIGTERM handling instead of assuming it
- Idempotence: run `main` twice against the same fixture and assert identical results — the cheapest test that catches non-rerunnable scripts
- Hostile inputs belong in the fixture set, not in your imagination: create files named `a b.txt`, `-rf`, `x'y`, and one with a newline (`touch "$(printf 'a\nb')"`)

## Golden Output

```bash
diff <(./render.sh fixtures/input.json) fixtures/expected.txt   # empty = pass
```

- Normalize what legitimately varies (timestamps, temp paths, hostnames) with a `sed` filter before diffing, or the test fails daily for the wrong reason
- Regenerate goldens with an explicit `UPDATE_GOLDEN=1` flag so a reviewer sees the diff in the pull request

## No-Dependency Harness

When bats cannot be installed (locked-down runners, `bash_floor` of 3.2), 20 lines are enough:

```bash
fails=0
check() { # check <description> <expected> <actual>
  [[ $2 == "$3" ]] && { printf 'ok   %s\n' "$1"; return; }
  printf 'FAIL %s\n  expected: %q\n  actual:   %q\n' "$1" "$2" "$3" >&2; fails=$((fails+1))
}
check "strips v prefix" "1.2.3" "$(parse_version v1.2.3)"
exit $(( fails > 0 ))
```

It gives you the two things that matter — a nonzero exit and a readable diff — and it runs anywhere bash runs. Upgrade to bats when the suite outgrows one file.
