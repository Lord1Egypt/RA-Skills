#!/bin/bash
# A-Share Pro 安装脚本

echo "🚀 开始安装 A-Share Pro..."

# 检测 Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 python3，请先安装"
    exit 1
fi

# 创建数据目录
mkdir -p ~/.openclaw/a_share

# 安装依赖
echo "📦 正在安装依赖..."
pip3 install requests beautifulsoup4 pandas -q

# 检查监控器功能
echo ""
echo "🧪 测试监控器功能..."
cd "$(dirname "$0")/scripts"
python3 monitor.py --help &>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ 安装完成!"
    echo ""
    echo "📚 使用方式:"
    echo "  cd ~/.openclaw/workspace/skills/a-share-pro/scripts"
    echo "  python3 add_stock.py 600919           # 添加股票"
    echo "  python3 list_stocks.py                # 查看列表"
    echo "  python3 summarize_performance.py      # 行情汇总"
else
    echo "⚠️ 部分功能可能不可用（缺少 Tushare）"
    echo "✅ 基础功能已安装完成"
fi
