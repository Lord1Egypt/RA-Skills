#!/usr/bin/env bash
# 🦞 API Logger 一键安装脚本
# 用法: bash install.sh

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$HOME/.openclaw/workspace/company/api-proxy"
LOG_DIR="$HOME/.openclaw/workspace/company/api-logs"
PLIST_PATH="$HOME/Library/LaunchAgents/com.lobster.api-proxy.plist"
PROXY_PORT=18790
UPSTREAM="http://model.mify.ai.srv/anthropic"

echo ""
echo "🦞 开始安装 API Logger..."
echo ""

# 1. 创建安装目录
echo "📁 创建安装目录: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

# 2. 复制 proxy.py 和 log_viewer.py
echo "📋 复制代理服务文件..."
cp "$SKILL_DIR/proxy.py" "$INSTALL_DIR/proxy.py"
cp "$SKILL_DIR/log_viewer.py" "$INSTALL_DIR/log_viewer.py"
echo "   ✓ proxy.py → $INSTALL_DIR/proxy.py"
echo "   ✓ log_viewer.py → $INSTALL_DIR/log_viewer.py"

# 3. 创建日志目录
echo "📁 创建日志目录: $LOG_DIR"
mkdir -p "$LOG_DIR"

# 4. 检查 aiohttp 依赖
echo "🔍 检查 Python 依赖..."
if ! python3 -c "import aiohttp" 2>/dev/null; then
    echo "   ⚠️  未检测到 aiohttp，正在安装..."
    pip3 install aiohttp --quiet
    echo "   ✓ aiohttp 已安装"
else
    echo "   ✓ aiohttp 已就绪"
fi

# 5. 写入 LaunchAgent plist
echo "⚙️  写入 LaunchAgent plist: $PLIST_PATH"
mkdir -p "$HOME/Library/LaunchAgents"
cat > "$PLIST_PATH" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.lobster.api-proxy</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>${INSTALL_DIR}/proxy.py</string>
        <string>--port</string>
        <string>${PROXY_PORT}</string>
        <string>--upstream</string>
        <string>${UPSTREAM}</string>
        <string>--log-dir</string>
        <string>${LOG_DIR}</string>
    </array>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>

    <key>StandardOutPath</key>
    <string>${LOG_DIR}/proxy.stdout.log</string>

    <key>StandardErrorPath</key>
    <string>${LOG_DIR}/proxy.stderr.log</string>

    <key>WorkingDirectory</key>
    <string>${INSTALL_DIR}</string>
</dict>
</plist>
EOF
echo "   ✓ plist 已写入"

# 6. 加载 LaunchAgent（先卸载再加载，避免重复）
echo "🚀 启动代理服务..."
launchctl unload "$PLIST_PATH" 2>/dev/null || true
launchctl load "$PLIST_PATH"
echo "   ✓ 服务已启动"

# 7. 等待一秒，检查服务是否正常
sleep 1
if launchctl list | grep -q "com.lobster.api-proxy"; then
    echo "   ✓ 服务运行正常（端口 $PROXY_PORT）"
else
    echo "   ⚠️  服务可能未正常启动，请检查日志：$LOG_DIR/proxy.stderr.log"
fi

echo ""
echo "========================================"
echo "✅ API Logger 安装完成！"
echo ""
echo "⚠️  还需要手动完成以下配置："
echo ""
echo "1. 修改 openclaw.json 中的 baseUrl："
echo "   文件路径：~/.openclaw/openclaw.json"
echo "   找到你使用的 provider，将 baseUrl 改为："
echo "   \"baseUrl\": \"http://127.0.0.1:${PROXY_PORT}/anthropic\""
echo ""
echo "2. 确认代理上游地址正确："
echo "   文件路径：${INSTALL_DIR}/proxy.py"
echo "   找到 --upstream 参数默认值，改为你的实际模型 API 地址。"
echo "   当前默认值：${UPSTREAM}"
echo ""
echo "3. 修改完成后，请与用户确认后再重启 Gateway："
echo "   openclaw gateway restart"
echo ""
echo "代理服务已在后台运行，端口 ${PROXY_PORT}。"
echo "日志路径：${LOG_DIR}/"
echo "========================================"
echo ""
echo "💡 查看日志使用方法："
echo "   python3 ${INSTALL_DIR}/log_viewer.py"
echo "   python3 ${INSTALL_DIR}/log_viewer.py --stats"
echo "   python3 ${INSTALL_DIR}/log_viewer.py --last 5"
echo ""
