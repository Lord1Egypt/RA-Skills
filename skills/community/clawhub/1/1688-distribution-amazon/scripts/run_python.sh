#!/usr/bin/env bash
set -euo pipefail

if [[ -n "${PYTHON_BIN:-}" && -x "${PYTHON_BIN}" ]]; then
  exec "${PYTHON_BIN}" "$@"
fi

newton_python="${HOME}/Library/Application Support/Newton/runtimes/v3/python/bin/python3"
if [[ -x "${newton_python}" ]]; then
  exec "${newton_python}" "$@"
fi

if command -v python3 >/dev/null 2>&1; then
  exec python3 "$@"
fi

echo "[ERROR] python3 not found; set PYTHON_BIN to a Python 3 executable" >&2
exit 127
