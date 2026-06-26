#!/bin/bash
# bw-openclaw-boost 安装脚本

SKILL_DIR="$HOME/.openclaw/bw-openclaw-boost"

echo "安装 bw-openclaw-boost 到 $SKILL_DIR"

mkdir -p "$SKILL_DIR"
mkdir -p "$SKILL_DIR/config"
mkdir -p "$SKILL_DIR/memory"

# 复制所有文件
cp -r tools "$SKILL_DIR/"
cp SKILL.md "$SKILL_DIR/"
cp version.json "$SKILL_DIR/"
cp launch.sh "$SKILL_DIR/"

# 设置执行权限
chmod +x "$SKILL_DIR/tools/"*.sh "$SKILL_DIR/tools/"*.py
chmod +x "$SKILL_DIR/launch.sh"

echo "安装完成！"
echo ""
echo "使用方式："
echo "  bash $SKILL_DIR/launch.sh cost      # 成本追踪"
echo "  bash $SKILL_DIR/launch.sh memory    # 记忆检索"
echo "  bash $SKILL_DIR/launch.sh budget    # Token 预算"
echo "  bash $SKILL_DIR/launch.sh all-status  # 所有状态"
