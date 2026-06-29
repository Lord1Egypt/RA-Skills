#!/bin/bash
# serve.sh — Start the Orchestration Dashboard
# Usage: bash dashboard/serve.sh [port] [--pm2]
# Default port: 8766
# Data from: $ORCHESTRATOR_DATA_DIR (default: ../orchestrator-data/ from skill root)
# Open: http://localhost:8766

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="${ORCHESTRATOR_DATA_DIR:-$(dirname "$(dirname "$SKILL_DIR")")/orchestrator-data}"
PORT="${1:-8766}"
USE_PM2=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --pm2) USE_PM2=true; shift ;;
        *) PORT="$1"; shift ;;
    esac
done

if $USE_PM2; then
    echo "=== PM2 Mode ==="
    echo "Use: bash scripts/pm2-setup.sh --start"
    echo ""
fi

echo "━━━ Orchestration Dashboard ━━━"
echo "Port: $PORT"
echo "Data: $DATA_DIR"
echo "Open: http://localhost:$PORT"
echo "Set ORCHESTRATOR_DATA_DIR to override data path"
echo ""

if $USE_PM2; then
    # PM2 mode - just show instructions
    echo "To start with PM2, run:"
    echo "  bash scripts/pm2-setup.sh --start"
else
    # Direct mode
    cd "$SCRIPT_DIR"
    ORCHESTRATOR_DATA_DIR="$DATA_DIR" DASHBOARD_PORT="$PORT" python3 server.py
fi