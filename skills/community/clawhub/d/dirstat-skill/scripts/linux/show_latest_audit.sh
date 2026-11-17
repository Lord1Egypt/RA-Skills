#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LATEST_RUN="$(find "$REPO_ROOT/outputs" -maxdepth 1 -mindepth 1 -type d -name '*_audit' | sort | tail -n 1)"

if [ -z "$LATEST_RUN" ]; then
  echo "ERROR: no audit run found" >&2
  exit 6
fi

echo "latest_run=$LATEST_RUN"
echo "=== summary.md ==="
sed -n '1,120p' "$LATEST_RUN/summary.md"
echo
echo "=== top_dirs.csv ==="
sed -n '1,80p' "$LATEST_RUN/top_dirs.csv"
echo
echo "=== top_files.csv ==="
sed -n '1,80p' "$LATEST_RUN/top_files.csv"
echo
echo "=== candidates.json ==="
sed -n '1,200p' "$LATEST_RUN/candidates.json"
