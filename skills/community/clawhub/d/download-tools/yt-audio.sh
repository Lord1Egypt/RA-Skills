#!/bin/bash

# =============================================================================
# YouTube 音频下载工具 v2.0
# =============================================================================
# 使用方法: 
#   ./yt-audio.sh "YouTube链接" [输出文件名]
#   
# 示例:
#   ./yt-audio.sh "https://www.youtube.com/watch?v=xxx"
#   ./yt-audio.sh "https://www.youtube.com/watch?v=xxx" my_audio
# =============================================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "============================================"
echo "   YouTube 音频下载工具"
echo "============================================"
echo ""

# 检查依赖
check_dependencies() {
    echo "🔧 检查依赖..."
    
    if ! command -v yt-dlp &> /dev/null; then
        echo -e "${RED}错误: yt-dlp 未安装${NC}"
        echo "安装方法: brew install yt-dlp"
        exit 1
    fi
    
    if ! command -v ffmpeg &> /dev/null; then
        echo -e "${RED}错误: ffmpeg 未安装${NC}"
        echo "安装方法: brew install ffmpeg"
        exit 1
    fi
    
    # 检查 Node.js (用于 YouTube)
    if ! command -v node &> /dev/null; then
        echo -e "${YELLOW}警告: Node.js 未安装，建议安装以提高成功率${NC}"
        echo "安装方法: brew install node"
    fi
    
    echo -e "${GREEN}✅ 依赖检查完成${NC}"
    echo ""
}

# 检查参数
check_args() {
    if [ -z "$1" ]; then
        echo "使用方法: $0 <YouTube链接> [输出文件名]"
        echo ""
        echo "参数说明:"
        echo "  YouTube链接 : YouTube 视频 URL (必需)"
        echo "  输出文件名 : 输出的音频文件名，不含扩展名 (可选，默认: audio)"
        echo ""
        echo "示例:"
        echo "  $0 \"https://www.youtube.com/watch?v=xxx\""
        echo "  $0 \"https://www.youtube.com/watch?v=xxx\" my_podcast"
        exit 1
    fi
}

# 下载音频
download_audio() {
    local URL="$1"
    local OUTPUT_NAME="$2"
    
    echo "📥 准备下载..."
    echo "   链接: $URL"
    echo "   输出: ${OUTPUT_NAME}.mp3"
    echo ""
    
    # 尝试多种方法下载
    local METHODS=(
        # 方法1: 使用 Android 客户端
        "--extractor-args youtube:player_client=android"
        # 方法2: 使用默认客户端
        ""
        # 方法3: 使用 Web Safari
        "--extractor-args youtube:player_client=web,default"
    )
    
    local success=false
    
    for method in "${METHODS[@]}"; do
        echo -e "${YELLOW}尝试下载方法...${NC}"
        
        if [ -z "$method" ]; then
            echo "使用默认方法"
        else
            echo "使用: $method"
        fi
        
        if yt-dlp -x --audio-format mp3 \
            --audio-quality 0 \
            --embed-thumbnail \
            --add-metadata \
            -o "${OUTPUT_NAME}.%(ext)s" \
            $method \
            "$URL" \
            --no-playlist \
            2>&1; then
            success=true
            break
        fi
        
        echo -e "${YELLOW}此方法失败，尝试下一个...${NC}"
        echo ""
    done
    
    if [ "$success" = true ]; then
        echo ""
        echo -e "${GREEN}✅ 下载完成!${NC}"
        echo "📁 文件位置: $(pwd)/${OUTPUT_NAME}.mp3"
        echo "📊 文件大小: $(ls -lh "${OUTPUT_NAME}.mp3" 2>/dev/null | awk '{print $5}')"
    else
        echo ""
        echo -e "${RED}❌ 下载失败${NC}"
        echo ""
        echo "可能的原因和解决方案:"
        echo ""
        echo "1. YouTube 限制了此视频的下载"
        echo "   - 尝试使用浏览器 cookie"
        echo "   - 使用: --cookies-from-browser chrome"
        echo ""
        echo "2. 需要登录 YouTube Premium"
        echo "   - 部分视频只有 Premium 用户才能下载"
        echo ""
        echo "3. 网络问题"
        echo "   - 尝试使用代理: --proxy \"socks5://127.0.0.1:1080\""
        echo ""
        echo "4. 更新 yt-dlp"
        echo "   - pip install -U yt-dlp"
        echo ""
        
        exit 1
    fi
}

# 主程序
main() {
    check_dependencies
    check_args "$@"
    
    local URL="$1"
    local OUTPUT_NAME="${2:-audio}"
    
    download_audio "$URL" "$OUTPUT_NAME"
}

main "$@"
