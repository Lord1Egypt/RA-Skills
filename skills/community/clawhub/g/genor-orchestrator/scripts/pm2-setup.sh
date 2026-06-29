#!/bin/bash
# pm2-setup.sh — Configure PM2 for the Orchestration Dashboard
# Usage: bash pm2-setup.sh [--start] [--stop] [--status] [--restart]
#
# This script sets up PM2 to keep the dashboard running as a background process.
# PM2 will auto-restart the dashboard if it crashes.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$SKILL_DIR/ecosystem.config.js"

ACTION="${1:---start}"

case "$ACTION" in
    --start)
        echo "Starting Orchestration Dashboard via PM2..."
        if [ ! -f "$CONFIG_FILE" ]; then
            echo "Error: ecosystem.config.js not found at $CONFIG_FILE"
            exit 1
        fi
        pm2 start "$CONFIG_FILE"
        echo ""
        echo "Dashboard starting..."
        echo "View status: pm2 status"
        echo "View logs: pm2 logs orchestration-dashboard"
        ;;
    --stop)
        echo "Stopping Orchestration Dashboard..."
        pm2 delete orchestration-dashboard 2>/dev/null || echo "Not running"
        ;;
    --status)
        pm2 list | grep -E "orchestration-dashboard|pm2" || true
        ;;
    --restart)
        pm2 restart orchestration-dashboard 2>/dev/null || $0 --start
        ;;
    *)
        echo "Usage: $0 [--start|--stop|--status|--restart]"
        echo ""
        echo "Commands:"
        echo "  --start   Start the dashboard via PM2"
        echo "  --stop    Stop the dashboard"
        echo "  --status  Show PM2 status"
        echo "  --restart Restart the dashboard"
        echo ""
        echo "Dashboard will be available at: http://localhost:8766"
        exit 1
        ;;
esac