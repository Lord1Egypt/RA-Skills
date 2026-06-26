#!/bin/bash
# 每天 16:00 运行 agentfarm-finder

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/output/cron.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始运行 agentfarm-finder" >> "$LOG_FILE"

bash "${SCRIPT_DIR}/agentfarm.sh" >> "$LOG_FILE" 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 运行完成" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
