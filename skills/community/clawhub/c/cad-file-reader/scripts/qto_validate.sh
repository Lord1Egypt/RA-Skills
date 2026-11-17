#!/bin/sh
set -eu
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHON_BIN=""
for candidate in \
  "$HOME/.cache/codex-runtimes/"*/dependencies/python/bin/python3 \
  "$(command -v python3 || true)"
do
  if [ -n "${candidate}" ] && [ -x "${candidate}" ]; then
    PYTHON_BIN="${candidate}"
    break
  fi
done
if [ -z "${PYTHON_BIN}" ]; then
  echo "❌ Python 3 not found;" >&2
  exit 1
fi
exec "${PYTHON_BIN}" "$SCRIPT_DIR/qto_validate.py" "$@"
