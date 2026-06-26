#!/bin/bash

# Fullrun - Main Entry Point

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

case "${1:-help}" in
    start)
        "$SCRIPT_DIR/cron-manager.sh" start
        ;;
    stop)
        "$SCRIPT_DIR/cron-manager.sh" stop
        ;;
    run)
        "$SCRIPT_DIR/fullrun.sh" run
        ;;
    status)
        echo "=== Task Execution Status ==="
        "$SCRIPT_DIR/fullrun.sh" check
        echo ""
        echo "=== Monitor Status ==="
        "$SCRIPT_DIR/cron-manager.sh" status
        ;;
    help|*)
        echo "Fullrun - Task Executor"
        echo ""
        echo "Usage: $0 {start|stop|run|status}"
        echo ""
        echo "Commands:"
        echo "  start  - Start scheduled monitoring (checks every minute)"
        echo "  stop   - Stop scheduled monitoring"
        echo "  run    - Execute tasks once"
        echo "  status - Check current status"
        ;;
esac
