#!/bin/bash
# Creem Agent — ClawHub Install Script
# This runs automatically when someone installs the skill from ClawHub

set -e  # exit on any error

echo "🍦 Installing Creem Agent (Alfred)..."

# 1. Make the heartbeat script executable
chmod +x scripts/heartbeat.py

# 2. Ensure the state directory exists (for heartbeat-state.json)
mkdir -p ~/.creem

# 3. Optional: friendly message
echo "✅ Creem Agent installed successfully!"
echo ""
echo "Next steps:"
echo "   1. Make sure you have set CREEM_API_KEY in ~/.openclaw/.env"
echo "   2. Restart OpenClaw: openclaw gateway restart"
echo "   3. Talk to Alfred: 'What’s my current MRR?'"
echo ""
echo "Alfred is now your full-time Creem store operations worker."
