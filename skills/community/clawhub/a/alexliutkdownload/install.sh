#!/bin/bash
echo "🎵 正在安装抖音下载 Skill..."
mkdir -p "$HOME/.qclaw/workspace/skills/douyin-download"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cp "$SCRIPT_DIR/"*.py "$HOME/.qclaw/workspace/skills/douyin-download/" 2>/dev/null
cp "$SCRIPT_DIR/"*.md "$HOME/.qclaw/workspace/skills/douyin-download/" 2>/dev/null
echo "✅ 安装完成！发送抖音链接即可下载"
