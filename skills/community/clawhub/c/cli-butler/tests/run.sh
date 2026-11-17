#!/usr/bin/env bash
# cli-butler test runner: entrypoint smoke, library sandbox, then tests/test_*.sh modules.
set -u
cd "$(dirname "$0")/.." || exit 1
# shellcheck disable=SC1091  # sourced relative to repo root resolved above
. tests/lib.sh

section "entrypoints respond to -h"
for s in bin/*.sh; do t_ok "$s -h exits 0" "$s" -h; done

section "journal helpers (sandboxed)"
BUTLER_JOURNAL_DIR="$(mktemp -d)" bash -c '
  . lib/common.sh
  journal_add testcli manual 1700000000 "example-src" "note"
  [ -n "$(journal_get testcli)" ] || { echo "FAIL journal_add/get"; exit 1; }
  journal_del testcli
  [ -z "$(journal_get testcli)" ] || { echo "FAIL journal_del"; exit 1; }
'
journal_rc=$?
if [ "$journal_rc" -eq 0 ]; then t_ok "journal add/get/del cycle"; else t_fail "journal add/get/del cycle"; fi

for t in tests/test_*.sh; do
  [ -e "$t" ] || continue
  #shellcheck disable=SC1090
  . "$t"
done

finish
