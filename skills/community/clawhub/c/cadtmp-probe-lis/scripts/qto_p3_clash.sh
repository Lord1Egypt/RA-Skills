#!/bin/bash
# qto-project/v1 P3 跨专业交叉核对层入口（只读汇总，不计算量）
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-${PYTHON:-python3}}"
"$PYTHON_BIN" "$SKILL_DIR/scripts/qto_p3_clash.py" "$@"
