#!/bin/bash
# cc-changelog-monitor setup.sh - One-time setup

set -e

echo "🔧 Setting up cc-changelog-monitor..."

# Create directories
mkdir -p ~/clawd/projects/cc-changelog
mkdir -p ~/clawd/skills/cc-changelog-monitor/scripts

# Create version file if not exists
if [ ! -f ~/.cc-changelog-version ]; then
    echo "0.0.0" > ~/.cc-changelog-version
    echo "✅ Created version tracking file"
fi

# Make scripts executable
chmod +x ~/clawd/skills/cc-changelog-monitor/scripts/monitor.sh

# Run once to initialize
echo ""
echo "🚀 Running initial check..."
bash ~/clawd/skills/cc-changelog-monitor/scripts/monitor.sh

echo ""
echo "✅ Setup complete!"
echo ""
echo "To add to OpenClaw cron:"
echo "1. Open OpenClaw dashboard"
echo "2. Add cron job with schedule: every 2 hours"
echo "3. Payload: bash ~/clawd/skills/cc-changelog-monitor/scripts/monitor.sh"
echo ""
echo "Or use the cron-payload.md file for the exact OpenClaw cron configuration."
