#!/bin/zsh
# EvoMaster: Redis Checkpoint - Every 5 minutes
# Reports to: #evomaster-redis-checkpoint

LOGFILE="$HOME/.openclaw/logs/evomaster-$(date +%Y-%m-%d).log"
SLACK_CHANNEL="evomaster-redis-checkpoint"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] === Redis Memory Checkpoint ===" >> "$LOGFILE"

# Run Python checkpoint
python3 "$HOME/.openclaw/scripts/redis-memory-bridge.py" >> "$LOGFILE" 2>&1
CHECKPOINT_STATUS=$?

if [ $CHECKPOINT_STATUS -eq 0 ]; then
    STATUS="✅ Redis checkpoint successful"
else
    STATUS="❌ Redis checkpoint failed"
fi

# Send Slack notification (only every hour to avoid spam)
MINUTE=$(date +%M)
if [ "$MINUTE" = "00" ]; then
    bash "$HOME/.openclaw/scripts/slack-notify.sh" "$SLACK_CHANNEL" "🔄 **EvoMaster Redis Checkpoint** ($TIMESTAMP)

$STATUS
🧠 Memory synced to Redis
💾 4-layer persistence active

📄 Full log: \`$LOGFILE\`

*Runs every 5 minutes | Hourly report*"
fi

echo "[$TIMESTAMP] Checkpoint complete" >> "$LOGFILE"

exit 0
