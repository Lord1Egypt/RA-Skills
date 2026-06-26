#!/bin/bash
# AI 行业日报定时任务脚本
# 每天 7:00 自动运行
# SKILL: ai_daily_briefing_generator v1.3.1

export HTTP_PROXY="http://127.0.0.1:7897"
export HTTPS_PROXY="http://127.0.0.1:7897"

DATE=$(date '+%Y-%m-%d')
LOG_DIR=~/.openclaw/logs
mkdir -p "$LOG_DIR"

# 调用 ai_daily_briefing_generator SKILL
cd ~/.openclaw/skills/ai_daily_briefing_generator

# 运行 SKILL（通过 openclaw skill run）
/usr/local/bin/openclaw skill run ai_daily_briefing_generator \
  --target_date="$DATE" \
  --searxng_enabled=false \
  --tavily_enabled=true \
  >> "$LOG_DIR/ai_daily.log" 2>&1

echo "[$(date)] AI日报生成完成" >> "$LOG_DIR/ai_daily.log"