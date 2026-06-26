#!/usr/bin/env bash
# click.sh - Left click at coordinates in the E2B Desktop sandbox
# Usage: click.sh X Y

set -e

X="${1:?Usage: click.sh X Y}"
Y="${2:?Usage: click.sh X Y}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python3 - <<EOF
import os, sys
exec(open("$SCRIPT_DIR/_connect.py").read())

desktop.left_click(int("$X"), int("$Y"))
print(f"Left clicked at ($X, $Y)")
EOF
