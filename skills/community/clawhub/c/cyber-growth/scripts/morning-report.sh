#!/bin/bash
# Cyber Growth - 晨间报告
# 每天 9:00 自动发送进度面板到飞书
# 用法: morning-report.sh [--channel feishu|telegram|discord]

set -uo pipefail

GROW_SH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/grow.sh"
CHANNEL="${1:-feishu}"

# 生成报告
REPORT=$(bash "$GROW_SH" status 2>&1)

# 生成周报摘要
WEEK_REPORT=$(bash "$GROW_SH" report --days 7 2>&1)

# 组合消息
MSG="🔮 晨间神经报告

$REPORT

$WEEK_REPORT"

# 输出到 stdout（由外部 cron 或 heartbeat 调用时发送）
echo "$MSG"
