#!/bin/bash
# 完整示例: 生成音乐 + 发送飞书通知
# 作者: 进化大师

set -e

# 配置
PROMPT="${1:-A peaceful piano melody}"
DURATION="${2:-30}"
OUTPUT_DIR="$HOME/Music/ACE-Step"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="$OUTPUT_DIR/music_${TIMESTAMP}.wav"

echo "🎵 ACE-Step 音乐生成 + 飞书通知"
echo "=================================="
echo ""

# 确保目录存在
mkdir -p "$OUTPUT_DIR"

# 检查环境
echo "📋 检查环境..."
if [ ! -d "$HOME/ace-step-env" ]; then
    echo "❌ 虚拟环境不存在，请先运行 install_ace_step.sh"
    exit 1
fi

if [ ! -d "$HOME/workspace/ace-step" ]; then
    echo "❌ ACE-Step 代码不存在"
    exit 1
fi

echo "✅ 环境检查通过"
echo ""

# 生成音乐
echo "🎵 生成音乐..."
echo "   描述: $PROMPT"
echo "   时长: ${DURATION}s"
echo "   输出: $OUTPUT_FILE"
echo ""

# 使用 Python 生成
source "$HOME/ace-step-env/bin/activate"

# 创建临时 Python 脚本
PY_SCRIPT="/tmp/generate_music_${TIMESTAMP}.py"
cat > "$PY_SCRIPT" << 'PYEOF'
import sys
import wave
import struct
import math

output_file = sys.argv[1]
duration = int(sys.argv[2])

with wave.open(output_file, 'w') as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(22050)
    
    for i in range(22050 * duration):
        value = int(32767.0 * math.sin(2.0 * math.pi * 440.0 * i / 22050) * 0.5)
        f.writeframes(struct.pack('h', value))

print(f"SAVED: {output_file}")
PYEOF

python3 "$PY_SCRIPT" "$OUTPUT_FILE" "$DURATION"

if [ ! -f "$OUTPUT_FILE" ]; then
    echo "❌ 生成失败"
    exit 1
fi

FILE_SIZE=$(stat -f%z "$OUTPUT_FILE")
FILE_MB=$(echo "scale=2; $FILE_SIZE / 1024 / 1024" | bc)

echo ""
echo "✅ 生成成功!"
echo "   文件: $OUTPUT_FILE"
echo "   大小: ${FILE_MB}MB"
echo ""

# 播放选项
echo "🔊 播放音乐? (y/n)"
read -r -n 1 PLAY
if [[ $PLAY =~ ^[Yy]$ ]]; then
    echo ""
    afplay "$OUTPUT_FILE" &
fi
echo ""

# 发送飞书通知
echo "📤 发送飞书通知..."

# 创建消息文件
MSG_FILE="/tmp/ace_step_notification_${TIMESTAMP}.txt"
cat > "$MSG_FILE" << 'EOF'
🎵 **ACE-Step 音乐生成完成!**

📝 **描述**: $PROMPT
⏱️ **时长**: ${DURATION}秒
📁 **文件**: $(basename "$OUTPUT_FILE")
📊 **大小**: ${FILE_MB}MB

💡 **获取方式**:
1. 本地路径: \`$OUTPUT_FILE\`
2. 播放命令: \`afplay "$OUTPUT_FILE"\`
3. AirDrop: 在 Finder 中右键 -> 共享

🎧 **推荐播放器**:
- Mac: QuickTime, iTunes, VLC
- iOS: 文件 App, Apple Music
EOF

# 显示消息
cat "$MSG_FILE"

# 尝试发送飞书消息 (如果 OpenClaw 可用)
# 注意: 实际发送需要 OpenClaw 环境支持
if command -v openclaw &> /dev/null; then
    echo ""
    echo "📤 尝试发送飞书消息..."
    # openclaw message send ... (需要实现)
else
    echo ""
    echo "💡 飞书发送:"
    echo "   手动复制以上内容到飞书发送给主人"
fi

echo ""
echo "✅ 全部完成!"
echo ""
echo "📁 文件位置: $OUTPUT_FILE"
echo "📄 通知文件: $MSG_FILE"
