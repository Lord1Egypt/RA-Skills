#!/usr/bin/env bash
# wait.sh - Wait for a given number of milliseconds inside the E2B Desktop sandbox
# Usage: wait.sh MILLISECONDS

set -e

MS="${1:?Usage: wait.sh MILLISECONDS}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python3 - <<EOF
import os, sys
exec(open("$SCRIPT_DIR/_connect.py").read())

desktop.wait(int("$MS"))
print(f"Waited {$MS}ms")
EOF
