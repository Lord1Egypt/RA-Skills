#!/bin/bash
# install_heartbeat_cron.sh - Install heartbeat as recurring cron job

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HEARTBEAT_SCRIPT="$SCRIPT_DIR/heartbeat_check.sh"
CRON_INTERVAL="${1:-*/30}"  # Default: every 30 minutes

echo "📋 Installing heartbeat cron job..."
echo "   Interval: $CRON_INTERVAL * * * *"
echo "   Script: $HEARTBEAT_SCRIPT"
echo ""

# Create cron job
CRON_JOB="$CRON_INTERVAL * * * * bash $HEARTBEAT_SCRIPT > /tmp/heartbeat.log 2>&1"

# Check if already exists
if crontab -l 2>/dev/null | grep -q "heartbeat_check.sh"; then
  echo "⚠️  Cron job already exists!"
  echo ""
  echo "Current crontab:"
  crontab -l | grep heartbeat
  echo ""
  read -p "Remove and reinstall? (y/n) " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    crontab -l | grep -v "heartbeat_check.sh" | crontab -
    echo "✅ Removed old job"
  else
    exit 0
  fi
fi

# Install new job
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "✅ Installed cron job!"
echo ""
echo "📊 To view:"
echo "   crontab -l"
echo ""
echo "📝 Logs saved to:"
echo "   /tmp/heartbeat.log"
echo ""
echo "🛑 To remove:"
echo "   crontab -e  # then delete the heartbeat line"
echo ""
