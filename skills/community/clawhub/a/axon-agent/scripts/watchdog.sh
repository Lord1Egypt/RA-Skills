#!/bin/bash
# Axon agent-daemon watchdog — run via cron: */5 * * * * /opt/axon/watchdog.sh
# Usage: Set AXON_DIR, PRIVATE_KEY, and RPC below, then: crontab -e → add line above

AXON_DIR="${AXON_DIR:-/opt/axon}"
DAEMON="$AXON_DIR/tools/agent-daemon/agent-daemon"
PK_FILE="$AXON_DIR/private_key.txt"
RPC="${AXON_RPC:-https://mainnet-rpc.axonchain.ai/}"
LOG="$AXON_DIR/watchdog.log"

if ! pgrep -f "agent-daemon" > /dev/null 2>&1; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') [RESTART] daemon not running" >> "$LOG"
    nohup "$DAEMON" \
        --rpc "$RPC" \
        --private-key-file "$PK_FILE" \
        --heartbeat-interval 720 \
        --log-level info \
        >> "$AXON_DIR/daemon.log" 2>&1 &
    echo "$(date '+%Y-%m-%d %H:%M:%S') [RESTART] new PID: $!" >> "$LOG"
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') [OK] daemon running" >> "$LOG"
fi
