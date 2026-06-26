#!/bin/bash
# music-collector.sh - 自动搜索和下载免费背景音乐
#
# 使用方式:
#   bash music-collector.sh --keywords "chill lofi" --count 3 --output ./music
#   bash music-collector.sh --keywords "epic cinematic" --source youtube --count 5
#
# 音乐来源:
#   - pixabay: Pixabay Music (浏览器自动下载，质量高)
#   - youtube: YouTube 搜索免版权音乐 (yt-dlp 下载)
#   - ccmixter: ccMixter API (Creative Commons，直接下载)
#
# 依赖：curl, jq, yt-dlp (YouTube 源)

set -euo pipefail

source "$(dirname "$0")/colors.sh" 2>/dev/null || {
    RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
    BLUE='\033[0;34m'; CYAN='\033[0;36m'; NC='\033[0m'
}

KEYWORDS=""
COUNT=5
OUTPUT_DIR="./music"
SOURCE="ccmixter"    # ccmixter | youtube | pixabay

usage() {
    cat << 'EOF'
用法：music-collector.sh [选项]

必需:
  --keywords, -k      音乐搜索关键词

可选:
  --count, -n         下载数量 (默认：5)
  --output, -o        输出目录 (默认：./music)
  --source, -s        音乐源 (默认：ccmixter)
  --help              显示帮助

音乐源:
  ccmixter     ccMixter (Creative Commons, 免费直接下载)
  youtube      YouTube 搜索免版权音乐 (需要 yt-dlp)
  pixabay      打开 Pixabay Music 页面手动下载

示例:
  # 从 ccMixter 下载轻松音乐
  music-collector.sh -k "chill ambient" -n 3 -o ./bgm

  # 从 YouTube 搜索免版权音乐
  music-collector.sh -k "royalty free cinematic" -s youtube -n 3
EOF
    exit 0
}

while [[ $# -gt 0 ]]; do
    case $1 in
        --keywords|-k) KEYWORDS="$2"; shift 2 ;;
        --count|-n) COUNT="$2"; shift 2 ;;
        --output|-o) OUTPUT_DIR="$2"; shift 2 ;;
        --source|-s) SOURCE="$2"; shift 2 ;;
        --help|-h) usage ;;
        *) echo "未知参数：$1"; usage ;;
    esac
done

if [[ -z "$KEYWORDS" ]]; then
    echo -e "${RED}❌ 必须提供 --keywords 参数${NC}"
    usage
fi

mkdir -p "$OUTPUT_DIR"
META_FILE="$OUTPUT_DIR/music-meta.jsonl"

echo -e "${BLUE}🎵 音乐素材收集器${NC}"
echo -e "关键词：${GREEN}$KEYWORDS${NC}"
echo -e "音乐源：${GREEN}$SOURCE${NC}"
echo -e "数量：${GREEN}$COUNT${NC}"
echo -e "输出：${GREEN}$OUTPUT_DIR${NC}"
echo ""

DOWNLOADED=0
TOTAL_SIZE=0

# ============================
# ccMixter (Creative Commons)
# ============================
download_ccmixter() {
    echo -e "${CYAN}🎵 搜索 ccMixter (Creative Commons)...${NC}"
    
    TAGS=$(echo "$KEYWORDS" | tr ' ' ',')
    RESP=$(curl -s "http://ccmixter.org/api/query?tags=${TAGS}&limit=${COUNT}&f=json" --connect-timeout 10 --max-time 30 2>/dev/null || echo "[]")
    
    HITS=$(echo "$RESP" | jq 'length' 2>/dev/null || echo "0")
    
    if [[ "$HITS" -eq 0 || "$RESP" == "[]" ]]; then
        # 退回到全文搜索
        echo -e "${YELLOW}   标签搜索无结果，尝试全文搜索...${NC}"
        SEARCH_Q=$(echo "$KEYWORDS" | sed 's/ /+/g')
        RESP=$(curl -s "http://ccmixter.org/api/query?search=${SEARCH_Q}&limit=${COUNT}&f=json" --connect-timeout 10 --max-time 30 2>/dev/null || echo "[]")
        HITS=$(echo "$RESP" | jq 'length' 2>/dev/null || echo "0")
    fi
    
    if [[ "$HITS" -eq 0 ]]; then
        echo -e "${YELLOW}⚠️  ccMixter 未找到匹配音乐${NC}"
        return
    fi
    
    echo -e "${GREEN}✅ 找到 $HITS 首音乐${NC}"
    echo ""
    
    for i in $(seq 0 $((HITS - 1))); do
        [[ "$DOWNLOADED" -ge "$COUNT" ]] && break
        
        TITLE=$(echo "$RESP" | jq -r ".[$i].upload_name // \"untitled\"" 2>/dev/null)
        ARTIST=$(echo "$RESP" | jq -r ".[$i].user_name // \"unknown\"" 2>/dev/null)
        LICENSE=$(echo "$RESP" | jq -r ".[$i].license_name // \"CC\"" 2>/dev/null)
        
        # 获取 MP3 下载链接
        DL_URL=$(echo "$RESP" | jq -r ".[$i].files[] | select(.file_format_info.\"format-name\" | test(\"mp3\")) | .download_url" 2>/dev/null | head -1)
        # ccMixter SSL 证书有问题，强制用 http
        DL_URL=$(echo "$DL_URL" | sed 's|^https://|http://|')
        
        if [[ -z "$DL_URL" || "$DL_URL" == "null" ]]; then
            # 尝试从 file_page_url 构建
            FILE_PAGE=$(echo "$RESP" | jq -r ".[$i].file_page_url // empty" 2>/dev/null)
            [[ -z "$FILE_PAGE" ]] && continue
            DL_URL="$FILE_PAGE"
        fi
        
        SAFE_TITLE=$(echo "$TITLE" | sed 's/[^a-zA-Z0-9_-]/_/g' | head -c 40)
        FILENAME="ccm_$(printf '%02d' $((DOWNLOADED + 1)))_${SAFE_TITLE}.mp3"
        OUTPUT_FILE="$OUTPUT_DIR/$FILENAME"
        
        echo -e "${BLUE}⬇️  [$((DOWNLOADED+1))/$COUNT] $TITLE${NC}"
        echo -e "   👤 $ARTIST | 📜 $LICENSE"
        
        if curl -sL "$DL_URL" -o "$OUTPUT_FILE" --connect-timeout 15 --max-time 120 2>/dev/null; then
            FILE_SIZE=$(stat -f%z "$OUTPUT_FILE" 2>/dev/null || echo "0")
            
            if [[ "$FILE_SIZE" -gt 50000 ]]; then
                DOWNLOADED=$((DOWNLOADED + 1))
                TOTAL_SIZE=$((TOTAL_SIZE + FILE_SIZE))
                SIZE_MB=$(echo "scale=1; $FILE_SIZE / 1048576" | bc)
                
                # 检测时长
                DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUTPUT_FILE" 2>/dev/null | cut -d. -f1)
                [[ -n "$DUR" ]] && DUR_FMT="$((DUR/60)):$(printf '%02d' $((DUR%60)))" || DUR_FMT="?"
                
                echo -e "   ${GREEN}✅ $FILENAME (${SIZE_MB}MB, ${DUR_FMT})${NC}"
                
                jq -n \
                    --arg file "$FILENAME" \
                    --arg title "$TITLE" \
                    --arg artist "$ARTIST" \
                    --arg license "$LICENSE" \
                    --arg source "ccMixter" \
                    '{file: $file, title: $title, artist: $artist, license: $license, source: $source}' \
                    >> "$META_FILE"
            else
                rm -f "$OUTPUT_FILE"
                echo -e "   ${YELLOW}⚠️  文件太小，跳过${NC}"
            fi
        else
            echo -e "   ${RED}❌ 下载失败${NC}"
        fi
        
        sleep 0.5
    done
}

# ============================
# YouTube (yt-dlp)
# ============================
download_youtube() {
    if ! command -v yt-dlp &>/dev/null; then
        echo -e "${RED}❌ yt-dlp 未安装${NC}"
        echo -e "${YELLOW}💡 安装：brew install yt-dlp${NC}"
        return
    fi
    
    echo -e "${CYAN}🎵 搜索 YouTube 免版权音乐...${NC}"
    
    SEARCH_Q="royalty free ${KEYWORDS} background music"
    
    echo -e "${BLUE}⬇️  搜索并下载前 $COUNT 首...${NC}"
    echo -e "   搜索词：$SEARCH_Q"
    echo ""
    
    yt-dlp "ytsearch${COUNT}:${SEARCH_Q}" \
        -x --audio-format mp3 --audio-quality 0 \
        -o "${OUTPUT_DIR}/yt_%(autonumber)02d_%(title).40s.%(ext)s" \
        --no-playlist \
        --max-filesize 50M \
        --match-filter "duration < 600" \
        --print "after_move:%(filepath)s" \
        --no-warnings \
        2>&1 | while IFS= read -r line; do
            if [[ -f "$line" ]]; then
                FNAME=$(basename "$line")
                FSIZE=$(stat -f%z "$line" 2>/dev/null | awk '{printf "%.1f", $1/1048576}')
                DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$line" 2>/dev/null | cut -d. -f1)
                [[ -n "$DUR" ]] && DUR_FMT="$((DUR/60)):$(printf '%02d' $((DUR%60)))" || DUR_FMT="?"
                echo -e "   ${GREEN}✅ $FNAME (${FSIZE}MB, ${DUR_FMT})${NC}"
                DOWNLOADED=$((DOWNLOADED + 1))
            fi
        done
    
    # 统计实际下载数
    DOWNLOADED=$(ls "$OUTPUT_DIR"/yt_*.mp3 2>/dev/null | wc -l | tr -d ' ')
}

# ============================
# Pixabay (引导手动下载)
# ============================
download_pixabay() {
    SEARCH_Q=$(echo "$KEYWORDS" | sed 's/ /-/g')
    PIXABAY_URL="https://pixabay.com/music/search/${SEARCH_Q}/"
    
    echo -e "${CYAN}🎵 Pixabay Music${NC}"
    echo ""
    echo -e "${YELLOW}💡 Pixabay 音乐暂不支持 API 下载，请手动操作：${NC}"
    echo ""
    echo -e "   1. 打开：${BLUE}${PIXABAY_URL}${NC}"
    echo -e "   2. 选择喜欢的音乐 → 点击 ⬇️ 下载"
    echo -e "   3. 保存到：${GREEN}$OUTPUT_DIR/${NC}"
    echo ""
    echo -e "${GREEN}✅ Pixabay 音乐完全免费，无需署名${NC}"
    
    # 尝试用系统浏览器打开
    if command -v open &>/dev/null; then
        echo ""
        read -p "   是否打开浏览器？(y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            open "$PIXABAY_URL"
            echo -e "${GREEN}   ✅ 已打开浏览器${NC}"
        fi
    fi
}

# ============================
# 主流程
# ============================
case "$SOURCE" in
    ccmixter|cc) download_ccmixter ;;
    youtube|yt) download_youtube ;;
    pixabay) download_pixabay ;;
    *)
        echo -e "${YELLOW}⚠️  未知源：$SOURCE，使用 ccmixter${NC}"
        download_ccmixter
        ;;
esac

# ============================
# 汇总
# ============================
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# 列出已有的音乐文件
MUSIC_COUNT=0
echo -e "${GREEN}🎵 当前目录中的音乐文件：${NC}"
while IFS= read -r -d '' f; do
    FNAME=$(basename "$f")
    FSIZE=$(stat -f%z "$f" 2>/dev/null | awk '{printf "%.1f", $1/1048576}')
    DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$f" 2>/dev/null | cut -d. -f1)
    [[ -n "$DUR" ]] && DUR_FMT="$((DUR/60)):$(printf '%02d' $((DUR%60)))" || DUR_FMT="?"
    echo -e "   🎵 $FNAME (${FSIZE}MB, ${DUR_FMT})"
    MUSIC_COUNT=$((MUSIC_COUNT + 1))
done < <(find "$OUTPUT_DIR" -maxdepth 1 -type f \( -name '*.mp3' -o -name '*.wav' -o -name '*.m4a' -o -name '*.aac' -o -name '*.ogg' -o -name '*.flac' \) -print0 2>/dev/null)

if [[ "$MUSIC_COUNT" -eq 0 ]]; then
    echo -e "   ${YELLOW}暂无音乐文件${NC}"
fi

echo ""
echo -e "${GREEN}✅ 音乐文件保存在：$OUTPUT_DIR${NC}"
echo -e "${BLUE}💡 下一步：用 auto-bgm-match.sh 自动匹配到视频${NC}"
