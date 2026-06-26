#!/bin/bash

# Agent Memory System 一键安装脚本
# 用法：./install.sh

set -e

echo "🧠 Agent Memory System 安装程序"
echo "================================"
echo ""

# 1. 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# 2. 询问用户工作区路径
DEFAULT_WORKSPACE="$HOME/.openclaw/workspace"
read -p "请输入 OpenClaw 工作区路径 (默认: $DEFAULT_WORKSPACE): " WORKSPACE
WORKSPACE="${WORKSPACE:-$DEFAULT_WORKSPACE}"

echo ""
echo "📁 工作区：$WORKSPACE"
echo ""

# 3. 创建记忆目录结构
echo "📂 创建记忆目录..."
mkdir -p "$WORKSPACE/memory/lessons"
mkdir -p "$WORKSPACE/memory/decisions"
mkdir -p "$WORKSPACE/memory/people"
mkdir -p "$WORKSPACE/memory/reflections"
mkdir -p "$WORKSPACE/memory/.archive"
echo "✅ 目录创建完成"
echo ""

# 4. 复制模板文件
echo "📋 复制模板文件..."
cp "$SKILL_DIR/templates/MEMORY-template.md" "$WORKSPACE/MEMORY.md.example"
cp "$SKILL_DIR/templates/daily-log-template.md" "$WORKSPACE/memory/daily-log-template.md"
cp "$SKILL_DIR/templates/lesson-template.md" "$WORKSPACE/memory/lessons/lesson-template.md"
echo "✅ 模板复制完成"
echo ""

# 5. 配置 crontab（可选）
echo "⏰ 配置定时任务..."
read -p "是否配置自动 GC 和反思任务？(y/n, 默认:y): " CONFIG_CRON
CONFIG_CRON="${CONFIG_CRON:-y}"

if [[ "$CONFIG_CRON" == "y" || "$CONFIG_CRON" == "Y" ]]; then
    # 检查 crontab 是否已存在相关配置
    if crontab -l 2>/dev/null | grep -q "memory-gc.sh"; then
        echo "⚠️  检测到已有 memory-gc.sh 配置，跳过"
    else
        # 添加 GC 任务（每周日 00:00）
        (crontab -l 2>/dev/null | grep -v "memory-gc.sh" || true; echo "0 0 * * 0 $SCRIPT_DIR/memory-gc.sh") | crontab -
        echo "✅ 已添加每周 GC 任务"
    fi
    
    if crontab -l 2>/dev/null | grep -q "nightly-reflection.sh"; then
        echo "⚠️  检测到已有 nightly-reflection.sh 配置，跳过"
    else
        # 添加反思任务（每天 23:45）
        (crontab -l 2>/dev/null | grep -v "nightly-reflection.sh" || true; echo "45 23 * * * $SCRIPT_DIR/nightly-reflection.sh") | crontab -
        echo "✅ 已添加每日反思任务"
    fi
else
    echo "⏭️  跳过 crontab 配置，可以手动添加"
fi
echo ""

# 6. 显示使用说明
echo "================================"
echo "🎉 安装完成！"
echo ""
echo "📖 使用说明："
echo "1. 复制 MEMORY.md.example 为 MEMORY.md（如需要）"
echo "   cp $WORKSPACE/MEMORY.md.example $WORKSPACE/MEMORY.md"
echo ""
echo "2. 查看当前记忆状态："
echo "   $SCRIPT_DIR/memory-gc.sh --dry-run"
echo ""
echo "3. 手动执行夜间反思："
echo "   $SCRIPT_DIR/nightly-reflection.sh"
echo ""
echo "4. 从教训中提取技能："
echo "   $SCRIPT_DIR/extract-skill.sh <lesson-name>"
echo ""
echo "📚 详细文档：$SKILL_DIR/SKILL.md"
echo "================================"
