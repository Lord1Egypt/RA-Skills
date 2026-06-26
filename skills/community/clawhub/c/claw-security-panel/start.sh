#!/bin/bash
# OpenClaw Security Panel - 启动脚本

set -e

SKILL_DIR="$HOME/.openclaw/skills/claw-security-panel"
SCRIPT_DIR="$SKILL_DIR/scripts"
PORT=18790

echo "🛡️  OpenClaw Security Panel"
echo "=========================="
echo ""

# 运行安全检查
echo "📋 正在执行安全检查..."
RESULT=$(python3 "$SCRIPT_DIR/security_check.py" --output /tmp/security_report.json)

# 解析结果
TOKEN=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")
SUMMARY=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin)['summary']; print(f\"风险等级：{d['risk_level'].upper()}, 检查项：{d['total_checks']}, 风险数：{len(d['risks'])}\")")

echo "✅ $SUMMARY"
echo ""

# 停止旧的服务器
if [ -f /tmp/security_panel.pid ]; then
    OLD_PID=$(cat /tmp/security_panel.pid)
    if kill -0 $OLD_PID 2>/dev/null; then
        echo "🔄 停止旧的服务 (PID: $OLD_PID)..."
        kill $OLD_PID 2>/dev/null || true
        sleep 1
    fi
fi

# 启动新的服务器
echo "🚀 启动安全面板服务..."
nohup python3 /tmp/security_panel_server.py "$TOKEN" "$PORT" > /tmp/security_panel.log 2>&1 &
SERVER_PID=$!
echo $SERVER_PID > /tmp/security_panel.pid

sleep 2

# 检查服务是否启动成功
if curl -s "http://127.0.0.1:$PORT/claw_security_pannel?token=$TOKEN" > /dev/null; then
    echo ""
    echo "✅ 安全面板已启动!"
    echo ""
    echo "📊 访问链接:"
    echo "   http://127.0.0.1:$PORT/claw_security_pannel?token=$TOKEN"
    echo ""
    echo "⏰ Token 有效期：30 分钟"
    echo "📁 详细报告：/tmp/security_report.json"
    echo ""
else
    echo "❌ 服务启动失败，请查看日志：/tmp/security_panel.log"
    exit 1
fi
