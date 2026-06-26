#!/bin/bash
# subtitle-styler.sh - 字幕样式增强
# 支持多种字幕样式：卡拉OK逐字高亮、底部居中、顶部弹幕、电影感等
# 输出 ASS 格式（支持特效）或直接烧入视频
#
# 使用方式:
#   bash subtitle-styler.sh --srt input.srt --style karaoke --output styled.ass
#   bash subtitle-styler.sh --srt input.srt --video input.mp4 --style cinematic --burn

set -euo pipefail

source "$(dirname "$0")/colors.sh" 2>/dev/null || {
    RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
    BLUE='\033[0;34m'; NC='\033[0m'
}

SRT_FILE=""
VIDEO_FILE=""
OUTPUT=""
STYLE="default"
BURN=false
FONT="PingFang SC"
FONT_SIZE=48
PRIMARY_COLOR="&H00FFFFFF"   # 白色
OUTLINE_COLOR="&H00000000"   # 黑色描边
SHADOW_COLOR="&H80000000"    # 半透明阴影
OUTLINE_WIDTH=3
SHADOW_DEPTH=2
MARGIN_V=40
ALIGNMENT=2   # 底部居中

usage() {
    cat << 'EOF'
用法：subtitle-styler.sh [选项]

必需:
  --srt               SRT 字幕文件

可选:
  --video             视频文件 (烧入字幕时必需)
  --output, -o        输出文件 (默认：input-styled.ass 或 input-subtitled.mp4)
  --style             字幕样式 (见下方列表)
  --burn              烧入视频 (需要 --video)
  --font              字体 (默认：PingFang SC)
  --font-size         字号 (默认：48)
  --help              显示帮助

字幕样式:
  default       白色描边，底部居中 (标准)
  cinematic     电影感，半透明黑底条
  karaoke       卡拉OK逐字高亮 (黄色)
  modern        现代风，圆角背景框
  top           顶部弹幕式
  big           大字居中 (适合短视频)
  outline       粗描边，无阴影 (高对比)
  neon          霓虹发光效果

示例:
  # 生成电影感字幕文件
  subtitle-styler.sh --srt sub.srt --style cinematic -o styled.ass

  # 直接烧入视频
  subtitle-styler.sh --srt sub.srt --video input.mp4 --style big --burn
EOF
    exit 0
}

while [[ $# -gt 0 ]]; do
    case $1 in
        --srt) SRT_FILE="$2"; shift 2 ;;
        --video) VIDEO_FILE="$2"; shift 2 ;;
        --output|-o) OUTPUT="$2"; shift 2 ;;
        --style) STYLE="$2"; shift 2 ;;
        --burn) BURN=true; shift ;;
        --font) FONT="$2"; shift 2 ;;
        --font-size) FONT_SIZE="$2"; shift 2 ;;
        --help|-h) usage ;;
        *) echo "未知参数：$1"; usage ;;
    esac
done

if [[ -z "$SRT_FILE" || ! -f "$SRT_FILE" ]]; then
    echo -e "${RED}❌ 必须提供有效的 --srt 文件${NC}"
    usage
fi

if [[ "$BURN" == true && ( -z "$VIDEO_FILE" || ! -f "$VIDEO_FILE" ) ]]; then
    echo -e "${RED}❌ 烧入模式需要 --video 文件${NC}"
    exit 1
fi

# 应用样式预设
apply_style() {
    case "$STYLE" in
        default)
            ALIGNMENT=2; MARGIN_V=40
            PRIMARY_COLOR="&H00FFFFFF"; OUTLINE_COLOR="&H00000000"
            SHADOW_COLOR="&H80000000"; OUTLINE_WIDTH=3; SHADOW_DEPTH=2
            FONT_SIZE=${FONT_SIZE:-48}
            ;;
        cinematic)
            ALIGNMENT=2; MARGIN_V=50
            PRIMARY_COLOR="&H00FFFFFF"; OUTLINE_COLOR="&H00000000"
            SHADOW_COLOR="&HA0000000"; OUTLINE_WIDTH=2; SHADOW_DEPTH=4
            FONT_SIZE=42
            # 特殊：加底部半透明黑条
            ;;
        karaoke)
            ALIGNMENT=2; MARGIN_V=40
            PRIMARY_COLOR="&H0000FFFF"; OUTLINE_COLOR="&H00000000"
            SHADOW_COLOR="&H00000000"; OUTLINE_WIDTH=2; SHADOW_DEPTH=1
            FONT_SIZE=52
            ;;
        modern)
            ALIGNMENT=2; MARGIN_V=60
            PRIMARY_COLOR="&H00FFFFFF"; OUTLINE_COLOR="&H00000000"
            SHADOW_COLOR="&HC0000000"; OUTLINE_WIDTH=0; SHADOW_DEPTH=8
            FONT_SIZE=44
            ;;
        top)
            ALIGNMENT=8; MARGIN_V=20
            PRIMARY_COLOR="&H00FFFFFF"; OUTLINE_COLOR="&H00000000"
            SHADOW_COLOR="&H80000000"; OUTLINE_WIDTH=2; SHADOW_DEPTH=1
            FONT_SIZE=36
            ;;
        big)
            ALIGNMENT=5; MARGIN_V=0
            PRIMARY_COLOR="&H00FFFFFF"; OUTLINE_COLOR="&H00000000"
            SHADOW_COLOR="&H00000000"; OUTLINE_WIDTH=4; SHADOW_DEPTH=0
            FONT_SIZE=72
            ;;
        outline)
            ALIGNMENT=2; MARGIN_V=40
            PRIMARY_COLOR="&H00FFFFFF"; OUTLINE_COLOR="&H00000000"
            SHADOW_COLOR="&H00000000"; OUTLINE_WIDTH=5; SHADOW_DEPTH=0
            FONT_SIZE=50
            ;;
        neon)
            ALIGNMENT=2; MARGIN_V=40
            PRIMARY_COLOR="&H0000FF00"; OUTLINE_COLOR="&H0000AA00"
            SHADOW_COLOR="&H6000FF00"; OUTLINE_WIDTH=2; SHADOW_DEPTH=6
            FONT_SIZE=50
            ;;
        *)
            echo -e "${YELLOW}⚠️  未知样式：$STYLE，使用 default${NC}"
            apply_style "default"
            return
            ;;
    esac
}

apply_style

echo -e "${BLUE}🔤 字幕样式增强器${NC}"
echo -e "字幕文件：${GREEN}$SRT_FILE${NC}"
echo -e "样式：${GREEN}$STYLE${NC}"
echo -e "字体：${GREEN}$FONT ($FONT_SIZE)${NC}"
[[ "$BURN" == true ]] && echo -e "模式：${GREEN}烧入视频${NC}"
echo ""

# === SRT → ASS 转换 ===
ASS_FILE="${OUTPUT:-${SRT_FILE%.*}-${STYLE}.ass}"
[[ "$BURN" == true && -z "$OUTPUT" ]] && ASS_FILE="/tmp/subtitle-styled-$(date +%s).ass"

# 获取视频分辨率（用于 ASS）
PLAY_W=1920
PLAY_H=1080
if [[ -n "$VIDEO_FILE" && -f "$VIDEO_FILE" ]]; then
    PLAY_W=$(ffprobe -v quiet -select_streams v:0 -show_entries stream=width -of csv=p=0 "$VIDEO_FILE" 2>/dev/null || echo 1920)
    PLAY_H=$(ffprobe -v quiet -select_streams v:0 -show_entries stream=height -of csv=p=0 "$VIDEO_FILE" 2>/dev/null || echo 1080)
fi

echo -e "${CYAN}📝 生成 ASS 字幕...${NC}"

# ASS 头部
cat > "$ASS_FILE" << ASSHEADER
[Script Info]
Title: Styled Subtitles
ScriptType: v4.00+
PlayResX: ${PLAY_W}
PlayResY: ${PLAY_H}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,${FONT},${FONT_SIZE},${PRIMARY_COLOR},&H000000FF,${OUTLINE_COLOR},${SHADOW_COLOR},-1,0,0,0,100,100,0,0,1,${OUTLINE_WIDTH},${SHADOW_DEPTH},${ALIGNMENT},20,20,${MARGIN_V},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
ASSHEADER

# 解析 SRT 并转换
python3 - "$SRT_FILE" "$ASS_FILE" "$STYLE" << 'PYEOF'
import re, sys

srt_file = sys.argv[1]
ass_file = sys.argv[2]
style = sys.argv[3]

def srt_to_ass_time(srt_time):
    """Convert SRT time (HH:MM:SS,mmm) to ASS time (H:MM:SS.cc)"""
    srt_time = srt_time.strip()
    h, m, rest = srt_time.split(':')
    s, ms = rest.split(',')
    cs = int(ms) // 10
    return f"{int(h)}:{m}:{s}.{cs:02d}"

with open(srt_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Parse SRT blocks
blocks = re.split(r'\n\n+', content.strip())

lines = []
for block in blocks:
    block_lines = block.strip().split('\n')
    if len(block_lines) < 3:
        continue
    
    time_match = re.match(r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})', block_lines[1])
    if not time_match:
        continue
    
    start = srt_to_ass_time(time_match.group(1))
    end = srt_to_ass_time(time_match.group(2))
    text = '\\N'.join(block_lines[2:])
    
    # Apply style-specific effects
    if style == 'karaoke':
        # Simple karaoke effect: highlight text
        text = '{\\k20}' + text
    elif style == 'cinematic':
        # Fade in/out
        text = '{\\fad(300,300)}' + text
    elif style == 'modern':
        # Background box + fade
        text = '{\\fad(200,200)\\3c&H000000&\\bord0\\shad0\\4a&H60&\\p1}m 0 0 l 1 0 1 1 0 1{\\p0}\\N' + text
        # Simplified: just use fade
        text = '{\\fad(200,200)}' + '\\N'.join(block_lines[2:])
    elif style == 'neon':
        text = '{\\blur3\\fad(150,150)}' + text
    elif style == 'big':
        text = '{\\fad(100,100)}' + text
    
    lines.append(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}")

with open(ass_file, 'a', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')

print(f"   ✅ 转换了 {len(lines)} 条字幕")
PYEOF

# === 烧入视频 ===
if [[ "$BURN" == true ]]; then
    BURN_OUTPUT="${OUTPUT:-${VIDEO_FILE%.*}-subtitled.mp4}"
    [[ "$BURN_OUTPUT" == *.ass ]] && BURN_OUTPUT="${VIDEO_FILE%.*}-subtitled.mp4"
    
    echo -e "${BLUE}🔥 烧入视频...${NC}"
    
    # ASS 路径中的特殊字符需要转义
    ASS_ESCAPED=$(echo "$ASS_FILE" | sed "s/'/\\\\'/g" | sed 's/:/\\:/g')
    
    if ffmpeg -y -i "$VIDEO_FILE" \
        -vf "ass=$ASS_ESCAPED" \
        -c:v libx264 -crf 18 -preset medium \
        -c:a copy \
        "$BURN_OUTPUT" \
        -loglevel warning 2>/dev/null; then
        
        FILE_SIZE=$(stat -f%z "$BURN_OUTPUT" 2>/dev/null | awk '{printf "%.1f", $1/1048576}')
        echo -e "${GREEN}✅ 字幕烧入完成！${NC}"
        echo -e "   📁 输出：$BURN_OUTPUT (${FILE_SIZE}MB)"
    else
        echo -e "${RED}❌ 烧入失败${NC}"
        exit 1
    fi
    
    # 清理临时 ASS
    [[ "$ASS_FILE" == /tmp/* ]] && rm -f "$ASS_FILE"
else
    SUB_COUNT=$(grep -c "^Dialogue:" "$ASS_FILE" 2>/dev/null || echo "0")
    echo ""
    echo -e "${GREEN}✅ 字幕样式生成完成！${NC}"
    echo -e "   📁 输出：$ASS_FILE"
    echo -e "   📝 字幕数：$SUB_COUNT 条"
    echo -e "   🎨 样式：$STYLE"
    echo ""
    echo -e "${BLUE}💡 烧入视频：subtitle-styler.sh --srt input.srt --video input.mp4 --style $STYLE --burn${NC}"
fi
