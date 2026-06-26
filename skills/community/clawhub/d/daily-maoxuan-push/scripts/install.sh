#!/bin/bash
# 每日毛选语录推送技能安装脚本

set -e

echo "📦 开始安装每日毛选语录推送技能"
echo "================================="

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装 Python3"
    exit 1
fi

echo "✓ Python3 已安装: $(python3 --version)"

# 检查依赖
echo "🔧 检查依赖..."
if ! python3 -c "import requests" &> /dev/null; then
    echo "📦 安装 requests 库..."
    pip3 install "requests>=2.31.0,<3"
fi

echo "✓ 依赖检查完成"

# 创建日志目录
mkdir -p logs
echo "✓ 创建日志目录: logs/"

# 设置权限
chmod +x scripts/*.py
echo "✓ 设置脚本执行权限"

# 检查配置文件
if [ ! -f references/config.json ]; then
    echo "⚠️  配置文件不存在，创建默认配置"
    cp references/config.example.json references/config.json 2>/dev/null || true
fi

# 检查语录库
if [ ! -f references/maoxuan_quotes.json ]; then
    echo "⚠️  语录库不存在，创建默认语录库"
    cp references/maoxuan_quotes.example.json references/maoxuan_quotes.json 2>/dev/null || true
fi

echo ""
echo "🎉 安装完成！"
echo ""
echo "📋 接下来需要:"
echo "  1. 配置 API Key:"
echo "     openclaw config set 'skills.entries.daily-maoxuan-push.seedreamApiKey' --value '你的API Key'"
echo ""
echo "  2. 测试生成:"
echo "     python3 scripts/generate_daily.py --test"
echo ""
echo "  3. 配置定时任务:"
echo "     openclaw cron create --name '每日毛选语录推送' --schedule '0 9 * * *' --agent imagor --task '执行每日毛选语录推送'"
echo ""
echo "📚 详细文档请查看 README.md"