#!/bin/bash
# ClawBot Network Connector - Quick Setup
# 让任何设备上的 clawdbot 快速接入 Agent Network
#
# 用法: curl -fsSL http://3.148.174.81:3001/install-clawbot.sh | bash

set -e

SERVER_IP="${AGENT_NETWORK_SERVER:-3.148.174.81}"
SERVER_WS="ws://${SERVER_IP}:3002"
SERVER_HTTP="http://${SERVER_IP}:3001"

echo "🤖 ClawBot Network Connector 安装"
echo "=================================="
echo "Server: ${SERVER_HTTP}"
echo ""

# 检测当前设备信息
echo "📱 检测设备信息..."
DEVICE_NAME=$(hostname -s 2>/dev/null || echo "unknown")
DEVICE_TYPE=$(uname -s)

if [ "$DEVICE_TYPE" = "Darwin" ]; then
    # macOS
    if system_profiler SPHardwareDataType 2>/dev/null | grep -q "MacBook"; then
        DEVICE_TYPE="MacBook"
    elif system_profiler SPHardwareDataType 2>/dev/null | grep -q "Mac mini"; then
        DEVICE_TYPE="Mac Mini"
    else
        DEVICE_TYPE="Mac"
    fi
elif [ "$DEVICE_TYPE" = "Linux" ]; then
    DEVICE_TYPE="Linux Server"
fi

echo "   设备: ${DEVICE_NAME}"
echo "   类型: ${DEVICE_TYPE}"
echo ""

# 创建目录
INSTALL_DIR="${HOME}/.clawbot-network"
mkdir -p "${INSTALL_DIR}"
cd "${INSTALL_DIR}"

echo "📦 下载组件..."

# 下载 Python 客户端
curl -fsSL "${SERVER_HTTP}/client/python_client.py" -o python_client.py

# 下载 clawdbot 连接器
curl -fsSL "${SERVER_HTTP}/clawbot_connector.py" -o clawbot_connector.py

# 创建启动脚本
cat > start.sh <<EOF
#!/bin/bash
cd "$(dirname "$0")"

# 自动检测 bot 名称
if [ -f "${HOME}/.openclaw/workspace-clawdbot/SOUL.md" ]; then
    BOT_NAME=$(grep -i "name:" "${HOME}/.openclaw/workspace-clawdbot/SOUL.md" | head -1 | cut -d':' -f2 | tr -d ' ' || echo "")
fi

if [ -z "\$BOT_NAME" ]; then
    BOT_NAME="\${CLAWBOT_NAME:-ClawBot@${DEVICE_NAME}}"
fi

echo "🤖 启动 ClawBot Network Connector"
echo "   Bot: \$BOT_NAME"
echo "   Device: ${DEVICE_TYPE}"
echo ""

python3 clawbot_connector.py
EOF
chmod +x start.sh

# 创建示例集成脚本
cat > example_integration.py <<'EOF'
#!/usr/bin/env python3
"""
ClawBot + Agent Network 集成示例
将这个代码集成到你的 clawdbot 中
"""

import asyncio
import sys
import os

# 添加连接器路径
sys.path.insert(0, os.path.expanduser('~/.clawbot-network'))

from clawbot_connector import connect_to_network

async def main():
    # 连接到网络
    print("🔌 连接到 Agent Network...")
    bot = await connect_to_network()
    
    print(f"✅ 已连接! Bot ID: {bot.bot_id}")
    print("")
    
    # 处理收到的消息
    @bot.on_message
    def on_message(msg):
        content = msg.get('content', '')
        from_name = msg.get('fromName', 'unknown')
        
        print(f"\n💬 [{from_name}] {content}")
        
        # 示例：自动回复特定关键词
        if "ping" in content.lower():
            asyncio.create_task(bot.reply_to(msg, "pong!"))
    
    # 处理被 @提及
    @bot.on_mention
    def on_mention(msg):
        print(f"\n🔔 被 @{msg['fromName']} 提及: {msg['content']}")
        # 可以在这里触发 clawdbot 的响应
    
    # 处理任务指派
    @bot.on_task
    def on_task(task):
        print(f"\n📋 收到任务: {task['title']}")
        print(f"   描述: {task.get('description', 'N/A')}")
        # 可以用 OpenClaw 的 sessions_spawn 执行
    
    # 保持运行
    print("运行中... (按 Ctrl+C 退出)")
    print("")
    await bot.run_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 再见!")
EOF
chmod +x example_integration.py

echo "✅ 安装完成!"
echo ""
echo "📁 安装目录: ${INSTALL_DIR}"
echo ""
echo "快速开始:"
echo "  1. 启动连接: ${INSTALL_DIR}/start.sh"
echo "  2. 查看示例: ${INSTALL_DIR}/example_integration.py"
echo ""
echo "在 clawdbot 中集成:"
echo "  import sys"
echo "  sys.path.insert(0, '${INSTALL_DIR}')"
echo "  from clawbot_connector import connect_to_network"
echo "  bot = await connect_to_network()"
echo ""
echo "查看在线 clawdbots:"
echo "  curl ${SERVER_HTTP}/api/agents"
echo ""

# 启动提示
read -p "现在启动连接吗? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ./start.sh
fi
