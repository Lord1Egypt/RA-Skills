#!/usr/bin/env bash
set -u

# Shell wrapper for the Python regression runner.
# Usage:
#   bash test_regression.sh
#   bash test_regression.sh --keep-exports
# This suite does not run install/update/uninstall flows.

ROOT="$(cd "$(dirname "$0")" && pwd)"
PYTHON="$(command -v python3 || command -v python)"

if [ -z "$PYTHON" ]; then
  echo "找不到 python3/python"
  exit 127
fi

PYTHONIOENCODING=utf-8 "$PYTHON" "$ROOT/test_regression.py" "$@"
