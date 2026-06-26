#!/usr/bin/env bash
set -euo pipefail

# usage: run_synth.sh <rtl-file> <top-module> <work-dir>
RTL_FILE="${1:-}"
TOP="${2:-}"
WORK_DIR="${3:-synth}"

if [[ -z "$RTL_FILE" || -z "$TOP" ]]; then
  echo "usage: run_synth.sh <rtl-file> <top-module> <work-dir>" >&2
  exit 1
fi

mkdir -p "$WORK_DIR"
cat > "$WORK_DIR/synth.ys" <<EOF
read_verilog $RTL_FILE
hierarchy -check -top $TOP
synth -top $TOP
stat
write_verilog $WORK_DIR/synth_output.v
EOF

yosys -s "$WORK_DIR/synth.ys" >"$WORK_DIR/synth.log" 2>&1
