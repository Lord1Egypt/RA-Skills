#!/usr/bin/env bash
# Tests for lib/common.sh primitives (Task 2). Sourced by tests/run.sh from repo root.

section "realpath_safe"
rt_setup="$(mktemp -d)"
mkdir -p "$rt_setup/target"
ln -s "$rt_setup/target" "$rt_setup/l1"
ln -s "$rt_setup/l1" "$rt_setup/l2"
ln -s "$rt_setup/l2" "$rt_setup/l3"
out=$(bash -c '. lib/common.sh; realpath_safe "'"$rt_setup"'/l3"')
expected=$(cd "$rt_setup/target" && pwd -P)
t_eq "3-deep symlink chain resolves" "$expected" "$out"
out=$(bash -c '. lib/common.sh; realpath_safe "'"$rt_setup"'/nope"')
expected=$(cd "$rt_setup" && pwd -P)/nope
t_eq "missing path falls back to input" "$expected" "$out"
mkdir -p "$rt_setup/@scope/bin"
out=$(bash -c '. lib/common.sh; realpath_safe "'"$rt_setup"'/@scope/bin/tool" 2>&1')
expected="$(cd "$rt_setup/@scope/bin" && pwd -P)/tool"
t_eq "@ in dir path: valid key, no bad substitution" "$expected" "$out"
rm -rf "$rt_setup"

section "is_darwin / is_system_path"
t_fail "override Linux is not darwin" bash -c '. lib/common.sh; BUTLER_OS_OVERRIDE=Linux is_darwin'
t_ok "override Darwin is darwin" bash -c '. lib/common.sh; BUTLER_OS_OVERRIDE=Darwin is_darwin'
t_ok "system path on darwin" bash -c '. lib/common.sh; BUTLER_OS_OVERRIDE=Darwin is_system_path /usr/bin/docker'
t_fail "/usr/local is not a system prefix" bash -c '. lib/common.sh; BUTLER_OS_OVERRIDE=Darwin is_system_path /usr/local/bin/docker'
t_fail "/usr/bin not system on Linux" bash -c '. lib/common.sh; BUTLER_OS_OVERRIDE=Linux is_system_path /usr/bin/docker'
t_ok "BUTLER_SYSTEM_PREFIXES override" bash -c '. lib/common.sh; BUTLER_SYSTEM_PREFIXES="/fake/usr/bin:/x" BUTLER_OS_OVERRIDE=Darwin is_system_path /fake/usr/bin/tool'
t_fail "relative path is never system" bash -c '. lib/common.sh; BUTLER_OS_OVERRIDE=Darwin is_system_path "usr/bin/docker"'

section "kv_field sanitization"
out=$(bash -c '. lib/common.sh; kv_field desc "$(printf "a\tb\nc")"; echo; exit 0' | awk -F'\t' 'NR==1{print $1}')
t_eq "TAB/NL stripped to space" "desc=a b c" "$out"
out=$(bash -c '. lib/common.sh; kv_field name docker; echo; exit 0' | awk -F'\t' 'NR==1{print $1}')
t_eq "plain value preserved" "name=docker" "$out"

section "du_size"
ds="$(mktemp -d)"; printf '12345' > "$ds/f"
out=$(bash -c '. lib/common.sh; du_size "'"$ds"'/f"')
t_eq "file size in bytes" "5" "$out"
out=$(bash -c '. lib/common.sh; du_size "'"$ds"'/missing"')
t_eq "missing path yields dash" "-" "$out"
printf 'hidden' > "$ds/locked"; chmod 000 "$ds/locked"
out=$(bash -c '. lib/common.sh; du_size "'"$ds"'/locked"' 2>&1)
t_eq "unreadable file yields dash, no stderr leak" "-" "$out"
rm -rf "$ds"

section "hist_last_used"
out=$(BUTLER_HIST_FILE="$FIXTURES/data/zsh_history" bash -c '. lib/common.sh; hist_last_used docker')
t_eq "max epoch for name" "1799000000" "$out"
out=$(BUTLER_HIST_FILE="$FIXTURES/data/zsh_history" bash -c '. lib/common.sh; hist_last_used git')
t_eq "single epoch extracted" "1700000001" "$out"
out=$(BUTLER_HIST_FILE="$FIXTURES/data/zsh_history" bash -c '. lib/common.sh; hist_last_used neverseen')
t_eq "absent name empty" "" "$out"
out=$(BUTLER_HIST_FILE="$FIXTURES/data/does-not-exist" bash -c '. lib/common.sh; hist_last_used docker')
t_eq "missing history empty" "" "$out"
