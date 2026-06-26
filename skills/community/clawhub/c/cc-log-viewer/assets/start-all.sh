#!/bin/bash
# log-viewer 一键启动
# 内部管理 CC 进程 + WebSocket 推送 + 前端页面

set -e

PORT=${1:-18798}
NO_CC=""
if [ "$2" = "--no-cc" ]; then NO_CC="--no-cc"; fi

echo "=== log-viewer 启动 ==="

# 清理旧的
kill $(lsof -t -i:$PORT) 2>/dev/null || true

cd "$(dirname "$0")"
nohup node log-streamer.js --port=$PORT $NO_CC > /tmp/log-streamer.log 2>&1 &

sleep 2

# 获取本机局域网 IP
LAN_IP=$(ip -4 addr show 2>/dev/null | grep -oP 'inet \K[\d.]+' | grep -v '127.0.0.1' | head -1)
# 获取 Tailscale IP（如果安装了 Tailscale）
TS_IP=$(tailscale ip -4 2>/dev/null || true)

echo "✅ log-viewer 已启动"
if [ -n "$LAN_IP" ]; then echo "   局域网: http://$LAN_IP:$PORT/"; fi
if [ -n "$TS_IP" ]; then echo "   Tailscale: http://$TS_IP:$PORT/"; fi
echo "   本机: http://localhost:$PORT/"
if [ -n "$NO_CC" ]; then echo "   模式: 仅 Web 服务（不启动 CC）"; fi
echo "   日志: /tmp/log-streamer.log"
