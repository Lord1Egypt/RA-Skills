#!/bin/bash
# CryptoScope SkillPay 配置脚本
# 用途：在 SkillPay 后台创建技能并更新配置

set -e

echo "🔧 CryptoScope SkillPay 配置向导"
echo "=================================================="
echo ""

# 当前配置
CURRENT_SKILL_ID="f3d8a4b2-1c7e-4f9a-8c3d-5e7b8d9f1a2b"
API_KEY="sk_0de94ea93e9aca73aafc2b6457b8de378389a21661f9c6ad4e6b7929e390e971"

echo "📋 当前状态："
echo "  Skill ID: $CURRENT_SKILL_ID (临时ID)"
echo "  API Key: ${API_KEY:0:20}..."
echo ""

echo "=================================================="
echo "步骤1️⃣ : 在 SkillPay 后台创建技能"
echo "=================================================="
echo ""
echo "👉 请打开浏览器访问："
echo "   https://skillpay.me/dashboard/skills"
echo ""
echo "📝 填写以下信息："
echo ""
echo "┌─────────────────────────────────────────┐"
echo "│ 技能名称: CryptoScope                   │"
echo "│ 描述: 加密货币技术分析和交易信号生成      │"
echo "│                                         │"
echo "│ 详细说明:                               │"
echo "│ ✅ 支持10000+币种实时价格查询           │"
echo "│ ✅ 多种技术指标（MA20/50、RSI、MACD）   │"
echo "│ ✅ 智能交易信号（BUY/SELL/HOLD）        │"
echo "│ ✅ 置信度和风险评估                     │"
echo "│ ✅ 历史数据分析（90天）                 │"
echo "│ ✅ CoinGecko API（免费，无需Key）       │"
echo "│                                         │"
echo "│ 定价: \$0.05 USDT / 次                  │"
echo "│ 分类: 数据分析                          │"
echo "│ 标签: crypto, bitcoin, trading, analysis│"
echo "└─────────────────────────────────────────┘"
echo ""

read -p "✅ 已创建技能？按回车继续..."
echo ""

echo "=================================================="
echo "步骤2️⃣ : 复制真实 Skill ID"
echo "=================================================="
echo ""
echo "👉 在 SkillPay 页面找到："
echo "   Skill ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
echo ""
echo "   ⚠️  请立即复制这个ID！"
echo ""

read -p "请粘贴 Skill ID: " NEW_SKILL_ID
echo ""

if [ -z "$NEW_SKILL_ID" ]; then
    echo "❌ 错误：Skill ID 不能为空"
    exit 1
fi

echo "=================================================="
echo "步骤3️⃣ : 更新配置文件"
echo "=================================================="
echo ""

# 备份原文件
SCRIPT_PATH="$HOME/.openclaw/workspace/skills/crypto-scope/scripts/crypto_analyzer_paid.py"
cp "$SCRIPT_PATH" "${SCRIPT_PATH}.backup"

# 更新 Skill ID
sed -i.tmp "s/$CURRENT_SKILL_ID/$NEW_SKILL_ID/g" "$SCRIPT_PATH"
rm -f "${SCRIPT_PATH}.tmp"

echo "✅ 配置已更新"
echo "  旧ID: $CURRENT_SKILL_ID"
echo "  新ID: $NEW_SKILL_ID"
echo "  备份: ${SCRIPT_PATH}.backup"
echo ""

echo "=================================================="
echo "步骤4️⃣ : 验证配置"
echo "=================================================="
echo ""

# 验证更新
if grep -q "$NEW_SKILL_ID" "$SCRIPT_PATH"; then
    echo "✅ 验证成功：Skill ID 已更新"
else
    echo "❌ 验证失败：请手动检查文件"
    exit 1
fi

echo ""

echo "=================================================="
echo "步骤5️⃣ : 测试付费流程（可选）"
echo "=================================================="
echo ""

read -p "是否测试付费流程？(y/N): " TEST_CHOICE
echo ""

if [ "$TEST_CHOICE" = "y" ] || [ "$TEST_CHOICE" = "Y" ]; then
    echo "🧪 测试中..."
    cd "$HOME/.openclaw/workspace/skills/crypto-scope"
    python3 scripts/crypto_analyzer_paid.py signal bitcoin --user-id test_user 2>&1 | head -20
    echo ""
    echo "✅ 测试完成"
else
    echo "⏭️  跳过测试"
fi

echo ""

echo "=================================================="
echo "🎉 配置完成！"
echo "=================================================="
echo ""
echo "📊 技能状态："
echo "  ✅ CryptoScope 已上线"
echo "  ✅ 定价: \$0.05 USDT/次"
echo "  ✅ Skill ID: $NEW_SKILL_ID"
echo ""
echo "💰 预期收益："
echo "  日收入: \$0.25 (5次调用)"
echo "  月收入: \$7.5"
echo "  年收入: \$90"
echo ""
echo "🚀 下一步："
echo "  1. 推广到社区（掘金/即刻）"
echo "  2. 监控 SkillPay Dashboard"
echo "  3. 收集用户反馈并优化"
echo ""
echo "📚 相关文件："
echo "  - 配置文件: $SCRIPT_PATH"
echo "  - 备份文件: ${SCRIPT_PATH}.backup"
echo "  - 使用文档: ~/.openclaw/workspace/skills/crypto-scope/SKILL.md"
echo ""
