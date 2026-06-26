#!/bin/bash
# Business API Recorder - 网络监控脚本

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MONITOR_SCRIPT="$SCRIPT_DIR/scripts/network-monitor.js"

# 检查脚本是否存在
if [ ! -f "$MONITOR_SCRIPT" ]; then
    echo "Error: network-monitor.js not found"
    exit 1
fi

# 输出脚本内容（供注入使用）
cat "$MONITOR_SCRIPT"
