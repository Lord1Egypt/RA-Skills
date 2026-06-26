#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
SKILL_DIR="$SCRIPT_DIR"

if [[ -n "${PYTHON_BIN:-}" ]]; then
  PYTHON_CMD="$PYTHON_BIN"
elif [[ -x "$ROOT_DIR/.venv/bin/python" ]]; then
  PYTHON_CMD="$ROOT_DIR/.venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD="$(command -v python3)"
else
  echo "Python interpreter not found. Set PYTHON_BIN or create ../.venv." >&2
  exit 1
fi

if [[ ! -x "$PYTHON_CMD" ]]; then
  echo "Python interpreter is not executable: $PYTHON_CMD" >&2
  exit 1
fi

cd "$SKILL_DIR"
exec "$PYTHON_CMD" -m amath_skill
