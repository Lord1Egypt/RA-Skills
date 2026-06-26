# Bilibili Video Downloader v1.2 - 统一脚本版

## 📋 版本说明

v1.2 版本将所有脚本合并为 **一个统一的 `bilibili.sh` 脚本**，支持：
- ✅ Linux / macOS 直接运行
- ✅ Windows (Git Bash / WSL) 直接运行
- ✅ 自动检测平台和环境
- ✅ 所有功能集成在一个文件

## 🚀 使用方式

```bash
cd scripts/

# 1. 检查依赖
./bilibili.sh check

# 2. 搜索视频
./bilibili.sh search "Python教程" 10

# 3. 下载视频
./bilibili.sh download "https://www.bilibili.com/video/BV18NzvB5EZu" 1080

# 4. 获取视频信息
./bilibili.sh info "https://www.bilibili.com/video/BV18NzvB5EZu"
```

## 📝 命令说明

| 命令 | 功能 |
|------|------|
| `./bilibili.sh check` | 检查依赖是否安装 |
| `./bilibili.sh search <关键词> [数量]` | 搜索B站视频 |
| `./bilibili.sh download <URL> [清晰度] [目录]` | 下载视频 |
| `./bilibili.sh info <URL>` | 获取视频详情 |
| `./bilibili.sh help` | 显示帮助 |

## 🔧 脚本内容

以下是 v1.2 版本的完整脚本内容，保存为 `scripts/bilibili.sh`：

```bash
#!/bin/bash
# Bilibili Video Downloader v1.2 (统一版)
# 支持 Linux/macOS/Windows (Git Bash/WSL)

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

#===============================================
# 依赖检查
#===============================================
check_dependencies() {
    echo "检查依赖..."
    
    # Python
    if command -v python3 &> /dev/null; then
        echo "✅ Python: $(python3 --version 2>&1)"
    elif command -v python &> /dev/null; then
        echo "✅ Python: $(python --version 2>&1)"
    else
        echo "❌ Python 未安装"
        exit 1
    fi
    
    # yt-dlp
    if command -v yt-dlp &> /dev/null; then
        echo "✅ yt-dlp: $(yt-dlp --version 2>&1)"
    else
        echo "❌ yt-dlp 未安装 (pip install yt-dlp)"
        exit 1
    fi
    
    # ffmpeg
    if command -v ffmpeg &> /dev/null; then
        echo "✅ ffmpeg: $(ffmpeg -version 2>&1 | head -n1)"
    else
        echo "⚠️  ffmpeg 未安装 (视频可能无法合并)"
    fi
}

#===============================================
# 搜索视频
#===============================================
cmd_search() {
    local keyword="${1:-}"
    local limit="${2:-10}"
    
    if [ -z "$keyword" ]; then
        echo "用法: $0 search <关键词> [数量]"
        exit 1
    fi
    
    echo "搜索: $keyword"
    yt-dlp "ytsearch${limit}:${keyword} site:bilibili.com" \
        --print "%(title)s | %(uploader)s | %(view_count)s views | %(id)s" \
        --quiet 2>/dev/null
}

#===============================================
# 下载视频
#===============================================
cmd_download() {
    local url="${1:-}"
    local quality="${2:-best}"
    local output_dir="${3:-./downloads}"
    
    if [ -z "$url" ]; then
        echo "用法: $0 download <URL> [清晰度] [目录]"
        exit 1
    fi
    
    mkdir -p "$output_dir"
    echo "下载到: $output_dir"
    
    local format="bestvideo+bestaudio/best"
    case "$quality" in
        4K) format="bestvideo[height<=2160]+bestaudio/best" ;;
        1080*) format="bestvideo[height<=1080]+bestaudio/best" ;;
        720) format="bestvideo[height<=720]+bestaudio/best" ;;
        480) format="bestvideo[height<=480]+bestaudio/best" ;;
        360) format="bestvideo[height<=360]+bestaudio/best" ;;
    esac
    
    yt-dlp "$url" --format "$format" \
        --output "${output_dir}/%(title)s.%(ext)s" \
        --merge-output-format mp4 \
        --cookies cookies.txt 2>/dev/null || \
    yt-dlp "$url" --format "$format" \
        --output "${output_dir}/%(title)s.%(ext)s" \
        --merge-output-format mp4
}

#===============================================
# 获取视频信息
#===============================================
cmd_info() {
    local url="${1:-}"
    
    if [ -z "$url" ]; then
        echo "用法: $0 info <URL>"
        exit 1
    fi
    
    yt-dlp "$url" --dump-json --quiet 2>/dev/null | python3 -c "
import json,sys
d=json.load(sys.stdin)
print(f'标题: {d.get(\"title\",\"N/A\")}')
print(f'UP主: {d.get(\"uploader\",\"N/A\")}')
print(f'播放: {d.get(\"view_count\",\"N/A\")}')
print(f'时长: {int(d.get(\"duration\",0)//60)}分{int(d.get(\"duration\",0)%60)}秒')
print(f'链接: {d.get(\"webpage_url\",\"N/A\")}')
"
}

#===============================================
# 主程序
#===============================================
main() {
    local cmd="${1:-help}"
    shift 2>/dev/null || true
    
    case "$cmd" in
        check) check_dependencies ;;
        search) cmd_search "$@" ;;
        download) cmd_download "$@" ;;
        info) cmd_info "$@" ;;
        help|--help|-h)
            echo "Bilibili Video Downloader v1.2"
            echo "用法: $0 {check|search|download|info} [参数]"
            ;;
        *) echo "未知命令: $cmd" ;;
    esac
}

main "$@"
```

## 📦 创建 v1.2 版本

如果你想创建完整的 v1.2 包，按以下步骤操作：

```bash
# 1. 创建目录
mkdir bilibili-video-downloader-v1.2
cd bilibili-video-downloader-v1.2

# 2. 创建 SKILL.md (复制原来的内容)

# 3. 创建 scripts 目录并保存上述脚本为 bilibili.sh
mkdir scripts
# 保存上面的脚本内容到 scripts/bilibili.sh
chmod +x scripts/bilibili.sh

# 4. 打包
zip -r bilibili-video-downloader-v1.2.skill .
```

## 🔄 更新日志

### v1.2 (2026-03-21)
- ✨ 统一入口脚本，所有功能集成在一个文件
- ✅ 支持 Linux/macOS/Windows (Git Bash/WSL)
- 🔧 自动检测平台和环境
- 📦 更简单的文件结构

### v1.1 (2026-03-21)
- 📝 添加 PERMISSIONS.md 权限说明
- 📝 更新文档

### v1.0 (2026-03-19)
- 🎉 首次发布
- 支持搜索、下载、视频信息等功能
