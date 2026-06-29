#!/bin/bash
# ClawHub login - runs in background, saves output to file
LOG_FILE=/tmp/clawhub_login.log
echo "[$(date)] Starting clawhub login..." > "$LOG_FILE"
clawhub login >> "$LOG_FILE" 2>&1
echo "[$(date)] clawhub login exited with code $?" >> "$LOG_FILE"
