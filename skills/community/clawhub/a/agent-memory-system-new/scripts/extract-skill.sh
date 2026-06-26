#!/bin/bash

# extract-skill.sh - 从经验教训中提取可复用技能
# 
# 用法：./extract-skill.sh <lesson-name> [skill-name]
#   lesson-name: lessons 目录中的文件名（不含.md）
#   skill-name:  可选，技能包名称（默认与 lesson 同名）
#
# 示例：
#   ./extract-skill.sh deploy-without-test
#   ./extract-skill.sh deploy-without-test safe-deploy

set -e

LESSON_NAME="$1"
SKILL_NAME="${2:-$LESSON_NAME}"
WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
LESSONS_DIR="$WORKSPACE/memory/lessons"
SKILLS_DIR="$WORKSPACE/skills"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_section() {
    echo ""
    echo -e "${BLUE}=== $1 ===${NC}"
}

# 参数检查
if [ -z "$LESSON_NAME" ]; then
    echo "用法：$0 <lesson-name> [skill-name]"
    echo ""
    echo "参数说明："
    echo "  lesson-name: lessons 目录中的文件名（不含.md）"
    echo "  skill-name:  可选，技能包名称（默认与 lesson 同名）"
    echo ""
    echo "示例："
    echo "  $0 deploy-without-test"
    echo "  $0 deploy-without-test safe-deploy"
    echo ""
    echo "可用的 lessons："
    if [ -d "$LESSONS_DIR" ]; then
        for f in "$LESSONS_DIR"/*.md; do
            if [ -f "$f" ]; then
                name=$(basename "$f" .md)
                if [ "$name" != "README" ] && [ "$name" != "TEMPLATE" ]; then
                    echo "  - $name"
                fi
            fi
        done
    else
        echo "  (lessons 目录不存在)"
    fi
    exit 1
fi

LESSON_FILE="$LESSONS_DIR/${LESSON_NAME}.md"
SKILL_DIR="$SKILLS_DIR/$SKILL_NAME"

# 检查 lesson 文件
if [ ! -f "$LESSON_FILE" ]; then
    log_error "找不到课程文件：$LESSON_FILE"
    echo ""
    echo "可用的 lessons："
    for f in "$LESSONS_DIR"/*.md; do
        if [ -f "$f" ]; then
            name=$(basename "$f" .md)
            if [ "$name" != "README" ] && [ "$name" != "TEMPLATE" ]; then
                echo "  - $name"
            fi
        fi
    done
    exit 1
fi

log_section "从课程提取技能"
echo "  Lesson: $LESSON_NAME"
echo "  Skill:  $SKILL_NAME"

# 检查技能目录是否已存在
if [ -d "$SKILL_DIR" ]; then
    log_warn "技能目录已存在：$SKILL_DIR"
    read -p "是否覆盖？(y/N): " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        log_info "已取消"
        exit 0
    fi
    rm -rf "$SKILL_DIR"
fi

# 创建技能目录结构
mkdir -p "$SKILL_DIR"
mkdir -p "$SKILL_DIR/.clawhub"
mkdir -p "$SKILL_DIR/scripts"

log_info "创建技能包结构..."

# 创建 SKILL.md
cat > "$SKILL_DIR/SKILL.md" << EOF
---
name: $SKILL_NAME
version: 1.0.0
description: "从经验教训提炼的技能 - 详见 memory/lessons/${LESSON_NAME}.md"
author: Agent
keywords: [skill, extracted, lesson]
metadata:
  openclaw:
    emoji: "🛠️"
    source:
      lesson: "memory/lessons/${LESSON_NAME}.md"
      extracted_at: "$(date -Iseconds)"
---

# $SKILL_NAME 技能

> 从经验教训中提炼的可复用能力

**来源课程**: [[${LESSON_NAME}]]  
**提炼时间**: $(date +%Y-%m-%d)

---

## 核心能力

<!-- 从课程中提炼的核心能力描述 -->

待补充...

---

## 使用方式

\`\`\`bash
# 示例用法
# TODO: 补充具体使用方式
\`\`\`

---

## 检查清单

- [ ] 核心能力已完善
- [ ] 使用示例已补充
- [ ] 脚本已测试

---

## 相关经验教训

- [[${LESSON_NAME}]] - 原始经验记录

---

*此技能由 extract-skill.sh 自动创建，请手动完善内容*
EOF

log_info "创建 SKILL.md"

# 创建 README.md
cat > "$SKILL_DIR/README.md" << EOF
# $SKILL_NAME

自动生成的技能包。

## 状态

- [ ] 核心能力待完善
- [ ] 使用示例待补充
- [ ] 测试用例待添加

## 下一步

1. 阅读源课程 \`memory/lessons/${LESSON_NAME}.md\`
2. 提炼核心能力到 SKILL.md
3. 添加使用示例和脚本
4. 测试技能是否正常工作

## 来源

- Lesson: \`memory/lessons/${LESSON_NAME}.md\`
- 提取时间: $(date '+%Y-%m-%d %H:%M:%S')
EOF

log_info "创建 README.md"

# 创建 .clawhub/origin.json
cat > "$SKILL_DIR/.clawhub/origin.json" << EOF
{
  "version": 1,
  "registry": "https://clawhub.ai",
  "slug": "$SKILL_NAME",
  "installedVersion": "1.0.0",
  "installedAt": $(date +%s)000
}
EOF

log_info "创建 .clawhub/origin.json"

# 创建 _meta.json
cat > "$SKILL_DIR/_meta.json" << EOF
{
  "ownerId": "local",
  "slug": "$SKILL_NAME",
  "version": "1.0.0",
  "publishedAt": $(date +%s)000
}
EOF

log_info "创建 _meta.json"

log_section "完成"
echo ""
log_info "✅ 技能包已创建：$SKILL_DIR"
echo ""
echo "📝 下一步："
echo "   1. 编辑 $SKILL_DIR/SKILL.md 完善核心能力"
echo "   2. 添加必要的脚本到 $SKILL_DIR/scripts/"
echo "   3. 更新源课程的 status 为 'promoted_to_skill'"
echo "   4. 在源课程中添加 Skill-Path: $SKILL_DIR"
echo ""

# 更新源课程状态
if [ -f "$LESSON_FILE" ]; then
    # 检查是否有 frontmatter
    if head -1 "$LESSON_FILE" | grep -q "^---"; then
        # 有 frontmatter，添加 status 和 skill-path
        if grep -q "^status:" "$LESSON_FILE"; then
            sed -i "s/^status:.*/status: promoted_to_skill/" "$LESSON_FILE"
        else
            sed -i "/^---$/a status: promoted_to_skill" "$LESSON_FILE"
        fi
        if ! grep -q "^skill-path:" "$LESSON_FILE"; then
            sed -i "/^status: promoted_to_skill/a skill-path: $SKILL_DIR" "$LESSON_FILE"
        fi
    fi
    log_info "已更新源课程状态"
fi