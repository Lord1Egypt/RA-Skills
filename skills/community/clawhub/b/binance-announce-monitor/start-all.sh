#!/bin/bash
# Binance Monitor - 完整监控启动脚本
# 同时启动公告监控和 X 账号监控

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 Binance Monitor - 完整监控启动"
echo "================================"

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误：Node.js 未安装"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ 错误：需要 Node.js 18+ (当前：$(node -v))"
    exit 1
fi

echo "✅ Node.js: $(node -v)"
echo ""

# 启动公告监控
echo "启动公告监控..."
node monitor.js &
MONITOR_PID=$!
echo "✅ 公告监控 PID: $MONITOR_PID"

# 启动 X 账号监控
echo "启动 X 账号监控..."
node x-monitor.js &
X_MONITOR_PID=$!
echo "✅ X 账号监控 PID: $X_MONITOR_PID"

echo ""
echo "================================"
echo "监控已全部启动："
echo "- 公告监控：$MONITOR_PID"
echo "- X 账号监控：$X_MONITOR_PID"
echo ""
echo "提示："
echo "- 按 Ctrl+C 停止所有监控"
echo "- 日志输出到当前终端"
echo "- 状态文件：binance-*-state.json"
echo "- 通知文件：binance-*-notify.json"
echo ""

# 等待进程
wait
