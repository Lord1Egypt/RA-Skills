#!/usr/bin/env bash
# tests for bin/list.sh (F1: grouped inventory)

JDIR="$(mktemp -d "${TMPDIR:-/tmp}/butler-list.XXXXXX")"
trap 'rm -rf "$JDIR"' EXIT
BUTLER_JOURNAL_DIR="$JDIR"   # must be set before common.sh computes JOURNAL
. "$REPO_ROOT/lib/common.sh"

LIST_RUN() { # extra env as args; runs list --kv in fake env
  env PATH="$FAKE_PATH:$FIXTURES/prefix/systembin" \
    BUTLER_LIST_PATH="$FAKE_BIN:$FIXTURES/prefix/systembin" \
    BUTLER_OS_OVERRIDE=Darwin \
    BUTLER_SYSTEM_PREFIXES="$FIXTURES/prefix/systembin" \
    BUTLER_JOURNAL_DIR="$JDIR" \
    "$@" \
    bash "$REPO_ROOT/bin/list.sh" --kv 2>/dev/null
}

section "list --kv structure"

kv=$(LIST_RUN)
t_ok "kv output non-empty" test -n "$kv"

row() { # row <name> <kv-output> -> single line for that name
  printf '%s\n' "$2" | awk -F'\t' -v n="$1" '$1 == "name=" n { print; exit }'
}
count() { printf '%s\n' "$2" | awk -F'\t' -v n="$1" '$1 == "name=" n { c++ } END { print c + 0 }'; }

c=$(row cowsay "$kv")
t_contains "row has name field" "name=cowsay" "$c"
t_contains "row has version" "version=3.7.0" "$c"
t_contains "cowsay resolves to brew" "channel=brew" "$c"
t_contains "cowsay category managed" "category=managed" "$c"
t_contains "cowsay desc from brew desc" "desc=Configurable talking cow" "$c"
t_contains "cowsay path resolved on PATH" "path=$FAKE_BIN/cowsay" "$c"

orb=$(row orbstack "$kv")
t_contains "cask orbstack channel brew" "channel=brew" "$orb"
t_contains "cask version" "version=1.9.1" "$orb"

ts=$(row typescript "$kv")
t_contains "typescript channel npm" "channel=npm" "$ts"
t_contains "npm desc from package.json" "desc=TypeScript is a superset of JavaScript" "$ts"

nest=$(row @nestjs/cli "$kv")
t_contains "pnpm scoped name intact" "version=11.0.0" "$nest"

sh_row=$(row sh "$kv")
t_contains "system prefix binary categorized system" "category=system" "$sh_row"
t_contains "system channel label" "channel=system" "$sh_row"

lt=$(row loose-tool "$kv")
t_contains "unjournaled loose binary untracked" "category=untracked" "$lt"
t_contains "whatis fallback desc" "desc=a loose test tool" "$lt"

tp=$(row tool-plain "$kv")
t_contains "second untracked fixture present" "category=untracked" "$tp"

# whatis budget 0: fallback disabled -> desc-sourced rows keep desc, others empty
kv3=$(env PATH="$FAKE_PATH:$FIXTURES/prefix/systembin" \
  BUTLER_LIST_PATH="$FAKE_BIN:$FIXTURES/prefix/systembin" BUTLER_OS_OVERRIDE=Darwin \
  BUTLER_SYSTEM_PREFIXES="$FIXTURES/prefix/systembin" BUTLER_JOURNAL_DIR="$JDIR" \
  BUTLER_WHATIS_BUDGET=0 bash "$REPO_ROOT/bin/list.sh" --kv)
lt3=$(row loose-tool "$kv3")
d3="${lt3##*desc=}"; d3="${d3//[[:space:]]/}"
t_eq "budget 0: whatis fallback desc exactly empty" "" "$d3"
cs3=$(row cowsay "$kv3")
t_contains "budget 0: bulk desc sources unaffected" "desc=Configurable talking cow" "$cs3"
tp3=$(row tool-plain "$kv3")
d3="${tp3##*desc=}"; d3="${d3//[[:space:]]/}"
t_eq "budget 0: tool-plain desc exactly empty" "" "$d3"

# journal loose-tool -> becomes manual
journal_add loose-tool manual "$(date +%s)" test "hand placed"
kv2=$(LIST_RUN)
lt2=$(row loose-tool "$kv2")
t_contains "journaled binary categorized manual" "category=manual" "$lt2"

t_eq "cowsay listed once (no dup across sources)" 1 "$(count cowsay "$kv")"
t_eq "fd listed once" 1 "$(count fd "$kv")"

section "human output"

human=$(env PATH="$FAKE_PATH:$FIXTURES/prefix/systembin" \
  BUTLER_LIST_PATH="$FAKE_BIN:$FIXTURES/prefix/systembin" BUTLER_OS_OVERRIDE=Darwin \
  BUTLER_SYSTEM_PREFIXES="$FIXTURES/prefix/systembin" \
  BUTLER_JOURNAL_DIR="$JDIR" bash "$REPO_ROOT/bin/list.sh" 2>/dev/null)
t_contains "brew group header with count" "== brew (4)" "$human"
t_contains "system group present" "system" "$human"
t_contains "system group warns non-uninstallable" "NOT uninstallable" "$human"
t_contains "untracked group present" "untracked" "$human"
t_contains "desc column populated" "Configurable talking cow" "$human"

section "slow channel does not block"

slowdir="$(mktemp -d "${TMPDIR:-/tmp}/butler-slow.XXXXXX")"
printf '#!/bin/sh\nsleep 300\n' > "$slowdir/npm"
chmod +x "$slowdir/npm"
t0=$(date +%s)
kv3=$(env PATH="$slowdir:$FAKE_PATH:$FIXTURES/prefix/systembin" \
  BUTLER_LIST_PATH="$FAKE_BIN:$FIXTURES/prefix/systembin" BUTLER_OS_OVERRIDE=Darwin \
  BUTLER_SYSTEM_PREFIXES="$FIXTURES/prefix/systembin" \
  BUTLER_JOURNAL_DIR="$JDIR" BUTLER_PROBE_TIMEOUT=1 \
  bash "$REPO_ROOT/bin/list.sh" --kv 2>/dev/null)
t1=$(date +%s)
t_ok "list completed in $((t1 - t0))s despite hanging npm" test $((t1 - t0)) -lt 15
t_contains "brew still listed with npm hung" "channel=brew" "$(row cowsay "$kv3")"
rm -rf "$slowdir"

section "empty environment"

env PATH=/nonexistent BUTLER_OS_OVERRIDE=Darwin BUTLER_JOURNAL_DIR="$JDIR" \
  /bin/bash "$REPO_ROOT/bin/list.sh" --kv >/dev/null 2>&1
t_ok "empty env exits 0" test "$?" -eq 0

