#!/bin/bash
#===============================================
# Bilibili Video Downloader - 统一入口脚本
# 支持: Linux, macOS, Windows (Git Bash/WSL)
#===============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLATFORM="$(uname -s)"

# 检测 Windows 环境
is_windows() {
    case "$PLATFORM" in
        CYGWIN*|MINGW*|MSYS*) return 0 ;;
        *) return 1 ;;
    esac
}

# 检测 PowerShell 是否可用
is_powershell() {
    command -v pwsh &> /dev/null || command -v powershell &> /dev/null
}

#===============================================
# 依赖检查
#===============================================
check_dependencies() {
    echo "检查依赖..."
    echo ""
    
    # 检查 Python
    local python_cmd=""
    if command -v python3 &> /dev/null; then
        python_cmd="python3"
    elif command -v python &> /dev/null; then
        python_cmd="python"
    fi
    
    if [ -n "$python_cmd" ]; then
        echo "✅ Python: $($python_cmd --version 2>&1)"
    else
        echo "❌ Python 未安装"
        echo "   下载: https://www.python.org/downloads/"
        exit 1
    fi
    
    # 检查 yt-dlp
    if command -v yt-dlp &> /dev/null; then
        echo "✅ yt-dlp: $(yt-dlp --version 2>&1)"
    else
        echo "⚠️  yt-dlp 未安装"
        echo "   安装: pip install yt-dlp"
        exit 1
    fi
    
    # 检查 ffmpeg
    if command -v ffmpeg &> /dev/null; then
        echo "✅ ffmpeg: $(ffmpeg -version 2>&1 | head -n1)"
    else
        echo "⚠️  ffmpeg 未安装"
        if is_windows; then
            echo "   安装: winget install Gyan.FFmpeg"
        else
            echo "   macOS: brew install ffmpeg"
            echo "   Linux: sudo apt install ffmpeg"
        fi
    fi
    
    echo ""
}

#===============================================
# 搜索视频
#===============================================
cmd_search() {
    local keyword="${1:-}"
    local limit="${2:-10}"
    
    if [ -z "$keyword" ]; then
        echo "用法: $0 search <关键词> [数量]"
        echo "示例: $0 search Python教程 20"
        exit 1
    fi
    
    echo "搜索: $keyword (前 $limit 个结果)"
    echo ""
    
    yt-dlp "ytsearch${limit}:${keyword} site:bilibili.com" \
        --print "%(title)s | %(uploader)s | %(view_count)s views | %(id)s" \
        --quiet 2>/dev/null || echo "搜索失败"
}

#===============================================
# 下载视频
#===============================================
cmd_download() {
    local url="${1:-}"
    local quality="${2:-best}"
    local output_dir="${3:-./downloads}"
    
    if [ -z "$url" ]; then
        echo "用法: $0 download <URL> [清晰度] [输出目录]"
        echo "示例: $0 download https://www.bilibili.com/video/BV1xx411c7mD 1080 ./videos"
        exit 1
    fi
    
    mkdir -p "$output_dir"
    
    echo "下载视频..."
    echo "URL: $url"
    echo "清晰度: $quality"
    echo "保存到: $output_dir"
    echo ""
    
    local format="best"
    case "$quality" in
        4K) format="bestvideo[height<=2160]+bestaudio/best[height<=2160]" ;;
        1080p+|1080+) format="bestvideo[height<=1080]+bestaudio/best[height<=1080]" ;;
        1080) format="bestvideo[height<=1080]+bestaudio/best[height<=1080]" ;;
        720) format="bestvideo[height<=720]+bestaudio/best[height<=720]" ;;
        480) format="bestvideo[height<=480]+bestaudio/best[height<=480]" ;;
        360) format="bestvideo[height<=360]+bestaudio/best[height<=360]" ;;
    esac
    
    yt-dlp "$url" \
        --format "$format" \
        --output "${output_dir}/%(title)s [%(uploader)s].%(ext)s" \
        --merge-output-format mp4 \
        --embed-subs \
        --sub-langs zh-CN,zh-TW,en \
        --cookies cookies.txt 2>/dev/null || \
    yt-dlp "$url" \
        --format "$format" \
        --output "${output_dir}/%(title)s [%(uploader)s].%(ext)s" \
        --merge-output-format mp4
    
    echo ""
    echo "✅ 下载完成！"
}

#===============================================
# 获取视频信息
#===============================================
cmd_info() {
    local url="${1:-}"
    
    if [ -z "$url" ]; then
        echo "用法: $0 info <URL>"
        echo "示例: $0 info https://www.bilibili.com/video/BV1xx411c7mD"
        exit 1
    fi
    
    echo "获取视频信息..."
    echo ""
    
    yt-dlp "$url" --dump-json --quiet 2>/dev/null | python3 -c "
import json, sys, math
data = json.load(sys.stdin)
print(f'标题: {data.get(\"title\", \"N/A\")}')
print(f'UP主: {data.get(\"uploader\", \"N/A\")}')
print(f'播放: {data.get(\"view_count\", \"N/A\")}')
print(f'点赞: {data.get(\"like_count\", \"N/A\")}')
duration = data.get('duration', 0)
print(f'时长: {int(duration//60)}分{int(duration%60)}秒')
print(f'BV号: {data.get(\"id\", \"N/A\")}')
print(f'链接: {data.get(\"webpage_url\", \"N/A\")}')
" || echo "获取失败"
}

#===============================================
# 主程序
#===============================================
main() {
    local cmd="${1:-help}"
    shift 2>/dev/null || true
    
    case "$cmd" in
        check|install-check)
            check_dependencies
            ;;
        search)
            cmd_search "$@"
            ;;
        download)
            cmd_download "$@"
            ;;
        info|video-info)
            cmd_info "$@"
            ;;
        help|--help|-h)
            echo "Bilibili Video Downloader v1.2 (统一版)"
            echo ""
            echo "用法:"
            echo "  $0 check          - 检查依赖"
            echo "  $0 search <关键词> [数量]  - 搜索视频"
            echo "  $0 download <URL> [清晰度] [目录]  - 下载视频"
            echo "  $0 info <URL>     - 获取视频信息"
            echo "  $0 help           - 显示帮助"
            echo ""
            echo "示例:"
            echo "  $0 search Python教程 10"
            echo "  $0 download https://www.bilibili.com/video/BV1xx411c7mD 1080"
            echo ""
            ;;
        *)
            echo "未知命令: $cmd"
            echo "运行 '$0 help' 查看帮助"
            exit 1
            ;;
    esac
}

main "$@"
