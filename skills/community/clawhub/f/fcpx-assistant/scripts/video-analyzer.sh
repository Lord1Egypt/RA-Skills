#!/bin/bash
# video-analyzer.sh - 视频质量分析
# 分析画面亮度、色调分布、音频响度曲线，输出质量报告
#
# 使用方式:
#   bash video-analyzer.sh input.mp4
#   bash video-analyzer.sh input.mp4 --output report.json --verbose

set -euo pipefail

source "$(dirname "$0")/colors.sh" 2>/dev/null || {
    RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
    BLUE='\033[0;34m'; CYAN='\033[0;36m'; NC='\033[0m'
}

VIDEO=""
OUTPUT=""
VERBOSE=false

usage() {
    cat << 'EOF'
用法：video-analyzer.sh <视频文件> [选项]

选项:
  --output, -o     输出报告文件 (JSON，默认打印到终端)
  --verbose        显示详细分析过程
  --help           显示帮助

分析内容:
  📐 基本信息    分辨率、帧率、时长、编码、文件大小
  🎨 画面分析    平均亮度、对比度、色温偏向
  🔊 音频分析    响度 (LUFS)、峰值、动态范围
  📊 质量评分    综合评分 + 改进建议

示例:
  video-analyzer.sh video.mp4
  video-analyzer.sh video.mp4 -o report.json --verbose
EOF
    exit 0
}

while [[ $# -gt 0 ]]; do
    case $1 in
        --output|-o) OUTPUT="$2"; shift 2 ;;
        --verbose) VERBOSE=true; shift ;;
        --help|-h) usage ;;
        -*)
            echo "未知参数：$1"; usage ;;
        *)
            if [[ -z "$VIDEO" ]]; then VIDEO="$1"; fi
            shift ;;
    esac
done

if [[ -z "$VIDEO" || ! -f "$VIDEO" ]]; then
    echo -e "${RED}❌ 必须提供有效的视频文件${NC}"
    usage
fi

echo -e "${BLUE}📊 视频质量分析器${NC}"
echo -e "文件：${GREEN}$VIDEO${NC}"
echo ""

TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# ============================
# 1. 基本信息
# ============================
echo -e "${CYAN}📐 基本信息${NC}"

WIDTH=$(ffprobe -v quiet -select_streams v:0 -show_entries stream=width -of csv=p=0 "$VIDEO" 2>/dev/null)
HEIGHT=$(ffprobe -v quiet -select_streams v:0 -show_entries stream=height -of csv=p=0 "$VIDEO" 2>/dev/null)
FPS=$(ffprobe -v quiet -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$VIDEO" 2>/dev/null)
FPS_FLOAT=$(echo "$FPS" | bc -l 2>/dev/null | xargs printf "%.2f" 2>/dev/null || echo "$FPS")
DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$VIDEO" 2>/dev/null)
DUR_INT=${DURATION%.*}
CODEC=$(ffprobe -v quiet -select_streams v:0 -show_entries stream=codec_name -of csv=p=0 "$VIDEO" 2>/dev/null)
ACODEC=$(ffprobe -v quiet -select_streams a:0 -show_entries stream=codec_name -of csv=p=0 "$VIDEO" 2>/dev/null || echo "none")
BITRATE=$(ffprobe -v quiet -show_entries format=bit_rate -of csv=p=0 "$VIDEO" 2>/dev/null)
BITRATE_KBPS=$((BITRATE / 1000))
FILE_SIZE=$(stat -f%z "$VIDEO" 2>/dev/null || stat -c%s "$VIDEO" 2>/dev/null)
SIZE_MB=$(echo "scale=1; $FILE_SIZE / 1048576" | bc)

echo -e "   分辨率：${GREEN}${WIDTH}x${HEIGHT}${NC}"
echo -e "   帧率：${GREEN}${FPS_FLOAT} fps${NC}"
echo -e "   时长：${GREEN}${DUR_INT}s ($((DUR_INT/60)):$(printf '%02d' $((DUR_INT%60))))${NC}"
echo -e "   编码：${GREEN}${CODEC} / ${ACODEC}${NC}"
echo -e "   码率：${GREEN}${BITRATE_KBPS} kbps${NC}"
echo -e "   大小：${GREEN}${SIZE_MB}MB${NC}"
echo ""

# 分辨率评分
RES_SCORE=0
PIXELS=$((WIDTH * HEIGHT))
if [[ $PIXELS -ge 8294400 ]]; then RES_SCORE=100; RES_LABEL="4K"
elif [[ $PIXELS -ge 2073600 ]]; then RES_SCORE=90; RES_LABEL="1080p"
elif [[ $PIXELS -ge 921600 ]]; then RES_SCORE=70; RES_LABEL="720p"
elif [[ $PIXELS -ge 409920 ]]; then RES_SCORE=50; RES_LABEL="480p"
else RES_SCORE=30; RES_LABEL="低分辨率"
fi

# ============================
# 2. 画面分析 (采样分析)
# ============================
echo -e "${CYAN}🎨 画面分析${NC}"

# 用 signalstats 分析亮度和色度 (采样 10 帧)
[[ "$VERBOSE" == true ]] && echo -e "   ${BLUE}⏳ 分析画面...${NC}"

SIGNAL_LOG="$TEMP_DIR/signal.txt"
FPS_INT=$(echo "$FPS_FLOAT" | cut -d. -f1)
[[ "$FPS_INT" -lt 1 ]] && FPS_INT=24
SAMPLE_INTERVAL=$((FPS_INT * 3))

ffmpeg -i "$VIDEO" -vf "select='not(mod(n\,${SAMPLE_INTERVAL}))',signalstats,metadata=print:file=${SIGNAL_LOG}" \
    -f null - -loglevel warning 2>/dev/null || true

# 提取平均亮度 (YAVG)
AVG_BRIGHTNESS=$(grep 'YAVG=' "$SIGNAL_LOG" 2>/dev/null | sed 's/.*YAVG=//' | awk '{sum+=$1; n++} END {if(n>0) printf "%.1f", sum/n; else print "N/A"}')
# 提取亮度范围
YLOW=$(grep 'YLOW=' "$SIGNAL_LOG" 2>/dev/null | sed 's/.*YLOW=//' | awk '{sum+=$1; n++} END {if(n>0) printf "%.1f", sum/n; else print "N/A"}')
YHIGH=$(grep 'YHIGH=' "$SIGNAL_LOG" 2>/dev/null | sed 's/.*YHIGH=//' | awk '{sum+=$1; n++} END {if(n>0) printf "%.1f", sum/n; else print "N/A"}')
# 色度
UAVG=$(grep 'UAVG=' "$SIGNAL_LOG" 2>/dev/null | sed 's/.*UAVG=//' | awk '{sum+=$1; n++} END {if(n>0) printf "%.1f", sum/n; else print "128"}')
VAVG=$(grep 'VAVG=' "$SIGNAL_LOG" 2>/dev/null | sed 's/.*VAVG=//' | awk '{sum+=$1; n++} END {if(n>0) printf "%.1f", sum/n; else print "128"}')

# 判断亮度情况
BRIGHTNESS_NOTE=""
BRIGHTNESS_SCORE=80
if [[ "$AVG_BRIGHTNESS" != "N/A" ]]; then
    B_INT=${AVG_BRIGHTNESS%.*}
    if [[ $B_INT -lt 50 ]]; then
        BRIGHTNESS_NOTE="偏暗"
        BRIGHTNESS_SCORE=50
    elif [[ $B_INT -lt 80 ]]; then
        BRIGHTNESS_NOTE="略暗"
        BRIGHTNESS_SCORE=65
    elif [[ $B_INT -gt 200 ]]; then
        BRIGHTNESS_NOTE="过曝"
        BRIGHTNESS_SCORE=40
    elif [[ $B_INT -gt 170 ]]; then
        BRIGHTNESS_NOTE="偏亮"
        BRIGHTNESS_SCORE=65
    else
        BRIGHTNESS_NOTE="正常"
        BRIGHTNESS_SCORE=90
    fi
fi

# 色温判断
COLOR_TEMP="中性"
if [[ "$UAVG" != "N/A" && "$VAVG" != "N/A" ]]; then
    U_INT=${UAVG%.*}
    V_INT=${VAVG%.*}
    if [[ $V_INT -gt 135 ]]; then COLOR_TEMP="偏暖 (暖色调)"
    elif [[ $V_INT -lt 120 ]]; then COLOR_TEMP="偏冷 (冷色调)"
    else COLOR_TEMP="中性"
    fi
fi

echo -e "   平均亮度：${GREEN}${AVG_BRIGHTNESS}/255 ($BRIGHTNESS_NOTE)${NC}"
echo -e "   亮度范围：${GREEN}${YLOW} ~ ${YHIGH}${NC}"
echo -e "   色温倾向：${GREEN}${COLOR_TEMP}${NC}"
echo ""

# ============================
# 3. 音频分析
# ============================
echo -e "${CYAN}🔊 音频分析${NC}"

AUDIO_SCORE=80

if [[ "$ACODEC" != "none" && "$ACODEC" != "N/A" ]]; then
    LOUDNESS_LOG="$TEMP_DIR/loudness.txt"
    ffmpeg -i "$VIDEO" -af loudnorm=print_format=json -f null - 2>"$LOUDNESS_LOG" || true
    
    # 解析 loudnorm 输出
    INPUT_I=$(grep '"input_i"' "$LOUDNESS_LOG" 2>/dev/null | sed 's/.*: *"//;s/".*//' | tail -1)
    INPUT_TP=$(grep '"input_tp"' "$LOUDNESS_LOG" 2>/dev/null | sed 's/.*: *"//;s/".*//' | tail -1)
    INPUT_LRA=$(grep '"input_lra"' "$LOUDNESS_LOG" 2>/dev/null | sed 's/.*: *"//;s/".*//' | tail -1)
    [[ -z "$INPUT_I" ]] && INPUT_I="N/A"
    [[ -z "$INPUT_TP" ]] && INPUT_TP="N/A"
    [[ -z "$INPUT_LRA" ]] && INPUT_LRA="N/A"
    
    echo -e "   响度 (LUFS)：${GREEN}${INPUT_I} LUFS${NC}"
    echo -e "   真峰值：${GREEN}${INPUT_TP} dBTP${NC}"
    echo -e "   动态范围：${GREEN}${INPUT_LRA} LU${NC}"
    
    # 评分
    if [[ "$INPUT_I" != "N/A" ]]; then
        I_INT=$(echo "$INPUT_I" | cut -d. -f1 | tr -d '-')
        if [[ $I_INT -ge 20 && $I_INT -le 26 ]]; then
            AUDIO_SCORE=90
            echo -e "   评价：${GREEN}✅ 响度适中 (推荐 -23 LUFS)${NC}"
        elif [[ $I_INT -lt 16 ]]; then
            AUDIO_SCORE=50
            echo -e "   评价：${YELLOW}⚠️  响度过高，可能失真${NC}"
        elif [[ $I_INT -gt 30 ]]; then
            AUDIO_SCORE=55
            echo -e "   评价：${YELLOW}⚠️  响度偏低，建议标准化${NC}"
        else
            AUDIO_SCORE=75
            echo -e "   评价：${YELLOW}响度可接受${NC}"
        fi
    fi
    
    # 检查削波
    if [[ "$INPUT_TP" != "N/A" ]]; then
        TP_FLOAT=$(echo "$INPUT_TP" | tr -d '-')
        TP_INT=${TP_FLOAT%.*}
        if [[ $TP_INT -le 1 ]]; then
            echo -e "   ${RED}⚠️  检测到削波风险 (峰值接近 0 dBTP)${NC}"
            AUDIO_SCORE=$((AUDIO_SCORE - 15))
        fi
    fi
else
    echo -e "   ${YELLOW}⚠️  无音频轨道${NC}"
    AUDIO_SCORE=0
fi

echo ""

# ============================
# 4. 综合评分 + 建议
# ============================
echo -e "${CYAN}📊 综合评分${NC}"

TOTAL_SCORE=$(( (RES_SCORE + BRIGHTNESS_SCORE + AUDIO_SCORE) / 3 ))

# 帧率加分/减分
if [[ $(echo "$FPS_FLOAT" | cut -d. -f1) -ge 24 ]]; then
    TOTAL_SCORE=$((TOTAL_SCORE + 5))
fi

# 码率评估
if [[ $BITRATE_KBPS -gt 8000 ]]; then
    TOTAL_SCORE=$((TOTAL_SCORE + 5))
elif [[ $BITRATE_KBPS -lt 2000 ]]; then
    TOTAL_SCORE=$((TOTAL_SCORE - 10))
fi

[[ $TOTAL_SCORE -gt 100 ]] && TOTAL_SCORE=100
[[ $TOTAL_SCORE -lt 0 ]] && TOTAL_SCORE=0

# 评级
if [[ $TOTAL_SCORE -ge 85 ]]; then
    GRADE="A"; GRADE_COLOR="${GREEN}"
elif [[ $TOTAL_SCORE -ge 70 ]]; then
    GRADE="B"; GRADE_COLOR="${GREEN}"
elif [[ $TOTAL_SCORE -ge 55 ]]; then
    GRADE="C"; GRADE_COLOR="${YELLOW}"
elif [[ $TOTAL_SCORE -ge 40 ]]; then
    GRADE="D"; GRADE_COLOR="${YELLOW}"
else
    GRADE="F"; GRADE_COLOR="${RED}"
fi

echo -e "   分辨率：${GREEN}${RES_SCORE}/100${NC} ($RES_LABEL)"
echo -e "   画面：${GREEN}${BRIGHTNESS_SCORE}/100${NC} ($BRIGHTNESS_NOTE)"
echo -e "   音频：${GREEN}${AUDIO_SCORE}/100${NC}"
echo ""
echo -e "   总分：${GRADE_COLOR}${TOTAL_SCORE}/100 ($GRADE)${NC}"
echo ""

# 改进建议
echo -e "${CYAN}💡 改进建议${NC}"
SUGGESTIONS=()

[[ $RES_SCORE -lt 70 ]] && SUGGESTIONS+=("📐 分辨率偏低，建议至少 720p")
[[ $BRIGHTNESS_SCORE -lt 70 && "$BRIGHTNESS_NOTE" == *"暗"* ]] && SUGGESTIONS+=("🔆 画面偏暗，建议用 auto-color-grade.sh --style fresh 提亮")
[[ $BRIGHTNESS_SCORE -lt 70 && "$BRIGHTNESS_NOTE" == *"曝"* ]] && SUGGESTIONS+=("🔅 画面过曝，建议降低曝光")
[[ $AUDIO_SCORE -lt 70 && $AUDIO_SCORE -gt 0 ]] && SUGGESTIONS+=("🔊 音频响度不标准，建议用 audio-normalizer.sh 标准化到 -23 LUFS")
[[ $AUDIO_SCORE -eq 0 ]] && SUGGESTIONS+=("🔇 无音频轨道，建议添加配音或 BGM")
[[ $BITRATE_KBPS -lt 2000 ]] && SUGGESTIONS+=("📈 码率偏低 (${BITRATE_KBPS}kbps)，画面可能模糊")

if [[ ${#SUGGESTIONS[@]} -eq 0 ]]; then
    echo -e "   ${GREEN}✅ 视频质量良好，无明显问题${NC}"
else
    for s in "${SUGGESTIONS[@]}"; do
        echo -e "   $s"
    done
fi

# === 输出 JSON 报告 ===
if [[ -n "$OUTPUT" ]]; then
    jq -n \
        --arg file "$VIDEO" \
        --argjson width "$WIDTH" \
        --argjson height "$HEIGHT" \
        --arg fps "$FPS_FLOAT" \
        --argjson duration "${DUR_INT}" \
        --arg codec "$CODEC" \
        --arg acodec "$ACODEC" \
        --argjson bitrate_kbps "$BITRATE_KBPS" \
        --arg size_mb "$SIZE_MB" \
        --arg avg_brightness "$AVG_BRIGHTNESS" \
        --arg brightness_note "$BRIGHTNESS_NOTE" \
        --arg color_temp "$COLOR_TEMP" \
        --arg loudness_lufs "${INPUT_I:-N/A}" \
        --arg true_peak "${INPUT_TP:-N/A}" \
        --arg dynamic_range "${INPUT_LRA:-N/A}" \
        --argjson res_score "$RES_SCORE" \
        --argjson brightness_score "$BRIGHTNESS_SCORE" \
        --argjson audio_score "$AUDIO_SCORE" \
        --argjson total_score "$TOTAL_SCORE" \
        --arg grade "$GRADE" \
        '{
            file: $file,
            basic: {width: $width, height: $height, fps: $fps, duration_s: $duration, codec: $codec, audio_codec: $acodec, bitrate_kbps: $bitrate_kbps, size_mb: $size_mb},
            video: {avg_brightness: $avg_brightness, brightness_note: $brightness_note, color_temp: $color_temp},
            audio: {loudness_lufs: $loudness_lufs, true_peak: $true_peak, dynamic_range_lu: $dynamic_range},
            scores: {resolution: $res_score, brightness: $brightness_score, audio: $audio_score, total: $total_score, grade: $grade}
        }' > "$OUTPUT"
    
    echo ""
    echo -e "${GREEN}📄 报告已保存：$OUTPUT${NC}"
fi

echo ""
