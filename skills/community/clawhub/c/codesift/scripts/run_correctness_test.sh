#!/usr/bin/env bash
# Preserve the public command entry point and share execution, timeout, and evidence handling.
set -euo pipefail
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
export PYTHONDONTWRITEBYTECODE=1
exec "${CODESIFT_PYTHON:-python3}" "$SCRIPT_DIR/lib/check_runner.py" correctness "$@"
