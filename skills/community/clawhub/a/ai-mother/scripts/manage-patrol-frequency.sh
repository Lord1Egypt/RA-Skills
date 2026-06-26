#!/bin/bash
# Dynamic patrol frequency manager
# Tracks active conversations and adjusts patrol frequency

SKILL_DIR="$HOME/.openclaw/skills/ai-mother"
CONV_DIR="$SKILL_DIR/conversations"

# Prevent concurrent runs
LOCK_FILE="$SKILL_DIR/.freq.lock"
exec 9>"$LOCK_FILE"
flock -n 9 || exit 0

NOW=$(date +%s)
THIRTY_MIN_AGO=$((NOW - 1800))
TEN_MIN_AGO=$((NOW - 600))

HIGH_FREQ_PIDS=()

count_recent_messages() {
    local log_file="$1"
    local cutoff="$2"
    local count=0

    while IFS= read -r line; do
        # Extract timestamp: [YYYY-MM-DD HH:MM:SS]
        ts=$(echo "$line" | sed -n 's/^\[\([0-9-]* [0-9:]*\)\].*/\1/p')
        [ -z "$ts" ] && continue
        epoch=$(date -d "$ts" +%s 2>/dev/null)
        [ -z "$epoch" ] && continue
        [ "$epoch" -ge "$cutoff" ] && count=$((count + 1))
    done < <(grep "to_baby:" "$log_file" 2>/dev/null)

    echo "$count"
}

# Check each conversation log for recent activity
if [ -d "$CONV_DIR" ]; then
    for log_file in "$CONV_DIR"/*.log; do
        [ -f "$log_file" ] || continue

        PID=$(basename "$log_file" .log)
        ps -p "$PID" > /dev/null 2>&1 || continue

        RECENT_30MIN=$(count_recent_messages "$log_file" "$THIRTY_MIN_AGO")
        RECENT_10MIN=$(count_recent_messages "$log_file" "$TEN_MIN_AGO")

        # High-frequency threshold: ≥3 messages in 30min OR ≥2 in 10min
        if [ "$RECENT_30MIN" -ge 3 ] || [ "$RECENT_10MIN" -ge 2 ]; then
            HIGH_FREQ_PIDS+=("$PID")
            echo "PID $PID: Active ($RECENT_30MIN msgs/30min, $RECENT_10MIN msgs/10min) → high-freq patrol"
        else
            echo "PID $PID: Quiet ($RECENT_30MIN msgs/30min) → normal patrol"
        fi
    done
fi

# Get existing high-freq job ID
get_highfreq_job_id() {
    openclaw cron list --json 2>/dev/null | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    jobs = d.get('jobs', d) if isinstance(d, dict) else d
    for j in jobs:
        if j.get('name') == 'ai-mother-patrol-high-freq':
            print(j.get('id',''))
            break
except: pass
" 2>/dev/null
}

# Manage cron jobs based on activity
if [ ${#HIGH_FREQ_PIDS[@]} -gt 0 ]; then
    echo ""
    echo "🔥 ${#HIGH_FREQ_PIDS[@]} active process(es): ${HIGH_FREQ_PIDS[*]}"

    EXISTING_ID=$(get_highfreq_job_id)
    if [ -z "$EXISTING_ID" ]; then
        echo "   Creating high-frequency patrol (every 5 min) for active PIDs..."
        # Store active PIDs in a file for patrol to check
        echo "${HIGH_FREQ_PIDS[*]}" > "$SKILL_DIR/.active_pids"
        
        openclaw cron add \
            --name "ai-mother-patrol-high-freq" \
            --every 5m \
            --system-event "AI Mother high-frequency patrol for active conversations. Run: ~/.openclaw/skills/ai-mother/scripts/patrol.sh --quiet. Only notify for PIDs in .active_pids file." \
            2>/dev/null && echo "   ✅ High-frequency patrol enabled (every 5 min)"
    else
        # Update active PIDs file
        echo "${HIGH_FREQ_PIDS[*]}" > "$SKILL_DIR/.active_pids"
        echo "   ✅ High-frequency patrol active, updated active PIDs"
    fi
else
    # Clean up active PIDs file
    rm -f "$SKILL_DIR/.active_pids"
    
    EXISTING_ID=$(get_highfreq_job_id)
    if [ -n "$EXISTING_ID" ]; then
        echo "   No active conversations — downgrading to normal patrol (30 min)..."
        openclaw cron rm "$EXISTING_ID" 2>/dev/null && echo "   ✅ Downgraded to normal frequency"
    else
        echo "✅ Normal patrol frequency (30 min) is sufficient"
    fi
fi
