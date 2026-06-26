#!/bin/bash
# 投资研究系统 - 卸载脚本

echo "🗑️ 卸载投资研究系统..."
echo ""

# 询问是否删除数据
read -p "是否删除分析报告和历史数据？(y/N) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf ~/.openclaw/investment
    echo "✅ 已删除数据目录"
else
    echo "ℹ️ 数据目录已保留：~/.openclaw/investment"
fi

echo ""
echo "✅ 卸载完成"
