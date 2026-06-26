#!/usr/bin/env bash
# start_sandbox.sh - Create a new E2B Desktop sandbox
# Usage: start_sandbox.sh [--resolution WxH] [--timeout SECS] [--stream]
#
# Outputs sandbox ID and optionally stream URL.
# Saves sandbox ID to ~/.e2b_state for use by other scripts.

set -e

RESOLUTION="1024x768"
TIMEOUT="300"
STREAM=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --resolution) RESOLUTION="$2"; shift 2 ;;
    --timeout)    TIMEOUT="$2"; shift 2 ;;
    --stream)     STREAM=true; shift ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

W="${RESOLUTION%x*}"
H="${RESOLUTION#*x}"

python3 - <<EOF
import os, json, sys
from e2b_desktop import Sandbox

api_key = os.environ.get("E2B_API_KEY")
if not api_key:
    print("ERROR: E2B_API_KEY not set", file=sys.stderr)
    sys.exit(1)

desktop = Sandbox.create(
    resolution=(int("$W"), int("$H")),
    timeout=int("$TIMEOUT"),
)

stream_url = None
if "$STREAM" == "true":
    desktop.stream.start()
    stream_url = desktop.stream.get_url()

state = {"sandbox_id": desktop.sandbox_id}
state_path = os.path.expanduser("~/.e2b_state")
with open(state_path, "w") as f:
    json.dump(state, f)

print(f"SANDBOX_ID={desktop.sandbox_id}")
if stream_url:
    print(f"STREAM_URL={stream_url}")
print(f"State saved to {state_path}")
EOF
