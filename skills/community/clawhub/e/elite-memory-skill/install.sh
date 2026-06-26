#!/bin/bash
# Elite Memory Skill 安装脚本

set -e

SKILL_NAME="elite-memory"
TARGET_DIR="${1:-$HOME/.openclaw/workspace/skills/$SKILL_NAME}"
SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "🧠 正在安装 Elite Memory 技能..."
echo "源目录：$SOURCE_DIR"
echo "目标目录：$TARGET_DIR"

# 创建目标目录
mkdir -p "$TARGET_DIR"

# 复制文件
cp -r "$SOURCE_DIR"/* "$TARGET_DIR/"

# 设置权限
chmod +x "$TARGET_DIR/scripts"/*.sh 2>/dev/null || true

echo ""
echo "✅ 安装完成！"
echo ""
echo "下一步配置:"
echo "1. 配置飞书通知 (可选):"
echo "   export FEISHU_USER_ID=\"ou_xxxxx\""
echo ""
echo "2. 配置 GitHub remote:"
echo "   cd ~/.openclaw/workspace"
echo "   gh repo create ai-memory --private"
echo "   git remote add memory git@github.com:username/ai-memory.git"
echo ""
echo "3. 添加定时任务:"
echo "   crontab -e"
echo "   55 23 * * * ~/.openclaw/workspace/scripts/sync-memory-to-github.sh"
echo "   0 8 * * * ~/.openclaw/workspace/scripts/morning-memory-read.sh"
echo ""
