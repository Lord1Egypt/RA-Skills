#!/bin/bash
# Multi-language Subtitle Generator
# 使用 Whisper 转录 → 生成 SRT 字幕 → 可选翻译
# Whisper 直接输出带时间戳的 SRT，比旧版 ASR 精准得多

set -euo pipefail

VIDEO_FILE="${1:-}"
TARGET_LANG="${2:-en}"
WHISPER_MODEL="${3:-turbo}"

if [[ -z "$VIDEO_FILE" ]]; then
    echo "❌ 用法：multi-lang-subtitles.sh <视频文件> [目标语言] [whisper模型]"
    echo "   目标语言：en, ja, ko, fr, de, es (默认：en)"
    echo "   whisper模型：tiny, base, small, medium, large, turbo (默认：turbo)"
    echo ""
    echo "示例："
    echo "   multi-lang-subtitles.sh video.mp4"
    echo "   multi-lang-subtitles.sh video.mp4 ja"
    echo "   multi-lang-subtitles.sh video.mp4 en medium"
    exit 1
fi

if [[ ! -f "$VIDEO_FILE" ]]; then
    echo "❌ 文件不存在：$VIDEO_FILE"
    exit 1
fi

# 检查依赖
if ! command -v whisper &>/dev/null; then
    echo "❌ whisper 未安装"
    echo "💡 安装：brew install openai-whisper"
    exit 1
fi

OUTPUT_CN="${VIDEO_FILE%.*}-zh.srt"
OUTPUT_TRANSLATED="${VIDEO_FILE%.*}-${TARGET_LANG}.srt"

echo "🌍 多语言字幕生成器 (Whisper)"
echo "📁 视频：$VIDEO_FILE"
echo "🤖 模型：$WHISPER_MODEL"
echo "🎯 目标语言：$TARGET_LANG"
echo ""

# Step 1: 提取音频
echo "🎵 步骤 1: 提取音频..."
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

AUDIO_FILE="$TEMP_DIR/audio.wav"
ffmpeg -y -i "$VIDEO_FILE" -vn -acodec pcm_s16le -ar 16000 -ac 1 "$AUDIO_FILE" -loglevel error 2>/dev/null

if [[ ! -f "$AUDIO_FILE" ]]; then
    echo "❌ 音频提取失败"
    exit 1
fi

AUDIO_DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$AUDIO_FILE" 2>/dev/null)
echo "   ✅ 音频提取完成 (${AUDIO_DUR}s)"

# Step 2: Whisper 转录 → 直接生成 SRT
echo "🎤 步骤 2: 语音识别 (Whisper $WHISPER_MODEL)..."
echo "   ⏳ 转录中，请稍候..."

whisper "$AUDIO_FILE" \
    --model "$WHISPER_MODEL" \
    --language zh \
    --output_format srt \
    --output_dir "$TEMP_DIR" \
    2>&1 | grep -v "UserWarning\|warnings.warn" || true

SRT_FILE="$TEMP_DIR/audio.srt"

if [[ ! -f "$SRT_FILE" ]] || [[ ! -s "$SRT_FILE" ]]; then
    echo "❌ 语音识别失败或无语音内容"
    exit 1
fi

# 统计字幕条数
SUB_COUNT=$(grep -c '^[0-9]\+$' "$SRT_FILE" 2>/dev/null || echo "0")
echo "   ✅ 识别完成 ($SUB_COUNT 条字幕)"

# 预览前几条
echo "   📝 预览："
head -12 "$SRT_FILE" | sed 's/^/      /'
echo ""

# Step 3: 保存中文字幕
echo "📝 步骤 3: 保存中文字幕..."
cp "$SRT_FILE" "$OUTPUT_CN"
echo "   ✅ 中文字幕：$OUTPUT_CN"
echo ""

# Step 4: 翻译（使用 Whisper translate 功能，仅支持翻译到英文）
if [[ "$TARGET_LANG" == "en" ]]; then
    echo "🌐 步骤 4: 翻译到英文 (Whisper translate)..."
    
    whisper "$AUDIO_FILE" \
        --model "$WHISPER_MODEL" \
        --task translate \
        --output_format srt \
        --output_dir "$TEMP_DIR" \
        2>&1 | grep -v "UserWarning\|warnings.warn" || true
    
    # Whisper translate 会覆盖同名文件，所以直接拷贝
    if [[ -f "$SRT_FILE" ]]; then
        cp "$SRT_FILE" "$OUTPUT_TRANSLATED"
        echo "   ✅ 英文字幕：$OUTPUT_TRANSLATED"
    else
        echo "   ⚠️ 翻译失败，已保存翻译模板"
        cp "$OUTPUT_CN" "$OUTPUT_TRANSLATED"
    fi
else
    echo "🌐 步骤 4: 翻译到 $TARGET_LANG..."
    echo ""
    echo "   ⚠️ Whisper 仅支持自动翻译到英文"
    echo "   💡 其他语言推荐方式："
    echo "      1. 让 Agent 读取 $OUTPUT_CN 并翻译"
    echo "      2. 使用在线翻译工具（DeepL / Google Translate）"
    echo "      3. 手动翻译后保存为 $OUTPUT_TRANSLATED"
    echo ""
    
    # 复制中文字幕作为翻译模板（保留时间戳）
    cp "$OUTPUT_CN" "$OUTPUT_TRANSLATED"
    echo "   📄 已生成翻译模板：$OUTPUT_TRANSLATED"
    echo "   （时间戳已保留，替换中文内容即可）"
fi

echo ""
echo "✅ 字幕生成完成！"
echo ""
echo "📄 输出文件："
echo "   中文字幕：$OUTPUT_CN"
echo "   ${TARGET_LANG} 字幕：$OUTPUT_TRANSLATED"
