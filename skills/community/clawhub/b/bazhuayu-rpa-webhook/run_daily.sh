#!/bin/bash
# 八爪鱼 RPA Webhook 每日自动运行脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/run.log"

# 确保日志文件存在并设置安全权限 (600)
touch "$LOG_FILE"
chmod 600 "$LOG_FILE"

# 记录运行日志
echo "=== 运行时间：$(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG_FILE"

# 运行任务（使用默认参数）
cd "$SCRIPT_DIR"
python3 bazhuayu-webhook.py run >> "$LOG_FILE" 2>&1

# 记录运行结果
if [ $? -eq 0 ]; then
    echo "✅ 运行成功" >> "$LOG_FILE"
else
    echo "❌ 运行失败" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"

# 再次确保日志文件权限正确（防止被重新创建）
chmod 600 "$LOG_FILE"
