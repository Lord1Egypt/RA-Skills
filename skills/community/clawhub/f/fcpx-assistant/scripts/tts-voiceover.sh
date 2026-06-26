#!/bin/bash
# tts-voiceover.sh - 用 edge-tts 为文案生成配音
#
# 使用方式:
#   bash tts-voiceover.sh --script "第一段\n第二段\n第三段" --output ./voiceover/
#   bash tts-voiceover.sh --script-file ./script.txt --output ./voiceover/ --merge
#   bash tts-voiceover.sh --script "文案" --voice zh-CN-XiaoxiaoNeural --output ./vo/
#
# 依赖：edge-tts, ffmpeg

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 默认参数
SCRIPT_TEXT=""
SCRIPT_FILE=""
OUTPUT_DIR="./voiceover"
VOICE="zh-CN-YunxiNeural"
RATE="+0%"
TRIM_SILENCE=true
SILENCE_THRESHOLD="-40dB"
MERGE_MODE=false

usage() {
    cat << EOF
用法：$0 [选项]

必需:
  --script, -s        文案内容 (每行一段)
  --script-file       文案文件路径

可选:
  --output, -o        输出目录 (默认：./voiceover)
  --voice             edge-tts 声音 (默认：zh-CN-YunxiNeural)
  --rate              语速调整 (如 +10%, -5%, 默认 +0%)
  --merge             合并文案一次性生成 (音色一致，强烈推荐！)
  --no-trim           不修剪静音
  --list-voices       列出可用中文声音
  --help              显示帮助

可用中文声音:
  zh-CN-YunxiNeural      男声，活泼阳光 (默认)
  zh-CN-YunjianNeural    男声，激情有力
  zh-CN-YunyangNeural    男声，专业新闻
  zh-CN-XiaoxiaoNeural   女声，温暖亲切
  zh-CN-XiaoyiNeural     女声，活泼可爱

示例:
  # 分段生成 (每段独立调用 TTS)
  bash $0 --script-file ./script.txt --output ./voiceover/
  
  # 合并生成 (一次性生成完整文案，音色一致)
  bash $0 --script-file ./script.txt --output ./voiceover/ --merge
  
  # 用女声
  bash $0 --script "你好世界" --voice zh-CN-XiaoxiaoNeural --output ./vo/
EOF
    exit 0
}

while [[ $# -gt 0 ]]; do
    case $1 in
        --script|-s) SCRIPT_TEXT="$2"; shift 2 ;;
        --script-file) SCRIPT_FILE="$2"; shift 2 ;;
        --output|-o) OUTPUT_DIR="$2"; shift 2 ;;
        --voice) VOICE="$2"; shift 2 ;;
        --rate) RATE="$2"; shift 2 ;;
        --merge) MERGE_MODE=true; shift ;;
        --no-trim) TRIM_SILENCE=false; shift ;;
        --list-voices) edge-tts --list-voices 2>/dev/null | grep 'zh-CN'; exit 0 ;;
        --help) usage ;;
        *) echo "未知参数：$1"; usage ;;
    esac
done

if [[ -n "$SCRIPT_FILE" ]] && [[ -f "$SCRIPT_FILE" ]]; then
    SCRIPT_TEXT=$(cat "$SCRIPT_FILE")
fi

if [[ -z "$SCRIPT_TEXT" ]]; then
    echo -e "${RED}❌ 必须提供 --script 或 --script-file${NC}"
    usage
fi

# 检查依赖
if ! command -v edge-tts &>/dev/null; then
    echo -e "${RED}❌ edge-tts 未安装${NC}"
    echo -e "${YELLOW}💡 安装：pipx install edge-tts${NC}"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo -e "${BLUE}🎙️ TTS 配音生成器 (edge-tts)${NC}"
echo -e "声音：${GREEN}$VOICE${NC}"
echo -e "语速：${GREEN}$RATE${NC}"
echo -e "输出：${GREEN}$OUTPUT_DIR${NC}"
echo -e "模式：${GREEN}$([ "$MERGE_MODE" = true ] && echo '合并一次性生成' || echo '分段生成')${NC}"
echo ""

# 处理音频：转 wav + 可选修剪静音
process_audio() {
    local input="$1"
    local output="$2"
    
    if [[ "$TRIM_SILENCE" == "true" ]]; then
        ffmpeg -y -i "$input" \
            -af "silenceremove=start_periods=1:start_threshold=${SILENCE_THRESHOLD}:start_duration=0.05,areverse,silenceremove=start_periods=1:start_threshold=${SILENCE_THRESHOLD}:start_duration=0.05,areverse" \
            "$output" \
            -loglevel warning 2>/dev/null
    else
        ffmpeg -y -i "$input" "$output" -loglevel warning 2>/dev/null
    fi
    rm -f "$input"
}

# 拆分段落
PARAGRAPHS=()
while IFS= read -r line; do
    trimmed=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    if [[ -n "$trimmed" ]]; then
        PARAGRAPHS+=("$trimmed")
    fi
done <<< "$SCRIPT_TEXT"

NUM_PARAGRAPHS=${#PARAGRAPHS[@]}
echo -e "文案段落：${GREEN}$NUM_PARAGRAPHS${NC}"
echo ""

# === 合并模式：一次性生成完整配音 ===
if [[ "$MERGE_MODE" == true ]]; then
    echo -e "${BLUE}🎤 合并模式：将所有文案合并后一次性生成${NC}"
    
    FULL_TEXT=$(printf '%s ' "${PARAGRAPHS[@]}")
    echo -e "   总字符数：${GREEN}${#FULL_TEXT}${NC}"
    
    TEMP_MP3="/tmp/edge-tts-merge-$(date +%s).mp3"
    OUTPUT_FILE="$OUTPUT_DIR/full_voiceover.wav"
    
    echo -e "${BLUE}🚀 调用 edge-tts...${NC}"
    if ! edge-tts --voice "$VOICE" --rate "$RATE" --text "$FULL_TEXT" --write-media "$TEMP_MP3" 2>/dev/null; then
        echo -e "${RED}❌ edge-tts 生成失败${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}✂️  处理音频...${NC}"
    process_audio "$TEMP_MP3" "$OUTPUT_FILE"
    
    if [[ -f "$OUTPUT_FILE" ]]; then
        DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUTPUT_FILE" 2>/dev/null)
        FSIZE=$(stat -f%z "$OUTPUT_FILE" 2>/dev/null | awk '{printf "%.1f", $1/1024/1024}')
        echo -e "${GREEN}✅ 完整配音生成成功！${NC}"
        echo -e "   时长：${DUR}s"
        echo -e "   大小：${FSIZE}MB"
        echo -e "   文件：${OUTPUT_FILE}"
    else
        echo -e "${RED}❌ 音频处理失败${NC}"
        exit 1
    fi
    
    echo ""
    echo -e "${GREEN}✅ 配音文件保存在：$OUTPUT_DIR${NC}"
    echo -e "${BLUE}下一步：用 auto-video-maker.sh --voiceover $OUTPUT_DIR/ 组装成片！${NC}"
    exit 0
fi

# === 分段模式：逐段生成 ===
GENERATED=0

for i in $(seq 0 $((NUM_PARAGRAPHS - 1))); do
    PARA="${PARAGRAPHS[$i]}"
    echo -e "${BLUE}🎤 段落 $((i+1))/$NUM_PARAGRAPHS: \"${PARA:0:40}$([ ${#PARA} -gt 40 ] && echo '...')\"${NC}"
    
    TEMP_MP3="/tmp/edge-tts-seg${i}-$(date +%s).mp3"
    OUTPUT_FILE="$OUTPUT_DIR/vo_$(printf '%03d' $i).wav"
    
    if ! edge-tts --voice "$VOICE" --rate "$RATE" --text "$PARA" --write-media "$TEMP_MP3" 2>/dev/null; then
        echo -e "   ${RED}❌ 生成失败${NC}"
        continue
    fi
    
    process_audio "$TEMP_MP3" "$OUTPUT_FILE"
    
    if [[ -f "$OUTPUT_FILE" ]]; then
        DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUTPUT_FILE" 2>/dev/null | cut -d. -f1-2)
        echo -e "   ${GREEN}✅ vo_$(printf '%03d' $i).wav (${DUR}s)${NC}"
        GENERATED=$((GENERATED + 1))
    else
        echo -e "   ${RED}❌ 音频处理失败${NC}"
    fi
done

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎙️ 配音生成完成！${NC}"
echo -e "   生成：${GREEN}${GENERATED}/${NUM_PARAGRAPHS}${NC} 段"
echo ""

for f in "$OUTPUT_DIR"/vo_*.wav; do
    [[ -f "$f" ]] || continue
    DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$f" 2>/dev/null)
    echo -e "   $(basename "$f"): ${DUR}s"
done

# 合并所有段落
if [[ "$GENERATED" -gt 1 ]]; then
    echo ""
    CONCAT_LIST="$OUTPUT_DIR/concat.txt"
    > "$CONCAT_LIST"
    for f in "$OUTPUT_DIR"/vo_*.wav; do
        [[ -f "$f" ]] || continue
        echo "file '$(realpath "$f")'" >> "$CONCAT_LIST"
    done
    
    FULL_VO="$OUTPUT_DIR/full_voiceover.wav"
    ffmpeg -y -f concat -safe 0 -i "$CONCAT_LIST" -c copy "$FULL_VO" -loglevel warning 2>/dev/null
    
    if [[ -f "$FULL_VO" ]]; then
        FULL_DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$FULL_VO" 2>/dev/null)
        echo -e "   📎 完整配音：full_voiceover.wav (${FULL_DUR}s)"
    fi
    
    rm -f "$CONCAT_LIST"
fi

echo ""
echo -e "${GREEN}✅ 配音文件保存在：$OUTPUT_DIR${NC}"
echo -e "${BLUE}下一步：用 auto-video-maker.sh --voiceover $OUTPUT_DIR/ 组装成片！${NC}"
