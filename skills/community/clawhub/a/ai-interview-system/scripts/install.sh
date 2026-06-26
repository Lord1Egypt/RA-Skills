#!/bin/bash
# AI 面试系统安装脚本

set -e

echo "🤖 AI 面试系统安装向导"
echo "======================"

# 检查 OpenClaw 是否安装
if ! command -v openclaw &> /dev/null; then
    echo "❌ OpenClaw 未安装，请先安装 OpenClaw"
    exit 1
fi

# 创建工作空间
echo "📁 创建 Agent 工作空间..."
mkdir -p ~/.openclaw/workspace-job-seeker
mkdir -p ~/.openclaw/workspace-recruiter

# 复制配置模板
echo "📋 复制配置模板..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$SCRIPT_DIR/config"

if [ -f "$CONFIG_DIR/job-seeker/IDENTITY.md" ]; then
    cp "$CONFIG_DIR/job-seeker/IDENTITY.md" ~/.openclaw/workspace-job-seeker/IDENTITY.md
    echo "✅ job-seeker 配置已创建"
fi

if [ -f "$CONFIG_DIR/recruiter/IDENTITY.md" ]; then
    cp "$CONFIG_DIR/recruiter/IDENTITY.md" ~/.openclaw/workspace-recruiter/IDENTITY.md
    echo "✅ recruiter 配置已创建"
fi

# 提示用户配置飞书应用
echo ""
echo "📝 下一步："
echo "1. 在飞书开放平台创建两个应用"
echo "2. 编辑 ~/.openclaw/openclaw.json 添加配置"
echo "3. 运行 openclaw gateway start 启动服务"
echo ""
echo "详细说明请查看 SKILL.md"
echo ""

# 启动可视化面板（可选）
read -p "是否启动可视化面板？(y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 启动可视化面板..."
    cd "$SCRIPT_DIR"
    python3 server.py &
    echo "✅ 可视化面板已启动，访问 http://localhost:8091"
fi

echo ""
echo "🎉 安装完成！"
