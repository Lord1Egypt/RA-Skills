#!/bin/bash
# OpenClaw Gateway Watchdog — keeps the gateway alive
# Runs every 2 minutes via cron

GATEWAY_PORT=18789
LOG_FILE="/home/openclaw/.openclaw/workspace/logs/watchdog.log"
mkdir -p "$(dirname "$LOG_FILE")"

log() { echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" >> "$LOG_FILE"; }

# Check if gateway is responding
if curl -sf -m 5 "http://127.0.0.1:${GATEWAY_PORT}/health" > /dev/null 2>&1; then
    log "OK: gateway healthy on :${GATEWAY_PORT}"
    exit 0
fi

log "WARN: gateway not responding on :${GATEWAY_PORT}, attempting restart"

# Kill any stale gateway process
pkill -f "openclaw.*gateway.*${GATEWAY_PORT}" 2>/dev/null
sleep 2

# Restart
cd /home/openclaw/.openclaw
nohup /usr/bin/node /usr/lib/node_modules/openclaw/dist/index.js gateway --port "${GATEWAY_PORT}" > /home/openclaw/.openclaw/workspace/logs/gateway.log 2>&1 &

# Wait and verify
sleep 10
if curl -sf -m 5 "http://127.0.0.1:${GATEWAY_PORT}/health" > /dev/null 2>&1; then
    log "OK: gateway restarted successfully"
else
    log "FAIL: gateway restart failed!"
fi
