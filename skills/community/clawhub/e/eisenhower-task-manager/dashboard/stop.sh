#!/bin/bash
# Eisenhower Task Dashboard Stop Script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/dashboard.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "[Dashboard] Stopping server (PID: $PID)..."
        kill "$PID"
        sleep 2
        if kill -0 "$PID" 2>/dev/null; then
            echo "[Dashboard] Force killing..."
            kill -9 "$PID"
        fi
        rm -f "$PID_FILE"
        echo "[Dashboard] Stopped"
    else
        echo "[Dashboard] Not running (stale PID file removed)"
        rm -f "$PID_FILE"
    fi
else
    echo "[Dashboard] Not running (no PID file found)"
fi
