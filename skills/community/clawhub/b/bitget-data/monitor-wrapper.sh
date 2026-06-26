#!/bin/bash
# Bitget 多网格监控包装脚本 - 用于 cron 调用

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/grid_monitor.log"

# 运行监控脚本
cd "$SCRIPT_DIR"
node monitor-grid.js 2>&1

EXIT_CODE=$?

# 读取最后几行日志判断状态
if [ $EXIT_CODE -eq 0 ]; then
    # 检查日志中是否有错误
    if tail -20 "$LOG_FILE" | grep -q "❌"; then
        echo "ABNORMAL"
        tail -30 "$LOG_FILE" | grep "❌\|⚠️"
    else
        echo "HEARTBEAT_OK"
    fi
else
    echo "ABNORMAL"
    echo "脚本执行失败，退出码：$EXIT_CODE"
    tail -30 "$LOG_FILE"
fi
