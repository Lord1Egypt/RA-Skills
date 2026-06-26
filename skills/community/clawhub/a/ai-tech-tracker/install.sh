#!/bin/bash
# AI技术动向追踪 Skill 安装脚本
# 支持 macOS 和 Linux

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SKILL_NAME="ai-tech-tracker"
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "========================================"
echo "  🤖 AI技术动向追踪 Skill 安装器"
echo "========================================"
echo ""

# 检测操作系统
OS="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
fi

echo -e "${BLUE}ℹ${NC} 检测到操作系统: $OS"
echo ""

# 检测 Claude Code
CLAUDE_CMD=$(which claude 2>/dev/null || echo "")

if [ -n "$CLAUDE_CMD" ]; then
    echo -e "${GREEN}✓${NC} 检测到 Claude Code: $CLAUDE_CMD"
else
    echo -e "${YELLOW}!${NC} 未检测到 Claude Code 命令"
fi

echo ""

# 查找或创建 skills 目录
detect_skills_dir() {
    local possible_dirs=(
        "$HOME/.claude/skills"
        "$HOME/.config/claude/skills"
        "$HOME/Library/Application Support/Claude/skills"
        "$HOME/.local/share/claude/skills"
    )
    
    for dir in "${possible_dirs[@]}"; do
        if [ -d "$dir" ]; then
            echo "$dir"
            return 0
        fi
    done
    
    echo "$HOME/.claude/skills"
    return 0
}

# 如果提供了参数，使用参数作为目标目录
if [ -n "$1" ]; then
    TARGET_DIR="$1"
    echo -e "${BLUE}ℹ${NC} 使用指定的安装目录: $TARGET_DIR"
else
    TARGET_DIR=$(detect_skills_dir)
    echo -e "${BLUE}ℹ${NC} 检测到 Skills 目录: $TARGET_DIR"
fi

echo ""

# 确认安装
if [ -d "$TARGET_DIR/$SKILL_NAME" ]; then
    echo -e "${YELLOW}!${NC} Skill 已存在: $TARGET_DIR/$SKILL_NAME"
    read -p "是否覆盖安装? (y/N): " confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
    rm -rf "$TARGET_DIR/$SKILL_NAME"
fi

# 创建目录
echo "📁 创建目录: $TARGET_DIR"
mkdir -p "$TARGET_DIR"

# 复制 Skill
echo "📦 复制 Skill 文件..."
cp -r "$SKILL_DIR" "$TARGET_DIR/"

# 验证安装
echo "🔍 验证安装..."
if [ -f "$TARGET_DIR/$SKILL_NAME/SKILL.md" ]; then
    echo -e "${GREEN}✓${NC} SKILL.md 存在"
else
    echo -e "${RED}✗${NC} SKILL.md 不存在"
    exit 1
fi

# 设置权限
echo "🔧 设置文件权限..."
chmod 755 "$TARGET_DIR/$SKILL_NAME"
chmod 644 "$TARGET_DIR/$SKILL_NAME"/*.md
chmod 755 "$TARGET_DIR/$SKILL_NAME/scripts" 2>/dev/null || true
chmod 644 "$TARGET_DIR/$SKILL_NAME/scripts/"* 2>/dev/null || true
chmod 755 "$TARGET_DIR/$SKILL_NAME/scripts/"*.py 2>/dev/null || true
chmod 755 "$TARGET_DIR/$SKILL_NAME/references" 2>/dev/null || true
chmod 644 "$TARGET_DIR/$SKILL_NAME/references/"* 2>/dev/null || true
chmod 755 "$TARGET_DIR/$SKILL_NAME/assets" 2>/dev/null || true
chmod 644 "$TARGET_DIR/$SKILL_NAME/assets/"* 2>/dev/null || true

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  ✅ 安装成功!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "📍 安装位置: $TARGET_DIR/$SKILL_NAME"
echo ""
echo "🚀 使用方法:"
echo "  1. 重启 Claude Code"
echo "  2. 在对话中输入:"
echo ""
echo -e "     ${YELLOW}帮我整理一下本周AI领域的最新动态${NC}"
echo ""
echo "  或者:"
echo ""
echo -e "     ${YELLOW}最近OpenAI和Google有什么新发布？${NC}"
echo ""
echo "📖 查看详细文档:"
echo "  cat $TARGET_DIR/$SKILL_NAME/README.md"
echo ""

# 验证 Skill 格式
if command -v python3 &> /dev/null; then
    python3 -c "
import yaml
import sys

try:
    with open('$TARGET_DIR/$SKILL_NAME/SKILL.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    if content.startswith('---'):
        _, frontmatter, _ = content.split('---', 2)
        data = yaml.safe_load(frontmatter)
        
        print('📋 Skill 信息:')
        print(f'  名称: {data.get(\"name\", \"N/A\")}')
        print(f'  描述: {data.get(\"description\", \"N/A\")[:60]}...')
        print('')
        print('✅ Skill 格式验证通过')
    else
        print('⚠️  SKILL.md 格式可能不正确')
except Exception as e:
    print(f'⚠️  验证警告: {e}')
"
else
    echo "⚠️  未检测到 Python3，跳过格式验证"
fi

echo ""
echo "🗑️  如需卸载，请运行:"
echo "  rm -rf $TARGET_DIR/$SKILL_NAME"
echo ""
echo "========================================"
echo "  感谢使用 AI技术动向追踪 Skill! 🤖"
echo "========================================"
