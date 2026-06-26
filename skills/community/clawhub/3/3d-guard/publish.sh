#!/bin/bash
# 简化的Skill发布脚本
# 使用说明：./publish.sh

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SKILL_DIR="${SCRIPT_DIR}"

cd "$SKILL_DIR" || exit 1

# 尝试从package.json读取
if [ -f "package.json" ]; then
    SLUG=$(cat package.json | grep -o '"slug":[[:space:]]*"[^"]*"' | sed 's/.*"\([^"]*\)".*/\1/')
    NAME=$(cat package.json | grep -o '"displayName":[[:space:]]*"[^"]*"' | sed 's/.*"\([^"]*\)".*/\1/')
    VERSION=$(cat package.json | grep -o '"version":[[:space:]]*"[^"]*"' | sed 's/.*"\([^"]*\)".*/\1/')
    CHANGELOG=$(cat package.json | grep -o '"changelog":[[:space:]]*"[^"]*"' | sed 's/.*"\([^"]*\)".*/\1/')
fi

# 如果没有package.json，从SKILL.md读取（仅name）
if [ -z "$SLUG" ] && [ -f "SKILL.md" ]; then
    SLUG=$(grep "^name:" SKILL.md | cut -d':' -f2 | xargs)
    NAME=$(grep "^description:" SKILL.md | head -1 | sed 's/description: //' | head -c 100)
fi

# 设置默认值
SLUG=${SLUG:-"my-skill"}
NAME=${NAME:-"My Skill"}
VERSION=${VERSION:-"1.0.0"}
CHANGELOG=${CHANGELOG:-"Update"}

# 显示将要发布的信息
echo "========================================="
echo "准备发布Skill："
echo "========================================="
echo "Slug:      $SLUG"
echo "Name:       $NAME"
echo "Version:    $VERSION"
echo "Changelog:   $CHANGELOG"
echo "========================================="
echo ""

# 执行发布命令
echo "正在发布..."
clawhub publish . \
    --slug "$SLUG" \
    --name "$NAME" \
    --version "$VERSION" \
    --changelog "$CHANGELOG"
