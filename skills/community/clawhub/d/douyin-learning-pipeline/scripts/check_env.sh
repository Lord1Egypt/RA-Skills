#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCAL_CONFIG="$SKILL_DIR/local/config.json"
DOWNLOADER_DIR="$SKILL_DIR/assets/douyin-downloader"

echo "=== 抖音学习流水线环境自检 ==="
echo ""

echo "[1/5] 检查 Python 3..."
if command -v python3 &>/dev/null; then
    python3 --version
else
    echo "✗ Python 3 未安装" >&2
    exit 1
fi

echo ""
echo "[2/5] 检查 ffmpeg..."
if command -v ffmpeg &>/dev/null; then
    echo "✓ ffmpeg 已安装"
else
    echo "✗ ffmpeg 未安装"
    echo "  该依赖需要用户确认后安装。可选命令："
    echo "  Ubuntu/Debian: sudo apt update && sudo apt install -y ffmpeg"
    echo "  macOS: brew install ffmpeg"
fi

echo ""
echo "[3/5] 检查 yt-dlp..."
if command -v yt-dlp &>/dev/null; then
    echo "✓ yt-dlp 已安装"
else
    echo "✗ yt-dlp 未安装，尝试用户级安装..."
    python3 -m pip install yt-dlp --user || echo "  用户级安装失败，请手动安装 yt-dlp"
fi

echo ""
echo "[4/5] 检查 douyin-downloader..."
if [[ -d "$DOWNLOADER_DIR/.git" || -f "$DOWNLOADER_DIR/run.py" ]]; then
    echo "✓ douyin-downloader 已部署"
else
    echo "✗ douyin-downloader 未部署，尝试自动克隆..."
    git clone https://github.com/jiji262/douyin-downloader.git "$DOWNLOADER_DIR"
    echo "  已克隆到 $DOWNLOADER_DIR"
    echo "  请配置 Cookie: $DOWNLOADER_DIR/config.yml"
fi

echo ""
echo "[5/5] 检查 SiliconFlow API Key..."
if [[ -n "${SILICONFLOW_API_KEY:-}" ]]; then
    echo "✓ SILICONFLOW_API_KEY 环境变量已设置"
elif [[ -f "$LOCAL_CONFIG" ]] && python3 -c "import json; c=json.load(open('$LOCAL_CONFIG')); exit(0 if c.get('siliconflow_api_key') else 1)" 2>/dev/null; then
    echo "✓ local/config.json 中已配置 siliconflow_api_key"
else
    echo "✗ SiliconFlow API Key 未配置"
    echo "  请设置环境变量: export SILICONFLOW_API_KEY='your-key'"
    echo "  或运行配置脚本: python3 scripts/setup_config.py"
fi

echo ""
echo "=== 环境自检完成 ==="
echo "下一步:"
echo "1. 配置 SiliconFlow API Key: export SILICONFLOW_API_KEY='your-key'"
echo "2. 配置本地模板: python3 scripts/setup_config.py"
echo "3. 配置抖音 Cookie: 编辑 $DOWNLOADER_DIR/config.yml"
