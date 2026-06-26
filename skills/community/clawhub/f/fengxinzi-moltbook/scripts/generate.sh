#!/bin/bash
# Moltbook日报生成脚本
# 需要配置环境变量

# ============ 配置区域 ============
# 建议通过环境变量配置，敏感信息不要写死在代码中

# Get笔记配置（从环境变量读取）
GETNOTE_KEY="${GETNOTE_API_KEY:-}"
GETNOTE_CLIENT="${GETNOTE_CLIENT_ID:-}"

# Moltbook API
MOLTBOOK_KEY="${MOLTBOOK_API_KEY:-}"

# 邮件配置（可选）
SMTP_PASSWORD="${SMTP_PASSWORD:-}"
RECIPIENT="${RECIPIENT:-zeng5827@163.com}"

# 检查必需配置
if [ -z "$GETNOTE_KEY" ] || [ -z "$GETNOTE_CLIENT" ]; then
    echo "⚠️ 请配置环境变量 GETNOTE_API_KEY 和 GETNOTE_CLIENT_ID"
    echo "详见: https://github.com/your-repo/moltbook-generator"
    exit 1
fi

if [ -z "$MOLTBOOK_KEY" ]; then
    echo "⚠️ 请配置环境变量 MOLTBOOK_API_KEY"
    exit 1
fi

# ============ 以下为核心逻辑 ============

WORKSPACE="/path/to/moltbook-generator"
DATE=$(date +%Y-%m-%d)
NOTE_TITLE="🦞 Moltbook 日报 - ${DATE}"
OUTPUT_FILE="$WORKSPACE/output/moltbook-report-${DATE}.md"
LOG_FILE="${MOLTBOOK_LOG:-/tmp/moltbook.log}"

# 创建输出目录
mkdir -p "$WORKSPACE/output"

echo "🔍 开始抓取Moltbook热门内容... $(date)"

# ============ 1. 收集数据 ============
echo "📊 步骤1: 收集Moltbook数据..."

# 调用Moltbook API（示例，实际需要根据API调整）
# API文档: https://www.moltbook.com/api/docs

# 这里需要调用 collect-moltbook.sh 或直接调用API
# 假设数据保存在 moltbook-daily/ 目录

DATA_FILE="$WORKSPACE/data/moltbook-top20-${DATE}.csv"

if [ ! -f "$DATA_FILE" ]; then
    echo "⚠️ 数据文件不存在: $DATA_FILE"
    echo "请先运行数据收集脚本"
    exit 1
fi

# ============ 2. 过滤去重 ============
echo "🔎 步骤2: 过滤重复内容..."

# 按标题去重，保留15条
CONTENT_DATA=$(tail -n +2 "$DATA_FILE" | awk -F',' '!seen[$3]++ {print}' | head -15)
TOTAL_LINES=$(echo "$CONTENT_DATA" | wc -l)
echo "✅ 过滤后保留: $TOTAL_LINES 条内容"

# ============ 3. 生成结构化报告 ============
echo "📝 步骤3: 生成结构化报告..."

# 这里需要AI模型深度处理
# 实际执行时由AI模型读取数据并按模板输出

cat > "$OUTPUT_FILE" << 'TEMPLATE'
# 🦞 Moltbook AI Agent 社交网络日报

**日期**: DATE_PLACEHOLDER
**发送者**: fengxinzi_pm (疯信子项目总监)
**内容**: 15条高价值热门内容 + AI深度思考

---

## 🔥 1. [热门评论] 标题

**一句话懂It**: [15字以内]

**内容摘要**:
> * [核心观点]
> * [背景/上下文]
> * [价值点]

**AI深度思考**:
- 分析: [深度解读]
- 讨论点: [可能话题]
- 价值: [对读者的意义]

**来源信息**:
- 作者: @xxx
- 赞: x 评: x
- 质量评分: x.x
- 链接: [原文]

---

TEMPLATE

# 替换日期
sed -i "s/DATE_PLACEHOLDER/$DATE/g" "$OUTPUT_FILE"

# ============ 4. 保存到GetNote ============
echo "💾 步骤4: 保存到Get笔记..."

CONTENT=$(cat "$OUTPUT_FILE")
JSON_CONTENT=$(python3 -c "import json; print(json.dumps('''$CONTENT'''))")

RESULT=$(curl -s -X POST "https://openapi.biji.com/open/api/v1/resource/note/save" \
  -H "Authorization: ${GETNOTE_KEY}" \
  -H "X-Client-ID: ${GETNOTE_CLIENT}" \
  -H "Content-Type: application/json" \
  -d "{\"note_type\":\"plain_text\",\"title\":\"${NOTE_TITLE}\",\"content\":${JSON_CONTENT},\"tags\":[\"Moltbook\",\"AI\",\"日报\"]}")

if echo "$RESULT" | grep -q '"success":true'; then
    echo "✅ GetNote保存完成"
    echo "$(date) - SUCCESS" >> "$LOG_FILE"
else
    echo "⚠️ GetNote保存失败: $RESULT"
    echo "$(date) - FAILED: $RESULT" >> "$LOG_FILE"
fi

# ============ 5. 发送邮件（可选）===========
if [ -n "$SMTP_PASSWORD" ] && [ -n "$RECIPIENT" ]; then
    echo "📧 步骤5: 发送邮件..."
    # 邮件发送逻辑（需要SMTP配置）
    echo "📝 邮件功能需要额外配置SMTP"
fi

echo "🎉 任务完成 - $(date)"
