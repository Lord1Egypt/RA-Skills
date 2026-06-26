#!/usr/bin/env bash
# bytesagain-x-manager — X (Twitter) account management skill
# Usage: bash scripts/script.sh <command> [options]
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
MONITOR="$SKILL_DIR/scripts/x-monitor.py"
ENGAGE="$SKILL_DIR/scripts/x-engage.py"

_log() { echo "[$(date '+%H:%M:%S')] $*" >&2; }

cmd_draft() {
    # Generate 3 tweet drafts for today using xAI trend analysis
    _log "Generating daily tweet drafts..."
    python3 "$MONITOR" --draft-only
}

cmd_post() {
    # Post a tweet from today's saved drafts
    # Usage: post --index 0|1|2
    local index=0
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --index) index="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
    _log "Posting tweet #$((index+1)) from today's drafts..."
    python3 "$MONITOR" --auto-post --post-index "$index"
}

cmd_monitor() {
    # Run brand + competitor monitoring report (sends Telegram)
    _log "Running brand monitoring report..."
    python3 "$MONITOR" --monitor-only
}

cmd_like() {
    # Auto-like AI/skill related tweets to grow visibility
    _log "Auto-liking relevant tweets..."
    python3 "$ENGAGE" --like
}

cmd_scan_mentions() {
    # Scan @bytesagain mentions, draft replies, send Telegram for approval
    _log "Scanning mentions..."
    python3 "$ENGAGE" --monitor
}

cmd_send_reply() {
    # Send approved reply to one or more tweet IDs (staggered 30-90s)
    # Usage: send-reply <tweet_id> [tweet_id2 ...]
    if [[ $# -eq 0 ]]; then
        echo "Usage: bash scripts/script.sh send-reply <tweet_id> [tweet_id2 ...]" >&2
        exit 1
    fi
    _log "Sending approved replies to: $*"
    python3 "$ENGAGE" --send "$@"
}

cmd_status() {
    # Show current account status and pending queue
    _log "Checking status..."
    echo "=== Pending Replies ==="
    python3 - << 'PYEOF'
import json, os
f = "/tmp/x-pending-replies.json"
if os.path.exists(f):
    data = json.load(open(f))
    if data:
        for p in data:
            print(f"  [{p['tweet_id']}] @{p['author']} ({p['followers']:,} followers)")
            print(f"    Draft: {p['draft_reply'][:80]}...")
    else:
        print("  No pending replies")
else:
    print("  No pending replies file")

print("\n=== Today's Drafts ===")
from datetime import datetime
df = f"/tmp/x-drafts-{datetime.now().strftime('%Y-%m-%d')}.json"
if os.path.exists(df):
    data = json.load(open(df))
    for i, t in enumerate(data.get("tweets", [])):
        print(f"  [{i}] {t[:80]}...")
else:
    print("  No drafts generated yet today")
PYEOF
}

cmd_help() {
    cat << 'EOF'
bytesagain-x-manager — X (Twitter) account management

Commands:
  draft              Generate 3 tweet drafts for today (1x xAI call)
  post --index N     Post tweet #N from today's drafts (0=first, 1=second, 2=third)
  monitor            Brand + competitor monitoring report → Telegram
  like               Auto-like AI/skill related tweets
  scan-mentions      Scan @bytesagain mentions → draft replies → Telegram approval
  send-reply <id>    Send approved reply (multiple IDs staggered 30-90s apart)
  status             Show pending replies and today's drafts
  help               Show this help

Examples:
  bash scripts/script.sh draft
  bash scripts/script.sh post --index 0
  bash scripts/script.sh monitor
  bash scripts/script.sh like
  bash scripts/script.sh scan-mentions
  bash scripts/script.sh send-reply 2044039333045301434
  bash scripts/script.sh send-reply 111 222 333

Cron schedule (recommended):
  30 8  * * *       monitor
  0  9  * * *       draft
  0  9,13,17,21 * * *  like
  5  10 * * *       post --index 0
  5  15 * * *       post --index 1
  5  20 * * *       post --index 2
  0  */2 * * *      scan-mentions

Powered by BytesAgain | bytesagain.com
EOF
}

# Main dispatcher
CMD="${1:-help}"
shift 2>/dev/null || true

case "$CMD" in
    draft)          cmd_draft "$@" ;;
    post)           cmd_post "$@" ;;
    monitor)        cmd_monitor "$@" ;;
    like)           cmd_like "$@" ;;
    scan-mentions)  cmd_scan_mentions "$@" ;;
    send-reply)     cmd_send_reply "$@" ;;
    status)         cmd_status "$@" ;;
    help|--help|-h) cmd_help ;;
    *)
        echo "Unknown command: $CMD" >&2
        cmd_help
        exit 1
        ;;
esac
