---
name: ai-agent-news-aggregator
description: |
  搜集 AI Agent 领域最新资讯并推送到飞书群聊。使用 DuckDuckGo 搜索 + RSS 源监控，
  自动过滤、去重、摘要，生成每日/每周简报。适用于 AI Agent 行业动态追踪、
  技术进展监控、竞品信息收集。支持定时任务（cron）自动推送。
---

# AI Agent 资讯聚合技能

## 功能概述

本技能自动搜集 AI Agent 相关最新资讯，整理后推送到飞书群聊。

### 核心能力
- 🔍 **多源搜索** - DuckDuckGo 搜索 + RSS 源监控
- 🧹 **智能去重** - 基于标题/URL 相似度合并相同新闻
- 📝 **自动摘要** - 为每条新闻生成一句话摘要
- 📊 **分类整理** - 按技术进展/公司动态/行业应用分类
- 🚀 **飞书推送** - 直接发送到群聊或私聊

---

## 数据源

### 搜索关键词（使用 ddg-search）
- "AI Agent framework"
- "LangChain new release"
- "AutoGen update"
- "Multi-agent system research"
- "Agentic AI"
- "CrewAI"
- "LlamaIndex"

### RSS 源（使用 blogwatcher）
- Hacker News AI/ML tag
- r/LocalLLaMA
- Anthropic Blog
- OpenAI Blog
- Hugging Face Blog
- LangChain Blog

详细配置见 `scripts/sources.json`

---

## 使用方法

### 一次性搜集

```json
{
  "action": "collect",
  "time_range": "24h",
  "channel_id": "oc_xxxxxx"
}
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| time_range | 搜集时间范围 | 24h |
| channel_id | 飞书会话 ID | 当前会话 |

### 定时推送（配合 cron）

```json
{
  "action": "schedule",
  "cron": "0 9 * * 1-5",
  "channel_id": "oc_xxxxxx",
  "time_range": "24h"
}
```

示例：工作日每天 9 点推送前一天的资讯

---

## 输出格式（飞书消息）

```
🤖 AI Agent 每日简报 - 2026-03-16

🔥 头条
• LangChain 发布新 Agent 框架 - 支持 XX 功能 [链接]

🛠️ 框架更新
• AutoGen v0.4.0 - 新增多 Agent 协作 [链接]
• CrewAI 支持 XX [链接]

📚 研究论文
• [论文标题] - arXiv [链接]

🏢 公司动态
• Anthropic 发布 XX [链接]

💼 行业应用
• XX 公司用 Agent 实现 XX [链接]

---
共 12 条资讯 | 来源：DDG + 6 RSS 源
```

---

## 脚本说明

### scripts/search_news.py
调用 ddg-search 搜索多个关键词，返回原始结果列表。

**输入：**
```json
{
  "keywords": ["AI Agent", "LangChain"],
  "time_range": "24h"
}
```

**输出：**
```json
{
  "items": [
    {"title": "...", "url": "...", "snippet": "...", "source": "ddg"},
    ...
  ]
}
```

### scripts/deduplicate.py
基于标题和 URL 相似度去重。

**输入：**
```json
{
  "items": [...],
  "threshold": 0.85
}
```

**输出：**
```json
{
  "items": [...],
  "removed_count": 5
}
```

### scripts/summarize.py
调用 LLM 为每条新闻生成一句话摘要。

**输入：**
```json
{
  "items": [...],
  "max_length": 50
}
```

**输出：**
```json
{
  "items": [
    {"title": "...", "url": "...", "summary": "..."},
    ...
  ]
}
```

### scripts/push_to_feishu.py
格式化消息并推送到飞书。

**输入：**
```json
{
  "items": [...],
  "channel_id": "oc_xxxxxx",
  "date": "2026-03-16"
}
```

**输出：**
```json
{
  "success": true,
  "message_id": "msg_xxxxxx"
}
```

### scripts/sources.json
配置数据源和推送目标。

```json
{
  "keywords": [
    "AI Agent framework",
    "LangChain",
    "AutoGen",
    "CrewAI",
    "Multi-agent system"
  ],
  "rss_sources": [
    "https://news.ycombinator.com/newest",
    "https://www.anthropic.com/news/rss.xml",
    "https://openai.com/blog/rss/"
  ],
  "feishu": {
    "channel_id": "oc_xxxxxx"
  },
  "filters": {
    "min_relevance": 0.7,
    "max_items_per_category": 5
  }
}
```

---

## 完整工作流程

```
1. search_news.py    → 从 DDG + RSS 抓取原始内容
        ↓
2. deduplicate.py    → 去重（基于相似度）
        ↓
3. categorize.py     → 分类（头条/框架/论文/公司/应用）
        ↓
4. summarize.py      → 生成摘要
        ↓
5. push_to_feishu.py → 格式化并推送
```

---

## 依赖工具

- `ddg-search` - DuckDuckGo 网页搜索
- `blogwatcher` - RSS 源监控（可选）
- `web_fetch` - 抓取网页详情（可选）

---

## 配置步骤

1. **编辑 `scripts/sources.json`**
   - 设置你的飞书 `channel_id`
   - 自定义搜索关键词
   - 添加/删除 RSS 源

2. **测试运行**
   ```
   python scripts/search_news.py
   ```

3. **设置定时任务（可选）**
   使用 cron 技能设置每日/每周自动推送

---

## 注意事项

- 首次运行需要安装 Python 依赖（见 scripts/requirements.txt）
- 飞书 channel_id 可从群聊 URL 或消息元数据中获取
- 如需推送到私聊，使用你的个人 session_id
