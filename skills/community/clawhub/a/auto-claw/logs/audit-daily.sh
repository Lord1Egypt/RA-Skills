#!/bin/bash
# Auto-Claw Daily Health Check
# Generated: 2026-03-24 09:02 UTC

DATE=$(date +%Y%m%d_%H%M%S)
LOG_DIR="$(dirname \"$0\")\"
PROJECT_DIR="$(dirname \"$LOG_DIR\")"

cd "$PROJECT_DIR" || exit 1

echo "=== $(date) ===" >> "$LOG_DIR/audit.log"
python3 cli.py full-audit 2>&1 | tail -10 >> "$LOG_DIR/audit.log"
echo "" >> "$LOG_DIR/audit.log"
