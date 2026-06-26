#!/usr/bin/env bash
set -euo pipefail

# usage: run_sim.sh <rtl-file> <tb-file> <work-dir>
RTL_FILE="${1:-}"
TB_FILE="${2:-}"
WORK_DIR="${3:-sim}"

if [[ -z "$RTL_FILE" || -z "$TB_FILE" ]]; then
  echo "usage: run_sim.sh <rtl-file> <tb-file> <work-dir>" >&2
  exit 1
fi

mkdir -p "$WORK_DIR"
iverilog -o "$WORK_DIR/sim.out" "$RTL_FILE" "$TB_FILE" >"$WORK_DIR/compile.log" 2>&1
(
  cd "$WORK_DIR"
  vvp ./sim.out > sim.log 2>&1 || true
)
