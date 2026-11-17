#!/usr/bin/env bash
# Tests for bin/manage.sh (F2, Task 10). Sourced by tests/run.sh from repo root.

section "manage info/outdated/upgrade"

JDIR="$(mktemp -d "${TMPDIR:-/tmp}/butler-manage.XXXXXX")"
LOG="$JDIR/manage.log"
BUTLER_JOURNAL_DIR="$JDIR"
. "$REPO_ROOT/lib/common.sh"

logsz() { [ -f "$1" ] && wc -c < "$1" | tr -d ' ' || echo 0; }

mg_run() { # <extra-env> args...
  local extra="$1"; shift
  env PATH="$FAKE_PATH" BUTLER_JOURNAL_DIR="$JDIR" BUTLER_OS_OVERRIDE=Darwin \
    BUTLER_FAKE_INSTALL_LOG="$LOG" BUTLER_LAUNCHD_DIRS="$FIXTURES/home/LaunchAgents" $extra bash "$REPO_ROOT/bin/manage.sh" "$@"
}

# info: path/owner/size/launchd refs (reuses refchain output)
out=$(mg_run "" info cowsay)
t_contains "info shows real path" "realpath=$FAKE_BIN/cowsay" "$out"
t_contains "info shows owner" "owner=brew|managed" "$out"
t_contains "info shows size" "size=" "$out"

out=$(mg_run "" info loose-tool)
t_contains "info shows launchd refs" "launchd-ref=" "$out"

mg_run "" info neverseen >/dev/null 2>&1
t_ok "info unknown rc nonzero" test "$?" -ne 0

# outdated: per available channel, native support only, no guessing
out=$(mg_run "" outdated)
t_contains "outdated brew section lists cowsay" "cowsay" "$out"
t_contains "outdated parses versions" "3.8.0" "$out"
t_contains "outdated notes unsupported channels explicitly" "not supported" "$out"
out=$(mg_run "" outdated --channel cargo 2>&1)
t_contains "outdated explicit unsupported channel errors" "not supported" "$out"

# upgrade: resolve owner, dry-run default, --yes executes route cmd
out=$(mg_run "" upgrade cowsay)
t_contains "upgrade prints route command" "brew upgrade cowsay" "$out"
t_eq "upgrade default executes nothing" 0 "$(logsz "$LOG")"
: > "$LOG"
out=$(mg_run "" upgrade cowsay --yes)
t_contains "upgrade --yes executes via channel" "brew upgrade cowsay" "$(cat "$LOG" 2>/dev/null)"
t_ok "channel-owned path never rm'd on upgrade" test -f "$FAKE_BIN/cowsay"

mg_run "" upgrade loose-tool >/dev/null 2>&1
t_ok "upgrade untracked refuses rc nonzero" test "$?" -ne 0

mg_run "" frobnicate >/dev/null 2>&1
t_ok "unknown subcommand rc nonzero" test "$?" -ne 0
