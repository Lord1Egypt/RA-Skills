#!/bin/bash
# Cyber Growth - 事件积累器
# 超轻量：只追加一行到日志文件，不读不写数据库
# 用法: accumulate.sh <描述> [--domain <领域>] [--xp <数值>] [--type <类型>]

set -uo pipefail

LOG_DIR="${CYBER_GROWTH_LOG:-$HOME/.openclaw/memory/cyber-growth-events}"
mkdir -p "$LOG_DIR"

# 当日日志文件
TODAY=$(date +"%Y-%m-%d")
LOG_FILE="$LOG_DIR/$TODAY.jsonl"

# 解析参数
description="" domain="general" xp=0 type="mission-cleared"
while [[ $# -gt 0 ]]; do
    case "$1" in
        --domain) domain="$2"; shift 2 ;;
        --xp) xp="$2"; shift 2 ;;
        --type) type="$2"; shift 2 ;;
        -*) shift ;;
        *)
            if [ -z "$description" ]; then description="$1"; fi
            shift
            ;;
    esac
done

if [ -z "$description" ]; then
    echo "Usage: accumulate.sh <description> [--domain <d>] [--xp <n>] [--type <t>]" >&2
    exit 1
fi

# 追加一行 JSONL（单次写入，不读文件）
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
printf '{"ts":"%s","desc":"%s","domain":"%s","xp":%d,"type":"%s"}\n' \
    "$timestamp" "$description" "$domain" "$xp" "$type" >> "$LOG_FILE"

# 极简输出
echo "📡 +${xp}XP [${domain}] ${description}" >&2
