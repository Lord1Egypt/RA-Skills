#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   scripts/check_capability.sh <python-bin> <module1> [module2 ...]
# Example:
#   scripts/check_capability.sh ~/.openclaw/workspace/.venv-img/bin/python cv2 PIL numpy

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <python-bin> <module1> [module2 ...]" >&2
  exit 2
fi

PY_BIN="$1"
shift

if [[ ! -x "$PY_BIN" ]]; then
  echo "ERROR: python interpreter not executable: $PY_BIN" >&2
  exit 1
fi

"$PY_BIN" - "$@" <<'PY'
import importlib.util
import sys

mods = sys.argv[1:]
failed = []

print(f"Python: {sys.executable}")
for m in mods:
    ok = importlib.util.find_spec(m) is not None
    print(f"{m}: {'OK' if ok else 'MISSING'}")
    if not ok:
        failed.append(m)

if failed:
    print("Missing modules:", ", ".join(failed))
    sys.exit(1)

print("All requested modules are available.")
PY
