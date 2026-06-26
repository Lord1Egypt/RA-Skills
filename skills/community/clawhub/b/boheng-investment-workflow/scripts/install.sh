#!/bin/bash
# boheng-investment-workflow 安装脚本 v1.2.0
# 
# 安全说明：
# - 建议在 Python 虚拟环境中安装
# - 仅安装必要的 Python 依赖
# - 不执行系统级操作

set -e  # 遇到错误立即退出

echo "================================================"
echo "  boheng-investment-workflow 安装脚本 v1.2.0"
echo "================================================"
echo ""

# 检查 Python 版本
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "📋 Python 版本: $PYTHON_VERSION"

# 创建数据目录
DATA_DIR="$HOME/.openclaw/workspace/investment"
echo "📁 创建数据目录: $DATA_DIR"
mkdir -p "$DATA_DIR/reports"
touch "$DATA_DIR/watchlist.txt"

# 安装 Python 依赖
echo ""
echo "📦 安装 Python 依赖..."
echo "   提示：建议在虚拟环境中运行 (python3 -m venv venv && source venv/bin/activate)"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ -f "$SCRIPT_DIR/../requirements.txt" ]; then
    pip3 install -r "$SCRIPT_DIR/../requirements.txt" || {
        echo "❌ 依赖安装失败，请检查 pip 或网络连接"
        exit 1
    }
else
    # 仅安装必需依赖，akshare 为可选依赖
    pip3 install requests beautifulsoup4 || {
        echo "❌ 依赖安装失败，请检查 pip 或网络连接"
        exit 1
    }
    echo ""
    echo "⚠️ 可选依赖："
    echo "   如需使用 --akshare 模式获取深度财务数据，请手动安装："
    echo "   pip3 install akshare pandas"
fi

# 测试基本功能
echo ""
echo "🧪 测试模块加载..."
cd "$SCRIPT_DIR"

python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from config import DATA_DIR, ALLOWED_DOMAINS
    print(f'✅ 配置加载成功')
    print(f'   数据目录: {DATA_DIR}')
    print(f'   允许域名: {ALLOWED_DOMAINS}')
except ImportError as e:
    print(f'❌ 配置加载失败: {e}')
    sys.exit(1)

try:
    from financial_data import FinancialDataFetcher
    from analysts import run_all_analysts
    print('✅ 分析模块加载成功')
except ImportError as e:
    print(f'⚠️ 部分模块加载失败: {e}')
" || {
    echo ""
    echo "⚠️ 模块测试失败，请检查依赖安装"
    exit 1
}

echo ""
echo "================================================"
echo "✅ 安装完成!"
echo "================================================"
echo ""
echo "📚 使用方式:"
echo "  cd ~/.openclaw/skills/boheng-investment-workflow/scripts"
echo "  python3 analyze_stock.py 600919                  # 快速分析"
echo "  python3 analyze_stock.py 600919 江苏银行        # 指定名称"
echo "  python3 analyze_stock.py 600919 --akshare       # 完整分析（需安装akshare）"
echo ""
echo "🔒 安全提示:"
echo "  - 白名单域名: qt.gtimg.cn, web.ifzq.gtimg.cn"
echo "  - 数据存储在: ~/.openclaw/workspace/investment/"
echo "  - 建议在虚拟环境中运行"
echo "  - --akshare 模式需要 akshare 库（可选）"
echo ""