#!/bin/bash
# Binance Announce Monitor - 快速启动脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 币安公告监控启动器"
echo "=================="

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误：Node.js 未安装"
    echo "请安装 Node.js 18+: https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ 错误：需要 Node.js 18+ (当前：$(node -v))"
    exit 1
fi

echo "✅ Node.js: $(node -v)"

# 启动监控
echo ""
echo "启动监控..."
node monitor.js &
MONITOR_PID=$!

echo "监控进程 PID: $MONITOR_PID"
echo ""
echo "提示："
echo "- 按 Ctrl+C 停止"
echo "- 日志输出到当前终端"
echo "- 状态文件：binance-announce-state.json"
echo "- 通知文件：binance-pending-notify.json"
echo ""

# 等待进程
wait $MONITOR_PID
