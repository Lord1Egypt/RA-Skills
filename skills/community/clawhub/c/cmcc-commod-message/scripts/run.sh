#!/bin/sh
set -eu

if [ -n "${CMCC_NEWMSG_HOME:-}" ]; then
  STATE_DIR="$CMCC_NEWMSG_HOME"
elif [ -n "${HERMES_HOME:-}" ]; then
  STATE_DIR="$HERMES_HOME/cmcc-newmsg"
else
  STATE_DIR="$HOME/.cmcc-newmsg"
fi

PY="$STATE_DIR/venv/bin/python"
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
if [ ! -x "$PY" ]; then
  PY="${PYTHON_BIN:-python3}"
fi
exec "$PY" "$SCRIPT_DIR/cmcc_newmsg.py" "$@"
