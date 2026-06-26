#!/usr/bin/env bash
# heartbeat.sh - Hook: pick the next executable task during heartbeat
#
# Integration:
#   cd /path/to/agent-todo && ./script.sh run-pending --claim
#
# If there is no pending task, the command prints HEARTBEAT_OK.
# If a task is found, it prints an EXECUTE_NOW brief for the agent to act on.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

exec "${SKILL_DIR}/script.sh" run-pending --claim
