---
name: ai-devblog-factory
description: AI 开发博客工厂 - 自动抓取 GitHub Trending 与技术资讯，生成结构化开发周报并发布至飞书
category: AI
triggers: 开发博客, 技术周报, GitHub Trending, 开发者资讯, 生成周报
---

# AI 开发博客工厂 (ai-devblog-factory)

> GitHub Trending + 技术资讯 → AI 分析 → 结构化博客 → 飞书文档

## 🎯 解决痛点

- ❌ 每天刷 GitHub Trending 太耗时，看不完
- ❌ 技术资讯分散在不同平台，汇总困难
- ❌ 手动整理周报费时费力
- ❌ 好内容无法转化为团队知识沉淀

## 💡 解决方案

```
GitHub Trending（今日热门）
        ↓
┌─────────────────────┐
│  Agent-Reach         │ → 抓取 Trending 列表 + 技术资讯
└────────┬────────────┘
         │ 原始数据
   ┌─────▼─────┐
   │  summarize  │ → AI 分析趋势、提炼要点、生成洞察
   └─────┬─────┘
         │ 分析结果
   ┌─────▼──────────┐
   │wechat-article-pro│ → 生成完整博客文章
   └─────┬──────────┘
         │ 文章
   ┌─────▼─────┐
   │ feishu_doc  │ → 发布至飞书 Wiki / 云文档
   └─────────────┘
```

## 📦 包含 Skills

| Skill | 作用 | 调用顺序 |
|-------|------|---------|
| Agent-Reach | 抓取 GitHub Trending 和技术资讯 | 1 |
| summarize | AI 分析趋势、提炼要点 | 2 |
| wechat-article-pro | 生成结构化技术博客 | 3 |
| feishu_doc | 发布至飞书文档 | 4 |

## 🔧 前置要求

1. **GitHub Cookie**（可选）：用于获取更完整的 Trending 数据
2. **飞书机器人**：已配置 feishu_doc 权限
3. **Agent-Reach 配置**：支持 GitHub 和 RSS 源抓取

## 📝 使用方法

### 触发方式

```
/ai-devblog-factory
生成今日技术博客
技术周报生成
```

### 手动执行

```bash
# 方式 1：通过 OpenClaw
openclaw run ai-devblog-factory

# 方式 2：通过 cron 定时生成
# 建议时间：每天早上 9:00 (UTC)
openclaw cron add \
  --name "每日技术博客" \
  --schedule "0 9 * * *" \
  --skill ai-devblog-factory
```

## 🔄 工作流详情

### Step 1: Agent-Reach 内容抓取

```yaml
步骤: 1
技能: Agent-Reach
输入:
  sources:
    - type: github_trending
      params:
        language: all
        since: daily
    - type: rss
      sources:
        - https://dev.to/feed
        - https://hacker-news.firebaseio.com/newstories.json
  tasks:
    - fetch_trending_repos
    - fetch_dev_news
输出:
  trending_repos: ${raw_trending.json}
  dev_news: ${raw_news.json}
```

### Step 2: AI 分析与洞察

```yaml
步骤: 2
技能: summarize
输入:
  content: ${raw_trending.json} + ${raw_news.json}
  tasks:
    - analyze_trends
    - extract_key_insights
    - identify_notable_projects
  outputFormat: structured_json
输出:
  analysis: ${analysis.json}
  insights: ${insights.md}
```

### Step 3: 生成博客文章

```yaml
步骤: 3
技能: wechat-article-pro
输入:
  topic: "GitHub Trending X 日精选 | 技术趋势与开源热点"
  source_data: ${analysis.json}
  style: 技术博客风格
  wordCount: 3000-4000
输出:
  article: ${article.md}
  title: ${title}
```

### Step 4: 发布至飞书

```yaml
步骤: 4
技能: feishu_doc
输入:
  title: "GitHub Trending $(date +%Y-%m-%d) | 技术周报"
  content: ${article.md}
  folder_token: ${target_folder}
  grant_to_requester: true
输出:
  doc_url: ${docUrl}
  doc_id: ${docId}
```

## 📊 输出示例

### 生成的博客结构

```markdown
# GitHub Trending 精选 | 2026-04-15

> 本周最值得关注的技术趋势与开源项目

## 📊 概览
- 新增项目：1,247 个
- 编程语言分布：Python(28%) / JavaScript(22%) / Rust(15%)
- 热榜最高：某 AI 相关项目（3.2k Stars today）

## 🔥 本周热点

### 1. [项目名称](url) ⭐ 2.1k
**语言**: Python | **作者**: xxx
**描述**: 项目简介...
**为什么值得关注**: 关键洞察...

### 2. [项目名称](url) ⭐ 1.8k
...

## 💡 技术趋势分析

**趋势 1：AI 代码生成工具爆发**
过去一周有 23 个新 AI 代码相关项目上榜...

**趋势 2：Rust 在系统编程领域持续增长**
...

## 📰 技术资讯精选

[从 dev.to / HN 精选的技术文章及解读]
...

## 🛠️ 本周推荐学习路径

1. [项目] - 入门指南
2. [项目] - 进阶实践
...

---
*由 AI DevBlog Factory 自动生成 | $(date)*
```

## ⚙️ 自定义配置

### 修改抓取范围

编辑 `workflow.json` 中的 source 配置：

```json
{
  "sources": {
    "github_trending": {
      "languages": ["python", "typescript", "rust"],
      "since": "weekly"
    },
    "rss": {
      "feeds": [
        "https://dev.to/feed",
        "https://news.ycombinator.com/rss"
      ]
    }
  }
}
```

### 修改输出格式

```json
{
  "output": {
    "format": "markdown",
    "platform": "feishu",
    "folder": "your-folder-token",
    "include_code_examples": true
  }
}
```

## 🔒 安全说明

- 抓取内容仅用于个人/团队学习
- 尊重 GitHub API 限制，建议设置抓取间隔
- 飞书文档权限默认仅创建者可见

## 🚀 扩展用法

### 1. 多语言 Trending

```bash
# 生成 Python 技术周报
openclaw run ai-devblog-factory \
  --language python \
  --title "Python 技术周报"
```

### 2. 定时推送至团队群

```bash
# 生成后自动发飞书消息
openclaw run ai-devblog-factory \
  --notify true \
  --chat_id "oc_xxx"
```

### 3. 对比历史趋势

```bash
# 生成趋势对比报告
openclaw run ai-devblog-factory \
  --compare true \
  --compare_weeks 4
```

## ⚠️ 注意事项

1. **API 限制**：GitHub API 有速率限制，大规模抓取建议添加认证
2. **内容质量**：AI 生成的分析仅供参考，请结合实际情况判断
3. **定时任务**：建议设置 12 小时以上的间隔避免 API 限制

## 📞 故障排除

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 抓取为空 | 网络问题 | 检查 Agent-Reach 配置 |
| 文章生成失败 | 内容不足 | 补充 RSS 源 |
| 飞书发布失败 | 权限不足 | 确认 feishu_doc 机器人权限 |
