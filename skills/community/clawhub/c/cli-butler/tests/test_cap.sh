#!/usr/bin/env bash
# Tests for bin/cap.sh (F6, Task 7). Sourced by tests/run.sh from repo root.

section "cap"

CAP_BIN="$FIXTURES/cap"
cap_run() { env PATH="$FAKE_PATH:$CAP_BIN" BUTLER_PROBE_TIMEOUT=1 \
  bash "$REPO_ROOT/bin/cap.sh" "$@" 2>/dev/null; }

out=$(cap_run good-cli)
t_contains "usage line extracted" "usage=Usage: good-cli <command> [options]" "$out"
t_contains "subcommand build" "command=build" "$out"
t_contains "subcommand build desc" "command=build	build stuff" "$out"
t_contains "subcommand deploy" "command=deploy" "$out"
t_eq "flags not listed as subcommands" 0 "$(printf '%s' "$out" | grep -c 'command=-v')"

out=$(cap_run h-only)
t_contains "falls back to -h" "usage=Usage: h-only [cmd]" "$out"

out=$(cap_run garbage-cli)
t_contains "unparseable help returns raw first paragraph" "raw=" "$out"

env PATH="$FAKE_PATH:$CAP_BIN" BUTLER_PROBE_TIMEOUT=1 bash "$REPO_ROOT/bin/cap.sh" slow-cli >/dev/null 2>&1
t_eq "slow help killed by probe timeout (rc=1)" 1 "$?"
out=$(env PATH="$FAKE_PATH:$CAP_BIN" BUTLER_PROBE_TIMEOUT=1 bash "$REPO_ROOT/bin/cap.sh" slow-cli 2>&1)
t_contains "timeout reports no help output" "no help output" "$out"

env PATH="$FAKE_PATH" bash "$REPO_ROOT/bin/cap.sh" neverseen-bin >/dev/null 2>&1
t_eq "missing cli rc=1" 1 "$?"
t_contains "no arg usage" "usage" "$(env PATH="$FAKE_PATH" bash "$REPO_ROOT/bin/cap.sh" 2>&1)"
