#!/bin/bash
# Gateway Keepalive - 安装脚本
# 作者: 康妃 (config)
# 版本: 1.1.0

set -e

echo "🦞 Gateway Keepalive 安装"
echo "========================"
echo ""

# 检查是否为 macOS
if [[ "$(uname)" != "Darwin" ]]; then
    echo "❌ 此技能仅支持 macOS"
    exit 1
fi

# 检查 OpenClaw 是否已安装
if ! command -v openclaw &> /dev/null; then
    echo "❌ OpenClaw 未安装"
    exit 1
fi

# 创建目录
echo "📁 创建目录..."
mkdir -p ~/.openclaw/backups/golden-config
mkdir -p ~/.openclaw/logs
mkdir -p ~/.openclaw/state
mkdir -p ~/.openclaw/scripts

# 创建黄金备份
if [ ! -f ~/.openclaw/backups/golden-config/openclaw.json ]; then
    echo "📦 创建黄金备份..."
    cp ~/.openclaw/openclaw.json ~/.openclaw/backups/golden-config/openclaw.json

    cat > ~/.openclaw/backups/golden-config/metadata.json <<EOF
{
  "created_at": "$(date -Iseconds)",
  "description": "黄金备份 - 已验证可用的稳定配置",
  "verified": true
}
EOF
else
    echo "✅ 黄金备份已存在"
fi

# 复制健康检测脚本
echo "📋 安装健康检测脚本..."
SCRIPT_DIR="$(dirname "$0")"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

if [ -f "$SKILL_DIR/../scripts/health-check-recovery.sh" ]; then
    cp "$SKILL_DIR/../scripts/health-check-recovery.sh" ~/.openclaw/scripts/
else
    echo "⚠️ 健康检测脚本不存在，请手动复制"
fi

chmod +x ~/.openclaw/scripts/health-check-recovery.sh 2>/dev/null || true

# 创建配置文件（如果不存在）
mkdir -p ~/.openclaw/config
if [ ! -f ~/.openclaw/config/keepalive.conf ]; then
    echo "📝 创建配置文件..."
    cp ~/.openclaw/skills/gateway-keepalive/config/keepalive.conf.example ~/.openclaw/config/keepalive.conf

    # 询问是否配置 Telegram 通知
    echo ""
    echo "📱 Telegram 通知配置（可选）"
    echo "是否要配置 Telegram 通知？(y/N)"
    read -r RESPONSE

    if [[ $RESPONSE =~ ^[Yy]$ ]]; then
        echo "请输入 Telegram Bot Token (格式: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz):"
        read -r BOT_TOKEN

        echo "请输入 Telegram Chat ID (格式: 123456789):"
        read -r CHAT_ID

        # 更新配置文件
        cat > ~/.openclaw/config/keepalive.conf <<EOF
# OpenClaw Keepalive 配置文件
# 由安装脚本自动生成于 $(date '+%Y-%m-%d %H:%M:%S')

# Telegram 通知配置
TELEGRAM_BOT_TOKEN="$BOT_TOKEN"
TELEGRAM_CHAT_ID="$CHAT_ID"
EOF

        echo "✅ Telegram 通知已配置"
    else
        echo "⏭️  跳过 Telegram 配置（可稍后编辑 ~/.openclaw/config/keepalive.conf）"
    fi
fi

# 创建 Gateway LaunchAgent
echo "🔧 创建 Gateway LaunchAgent..."
USERNAME=$(whoami)

cat > ~/Library/LaunchAgents/ai.openclaw.gateway.plist <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>ai.openclaw.gateway</string>
    <key>Comment</key>
    <string>OpenClaw Gateway (v2026.3.2)</string>
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
      <string>/opt/homebrew/opt/node/bin/node</string>
      <string>/opt/homebrew/lib/node_modules/openclaw/dist/index.js</string>
      <string>gateway</string>
      <string>--port</string>
      <string>18789</string>
    </array>
    <key>StandardOutPath</key>
    <string>/Users/$USERNAME/.openclaw/logs/gateway.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/$USERNAME/.openclaw/logs/gateway.err.log</string>
    <key>EnvironmentVariables</key>
    <dict>
      <key>HOME</key>
      <string>/Users/$USERNAME</string>
      <key>PATH</key>
      <string>/Users/$USERNAME/.local/bin:/Users/$USERNAME/.npm-global/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
    </dict>
  </dict>
</plist>
EOF

# 创建健康检测 LaunchAgent
echo "🔧 创建健康检测 LaunchAgent..."
cat > ~/Library/LaunchAgents/com.openclaw.health-check.plist <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.health-check</string>
    <key>Comment</key>
    <string>OpenClaw 自动健康检测与恢复服务</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/$USERNAME/.openclaw/scripts/health-check-recovery.sh</string>
    </array>
    <key>StartInterval</key>
    <integer>60</integer>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/$USERNAME/.openclaw/logs/health-check.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/$USERNAME/.openclaw/logs/health-check.err.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
    </dict>
</dict>
</plist>
EOF

# 加载 LaunchAgents
echo "🚀 加载 LaunchAgents..."

# 停止旧服务（如果存在）
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist 2>/dev/null || true
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.openclaw.health-check.plist 2>/dev/null || true

# 加载新服务
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.openclaw.health-check.plist

echo ""
echo "✅ 安装完成！"
echo ""
echo "📊 验证安装："
echo "  launchctl list | grep openclaw"
echo ""
echo "📋 查看日志："
echo "  tail -f ~/.openclaw/logs/health-recovery.log"
