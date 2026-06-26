#!/bin/bash
# Edge TTS Skill 安装脚本

set -e

echo "🎤 Edge TTS Skill 安装脚本"
echo "=========================="

# 检查 OpenClaw 是否已安装
if ! command -v openclaw &> /dev/null; then
    echo "❌ 错误：未找到 openclaw 命令"
    echo "请先安装 OpenClaw: npm install -g openclaw"
    exit 1
fi

echo "✅ 检测到 OpenClaw"

# 应用配置
echo "📝 应用 Edge TTS 配置..."
openclaw config set messages.tts.provider edge
openclaw config set messages.tts.auto always
openclaw config set messages.tts.providers.edge.enabled true
openclaw config set messages.tts.providers.edge.voice zh-CN-XiaoxiaoNeural

echo "✅ 配置完成"

# 重启 Gateway
echo "🔄 重启 Gateway..."
openclaw gateway restart

echo ""
echo "🎉 Edge TTS 安装完成！"
echo ""
echo "测试方法："
echo "1. 打开 Control UI 或消息频道"
echo "2. 发送一条消息"
echo "3. AI 的回复会自动转换为语音"
echo ""
echo "如需更换语音，运行："
echo "  openclaw config set messages.tts.providers.edge.voice <语音 ID>"
echo ""
echo "可用语音参考 SKILL.md 文件"
