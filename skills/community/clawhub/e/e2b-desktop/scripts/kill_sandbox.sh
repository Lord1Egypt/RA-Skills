#!/usr/bin/env bash
# kill_sandbox.sh - Kill an E2B Desktop sandbox
# Usage: kill_sandbox.sh [SANDBOX_ID]
# If no sandbox ID given, reads from ~/.e2b_state or E2B_SANDBOX_ID env var.

set -e

if [[ -n "$1" ]]; then
  export E2B_SANDBOX_ID="$1"
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python3 - <<EOF
import os, sys
exec(open("$SCRIPT_DIR/_connect.py").read())

desktop.kill()
print(f"Sandbox {sandbox_id} killed.")

import json
state_path = os.path.expanduser("~/.e2b_state")
if os.path.exists(state_path):
    os.remove(state_path)
    print("State file removed.")
EOF
