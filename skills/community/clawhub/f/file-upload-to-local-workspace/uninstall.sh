#!/bin/bash
# file-upload skill 卸载脚本

set -e

WORKSPACE="${HOME}/.openclaw/workspace"

echo "╔═══════════════════════════════════════════════════════╗"
║     OpenClaw File Upload Skill 卸载                         ║"
echo "╚═══════════════════════════════════════════════════════╝"

# 停止服务
if systemctl is-active --quiet openclaw-upload.service 2>/dev/null; then
    echo "⏹️  停止 systemd 服务..."
    systemctl stop openclaw-upload.service
    systemctl disable openclaw-upload.service
    rm -f /etc/systemd/system/openclaw-upload.service
    systemctl daemon-reload
    echo "✅ systemd 服务已卸载"
else
    echo "⏹️  停止后台进程..."
    pkill -f "node upload-server.js" || true
    echo "✅ 后台进程已停止"
fi

# 删除文件
echo "🗑️  删除文件..."
rm -f "${WORKSPACE}/upload-server.js"
rm -f "${WORKSPACE}/upload.html"
rm -f "${WORKSPACE}/upload-server.log"

echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║     卸载完成！                                        ║"
echo "╠═══════════════════════════════════════════════════════╣"
echo "║  已删除：                                             ║"
echo "║  - upload-server.js                                   ║"
echo "║  - upload.html                                        ║"
echo "║  - upload-server.log                                  ║"
echo "║  - systemd 服务配置                                   ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""
echo "💡 如需重新安装，运行："
echo "   openclaw skills install file-upload"
echo ""
