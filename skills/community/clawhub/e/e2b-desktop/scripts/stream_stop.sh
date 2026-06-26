#!/usr/bin/env bash
# stream_stop.sh - Stop the VNC stream of an E2B Desktop sandbox
# Usage: stream_stop.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python3 - <<EOF
import os, sys
exec(open("$SCRIPT_DIR/_connect.py").read())

desktop.stream.stop()
print("Stream stopped.")
EOF
