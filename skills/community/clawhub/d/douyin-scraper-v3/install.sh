#!/bin/bash
# 抖音爆款爬虫 Skill 安装脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📦 正在安装抖音爆款爬虫 Skill..."
echo ""

# 检查 Python
if command -v python3 &> /dev/null; then
    echo "✅ Python3 已安装"
else
    echo "❌ 未找到 Python3，请先安装 Python3"
    exit 1
fi

# 检查 Node.js（可选）
if command -v node &> /dev/null; then
    echo "✅ Node.js 已安装"
else
    echo "⚠️  未找到 Node.js，将只安装 Python 版本"
fi

# 创建 Python 虚拟环境
echo ""
echo "🐍 创建 Python 虚拟环境..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ 虚拟环境已创建"
else
    echo "✅ 虚拟环境已存在"
fi

# 激活虚拟环境并安装依赖
echo ""
echo "📦 正在安装 Python 依赖..."
source venv/bin/activate
pip install --upgrade pip
pip install playwright

# 安装浏览器
echo ""
echo "🌐 正在安装 Playwright 浏览器..."
playwright install chromium

# 安装 Node.js 依赖（如果有 Node.js）
if command -v npm &> /dev/null; then
    echo ""
    echo "📦 正在安装 Node.js 依赖..."
    npm install
fi

# 设置脚本权限
echo ""
echo "🔧 设置脚本权限..."
chmod +x scripts/scraper.py
chmod +x scripts/douyin_scraper.js

# 创建启动脚本
echo ""
echo "🚀 创建启动脚本..."

cat > run.sh << 'EOF'
#!/bin/bash
# 抖音爬虫启动脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 激活虚拟环境
source venv/bin/activate

# 运行 Python 爬虫
python scripts/scraper.py "$@"
EOF

chmod +x run.sh

echo ""
echo "✅ 安装完成！"
echo ""
echo "🚀 快速开始："
echo ""
echo "方式一：使用启动脚本（推荐）"
echo "  ./run.sh search --keyword \"海鲜\" --limit 10"
echo "  ./run.sh hot --limit 20"
echo ""
echo "方式二：手动激活虚拟环境"
echo "  source venv/bin/activate"
echo "  python scripts/scraper.py search --keyword \"海鲜\" --limit 10"
echo ""
echo "Node.js 版本："
echo "  node scripts/douyin_scraper.js search \"海鲜\" 10"
echo "  node scripts/douyin_scraper.js hot 20"
echo ""
echo "📖 更多说明请查看："
echo "  README.md - 快速开始指南"
echo "  SKILL.md - 详细使用文档"
echo ""
