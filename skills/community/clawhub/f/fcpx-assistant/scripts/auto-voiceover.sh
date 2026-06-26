#!/bin/bash
# Auto Voice-Over - 简易单文件 TTS 配音（基于 edge-tts）
# 完整多段配音请用 tts-voiceover.sh

set -euo pipefail

# 默认参数
VOICE="zh-CN-YunxiNeural"
RATE="+0%"
OUTPUT_FILE=""
SCRIPT_TEXT=""
SCRIPT_FILE=""

usage() {
    cat << 'EOF'
用法：auto-voiceover.sh <文本> [输出文件]
      auto-voiceover.sh --file <文案文件> [--output out.wav]

选项：
  --file, -f       文案文件
  --voice          edge-tts 声音 (默认：zh-CN-YunxiNeural)
  --rate           语速调整 (如 +10%, -5%, 默认 +0%)
  --output, -o     输出文件 (默认：/tmp/voiceover-时间戳.wav)
  --list-voices    列出可用中文声音
  --help, -h       显示帮助

可用中文声音：
  zh-CN-YunxiNeural      男声，活泼阳光 (默认)
  zh-CN-YunjianNeural    男声，激情有力
  zh-CN-YunyangNeural    男声，专业新闻
  zh-CN-XiaoxiaoNeural   女声，温暖亲切
  zh-CN-XiaoyiNeural     女声，活泼可爱

💡 多段配音请用 tts-voiceover.sh
EOF
    exit 0
}

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --file|-f) SCRIPT_FILE="$2"; shift 2 ;;
        --voice) VOICE="$2"; shift 2 ;;
        --rate) RATE="$2"; shift 2 ;;
        --output|-o) OUTPUT_FILE="$2"; shift 2 ;;
        --list-voices) edge-tts --list-voices 2>/dev/null | grep 'zh-CN'; exit 0 ;;
        --help|-h) usage ;;
        *)
            if [[ -z "$SCRIPT_TEXT" ]]; then
                SCRIPT_TEXT="$1"
            elif [[ -z "$OUTPUT_FILE" ]]; then
                OUTPUT_FILE="$1"
            fi
            shift
            ;;
    esac
done

# 读取文件
if [[ -n "$SCRIPT_FILE" ]]; then
    if [[ ! -f "$SCRIPT_FILE" ]]; then
        echo "❌ 文件不存在：$SCRIPT_FILE"
        exit 1
    fi
    SCRIPT_TEXT=$(cat "$SCRIPT_FILE")
fi

if [[ -z "$SCRIPT_TEXT" ]]; then
    echo "❌ 用法：auto-voiceover.sh <文本> [输出文件]"
    echo "   或：auto-voiceover.sh --file <文案文件>"
    exit 1
fi

if [[ -z "$OUTPUT_FILE" ]]; then
    OUTPUT_FILE="/tmp/voiceover-$(date +%s).wav"
fi

# 检查依赖
if ! command -v edge-tts &>/dev/null; then
    echo "❌ edge-tts 未安装"
    echo "💡 安装：pipx install edge-tts"
    exit 1
fi

echo "🎙️ 自动配音生成器 (edge-tts)"
echo "📝 文本：${SCRIPT_TEXT:0:50}$([ ${#SCRIPT_TEXT} -gt 50 ] && echo '...')"
echo "🎤 声音：$VOICE"
echo "⚡ 语速：$RATE"
echo "📤 输出：$OUTPUT_FILE"
echo ""

# 生成临时 mp3
TEMP_MP3="/tmp/edge-tts-$(date +%s).mp3"
echo "🔊 正在生成语音..."

if ! edge-tts --voice "$VOICE" --rate "$RATE" --text "$SCRIPT_TEXT" --write-media "$TEMP_MP3" 2>/dev/null; then
    echo "❌ edge-tts 生成失败"
    exit 1
fi

# 转换为 wav + 修剪首尾静音
ffmpeg -y -i "$TEMP_MP3" \
    -af "silenceremove=start_periods=1:start_threshold=-40dB:start_duration=0.05,areverse,silenceremove=start_periods=1:start_threshold=-40dB:start_duration=0.05,areverse" \
    "$OUTPUT_FILE" \
    -loglevel warning 2>/dev/null

rm -f "$TEMP_MP3"

if [[ -f "$OUTPUT_FILE" ]]; then
    DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUTPUT_FILE" 2>/dev/null)
    SIZE=$(stat -f%z "$OUTPUT_FILE" 2>/dev/null | awk '{printf "%.1f", $1/1024}')

    echo ""
    echo "✅ 语音生成完成！"
    echo "   📁 文件：$OUTPUT_FILE"
    echo "   ⏱️ 时长：${DURATION}s"
    echo "   💾 大小：${SIZE}KB"
else
    echo "❌ 音频处理失败"
    exit 1
fi
