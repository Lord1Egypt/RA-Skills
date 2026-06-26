#!/bin/bash
# Fast Claude Code - Main entry point
# Usage: fast-claude-code.sh <mode> [options]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

show_usage() {
    echo "Fast Claude Code - Callback Runtime"
    echo ""
    echo "Usage: fast-claude-code.sh <mode> [options]"
    echo ""
    echo "Modes:"
    echo "  single       Run a single task with callback"
    echo "  interactive  Start an interactive session"
    echo "  team         Start a team session"
    echo "  send-task    Send a task to an interactive session (with monitoring)"
    echo ""
    echo "Options:"
    echo "  --task TEXT           Task description"
    echo "  --project PATH        Project directory (single/interactive/team)"
    echo "  --session NAME        Session label (send-task mode)"
    echo "  --template NAME       Team template (team mode)"
    echo "  --callback TYPE       Callback backend: openclaw|webhook|ntfy (default: openclaw)"
    echo "  --permission-mode     Permission mode: plan|auto (default: auto)"
    echo "  --label NAME          Session label (interactive mode)"
    echo "  --timeout SECS        Task timeout in seconds (send-task mode, default: 600)"
    echo "  --session-key KEY     OpenClaw session key for callback routing (required)"
    echo "  --help                Show this help"
    echo ""
    echo "Examples:"
    echo "  # Single task"
    echo "  bin/fast-claude-code.sh single --task 'Refactor auth module' --project ~/project --session-key agent:main:main"
    echo ""
    echo "  # Start interactive session"
    echo "  bin/fast-claude-code.sh interactive --project ~/project --task 'List files'"
    echo ""
    echo "  # Send tasks to interactive session (each with monitoring)"
    echo "  bin/fast-claude-code.sh send-task --session mysession --task 'Analyze this file'"
    echo "  bin/fast-claude-code.sh send-task --session mysession --task 'Add unit tests'"
    echo ""
    echo "  # Team mode"
    echo "  bin/fast-claude-code.sh team --project ~/project --template parallel-review --session-key agent:main:main"
    echo ""
    echo "To use safer plan mode:"
    echo "  bin/fast-claude-code.sh single --task 'Refactor auth module' --project ~/project --permission-mode plan"
}

log_info() {
    echo -e "${BLUE}ℹ${NC} $*"
}

log_success() {
    echo -e "${GREEN}✅${NC} $*"
}

log_error() {
    echo -e "${RED}❌${NC} $*"
}

# Parse mode
MODE="${1:-}"
shift || true

case "$MODE" in
    single)
        exec "$BASE_DIR/modes/single.sh" "$@"
        ;;
    interactive)
        exec "$BASE_DIR/modes/interactive.sh" "$@"
        ;;
    team)
        exec "$BASE_DIR/modes/team.sh" "$@"
        ;;
    send-task)
        exec "$BASE_DIR/modes/send-task.sh" "$@"
        ;;
    -h|--help|help)
        show_usage
        exit 0
        ;;
    "")
        show_usage
        exit 1
        ;;
    *)
        log_error "Unknown mode: $MODE"
        show_usage
        exit 1
        ;;
esac
