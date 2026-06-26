#!/usr/bin/env bash
# script.sh - CLI entry point for agent-todo skill

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

exec "${SCRIPT_DIR}/todo.sh" "$@"
