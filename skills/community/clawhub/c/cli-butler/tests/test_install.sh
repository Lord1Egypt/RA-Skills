#!/usr/bin/env bash
# Tests for bin/install.sh (F3, Task 8). Sourced by tests/run.sh from repo root.

section "install routing + journal"

JDIR="$(mktemp -d "${TMPDIR:-/tmp}/butler-install.XXXXXX")"
LOG="$JDIR/install.log"
BUTLER_JOURNAL_DIR="$JDIR"
. "$REPO_ROOT/lib/common.sh" # recompute JOURNAL for assertions

logsz() { [ -f "$1" ] && wc -c < "$1" | tr -d ' ' || echo 0; }

ins_run() { # <extra-env> args... -> (stdout, rc in $?)
  local extra="$1"; shift
  env PATH="$FAKE_PATH" BUTLER_JOURNAL_DIR="$JDIR" BUTLER_OS_OVERRIDE=Darwin \
    BUTLER_FAKE_INSTALL_LOG="$LOG" $extra bash "$REPO_ROOT/bin/install.sh" "$@"
}

out=$(ins_run "" fakesay --dry-run)
t_eq "dry-run executes nothing" 0 "$(logsz "$LOG")"
t_contains "dry-run prints constructed command for fresh name" "brew install fakesay" "$out"
t_contains "plan names channel" "channel=brew" "$out"

out=$(ins_run "" fakesay --channel npm --dry-run)
t_contains "channel override routes to npm" "npm install -g fakesay" "$out"

: > "$LOG"
out=$(ins_run "" fakesay)
t_contains "new install executes by default" "brew install fakesay" "$(cat "$LOG" 2>/dev/null)"
t_contains "executed command carries proxy from webget" "proxy=http://127.0.0.1:7892" "$(cat "$LOG" 2>/dev/null)"
t_contains "install journaled" "fakesay" "$(journal_get fakesay)"
t_contains "plan line before execution" "channel=brew" "$out"

: > "$LOG"
out=$(ins_run "" fakesay) # already installed (journaled)
t_contains "overwrite is dry-run by default" "already installed" "$out"
t_eq "overwrite executes nothing without --yes" 0 "$(logsz "$LOG")"

: > "$LOG"
out=$(ins_run "" fakesay --yes)
t_contains "overwrite with --yes executes" "brew install fakesay" "$(cat "$LOG" 2>/dev/null)"

out=$(ins_run "" httpie --channel npm --dry-run)
t_contains "npm prefix mismatch warns" "prefix-warn" "$out"

out=$(ins_run "" neverseen-pkg --dry-run)
t_contains "unknown name still routed to a channel" "channel=brew" "$out"

env PATH="$FAKE_PATH" bash "$REPO_ROOT/bin/install.sh" >/dev/null 2>&1
t_ok "no arg rc nonzero" test "$?" -ne 0
