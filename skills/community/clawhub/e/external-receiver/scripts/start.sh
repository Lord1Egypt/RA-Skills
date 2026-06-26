#!/usr/bin/env bash
# ─────────────────────────────────────────────
# External Receiver - 启动脚本
# ─────────────────────────────────────────────

set -e

PORT="${RECEIVER_PORT:-8080}"
HOST="${RECEIVER_HOST:-0.0.0.0}"
SECRET="${RECEIVER_SECRET:-}"

echo "🌐 External Receiver 启动"
echo "   地址: http://$HOST:$PORT"
echo "   目录: $(cd $(dirname $0)/.. && pwd)/received"
echo ""

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

# 检查 python3
if ! command -v python3 &> /dev/null; then
    echo "❌ python3 未安装"
    exit 1
fi

# 启动服务
ARGs=(--port "$PORT" --host "$HOST")
if [ -n "$SECRET" ]; then
    ARGs+=(--secret "$SECRET")
fi

echo "按 Ctrl+C 停止"
echo "---"

python3 receiver_server.py "${ARGs[@]}"
