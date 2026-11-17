#!/usr/bin/env bash
# Tests for bin/uninstall.sh (F4, Task 9). Sourced by tests/run.sh from repo root.

section "uninstall safety matrix"

JDIR="$(mktemp -d "${TMPDIR:-/tmp}/butler-uninst.XXXXXX")"
LOG="$JDIR/uninst.log"
BUTLER_JOURNAL_DIR="$JDIR"
. "$REPO_ROOT/lib/common.sh" # recompute JOURNAL for assertions

THOME="$(mktemp -d "${TMPDIR:-/tmp}/butler-uninst-home.XXXXXX")"
mkdir -p "$THOME/Library/LaunchAgents"
printf '<?xml version="1.0"?>\n<string>%s</string>\n' "$FAKE_BIN/manual-tool" \
  > "$THOME/Library/LaunchAgents/com.fake.manual.plist"

logsz() { [ -f "$1" ] && wc -c < "$1" | tr -d ' ' || echo 0; }

un_run() { # <extra-env> args...
  local extra="$1"; shift
  env PATH="$FAKE_PATH" HOME="$THOME" BUTLER_JOURNAL_DIR="$JDIR" BUTLER_OS_OVERRIDE=Darwin \
    BUTLER_FAKE_INSTALL_LOG="$LOG" $extra bash "$REPO_ROOT/bin/uninstall.sh" "$@"
}

# system: refuse outright, no plan, no execution
out=$(un_run "" sh 2>&1)
t_ok "system refuse rc nonzero" test "$?" -ne 0
t_contains "system refuse names reason" "system" "$out"
t_eq "system executes nothing" 0 "$(logsz "$LOG")"

# managed: dry-run plan by default; --yes routes via channel; channel-owned path never rm'd
out=$(un_run "" cowsay)
t_contains "managed dry-run prints route command" "brew uninstall cowsay" "$out"
t_eq "managed default executes nothing" 0 "$(logsz "$LOG")"

: > "$LOG"
out=$(un_run "" cowsay --yes)
t_contains "managed --yes executes via channel" "brew uninstall cowsay" "$(cat "$LOG" 2>/dev/null)"
t_ok "channel-owned path never rm'd" test -f "$FAKE_BIN/cowsay"

# manual journaled: refchain summary + dry-run; --yes removes + journal_del + plist moved
printf '#!/bin/sh\nexit 0\n' > "$FAKE_BIN/manual-tool"; chmod +x "$FAKE_BIN/manual-tool"
journal_add manual-tool manual 1700000000 "$FAKE_BIN/manual-tool" "fixture"
out=$(un_run "" manual-tool)
t_contains "manual shows refchain summary" "refs:" "$out"
t_contains "manual defaults to dry-run" "nothing executed" "$out"
t_ok "manual dry-run keeps file" test -f "$FAKE_BIN/manual-tool"

out=$(un_run "" manual-tool --yes)
t_ok "manual --yes removes file" test ! -f "$FAKE_BIN/manual-tool"
t_eq "manual --yes clears journal" 0 "$([ -n "$(journal_get manual-tool)" ] && echo 1 || echo 0)"
t_ok "launchd plist moved away (.off)" test -f "$THOME/Library/LaunchAgents/com.fake.manual.plist.off"

# untracked: same gate, no journal row to clear
printf '#!/bin/sh\nexit 0\n' > "$FAKE_BIN/stray-tool"; chmod +x "$FAKE_BIN/stray-tool"
out=$(un_run "" stray-tool)
t_contains "untracked dry-run shows refs" "refs:" "$out"
t_ok "untracked dry-run keeps file" test -f "$FAKE_BIN/stray-tool"
out=$(un_run "" stray-tool --yes)
t_ok "untracked --yes removes file" test ! -f "$FAKE_BIN/stray-tool"

env PATH="$FAKE_PATH" bash "$REPO_ROOT/bin/uninstall.sh" >/dev/null 2>&1
t_ok "no arg rc nonzero" test "$?" -ne 0
