#!/bin/bash
# auto-video-maker.sh - 自动将素材 + 文案 + 音乐组装成完整视频（增强版）
#
# 功能增强:
#   ✅ 自动检测语音时长并对齐字幕
#   ✅ 自动清理中间文件和试错素材
#   ✅ 强制三轨混合（视频 +TTS+BGM）
#   ✅ 音量自动平衡（人声:BGM = 3:1）

set -euo pipefail

# === 颜色 ===
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# === 默认参数 ===
PROJECT_DIR=""
SCRIPT_TEXT=""
SCRIPT_FILE=""
MUSIC_FILE=""
VOICEOVER_DIR=""
OUTPUT_FILE="output.mp4"
STYLE="default"
RESOLUTION="1920x1080"
FPS=30
FONT_SIZE=42
SUBTITLE_POSITION="bottom"
NO_SUBTITLE=false
AUTO_CLEANUP=true
TARGET_DURATION=0  # 0 = 自动（跟配音走或估算）

usage() {
    echo "用法：$0 [选项]"
    echo ""
    echo "必需:"
    echo "  --project, -p       素材目录"
    echo "  --script, -s        文案内容"
    echo "  --script-file       文案文件"
    echo ""
    echo "可选:"
    echo "  --music, -m         背景音乐"
    echo "  --voiceover         TTS 配音目录"
    echo "  --output, -o        输出文件"
    echo "  --style             风格：default/vlog/cinematic/fast"
    echo "  --duration          目标时长（秒），强制控制视频总时长"
    echo "  --no-subtitle       不加字幕"
    echo "  --no-auto-cleanup   不清理中间文件"
    echo "  --help              显示帮助"
    exit 0
}

# === 解析参数 ===
while [[ $# -gt 0 ]]; do
    case $1 in
        --project|-p) PROJECT_DIR="$2"; shift 2 ;;
        --script|-s) SCRIPT_TEXT="$2"; shift 2 ;;
        --script-file) SCRIPT_FILE="$2"; shift 2 ;;
        --music|-m) MUSIC_FILE="$2"; shift 2 ;;
        --voiceover) VOICEOVER_DIR="$2"; shift 2 ;;
        --output|-o) OUTPUT_FILE="$2"; shift 2 ;;
        --style) STYLE="$2"; shift 2 ;;
        --duration) TARGET_DURATION="$2"; shift 2 ;;
        --no-subtitle) NO_SUBTITLE=true; shift ;;
        --no-auto-cleanup) AUTO_CLEANUP=false; shift ;;
        --help) usage ;;
        *) echo "未知参数：$1"; usage ;;
    esac
done

# === 风格预设 ===
case "$STYLE" in
    vlog) FONT_SIZE=26; TRANSITION_DURATION=0.3 ;;
    cinematic) FONT_SIZE=30; TRANSITION_DURATION=1.0 ;;
    fast) FONT_SIZE=24; TRANSITION_DURATION=0.2 ;;
    *) FONT_SIZE=28; TRANSITION_DURATION=0.5 ;;
esac

echo -e "${BLUE}🎬 自动成片器${NC}"
echo -e "风格：${GREEN}$STYLE${NC}"
echo -e "分辨率：${GREEN}$RESOLUTION${NC}"
echo -e "自动清理：${GREEN}$AUTO_CLEANUP${NC}"
echo ""

# === 步骤 1: 解析文案 ===
echo -e "${CYAN}📝 Step 1: 解析文案...${NC}"

if [[ -n "$SCRIPT_FILE" ]] && [[ -f "$SCRIPT_FILE" ]]; then
    SCRIPT_TEXT=$(cat "$SCRIPT_FILE")
fi

# 按行拆分文案（兼容 bash 3.x）
SCRIPT_LINES=()
while IFS= read -r line; do
    [[ -n "$line" ]] && SCRIPT_LINES+=("$line")
done <<< "$SCRIPT_TEXT"
PARAGRAPH_COUNT=${#SCRIPT_LINES[@]}

echo -e "   文案段落数：${GREEN}$PARAGRAPH_COUNT${NC}"

# === 步骤 2: 收集素材 ===
echo -e "${CYAN}📹 Step 2: 收集素材...${NC}"

VIDEOS_DIR="$PROJECT_DIR/videos"
VIDEO_FILES=()

if [[ -d "$VIDEOS_DIR" ]]; then
    while IFS= read -r -d '' file; do
        VIDEO_FILES+=("$file")
    done < <(find "$VIDEOS_DIR" -type f \( -name "*.mp4" -o -name "*.mov" \) -print0 2>/dev/null)
fi

if [[ ${#VIDEO_FILES[@]} -eq 0 ]]; then
    echo -e "${RED}❌ 未找到视频素材${NC}"
    exit 1
fi

echo -e "   可用视频素材：${GREEN}${#VIDEO_FILES[@]}${NC}"

# === 步骤 3: 获取语音时长（如果有配音）===
echo -e "${CYAN}🎤 Step 3: 分析语音时长...${NC}"

declare -a VOICE_DURATIONS=()
TOTAL_VOICE_DURATION=0
HAS_VOICEOVER=false

if [[ -n "$VOICEOVER_DIR" ]] && [[ -d "$VOICEOVER_DIR" ]]; then
    # 优先使用分段配音（时长更精准），其次完整配音
    if ls "$VOICEOVER_DIR"/vo_*.wav 1>/dev/null 2>&1; then
        # 检查是否有分段配音
        HAS_VOICEOVER=true
        for i in $(seq 0 $((PARAGRAPH_COUNT - 1))); do
            VO_FILE="$VOICEOVER_DIR/vo_$(printf '%03d' $i).wav"
            if [[ -f "$VO_FILE" ]]; then
                DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$VO_FILE" 2>/dev/null || echo "0")
                VOICE_DURATIONS+=("$DUR")
                TOTAL_VOICE_DURATION=$(echo "$TOTAL_VOICE_DURATION + $DUR" | bc)
                echo -e "   段落 $((i+1)): ${GREEN}${DUR}s${NC}"
            else
                EST_DUR=$(echo "${#SCRIPT_LINES[$i]} * 0.15" | bc)
                VOICE_DURATIONS+=("$EST_DUR")
                TOTAL_VOICE_DURATION=$(echo "$TOTAL_VOICE_DURATION + $EST_DUR" | bc)
            fi
        done
        echo -e "   总语音时长：${GREEN}${TOTAL_VOICE_DURATION}s${NC} (分段配音)"
    elif [[ -f "$VOICEOVER_DIR/full_voiceover.wav" ]]; then
        # 仅有完整配音文件（无分段），平均分配
        HAS_VOICEOVER=true
        FULL_VOICE_FILE="$VOICEOVER_DIR/full_voiceover.wav"
        FULL_DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$FULL_VOICE_FILE" 2>/dev/null || echo "0")
        AVG_DURATION=$(echo "scale=3; $FULL_DURATION / $PARAGRAPH_COUNT" | bc)
        for i in $(seq 0 $((PARAGRAPH_COUNT - 1))); do
            VOICE_DURATIONS+=("$AVG_DURATION")
            TOTAL_VOICE_DURATION=$(echo "$TOTAL_VOICE_DURATION + $AVG_DURATION" | bc)
            echo -e "   段落 $((i+1)): ${GREEN}${AVG_DURATION}s${NC}"
        done
        echo -e "   总语音时长：${GREEN}${FULL_DURATION}s${NC} (完整配音，平均分配)"
    else
        # 无配音文件，用目标时长或估算
        if [[ "$TARGET_DURATION" -gt 0 ]]; then
            AVG_DUR=$(echo "scale=3; $TARGET_DURATION / $PARAGRAPH_COUNT" | bc)
            for i in $(seq 0 $((PARAGRAPH_COUNT - 1))); do
                VOICE_DURATIONS+=("$AVG_DUR")
                TOTAL_VOICE_DURATION=$(echo "$TOTAL_VOICE_DURATION + $AVG_DUR" | bc)
            done
            echo -e "   ${YELLOW}⚠️  无配音，使用目标时长 ${TARGET_DURATION}s 均分${NC}"
        else
            for i in $(seq 0 $((PARAGRAPH_COUNT - 1))); do
                EST_DUR=$(echo "${#SCRIPT_LINES[$i]} * 0.15 + 2" | bc)
                VOICE_DURATIONS+=("$EST_DUR")
                TOTAL_VOICE_DURATION=$(echo "$TOTAL_VOICE_DURATION + $EST_DUR" | bc)
            done
            echo -e "   ${YELLOW}⚠️  无配音，使用估算时长${NC}"
        fi
    fi
else
    # 无配音目录
    if [[ "$TARGET_DURATION" -gt 0 ]]; then
        AVG_DUR=$(echo "scale=3; $TARGET_DURATION / $PARAGRAPH_COUNT" | bc)
        for i in $(seq 0 $((PARAGRAPH_COUNT - 1))); do
            VOICE_DURATIONS+=("$AVG_DUR")
            TOTAL_VOICE_DURATION=$(echo "$TOTAL_VOICE_DURATION + $AVG_DUR" | bc)
        done
        echo -e "   ${YELLOW}⚠️  无配音，使用目标时长 ${TARGET_DURATION}s 均分${NC}"
    else
        for i in $(seq 0 $((PARAGRAPH_COUNT - 1))); do
            EST_DUR=$(echo "${#SCRIPT_LINES[$i]} * 0.15 + 2" | bc)
            VOICE_DURATIONS+=("$EST_DUR")
            TOTAL_VOICE_DURATION=$(echo "$TOTAL_VOICE_DURATION + $EST_DUR" | bc)
        done
        echo -e "   ${YELLOW}⚠️  无配音，使用估算时长${NC}"
    fi
fi



# === 步骤 4: 剪辑片段 ===
echo -e "${CYAN}✂️  Step 4: 剪辑片段...${NC}"

TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

VIDEO_INDEX=0
for i in $(seq 0 $((PARAGRAPH_COUNT - 1))); do
    TARGET_DUR="${VOICE_DURATIONS[$i]}"
    SOURCE_VIDEO="${VIDEO_FILES[$VIDEO_INDEX % ${#VIDEO_FILES[@]}]}"
    SOURCE_DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$SOURCE_VIDEO" 2>/dev/null || echo "10")
    
    OUTPUT_SEGMENT="$TEMP_DIR/segment_$(printf '%03d' $i).mp4"
    
    if (( $(echo "$TARGET_DUR <= $SOURCE_DUR" | bc -l) )); then
        # 素材够长，直接截取
        ffmpeg -y -i "$SOURCE_VIDEO" \
            -t "$TARGET_DUR" \
            -vf "scale=${RESOLUTION%%x*}:${RESOLUTION##*x}:force_original_aspect_ratio=decrease,pad=${RESOLUTION%%x*}:${RESOLUTION##*x}:(ow-iw)/2:(oh-ih)/2" \
            -c:v libx264 -preset fast -crf 23 \
            -an \
            "$OUTPUT_SEGMENT" \
            -loglevel error 2>/dev/null
    else
        # 素材不够长，循环播放到目标时长
        ffmpeg -y -stream_loop -1 -i "$SOURCE_VIDEO" \
            -t "$TARGET_DUR" \
            -vf "scale=${RESOLUTION%%x*}:${RESOLUTION##*x}:force_original_aspect_ratio=decrease,pad=${RESOLUTION%%x*}:${RESOLUTION##*x}:(ow-iw)/2:(oh-ih)/2" \
            -c:v libx264 -preset fast -crf 23 \
            -an \
            "$OUTPUT_SEGMENT" \
            -loglevel error 2>/dev/null
    fi
    
    ACTUAL_DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUTPUT_SEGMENT" 2>/dev/null || echo "?")
    echo -e "   段落 $((i+1)): $(basename "$SOURCE_VIDEO") → ${GREEN}${ACTUAL_DUR}s${NC} (目标 ${TARGET_DUR}s)"
    
    VIDEO_INDEX=$((VIDEO_INDEX + 1))
done

# === 步骤 5: 拼接片段 ===
echo -e "${CYAN}🔗 Step 5: 拼接片段...${NC}"

# 先统一所有片段的编码参数，然后 concat
for i in $(seq 0 $((PARAGRAPH_COUNT - 1))); do
    SEG="$TEMP_DIR/segment_$(printf '%03d' $i).mp4"
    NORM="$TEMP_DIR/norm_$(printf '%03d' $i).ts"
    ffmpeg -y -i "$SEG" \
        -c:v libx264 -preset fast -crf 23 \
        -r $FPS -an \
        -bsf:v h264_mp4toannexb \
        -f mpegts \
        "$NORM" \
        -loglevel error 2>/dev/null
done

# 用 concat protocol 拼接 ts 文件（最可靠的方式）
CONCAT_INPUT="concat:"
FIRST=true
for i in $(seq 0 $((PARAGRAPH_COUNT - 1))); do
    NORM="$TEMP_DIR/norm_$(printf '%03d' $i).ts"
    if [[ "$FIRST" == true ]]; then
        CONCAT_INPUT+="$NORM"
        FIRST=false
    else
        CONCAT_INPUT+="|$NORM"
    fi
done

TEMP_VIDEO="$TEMP_DIR/concatenated.mp4"

TRIM_OPT=""
if (( $(echo "$TOTAL_VOICE_DURATION > 0" | bc -l) )); then
    TRIM_OPT="-t $TOTAL_VOICE_DURATION"
    echo -e "   目标时长：${GREEN}${TOTAL_VOICE_DURATION}s${NC}"
fi

ffmpeg -y -i "$CONCAT_INPUT" \
    $TRIM_OPT \
    -c:v libx264 -preset fast -crf 23 -an \
    "$TEMP_VIDEO" \
    -loglevel error 2>/dev/null

echo -e "   ${GREEN}✅ 视频拼接完成${NC}"

# === 步骤 6: 混入音频（TTS + BGM）===
echo -e "${CYAN}🎵 Step 6: 混入音频...${NC}"

# 查找 BGM
if [[ -z "$MUSIC_FILE" ]]; then
    MUSIC_DIR="$PROJECT_DIR/music"
    if [[ -d "$MUSIC_DIR" ]]; then
        MUSIC_FILE=$(find "$MUSIC_DIR" -type f \( -name "*.mp3" -o -name "*.wav" -o -name "*.m4a" \) | head -1)
    fi
fi

# 检查是否有配音（支持分段和完整两种模式）
HAS_VOICEOVER=false
USE_FULL_VOICE=false
FULL_VOICE_FILE=""

if [[ -n "$VOICEOVER_DIR" ]] && [[ -d "$VOICEOVER_DIR" ]]; then
    # 优先分段配音
    if ls "$VOICEOVER_DIR"/vo_*.wav 1>/dev/null 2>&1; then
        HAS_VOICEOVER=true
    elif [[ -f "$VOICEOVER_DIR/full_voiceover.wav" ]]; then
        HAS_VOICEOVER=true
        USE_FULL_VOICE=true
        FULL_VOICE_FILE="$VOICEOVER_DIR/full_voiceover.wav"
    fi
fi

if [[ "$HAS_VOICEOVER" == true ]] && [[ -n "$MUSIC_FILE" ]] && [[ -f "$MUSIC_FILE" ]]; then
    # 三轨混合：视频 +TTS+BGM
    echo -e "   🎤 TTS 配音：已启用"
    echo -e "   🎵 背景音乐：$(basename "$MUSIC_FILE")"
    echo -e "   📎 混合模式：TTS + BGM (音量比 3:1)"
    
    MERGED_TTS="$TEMP_DIR/merged_tts.wav"
    
    if [[ "$USE_FULL_VOICE" == true ]]; then
        # 使用完整配音文件
        echo -e "   📎 使用完整配音文件"
        cp "$FULL_VOICE_FILE" "$MERGED_TTS"
    else
        # 合并所有 TTS 片段
        TTS_LIST="$TEMP_DIR/tts_list.txt"
        > "$TTS_LIST"
        for i in $(seq 0 $((PARAGRAPH_COUNT - 1))); do
            VO_FILE="$VOICEOVER_DIR/vo_$(printf '%03d' $i).wav"
            [[ -f "$VO_FILE" ]] && echo "file '$(realpath "$VO_FILE")'" >> "$TTS_LIST"
        done
        ffmpeg -y -f concat -safe 0 -i "$TTS_LIST" -c copy "$MERGED_TTS" 2>/dev/null
    fi
    
    # 获取视频时长
    VIDEO_DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$TEMP_VIDEO" 2>/dev/null || echo "30")
    
    # 混合 TTS 和 BGM
    ffmpeg -y -i "$TEMP_VIDEO" -i "$MERGED_TTS" -i "$MUSIC_FILE" \
        -filter_complex "[1:a]volume=1.0[voice];[2:a]volume=0.3,afade=t=in:st=0:d=2,afade=t=out:st=$(echo "$VIDEO_DURATION - 3" | bc):d=3,atrim=0:${VIDEO_DURATION}[music];[voice][music]amix=inputs=2:duration=first:dropout_transition=2:weights='1 0.5'[aout]" \
        -map 0:v -map "[aout]" \
        -c:v copy -c:a aac -b:a 192k \
        -shortest \
        "$OUTPUT_FILE" \
        -loglevel warning 2>/dev/null
    
    echo -e "   ${GREEN}✅ TTS + BGM 混合完成${NC}"
    
elif [[ "$HAS_VOICEOVER" == true ]]; then
    # 只有 TTS
    echo -e "   🎤 TTS 配音：已启用"
    echo -e "   ${YELLOW}⚠️  无背景音乐${NC}"
    
    MERGED_TTS="$TEMP_DIR/merged_tts.wav"
    
    if [[ "$USE_FULL_VOICE" == true ]]; then
        cp "$FULL_VOICE_FILE" "$MERGED_TTS"
    else
        TTS_LIST="$TEMP_DIR/tts_list.txt"
        > "$TTS_LIST"
        for i in $(seq 0 $((PARAGRAPH_COUNT - 1))); do
            VO_FILE="$VOICEOVER_DIR/vo_$(printf '%03d' $i).wav"
            [[ -f "$VO_FILE" ]] && echo "file '$(realpath "$VO_FILE")'" >> "$TTS_LIST"
        done
        ffmpeg -y -f concat -safe 0 -i "$TTS_LIST" -c copy "$MERGED_TTS" 2>/dev/null
    fi
    
    ffmpeg -y -i "$TEMP_VIDEO" -i "$MERGED_TTS" \
        -c:v copy -c:a aac -b:a 192k \
        -shortest \
        "$OUTPUT_FILE" \
        -loglevel warning 2>/dev/null
    
    echo -e "   ${GREEN}✅ 已混入 TTS 配音${NC}"
    
elif [[ -n "$MUSIC_FILE" ]] && [[ -f "$MUSIC_FILE" ]]; then
    # 只有 BGM
    echo -e "   🎵 背景音乐：$(basename "$MUSIC_FILE")"
    
    VIDEO_DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$TEMP_VIDEO" 2>/dev/null || echo "30")
    
    ffmpeg -y -i "$TEMP_VIDEO" -i "$MUSIC_FILE" \
        -filter_complex "[1:a]volume=0.3,afade=t=in:st=0:d=2,afade=t=out:st=$(echo "$VIDEO_DURATION - 3" | bc):d=3[music]" \
        -map 0:v -map "[music]" \
        -c:v copy -c:a aac -b:a 192k \
        -shortest \
        "$OUTPUT_FILE" \
        -loglevel warning 2>/dev/null
    
    echo -e "   ${GREEN}✅ 已混入背景音乐${NC}"
else
    # 无音频
    echo -e "   ${YELLOW}⚠️  无音频，输出静音视频${NC}"
    
    cp "$TEMP_VIDEO" "$OUTPUT_FILE"
fi

# === 步骤 7: 添加字幕（自动对齐）===
if [[ "$NO_SUBTITLE" != true ]]; then
    echo -e "${CYAN}📝 Step 7: 生成字幕...${NC}"
    
    SUBTITLE_SRT="$TEMP_DIR/subtitles.srt"
    
    # 辅助函数：格式化 SRT 时间
    format_srt_time() {
        local t="$1"
        local h=$(awk "BEGIN {printf \"%d\", int($t / 3600)}")
        local m=$(awk "BEGIN {printf \"%d\", int(($t % 3600) / 60)}")
        local s=$(awk "BEGIN {printf \"%d\", int($t % 60)}")
        local ms=$(awk "BEGIN {printf \"%d\", int(($t - int($t)) * 1000)}")
        printf "%02d:%02d:%02d,%03d" $h $m $s $ms
    }
    
    # 将长段落拆成短句（按句号、逗号、感叹号、问号等断句，每条最多 20 字）
    MAX_CHARS_PER_SUB=20
    SUB_INDEX=1
    CURRENT_TIME=0
    TOTAL_SUBS=0
    
    for i in $(seq 0 $((PARAGRAPH_COUNT - 1))); do
        PARA="${SCRIPT_LINES[$i]}"
        PARA_DUR="${VOICE_DURATIONS[$i]}"
        PARA_LEN=${#PARA}
        
        # 按标点拆成短句
        SENTENCES=()
        # 用 awk 按中文标点和英文标点拆分
        while IFS= read -r sent; do
            [[ -n "$sent" ]] && SENTENCES+=("$sent")
        done < <(echo "$PARA" | sed 's/[。！？!?]/&\n/g' | sed 's/[，,；;：:]/&\n/g' | while IFS= read -r chunk; do
            chunk=$(echo "$chunk" | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
            [[ -z "$chunk" ]] && continue
            # 如果还是太长，按字数硬切
            if [[ ${#chunk} -gt $MAX_CHARS_PER_SUB ]]; then
                while [[ ${#chunk} -gt 0 ]]; do
                    echo "${chunk:0:$MAX_CHARS_PER_SUB}"
                    chunk="${chunk:$MAX_CHARS_PER_SUB}"
                done
            else
                echo "$chunk"
            fi
        done)
        
        NUM_SENTS=${#SENTENCES[@]}
        if [[ $NUM_SENTS -eq 0 ]]; then
            SENTENCES=("$PARA")
            NUM_SENTS=1
        fi
        
        # 按字符数比例分配时长
        TOTAL_SENT_CHARS=0
        for sent in "${SENTENCES[@]}"; do
            TOTAL_SENT_CHARS=$((TOTAL_SENT_CHARS + ${#sent}))
        done
        [[ $TOTAL_SENT_CHARS -eq 0 ]] && TOTAL_SENT_CHARS=1
        
        for j in $(seq 0 $((NUM_SENTS - 1))); do
            SENT="${SENTENCES[$j]}"
            SENT_LEN=${#SENT}
            # 按字符比例分配时长
            SENT_DUR=$(awk "BEGIN {printf \"%.3f\", $PARA_DUR * $SENT_LEN / $TOTAL_SENT_CHARS}")
            # 最少 1 秒
            SENT_DUR=$(awk "BEGIN {d=$SENT_DUR; if(d<1.0) d=1.0; printf \"%.3f\", d}")
            
            START_FMT=$(format_srt_time "$CURRENT_TIME")
            END_TIME=$(echo "$CURRENT_TIME + $SENT_DUR" | bc)
            END_FMT=$(format_srt_time "$END_TIME")
            
            echo "$SUB_INDEX" >> "$SUBTITLE_SRT"
            echo "$START_FMT --> $END_FMT" >> "$SUBTITLE_SRT"
            echo "$SENT" >> "$SUBTITLE_SRT"
            echo "" >> "$SUBTITLE_SRT"
            
            CURRENT_TIME="$END_TIME"
            SUB_INDEX=$((SUB_INDEX + 1))
            TOTAL_SUBS=$((TOTAL_SUBS + 1))
        done
    done
    
    echo -e "   生成 ${GREEN}$TOTAL_SUBS${NC} 条字幕（从 $PARAGRAPH_COUNT 段拆分）"
    
    # 烧入字幕
    TEMP_WITH_SUBS="$TEMP_DIR/with_subtitles.mp4"
    ffmpeg -y -i "$OUTPUT_FILE" \
        -vf "subtitles=$SUBTITLE_SRT:force_style='FontName=PingFang SC,FontSize=$FONT_SIZE,PrimaryColour=&H00FFFFFF,BackColour=&H80000000,Alignment=2,MarginV=28,BorderStyle=4'" \
        -c:a copy \
        "$TEMP_WITH_SUBS" \
        -loglevel warning 2>/dev/null
    
    mv "$TEMP_WITH_SUBS" "$OUTPUT_FILE"
    echo -e "   ${GREEN}✅ 字幕已烧入${NC}"
fi

# === 步骤 8: 自动清理 ===
if [[ "$AUTO_CLEANUP" == true ]]; then
    echo -e "${CYAN}🗑️  Step 8: 自动清理...${NC}"
    
    # 删除试错文件
    find "$(dirname "$OUTPUT_FILE")" -maxdepth 1 -name "*.mp4" ! -name "$(basename "$OUTPUT_FILE")" -type f -delete 2>/dev/null && \
        echo -e "   删除试错视频文件"
    
    # 删除旧字幕文件
    find "$(dirname "$OUTPUT_FILE")" -maxdepth 1 -name "*.srt" -type f -delete 2>/dev/null && \
        echo -e "   删除旧字幕文件"
    
    # 删除临时配音（保留 segmented 目录）
    if [[ -d "$PROJECT_DIR/voiceover" ]] && [[ "$PROJECT_DIR/voiceover" != "$VOICEOVER_DIR" ]]; then
        trash "$PROJECT_DIR/voiceover" 2>/dev/null || rm -rf "$PROJECT_DIR/voiceover"
        echo -e "   删除旧配音文件"
    fi
    
    echo -e "   ${GREEN}✅ 清理完成${NC}"
fi

# === 完成 ===
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 视频制作完成！${NC}"
echo ""

FILE_SIZE=$(stat -f%z "$OUTPUT_FILE" 2>/dev/null || stat -c%s "$OUTPUT_FILE" 2>/dev/null || echo "0")
DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUTPUT_FILE" 2>/dev/null || echo "0")

echo -e "   📁 文件：${GREEN}$OUTPUT_FILE${NC}"
echo -e "   ⏱️  时长：${GREEN}${DURATION}s${NC}"
echo -e "   📐 分辨率：${GREEN}$RESOLUTION${NC}"
echo -e "   💾 大小：${GREEN}$(echo "scale=1; $FILE_SIZE / 1048576" | bc)MB${NC}"
echo -e "   🎬 段落：${GREEN}$PARAGRAPH_COUNT${NC}"
echo ""
echo -e "${GREEN}🎉 所有工作完成！${NC}"
