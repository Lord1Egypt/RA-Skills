#!/bin/bash
# AgentLoop Skill Setup for OpenClaw

echo ""
echo "  AgentLoop — OpenClaw Skill Setup"
echo "  ================================="
echo ""
echo "  This skill requires AGENTLOOP_API_KEY to be set in your environment."
echo "  Get your key at: https://agentloop.life/dashboard/api-keys"
echo ""
echo "  Add this line to your shell profile (~/.bashrc, ~/.zshrc, etc.):"
echo ""
echo "    export AGENTLOOP_API_KEY=al_live_your_key_here"
echo ""
echo "  Or set it securely in your system keychain / secret manager."
echo ""
echo "  NOTE: Do not paste your key here. Set it in your environment before"
echo "  running OpenClaw. This script does not store or transmit your key."
echo ""

if [ -n "$AGENTLOOP_API_KEY" ]; then
  echo "  AGENTLOOP_API_KEY is already set. Testing connection..."
  node "$(dirname "$0")/agentloop-check.js" "connection test" "test response" 2>/dev/null \
    | grep -q "shouldMention" \
    && echo "  Connected successfully to agentloop.life!" \
    || echo "  Could not connect — check your API key."
else
  echo "  AGENTLOOP_API_KEY is not set. Set it in your environment and re-run this script to test."
fi

echo ""
