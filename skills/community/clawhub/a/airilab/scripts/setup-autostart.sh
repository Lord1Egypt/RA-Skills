#!/bin/bash
# AiriLab Worker 开机自启配置脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CRON_ENTRY="@reboot $SCRIPT_DIR/start-worker.sh"

echo "🔧 AiriLab Worker 开机自启配置"
echo "=" | tr -d '\n' && printf '%.0s=' {1..40} && echo
echo ""

# 检查 crontab
if ! command -v crontab &> /dev/null; then
    echo "❌ 错误：找不到 crontab 命令"
    exit 1
fi

# 检查是否已配置
EXISTING=$(crontab -l 2>/dev/null | grep -F "start-worker.sh" || true)

if [ -n "$EXISTING" ]; then
    echo "✅ 开机自启已配置"
    echo "   $EXISTING"
    echo ""
    echo "💡 如需移除，执行:"
    echo "   crontab -l | grep -v 'start-worker.sh' | crontab -"
else
    echo "📝 添加开机自启配置..."
    (crontab -l 2>/dev/null | grep -v '^#'; echo "$CRON_ENTRY") | crontab -
    echo "✅ 开机自启已配置"
    echo "   $CRON_ENTRY"
fi

echo ""
echo "📊 当前 crontab 配置:"
crontab -l | grep -E "(start-worker|airilab)" || echo "   (无)"

echo ""
echo "💡 提示：重启系统后 worker 会自动启动"
