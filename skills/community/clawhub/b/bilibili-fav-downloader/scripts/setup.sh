#!/bin/bash
# Bilibili Favorite Downloader - 环境安装脚本
# 支持 Ubuntu/Debian，自动安装 yt-dlp 和 ffmpeg

set -e

echo "[*] 安装 Bilibili 下载器环境..."

# 检测系统
if command -v apt-get &>/dev/null; then
    PKG_MANAGER="apt-get"
elif command -v dnf &>/dev/null; then
    PKG_MANAGER="dnf"
elif command -v yum &>/dev/null; then
    PKG_MANAGER="yum"
else
    echo "[!] 不支持的包管理器"
    exit 1
fi

echo "[*] 使用: $PKG_MANAGER"

# 安装 ffmpeg
if ! command -v ffmpeg &>/dev/null; then
    echo "[*] 安装 ffmpeg..."
    if [ "$PKG_MANAGER" = "apt-get" ]; then
        sudo apt-get install -y ffmpeg
    else
        sudo $PKG_MANAGER install -y ffmpeg
    fi
else
    echo "[+] ffmpeg 已安装: $(ffmpeg -version | head -1)"
fi

# 安装 yt-dlp
if ! command -v yt-dlp &>/dev/null; then
    echo "[*] 安装 yt-dlp..."
    if command -v pip3 &>/dev/null; then
        pip3 install --break-system-packages yt-dlp
    elif command -v pip &>/dev/null; then
        pip install yt-dlp
    else
        # 下载二进制
        sudo curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
        sudo chmod a+rx /usr/local/bin/yt-dlp
    fi
else
    echo "[+] yt-dlp 已安装: $(yt-dlp --version)"
fi

echo ""
echo "[✅] 环境安装完成！"
echo ""
echo "下一步:"
echo "  1. 获取 Bilibili Cookie (见 references/cookie-guide.md)"
echo "  2. 获取收藏夹 ID (见 references/favorite-guide.md)"
echo "  3. 配置下载脚本"
