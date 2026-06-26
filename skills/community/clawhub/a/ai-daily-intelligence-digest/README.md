# AI Daily Intelligence Digest

> 多源热点聚合 → AI智能摘要 → 飞书Wiki一键发布

---

## 🔍 业务场景

某科技公司产品运营团队，每天早上需要快速了解：
- 行业最新热点（TechCrunch、HackerNews、BBC Tech）
- 竞品动态
- AI/大模型前沿进展

**现状痛点**：运营同学手动打开10+网站→复制粘贴→整理→发到飞书，耗时1小时+，且容易遗漏。

---

## 💡 解决方案

**AI Daily Intelligence Digest** 自动化这个流程：

```
┌─────────────────┐
│  rss-aggregator  │  批量抓取 TechCrunch / HackerNews / BBC Tech 等 RSS 源
└────────┬────────┘
         │ raw articles (title + link + description)
         ▼
┌─────────────────┐
│  summarize-pro  │  GPT-4o-mini 批量摘要，提取核心观点，生成要点bullet
└────────┬────────┘
         │ digest markdown
         ▼
┌─────────────────┐
│   feishu-wiki   │  格式化为飞书Wiki页面，自动创建/更新知识库节点
└─────────────────┘
         │
         ▼
   📄 飞书Wiki知识库页面（团队共享）
```

---

## 🎯 痛点分析

| 痛点 | 解决方式 |
|---|---|
| 信息源分散，逐一打开耗时 | rss-aggregator 批量并发抓取 |
| 英文内容阅读慢 | summarize-pro 自动翻译+摘要 |
| 手动复制粘贴格式混乱 | workflow.json 标准化输出模板 |
| 每天重复操作烦琐 | cron 定时自动执行（推荐早8:00） |
| 知识无法积累沉淀 | 持续写入飞书Wiki，形成团队知识库 |

---

## 📊 编排图谱

```
rss-aggregator          summarize-pro           feishu-wiki
─────────────────       ──────────────          ───────────
输入: RSS URL列表          输入: 原始文章列表        输入: Markdown摘要
      │                         │                      │
      ▼                         ▼                      ▼
输出: 文章列表         →   输出: 摘要Bullet    →   输出: Wiki页面链接
    title, link,             key insights,            wiki_page_url
    description              tl;dr summary
```

---

## 🚀 使用示例

### 手动触发

```bash
openclaw run ai-daily-intelligence-digest
```

### 查看输出

```
✅ RSS抓取完成: 抓取 3 个来源，共 23 篇文章
✅ AI摘要完成: 生成 10 条关键洞察
✅ 飞书Wiki发布成功: https://feishu.cn/wiki/xxx
📅 页面标题: 📰 AI日报 | 2026年04月14日
```

### Cron 定时（推荐）

```bash
openclaw cron add "0 8 * * *" "ai-daily-intelligence-digest" \
  --name "AI每日益汇报" \
  --channel feishu
```

---

## 📁 文件结构

```
ai-daily-intelligence-digest/
├── SKILL.md          # 技能定义（含frontmatter元数据）
├── README.md         # 本文件（业务场景+编排说明）
├── workflow.json     # 工作流编排定义
└── config.yaml       # 配置文件（RSS源、Feishu参数）
```

---

## ⚙️ 配置说明

### config.yaml 示例

```yaml
rss:
  feeds:
    - https://hnrss.org/frontpage          # HackerNews
    - https://feeds.bbci.co.uk/news/technology/rss.xml
    - https://www.techcrunch.com/feed/
  max_articles: 10      # 每个源最多取多少篇
  language: en

summarize:
  model: gpt-4o-mini
  max_length: 300       # 每条摘要最大字符数
  style: bullet_points  # 输出风格: bullet_points | paragraph

feishu:
  wiki_space_id: "${FEISHU_WIKI_SPACE_ID}"
  parent_node_token: "${FEISHU_PARENT_NODE}"
  title_prefix: "📰 AI日报"
  time_format: "%Y年%m月%d日"
```

---

## 🔗 依赖技能

| 技能 | 版本 | 用途 |
|---|---|---|
| `rss-aggregator` | ≥1.0.0 | 多源RSS热点抓取 |
| `summarize-pro` | ≥1.0.0 | AI批量摘要+翻译 |
| `feishu-wiki` | ≥1.0.0 | 飞书Wiki知识库写入 |

---

## 📌 适用人群

- **运营同学**：每日益汇报、竞品动态追踪
- **产品经理**：行业热点监控、需求灵感收集
- **管理层**：每日行业简报，高效信息同步
- **研究团队**：持续积累行业知识库
