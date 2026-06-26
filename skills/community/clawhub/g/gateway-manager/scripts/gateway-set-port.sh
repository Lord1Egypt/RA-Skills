#!/bin/bash
# gateway-set-port.sh - 修改网关端口

INSTANCE="$1"
NEW_PORT="$2"

if [ -z "$INSTANCE" ] || [ -z "$NEW_PORT" ]; then
    echo "用法：gateway-set-port.sh <实例名> <新端口>"
    echo ""
    echo "实例名别名:"
    echo "  local-shrimp / 本地虾 / 18789 → ~/.jvs/.openclaw/"
    echo "  feishu / 飞书 / 18790 → ~/.openclaw/"
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
        echo "可用：local-shrimp, 本地虾，feishu, 飞书"
        exit 1
        ;;
esac

echo "🔧 修改 $INSTANCE_NAME 端口 → $NEW_PORT"
echo ""

# 1. 检查端口是否被占用
if lsof -i :$NEW_PORT > /dev/null 2>&1; then
    echo "❌ 端口 $NEW_PORT 已被占用"
    lsof -i :$NEW_PORT
    exit 1
fi
echo "✅ 端口 $NEW_PORT 可用"

# 2. 修改配置文件
CONFIG_FILE="$CONFIG_DIR/openclaw.json"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ 配置文件不存在：$CONFIG_FILE"
    exit 1
fi

# 备份原配置
cp "$CONFIG_FILE" "$CONFIG_FILE.backup.$(date +%Y%m%d%H%M%S)"

# 修改端口
cat "$CONFIG_FILE" | jq ".gateway.port = $NEW_PORT" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
echo "✅ 配置文件已更新：$CONFIG_FILE"

# 同步到嵌套配置（如果有）
if [ -d "$CONFIG_DIR/.openclaw" ]; then
    cp "$CONFIG_FILE" "$CONFIG_DIR/.openclaw/openclaw.json"
    echo "✅ 嵌套配置已同步"
fi

# 3. 修改 LaunchAgent plist
if [ -f "$PLIST_FILE" ]; then
    plutil -replace ProgramArguments.6 -string "$NEW_PORT" "$PLIST_FILE"
    plutil -replace EnvironmentVariables.OPENCLAW_GATEWAY_PORT -string "$NEW_PORT" "$PLIST_FILE"
    echo "✅ LaunchAgent 已更新：$PLIST_FILE"
else
    echo "⚠️  未找到 LaunchAgent plist: $PLIST_FILE"
fi

# 4. 重启网关
echo ""
echo "🔄 重启网关..."
launchctl kickstart -k gui/$(id -u)/$(basename "$PLIST_FILE" .plist) 2>/dev/null || echo "⚠️  LaunchAgent 重启失败，尝试手动重启"
sleep 3

# 5. 验证
echo ""
if lsof -i :$NEW_PORT | grep LISTEN > /dev/null 2>&1; then
    echo "✅ 网关已在端口 $NEW_PORT 运行"
    echo ""
    echo "📊 Dashboard: http://127.0.0.1:$NEW_PORT/"
else
    echo "⚠️  网关未在端口 $NEW_PORT 监听"
    echo "请手动执行：OPENCLAW_HOME=$CONFIG_DIR openclaw gateway restart"
fi
