#!/usr/bin/env bash
# Tests for bin/refchain.sh (F5, Task 6). Sourced by tests/run.sh from repo root.

section "refchain five layers"

RC_BIN="$FIXTURES/refchain/bin"
JDIR="$(mktemp -d "${TMPDIR:-/tmp}/butler-refchain.XXXXXX")"
BUTLER_JOURNAL_DIR="$JDIR"  # journal_add below must hit the same dir ref_run sees
. "$REPO_ROOT/lib/common.sh"  # recompute JOURNAL from the dir above
RC_ZSHRC="$JDIR/zshrc"
printf 'export PATH="%s:$PATH"\nalias l3q="l3 -q"\n' "$RC_BIN" > "$RC_ZSHRC"

ref_run() { # <extra-env-k=v ...> <name> -> stdout of refchain
  local extra="$1"; shift
  env PATH="$FAKE_PATH:$RC_BIN" \
    BUTLER_SHELL_CONFIGS="$RC_ZSHRC" \
    BUTLER_LAUNCHD_DIRS="$FIXTURES/home/LaunchAgents" \
    BUTLER_CONFIG_FILES="$FIXTURES/home/.ssh/config:$FIXTURES/home/.gitconfig" \
    BUTLER_HIST_FILE="$FIXTURES/home/zsh_history" \
    BUTLER_JOURNAL_DIR="$JDIR" BUTLER_OS_OVERRIDE=Darwin BUTLER_SYSTEM_PREFIXES="" \
    $extra bash "$REPO_ROOT/bin/refchain.sh" "$@" 2>/dev/null
}

out=$(ref_run "" l3)
rc=$?
t_ok "refchain exits 0 on fixture chain" test "$rc" -eq 0

# layer 1: realpath + symlink chain (each hop shown, relative links normalized)
t_contains "layer1 realpath resolves to real-tool" \
  "realpath=$FIXTURES/refchain/real/real-tool" "$out"
t_contains "layer1 chain shows all hops" \
  "chain=$RC_BIN/l3 -> $RC_BIN/l2 -> $RC_BIN/l1 -> $FIXTURES/refchain/real/real-tool" "$out"

# layer 2: owner (untracked until journaled)
t_contains "layer2 owner untracked by default" "owner=manual|untracked" "$out"
journal_add l3 manual "$(date +%s)" test "hand placed"
out=$(ref_run "" l3)
t_contains "layer2 journaled manual" "owner=manual|manual" "$out"

# layer 3: PATH definition lines (dir export) and name mentions
t_contains "layer3 PATH export line" "path-ref=$RC_ZSHRC:1:" "$out"
t_contains "layer3 name mention line" "path-ref=$RC_ZSHRC:2:" "$out"

# last-used from zsh extended history
t_contains "last-used from zsh history epoch" "last-used=1700000000" "$out"

# layers 4+5 on loose-tool (fixtures reference it in plists and configs)
journal_add loose-tool manual "$(date +%s)" test "hand placed"
out=$(ref_run "" loose-tool)
t_contains "layer2 loose-tool journaled" "owner=manual|manual" "$out"
t_contains "layer4 active plist" \
  "launchd-ref=$FIXTURES/home/LaunchAgents/com.fake.brewsvc.plist" "$out"
t_contains "layer4 disabled plist flagged" \
  "launchd-ref=$FIXTURES/home/LaunchAgents/ai.fake.tool.plist.off (disabled)" "$out"
t_contains "layer5 ssh config ref" "config-ref=$FIXTURES/home/.ssh/config:" "$out"
t_contains "layer5 gitconfig ref" "config-ref=$FIXTURES/home/.gitconfig:" "$out"

# brew-owned binary resolves owner via channel enumeration
out=$(ref_run "" cowsay)
t_contains "layer2 brew prefix rule" "owner=brew|managed" "$out"

# missing arg / unknown binary
env PATH="$FAKE_PATH" BUTLER_JOURNAL_DIR="$JDIR" bash "$REPO_ROOT/bin/refchain.sh" neverseen-bin >/dev/null 2>&1
t_eq "unknown binary rc=1" 1 "$?"
t_contains "no arg usage" "usage" "$(env PATH="$FAKE_PATH" bash "$REPO_ROOT/bin/refchain.sh" 2>&1)"
