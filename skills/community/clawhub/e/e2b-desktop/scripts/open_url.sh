#!/usr/bin/env bash
# open_url.sh - Open a URL or file in the default application inside the sandbox
# Usage: open_url.sh URL_OR_PATH

set -e

TARGET="${1:?Usage: open_url.sh URL_OR_PATH}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python3 - <<EOF
import os, sys
exec(open("$SCRIPT_DIR/_connect.py").read())

desktop.open("$TARGET")
print(f"Opened: $TARGET")
EOF
