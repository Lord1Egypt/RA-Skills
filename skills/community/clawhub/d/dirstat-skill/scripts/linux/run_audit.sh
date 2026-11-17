#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
STAMP="$(date +%Y%m%d_%H%M_audit)"
RUN_DIR="$REPO_ROOT/outputs/$STAMP"
TARGET_PATH="${1:-/home}"

mkdir -p "$RUN_DIR"
bash "$REPO_ROOT/scripts/linux/verify_ncdu.sh"
PYTHONPATH="$REPO_ROOT/src" python3 -m dirstat_skill.cli audit \
  --path "$TARGET_PATH" \
  --engine ncdu \
  --output-dir "$RUN_DIR" \
  --config "$REPO_ROOT/config/defaults.json"
echo "run_dir=$RUN_DIR"

