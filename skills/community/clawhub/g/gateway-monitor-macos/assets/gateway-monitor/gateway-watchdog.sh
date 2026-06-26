#!/bin/zsh
set -euo pipefail

NODE_BIN="/opt/homebrew/opt/node/bin/node"
OPENCLAW_BIN="/opt/homebrew/bin/openclaw"
OPENCLAW_JS="/opt/homebrew/lib/node_modules/openclaw/dist/index.js"
GATEWAY_LABEL="ai.openclaw.gateway"
UID_NUM="$(id -u)"
LOG_FILE="$HOME/.openclaw/logs/gateway-watchdog.log"
ERR_FILE="$HOME/.openclaw/logs/gateway-watchdog.err.log"

mkdir -p "$HOME/.openclaw/logs"

status_json=""
if ! status_json="$($NODE_BIN $OPENCLAW_JS gateway status --json 2>>"$ERR_FILE")"; then
  echo "[$(date '+%F %T')] status check failed -> reload plist" >> "$LOG_FILE"
  launchctl unload "$HOME/Library/LaunchAgents/${GATEWAY_LABEL}.plist" 2>/dev/null || true
  launchctl load "$HOME/Library/LaunchAgents/${GATEWAY_LABEL}.plist" >> "$LOG_FILE" 2>>"$ERR_FILE"
  exit 0
fi

runtime_status="$(printf '%s' "$status_json" | python3 -c 'import sys,json
j=json.load(sys.stdin)
print((j.get("service",{}).get("runtime",{}).get("status") or "unknown"))' 2>>"$ERR_FILE" || echo unknown)"
loaded="$(printf '%s' "$status_json" | python3 -c 'import sys,json
j=json.load(sys.stdin)
print("true" if j.get("service",{}).get("loaded") else "false")' 2>>"$ERR_FILE" || echo false)"

if [[ "$runtime_status" != "running" || "$loaded" != "true" ]]; then
  echo "[$(date '+%F %T')] not healthy (loaded=$loaded, status=$runtime_status) -> reload plist" >> "$LOG_FILE"
  launchctl unload "$HOME/Library/LaunchAgents/${GATEWAY_LABEL}.plist" 2>/dev/null || true
  launchctl load "$HOME/Library/LaunchAgents/${GATEWAY_LABEL}.plist" >> "$LOG_FILE" 2>>"$ERR_FILE"
fi
