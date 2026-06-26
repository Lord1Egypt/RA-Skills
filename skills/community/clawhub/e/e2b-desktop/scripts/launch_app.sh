#!/usr/bin/env bash
# launch_app.sh - Launch an application in the E2B Desktop sandbox
# Usage: launch_app.sh APP_NAME
# Common apps: google-chrome, firefox, vscode, gedit, nautilus

set -e

APP="${1:?Usage: launch_app.sh APP_NAME}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python3 - <<EOF
import os, sys
exec(open("$SCRIPT_DIR/_connect.py").read())

desktop.launch("$APP")
print(f"Launched: $APP")
EOF
