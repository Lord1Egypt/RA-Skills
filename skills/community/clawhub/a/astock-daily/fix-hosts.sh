#!/bin/bash
# 修复阿里云 SMTP DNS 解析问题

echo "🔧 修复阿里云 SMTP DNS 解析"
echo ""

# 检查是否已有记录
if grep -q "smtp.qiye.aliyun.com" /etc/hosts 2>/dev/null; then
    echo "⚠️  /etc/hosts 中已有 smtp.qiye.aliyun.com 记录"
else
    echo "添加 hosts 记录..."
    sudo sh -c 'echo "47.246.165.89 smtp.qiye.aliyun.com" >> /etc/hosts'
    echo "✅ 已添加 smtp.qiye.aliyun.com"
fi

if grep -q "smtp.mxhichina.com" /etc/hosts 2>/dev/null; then
    echo "⚠️  /etc/hosts 中已有 smtp.mxhichina.com 记录"
else
    echo "添加 hosts 记录..."
    sudo sh -c 'echo "47.246.165.89 smtp.mxhichina.com" >> /etc/hosts'
    echo "✅ 已添加 smtp.mxhichina.com"
fi

echo ""
echo "📋 当前 hosts 文件中的阿里云记录:"
grep "aliyun\|mxhichina" /etc/hosts

echo ""
echo "🧪 测试解析:"
ping -c 1 smtp.qiye.aliyun.com 2>&1 | head -2

echo ""
echo "✅ 完成！现在可以重新测试 SMTP 发送了"
echo "   cd /Users/batype/.openclaw/workspace-work/skills/astock-daily"
echo "   source .env && node index.js"
