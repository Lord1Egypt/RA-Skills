#!/bin/bash
# 竞品数据定时监控 Skill 安装脚本

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SKILL_NAME="competitor-monitor"
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "========================================"
echo "  📊 竞品数据监控 Skill 安装器"
echo "========================================"
echo ""

# 检测Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ 未检测到 Python3${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python3: $(python3 --version)"
echo ""

# 安装Python依赖
echo "📦 安装Python依赖..."
pip3 install playwright schedule requests pandas 2>/dev/null || pip install playwright schedule requests pandas

# 安装浏览器
echo "🌐 安装Chromium浏览器..."
python3 -m playwright install chromium

# 查找Skills目录
detect_skills_dir() {
    local possible_dirs=(
        "$HOME/.claude/skills"
        "$HOME/.config/claude/skills"
    )
    
    for dir in "${possible_dirs[@]}"; do
        if [ -d "$dir" ]; then
            echo "$dir"
            return 0
        fi
    done
    
    echo "$HOME/.claude/skills"
}

TARGET_DIR=${1:-$(detect_skills_dir)}
echo -e "${BLUE}ℹ${NC} 安装目录: $TARGET_DIR"
echo ""

# 确认安装
if [ -d "$TARGET_DIR/$SKILL_NAME" ]; then
    echo -e "${YELLOW}!${NC} Skill 已存在"
    read -p "是否覆盖安装? (y/N): " confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
    rm -rf "$TARGET_DIR/$SKILL_NAME"
fi

# 创建目录并复制
echo "📁 创建目录..."
mkdir -p "$TARGET_DIR"

echo "📦 复制 Skill 文件..."
cp -r "$SKILL_DIR" "$TARGET_DIR/"

# 创建数据目录
mkdir -p "$TARGET_DIR/$SKILL_NAME/assets/data"
mkdir -p "$TARGET_DIR/$SKILL_NAME/assets/screenshots"

# 设置权限
echo "🔧 设置权限..."
chmod 755 "$TARGET_DIR/$SKILL_NAME"
chmod -R 755 "$TARGET_DIR/$SKILL_NAME/scripts"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  ✅ 安装成功!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "📍 安装位置: $TARGET_DIR/$SKILL_NAME"
echo ""
echo "🚀 快速开始:"
echo ""
echo "  1. 复制配置文件:"
echo "     cp $TARGET_DIR/$SKILL_NAME/assets/config/monitor_tasks.example.json \\"
echo "        $TARGET_DIR/$SKILL_NAME/assets/config/monitor_tasks.json"
echo ""
echo "  2. 编辑配置:"
echo "     vim $TARGET_DIR/$SKILL_NAME/assets/config/monitor_tasks.json"
echo ""
echo "  3. 启动监控:"
echo "     python3 $TARGET_DIR/$SKILL_NAME/scripts/monitor_service.py start"
echo ""
echo "📖 更多信息请查看 README.md"
echo ""
