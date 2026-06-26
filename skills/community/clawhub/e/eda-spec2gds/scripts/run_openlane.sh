#!/usr/bin/env bash
set -euo pipefail

# usage: run_openlane.sh <project-dir> <config-json>
PROJECT_DIR="${1:-}"
CONFIG_JSON="${2:-}"

if [[ -z "$PROJECT_DIR" || -z "$CONFIG_JSON" ]]; then
  echo "usage: run_openlane.sh <project-dir> <config-json>" >&2
  exit 1
fi

if command -v openlane >/dev/null 2>&1; then
  OPENLANE_CMD="$(command -v openlane)"
elif [[ -x "$HOME/.venvs/openlane/bin/openlane" ]]; then
  OPENLANE_CMD="$HOME/.venvs/openlane/bin/openlane"
else
  echo "openlane not found in PATH or ~/.venvs/openlane/bin/openlane" >&2
  exit 1
fi

PROJECT_DIR="$(cd "$PROJECT_DIR" && pwd)"
CONFIG_PATH="$(cd "$PROJECT_DIR" && python3 - <<'PY' "$CONFIG_JSON"
import os, sys
print(os.path.abspath(sys.argv[1]))
PY
)"
cd "$PROJECT_DIR"
"$OPENLANE_CMD" --docker-no-tty --dockerized "$CONFIG_PATH"
