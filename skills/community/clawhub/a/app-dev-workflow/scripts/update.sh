#!/bin/bash
# 版本更新脚本
# 用法: ./update.sh [patch|minor|major] "更新说明"

set -e

VERSION_TYPE="$1"
MESSAGE="$2"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

usage() {
    echo "用法: ./update.sh [patch|minor|major] \"更新说明\""
    echo ""
    echo "版本号规则 (Semantic Versioning):"
    echo "  patch - 修复bug (1.0.0 -> 1.0.1)"
    echo "  minor - 新增功能 (1.0.0 -> 1.1.0)"
    echo "  major - 重大变更 (1.0.0 -> 2.0.0)"
    echo ""
    echo "示例:"
    echo "  ./update.sh patch \"修复DIYCoffeeService空指针问题\""
    echo "  ./update.sh minor \"新增风味分析算法\""
    exit 1
}

if [ -z "$VERSION_TYPE" ] || [ -z "$MESSAGE" ]; then
    usage
fi

if [ ! -f "version.json" ]; then
    echo -e "${RED}❌ 错误: 当前目录不是有效的豆因项目${NC}"
    exit 1
fi

# 读取当前版本
CURRENT_VERSION=$(cat version.json | grep -o '"version": "[^"]*"' | cut -d'"' -f4)
BUILD_NUMBER=$(cat version.json | grep -o '"build": [0-9]*' | grep -o '[0-9]*')
COMPONENT_NAME=$(cat version.json | grep -o '"target": "[^"]*"' | cut -d'"' -f4)

echo -e "${BLUE}📦 组件: $COMPONENT_NAME${NC}"
echo -e "${BLUE}🔖 当前版本: $CURRENT_VERSION (build $BUILD_NUMBER)${NC}"

# 计算新版本
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT_VERSION"

case "$VERSION_TYPE" in
    patch)
        PATCH=$((PATCH + 1))
        ;;
    minor)
        MINOR=$((MINOR + 1))
        PATCH=0
        ;;
    major)
        MAJOR=$((MAJOR + 1))
        MINOR=0
        PATCH=0
        ;;
    *)
        echo -e "${RED}❌ 错误的版本类型: $VERSION_TYPE${NC}"
        usage
        ;;
esac

NEW_VERSION="$MAJOR.$MINOR.$PATCH"
NEW_BUILD=$((BUILD_NUMBER + 1))
TODAY=$(date +"%Y-%m-%d")

echo -e "${GREEN}🆕 新版本: $NEW_VERSION (build $NEW_BUILD)${NC}"

# 1. 更新 version.json
echo -e "${YELLOW}📝 更新 version.json...${NC}"
cat > version.json <<EOF
{
  "version": "$NEW_VERSION",
  "build": $NEW_BUILD,
  "lastUpdate": "$TODAY",
  "target": "$COMPONENT_NAME",
  "type": "service"
}
EOF

# 2. 更新 CHANGELOG.md
echo -e "${YELLOW}📝 更新 CHANGELOG.md...${NC}"

# 读取现有的CHANGELOG内容
if [ -f "CHANGELOG.md" ]; then
    CHANGELOG_CONTENT=$(cat CHANGELOG.md)
else
    CHANGELOG_CONTENT="# $COMPONENT_NAME 更新日志"
fi

# 创建新的变更日志条目
NEW_ENTRY="## [$NEW_VERSION] - $TODAY
### $([ "$VERSION_TYPE" = "patch" ] && echo "Fixed" || [ "$VERSION_TYPE" = "minor" ] && echo "Added" || echo "Changed")
- $MESSAGE
- Build $NEW_BUILD
"

# 在Unreleased和第一个版本之间插入新条目
if echo "$CHANGELOG_CONTENT" | grep -q "## \[Unreleased\]"; then
    UPDATED_CHANGELOG=$(echo "$CHANGELOG_CONTENT" | sed "s/## \[Unreleased\]/## [Unreleased]\n\n## [$NEW_VERSION] - $TODAY\n### $([ "$VERSION_TYPE" = "patch" ] && echo "Fixed" || [ "$VERSION_TYPE" = "minor" ] && echo "Added" || echo "Changed")\n- $MESSAGE\n- Build $NEW_BUILD/")
else
    UPDATED_CHANGELOG="$CHANGELOG_CONTENT

$NEW_ENTRY"
fi

echo "$UPDATED_CHANGELOG" > CHANGELOG.md

# 3. 统计代码
echo -e "${YELLOW}📊 统计代码...${NC}"

TOTAL_FILES=0
TOTAL_LINES=0

if [ -d "src" ]; then
    TOTAL_FILES=$(find src -name "*.ts" -o -name "*.ets" | wc -l)
    TOTAL_LINES=$(find src -name "*.ts" -o -name "*.ets" -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print $1}')
fi

echo "   文件数: $TOTAL_FILES"
echo "   代码行: $TOTAL_LINES"

# 4. 更新 PROJECT.md
echo -e "${YELLOW}📝 更新 PROJECT.md...${NC}"

if [ -f "PROJECT.md" ]; then
    # 更新版本号
    sed -i.bak "s/\*\*版本\*\*: .*/\*\*版本\*\*: $NEW_VERSION/" PROJECT.md 2>/dev/null || \
    sed -i "s/\*\*版本\*\*: .*/\*\*版本\*\*: $NEW_VERSION/" PROJECT.md

    # 更新代码统计
    sed -i.bak "s/\*\*总计\*\*: .*/\*\*总计\*\*: ${TOTAL_LINES}行/" PROJECT.md 2>/dev/null || \
    sed -i "s/\*\*总计\*\*: .*/\*\*总计\*\*: ${TOTAL_LINES}行/" PROJECT.md

    rm -f PROJECT.md.bak
fi

# 5. 运行规范检查
echo -e "${YELLOW}🔍 运行规范检查...${NC}"

if [ -f "scripts/lint.sh" ]; then
    # 检查所有src文件
    LINT_PASSED=true
    for file in $(find src -name "*.ts" -o -name "*.ets" 2>/dev/null); do
        echo "   检查: $file"
        if ! bash scripts/lint.sh "$file" 2>/dev/null; then
            LINT_PASSED=false
        fi
    done

    if [ "$LINT_PASSED" = true ]; then
        echo -e "${GREEN}✅ 所有规范检查通过${NC}"
    else
        echo -e "${YELLOW}⚠️ 部分检查未通过，请查看详情${NC}"
    fi
fi

# 6. 备份当前版本
echo -e "${YELLOW}💾 备份到 versions/...${NC}"

mkdir -p versions

# 复制当前代码到versions目录
BACKUP_DIR="versions/${COMPONENT_NAME}-v${NEW_VERSION}"
mkdir -p "$BACKUP_DIR"

cp -r src "$BACKUP_DIR/" 2>/dev/null || true
cp -r test "$BACKUP_DIR/" 2>/dev/null || true
cp PROJECT.md "$BACKUP_DIR/" 2>/dev/null || true
cp version.json "$BACKUP_DIR/" 2>/dev/null || true

echo "   备份: $BACKUP_DIR"

# 7. 完成
echo ""
echo -e "${GREEN}✅ 版本更新完成!${NC}"
echo ""
echo "📋 更新摘要:"
echo "   版本: $CURRENT_VERSION -> $NEW_VERSION"
echo "   Build: $BUILD_NUMBER -> $NEW_BUILD"
echo "   说明: $MESSAGE"
echo "   代码: $TOTAL_LINES 行"
echo ""
echo "📝 变更记录:"
echo "   - version.json"
echo "   - CHANGELOG.md"
echo "   - PROJECT.md"
echo "   - versions/$COMPONENT_NAME-v$NEW_VERSION/"
echo ""
