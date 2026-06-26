#!/usr/bin/env bash
set -e
echo "🚀 Super Agent — 环境部署脚本"
echo "============================="

# 1. 创建输出目录
OUTPUT_DIR="$HOME/Desktop/douyin-super-agent/"
if [ ! -d "$OUTPUT_DIR" ]; then
    mkdir -p "$OUTPUT_DIR"
    echo ""
    echo "✅ 输出目录已创建: $OUTPUT_DIR"
else
    echo ""
    echo "✅ 输出目录已存在: $OUTPUT_DIR"
fi

# 2. 检查 Python
if command -v python3 &>/dev/null; then
    PYTHON_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    echo "✅ Python $PYTHON_VER 已安装"
else
    echo "❌ 缺 Python，请先安装:"
    echo "   brew install python3"
    exit 1
fi

# 3. 安装 Python 依赖
echo ""
echo "⏳ 安装 Python 依赖..."
pip3 install -q -r "$(dirname "$0")/requirements.txt" 2>/dev/null || \
pip3 install -r "$(dirname "$0")/requirements.txt"
echo "✅ Python 依赖已安装"

# 4. 检查 ffmpeg
if command -v ffmpeg &>/dev/null; then
    echo "✅ ffmpeg 已安装"
else
    echo "⏳ 安装 ffmpeg..."
    if command -v brew &>/dev/null; then
        brew install ffmpeg
    else
        echo "❌ 缺 ffmpeg，请手动安装 (brew install ffmpeg)"
    fi
fi

# 5. 检查 mcporter（可选但推荐）
if command -v mcporter &>/dev/null; then
    echo "✅ mcporter 已安装"
else
    echo "⚠️  未安装 mcporter（推荐安装用于抖音解析）"
    echo "   npm install -g mcporter 或见 openclaw 文档"
fi

# 6. 验证脚本
echo ""
echo "⏳ 验证环境..."
python3 "$(dirname "$0")/scripts/douyin.py" stats
echo ""
echo "🎉 安装完成！"
echo ""
echo "第一个任务:"
echo "  python3 ~/.openclaw/skills/douyin/scripts/douyin.py video \"https://v.douyin.com/xxx/\""
echo ""
echo "文件输出目录: $OUTPUT_DIR"
