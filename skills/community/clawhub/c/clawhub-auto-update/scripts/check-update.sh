#!/usr/bin/env bash
# clawhub-auto-update.sh - 自动更新ClawHub技能（简化版）

LOG_FILE="$HOME/.openclaw/logs/skill-update.log"

echo "🔄 检查ClawHub技能更新... [$(date '+%Y-%m-%d %H:%M')]" | tee -a "$LOG_FILE"

# 直接运行更新
npx clawhub update --all 2>&1 | tee -a "$LOG_FILE"

echo "✅ 检查完成 [$(date '+%Y-%m-%d %H:%M')]" | tee -a "$LOG_FILE"
