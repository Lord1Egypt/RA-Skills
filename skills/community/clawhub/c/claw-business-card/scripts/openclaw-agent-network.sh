#!/bin/bash
# agent-network skill macOS/Linux wrapper
# 用法: ./openclaw-agent-network.sh <command> [args...]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="${WORKSPACE:-$HOME/.qclaw/workspace}"
PYTHON="${PYTHON:-python3}"

show_help() {
    echo "Usage: $0 <command> [args...]"
    echo ""
    echo "Commands:"
    echo "  init                 Initialize agent-network directory"
    echo "  identity             Show/edit agent identity card"
    echo " friends              Show friends list"
    echo "  add-friend <json>   Add a friend"
    echo "  show-ledger         Show token ledger"
    echo "  create-task         Create a new task"
    echo "  calculate-bill      Calculate bill"
    echo "  validate-bill       Validate bill"
    echo "  settle              Complete settlement"
}

case "$1" in
    init)
        "$PYTHON" "$SCRIPT_DIR/scripts/init.py" --workspace "$WORKSPACE"
        ;;
    identity)
        if [ -f "$WORKSPACE/agent-network/identity.json" ]; then
            cat "$WORKSPACE/agent-network/identity.json"
        else
            echo "[ERROR] identity.json not found. Run init first."
            exit 1
        fi
        ;;
    friends)
        if [ -f "$WORKSPACE/agent-network/friends.json" ]; then
            cat "$WORKSPACE/agent-network/friends.json"
        else
            echo "[ERROR] friends.json not found. Run init first."
            exit 1
        fi
        ;;
    show-ledger)
        shift
        "$PYTHON" "$SCRIPT_DIR/scripts/show_ledger.py" --workspace "$WORKSPACE" "$@"
        ;;
    calculate-bill)
        shift
        "$PYTHON" "$SCRIPT_DIR/scripts/calculate_bill.py" --workspace "$WORKSPACE" "$@"
        ;;
    validate-bill)
        shift
        "$PYTHON" "$SCRIPT_DIR/scripts/validate_bill.py" --workspace "$WORKSPACE" "$@"
        ;;
    settle)
        shift
        "$PYTHON" "$SCRIPT_DIR/scripts/settle.py" --workspace "$WORKSPACE" "$@"
        ;;
    create-task)
        shift
        "$PYTHON" "$SCRIPT_DIR/scripts/create_task.py" --workspace "$WORKSPACE" "$@"
        ;;
    *)
        show_help
        exit 1
        ;;
esac
