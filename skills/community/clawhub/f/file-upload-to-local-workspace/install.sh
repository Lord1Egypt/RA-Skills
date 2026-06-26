#!/bin/bash
# file-upload skill 安装脚本

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${HOME}/.openclaw/workspace"
CONFIG_FILE="${HOME}/.openclaw/openclaw.json"

echo "╔═══════════════════════════════════════════════════════╗"
echo "║     OpenClaw File Upload Skill 安装                   ║"
echo "╚═══════════════════════════════════════════════════════╝"

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误：需要安装 Node.js"
    exit 1
fi

echo "✅ Node.js 版本：$(node -v)"

# 复制文件到 workspace
echo "📦 复制文件到 workspace..."
cp "${SKILL_DIR}/src/upload-server.js" "${WORKSPACE}/upload-server.js"
cp "${SKILL_DIR}/src/upload.html" "${WORKSPACE}/upload.html"
chmod +x "${WORKSPACE}/upload-server.js"

# 读取 Gateway 认证信息
echo "🔐 读取 Gateway 认证配置..."
AUTH_VALUE=""

if [ -f "${CONFIG_FILE}" ]; then
    # 尝试读取 token
    GATEWAY_TOKEN=$(grep -o '"token": *"[^"]*"' "${CONFIG_FILE}" 2>/dev/null | head -1 | cut -d'"' -f4)
    
    # 尝试读取 password（如果没有 token）
    GATEWAY_PASSWORD=$(grep -o '"password": *"[^"]*"' "${CONFIG_FILE}" 2>/dev/null | head -1 | cut -d'"' -f4)
    
    # 检查认证模式
    AUTH_MODE=$(grep -o '"mode": *"[^"]*"' "${CONFIG_FILE}" 2>/dev/null | head -1 | cut -d'"' -f4)
    
    if [ -n "${GATEWAY_TOKEN}" ]; then
        echo "✅ 认证模式：Token"
        echo "✅ 已找到 Gateway Token"
        AUTH_VALUE="${GATEWAY_TOKEN}"
    elif [ -n "${GATEWAY_PASSWORD}" ]; then
        echo "✅ 认证模式：Password"
        echo "✅ 已找到 Gateway Password"
        AUTH_VALUE="${GATEWAY_PASSWORD}"
    else
        echo "⚠️  未找到认证配置，将使用空认证"
        echo "💡 建议配置 gateway.auth.token 或 gateway.auth.password"
        AUTH_VALUE=""
    fi
else
    echo "⚠️  未找到配置文件，将使用空认证"
    echo "💡 建议配置 gateway.auth.token 或 gateway.auth.password"
    AUTH_VALUE=""
fi

# 创建 uploads 目录
echo "📂 创建上传目录..."
mkdir -p "${WORKSPACE}/uploads"

# 创建 systemd 服务文件（可选）
if [ -d "/etc/systemd/system" ]; then
    echo "🔧 创建 systemd 服务..."
    cat > /etc/systemd/system/openclaw-upload.service << EOF
[Unit]
Description=OpenClaw File Upload Service
After=network.target

[Service]
Type=simple
User=${USER}
WorkingDirectory=${WORKSPACE}
Environment=UPLOAD_PORT=15170
Environment=WORKSPACE=${WORKSPACE}
Environment=GATEWAY_AUTH_VALUE=${AUTH_VALUE}
ExecStart=/usr/bin/node ${WORKSPACE}/upload-server.js
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
    
    systemctl daemon-reload
    systemctl enable openclaw-upload.service
    systemctl start openclaw-upload.service
    
    echo "✅ systemd 服务已创建并启动"
else
    # 直接启动服务
    echo "🚀 启动上传服务..."
    cd "${WORKSPACE}"
    nohup env UPLOAD_PORT=15170 WORKSPACE="${WORKSPACE}" GATEWAY_AUTH_VALUE="${AUTH_VALUE}" \
        node upload-server.js > upload-server.log 2>&1 &
    echo "✅ 上传服务已启动（后台运行）"
fi

# 获取服务器 IP
SERVER_IP=$(hostname -I | awk '{print $1}')

echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║     安装完成！                                        ║"
echo "╠═══════════════════════════════════════════════════════╣"
echo "║  上传页面：http://${SERVER_IP}:15170/                    ║"
if [ -n "${AUTH_VALUE}" ]; then
    echo "║  认证方式：Token/Password 已配置                        ║"
else
    echo "║  认证方式：无（建议配置认证）                            ║"
fi
echo "║                                                       ║"
echo "║  完整 URL: http://${SERVER_IP}:15170/?token=xxx         ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""
echo "📝 使用说明："
echo "  1. 访问上传页面"
echo "  2. 拖拽或选择文件上传"
echo "  3. 文件保存在：${WORKSPACE}/uploads/"
echo ""
echo "🔧 管理命令："
echo "  启动：systemctl start openclaw-upload"
echo "  停止：systemctl stop openclaw-upload"
echo "  重启：systemctl restart openclaw-upload"
echo "  日志：journalctl -u openclaw-upload -f"
echo ""
echo "🔐 认证说明："
if [ -n "${AUTH_VALUE}" ]; then
    echo "  - 使用 Gateway 配置的 token/password"
    echo "  - URL 参数：?token=<你的 token 或 password>"
else
    echo "  - 当前无认证保护"
    echo "  - 建议配置：openclaw config set gateway.auth.token <随机 token>"
fi
echo ""
