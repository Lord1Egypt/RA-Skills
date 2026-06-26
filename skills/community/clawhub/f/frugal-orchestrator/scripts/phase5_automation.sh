#!/usr/bin/env bash
# Phase 5 weekly automation – gather token metrics, convert to TOON, commit, and log

# Exit on any error
set -e

# Directories
LOG_DIR=/a0/usr/projects/frugal_orchestrator/logs
SCRIPT_DIR=/a0/usr/projects/frugal_orchestrator/scripts

# 1. Run token_tracker.py and capture output
python3 "$LOG_DIR/../scripts/token_tracker.py" > "$LOG_DIR/token_metrics.json"

# 2. Convert JSON metrics to compact TOON format
TOON_PATH="$LOG_DIR/phase5_metrics.toon"
if command -v jq >/dev/null 2>&1; then
    # Extract relevant fields (adjust keys if your tracker uses different names)
    SAVED=$(jq -r '.saved_tokens // 0' "$LOG_DIR/token_metrics.json")
    PERCENT=$(jq -r '.savings_percent // 0' "$LOG_DIR/token_metrics.json")
    TIMESTAMP=$(date -u "+%Y-%m-%dT%H:%M:%SZ")
    
    # Write TOON header
    cat > "$TOON_PATH" <<TOON_EOF
metrics:
  saved_tokens: $SAVED
  savings_percent: $PERCENT
  timestamp: $TIMESTAMP
TOON_EOF
else
    # Fallback: just copy the JSON as plain text
    cp "$LOG_DIR/token_metrics.json" "$TOON_PATH"
fi

# 3. Commit both files and push
cd /a0/usr/projects/frugal_orchestrator
GIT_AUTHOR_DATE="$TIMESTAMP" GIT_COMMITTER_DATE="$TIMESTAMP" \
git add "$LOG_DIR/token_metrics.json" "$TOON_PATH" docs/phase5_log.md \
git commit -m "Update Phase 5 metrics and TOON file [skip ci]" || true
git push origin main

# 4. Append a short entry to the log
 echo "$(date) - Updated token metrics and TOON representation" >> docs/phase5_log.md

# End of script
exit 0
