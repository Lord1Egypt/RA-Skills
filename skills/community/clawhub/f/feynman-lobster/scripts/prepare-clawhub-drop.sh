#!/bin/bash
# 费曼虾 — 生成可直接拖拽到 ClawHub 网页的文件夹
# 用法：bash scripts/prepare-clawhub-drop.sh
# 输出：项目根目录下的 feynman-lobster-drop/（无 .git、无 .gitignore）

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
DROP_DIR="$ROOT_DIR/feynman-lobster-drop"

echo "🦞 生成 ClawHub 拖拽用文件夹..."
rm -rf "$DROP_DIR"
mkdir -p "$DROP_DIR"

rsync -a \
  --exclude='.git' \
  --exclude='.gitignore' \
  --exclude='feynman-lobster-drop' \
  --exclude='feynman-lobster-drop.zip' \
  --exclude='dist-clawhub' \
  --exclude='.DS_Store' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='node_modules' \
  "$ROOT_DIR/" "$DROP_DIR/"

# 自动生成 zip
ZIP_PATH="$ROOT_DIR/feynman-lobster-drop.zip"
rm -f "$ZIP_PATH"
(cd "$ROOT_DIR" && zip -r feynman-lobster-drop.zip feynman-lobster-drop -x "*.DS_Store")

echo ""
echo "✓ 已生成："
echo "  文件夹：$DROP_DIR"
echo "  Zip：  $ZIP_PATH"
echo ""
echo "→ 直接拖拽 feynman-lobster-drop.zip 到 ClawHub 网页即可"
echo ""
