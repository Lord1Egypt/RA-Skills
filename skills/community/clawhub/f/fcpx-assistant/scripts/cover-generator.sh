#!/bin/bash
# cover-generator.sh - 视频封面图生成
# 从视频关键帧 + 标题文字生成各平台封面图
#
# 使用方式:
#   bash cover-generator.sh --video input.mp4 --title "视频标题" --output ./covers/
#   bash cover-generator.sh --video input.mp4 --title "标题" --platforms bilibili youtube tiktok
#   bash cover-generator.sh --image bg.jpg --title "标题" --style gradient

set -euo pipefail

source "$(dirname "$0")/colors.sh" 2>/dev/null || {
    RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
    BLUE='\033[0;34m'; CYAN='\033[0;36m'; NC='\033[0m'
}

VIDEO=""
IMAGE=""
TITLE=""
SUBTITLE=""
OUTPUT_DIR="./covers"
PLATFORMS=()
ALL_PLATFORMS=false
STYLE="overlay"      # overlay | gradient | solid | blur
FRAME_TIME=""        # 指定截取时间点，空则自动选最佳帧
TEXT_COLOR="white"
FONT="PingFang SC"
FONT_SIZE=72
QUALITY=95

usage() {
    cat << 'EOF'
用法：cover-generator.sh [选项]

必需:
  --title             封面标题文字

背景来源 (二选一):
  --video             从视频截取关键帧
  --image             使用指定图片

可选:
  --subtitle          副标题
  --output, -o        输出目录 (默认：./covers)
  --platforms, -p     目标平台 (可多选)
  --all               所有平台
  --style             文字叠加样式 (见下方)
  --time              视频截取时间点 (如 00:00:05，默认自动选)
  --text-color        文字颜色 (默认：white)
  --font-size         字号 (默认：72)
  --help              显示帮助

平台尺寸:
  bilibili     1146x717  (16:10)
  youtube      1280x720  (16:9)
  tiktok       1080x1920 (9:16)
  xiaohongshu  1080x1440 (3:4)
  xhs-square   1080x1080 (1:1)
  wechat       900x383   (微信视频号)

样式:
  overlay      半透明暗层 + 白字 (默认)
  gradient     底部渐变暗 + 白字
  solid        纯色背景条 + 白字
  blur         模糊背景 + 清晰文字
  clean        无文字，仅截取关键帧

示例:
  # 从视频生成 B站+YouTube 封面
  cover-generator.sh --video video.mp4 --title "10个编程技巧" -p bilibili youtube

  # 用图片 + 渐变样式
  cover-generator.sh --image bg.jpg --title "旅行Vlog" --style gradient --all
EOF
    exit 0
}

get_platform_size() {
    case "$1" in
        bilibili)     echo "1146:717" ;;
        youtube)      echo "1280:720" ;;
        tiktok)       echo "1080:1920" ;;
        xiaohongshu)  echo "1080:1440" ;;
        xhs-square)   echo "1080:1080" ;;
        wechat)       echo "900:383" ;;
        *) echo "" ;;
    esac
}

ALL_PLATFORM_LIST="bilibili youtube tiktok xiaohongshu xhs-square wechat"

while [[ $# -gt 0 ]]; do
    case $1 in
        --video) VIDEO="$2"; shift 2 ;;
        --image) IMAGE="$2"; shift 2 ;;
        --title) TITLE="$2"; shift 2 ;;
        --subtitle) SUBTITLE="$2"; shift 2 ;;
        --output|-o) OUTPUT_DIR="$2"; shift 2 ;;
        --platforms|-p)
            shift
            while [[ $# -gt 0 && ! "$1" =~ ^-- ]]; do
                PLATFORMS+=("$1"); shift
            done
            ;;
        --all) ALL_PLATFORMS=true; shift ;;
        --style) STYLE="$2"; shift 2 ;;
        --time) FRAME_TIME="$2"; shift 2 ;;
        --text-color) TEXT_COLOR="$2"; shift 2 ;;
        --font-size) FONT_SIZE="$2"; shift 2 ;;
        --help|-h) usage ;;
        *) echo "未知参数：$1"; usage ;;
    esac
done

if [[ -z "$TITLE" ]]; then
    echo -e "${RED}❌ 必须提供 --title${NC}"
    usage
fi

if [[ -z "$VIDEO" && -z "$IMAGE" ]]; then
    echo -e "${RED}❌ 必须提供 --video 或 --image${NC}"
    usage
fi

if [[ "$ALL_PLATFORMS" == true ]]; then
    PLATFORMS=($ALL_PLATFORM_LIST)
fi

[[ ${#PLATFORMS[@]} -eq 0 ]] && PLATFORMS=(bilibili youtube)

mkdir -p "$OUTPUT_DIR"

echo -e "${BLUE}🖼️ 视频封面生成器${NC}"
echo -e "标题：${GREEN}$TITLE${NC}"
[[ -n "$SUBTITLE" ]] && echo -e "副标题：${GREEN}$SUBTITLE${NC}"
echo -e "样式：${GREEN}$STYLE${NC}"
echo -e "平台：${GREEN}${#PLATFORMS[@]} 个${NC}"
echo ""

# === 获取背景图 ===
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

BG_IMAGE=""

if [[ -n "$VIDEO" && -f "$VIDEO" ]]; then
    DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$VIDEO" 2>/dev/null)
    DUR_INT=${DURATION%.*}
    
    if [[ -z "$FRAME_TIME" ]]; then
        # 自动选帧：取 1/3 处（通常比开头/结尾更有代表性）
        FRAME_SEC=$((DUR_INT / 3))
        FRAME_TIME="00:$(printf '%02d' $((FRAME_SEC/60))):$(printf '%02d' $((FRAME_SEC%60)))"
    fi
    
    echo -e "${CYAN}📸 截取关键帧 ($FRAME_TIME)...${NC}"
    BG_IMAGE="$TEMP_DIR/frame.jpg"
    ffmpeg -y -ss "$FRAME_TIME" -i "$VIDEO" -vframes 1 -q:v 2 "$BG_IMAGE" -loglevel warning 2>/dev/null
    
    if [[ ! -f "$BG_IMAGE" ]]; then
        echo -e "${RED}❌ 截取帧失败${NC}"
        exit 1
    fi
elif [[ -n "$IMAGE" && -f "$IMAGE" ]]; then
    BG_IMAGE="$IMAGE"
else
    echo -e "${RED}❌ 视频/图片文件不存在${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 背景图就绪${NC}"
echo ""

# === 逐平台生成封面 ===
GENERATED=0

for PLATFORM in "${PLATFORMS[@]}"; do
    SIZE=$(get_platform_size "$PLATFORM")
    
    if [[ -z "$SIZE" ]]; then
        echo -e "${YELLOW}⚠️  未知平台：$PLATFORM，跳过${NC}"
        continue
    fi
    
    TGT_W=$(echo "$SIZE" | cut -d: -f1)
    TGT_H=$(echo "$SIZE" | cut -d: -f2)
    
    OUT_FILE="$OUTPUT_DIR/cover-${PLATFORM}.jpg"
    
    echo -e "${BLUE}🖼️ $PLATFORM (${TGT_W}x${TGT_H})${NC}"
    
    # 基础：缩放+裁切到目标尺寸
    BASE_VF="scale=${TGT_W}:${TGT_H}:force_original_aspect_ratio=increase,crop=${TGT_W}:${TGT_H}"
    
    # 文字位置
    TITLE_FS=$FONT_SIZE
    SUB_FS=$((FONT_SIZE * 5 / 10))
    
    # 竖屏适配：字号缩小
    if [[ $TGT_H -gt $TGT_W ]]; then
        TITLE_FS=$((FONT_SIZE * 8 / 10))
        SUB_FS=$((FONT_SIZE * 4 / 10))
    fi
    
    case "$STYLE" in
        overlay)
            # 半透明暗层
            VF="${BASE_VF},drawbox=x=0:y=0:w=${TGT_W}:h=${TGT_H}:color=black@0.4:t=fill"
            VF="${VF},drawtext=text='${TITLE}':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=${TITLE_FS}:fontcolor=${TEXT_COLOR}:x=(w-text_w)/2:y=(h-text_h)/2"
            if [[ -n "$SUBTITLE" ]]; then
                VF="${VF},drawtext=text='${SUBTITLE}':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=${SUB_FS}:fontcolor=${TEXT_COLOR}@0.8:x=(w-text_w)/2:y=(h-text_h)/2+${TITLE_FS}"
            fi
            ;;
        gradient)
            # 底部渐变暗
            VF="${BASE_VF},drawbox=x=0:y=ih*0.6:w=${TGT_W}:h=ih*0.4:color=black@0.7:t=fill"
            VF="${VF},drawtext=text='${TITLE}':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=${TITLE_FS}:fontcolor=${TEXT_COLOR}:x=(w-text_w)/2:y=h*0.72"
            if [[ -n "$SUBTITLE" ]]; then
                VF="${VF},drawtext=text='${SUBTITLE}':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=${SUB_FS}:fontcolor=${TEXT_COLOR}@0.8:x=(w-text_w)/2:y=h*0.72+${TITLE_FS}+10"
            fi
            ;;
        solid)
            # 底部纯色条
            VF="${BASE_VF},drawbox=x=0:y=ih*0.75:w=${TGT_W}:h=ih*0.25:color=black@0.85:t=fill"
            VF="${VF},drawtext=text='${TITLE}':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=${TITLE_FS}:fontcolor=${TEXT_COLOR}:x=(w-text_w)/2:y=h*0.82"
            ;;
        blur)
            # 模糊背景 + 清晰文字
            VF="${BASE_VF},boxblur=15:5"
            VF="${VF},drawtext=text='${TITLE}':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=${TITLE_FS}:fontcolor=${TEXT_COLOR}:borderw=3:bordercolor=black:x=(w-text_w)/2:y=(h-text_h)/2"
            if [[ -n "$SUBTITLE" ]]; then
                VF="${VF},drawtext=text='${SUBTITLE}':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=${SUB_FS}:fontcolor=${TEXT_COLOR}@0.8:borderw=2:bordercolor=black:x=(w-text_w)/2:y=(h-text_h)/2+${TITLE_FS}"
            fi
            ;;
        clean)
            # 纯截图，无文字
            VF="${BASE_VF}"
            ;;
        *)
            echo -e "${YELLOW}⚠️  未知样式：$STYLE，使用 overlay${NC}"
            VF="${BASE_VF}"
            ;;
    esac
    
    if ffmpeg -y -i "$BG_IMAGE" -vf "$VF" -q:v $((100 - QUALITY + 2)) "$OUT_FILE" -loglevel warning 2>/dev/null; then
        FILE_SIZE=$(stat -f%z "$OUT_FILE" 2>/dev/null | awk '{printf "%.0f", $1/1024}')
        echo -e "   ${GREEN}✅ cover-${PLATFORM}.jpg (${FILE_SIZE}KB)${NC}"
        GENERATED=$((GENERATED + 1))
    else
        echo -e "   ${RED}❌ 生成失败${NC}"
    fi
done

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🖼️ 封面生成完成！${NC}"
echo -e "   成功：${GREEN}${GENERATED}/${#PLATFORMS[@]}${NC} 个平台"
echo ""

for f in "$OUTPUT_DIR"/cover-*.jpg; do
    [[ -f "$f" ]] || continue
    FNAME=$(basename "$f")
    RES=$(ffprobe -v quiet -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$f" 2>/dev/null)
    FSIZE=$(stat -f%z "$f" 2>/dev/null | awk '{printf "%.0f", $1/1024}')
    echo -e "   📁 $FNAME (${RES}, ${FSIZE}KB)"
done

echo ""
echo -e "${GREEN}✅ 所有封面保存在：$OUTPUT_DIR${NC}"
