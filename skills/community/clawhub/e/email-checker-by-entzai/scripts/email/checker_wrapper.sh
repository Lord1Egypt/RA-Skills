#!/bin/bash
# Email Checker - Wrapper script for cron execution
# Runs the main Python checker and logs output

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CRON_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_DIR="$CRON_DIR/logs"
mkdir -p "$LOG_DIR"

echo "=== Email Check Started: $(date) ===" >> "$LOG_DIR/email_check.log"

# Run the Python checker — wrapper owns all logging, no crontab redirect needed
python3 "$SCRIPT_DIR/checker.py" >> "$LOG_DIR/email_check.log" 2>&1

echo "" >> "$LOG_DIR/email_check.log"
