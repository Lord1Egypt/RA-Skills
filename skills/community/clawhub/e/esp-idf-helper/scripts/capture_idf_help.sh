#!/usr/bin/env bash
set -euo pipefail

# Capture idf.py help text into references/ so it can be searched quickly.
# Uses IDF_PATH to activate the environment if available.

OUT_REL="references/idf-py-help.txt"

ESPIDF_ROOT="${IDF_PATH:-}"

cd "$(dirname "$0")/.."  # skill root

if [[ -n "${IDF_PATH:-}" && -f "$ESPIDF_ROOT/export.sh" ]]; then
  bash -lc "set -euo pipefail; source \"$ESPIDF_ROOT/export.sh\" >/dev/null; idf.py --help" > "$OUT_REL"
elif command -v idf.py >/dev/null 2>&1; then
  idf.py --help > "$OUT_REL"
else
  echo "ERROR: idf.py not found. Either activate ESP-IDF in this shell, or set IDF_PATH to an ESP-IDF checkout (with export.sh)." >&2
  exit 1
fi

echo "Wrote: $(pwd)/$OUT_REL"
