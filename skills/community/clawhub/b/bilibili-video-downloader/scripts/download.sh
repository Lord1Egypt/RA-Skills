#!/bin/bash
#===============================================
# Bilibili Video Downloader - 下载脚本
#===============================================

# 引用主脚本
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec "$SCRIPT_DIR/bilibili.sh" download "$@"
