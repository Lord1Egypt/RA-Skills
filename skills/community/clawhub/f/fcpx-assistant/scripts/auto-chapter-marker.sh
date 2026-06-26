#!/bin/bash
# Auto Chapter Marker - 基于场景变化和静音检测生成章节标记
# 使用 ffmpeg scdet (场景检测) + silencedetect (静音检测) 定位章节点

set -euo pipefail

VIDEO_FILE="$1"
THRESHOLD="${2:-0.3}"

if [[ -z "$VIDEO_FILE" ]]; then
    echo "❌ 用法：auto-chapter-marker.sh <视频文件> [场景阈值]"
    echo "   场景阈值：0.0-1.0，默认 0.3（越低越灵敏）"
    exit 1
fi

if [[ ! -f "$VIDEO_FILE" ]]; then
    echo "❌ 文件不存在：$VIDEO_FILE"
    exit 1
fi

OUTPUT_FILE="${VIDEO_FILE%.*}-chapters.txt"
OUTPUT_SRT="${VIDEO_FILE%.*}-chapters.srt"

DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$VIDEO_FILE" 2>/dev/null)

echo "📑 自动章节标记生成器"
echo "📁 视频：$VIDEO_FILE"
echo "⏱️ 时长：${DURATION}s"
echo "🎯 场景阈值：$THRESHOLD"
echo ""

# Step 1: 场景检测
echo "🔍 步骤 1: 检测场景变化..."
SCENE_LOG=$(mktemp)

ffmpeg -i "$VIDEO_FILE" \
    -filter_complex "scdet=threshold=${THRESHOLD}:sc_pass=1" \
    -f null - 2>&1 \
    | grep "lavfi.scd.time" > "$SCENE_LOG" || true

SCENE_COUNT=$(wc -l < "$SCENE_LOG" | tr -d ' ')
echo "   检测到 ${SCENE_COUNT} 个场景变化点"

# Step 2: 静音检测（辅助定位）
echo "🔇 步骤 2: 检测静音间隔..."
SILENCE_LOG=$(mktemp)

ffmpeg -i "$VIDEO_FILE" \
    -af "silencedetect=noise=-30dB:d=1.5" \
    -f null - 2>&1 \
    | grep "silence_start" > "$SILENCE_LOG" || true

SILENCE_COUNT=$(wc -l < "$SILENCE_LOG" | tr -d ' ')
echo "   检测到 ${SILENCE_COUNT} 个静音间隔（≥1.5s）"
echo ""

# Step 3: 合并分析，生成章节
echo "📊 步骤 3: 生成章节标记..."

python3 << PYEOF
import re, sys

duration = float("$DURATION")

# 解析场景变化时间点
scene_times = []
with open("$SCENE_LOG") as f:
    for line in f:
        m = re.search(r'lavfi\.scd\.time=([\d.]+)', line)
        if m:
            scene_times.append(float(m.group(1)))

# 解析静音开始时间
silence_times = []
with open("$SILENCE_LOG") as f:
    for line in f:
        m = re.search(r'silence_start:\s*([\d.]+)', line)
        if m:
            silence_times.append(float(m.group(1)))

# 合并场景变化和静音点（去重，最小间隔 10s）
all_points = sorted(set(scene_times + silence_times))
chapters = [0.0]  # 总是从 0 开始

MIN_GAP = max(10.0, duration / 20)  # 最小间隔：10s 或视频时长/20

for t in all_points:
    if t - chapters[-1] >= MIN_GAP and t < duration - 5:
        chapters.append(t)

# 格式化时间
def fmt_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"

def fmt_srt_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

# 输出章节列表
print(f"   生成 {len(chapters)} 个章节标记")
print("")

lines = []
srt_lines = []
for i, t in enumerate(chapters):
    label = f"章节 {i+1}"
    if i == 0:
        label = "开场"
    elif i == len(chapters) - 1 and t > duration * 0.8:
        label = "结尾"

    ts = fmt_time(t)
    lines.append(f"{ts} - {label}")
    print(f"   {ts} - {label}")

    # SRT 格式
    end_t = chapters[i+1] if i+1 < len(chapters) else duration
    srt_lines.append(f"{i+1}")
    srt_lines.append(f"{fmt_srt_time(t)} --> {fmt_srt_time(end_t)}")
    srt_lines.append(label)
    srt_lines.append("")

# 写入文件
with open("$OUTPUT_FILE", "w") as f:
    f.write("\n".join(lines) + "\n")

with open("$OUTPUT_SRT", "w") as f:
    f.write("\n".join(srt_lines))

PYEOF

echo ""
echo "✅ 章节标记生成完成！"
echo ""
echo "📄 输出文件："
echo "   文本格式：$OUTPUT_FILE"
echo "   SRT 格式：$OUTPUT_SRT"
echo ""
echo "💡 使用方式："
echo "   - YouTube 视频描述中粘贴文本格式的时间戳"
echo "   - FCP 中按 M 键在对应时间点添加标记"
echo "   - 导入 SRT 文件作为章节字幕"

rm -f "$SCENE_LOG" "$SILENCE_LOG"
