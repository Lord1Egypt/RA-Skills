#!/bin/bash
# Auto Rough Cut - 基于静音检测自动去除沉默片段
# 使用 ffmpeg silencedetect + silenceremove 实现

set -euo pipefail

INPUT_FILE="$1"
OUTPUT_FILE="${2:-}"
NOISE_DB="${3:--30dB}"
MIN_SILENCE="${4:-0.5}"

if [[ -z "$INPUT_FILE" ]]; then
    echo "❌ 用法：auto-rough-cut.sh <视频/音频文件> [输出文件] [噪音阈值] [最小静音秒数]"
    echo "   默认阈值：-30dB，最小静音：0.5s"
    echo ""
    echo "示例："
    echo "   bash auto-rough-cut.sh video.mp4"
    echo "   bash auto-rough-cut.sh video.mp4 trimmed.mp4 -35dB 1.0"
    exit 1
fi

if [[ ! -f "$INPUT_FILE" ]]; then
    echo "❌ 文件不存在：$INPUT_FILE"
    exit 1
fi

if [[ -z "$OUTPUT_FILE" ]]; then
    OUTPUT_FILE="${INPUT_FILE%.*}-trimmed.${INPUT_FILE##*.}"
fi

echo "✂️ 自动粗剪 - 移除沉默片段"
echo "📁 输入：$INPUT_FILE"
echo "📤 输出：$OUTPUT_FILE"
echo "🔇 噪音阈值：$NOISE_DB"
echo "⏱️ 最小静音：${MIN_SILENCE}s"
echo ""

# Step 1: 检测静音片段
echo "🔍 步骤 1: 检测静音片段..."
SILENCE_LOG=$(mktemp)

ffmpeg -i "$INPUT_FILE" -af "silencedetect=noise=${NOISE_DB}:d=${MIN_SILENCE}" -f null - 2>&1 \
    | grep -E "silence_start|silence_end|silence_duration" > "$SILENCE_LOG" || true

SILENCE_COUNT=$(grep -c "silence_start" "$SILENCE_LOG" 2>/dev/null || echo "0")

if [[ "$SILENCE_COUNT" -eq 0 ]]; then
    echo "✅ 未检测到明显静音片段，无需粗剪"
    rm -f "$SILENCE_LOG"
    exit 0
fi

echo "   检测到 ${SILENCE_COUNT} 个静音片段："
echo ""
while IFS= read -r line; do
    echo "   $line"
done < "$SILENCE_LOG"
echo ""

# Step 2: 使用 silenceremove 过滤器直接去除静音
echo "✂️ 步骤 2: 移除静音片段..."

# 检查输入是否有视频流
HAS_VIDEO=$(ffprobe -v quiet -select_streams v -show_entries stream=codec_type -of csv=p=0 "$INPUT_FILE" 2>/dev/null | head -1)

if [[ "$HAS_VIDEO" == "video" ]]; then
    # 有视频：需要用 segment 方式处理，因为 silenceremove 只能处理音频
    # 策略：提取有声段时间戳 → 分段裁剪 → 拼接
    echo "   📹 视频模式：提取有声片段并拼接..."

    # 解析静音段，构建有声片段列表
    SEGMENTS_FILE=$(mktemp)
    DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$INPUT_FILE" 2>/dev/null)

    python3 << PYEOF
import re, sys

silence_log = open("$SILENCE_LOG").read()
duration = float("$DURATION")

# 解析 silence_start / silence_end
starts = [float(m) for m in re.findall(r'silence_start:\s*([\d.]+)', silence_log)]
ends = [float(m) for m in re.findall(r'silence_end:\s*([\d.]+)', silence_log)]

# 构建有声片段 (非静音段)
voice_segments = []
pos = 0.0
for i, s in enumerate(starts):
    if s > pos + 0.05:  # 最小片段 50ms
        voice_segments.append((pos, s))
    if i < len(ends):
        pos = ends[i]
    else:
        pos = duration

if pos < duration - 0.05:
    voice_segments.append((pos, duration))

if not voice_segments:
    print("NO_SEGMENTS", file=sys.stderr)
    sys.exit(1)

with open("$SEGMENTS_FILE", "w") as f:
    for start, end in voice_segments:
        f.write(f"{start},{end}\n")

total_kept = sum(e - s for s, e in voice_segments)
print(f"   保留 {len(voice_segments)} 个有声片段，总时长 {total_kept:.1f}s（原 {duration:.1f}s）")
PYEOF

    # 分段裁剪并拼接
    TEMP_DIR=$(mktemp -d)
    trap "rm -rf $TEMP_DIR $SILENCE_LOG $SEGMENTS_FILE" EXIT

    CONCAT_LIST="$TEMP_DIR/concat.txt"
    SEG_IDX=0

    while IFS=',' read -r START END; do
        SEG_FILE="$TEMP_DIR/seg_$(printf '%04d' $SEG_IDX).ts"
        ffmpeg -y -i "$INPUT_FILE" -ss "$START" -to "$END" \
            -c:v libx264 -preset fast -crf 23 \
            -c:a aac -b:a 192k \
            -f mpegts "$SEG_FILE" \
            -loglevel error 2>/dev/null
        echo "file '$SEG_FILE'" >> "$CONCAT_LIST"
        SEG_IDX=$((SEG_IDX + 1))
    done < "$SEGMENTS_FILE"

    ffmpeg -y -f concat -safe 0 -i "$CONCAT_LIST" \
        -c:v libx264 -preset fast -crf 23 \
        -c:a aac -b:a 192k \
        "$OUTPUT_FILE" \
        -loglevel error 2>/dev/null

else
    # 纯音频：直接用 silenceremove
    echo "   🎵 音频模式：使用 silenceremove 过滤器..."
    ffmpeg -y -i "$INPUT_FILE" \
        -af "silenceremove=stop_periods=-1:stop_duration=${MIN_SILENCE}:stop_threshold=${NOISE_DB}" \
        "$OUTPUT_FILE" \
        -loglevel warning 2>/dev/null
    rm -f "$SILENCE_LOG"
fi

if [[ -f "$OUTPUT_FILE" ]]; then
    NEW_DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUTPUT_FILE" 2>/dev/null)
    OLD_DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$INPUT_FILE" 2>/dev/null)
    SAVED=$(python3 -c "print(f'{float(\"$OLD_DUR\") - float(\"$NEW_DUR\"):.1f}')" 2>/dev/null || echo "?")
    SIZE=$(stat -f%z "$OUTPUT_FILE" 2>/dev/null | awk '{printf "%.1f", $1/1024/1024}')

    echo ""
    echo "✅ 粗剪完成！"
    echo "   📁 输出：$OUTPUT_FILE"
    echo "   ⏱️ 原时长：${OLD_DUR}s → 新时长：${NEW_DUR}s（节省 ${SAVED}s）"
    echo "   💾 大小：${SIZE}MB"
else
    echo "❌ 粗剪失败"
    exit 1
fi
