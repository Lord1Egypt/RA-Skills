#!/bin/bash
# 设计师情报站 - 全自动每日执行脚本（v1.6.0）
# 使用方式：./execute_daily.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

DATE=$(date '+%Y-%m-%d')
TIME=$(date '+%H:%M:%S')
OUTPUT_DIR="temp"

echo "======================================"
echo "🚀 设计师情报站 v1.6.0 - 全自动执行"
echo "时间：${DATE} ${TIME}"
echo "======================================"
echo ""

# ========== 步骤 0: 依赖检查 ==========
echo "🔍 步骤 0: 检查依赖..."
if python3 tools/check_dependencies.py; then
    echo "   ✅ 依赖检查通过"
else
    echo "   ⚠️  依赖检查失败，请手动安装依赖"
    echo "   运行：pip install -r requirements.txt"
    exit 1
fi
echo ""

# 创建输出目录
mkdir -p /tmp/dis_daily
mkdir -p "$OUTPUT_DIR"

# ========== 步骤 1: RSS 抓取 ==========
echo "📡 步骤 1: 抓取 RSS 源..."
python3 tools/rss_fetcher.py fetch-all --json > /tmp/dis_daily/rss_items.json 2>&1 || true
RSS_COUNT=$(python3 -c "import json; print(len(json.load(open('/tmp/dis_daily/rss_items.json'))))" 2>/dev/null || echo "0")
echo "   ✅ RSS: $RSS_COUNT 条"
echo ""

# ========== 步骤 2: API 抓取 ==========
echo "🔌 步骤 2: 抓取 API 源..."
python3 tools/api_fetcher.py fetch-all --json > /tmp/dis_daily/api_items.json 2>&1 || true
API_COUNT=$(python3 -c "import json; print(len(json.load(open('/tmp/dis_daily/api_items.json'))))" 2>/dev/null || echo "0")
echo "   ✅ API: $API_COUNT 条"
echo ""

# ========== 步骤 3: Web 抓取（自动化） ==========
echo "🌐 步骤 3: 抓取网页源（自动化）..."
python3 tools/web_fetcher_standalone.py fetch-all 2>&1 | grep "✅" || true

# 合并所有 web 缓存文件（修复：之前只取最新 1 个文件，现在合并全部）
WEB_CACHES=$(ls data/cache/web_cache_*.json 2>/dev/null | sort)
if [ -n "$WEB_CACHES" ]; then
    # 使用 Python 合并所有缓存文件
    python3 << 'EOF'
import json
import glob

all_items = []
cache_files = sorted(glob.glob('data/cache/web_cache_*.json'))

for cache_file in cache_files:
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            items = json.load(f)
            if isinstance(items, list):
                all_items.extend(items)
    except Exception as e:
        print(f"⚠️ 读取 {cache_file} 失败：{e}")

# 去重（按 link 去重）
seen_links = set()
deduped_items = []
for item in all_items:
    link = item.get('link', '')
    if link and link not in seen_links:
        seen_links.add(link)
        deduped_items.append(item)

# 保存合并后的结果
with open('/tmp/dis_daily/web_items.json', 'w', encoding='utf-8') as f:
    json.dump(deduped_items, f, ensure_ascii=False, indent=2)

print(f"合并完成：{len(deduped_items)} 条（来自 {len(cache_files)} 个缓存文件）")
EOF
    WEB_COUNT=$(python3 -c "import json; print(len(json.load(open('/tmp/dis_daily/web_items.json'))))" 2>/dev/null || echo "0")
    echo "   ✅ Web: $WEB_COUNT 条"
else
    echo "   ⚠️  Web 抓取失败，使用空文件"
    echo "[]" > /tmp/dis_daily/web_items.json
    WEB_COUNT=0
fi
echo ""

# ========== 步骤 4: 合并结果 ==========
echo "📊 步骤 4: 合并所有结果..."
python3 tools/fetch_all.py --merge \
  /tmp/dis_daily/rss_items.json \
  /tmp/dis_daily/api_items.json \
  /tmp/dis_daily/web_items.json \
  --output /tmp/dis_daily/all_items.json 2>&1 | tail -3

TOTAL_COUNT=$(python3 -c "import json; print(len(json.load(open('/tmp/dis_daily/all_items.json'))))" 2>/dev/null || echo "0")
echo "   ✅ 合并后：$TOTAL_COUNT 条"
echo ""

# ========== 步骤 5: 输出统计 ==========
echo "======================================"
echo "✅ 抓取完成！"
echo "======================================"
echo ""
echo "📊 数据统计:"
echo "   RSS: $RSS_COUNT 条"
echo "   API: $API_COUNT 条"
echo "   Web: $WEB_COUNT 条"
echo "   总计：$TOTAL_COUNT 条（去重后）"
echo ""
echo "📁 输出文件:"
echo "   /tmp/dis_daily/all_items.json"
echo ""
echo "📝 下一步:"
echo "   Agent 将读取 /tmp/dis_daily/all_items.json"
echo "   按 5 维筛选标准判断，生成 v1.3.3 格式日报"
echo "   并发送 📊 摘要 + 📄 MD 文件给您"
echo ""
