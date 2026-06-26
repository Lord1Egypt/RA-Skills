#!/usr/bin/env bash
set -euo pipefail

# Verify dependencies for openclaw-csv-toolkit.
#
# The skill is pure Python 3 standard library, so only python3 is needed.
# No pip install required. This script exists so users can run the same
# `check_deps.sh` they see in the other openclaw-* skills before any
# workflow.

missing=0

check() {
  local label="$1"
  local cmd="$2"
  local version_flag="${3:---version}"
  if command -v "$cmd" >/dev/null 2>&1; then
    local version
    version="$("$cmd" $version_flag 2>&1 | head -n1)"
    printf '  ok   %-10s %s\n' "$label" "$version"
  else
    printf '  MISS %-10s not on PATH\n' "$label"
    missing=$((missing + 1))
  fi
}

check python3 python3

if [ "$missing" -eq 0 ]; then
  echo
  echo "All dependencies satisfied."
  exit 0
fi
echo
echo "Missing $missing dependency/dependencies."
exit 1
