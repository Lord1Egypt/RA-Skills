#!/usr/bin/env bash
# todo.sh - execution queue for agent-todo

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

exec python3 "${SCRIPT_DIR}/scripts/agent_todo.py" "$@"
