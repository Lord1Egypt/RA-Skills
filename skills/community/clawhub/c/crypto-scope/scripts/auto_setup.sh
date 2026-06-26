#!/bin/bash
# CryptoScope 一键配置脚本（自动化90%）
# 只需要提供Skill ID即可完成配置

set -e

echo "🚀 CryptoScope 自动配置"
echo "━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 检查Skill ID
if [ -z "$1" ]; then
    echo "⚠️  需要Skill ID才能完成配置"
    echo ""
    echo "📋 获取Skill ID（1分钟）："
    echo "1. 打开：https://skillpay.me/dashboard/skills"
    echo "2. 点击「创建技能」"
    echo "3. 填写："
    echo "   - 名称：CryptoScope - 加密货币分析助手"
    echo "   - 描述：实时价格查询、技术指标分析、交易信号生成"
    echo "   - 定价：0.05 USDT"
    echo "   - 标签：crypto, bitcoin, trading"
    echo "4. 点击「创建」"
    echo "5. 复制Skill ID"
    echo ""
    echo "💡 使用方法："
    echo "./scripts/auto_setup.sh YOUR_SKILL_ID"
    echo ""
    exit 1
fi

SKILL_ID="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ANALYZER="$SCRIPT_DIR/crypto_analyzer.py"

echo "✅ Skill ID: $SKILL_ID"
echo ""

# 1. 更新配置
echo "📝 更新配置..."
sed -i.bak "s/crypto-scope-v1/$SKILL_ID/g" "$ANALYZER"
echo "✅ 配置已更新"

# 2. 测试免费功能
echo ""
echo "🧪 测试免费功能..."
python3 "$ANALYZER" test
echo "✅ 测试通过"

# 3. 重新发布
echo ""
echo "📦 重新发布到ClawHub..."
cd "$SCRIPT_DIR/.."
npx clawhub publish . --version "1.0.4" --changelog "配置SkillPay Skill ID: $SKILL_ID"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 配置完成！"
echo ""
echo "📝 Skill ID: $SKILL_ID"
echo "📦 版本: v1.0.4"
echo "💰 定价: $0.05 / 次"
echo ""
echo "🚀 立即测试付费功能："
echo "python3 scripts/crypto_analyzer.py price bitcoin --user-id test_user --format text"
echo ""
echo "💳 充值地址："
echo "https://skillpay.me/dashboard/wallet"
echo ""
