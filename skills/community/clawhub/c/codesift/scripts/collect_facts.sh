#!/usr/bin/env bash
# Preserve the public command entry point and delegate shared parsing and reporting to Python.
set -euo pipefail
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
export PYTHONDONTWRITEBYTECODE=1
exec "${CODESIFT_PYTHON:-python3}" "$SCRIPT_DIR/lib/source_checks.py" facts "$@"
