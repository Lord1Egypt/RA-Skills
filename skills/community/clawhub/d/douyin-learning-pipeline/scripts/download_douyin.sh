#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <douyin_url> [output_dir]" >&2
    exit 1
fi

DOUYIN_URL="$1"
OUTPUT_DIR="${2:-/tmp/douyin_output_$(date +%s)}"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOWNLOADER_DIR="$SKILL_DIR/assets/douyin-downloader"
CONFIG_FILE="$DOWNLOADER_DIR/config.yml"

# 检查 douyin-downloader
if [[ -d "$DOWNLOADER_DIR/.git" || -f "$DOWNLOADER_DIR/run.py" ]]; then
    echo "检测到已存在 douyin-downloader：$DOWNLOADER_DIR"
elif [[ -d "$DOWNLOADER_DIR" ]]; then
    echo "错误: $DOWNLOADER_DIR 已存在，但不是有效的 douyin-downloader 目录。" >&2
    echo "请手动清理后重试。" >&2
    exit 2
else
    echo "douyin-downloader 未部署，正在克隆..."
    git clone https://github.com/jiji262/douyin-downloader.git "$DOWNLOADER_DIR"
fi

# 检查配置
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "错误: 未找到 config.yml，请先配置抖音 Cookie" >&2
    echo "参考: $DOWNLOADER_DIR/config.example.yml" >&2
    exit 1
fi

# 激活虚拟环境（如果存在）
if [[ -f "$DOWNLOADER_DIR/.venv/bin/activate" ]]; then
    # shellcheck disable=SC1091
    source "$DOWNLOADER_DIR/.venv/bin/activate"
fi

cd "$DOWNLOADER_DIR"
python run.py -c config.yml -u "$DOUYIN_URL" -p "$OUTPUT_DIR"

echo ""
echo "下载完成: $OUTPUT_DIR"
echo ""
echo "文件列表:"
find "$OUTPUT_DIR" -type f | head -20

echo "OUTPUT_DIR=$OUTPUT_DIR"
