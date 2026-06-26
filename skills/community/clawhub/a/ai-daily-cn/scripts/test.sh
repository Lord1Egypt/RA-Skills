#!/bin/bash
# AI Daily - 测试脚本
# 验证所有组件是否正常工作

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

echo "🧪 AI Daily - 测试套件"
echo "================================"
echo ""

# 1. 检查 Python
echo "1️⃣ 检查 Python 环境..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "   ✓ $PYTHON_VERSION"
else
    echo "   ✗ python3 not found"
    exit 1
fi

# 2. 检查配置文件
echo ""
echo "2️⃣ 检查配置文件..."
if [ -f "$BASE_DIR/config/sources.json" ]; then
    echo "   ✓ sources.json 存在"
    # 验证 JSON 格式
    if python3 -c "import json; json.load(open('$BASE_DIR/config/sources.json'))" 2>/dev/null; then
        echo "   ✓ sources.json 格式正确"
    else
        echo "   ✗ sources.json 格式错误"
        exit 1
    fi
else
    echo "   ✗ sources.json 不存在"
    exit 1
fi

# 3. 检查主脚本
echo ""
echo "3️⃣ 检查主脚本..."
if [ -f "$BASE_DIR/scripts/ai_daily.py" ]; then
    echo "   ✓ ai_daily.py 存在"
    # 检查语法
    if python3 -m py_compile "$BASE_DIR/scripts/ai_daily.py" 2>/dev/null; then
        echo "   ✓ ai_daily.py 语法正确"
    else
        echo "   ✗ ai_daily.py 语法错误"
        exit 1
    fi
else
    echo "   ✗ ai_daily.py 不存在"
    exit 1
fi

# 4. 检查输出目录
echo ""
echo "4️⃣ 检查输出目录..."
mkdir -p "$BASE_DIR/output"
echo "   ✓ output 目录已创建"

# 5. 检查环境变量
echo ""
echo "5️⃣ 检查环境变量..."
if [ -n "$TAVILY_API_KEY" ]; then
    echo "   ✓ TAVILY_API_KEY 已设置"
else
    echo "   ⚠ TAVILY_API_KEY 未设置（KOL 动态将跳过）"
fi

if [ -n "$ALIBABA_CLOUD_API_KEY" ]; then
    echo "   ✓ ALIBABA_CLOUD_API_KEY 已设置"
else
    echo "   ⚠ ALIBABA_CLOUD_API_KEY 未设置（LLM 处理将使用简化模式）"
fi

# 6. 测试 RSS 抓取
echo ""
echo "6️⃣ 测试 RSS 抓取..."
python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from ai_daily import DataFetcher, load_config

config = load_config()
fetcher = DataFetcher(config)

# 测试一个 RSS feed
test_feeds = [
    'https://news.ycombinator.com/rss',
    'https://xkcd.com/atom.xml'
]

for url in test_feeds:
    items = fetcher.fetch_rss(url)
    if items:
        print(f'   ✓ {url}: 获取 {len(items)} 项')
    else:
        print(f'   ⚠ {url}: 无内容')
"

# 7. 测试 arXiv 抓取
echo ""
echo "7️⃣ 测试 arXiv 抓取..."
python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from ai_daily import DataFetcher, load_config

config = load_config()
fetcher = DataFetcher(config)

papers = fetcher.fetch_arxiv(['cs.AI'], ['LLM'], 3)
if papers:
    print(f'   ✓ arXiv: 获取 {len(papers)} 篇论文')
    for p in papers[:1]:
        print(f'      - {p.title[:60]}...')
else:
    print('   ⚠ arXiv: 无内容')
"

# 8. 快速测试生成（仅 1 个源）
echo ""
echo "8️⃣ 快速测试生成..."
python3 "$SCRIPT_DIR/ai_daily.py" --debug 2>&1 | head -20

echo ""
echo "================================"
echo "✅ 测试完成！"
echo ""
echo "下一步:"
echo "  1. 配置环境变量（推荐）"
echo "  2. 运行：bash scripts/generate.sh"
echo "  3. 查看：bash scripts/view.sh today"
