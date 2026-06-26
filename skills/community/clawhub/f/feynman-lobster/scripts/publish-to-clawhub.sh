#!/bin/bash
# 费曼虾 — 发布到 ClawHub
# ClawHub 只接受文本文件，需排除 .git 及可能的 .gitignore
# 用法：bash scripts/publish-to-clawhub.sh [版本号] [changelog]
# 示例：bash scripts/publish-to-clawhub.sh 1.0.1 "修复面板 API"

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMP_DIR="${TMPDIR:-/tmp}/feynman-lobster-publish"
VERSION="${1:-1.0.0}"
CHANGELOG="${2:-}"

echo "🦞 准备发布到 ClawHub..."
echo "   版本: $VERSION"
echo ""

# 用 git archive 导出干净副本（不含 .git）
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"
cd "$ROOT_DIR"

if git rev-parse --git-dir > /dev/null 2>&1; then
  git archive HEAD | tar -x -C "$TEMP_DIR"
else
  # 非 git 仓库则用 rsync 排除 .git
  rsync -a --exclude='.git' --exclude='.gitignore' "$ROOT_DIR/" "$TEMP_DIR/"
fi

# ClawHub 只接受文本文件，移除 .gitignore（避免被误判为非文本）
rm -f "$TEMP_DIR/.gitignore"

echo "✓ 已导出到 $TEMP_DIR"
echo ""
echo "执行发布命令："
echo "  clawhub publish $TEMP_DIR --slug feynman-lobster --name \"费曼虾\" --version $VERSION --changelog \"$CHANGELOG\" --tags latest"
echo ""

clawhub publish "$TEMP_DIR" \
  --slug feynman-lobster \
  --name "费曼虾" \
  --version "$VERSION" \
  --changelog "$CHANGELOG" \
  --tags latest

echo ""
echo "🦞 发布完成！"
rm -rf "$TEMP_DIR"
