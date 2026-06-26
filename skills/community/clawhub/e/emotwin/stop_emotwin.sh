#!/bin/bash
# emoTwin Stop Script
# Stops emoPAD service and disables social cycles

echo "🌊 Stopping emoTwin..."
echo ""

# Step 1: Stop emoPAD service
if pgrep -f "emoPAD_service.py" > /dev/null; then
    echo "🛑 Stopping emoPAD service..."
    pkill -f "emoPAD_service.py"
    sleep 1
    
    if pgrep -f "emoPAD_service.py" > /dev/null; then
        echo "   ⚠️  Force killing..."
        pkill -9 -f "emoPAD_service.py"
    fi
    
    echo "✅ emoPAD service stopped"
else
    echo "✅ emoPAD service already stopped"
fi

# Step 2: Disable cron job
echo ""
echo "📝 Disabling emoTwin cron job..."

# Find and remove emoTwin cron jobs
CRON_JOBS=$(openclaw cron list 2>/dev/null | grep "emoTwin" | awk '{print $1}')

if [ -n "$CRON_JOBS" ]; then
    for job_id in $CRON_JOBS; do
        openclaw cron remove "$job_id" 2>/dev/null && echo "   ✅ Removed cron job: $job_id"
    done
    echo "✅ emoTwin cron jobs disabled"
else
    echo "✅ No active cron jobs found"
fi

# Step 3: Clean up state files
rm -f "$HOME/.emotwin/state.json" "$HOME/.emotwin/emotwin.pid" 2>/dev/null

# Read previous sync interval config (if exists)
SYNC_INTERVAL=$(cat "$HOME/.emotwin/sync_interval.txt" 2>/dev/null || echo "60")

echo ""
echo "✨ emoTwin has returned!"
echo ""
echo "Session summary:"
echo "   • emoPAD service: Stopped"
echo "   • Cron jobs: Disabled"
echo "   • Social cycles: Stopped"
echo "   • Last sync frequency: ${SYNC_INTERVAL}s"
echo "   • Moment cards saved to: ~/.emotwin/diary/"
echo ""
echo "To restart: say '带着情绪去 moltcn' or 'go to moltcn'"
echo ""
