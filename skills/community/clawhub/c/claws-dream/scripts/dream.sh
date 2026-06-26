#!/bin/bash
# claws-dream — Trigger nightly memory consolidation
# Called by launchd/systemd/cron at 3 AM daily

set -euo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
SKILL_DIR="$WORKSPACE/skills/claws-dream"
LOG_DIR="$WORKSPACE/logs"
DREAM_LOG="$LOG_DIR/claws-dream.log"
LOCK_FILE="$WORKSPACE/logs/claws-dream.lock"

mkdir -p "$LOG_DIR"

echo "=== claws-dream $(date) ===" >> "$DREAM_LOG"

# Idempotency: prevent concurrent runs
exec 200>"$LOCK_FILE"
if ! flock -n 200; then
    echo "Already running, skipping" >> "$DREAM_LOG"
    exit 0
fi

# Check if already ran today
TODAY=$(date +%Y-%m-%d)
if grep -m1 "^## 🌙 Dream" "$WORKSPACE/memory/dream-log.md" 2>/dev/null | grep -q "$TODAY"; then
    echo "Already dreamed today, skipping" >> "$DREAM_LOG"
    exit 0
fi

# Backup MEMORY.md before any write
if [ -f "$WORKSPACE/MEMORY.md" ]; then
    cp "$WORKSPACE/MEMORY.md" "$WORKSPACE/MEMORY.md.bak.$(date +%Y%m%d%H%M%S)"
    # Keep only last 3 backups
    ls -t "$WORKSPACE/MEMORY.md.bak."* 2>/dev/null | tail -n +4 | xargs rm -f 2>/dev/null || true
fi

echo "Triggering dream at $(date)" >> "$DREAM_LOG"

# Trigger via openclaw cron run (more reliable than sending message)
openclaw cron run 9426984b-de79-4ebd-b798-869eb9dc0a3f >> "$DREAM_LOG" 2>&1 || {
    echo "Cron run failed with exit code $?" >> "$DREAM_LOG"
    exit 1
}

echo "Dream triggered at $(date)" >> "$DREAM_LOG"