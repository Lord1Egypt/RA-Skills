#!/bin/bash
# Agent P2P Skill 本地安装脚本

set -e

echo "🦞 Agent P2P Skill 安装脚本"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 需要 Python 3，请先安装"
    exit 1
fi

echo "[1/3] 创建 Python 虚拟环境..."
cd "$(dirname "$0")"
python3 -m venv venv
echo "✅ 虚拟环境创建完成"

echo ""
echo "[2/3] 安装依赖..."
venv/bin/pip install --upgrade pip -q
venv/bin/pip install websockets websocket-client requests psutil -q
echo "✅ 依赖安装完成"

echo ""
echo "[3/3] 配置 systemd 服务..."

# 创建 systemd 服务文件
mkdir -p ~/.config/systemd/user

cat > ~/.config/systemd/user/agent-p2p-bridge.service << EOF
[Unit]
Description=Agent P2P Bridge (Python)
After=network.target

[Service]
Type=simple
WorkingDirectory=%h/.openclaw/workspace/skills/agent-p2p
ExecStart=%h/.openclaw/workspace/skills/agent-p2p/venv/bin/python3 local/bridge.py
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable agent-p2p-bridge.service
echo "✅ systemd 服务配置完成"

echo ""
echo "🎉 安装完成！"
echo ""
echo "使用方法："
echo "  1. 配置环境变量：编辑 ~/.openclaw/gateway.env"
echo "  2. 启动服务：systemctl --user start agent-p2p-bridge"
echo "  3. 查看状态：systemctl --user status agent-p2p-bridge"
echo "  4. 发送消息：python3 send.py -m '消息' -t <联系人ID>"
echo "  5. 发送文件：python3 send.py -f <文件> -t <联系人ID>"
echo ""
echo "详细配置请参考 CONFIG.md"
