#!/bin/bash
# auto-bgm-match.sh - 智能 BGM 匹配
# 分析视频时长/节奏，自动裁剪 BGM 并匹配
#
# 使用方式:
#   bash auto-bgm-match.sh --video input.mp4 --music ./bgm/ --output output.mp4
#   bash auto-bgm-match.sh --video input.mp4 --music track.mp3 --volume 15 --fade 3

set -euo pipefail

source "$(dirname "$0")/colors.sh" 2>/dev/null || {
    RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
    BLUE='\033[0;34m'; NC='\033[0m'
}

VIDEO=""
MUSIC=""
OUTPUT=""
VOLUME=15          # BGM 音量百分比
FADE_IN=2          # 淡入秒数
FADE_OUT=3         # 淡出秒数
KEEP_ORIGINAL=true # 保留原始音频
ORIGINAL_VOL=100   # 原始音频音量百分比

usage() {
    cat << 'EOF'
用法：auto-bgm-match.sh [选项]

必需:
  --video, -v         输入视频文件
  --music, -m         BGM 文件或目录 (目录则自动选最匹配的)

可选:
  --output, -o        输出文件 (默认：input-bgm.mp4)
  --volume            BGM 音量百分比 (默认：15)
  --fade-in           淡入秒数 (默认：2)
  --fade-out          淡出秒数 (默认：3)
  --no-original       去掉原始音频，只保留 BGM
  --original-vol      原始音频音量百分比 (默认：100)
  --help              显示帮助

示例:
  # 自动匹配目录中时长最接近的 BGM
  auto-bgm-match.sh -v video.mp4 -m ./bgm/ -o final.mp4

  # 指定 BGM 文件，音量 20%
  auto-bgm-match.sh -v video.mp4 -m track.mp3 --volume 20
EOF
    exit 0
}

while [[ $# -gt 0 ]]; do
    case $1 in
        --video|-v) VIDEO="$2"; shift 2 ;;
        --music|-m) MUSIC="$2"; shift 2 ;;
        --output|-o) OUTPUT="$2"; shift 2 ;;
        --volume) VOLUME="$2"; shift 2 ;;
        --fade-in) FADE_IN="$2"; shift 2 ;;
        --fade-out) FADE_OUT="$2"; shift 2 ;;
        --no-original) KEEP_ORIGINAL=false; shift ;;
        --original-vol) ORIGINAL_VOL="$2"; shift 2 ;;
        --help|-h) usage ;;
        *) echo "未知参数：$1"; usage ;;
    esac
done

if [[ -z "$VIDEO" || -z "$MUSIC" ]]; then
    echo -e "${RED}❌ 必须提供 --video 和 --music${NC}"
    usage
fi

if [[ ! -f "$VIDEO" ]]; then
    echo -e "${RED}❌ 视频文件不存在：$VIDEO${NC}"
    exit 1
fi

[[ -z "$OUTPUT" ]] && OUTPUT="${VIDEO%.*}-bgm.mp4"

echo -e "${BLUE}🎵 智能 BGM 匹配器${NC}"
echo ""

# === 获取视频时长 ===
VIDEO_DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$VIDEO" 2>/dev/null)
VIDEO_DUR_INT=${VIDEO_DUR%.*}
echo -e "🎬 视频时长：${GREEN}${VIDEO_DUR_INT}s ($((VIDEO_DUR_INT/60)):$(printf '%02d' $((VIDEO_DUR_INT%60))))${NC}"

# === 选择 BGM ===
BGM_FILE=""

if [[ -d "$MUSIC" ]]; then
    echo -e "📁 扫描 BGM 目录：$MUSIC"
    
    # 找时长最接近视频的音乐
    BEST_FILE=""
    BEST_DIFF=999999
    
    MATCH_TMP=$(mktemp)
    find "$MUSIC" -maxdepth 1 -type f \( -name '*.mp3' -o -name '*.wav' -o -name '*.m4a' -o -name '*.aac' -o -name '*.ogg' -o -name '*.flac' \) -print0 2>/dev/null | while IFS= read -r -d '' f; do
        MDUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$f" 2>/dev/null)
        [[ -z "$MDUR" || "$MDUR" == "N/A" ]] && continue
        MDUR_INT=${MDUR%.*}
        DIFF=$(( MDUR_INT > VIDEO_DUR_INT ? MDUR_INT - VIDEO_DUR_INT : VIDEO_DUR_INT - MDUR_INT ))
        echo -e "   🎵 $(basename "$f") (${MDUR_INT}s, 差距 ${DIFF}s)"
        echo "$DIFF $f" >> "$MATCH_TMP"
    done
    
    if [[ -s "$MATCH_TMP" ]]; then
        BEST_LINE=$(sort -n "$MATCH_TMP" | head -1)
        BEST_DIFF=$(echo "$BEST_LINE" | cut -d' ' -f1)
        BEST_FILE=$(echo "$BEST_LINE" | cut -d' ' -f2-)
    fi
    rm -f "$MATCH_TMP"
    
    if [[ -z "$BEST_FILE" ]]; then
        echo -e "${RED}❌ 目录中没有找到音频文件${NC}"
        exit 1
    fi
    
    BGM_FILE="$BEST_FILE"
    echo -e "${GREEN}✅ 最佳匹配：$(basename "$BGM_FILE") (差距 ${BEST_DIFF}s)${NC}"
elif [[ -f "$MUSIC" ]]; then
    BGM_FILE="$MUSIC"
else
    echo -e "${RED}❌ BGM 路径不存在：$MUSIC${NC}"
    exit 1
fi

BGM_DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$BGM_FILE" 2>/dev/null)
BGM_DUR_INT=${BGM_DUR%.*}
echo -e "🎵 BGM 时长：${GREEN}${BGM_DUR_INT}s${NC}"
echo -e "🔊 BGM 音量：${GREEN}${VOLUME}%${NC}"
echo ""

# === 构建 ffmpeg 滤镜 ===
BGM_VOL=$(echo "scale=2; $VOLUME / 100" | bc)
ORIG_VOL=$(echo "scale=2; $ORIGINAL_VOL / 100" | bc)

# BGM 处理：循环/裁剪到视频时长 + 淡入淡出 + 音量
LOOP_FLAG=""
if [[ "$BGM_DUR_INT" -lt "$VIDEO_DUR_INT" ]]; then
    echo -e "${YELLOW}⚠️  BGM 比视频短，将循环播放${NC}"
    LOOP_FLAG="-stream_loop -1"
fi

FADE_OUT_START=$(echo "$VIDEO_DUR - $FADE_OUT" | bc)

echo -e "${BLUE}🔧 合成中...${NC}"

if [[ "$KEEP_ORIGINAL" == true ]]; then
    # 混合原始音频 + BGM
    ffmpeg -y -i "$VIDEO" $LOOP_FLAG -i "$BGM_FILE" \
        -filter_complex "[1:a]atrim=0:${VIDEO_DUR},asetpts=PTS-STARTPTS,afade=t=in:d=${FADE_IN},afade=t=out:st=${FADE_OUT_START}:d=${FADE_OUT},volume=${BGM_VOL}[bgm];[0:a]volume=${ORIG_VOL}[orig];[orig][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]" \
        -map 0:v -map "[aout]" \
        -c:v copy -c:a aac -b:a 192k \
        -t "$VIDEO_DUR" \
        "$OUTPUT" \
        -loglevel warning 2>/dev/null
else
    # 只用 BGM
    ffmpeg -y -i "$VIDEO" $LOOP_FLAG -i "$BGM_FILE" \
        -filter_complex "[1:a]atrim=0:${VIDEO_DUR},asetpts=PTS-STARTPTS,afade=t=in:d=${FADE_IN},afade=t=out:st=${FADE_OUT_START}:d=${FADE_OUT},volume=${BGM_VOL}[bgm]" \
        -map 0:v -map "[bgm]" \
        -c:v copy -c:a aac -b:a 192k \
        -t "$VIDEO_DUR" \
        "$OUTPUT" \
        -loglevel warning 2>/dev/null
fi

if [[ -f "$OUTPUT" ]]; then
    OUT_SIZE=$(stat -f%z "$OUTPUT" 2>/dev/null | awk '{printf "%.1f", $1/1048576}')
    echo ""
    echo -e "${GREEN}✅ BGM 合成完成！${NC}"
    echo -e "   📁 输出：$OUTPUT"
    echo -e "   💾 大小：${OUT_SIZE}MB"
    echo -e "   🎵 BGM：$(basename "$BGM_FILE")"
    echo -e "   🔊 音量：${VOLUME}%"
else
    echo -e "${RED}❌ 合成失败${NC}"
    exit 1
fi
