#!/bin/bash

# 飞书语音回复技能安装脚本

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  飞书语音回复技能 安装"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 检查 Python
echo "📦 检查 Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python 3，请先安装"
    exit 1
fi
echo "   ✅ Python 3 已安装: $(python3 --version)"
echo ""

# 安装 edge-tts
echo "📦 安装 edge-tts..."
pip3 install edge-tts -i https://pypi.tuna.tsinghua.edu.cn/simple

# 验证安装
echo ""
echo "🔍 验证安装..."
python3 -c "import edge_tts; print('   ✅ edge-tts 安装成功')" || {
    echo "❌ edge-tts 安装失败"
    exit 1
}
echo ""

# 测试语音生成
echo "🎙️  测试语音生成..."
python3 edge_tts_async.py "测试" xiaoxiao test-voice.mp3

if [ -f "test-voice.mp3" ]; then
    echo "   ✅ 语音生成测试成功"
    rm -f test-voice.mp3
else
    echo "❌ 语音生成测试失败"
    exit 1
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 安装完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📚 使用方法："
echo "   python3 edge_tts_async.py \"你好，世界！\" xiaoxiao voice.mp3"
echo ""
echo "📖 文档："
echo "   cat SKILL.md"
echo "   cat README.md"
echo ""
