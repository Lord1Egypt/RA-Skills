#!/usr/bin/env bash
# cli-butler test helpers: asserts + counters. Sourced by tests/run.sh and tests/test_*.sh.
#shellcheck disable=SC2034  # helpers set globals consumed by sibling modules

TESTS_PASS=0
TESTS_FAIL=0
CURRENT_SECTION=""

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURES="$REPO_ROOT/tests/fixtures"
FAKE_BIN="$FIXTURES/bin"
FAKE_PATH="$FAKE_BIN:$PATH"

section() { CURRENT_SECTION="$1"; printf '\n== %s ==\n' "$1"; }

_pass() { TESTS_PASS=$((TESTS_PASS + 1)); }
_fail() { printf 'FAIL [%s] %s\n' "$CURRENT_SECTION" "$1"; TESTS_FAIL=$((TESTS_FAIL + 1)); }

t_ok() { local d="$1"; shift; if "$@" >/dev/null 2>&1; then _pass; else _fail "$d (exit $?)"; fi; }

t_fail() { local d="$1"; shift; if "$@" >/dev/null 2>&1; then _fail "$d: expected nonzero exit"; else _pass; fi; }

t_eq() { # t_eq <desc> <expected> <actual>
  local d="$1" e="$2" a="$3"
  if [ "$e" = "$a" ]; then _pass
  else printf 'FAIL [%s] %s\n  expected: %s\n  actual:   %s\n' "$CURRENT_SECTION" "$d" "$e" "$a"; TESTS_FAIL=$((TESTS_FAIL + 1))
  fi
}

t_contains() { # t_contains <desc> <needle> <haystack>
  local d="$1" n="$2" h="$3"
  case "$h" in
    *"$n"*) _pass ;;
    *) printf 'FAIL [%s] %s\n  needle:   %s\n  haystack: %s\n' "$CURRENT_SECTION" "$d" "$n" "$h"; TESTS_FAIL=$((TESTS_FAIL + 1)) ;;
  esac
}

with_fakes() { PATH="$FAKE_PATH" "$@"; }

finish() {
  printf '\ntests: %d passed, %d failed\n' "$TESTS_PASS" "$TESTS_FAIL"
  [ "$TESTS_FAIL" -eq 0 ]
}
