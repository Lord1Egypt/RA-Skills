#!/usr/bin/env bash
# pulse-check.sh — Detect stuck agents and notify
# Run via cron every 60 minutes when agents are active
#
# Stuck detection:
# 1. Check if tmux session exists but agent output hasn't changed in 30+ min
# 2. Check for known stuck patterns (auth prompts, waiting for input, error loops)
# 3. Kill stuck agents and notify

set -euo pipefail

SWARM_DIR="$(cd "$(dirname "$0")" && pwd)"
NOTIFY_FILE="$SWARM_DIR/pending-notifications.txt"
PULSE_STATE="$SWARM_DIR/pulse-state.json"
LOGS_DIR="$SWARM_DIR/logs"

mkdir -p "$LOGS_DIR"

# Initialize pulse state if missing
[[ -f "$PULSE_STATE" ]] || echo '{}' > "$PULSE_STATE"

# Get all agent tmux sessions
AGENT_SESSIONS=$(tmux ls 2>/dev/null | grep -E "^(claude|codex|gemini)-" | cut -d: -f1 || true)

if [[ -z "$AGENT_SESSIONS" ]]; then
  echo "No agent sessions running."
  # Check for pending notifications that haven't been sent
  if [[ -s "$NOTIFY_FILE" ]]; then
    echo "PENDING_NOTIFICATIONS"
    cat "$NOTIFY_FILE"
  fi
  exit 0
fi

STUCK_PATTERNS=(
  "Failed to login"
  "API key must be set"
  "Authentication required"
  "Enter your API key"
  "How would you like to authenticate"
  "Press Enter to continue"
  "Do you want to proceed"
  "y/n"
  "Permission denied"
  "rate limit"
  "429 Too Many Requests"
  "SIGTERM"
  "Error: EACCES"
)

NOW=$(date +%s)
IDLE_DONE_THRESHOLD=600  # 10 minutes

for SESSION in $AGENT_SESSIONS; do
  echo "Checking: $SESSION"
  
  # Capture current pane content
  CURRENT_OUTPUT=$(tmux capture-pane -t "$SESSION" -p 2>/dev/null || echo "CAPTURE_FAILED")
  CURRENT_HASH=$(echo "$CURRENT_OUTPUT" | md5sum | cut -d' ' -f1)
  
  # Get last known hash
  LAST_HASH=$(python3 -c "
import json
with open('$PULSE_STATE') as f: d = json.load(f)
print(d.get('$SESSION', {}).get('hash', ''))
" 2>/dev/null || echo "")
  
  LAST_CHECK=$(python3 -c "
import json
with open('$PULSE_STATE') as f: d = json.load(f)
print(d.get('$SESSION', {}).get('timestamp', 0))
" 2>/dev/null || echo "0")
  
  # Check for stuck patterns
  IS_STUCK="no"
  STUCK_REASON=""
  for PATTERN in "${STUCK_PATTERNS[@]}"; do
    if echo "$CURRENT_OUTPUT" | grep -qi "$PATTERN"; then
      IS_STUCK="yes"
      STUCK_REASON="$PATTERN"
      break
    fi
  done
  
  # Check if log indicates functional completion but terminal session is hanging idle (>10m)
  LOG_FILE="$LOGS_DIR/${SESSION}.log"
  if [[ -f "$LOG_FILE" ]]; then
    LOG_LAST_MOD=$(stat -c %Y "$LOG_FILE" 2>/dev/null || echo 0)
    if [[ "$LOG_LAST_MOD" -gt 0 ]]; then
      LOG_IDLE=$(( NOW - LOG_LAST_MOD ))
      if [[ $LOG_IDLE -gt $IDLE_DONE_THRESHOLD ]] && grep -Eqi "Work log finalized|PR (opened|created):|Branch pushed:|Pushed: .*feat/|Commit:\s+[0-9a-f]{7,}" "$LOG_FILE"; then
        IS_STUCK="functional_done"
        STUCK_REASON="Functionally complete and idle for $(( LOG_IDLE / 60 )) minutes"
      fi
    fi
  fi

  # Check if output hasn't changed in 30+ minutes
  if [[ "$CURRENT_HASH" == "$LAST_HASH" && "$LAST_HASH" != "" && "$IS_STUCK" == "no" ]]; then
    ELAPSED=$(( NOW - LAST_CHECK ))
    if [[ $ELAPSED -gt 1800 ]]; then  # 30 minutes
      IS_STUCK="yes"
      STUCK_REASON="No output change for $(( ELAPSED / 60 )) minutes"
    fi
  fi
  
  # Update state
  python3 -c "
import json
with open('$PULSE_STATE') as f: d = json.load(f)
d['$SESSION'] = {'hash': '$CURRENT_HASH', 'timestamp': $NOW, 'stuck': '$IS_STUCK' == 'yes'}
with open('$PULSE_STATE', 'w') as f: json.dump(d, f, indent=2)
" 2>/dev/null
  
  if [[ "$IS_STUCK" == "functional_done" ]]; then
    echo "ℹ️  FUNCTIONALLY DONE: $SESSION — $STUCK_REASON"
    tmux kill-session -t "$SESSION" 2>/dev/null || true
    echo "✅ Agent $SESSION appears functionally complete and was auto-closed. Reason: $STUCK_REASON" >> "$NOTIFY_FILE"
    echo "   → Auto-closed stale completed session and queued completion notification"
  elif [[ "$IS_STUCK" == "yes" ]]; then
    echo "⚠️  STUCK DETECTED: $SESSION — Reason: $STUCK_REASON"
    
    # Save last output to log
    echo "$CURRENT_OUTPUT" > "$LOGS_DIR/${SESSION}-stuck-$(date +%Y%m%d_%H%M%S).log"
    
    # Kill the stuck session
    tmux kill-session -t "$SESSION" 2>/dev/null || true
    
    # Write notification
    echo "⚠️ Agent $SESSION is STUCK and was killed. Reason: $STUCK_REASON. Check logs at $LOGS_DIR/" >> "$NOTIFY_FILE"
    
    echo "   → Killed session and queued notification"
  else
    echo "   ✅ Healthy (output changing, no stuck patterns)"
  fi
done

# Also check for completed agents (notifications waiting)
if [[ -s "$NOTIFY_FILE" ]]; then
  echo "---"
  echo "Pending notifications:"
  cat "$NOTIFY_FILE"
fi
