#!/usr/bin/env bash
# stream_start.sh - Start VNC stream for the E2B Desktop sandbox
# Usage: stream_start.sh [--auth]
# --auth: Enable password-protected stream (prints auth key + URL)

set -e

AUTH=false
while [[ $# -gt 0 ]]; do
  case "$1" in
    --auth) AUTH=true; shift ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python3 - <<EOF
import os, sys
exec(open("$SCRIPT_DIR/_connect.py").read())

require_auth = "$AUTH" == "true"
desktop.stream.start(require_auth=require_auth)

if require_auth:
    auth_key = desktop.stream.get_auth_key()
    url = desktop.stream.get_url(auth_key=auth_key)
    print(f"AUTH_KEY={auth_key}")
else:
    url = desktop.stream.get_url()

print(f"STREAM_URL={url}")
EOF
