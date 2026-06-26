#!/bin/bash
# CryptoScope SkillPay 快速配置脚本
# 使用方法: ./setup_skillpay.sh YOUR_SKILL_ID

set -e

# 检查参数
if [ -z "$1" ]; then
    echo "❌ 错误: 请提供Skill ID"
    echo "使用方法: ./setup_skillpay.sh YOUR_SKILL_ID"
    echo ""
    echo "获取Skill ID:"
    echo "1. 访问 https://skillpay.me/dashboard/skills"
    echo "2. 点击'创建技能'"
    echo "3. 填写信息（见SETUP.md）"
    echo "4. 复制Skill ID"
    exit 1
fi

SKILL_ID="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAID_SCRIPT="$SCRIPT_DIR/crypto_analyzer_paid.py"

echo "🚀 CryptoScope SkillPay 配置"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Skill ID: $SKILL_ID"
echo ""

# 检查文件是否存在
if [ ! -f "$PAID_SCRIPT" ]; then
    echo "❌ 错误: 找不到付费脚本"
    echo "路径: $PAID_SCRIPT"
    exit 1
fi

# 备份原文件
echo "✅ 备份原文件..."
cp "$PAID_SCRIPT" "${PAID_SCRIPT}.backup"

# 更新Skill ID
echo "✅ 更新Skill ID..."
sed -i.tmp "s/crypto-scope-v1-placeholder/$SKILL_ID/g" "$PAID_SCRIPT"
rm -f "${PAID_SCRIPT}.tmp"

# 验证更新
if grep -q "$SKILL_ID" "$PAID_SCRIPT"; then
    echo "✅ Skill ID更新成功！"
else
    echo "❌ 更新失败，恢复备份..."
    mv "${PAID_SCRIPT}.backup" "$PAID_SCRIPT"
    exit 1
fi

# 重新发布到ClawHub
echo ""
echo "📦 重新发布到ClawHub..."
cd "$SCRIPT_DIR/.."
npx clawhub publish . --version "1.0.2" --changelog "配置SkillPay Skill ID，启用付费功能"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 配置完成！"
echo ""
echo "📝 Skill ID: $SKILL_ID"
echo "📦 版本: v1.0.2"
echo "💰 定价: $0.05 / 次"
echo ""
echo "🚀 立即测试："
echo "python3 scripts/crypto_analyzer_paid.py price bitcoin --user-id test_user"
echo ""
echo "📝 配置文档: cat SETUP.md"
echo ""
