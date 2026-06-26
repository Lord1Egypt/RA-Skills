#!/bin/bash
# gateway-restart.sh - 重启网关

INSTANCE="$1"

if [ -z "$INSTANCE" ]; then
    echo "用法：gateway-restart.sh <实例名|all>"
    echo ""
    echo "实例名:"
    echo "  local-shrimp / 本地虾 → ~/.jvs/.openclaw/"
    echo "  feishu / 飞书 → ~/.openclaw/"
    echo "  all → 重启所有网关"
    exit 1
fi

restart_gateway() {
    local instance_name="$1"
    local config_dir="$2"
    local plist="$3"
    
    echo "🔄 重启 $instance_name..."
    
    if [ -f "$plist" ]; then
        launchctl kickstart -k gui/$(id -u)/$(basename "$plist" .plist)
        sleep 2
        echo "✅ $instance_name 已重启 (LaunchAgent)"
    else
        echo "⚠️  未找到 LaunchAgent: $plist"
        echo "尝试手动重启..."
        OPENCLAW_HOME="$config_dir" openclaw gateway restart
    fi
}

case "$INSTANCE" in
    all)
        restart_gateway "本地虾" "$HOME/.jvs/.openclaw" "$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist"
        echo ""
        restart_gateway "飞书机器人" "$HOME/.openclaw" "$HOME/Library/LaunchAgents/ai.openclaw.gateway-feishu.plist"
        ;;
    local-shrimp|本地虾 |18789|local)
        restart_gateway "本地虾" "$HOME/.jvs/.openclaw" "$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist"
        ;;
    feishu|飞书|18790|fly)
        restart_gateway "飞书机器人" "$HOME/.openclaw" "$HOME/Library/LaunchAgents/ai.openclaw.gateway-feishu.plist"
        ;;
    *)
        echo "❌ 未知实例名：$INSTANCE"
        exit 1
        ;;
esac

echo ""
echo "=== 验证状态 ==="
sleep 2
lsof -i -n -P | grep LISTEN | grep "node" | grep "openclaw" | awk -F: '{print "✅ 端口: " $2}' | awk '{print $1}'
