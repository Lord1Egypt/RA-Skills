#!/usr/bin/env bash
# Preserve the regression entry point while keeping tests inspectable as Python source.
set -euo pipefail
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
export PYTHONDONTWRITEBYTECODE=1
exec "${CODESIFT_PYTHON:-python3}" "$SCRIPT_DIR/smoke_test.py" "$@"
