#!/bin/bash

# Squad Initialization Script
# This script creates isolated OpenClaw agents for the "Calling Agent Squad" skill.

BASE_DIR="/Users/george/.openclaw/workspace/skills/calling-agent-squad"
AGENTS=("squad-manager" "architect" "researcher" "copywriter" "brand-reviewer" "coder" "code-reviewer" "observer")

echo "🦞 Initializing Agent Squad..."

for agent in "${AGENTS[@]}"; do
    echo "Creating agent: $agent"
    openclaw agents add "$agent" \
        --workspace "$BASE_DIR/agents/$agent" \
        --agent-dir "/Users/george/.openclaw/agents/$agent/agent" \
        --non-interactive
done

echo "✅ Squad initialized! You can now call the manager via CLI:"
echo "openclaw agent --agent squad-manager --message \"Your mission details here\""
