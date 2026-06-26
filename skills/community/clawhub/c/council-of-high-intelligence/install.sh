#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="${HOME}/.claude"

echo "Installing Council of High Intelligence..."

# Create directories
mkdir -p "${CLAUDE_DIR}/agents"
mkdir -p "${CLAUDE_DIR}/skills/council"

# Copy agents
cp "${SCRIPT_DIR}"/agents/council-*.md "${CLAUDE_DIR}/agents/"
echo "  Installed 8 council agents to ${CLAUDE_DIR}/agents/"

# Copy skill
cp "${SCRIPT_DIR}/SKILL.md" "${CLAUDE_DIR}/skills/council/SKILL.md"
echo "  Installed skill to ${CLAUDE_DIR}/skills/council/"

echo ""
echo "Done. Restart Claude Code and use /council to convene the council."
