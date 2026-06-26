#!/bin/bash
# install.sh - 安装 api-rate-limiter 技能到其他OpenClaw系统

set -e

OPENCLAW_SKILLS_DIR="$HOME/.openclaw/workspace/skills"
SKILL_NAME="api-rate-limiter"
SKILL_DIR="$OPENCLAW_SKILLS_DIR/$SKILL_NAME"

echo "正在安装 $SKILL_NAME 技能..."

# 检查依赖
if ! command -v jq &> /dev/null; then
    echo "错误: 需要安装 jq，但未找到。请先安装 jq。"
    exit 1
fi

if ! command -v bc &> /dev/null; then
    echo "警告: 未找到 bc 计算器，延迟功能可能受限。"
fi

# 创建技能目录
mkdir -p "$SKILL_DIR"
mkdir -p "$SKILL_DIR/scripts"

# 复制文件
cp SKILL.md "$SKILL_DIR/"
cp README.md "$SKILL_DIR/"
cp skill-api-rate-limiter.sh "$SKILL_DIR/"
cp scripts/api-rate-limiter.sh "$SKILL_DIR/scripts/"
cp default_config.json "$SKILL_DIR/"

# 设置执行权限
chmod +x "$SKILL_DIR/skill-api-rate-limiter.sh"
chmod +x "$SKILL_DIR/scripts/api-rate-limiter.sh"

# 创建系统链接
if command -v sudo &> /dev/null; then
    sudo ln -sf "$SKILL_DIR/scripts/api-rate-limiter.sh" /usr/local/bin/api-rate-limiter
else
    ln -sf "$SKILL_DIR/scripts/api-rate-limiter.sh" /usr/local/bin/api-rate-limiter
fi

echo "技能 $SKILL_NAME 已成功安装！"
echo ""
echo "使用方法:"
echo "  api-rate-limiter apply-delay [light|medium|heavy|custom]  # 应用请求延迟"
echo "  api-rate-limiter check-status                            # 检查限流状态"
echo "  api-rate-limiter show-config                             # 查看当前配置"
echo "  api-rate-limiter update-config --key KEY --value VALUE   # 更新配置项"
echo "  api-rate-limiter reset-config                            # 重置为默认配置"
echo ""
echo "配置文件位置: ~/.openclaw/workspace/config/api_rate_limiter_config.json"
echo "更多信息请参阅技能文档。"