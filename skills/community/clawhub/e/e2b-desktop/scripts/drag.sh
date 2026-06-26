#!/usr/bin/env bash
# drag.sh - Drag mouse from one position to another in the E2B Desktop sandbox
# Usage: drag.sh X1 Y1 X2 Y2

set -e

X1="${1:?Usage: drag.sh X1 Y1 X2 Y2}"
Y1="${2:?Usage: drag.sh X1 Y1 X2 Y2}"
X2="${3:?Usage: drag.sh X1 Y1 X2 Y2}"
Y2="${4:?Usage: drag.sh X1 Y1 X2 Y2}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python3 - <<EOF
import os, sys
exec(open("$SCRIPT_DIR/_connect.py").read())

desktop.drag((int("$X1"), int("$Y1")), (int("$X2"), int("$Y2")))
print(f"Dragged from ($X1, $Y1) to ($X2, $Y2)")
EOF
