#!/bin/bash
# OpenClaw Memory System — Cron Job Setup
# Run this to configure automated cron jobs for memory maintenance

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"
WORKSPACE="${1:-$(pwd)}"

info() { echo -e "\033[36m[INFO]\033[0m $1"; }
ok()   { echo -e "\033[32m[OK]\033[0m $1"; }
warn() { echo -e "\033[33m[WARN]\033[0m $1"; }

info "OpenClaw Memory System — Cron Setup"
info "Workspace: $WORKSPACE"

# Check if crontab is available
if ! command -v crontab &> /dev/null; then
    echo "Error: crontab not found. Please install cron."
    exit 1
fi

# Create temporary crontab file
TEMP_CRON=$(mktemp)
crontab -l > "$TEMP_CRON" 2> /dev/null || true

# Check if already configured
if grep -q "OpenClaw Memory System" "$TEMP_CRON"; then
    warn "OpenClaw Memory System cron jobs already configured."
    warn "Remove existing entries and re-run to update."
    rm "$TEMP_CRON"
    exit 0
fi

# Add cron jobs
cat >> "$TEMP_CRON" << EOF

# --- OpenClaw Memory System Cron Jobs ---
# Nightly memory extraction (23:00 daily)
0 23 * * * cd "$WORKSPACE" && "$SKILL_ROOT/scripts/memory-extract.sh" "$WORKSPACE" >> "$WORKSPACE/memory/cron.log" 2>&1

# Daily notes reminder (09:00 daily)
0 9 * * * cd "$WORKSPACE" && echo "## $(date '+\%H:\%M') -- Daily Notes Reminder" >> "$WORKSPACE/memory/$(date '+\%Y-\%m-\%d').md" 2>> /dev/null

# Heartbeat check (every 30 minutes)
*/30 * * * * cd "$WORKSPACE" && "$SKILL_ROOT/scripts/heartbeat-check.sh" "$WORKSPACE" >> "$WORKSPACE/memory/cron.log" 2>&1
# --- End OpenClaw Memory System ---

EOF

# Install crontab
crontab "$TEMP_CRON"
rm "$TEMP_CRON"

ok "Cron jobs installed successfully!"
echo ""
echo "Scheduled jobs:"
echo "  - Nightly memory extraction at 23:00"
echo "  - Daily notes reminder at 09:00"
echo "  - Heartbeat check every 30 minutes"
echo ""
echo "View with: crontab -l"
echo "Logs go to: $WORKSPACE/memory/cron.log"
