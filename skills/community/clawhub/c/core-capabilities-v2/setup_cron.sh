#!/bin/bash
# 配置记忆数据库定时同步任务
# 使用 memory_query_agent.py 进行同步（包含自然语言查询功能）

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/memory_query_agent.py"
LOG_FILE="$SCRIPT_DIR/logs/memory_sync.log"

mkdir -p "$(dirname "$LOG_FILE")"

echo "🔧 配置记忆数据库定时同步任务"
echo "======================================"

if crontab -l 2>/dev/null | grep -q "memory_query_agent.py"; then
    echo "✅ 定时任务已存在"
    crontab -l | grep "memory_query_agent"
else
    echo "📝 添加定时任务..."
    (crontab -l 2>/dev/null | grep -v "memory_query_agent.py" | grep -v "memory_to_sqlite.py"; \
     echo "*/30 * * * * cd $SCRIPT_DIR && python3 $PYTHON_SCRIPT --sync-now >> $LOG_FILE 2>&1") | crontab -
    echo "✅ 已添加定时任务："
    echo " - 每 30 分钟同步一次"
    echo " - 日志文件：$LOG_FILE"
fi

echo ""
echo "📋 当前所有定时任务："
crontab -l 2>/dev/null || echo "（无定时任务）"

echo ""
echo "💡 管理命令："
echo "  查看日志：tail -f $LOG_FILE"
echo "  查看任务：crontab -l"
echo "  删除任务：crontab -e"
echo "  手动同步：python3 $PYTHON_SCRIPT --sync-now"
echo "  查看状态：python3 $PYTHON_SCRIPT --sync-status"
echo "  交互查询：python3 $PYTHON_SCRIPT -i"
