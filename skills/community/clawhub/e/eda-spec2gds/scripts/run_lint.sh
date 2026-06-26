#!/usr/bin/env bash
set -euo pipefail

# usage: run_lint.sh <rtl-file> <log-file>
RTL_FILE="${1:-}"
LOG_FILE="${2:-lint.log}"

if [[ -z "$RTL_FILE" ]]; then
  echo "usage: run_lint.sh <rtl-file> <log-file>" >&2
  exit 1
fi

mkdir -p "$(dirname "$LOG_FILE")"

if command -v verilator >/dev/null 2>&1; then
  verilator --lint-only "$RTL_FILE" >"$LOG_FILE" 2>&1
elif command -v iverilog >/dev/null 2>&1; then
  iverilog -t null "$RTL_FILE" >"$LOG_FILE" 2>&1
else
  echo "No lint-capable tool found (need verilator or iverilog)" >"$LOG_FILE"
  exit 2
fi

echo "lint_ok" >>"$LOG_FILE"
