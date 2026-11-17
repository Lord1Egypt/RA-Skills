#!/bin/bash
# qto-project/v1 P2 汇总层入口（只汇总量算登记，不计算量）
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-${PYTHON:-python3}}"
"$PYTHON_BIN" "$SKILL_DIR/scripts/qto_p2_summarize.py" "$@"
