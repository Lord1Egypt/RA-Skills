#!/bin/bash
# gateway-verify.sh - 验证网关配置

INSTANCE="$1"

if [ -z "$INSTANCE" ]; then
    echo "用法：gateway-verify.sh <实例名>"
    echo ""
    echo "实例名:"
    echo "  local-shrimp / 本地虾 → ~/.jvs/.openclaw/"
    echo "  feishu / 飞书 → ~/.openclaw/"
    exit 1
fi

# 解析实例名
case "$INSTANCE" in
    local-shrimp|本地虾 |18789|local)
        CONFIG_DIR="$HOME/.jvs/.openclaw"
        PLIST_FILE="$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist"
        INSTANCE_NAME="本地虾"
        ;;
    feishu|飞书|18790|fly)
        CONFIG_DIR="$HOME/.openclaw"
        PLIST_FILE="$HOME/Library/LaunchAgents/ai.openclaw.gateway-feishu.plist"
        INSTANCE_NAME="飞书机器人"
        ;;
    *)
        echo "❌ 未知实例名：$INSTANCE"
        exit 1
        ;;
esac

echo "=== 验证 $INSTANCE_NAME 配置 ==="
echo ""

ERRORS=0

# 1. 检查配置文件
CONFIG_FILE="$CONFIG_DIR/openclaw.json"
if [ -f "$CONFIG_FILE" ]; then
    echo "✅ 配置文件存在：$CONFIG_FILE"
    PORT=$(cat "$CONFIG_FILE" | jq -r '.gateway.port')
    echo "   配置端口：$PORT"
else
    echo "❌ 配置文件不存在：$CONFIG_FILE"
    ERRORS=$((ERRORS + 1))
fi

# 2. 检查嵌套配置
if [ -f "$CONFIG_DIR/.openclaw/openclaw.json" ]; then
    NESTED_PORT=$(cat "$CONFIG_DIR/.openclaw/openclaw.json" | jq -r '.gateway.port')
    if [ "$PORT" = "$NESTED_PORT" ]; then
        echo "✅ 嵌套配置一致：$NESTED_PORT"
    else
        echo "❌ 嵌套配置不一致：$NESTED_PORT (应该是 $PORT)"
        ERRORS=$((ERRORS + 1))
    fi
fi

# 3. 检查 LaunchAgent plist
if [ -f "$PLIST_FILE" ]; then
    echo "✅ LaunchAgent 存在：$PLIST_FILE"
    PLIST_PORT=$(cat "$PLIST_FILE" | grep -A1 "ProgramArguments" | grep "187" | head -1 | tr -d ' \t<>/string')
    if [ -n "$PLIST_PORT" ]; then
        echo "   Plist 端口：$PLIST_PORT"
        if [ "$PORT" != "$PLIST_PORT" ]; then
            echo "⚠️  Plist 端口与配置文件不一致"
            ERRORS=$((ERRORS + 1))
        fi
    fi
else
    echo "❌ LaunchAgent 不存在：$PLIST_FILE"
    ERRORS=$((ERRORS + 1))
fi

# 4. 检查端口监听
if [ -n "$PORT" ]; then
    if lsof -i :$PORT | grep LISTEN > /dev/null 2>&1; then
        PID=$(lsof -i :$PORT | grep LISTEN | awk '{print $2}' | head -1)
        echo "✅ 端口 $PORT 正在监听 (PID: $PID)"
    else
        echo "❌ 端口 $PORT 未监听"
        ERRORS=$((ERRORS + 1))
    fi
fi

# 5. 检查进程
if ps aux | grep "openclaw.*gateway" | grep -v grep > /dev/null 2>&1; then
    echo "✅ 网关进程运行中"
else
    echo "❌ 网关进程未运行"
    ERRORS=$((ERRORS + 1))
fi

# 6. Dashboard 可访问性
if [ -n "$PORT" ]; then
    if curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:$PORT/" 2>/dev/null | grep -E "200|30[0-9]" > /dev/null; then
        echo "✅ Dashboard 可访问：http://127.0.0.1:$PORT/"
    else
        echo "⚠️  Dashboard 无法访问：http://127.0.0.1:$PORT/"
    fi
fi

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "🎉 所有检查通过！"
else
    echo "⚠️  发现 $ERRORS 个问题"
fi

exit $ERRORS
