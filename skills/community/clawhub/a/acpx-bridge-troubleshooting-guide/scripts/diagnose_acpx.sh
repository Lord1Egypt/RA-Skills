#!/bin/bash
# diagnose_acpx.sh - 诊断 acpx 桥接问题
# 检查配置、连接和 Gateway 状态

set -e

echo "🦞 acpx 桥接诊断工具"
echo "===================="
echo ""

# 1. 检查 gateway.token 文件
echo "1️⃣ 检查 gateway.token 文件:"
if [ -f ~/.openclaw/gateway.token ]; then
    echo "   ✅ ~/.openclaw/gateway.token 存在"
    echo "   Token: $(cat ~/.openclaw/gateway.token | head -c 10)..."
else
    echo "   ❌ ~/.openclaw/gateway.token 缺失"
    echo "   修复：echo \"<token>\" > ~/.openclaw/gateway.token"
fi
echo ""

# 2. 检查 acpx 配置
echo "2️⃣ 检查 acpx 配置:"
if [ -f ~/.acpx/config.json ]; then
    echo "   ✅ ~/.acpx/config.json 存在"
    echo "   配置内容:"
    cat ~/.acpx/config.json | sed 's/^/   /'
else
    echo "   ❌ ~/.acpx/config.json 缺失"
fi
echo ""

# 3. 检查 acpx 版本
echo "3️⃣ 检查 acpx 版本:"
acpx --version 2>/dev/null || echo "   ❌ acpx 未安装"
echo ""

# 4. 检查 Gateway 状态
echo "4️⃣ 检查 Gateway 状态:"
openclaw gateway status 2>/dev/null || echo "   ⚠️ 无法获取 Gateway 状态"
echo ""

# 5. 验证 OpenClaw 配置
echo "5️⃣ 验证 OpenClaw 配置:"
openclaw config validate 2>/dev/null || echo "   ⚠️ 配置验证失败"
echo ""

# 6. 运行 doctor
echo "6️⃣ 运行 openclaw doctor:"
openclaw doctor 2>/dev/null || echo "   ⚠️ doctor 检查失败"
echo ""

echo "🦞 诊断完成！"
