---
name: ai-daily-brief-xhs
description: AI 每日简报 - 全球 AI 行业新闻（公司/产品/论文）
version: "1.0.0"
author: seeu1688
license: MIT
slug: ai-daily-brief-xhs
---

# AI Daily Brief · AI 每日简报

## 核心原则

- **权威信源**：只采用权威媒体、官方发布、头部达人、同行评审论文
- **时效性**：推送前一天（24 小时内）的重要信息
- **精选而非堆砌**：每类别 3-5 条最重要信息，避免信息过载
- **结构化输出**：清晰分类，便于快速浏览
- **中文呈现**：英文内容提供中文摘要

---

## 信源列表

### AI 行业大公司新闻（权威媒体）

| 信源 | 类型 | 优先级 |
|------|------|--------|
| OpenAI Blog | 官方博客 | ⭐⭐⭐ |
| Google AI Blog | 官方博客 | ⭐⭐⭐ |
| Microsoft AI Blog | 官方博客 | ⭐⭐⭐ |
| Meta AI Blog | 官方博客 | ⭐⭐⭐ |
| Anthropic Updates | 官方博客 | ⭐⭐⭐ |
| DeepMind Blog | 官方博客 | ⭐⭐⭐ |
| The Verge (AI 板块) | 权威媒体 | ⭐⭐ |
| TechCrunch (AI 板块) | 权威媒体 | ⭐⭐ |
| Reuters Technology | 权威媒体 | ⭐⭐ |
| 机器之心 | 中文权威 | ⭐⭐ |
| 量子位 | 中文权威 | ⭐⭐ |

### AI 行业巨头言论（头部达人）

| 人物 | 平台 | 优先级 |
|------|------|--------|
| Sam Altman | Twitter/X | ⭐⭐⭐ |
| Satya Nadella | Twitter/X | ⭐⭐⭐ |
| Sundar Pichai | Twitter/X | ⭐⭐⭐ |
| Mark Zuckerberg | Twitter/X | ⭐⭐⭐ |
| Dario Amodei | Twitter/X | ⭐⭐⭐ |
| Demis Hassabis | Twitter/X | ⭐⭐⭐ |
| 李开复 | 微博/Twitter | ⭐⭐ |
| 吴恩达 | Twitter/Newsletter | ⭐⭐ |

### LLM/Agent/Skills 技术产品

| 信源 | 类型 | 优先级 |
|------|------|--------|
| GitHub Trending (AI) | 代码平台 | ⭐⭐⭐ |
| Product Hunt (AI) | 产品发布 | ⭐⭐⭐ |
| Hugging Face | 模型发布 | ⭐⭐⭐ |
| LangChain Blog | 技术博客 | ⭐⭐ |
| LlamaIndex Blog | 技术博客 | ⭐⭐ |

### 学术论文（可信来源）

| 信源 | 类型 | 优先级 |
|------|------|--------|
| arXiv (cs.CL/cs.LG/cs.AI) | 预印本 | ⭐⭐⭐ |
| ACL Anthology | 论文库 | ⭐⭐⭐ |
| Google AI Blog (论文) | 官方博客 | ⭐⭐⭐ |
| DeepMind Publications | 官方博客 | ⭐⭐⭐ |
| OpenAI Research | 官方博客 | ⭐⭐⭐ |

---

## 搜索策略

### 搜索工具优先级

**Tavily > 博查 > searxng**

优先使用 Tavily Search（AI 优化），其次博查 API，最后降级到 searxng。

---

### 使用 Tavily Search（首选）

```bash
# AI 公司新闻
node {baseDir}/../tavily-search/scripts/search.mjs "OpenAI OR Google AI OR Microsoft AI OR Meta AI OR Anthropic news yesterday" -n 10 --topic news

# 巨头言论
node {baseDir}/../tavily-search/scripts/search.mjs "Sam Altman OR Satya Nadella OR Mark Zuckerberg AI statement yesterday" -n 5 --topic news

# 技术产品
node {baseDir}/../tavily-search/scripts/search.mjs "LLM OR AI Agent OR AI Skills new release launch yesterday" -n 10 --topic news

# 学术论文（需要获取标题、作者、机构、摘要、arXiv 链接）
node {baseDir}/../tavily-search/scripts/search.mjs "arXiv cs.CL cs.LG cs.AI LLM Agent RAG paper yesterday" -n 10
```

---

### 使用博查 API（备用）

```bash
curl -X POST "https://api.bocha.cn/v1/web-search" \
  -H "Authorization: Bearer $BOCHA_API_KEY" \
  -d '{"query":"OpenAI Google AI Microsoft AI 新闻 昨天","freshness":"day"}'
```

---

### 使用 SearXNG（降级方案）

```bash
uv run {baseDir}/../searxng/scripts/searxng.py search "OpenAI Google AI news yesterday" -n 10 --format json
```

---

## 输出结构

### 固定格式

**注意：** 本技能以文字简报为主，不需要图表。如需可视化（如论文趋势图），参考 nowplaying skill 的浏览器渲染截图方案。

```markdown
# 🤖 AI 每日简报 | {日期}

> 过去 24 小时全球 AI 行业重要动态，助你起床即知天下 AI 事

---

## 🏢 大公司新闻

### 1. 【公司名】新闻标题
**来源：** 信源名称 | **时间：** X 小时前
**摘要：** 1-2 句核心内容摘要
**链接：** [阅读原文](url)

### 2. ...

---

## 💬 巨头言论

### 1. 【人名】(@username)
**平台：** Twitter/微博等 | **时间：** X 小时前
**言论：** 核心观点引用
**链接：** [查看原文](url)

---

## 🛠️ 技术产品

### 1. 【产品名】
**类型：** LLM/Agent/Skills/其他
**发布方：** 公司/团队名
**亮点：** 1-2 句核心功能/创新点
**链接：** [了解更多](url)

---

## 📄 精选论文

### 1. 【论文标题】
**作者：** 作者 1, 作者 2, ...（第一作者机构）
**机构：** 大学/研究机构/公司
**摘要：** 2-3 句核心贡献/方法/结果
**链接：** [arXiv](url) | [代码](github_url)

---

## 📊 今日概览

| 类别 | 数量 |
|------|------|
| 大公司新闻 | X 条 |
| 巨头言论 | X 条 |
| 技术产品 | X 条 |
| 精选论文 | X 条 |

---

*简报生成时间：{时间} | 信源：权威媒体/官方博客/头部达人/arXiv*
```

---

## 执行流程

### Step 1: 确定时间范围

- 获取当前日期和时间
- 计算"前一天"的时间范围（24 小时前至今）
- 格式化为搜索关键词（如"yesterday"、"2026-03-14"）

### Step 2: 并行搜索

同时执行以下搜索：

1. **大公司新闻** - OpenAI/Google/Microsoft/Meta/Anthropic
2. **巨头言论** - Sam Altman/Satya Nadella 等
3. **技术产品** - LLM/Agent/Skills 发布
4. **学术论文** - arXiv 最新论文

### Step 3: 筛选与去重

- 只保留 24 小时内的内容
- 去除重复新闻（同一事件多源报道只保留最佳信源）
- 按重要性排序（官方发布 > 权威媒体 > 其他）

### Step 4: 格式化输出

- 按固定结构组织内容
- 每类别精选 3-5 条
- 提供中文摘要和原文链接

---

## 异常处理

| 情况 | 处理方式 |
|------|----------|
| 某类别无重要新闻 | 标注"今日暂无重要动态"，不强制填充 |
| 搜索 API 异常 | 降级使用备用搜索源，并注明 |
| 周末/节假日 | 正常推送，标注"周末简报" |
| 重大 AI 事件 | 可增加特别板块"特别关注" |

---

## 配置要求

| 配置项 | 说明 | 是否必需 |
|--------|------|----------|
| `TAVILY_API_KEY` | Tavily API 密钥 | ✅ 必需 |
| `BOCHA_API_KEY` | 博查 API 密钥（备用） | ⚠️ 推荐 |

---

## 使用示例

### 手动触发

```
"生成今天的 AI 每日简报"
"昨天 AI 行业有什么大新闻"
```

### 定时任务（推荐）

每天上午 8:00 自动推送：

```json
{
  "name": "ai-daily-brief",
  "schedule": {"kind": "cron", "expr": "0 8 * * *", "tz": "Asia/Shanghai"},
  "payload": {
    "kind": "agentTurn",
    "message": "生成 AI 每日简报，推送过去 24 小时全球 AI 行业重要动态。"
  },
  "delivery": {"mode": "announce", "channel": "feishu"}
}
```
