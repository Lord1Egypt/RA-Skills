#!/usr/bin/env bash
# list_windows.sh - List windows of an application in the E2B Desktop sandbox
# Usage: list_windows.sh [APP_NAME]
# Without APP_NAME: prints current active window ID and title

set -e

APP="${1:-}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python3 - <<EOF
import os, sys
exec(open("$SCRIPT_DIR/_connect.py").read())

app = "$APP"
if app:
    window_ids = desktop.get_application_windows(app)
    for wid in window_ids:
        title = desktop.get_window_title(wid)
        print(f"  window_id={wid}  title={title!r}")
    if not window_ids:
        print(f"No windows found for: {app}")
else:
    wid = desktop.get_current_window_id()
    title = desktop.get_window_title(wid)
    print(f"ACTIVE_WINDOW_ID={wid}")
    print(f"ACTIVE_WINDOW_TITLE={title!r}")
EOF
