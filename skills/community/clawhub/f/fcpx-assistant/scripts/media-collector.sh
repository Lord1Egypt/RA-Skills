#!/bin/bash
# media-collector.sh - 自动搜索和下载免费视频素材 + 背景音乐
# 
# 使用方式:
#   bash media-collector.sh --keywords "nature mountain" --count 5 --output ./project-media
#   bash media-collector.sh --keywords "城市 夜景" --count 3 --orientation portrait --output ./media
#   bash media-collector.sh --keywords "coding technology" --music-keywords "electronic chill" --output ./media
#
# 素材来源: 
#   - Pexels (免费视频) - https://www.pexels.com/api/
#   - Pixabay (免费视频 + 音乐) - https://pixabay.com/api/docs/
#
# API Key: 
#   设置环境变量 PEXELS_API_KEY（免费注册 https://www.pexels.com/api/）
#   设置环境变量 PIXABAY_API_KEY（免费注册 https://pixabay.com/api/docs/）
#   如未设置，使用默认 key（可能有速率限制）

set -euo pipefail

# === 颜色 ===
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# === 默认参数 ===
KEYWORDS=""
MUSIC_KEYWORDS=""
COUNT=5
ORIENTATION="landscape"  # landscape | portrait | square
QUALITY="hd"             # hd | sd | 4k
OUTPUT_DIR="./project-media"
MIN_DURATION=3
MAX_DURATION=30
PEXELS_KEY="${PEXELS_API_KEY:-}"
PIXABAY_KEY="${PIXABAY_API_KEY:-}"
SOURCE="both"            # pexels | pixabay | both

usage() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  --keywords, -k      视频搜索关键词 (必需)"
    echo "  --music-keywords    背景音乐搜索关键词"
    echo "  --count, -n         下载视频数量 (默认: 5)"
    echo "  --orientation, -o   方向: landscape/portrait/square (默认: landscape)"
    echo "  --quality, -q       质量: sd/hd/4k (默认: hd)"
    echo "  --output, -d        输出目录 (默认: ./project-media)"
    echo "  --min-duration      最短时长秒 (默认: 3)"
    echo "  --max-duration      最长时长秒 (默认: 30)"
    echo "  --source, -s        素材源：pexels/pixabay/both (默认: both)"
    echo "  --pexels-key        Pexels API Key"
    echo "  --pixabay-key       Pixabay API Key"
    echo "  --help              显示帮助"
    exit 0
}

# === 解析参数 ===
while [[ $# -gt 0 ]]; do
    case $1 in
        --keywords|-k) KEYWORDS="$2"; shift 2 ;;
        --music-keywords) MUSIC_KEYWORDS="$2"; shift 2 ;;
        --count|-n) COUNT="$2"; shift 2 ;;
        --orientation|-o) ORIENTATION="$2"; shift 2 ;;
        --quality|-q) QUALITY="$2"; shift 2 ;;
        --output|-d) OUTPUT_DIR="$2"; shift 2 ;;
        --min-duration) MIN_DURATION="$2"; shift 2 ;;
        --max-duration) MAX_DURATION="$2"; shift 2 ;;
        --source|-s) SOURCE="$2"; shift 2 ;;
        --pexels-key) PEXELS_KEY="$2"; shift 2 ;;
        --pixabay-key) PIXABAY_KEY="$2"; shift 2 ;;
        --help) usage ;;
        *) echo "未知参数：$1"; usage ;;
    esac
done

if [[ -z "$KEYWORDS" ]]; then
    echo -e "${RED}❌ 必须提供 --keywords 参数${NC}"
    usage
fi

# === 创建目录 ===
VIDEOS_DIR="$OUTPUT_DIR/videos"
MUSIC_DIR="$OUTPUT_DIR/music"
META_DIR="$OUTPUT_DIR/meta"
mkdir -p "$VIDEOS_DIR" "$MUSIC_DIR" "$META_DIR"

echo -e "${BLUE}🎬 素材收集器 (Pexels + Pixabay)${NC}"
echo -e "关键词：${GREEN}$KEYWORDS${NC}"
echo -e "素材源：${GREEN}$SOURCE${NC}"
echo -e "数量：${GREEN}$COUNT${NC}"
echo -e "方向：${GREEN}$ORIENTATION${NC}"
echo -e "质量：${GREEN}$QUALITY${NC}"
echo -e "输出：${GREEN}$OUTPUT_DIR${NC}"
echo ""

# === 确定目标分辨率 ===
case "$ORIENTATION" in
    landscape)
        case "$QUALITY" in
            sd) TARGET_W=854; TARGET_H=480 ;;
            hd) TARGET_W=1280; TARGET_H=720 ;;
            4k) TARGET_W=3840; TARGET_H=2160 ;;
            *) TARGET_W=1920; TARGET_H=1080 ;;
        esac
        ;;
    portrait)
        case "$QUALITY" in
            sd) TARGET_W=480; TARGET_H=854 ;;
            hd) TARGET_W=720; TARGET_H=1280 ;;
            4k) TARGET_W=2160; TARGET_H=3840 ;;
            *) TARGET_W=1080; TARGET_H=1920 ;;
        esac
        ;;
    square)
        case "$QUALITY" in
            sd) TARGET_W=480; TARGET_H=480 ;;
            hd) TARGET_W=720; TARGET_H=720 ;;
            4k) TARGET_W=2160; TARGET_H=2160 ;;
            *) TARGET_W=1080; TARGET_H=1080 ;;
        esac
        ;;
esac

# === 全局计数器 ===
TOTAL_DOWNLOADED=0
ALL_CLIPS_META="[]"

# ============================
# 搜索和下载 Pexels 视频
# ============================

download_pexels() {
    if [[ "$SOURCE" == "pixabay" ]]; then
        return
    fi
    
    echo -e "${BLUE}📹 搜索 Pexels 视频素材...${NC}"
    
    # 多关键词策略：逐词搜索再合并
    KEYWORD_ARRAY=($KEYWORDS)
    ALL_VIDEOS="[]"
    VIDEOS_PER_KEYWORD=$(( (COUNT + ${#KEYWORD_ARRAY[@]} - 1) / ${#KEYWORD_ARRAY[@]} ))
    [[ "$VIDEOS_PER_KEYWORD" -lt 2 ]] && VIDEOS_PER_KEYWORD=2
    
    for kw in "${KEYWORD_ARRAY[@]}"; do
        echo -e "   搜索关键词：${YELLOW}$kw${NC}"
        PEXELS_URL="https://api.pexels.com/videos/search?query=${kw}&per_page=${VIDEOS_PER_KEYWORD}"
        
        KW_RESP=$(curl -s "$PEXELS_URL" \
            -H "Authorization: ${PEXELS_KEY:-pexels}" \
            --connect-timeout 10 \
            --max-time 30 2>/dev/null || echo '{"videos":[]}')
        
        KW_VIDEOS=$(echo "$KW_RESP" | jq '.videos // []' 2>/dev/null || echo '[]')
        KW_COUNT=$(echo "$KW_VIDEOS" | jq 'length' 2>/dev/null || echo "0")
        echo -e "   → 找到 ${KW_COUNT} 个结果"
        
        ALL_VIDEOS=$(echo "$ALL_VIDEOS" "$KW_VIDEOS" | jq -s '.[0] + .[1] | unique_by(.id)' 2>/dev/null || echo "$ALL_VIDEOS")
        sleep 0.3
    done
    
    PEXELS_RESP=$(echo "$ALL_VIDEOS" | jq '{videos: .}')
    VIDEO_COUNT=$(echo "$PEXELS_RESP" | jq '.videos | length' 2>/dev/null || echo "0")
    
    if [[ "$VIDEO_COUNT" -eq 0 ]]; then
        echo -e "${YELLOW}⚠️  Pexels 未找到视频素材${NC}"
        return
    fi
    
    echo -e "${GREEN}✅ Pexels 找到 $VIDEO_COUNT 个视频${NC}"
    echo "$PEXELS_RESP" | jq '.' > "$META_DIR/pexels-search.json" 2>/dev/null
    
    # 下载视频
    local downloaded=0
    for i in $(seq 0 $((VIDEO_COUNT - 1))); do
        [[ "$TOTAL_DOWNLOADED" -ge "$COUNT" ]] && break
        
        VIDEO_ID=$(echo "$PEXELS_RESP" | jq -r ".videos[$i].id")
        VIDEO_DURATION=$(echo "$PEXELS_RESP" | jq -r ".videos[$i].duration")
        VIDEO_USER=$(echo "$PEXELS_RESP" | jq -r ".videos[$i].user.name")
        VIDEO_URL_PAGE=$(echo "$PEXELS_RESP" | jq -r ".videos[$i].url")
        
        # 过滤时长
        if [[ "$VIDEO_DURATION" -lt "$MIN_DURATION" ]] || [[ "$VIDEO_DURATION" -gt "$MAX_DURATION" ]]; then
            echo -e "${YELLOW}⏭️  跳过 #$VIDEO_ID (${VIDEO_DURATION}s)${NC}"
            continue
        fi
        
        # 选择最佳质量
        DOWNLOAD_URL=$(echo "$PEXELS_RESP" | jq -r "
            .videos[$i].video_files 
            | sort_by((.width - $TARGET_W) | if . < 0 then -. else . end) 
            | .[0].link" 2>/dev/null)
        
        [[ -z "$DOWNLOAD_URL" || "$DOWNLOAD_URL" == "null" ]] && \
            DOWNLOAD_URL=$(echo "$PEXELS_RESP" | jq -r ".videos[$i].video_files[0].link")
        
        FILENAME="pexels_$(printf '%02d' $((TOTAL_DOWNLOADED + 1)))_${VIDEO_ID}.mp4"
        OUTPUT_FILE="$VIDEOS_DIR/$FILENAME"
        
        echo -e "${BLUE}⬇️  下载 Pexels #$VIDEO_ID (${VIDEO_DURATION}s)${NC}"
        
        if curl -sL "$DOWNLOAD_URL" -o "$OUTPUT_FILE" --connect-timeout 15 --max-time 120 2>/dev/null; then
            FILE_SIZE=$(stat -f%z "$OUTPUT_FILE" 2>/dev/null || stat -c%s "$OUTPUT_FILE" 2>/dev/null || echo "0")
            if [[ "$FILE_SIZE" -gt 10000 ]]; then
                downloaded=$((downloaded + 1))
                TOTAL_DOWNLOADED=$((TOTAL_DOWNLOADED + 1))
                
                CLIP_META=$(jq -n \
                    --arg file "$FILENAME" \
                    --argjson id "$VIDEO_ID" \
                    --argjson duration "$VIDEO_DURATION" \
                    --arg author "$VIDEO_USER" \
                    --arg source "$VIDEO_URL_PAGE" \
                    --arg platform "pexels" \
                    '{file: $file, id: $id, duration: $duration, author: $author, source: $source, platform: $platform}')
                ALL_CLIPS_META=$(echo "$ALL_CLIPS_META" "$CLIP_META" | jq -s '.[0] + [.[1]]')
                
                echo -e "${GREEN}   ✅ 已保存：$FILENAME${NC}"
            else
                rm -f "$OUTPUT_FILE"
            fi
        fi
        
        sleep 0.5
    done
    
    echo -e "${GREEN}📹 Pexels: 下载了 $downloaded 个视频${NC}"
}

# ============================
# 搜索和下载 Pixabay 视频
# ============================

download_pixabay_videos() {
    if [[ "$SOURCE" == "pexels" ]]; then
        return
    fi
    
    echo -e "${MAGENTA}🎬 搜索 Pixabay 视频素材...${NC}"
    
    KEYWORD_ARRAY=($KEYWORDS)
    VIDEOS_PER_KEYWORD=$(( (COUNT + ${#KEYWORD_ARRAY[@]} - 1) / ${#KEYWORD_ARRAY[@]} ))
    [[ "$VIDEOS_PER_KEYWORD" -lt 2 ]] && VIDEOS_PER_KEYWORD=2
    
    for kw in "${KEYWORD_ARRAY[@]}"; do
        [[ "$TOTAL_DOWNLOADED" -ge "$COUNT" ]] && break
        
        echo -e "   搜索关键词：${YELLOW}$kw${NC}"
        
        # Pixabay API: https://pixabay.com/api/docs/
        PIXABAY_URL="https://pixabay.com/api/videos/?key=${PIXABAY_KEY:-demo}&q=${kw}&per_page=${VIDEOS_PER_KEYWORD}&video_type=all"
        
        PIXABAY_RESP=$(curl -s "$PIXABAY_URL" \
            --connect-timeout 10 \
            --max-time 30 2>/dev/null || echo '{"hits":[]}')
        
        HIT_COUNT=$(echo "$PIXABAY_RESP" | jq '.totalHits // 0' 2>/dev/null || echo "0")
        echo -e "   → 找到 ${HIT_COUNT} 个结果"
        
        if [[ "$HIT_COUNT" -eq 0 ]]; then
            continue
        fi
        
        # 下载视频
        local downloaded=0
        local hits_length=$(echo "$PIXABAY_RESP" | jq '.hits | length' 2>/dev/null || echo "0")
        
        for i in $(seq 0 $((hits_length - 1))); do
            [[ "$TOTAL_DOWNLOADED" -ge "$COUNT" ]] && break
            
            VIDEO_ID=$(echo "$PIXABAY_RESP" | jq -r ".hits[$i].id")
            VIDEO_DURATION=$(echo "$PIXABAY_RESP" | jq -r ".hits[$i].duration")
            VIDEO_USER=$(echo "$PIXABAY_RESP" | jq -r ".hits[$i].user")
            VIDEO_URL_PAGE=$(echo "$PIXABAY_RESP" | jq -r ".hits[$i].url")
            
            # 过滤时长
            if [[ "$VIDEO_DURATION" -lt "$MIN_DURATION" ]] || [[ "$VIDEO_DURATION" -gt "$MAX_DURATION" ]]; then
                echo -e "${YELLOW}⏭️  跳过 #$VIDEO_ID (${VIDEO_DURATION}s)${NC}"
                continue
            fi
            
            # 选择最佳质量 (优先 1080p)
            DOWNLOAD_URL=$(echo "$PIXABAY_RESP" | jq -r ".hits[$i].videos.large.url // .hits[$i].videos.medium.url // .hits[$i].videos.small.url")
            
            [[ -z "$DOWNLOAD_URL" || "$DOWNLOAD_URL" == "null" ]] && continue
            
            FILENAME="pixabay_$(printf '%02d' $((TOTAL_DOWNLOADED + 1)))_${VIDEO_ID}.mp4"
            OUTPUT_FILE="$VIDEOS_DIR/$FILENAME"
            
            echo -e "${MAGENTA}⬇️  下载 Pixabay #$VIDEO_ID (${VIDEO_DURATION}s)${NC}"
            
            if curl -sL "$DOWNLOAD_URL" -o "$OUTPUT_FILE" --connect-timeout 15 --max-time 120 2>/dev/null; then
                FILE_SIZE=$(stat -f%z "$OUTPUT_FILE" 2>/dev/null || stat -c%s "$OUTPUT_FILE" 2>/dev/null || echo "0")
                if [[ "$FILE_SIZE" -gt 10000 ]]; then
                    downloaded=$((downloaded + 1))
                    TOTAL_DOWNLOADED=$((TOTAL_DOWNLOADED + 1))
                    
                    CLIP_META=$(jq -n \
                        --arg file "$FILENAME" \
                        --argjson id "$VIDEO_ID" \
                        --argjson duration "$VIDEO_DURATION" \
                        --arg author "$VIDEO_USER" \
                        --arg source "$VIDEO_URL_PAGE" \
                        --arg platform "pixabay" \
                        '{file: $file, id: $id, duration: $duration, author: $author, source: $source, platform: $platform}')
                    ALL_CLIPS_META=$(echo "$ALL_CLIPS_META" "$CLIP_META" | jq -s '.[0] + [.[1]]')
                    
                    echo -e "${GREEN}   ✅ 已保存：$FILENAME${NC}"
                else
                    rm -f "$OUTPUT_FILE"
                fi
            fi
            
            sleep 0.5
        done
        
        echo -e "${MAGENTA}🎬 Pixabay ($kw): 下载了 $downloaded 个视频${NC}"
        sleep 0.3
    done
}

# ============================
# 搜索和下载 Pixabay 音乐
# ============================

download_pixabay_music() {
    if [[ -z "$MUSIC_KEYWORDS" ]]; then
        return
    fi
    
    echo ""
    echo -e "${BLUE}🎵 搜索 Pixabay 背景音乐...${NC}"
    
    MUSIC_QUERY=$(echo "$MUSIC_KEYWORDS" | sed 's/ /+/g')
    PIXABAY_MUSIC_URL="https://pixabay.com/music/search/${MUSIC_QUERY}/"
    
    # 尝试 API 搜索
    MUSIC_RESP=$(curl -s "https://pixabay.com/api/music/?key=${PIXABAY_KEY:-demo}&q=${MUSIC_QUERY}&per_page=5" 2>/dev/null || echo '{"hits":[]}')
    MUSIC_COUNT=$(echo "$MUSIC_RESP" | jq '.totalHits // 0' 2>/dev/null || echo "0")
    
    if [[ "$MUSIC_COUNT" -gt 0 ]]; then
        echo -e "${GREEN}✅ 找到 $MUSIC_COUNT 首音乐${NC}"
        
        local music_downloaded=0
        local hits_length=$(echo "$MUSIC_RESP" | jq '.hits | length' 2>/dev/null || echo "0")
        
        for i in $(seq 0 $((hits_length - 1))); do
            [[ "$music_downloaded" -ge 3 ]] && break
            
            MUSIC_ID=$(echo "$MUSIC_RESP" | jq -r ".hits[$i].id")
            MUSIC_TITLE=$(echo "$MUSIC_RESP" | jq -r ".hits[$i].title")
            MUSIC_USER=$(echo "$MUSIC_RESP" | jq -r ".hits[$i].user")
            MUSIC_PREVIEW=$(echo "$MUSIC_RESP" | jq -r ".hits[$i].preview_url")
            
            if [[ -z "$MUSIC_PREVIEW" || "$MUSIC_PREVIEW" == "null" ]]; then
                continue
            fi
            
            FILENAME="pixabay_music_$(printf '%02d' $((music_downloaded + 1)))_${MUSIC_ID}.mp3"
            OUTPUT_FILE="$MUSIC_DIR/$FILENAME"
            
            echo -e "${BLUE}⬇️  下载音乐：$MUSIC_TITLE${NC}"
            
            if curl -sL "$MUSIC_PREVIEW" -o "$OUTPUT_FILE" --connect-timeout 15 --max-time 60 2>/dev/null; then
                FILE_SIZE=$(stat -f%z "$OUTPUT_FILE" 2>/dev/null || stat -c%s "$OUTPUT_FILE" 2>/dev/null || echo "0")
                if [[ "$FILE_SIZE" -gt 10000 ]]; then
                    music_downloaded=$((music_downloaded + 1))
                    
                    echo "{\"file\":\"$FILENAME\",\"id\":$MUSIC_ID,\"title\":\"$MUSIC_TITLE\",\"author\":\"$MUSIC_USER\",\"source\":\"Pixabay\",\"license\":\"Pixabay Music License\"}" \
                        | jq '.' >> "$META_DIR/music-meta.jsonl"
                    
                    echo -e "${GREEN}   ✅ 已保存：$FILENAME${NC}"
                else
                    rm -f "$OUTPUT_FILE"
                fi
            fi
            
            sleep 0.3
        done
        
        echo -e "${GREEN}🎵 音乐：下载了 $music_downloaded 首${NC}"
    else
        echo -e "${YELLOW}💡 API 未找到音乐，可以手动下载:${NC}"
        echo -e "   ${BLUE}🔗 Pixabay Music: ${PIXABAY_MUSIC_URL}${NC}"
        echo -e "   ${BLUE}🔗 Free Music Archive: https://freemusicarchive.org/search?quicksearch=${MUSIC_QUERY}${NC}"
        echo -e "   ${BLUE}🔗 Incompetech: https://incompetech.com/music/royalty-free/music.html${NC}"
    fi
}

# ============================
# 主流程
# ============================

download_pexels
download_pixabay_videos
download_pixabay_music

# ============================
# 生成汇总
# ============================

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}📦 素材收集完成！${NC}"
echo ""

# 保存所有 clips 元数据
echo "$ALL_CLIPS_META" | jq '.' > "$META_DIR/all-clips-meta.json" 2>/dev/null

# 列出下载的文件
echo -e "${BLUE}📹 视频素材:${NC}"
if ls "$VIDEOS_DIR"/*.mp4 1>/dev/null 2>&1; then
    for f in "$VIDEOS_DIR"/*.mp4; do
        FNAME=$(basename "$f")
        FSIZE=$(stat -f%z "$f" 2>/dev/null || stat -c%s "$f" 2>/dev/null || echo "0")
        FDURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$f" 2>/dev/null | cut -d. -f1 || echo "?")
        echo -e "   ${FNAME} (${FDURATION}s, $(echo "scale=1; $FSIZE / 1048576" | bc)MB)"
    done
else
    echo -e "   ${YELLOW}无视频文件${NC}"
fi

echo ""
echo -e "${BLUE}🎵 音乐素材:${NC}"
if ls "$MUSIC_DIR"/*.{mp3,wav,m4a,aac} 1>/dev/null 2>&1; then
    for f in "$MUSIC_DIR"/*.{mp3,wav,m4a,aac}; do
        [[ -f "$f" ]] || continue
        FNAME=$(basename "$f")
        echo -e "   $FNAME"
    done
else
    echo -e "   ${YELLOW}请手动添加音乐到 $MUSIC_DIR/${NC}"
fi

echo ""

# 保存项目信息
cat > "$META_DIR/project-info.json" << EOF
{
    "keywords": "$KEYWORDS",
    "music_keywords": "$MUSIC_KEYWORDS",
    "source": "$SOURCE",
    "orientation": "$ORIENTATION",
    "quality": "$QUALITY",
    "target_resolution": "${TARGET_W}x${TARGET_H}",
    "clips_downloaded": $TOTAL_DOWNLOADED,
    "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "videos_dir": "$VIDEOS_DIR",
    "music_dir": "$MUSIC_DIR"
}
EOF

echo -e "${GREEN}✅ 项目信息已保存到 $META_DIR/project-info.json${NC}"
echo -e "${BLUE}下一步：用 auto-video-maker.sh 组装成片！${NC}"
