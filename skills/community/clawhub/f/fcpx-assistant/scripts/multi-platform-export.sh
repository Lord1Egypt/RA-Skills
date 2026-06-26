#!/bin/bash
# multi-platform-export.sh - 多平台适配导出
# 一个视频导出多种尺寸，适配各平台
#
# 使用方式:
#   bash multi-platform-export.sh input.mp4 --platforms youtube tiktok bilibili
#   bash multi-platform-export.sh input.mp4 --all --output ./exports/

set -euo pipefail

source "$(dirname "$0")/colors.sh" 2>/dev/null || {
    RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
    BLUE='\033[0;34m'; CYAN='\033[0;36m'; NC='\033[0m'
}

VIDEO=""
OUTPUT_DIR=""
PLATFORMS=()
ALL_PLATFORMS=false
CROP_MODE="pad"      # pad (加黑边) | crop (智能裁切) | fit (缩放适配)
QUALITY="high"       # low | medium | high

usage() {
    cat << 'EOF'
用法：multi-platform-export.sh <视频文件> [选项]

选项:
  --platforms, -p     目标平台 (可多选，见下方列表)
  --all               导出所有平台格式
  --output, -o        输出目录 (默认：./exports)
  --mode              适配模式：pad (加黑边) / crop (智能裁切) / fit (缩放) (默认：pad)
  --quality, -q       质量：low / medium / high (默认：high)
  --help              显示帮助

支持的平台:
  youtube      16:9  1920x1080  (横屏)
  bilibili     16:9  1920x1080  (横屏)
  tiktok       9:16  1080x1920  (竖屏)
  reels        9:16  1080x1920  (竖屏/Instagram Reels)
  shorts       9:16  1080x1920  (竖屏/YouTube Shorts)
  xiaohongshu  3:4   1080x1440  (小红书竖屏)
  xhs-square   1:1   1080x1080  (小红书方形)
  twitter      16:9  1280x720   (横屏)
  wechat       16:9  1920x1080  (视频号横屏)
  wechat-v     9:16  1080x1920  (视频号竖屏)

示例:
  # 导出抖音 + B站
  multi-platform-export.sh video.mp4 -p tiktok bilibili

  # 导出所有平台，智能裁切
  multi-platform-export.sh video.mp4 --all --mode crop
EOF
    exit 0
}

# === 平台预设 ===
get_platform_spec() {
    local platform="$1"
    case "$platform" in
        youtube)      echo "1920:1080:16:9:YouTube" ;;
        bilibili)     echo "1920:1080:16:9:Bilibili" ;;
        tiktok)       echo "1080:1920:9:16:TikTok" ;;
        reels)        echo "1080:1920:9:16:Instagram_Reels" ;;
        shorts)       echo "1080:1920:9:16:YouTube_Shorts" ;;
        xiaohongshu)  echo "1080:1440:3:4:小红书" ;;
        xhs-square)   echo "1080:1080:1:1:小红书方形" ;;
        twitter)      echo "1280:720:16:9:Twitter" ;;
        wechat)       echo "1920:1080:16:9:微信视频号" ;;
        wechat-v)     echo "1080:1920:9:16:微信视频号竖屏" ;;
        *) echo "" ;;
    esac
}

ALL_PLATFORM_LIST="youtube bilibili tiktok reels shorts xiaohongshu xhs-square twitter wechat wechat-v"

# === 解析参数 ===
while [[ $# -gt 0 ]]; do
    case $1 in
        --platforms|-p)
            shift
            while [[ $# -gt 0 && ! "$1" =~ ^-- ]]; do
                PLATFORMS+=("$1"); shift
            done
            ;;
        --all) ALL_PLATFORMS=true; shift ;;
        --output|-o) OUTPUT_DIR="$2"; shift 2 ;;
        --mode) CROP_MODE="$2"; shift 2 ;;
        --quality|-q) QUALITY="$2"; shift 2 ;;
        --help|-h) usage ;;
        -*)
            echo "未知参数：$1"; usage ;;
        *)
            if [[ -z "$VIDEO" ]]; then VIDEO="$1"; fi
            shift ;;
    esac
done

if [[ -z "$VIDEO" ]]; then
    echo -e "${RED}❌ 必须提供视频文件${NC}"
    usage
fi

if [[ ! -f "$VIDEO" ]]; then
    echo -e "${RED}❌ 文件不存在：$VIDEO${NC}"
    exit 1
fi

if [[ "$ALL_PLATFORMS" == true ]]; then
    PLATFORMS=($ALL_PLATFORM_LIST)
fi

if [[ ${#PLATFORMS[@]} -eq 0 ]]; then
    echo -e "${RED}❌ 必须指定 --platforms 或 --all${NC}"
    usage
fi

[[ -z "$OUTPUT_DIR" ]] && OUTPUT_DIR="$(dirname "$VIDEO")/exports"
mkdir -p "$OUTPUT_DIR"

# === 获取源视频信息 ===
SRC_W=$(ffprobe -v quiet -select_streams v:0 -show_entries stream=width -of csv=p=0 "$VIDEO" 2>/dev/null)
SRC_H=$(ffprobe -v quiet -select_streams v:0 -show_entries stream=height -of csv=p=0 "$VIDEO" 2>/dev/null)
SRC_DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$VIDEO" 2>/dev/null)

echo -e "${BLUE}📱 多平台适配导出${NC}"
echo -e "源视频：${GREEN}${SRC_W}x${SRC_H}${NC} | ${GREEN}${SRC_DUR%.*}s${NC}"
echo -e "适配模式：${GREEN}$CROP_MODE${NC}"
echo -e "导出平台：${GREEN}${#PLATFORMS[@]} 个${NC}"
echo ""

# === 质量参数 ===
case "$QUALITY" in
    low)    CRF=28; PRESET="fast"; ABITRATE="128k" ;;
    medium) CRF=23; PRESET="medium"; ABITRATE="192k" ;;
    high)   CRF=18; PRESET="slow"; ABITRATE="256k" ;;
    *) CRF=23; PRESET="medium"; ABITRATE="192k" ;;
esac

# === 逐平台导出 ===
EXPORTED=0

for PLATFORM in "${PLATFORMS[@]}"; do
    SPEC=$(get_platform_spec "$PLATFORM")
    
    if [[ -z "$SPEC" ]]; then
        echo -e "${YELLOW}⚠️  未知平台：$PLATFORM，跳过${NC}"
        continue
    fi
    
    IFS=':' read -r TGT_W TGT_H RATIO_W RATIO_H LABEL <<< "$SPEC"
    
    BASENAME=$(basename "${VIDEO%.*}")
    OUT_FILE="$OUTPUT_DIR/${BASENAME}-${PLATFORM}.mp4"
    
    echo -e "${BLUE}📱 [$((EXPORTED+1))/${#PLATFORMS[@]}] $LABEL (${TGT_W}x${TGT_H}, ${RATIO_W}:${RATIO_H})${NC}"
    
    # 构建 video filter
    case "$CROP_MODE" in
        pad)
            # 缩放到目标尺寸内，不足部分加黑边
            VF="scale=${TGT_W}:${TGT_H}:force_original_aspect_ratio=decrease,pad=${TGT_W}:${TGT_H}:(ow-iw)/2:(oh-ih)/2:black"
            ;;
        crop)
            # 缩放后居中裁切
            VF="scale=${TGT_W}:${TGT_H}:force_original_aspect_ratio=increase,crop=${TGT_W}:${TGT_H}"
            ;;
        fit)
            # 直接缩放（可能变形）
            VF="scale=${TGT_W}:${TGT_H}"
            ;;
    esac
    
    if ffmpeg -y -i "$VIDEO" \
        -vf "$VF" \
        -c:v libx264 -crf "$CRF" -preset "$PRESET" \
        -c:a aac -b:a "$ABITRATE" \
        "$OUT_FILE" \
        -loglevel warning 2>/dev/null; then
        
        FILE_SIZE=$(stat -f%z "$OUT_FILE" 2>/dev/null | awk '{printf "%.1f", $1/1048576}')
        echo -e "   ${GREEN}✅ ${BASENAME}-${PLATFORM}.mp4 (${FILE_SIZE}MB)${NC}"
        EXPORTED=$((EXPORTED + 1))
    else
        echo -e "   ${RED}❌ 导出失败${NC}"
    fi
done

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}📱 多平台导出完成！${NC}"
echo -e "   成功：${GREEN}${EXPORTED}/${#PLATFORMS[@]}${NC} 个平台"
echo ""

for f in "$OUTPUT_DIR"/*.mp4; do
    [[ -f "$f" ]] || continue
    FNAME=$(basename "$f")
    FSIZE=$(stat -f%z "$f" 2>/dev/null | awk '{printf "%.1f", $1/1048576}')
    RES=$(ffprobe -v quiet -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$f" 2>/dev/null)
    echo -e "   📁 $FNAME (${RES}, ${FSIZE}MB)"
done

echo ""
echo -e "${GREEN}✅ 所有文件保存在：$OUTPUT_DIR${NC}"
