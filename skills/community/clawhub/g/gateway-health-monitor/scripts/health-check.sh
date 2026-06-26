#!/bin/bash
# health-check.sh — Quick gateway health check (exit 0 = ok, exit 1 = issue)
# Suitable for cron or heartbeat integration.

LABEL="ai.openclaw.gateway"

# Check if service is running
PRINT_OUT=$(launchctl print "gui/$(id -u)/$LABEL" 2>&1) || exit 1
PID=$(echo "$PRINT_OUT" | grep '	pid' | awk '{print $3}')

if [ -z "$PID" ] || ! kill -0 "$PID" 2>/dev/null; then
    echo "ALERT: Gateway not running"
    exit 1
fi

# Check if classified as inefficient
if echo "$PRINT_OUT" | grep -q "immediate reason = inefficient"; then
    echo "WARN: Gateway classified as inefficient by launchd"
    exit 1
fi

# Check restart count today
TODAY=$(date +%Y-%m-%d)
LOG="$HOME/.openclaw/logs/gateway.log"
if [ -f "$LOG" ]; then
    RESTARTS=$(grep "listening on ws:" "$LOG" | grep "$TODAY" | wc -l | xargs)
    if [ "$RESTARTS" -gt 10 ]; then
        echo "WARN: $RESTARTS restarts today — possible restart loop"
        exit 1
    fi
fi

UPTIME=$(ps -o etime= -p "$PID" 2>/dev/null | xargs)
echo "OK: Gateway running (PID $PID, uptime: $UPTIME)"
exit 0
