#!/bin/bash
# AI资讯生成脚本
# 需要配置环境变量或修改下方默认值

# ============ 配置区域 ============
# 建议通过环境变量配置，敏感信息不要写死在代码中

# Get笔记配置（从环境变量读取）
GETNOTE_KEY="${GETNOTE_API_KEY:-}"
GETNOTE_CLIENT="${GETNOTE_CLIENT_ID:-}"

# 如果环境变量为空，提示用户
if [ -z "$GETNOTE_KEY" ] || [ -z "$GETNOTE_CLIENT" ]; then
    echo "⚠️ 请配置环境变量 GETNOTE_API_KEY 和 GETNOTE_CLIENT_ID"
    echo "详见: https://github.com/your-repo/ai-news-generator"
    exit 1
fi

# ============ 以下为核心逻辑 ============

DATE=$(date +%Y-%m-%d)
NOTE_TITLE="[AI资讯] ${DATE}"
OUTPUT_FILE="/tmp/ai-news-${DATE}.md"
LOG_FILE="${AI_NEWS_LOG:-/tmp/ai-news.log}"

# 搜索关键词（可修改config/keywords.json）
INDUSTRY_KEYWORDS="GPT Claude 大模型 更新 2026 OpenAI Google Anthropic"
OPEN_SOURCE_KEYWORDS="GitHub trending AI 工具 开源"
INSIGHT_KEYWORDS="AI 趋势 报告 2026 research"

echo "🔍 开始抓取AI资讯... $(date)"

# ============ 搜索函数 ============
search_ddgs() {
    local query="$1"
    local count="${2:-10}"
    ddgs text -q "$query" -m "$count" 2>/dev/null
}

search_x() {
    local query="$1"
    local count="${2:-10}"
    # 需要安装 felo-x-search skill
    node /path/to/felo-x-search/scripts/run_x_search.mjs "$query" -l "$count" 2>&1 | grep -v "Searching"
}

fetch_content() {
    local url="$1"
    web_fetch --url "$url" --maxChars 5000 2>/dev/null || echo "FETCH_FAILED"
}

# ============ 搜索阶段 ============
echo "📡 搜索行业热点..."
INDUSTRY_RAW=$(search_ddgs "$INDUSTRY_KEYWORDS" 15)

echo "📡 搜索开源项目..."
OPEN_SOURCE_RAW=$(search_ddgs "$OPEN_SOURCE_KEYWORDS" 10)

echo "📡 搜索深度观点..."
INSIGHT_RAW=$(search_ddgs "$INSIGHT_KEYWORDS" 10)

# ============ 内容生成 ============
# 这里需要AI模型深度处理，生成结构化内容
# 实际执行时由AI模型读取搜索结果并按模板输出

echo "📝 生成结构化资讯..."

# 模板输出（实际由AI模型填充）
cat > "$OUTPUT_FILE" << 'TEMPLATE'
# AI资讯

**更新日期**: DATE_PLACEHOLDER

---

## 🔥 行业核弹

### 1. [标题]

**一句话懂它**: [15字以内]

**核心信息提取**:
> * [要点1]
> * [要点2]
> * [要点3]

**博主创作视角**: [解读切入点]

**来源溯源**: [链接]

---

TEMPLATE

# 替换日期
sed -i "s/DATE_PLACEHOLDER/$DATE/g" "$OUTPUT_FILE"

# ============ 保存到GetNote ============
echo "💾 保存到Get笔记..."
CONTENT=$(cat "$OUTPUT_FILE")
JSON_CONTENT=$(python3 -c "import json; print(json.dumps('''$CONTENT'''))")

RESULT=$(curl -s -X POST "https://openapi.biji.com/open/api/v1/resource/note/save" \
  -H "Authorization: ${GETNOTE_KEY}" \
  -H "X-Client-ID: ${GETNOTE_CLIENT}" \
  -H "Content-Type: application/json" \
  -d "{\"note_type\":\"plain_text\",\"title\":\"${NOTE_TITLE}\",\"content\":${JSON_CONTENT},\"tags\":[\"AI\",\"资讯\",\"每日汇总\"]}")

if echo "$RESULT" | grep -q '"success":true'; then
    echo "✅ AI资讯已保存到Get笔记"
    echo "$RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print('笔记ID:', d['data']['id'])"
    echo "$(date) - SUCCESS" >> "$LOG_FILE"
else
    echo "❌ 保存失败: $RESULT"
    echo "$(date) - FAILED: $RESULT" >> "$LOG_FILE"
    exit 1
fi

echo "🎉 完成！"
