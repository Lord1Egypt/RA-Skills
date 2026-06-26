#!/usr/bin/env bash
# press_key.sh - Press a key or key combination in the E2B Desktop sandbox
# Usage: press_key.sh KEY [KEY2 ...]
# Examples:
#   press_key.sh enter
#   press_key.sh space
#   press_key.sh ctrl c        (key combination)
#   press_key.sh ctrl shift t

set -e

if [[ $# -eq 0 ]]; then
  echo "Usage: press_key.sh KEY [KEY2 ...]" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Build Python list from args
KEYS_PY="["
for k in "$@"; do
  KEYS_PY+="\"$k\","
done
KEYS_PY="${KEYS_PY%,}]"

python3 - <<EOF
import os, sys
exec(open("$SCRIPT_DIR/_connect.py").read())

keys = $KEYS_PY
if len(keys) == 1:
    desktop.press(keys[0])
else:
    desktop.press(keys)
print(f"Pressed: {keys}")
EOF
