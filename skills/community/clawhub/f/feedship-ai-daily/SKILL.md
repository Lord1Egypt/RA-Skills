---
version: 1.21.0
name: feedship-ai-daily
description: "Generate daily AI news digest from feedship subscriptions. Use when user wants today's news summary, daily briefing, periodic news recap, AI daily digest, AI 日报, ai 日报, 生成简报, or 大模型日报. The workflow extracts articles, filters for AI/tech content, generates strategic analysis via LLM, and replaces citation placeholders. Requires feedship skill."
metadata:
  openclaw:
    requires:
      bins:
        - uv
    cron:
      syntax: cron([minute,] [hour,] [day-of-month,] [month,] [day-of-week])
      default: "0 8 * * *"  # Daily at 8:00 AM
      description: "Generate daily AI news digest every day at 8 AM"
---

# AI 日报 (Feedship AI Daily)

**Version:** 1.21.0
**For:** OpenClaw compatible agents
**Description:** Generate daily AI news digest via feedship article extraction + AI strategic analysis

## 为什么需要引用替换（Step 3.5）

LLM 生成的引用有两大幻觉风险：
1. **编号幻觉**：引用列表中不存在的编号（如 `${999}`）
2. **展开幻觉**：在引用中直接输出标题/链接时捏造内容

**解决方案：** LLM 只输出 `${N}` 占位符，标题和链接由 `replace_refs.py` 脚本从权威 JSON 中注入。脚本对无效编号会输出 `[无效引用 #N]` 并打印警告。

---

## 1. Setup

This skill requires feedship v1.8.0+. Use the local project version:

```bash
cd /Users/y3/feedship && uv run feedship --version
```

Verify `article` command is available:

```bash
cd /Users/y3/feedship && uv run feedship article --help
```

## 2. Usage

### On-Demand (Manual)

User triggers:
`"生成今日日报"`, `"今日新闻摘要"`, `"daily digest"`, `"AI日报"`, `"生成简报"`, `"大模型日报"`

The agent will activate this skill and run the **Generate Daily Report** flow (see section 3).

### Automatic (Cron)

Schedule daily reports at 8:00 AM Beijing time.

```bash
openclaw cron add \
  --name "feedship-ai-daily" \
  --agent feedship-ai-daily \
  --cron "0 8 * * *" \
  --tz Asia/Shanghai \
  --session isolated \
  --announce \
  --channel <your-channel> \
  --to <your-destination> \
  --timeout-seconds 900 \
  --message "使用 feedship-ai-daily skill 生成今日日报。" \
  --thinking xhigh
```

---

## 3. Generate Daily Report

### Step 1. 提取今日文章（带过滤）

```bash
# 提取今日文章
cd /Users/y3/feedship && uv run feedship article list \
  --since $(date -v-1d +%Y-%m-%d) \
  --until $(date +%Y-%m-%d) \
  --limit 3333 \
  --json > /tmp/today_articles_raw.json

# 过滤出 AI/技术相关标题（节省 token，提升信号比）
python3 -c "
import json, sys
data = json.load(open('/tmp/today_articles_raw.json'))
items = data.get('items', [])
keywords = 'AI|model|agent|LLM|GitHub|open.?source|developer|software|tech|coding|compute|GPU|inference|ML|neural|benchmark|API|protocol|framework|tool'
filtered = [item for item in items if any(k in (item.get('title','') + item.get('description','')) for k in keywords.split('|'))]
# 输出过滤后标题
for i, item in enumerate(filtered):
    t = item.get('title','').strip()
    if t:
        print(f'{i+1}. {t}')
# 保存过滤后数据供替换脚本使用
with open('/tmp/today_articles_filtered.json', 'w') as f:
    article_map = {}
    for i, item in enumerate(filtered):
        t = item.get('title','').strip()
        if t:
            article_map[str(i+1)] = {'title': t, 'link': item.get('link', '')}
    json.dump(article_map, f, ensure_ascii=False, indent=2)
print(f'过滤后: {len(filtered)} 篇 / 原始: {len(items)} 篇', file=sys.stderr)
" > /tmp/article_titles.txt
```

**验证结果:**
```bash
head -10 /tmp/article_titles.txt
echo "---"
python3 -c "import json; print(f'替换脚本使用 {len(json.load(open(\"/tmp/today_articles_filtered.json\")))} 篇文章')"
```

### Step 2. 拼接提示词

从 `references/prompt.md` 读取提示词模板，拼接过滤后的标题列表：

```bash
ARTICLE_TITLES=$(cat /tmp/article_titles.txt)
PROMPT=$(cat skills/feedship-ai-daily/references/prompt.md)
# 拼接：将 # Input Data 后追加标题列表
FULL_PROMPT=$(echo "$PROMPT"; echo ""; echo "$ARTICLE_TITLES")
```

### Step 3. 发送至 LLM

将 `$FULL_PROMPT` 发送给 LLM（MiniMax-M2.7 或同类模型）生成分析。

**⚠️ 重要提示给 LLM：** 在回复中，严格只使用 `${N}` 格式引用新闻，禁止展开标题或链接。

### Step 3.5. 替换引用占位符

```bash
TODAY_ARTICLES=$(python3 -c "import json; print(json.dumps(json.load(open('/tmp/today_articles_filtered.json'))))")
cat LLM_OUTPUT.txt | TODAY_ARTICLES="$TODAY_ARTICLES" \
  python3 skills/feedship-ai-daily/scripts/replace_refs.py > /tmp/daily_report_final.md
```

**脚本功能：**
- `${N}` → `[标题](链接)`
- `${3,7}` → 展开为两个独立链接（空格分隔）
- 无效编号 → `[无效引用 #N]`（带警告）
- **列表项格式** `${N}｜中文标题` → `${N}` 被替换，保留 `｜中文标题`
- 脚本底部打印统计：`[replace_refs] N 处引用已替换`

### Step 4. 输出最终报告

读取 `/tmp/daily_report_final.md` 输出给用户。

---

## 4. Prompt 模板参考

完整的提示词模板位于 `references/prompt.md`，包含：

- **Role**: Principal Tech Strategist & Open-Source Trend Forecaster
- **Citation Rules**: 防幻觉核心规则——LLM 只输出 `${N}`，禁止展开标题/链接
- **Execution Steps**: 4个步骤（分类解构 → 根本原因 → 暗线发现 → 价值翻译）
- **Output Rules**: 语气、结构、约束条件

---

## 5. Troubleshooting

| Problem | Solution |
|---------|----------|
| `feedship: command not found` | 使用 `cd /Users/y3/feedship && uv run feedship` |
| `report` command not found | 全局版本过旧，使用本地 v1.8.0+ 版本 |
| Empty article list | 检查日期范围，确认有文章发布 |
| 大量 `[无效引用 #N]` | LLM 引用了不存在的编号，检查 prompt.md 中的 Citation Rules 是否被遵循 |
| LLM 直接展开标题/链接 | 在 Step 3 发送时强调：禁止展开链接，只输出 `${N}` |
| LLM timeout | 减少 `--limit` 数量；或确保文章过滤后数量在 100 以内 |

---

## 6. Change Log

- **v1.21.0**: 新增文章过滤步骤（AI/Tech 关键词过滤）；强化 Citation Rules 防幻觉约束；替换脚本支持逗号分隔多引用和无效编号警告
- **v1.20.0**: 初始版本，从 `feedship report` 迁移到手动提取 → LLM → 替换 pipeline
