#!/bin/bash
# 技能安装脚本
# 用法：./install.sh <技能名> <目标目录> [--force]

set -e

SLUG="$1"
TARGET="$2"
FORCE="$3"

if [ -z "$SLUG" ] || [ -z "$TARGET" ]; then
  echo "❌ 用法：$0 <技能名> <目标目录> [--force]"
  echo "示例：$0 weather /Users/xubangbang/.openclaw/workspace/agents/MAIN/skills"
  exit 1
fi

# 清理目标路径（移除末尾斜杠）
TARGET=$(echo "$TARGET" | sed 's/\/$//')

ZIP_FILE="/tmp/${SLUG}.zip"
TEMP_DIR="/tmp/${SLUG}_install_$$"

echo "📦 正在安装：${SLUG}"
echo "  目标：${TARGET}/${SLUG}"

# 检查 ZIP 文件
if [ ! -f "$ZIP_FILE" ]; then
  echo "❌ ZIP 文件不存在：$ZIP_FILE"
  echo "  提示：先运行 ./download.sh ${SLUG}"
  exit 1
fi

# 检查目标目录
if [ -d "${TARGET}/${SLUG}" ]; then
  if [ "$FORCE" != "--force" ] && [ "$FORCE" != "-f" ]; then
    echo "⚠️ 技能已存在：${TARGET}/${SLUG}"
    echo "  使用 --force 覆盖安装"
    exit 1
  fi
  echo "  → 覆盖已存在的版本..."
  rm -rf "${TARGET}/${SLUG}"
fi

# 创建目标目录
mkdir -p "$TARGET"

# 创建临时目录
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

# 解压
echo "  → 解压中..."
unzip -q -o "$ZIP_FILE" -d "$TEMP_DIR"

# 检查解压结果
EXTRACTED_DIR=$(ls -d ${TEMP_DIR}/*/ 2>/dev/null | head -1)
if [ -z "$EXTRACTED_DIR" ]; then
  EXTRACTED_DIR="$TEMP_DIR"
fi

# 验证技能文件
if [ ! -f "${EXTRACTED_DIR}SKILL.md" ]; then
  echo "⚠️ 警告：未找到 SKILL.md，可能不是标准技能包"
fi

# 复制到目标目录
echo "  → 安装中..."
mkdir -p "${TARGET}/${SLUG}"
cp -r "${EXTRACTED_DIR}"* "${TARGET}/${SLUG}/"

# 清理临时文件
rm -rf "$TEMP_DIR"

# 验证安装
if [ -d "${TARGET}/${SLUG}" ]; then
  echo ""
  echo "✅ 安装成功！"
  echo "  位置：${TARGET}/${SLUG}"
  echo ""
  echo "📁 技能内容："
  ls -la "${TARGET}/${SLUG}/"
  
  # 显示版本信息
  if [ -f "${TARGET}/${SLUG}/_meta.json" ]; then
    echo ""
    echo "📋 版本信息："
    cat "${TARGET}/${SLUG}/_meta.json" | grep -E '"version"|"name"|"slug"' | sed 's/^/  /'
  fi
else
  echo "❌ 安装失败"
  exit 1
fi
