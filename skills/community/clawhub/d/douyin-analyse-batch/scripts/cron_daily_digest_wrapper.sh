#!/bin/bash
# cron_daily_digest_wrapper.sh — Cron 调用的入口脚本
# 设置环境变量后调用 run_daily_digest.py
set -e

# 读取 .env 文件（如果存在）
ENV_FILE="$(cd "$(dirname "$0")" && cd .. && pwd)/.env"
if [ -f "$ENV_FILE" ]; then
    set -a
    source "$ENV_FILE"
    set +a
fi

# SMTP 邮件配置（必填）
export SMTP_USER="${SMTP_USER:-3249331357@qq.com}"
export SMTP_PASS="${SMTP_PASS:-}"
export SMTP_HOST="${SMTP_HOST:-smtp.qq.com}"
export SMTP_PORT="${SMTP_PORT:-587}"

# 收件人配置
export DOUYIN_EMAIL_RECIPIENTS="${DOUYIN_EMAIL_RECIPIENTS:-3249331357@qq.com,1853026634@qq.com}"

# 输出目录
export DOUYIN_OUTPUT_DIR="${DOUYIN_OUTPUT_DIR:-$HOME/Documents/douyin_analysis}"
export DOUYIN_ANALYSIS_DIR="$(cd "$(dirname "$0")" && cd .. && pwd)"

# Python 虚拟环境
export DOUYIN_VENV_PY="${DOUYIN_VENV_PY:-/tmp/douyin_transcribe/venv/bin/python3}"

# 日报条数（默认15）
LIMIT="${1:-${DOUYIN_DIGEST_LIMIT:-15}}"

# 运行主脚本
exec "$HOME/.openclaw/workspace/skills/douyin-daily-report/scripts/run_daily_digest.py" \
    --limit "$LIMIT" \
    --skip-transcribe
