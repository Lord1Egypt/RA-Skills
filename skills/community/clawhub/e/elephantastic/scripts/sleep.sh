#!/usr/bin/env bash
# sleep.sh — Session Close wrapper for clawvault sleep
# Usage: sleep.sh "<summary>"
# Enforces non-empty next steps before writing handoff.
#
# This script is part of elephantastic. Place it in your workspace scripts/ directory
# or call directly from the skill path.

set -euo pipefail

SUMMARY="${1:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Find task_manager.py (prefer local, fallback to elephantastic install)
TASK_MANAGER=""
if [[ -f "${SCRIPT_DIR}/task_manager.py" ]]; then
    TASK_MANAGER="${SCRIPT_DIR}/task_manager.py"
elif [[ -f "${HOME}/.openclaw/skills/agent-gtd/scripts/task_manager.py" ]]; then
    TASK_MANAGER="${HOME}/.openclaw/skills/elephantastic/scripts/task_manager.py"
else
    echo "❌ task_manager.py not found"
    exit 1
fi

if [[ -z "$SUMMARY" ]]; then
    echo "❌ Usage: sleep.sh '<session summary>'"
    echo "   Summary must describe what was done AND what's next."
    exit 1
fi

# Use task_manager.py sleep command
python3 "$TASK_MANAGER" sleep "$SUMMARY"

echo ""
echo "✅ Handoff complete. Safe to /new or /reset."
