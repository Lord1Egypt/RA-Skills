#!/bin/bash
# gateway-create.sh - 创建新的 OpenClaw 网关实例

INSTANCE_NAME="$1"
PORT="$2"
CHANNEL="$3"

if [ -z "$INSTANCE_NAME" ] || [ -z "$PORT" ]; then
    echo "用法：gateway-create.sh <实例名> <端口> [频道]"
    echo ""
    echo "示例:"
    echo "  gateway-create.sh test-instance 18888 openim"
    echo "  gateway-create.sh wechat-bot 18889 wechat"
    exit 1
fi

# 检查依赖
if ! command -v jq &> /dev/null; then
    echo "❌ 错误：需要 jq 命令"
    echo "安装：brew install jq"
    exit 1
fi

CONFIG_DIR="$HOME/.openclaw-$INSTANCE_NAME"
PLIST_FILE="$HOME/Library/LaunchAgents/ai.openclaw.gateway-$INSTANCE_NAME.plist"

echo "🔧 创建新实例：$INSTANCE_NAME"
echo "   配置目录：$CONFIG_DIR"
echo "   端口：$PORT"
echo "   频道：${CHANNEL:-openim}"
echo ""

# 1. 检查端口是否被占用
if lsof -i :$PORT > /dev/null 2>&1; then
    echo "❌ 端口 $PORT 已被占用"
    exit 1
fi
echo "✅ 端口 $PORT 可用"

# 2. 创建配置目录
mkdir -p "$CONFIG_DIR"
echo "✅ 配置目录已创建：$CONFIG_DIR"

# 3. 复制基础配置（从现有实例）
if [ -f "$HOME/.jvs/.openclaw/openclaw.json" ]; then
    cp "$HOME/.jvs/.openclaw/openclaw.json" "$CONFIG_DIR/openclaw.json"
    echo "✅ 配置文件已复制"
elif [ -f "$HOME/.openclaw/openclaw.json" ]; then
    cp "$HOME/.openclaw/openclaw.json" "$CONFIG_DIR/openclaw.json"
    echo "✅ 配置文件已复制"
else
    echo "⚠️  未找到基础配置，需要手动配置"
fi

# 4. 修改端口
if [ -f "$CONFIG_DIR/openclaw.json" ]; then
    cat "$CONFIG_DIR/openclaw.json" | jq ".gateway.port = $PORT" > "$CONFIG_DIR/openclaw.json.tmp" && mv "$CONFIG_DIR/openclaw.json.tmp" "$CONFIG_DIR/openclaw.json"
    echo "✅ 端口已设置为：$PORT"
fi

# 5. 检测 Node 路径
NODE_PATH=$(which node 2>/dev/null || echo "/opt/homebrew/opt/node/bin/node")
echo "ℹ️  Node 路径：$NODE_PATH"

# 6. 创建 LaunchAgent plist（使用动态路径）
cat > "$PLIST_FILE" << PLISTEOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ai.openclaw.gateway-$INSTANCE_NAME</string>
    <key>Comment</key>
    <string>OpenClaw Gateway - $INSTANCE_NAME (port $PORT)</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>ThrottleInterval</key>
    <integer>1</integer>
    <key>Umask</key>
    <integer>63</integer>
    <key>ProgramArguments</key>
    <array>
        <string>$NODE_PATH</string>
        <string>-e</string>
        <string>require('child_process').execSync('openclaw gateway --port $PORT', {cwd: '$CONFIG_DIR', stdio: 'inherit', env: {...process.env, OPENCLAW_HOME: '$CONFIG_DIR'}})</string>
    </array>
    <key>StandardOutPath</key>
    <string>$CONFIG_DIR/logs/gateway.log</string>
    <key>StandardErrorPath</key>
    <string>$CONFIG_DIR/logs/gateway.err.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>HOME</key>
        <string>$HOME</string>
        <key>OPENCLAW_HOME</key>
        <string>$CONFIG_DIR</string>
        <key>OPENCLAW_GATEWAY_PORT</key>
        <string>$PORT</string>
    </dict>
</dict>
</plist>
PLISTEOF
echo "✅ LaunchAgent 已创建：$PLIST_FILE"

# 7. 加载并启动
launchctl load "$PLIST_FILE"
sleep 3
echo "✅ 网关已启动"

# 8. 验证
echo ""
echo "=== 验证 ==="
if lsof -i :$PORT | grep LISTEN > /dev/null 2>&1; then
    echo "✅ 网关运行在端口 $PORT"
    echo "📊 Dashboard: http://127.0.0.1:$PORT/"
else
    echo "⚠️  网关未启动，请检查日志：$CONFIG_DIR/logs/"
fi
