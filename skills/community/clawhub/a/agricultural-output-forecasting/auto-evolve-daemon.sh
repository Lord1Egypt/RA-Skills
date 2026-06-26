#!/bin/bash
# Auto-Evolution Daemon for agricultural-output-forecasting
SKILL_PATH="/home/node/.openclaw/workspace/skills/agricultural-output-forecasting"
LOG_FILE="$SKILL_PATH/auto-evolution.log"

echo "🧬 Auto-Evolution Started: $(date)" > $LOG_FILE
while true; do
    echo "[$(date)] Evolving..." >> $LOG_FILE
    cd $SKILL_PATH && python3 scripts/self_evolve.py >> $LOG_FILE 2>&1
    sleep 1800
done
