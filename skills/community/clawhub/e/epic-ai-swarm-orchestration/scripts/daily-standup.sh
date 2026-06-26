#!/usr/bin/env bash
# daily-standup.sh — Generate and send daily standup summary
#
# Usage: daily-standup.sh
# Typically called via cron at 09:00 PST
#
# Reads: active-tasks.json, inbox.json, tmux sessions, recent git logs
# Sends: Telegram summary via openclaw message send

export PATH="$(dirname "$(command -v openclaw 2>/dev/null || echo /usr/local/bin/openclaw)"):/usr/local/bin:/usr/bin:/bin:$PATH"

SWARM_DIR="$(cd "$(dirname "$0")" && pwd)"
TASKS_FILE="$SWARM_DIR/active-tasks.json"
INBOX_FILE="$SWARM_DIR/inbox.json"
LOGS_DIR="$SWARM_DIR/logs"
TODAY=$(date '+%Y-%m-%d')
NOW_MS=$(date +%s%3N)
CUTOFF_MS=$(( NOW_MS - 86400000 ))  # 24h ago in ms

mkdir -p "$LOGS_DIR"

# Source config
NOTIFY_TARGET=""
NOTIFY_CHANNEL="telegram"
[[ -f "$SWARM_DIR/swarm.conf" ]] && source "$SWARM_DIR/swarm.conf"
NOTIFY_TARGET="${SWARM_NOTIFY_TARGET:-$NOTIFY_TARGET}"
NOTIFY_CHANNEL="${SWARM_NOTIFY_CHANNEL:-$NOTIFY_CHANNEL}"

# ── Gather data ──────────────────────────────────────────────────────────────

# Completed and failed tasks from active-tasks.json (last 24h)
COMPLETED_LIST=""
COMPLETED_COUNT=0
FAILED_COUNT=0
REVIEW_COUNT=0

if [[ -f "$TASKS_FILE" ]]; then
  eval "$(python3 - "$TASKS_FILE" "$CUTOFF_MS" <<'PYEOF'
import json, sys

tasks_file = sys.argv[1]
cutoff_ms  = int(sys.argv[2])

try:
    with open(tasks_file) as f:
        data = json.load(f)
except Exception:
    print("COMPLETED_COUNT=0")
    print("FAILED_COUNT=0")
    print("REVIEW_COUNT=0")
    print("COMPLETED_LIST=''")
    sys.exit(0)

tasks = data.get('tasks', [])

completed_items = []
failed_count = 0
review_count = 0

for t in tasks:
    status = t.get('status', '')
    if status == 'done':
        completed_at = t.get('completedAt')
        if completed_at and int(completed_at) >= cutoff_ms:
            tid = t.get('id', 'unknown')
            proj = t.get('project', '')
            completed_items.append((tid, proj))
    elif status == 'failed':
        failed_at = t.get('failedAt')
        if failed_at and int(failed_at) >= cutoff_ms:
            failed_count += 1
    elif status == 'review':
        review_count += 1

# Build shell-safe list string
lines = []
for tid, proj in completed_items:
    if proj:
        lines.append(f"   - {tid} ({proj})")
    else:
        lines.append(f"   - {tid}")

completed_list = "\\n".join(lines)

print(f"COMPLETED_COUNT={len(completed_items)}")
print(f"FAILED_COUNT={failed_count}")
print(f"REVIEW_COUNT={review_count}")
# Use printf-safe encoding: pass via file to avoid quoting issues
import tempfile, os
tmp = tempfile.mktemp(prefix='/tmp/standup_list_')
with open(tmp, 'w') as fh:
    fh.write('\n'.join(f"   - {tid} ({proj})" if proj else f"   - {tid}" for tid, proj in completed_items))
print(f"COMPLETED_LIST_FILE={tmp}")
PYEOF
  )" 2>/dev/null || true
fi

# Read completed list from temp file
if [[ -n "${COMPLETED_LIST_FILE:-}" && -f "$COMPLETED_LIST_FILE" ]]; then
  COMPLETED_LIST=$(cat "$COMPLETED_LIST_FILE")
  rm -f "$COMPLETED_LIST_FILE"
fi

# Running agents: count tmux sessions matching (claude|codex|gemini|deepseek)-*
RUNNING_COUNT=0
TMUX_LIST=""
if tmux ls 2>/dev/null | grep -qE "^(claude|codex|gemini|deepseek)-"; then
  TMUX_LINE=$(tmux ls 2>/dev/null | grep -E "^(claude|codex|gemini|deepseek)-" || true)
  RUNNING_COUNT=$(echo "$TMUX_LINE" | grep -c . || echo 0)
  TMUX_LIST="$TMUX_LINE"
fi

# Inbox queued tasks
INBOX_COUNT=0
if [[ -f "$INBOX_FILE" ]]; then
  INBOX_COUNT=$(python3 -c "
import json, sys
try:
    with open('$INBOX_FILE') as f:
        data = json.load(f)
    print(len(data.get('tasks', [])))
except Exception:
    print(0)
" 2>/dev/null || echo 0)
fi

# ── Format message ────────────────────────────────────────────────────────────

COMPLETED_COUNT=${COMPLETED_COUNT:-0}
FAILED_COUNT=${FAILED_COUNT:-0}
REVIEW_COUNT=${REVIEW_COUNT:-0}

if [[ "$COMPLETED_COUNT" -eq 0 && "$RUNNING_COUNT" -eq 0 && "$FAILED_COUNT" -eq 0 && "$INBOX_COUNT" -eq 0 ]]; then
  MSG="🌅 Daily Standup — $TODAY
All quiet. No active work or queued tasks."
else
  MSG="🌅 Daily Standup — $TODAY

✅ Completed (24h): $COMPLETED_COUNT tasks"

  if [[ -n "$COMPLETED_LIST" ]]; then
    MSG="$MSG
$COMPLETED_LIST"
  fi

  MSG="$MSG
🔨 Running: $RUNNING_COUNT agents
🔍 In review: $REVIEW_COUNT tasks
❌ Failed: $FAILED_COUNT tasks
📥 Inbox: $INBOX_COUNT tasks queued"
fi

# ── Write to log ──────────────────────────────────────────────────────────────

STANDUP_LOG="$LOGS_DIR/standup-${TODAY}.md"
{
  echo "# Standup — $TODAY"
  echo ""
  echo '```'
  echo "$MSG"
  echo '```'
  echo ""
  echo "Generated: $(date '+%Y-%m-%d %H:%M:%S')"
} > "$STANDUP_LOG"

echo "[standup] Written to $STANDUP_LOG"

# ── Send notification ─────────────────────────────────────────────────────────

if [[ -z "$NOTIFY_TARGET" ]]; then
  echo "[standup] No NOTIFY_TARGET configured — skipping Telegram send"
  echo "$MSG"
  exit 0
fi

openclaw message send \
  --channel "$NOTIFY_CHANNEL" \
  --target "$NOTIFY_TARGET" \
  --message "$MSG" 2>/dev/null && echo "[standup] Sent to $NOTIFY_CHANNEL:$NOTIFY_TARGET" || {
  echo "[standup] ⚠️ Telegram send failed — standup saved to $STANDUP_LOG"
  echo "$MSG"
}
