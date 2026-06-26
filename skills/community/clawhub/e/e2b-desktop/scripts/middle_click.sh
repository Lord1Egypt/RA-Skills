#!/usr/bin/env bash
# middle_click.sh - Middle click at coordinates in the E2B Desktop sandbox
# Usage: middle_click.sh X Y

set -e

X="${1:?Usage: middle_click.sh X Y}"
Y="${2:?Usage: middle_click.sh X Y}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python3 - <<EOF
import os, sys
exec(open("$SCRIPT_DIR/_connect.py").read())

desktop.middle_click(int("$X"), int("$Y"))
print(f"Middle clicked at ($X, $Y)")
EOF
