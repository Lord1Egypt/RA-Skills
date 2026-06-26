#!/bin/bash
# 打包 Agent P2P Skill

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="agent-p2p"
VERSION="0.1.0"
OUTPUT_DIR="$SCRIPT_DIR/dist"

echo "=== 打包 Agent P2P Skill v$VERSION ==="

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 创建临时目录
TMP_DIR=$(mktemp -d)
trap "rm -rf $TMP_DIR" EXIT

# 复制必要文件
echo "复制文件..."
mkdir -p "$TMP_DIR/$SKILL_NAME"
cp -r "$SCRIPT_DIR/src" "$TMP_DIR/$SKILL_NAME/"
cp -r "$SCRIPT_DIR/scripts" "$TMP_DIR/$SKILL_NAME/"
cp -r "$SCRIPT_DIR/config" "$TMP_DIR/$SKILL_NAME/"
cp "$SCRIPT_DIR/client.py" "$TMP_DIR/$SKILL_NAME/"
cp "$SCRIPT_DIR/send.py" "$TMP_DIR/$SKILL_NAME/"
cp "$SCRIPT_DIR/install.py" "$TMP_DIR/$SKILL_NAME/"
cp "$SCRIPT_DIR/setup.sh" "$TMP_DIR/$SKILL_NAME/"
cp "$SCRIPT_DIR/requirements.txt" "$TMP_DIR/$SKILL_NAME/"
cp "$SCRIPT_DIR/README.md" "$TMP_DIR/$SKILL_NAME/"
cp "$SCRIPT_DIR/SKILL.md" "$TMP_DIR/$SKILL_NAME/"

# 创建压缩包
echo "创建压缩包..."
cd "$TMP_DIR"
tar -czf "$OUTPUT_DIR/${SKILL_NAME}-v${VERSION}.tar.gz" "$SKILL_NAME"

echo "=== 打包完成 ==="
echo "输出文件: $OUTPUT_DIR/${SKILL_NAME}-v${VERSION}.tar.gz"
echo ""
echo "安装方法:"
echo "  1. 复制到 OpenClaw workspace:"
echo "     cp dist/${SKILL_NAME}-v${VERSION}.tar.gz ~/.openclaw/workspace/skills/"
echo "  2. 解压:"
echo "     cd ~/.openclaw/workspace/skills/ && tar -xzf ${SKILL_NAME}-v${VERSION}.tar.gz"
echo "  3. 运行安装向导:"
echo "     cd agent-p2p && python3 install.py"
