---
name: claw-news
description: |
  智能每日新闻简报 Skill。支持两种新闻获取模式：(1) 主动搜索 - 基于用户关注的话题/关键词/人名，通过多 AI API 检索全网信息；(2) RSS 订阅 - 从配置的 RSS/Atom 源自动抓取新闻。
  支持智能去重、兴趣管理、AI 摘要、定时推送。
  触发关键词: "newsman", "新闻简报", "每日简报", "claw-news", "添加关注", "interest", "rss"
---

# Claw-News (Newsman)

智能每日新闻简报生成工具，支持**主动搜索**、**RSS 订阅**和**定向爬虫**三种模式。

## 核心功能

### 模式一：主动搜索 (AI Search)
基于用户关注的话题/关键词，通过多 AI API 主动检索全网信息。

- **定时简报** - 每日 9:00 自动生成昨日新闻简报
- **兴趣管理** - 动态添加/删除/查看关注列表
- **多源搜索** - Kimi、MiniMax、Claude API 轮询搜索
- **智能整合** - 自动去重、分类、排序

### 模式二：RSS 订阅 (RSS Feed)
从配置的 RSS/Atom 源自动抓取新闻。

- **RSS 抓取** - 从配置的 RSS 源获取新闻
- **AI 摘要** - 自动生成新闻摘要
- **分类筛选** - 支持按类别过滤 (tech/finance/world/science/sports)

### 模式三：定向爬虫 (Custom Tracker)
针对特定站点的定制化数据抓取。

- **Kickstarter 追踪** - 每周抓取 funding >1000% 的超热门众筹项目
- **可扩展** - 支持添加更多站点追踪器

### 通用功能
- **推送投递** - 通过 Slack/Channel 推送简报
- **定时任务** - 支持 Cron 定时执行

---

## ⚙️ 依赖安装与环境初始化

### 首次安装

```bash
# 进入 skill 目录
cd ~/.openclaw/workspace/skills/claw-news

# 创建虚拟环境（推荐）
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Linux/Mac:
# source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 依赖列表

主要依赖包：
- `openai` >= 1.0.0 (Kimi API)
- `anthropic` >= 0.18.0 (Claude API)
- `requests` >= 2.31.0
- `python-dateutil` >= 2.8.0
- `feedparser` (RSS 支持)
- `tqdm`, `python-dotenv`

---

## 快速开始

### 用户交互命令

```
# === 主动搜索模式 ===
@claw newsman add <关键词>              # 添加关注话题
@claw newsman add <人名> --type person  # 添加人名关注
@claw newsman remove <id>               # 删除关注
@claw newsman list                      # 查看关注列表
@claw newsman run                       # 立即执行简报生成
@claw newsman settings                  # 查看设置

# === RSS 订阅模式 ===
@claw newsman rss fetch                 # 抓取 RSS 新闻
@claw newsman rss digest                # 生成 RSS 简报
@claw newsman rss sources               # 查看 RSS 源列表

# === Kickstarter 追踪模式 ===
@claw newsman kickstarter               # 立即执行 Kickstarter 热门项目抓取
```

### 手动执行 - 主动搜索模式

```bash
# 执行简报生成
python scripts/newsman.py --mode digest

# 仅搜索特定关键词
python scripts/newsman.py --mode search --query "人工智能"

# 测试模式（不发送推送）
python scripts/newsman.py --mode digest --dry-run
```

### 手动执行 - Kickstarter 追踪模式

```bash
# 执行 Kickstarter 追踪（默认阈值 1000%）
python scripts/kickstarter_tracker.py

# 自定义阈值（例如 500%）
python scripts/kickstarter_tracker.py --threshold 500

# 只显示新增项目
python scripts/kickstarter_tracker.py --new-only

# 测试模式（不保存缓存）
python scripts/kickstarter_tracker.py --dry-run
```

### 手动执行 - RSS 订阅模式

```bash
# 抓取所有 RSS 源
python rss/rss_fetcher.py

# 抓取特定类别
python rss/rss_fetcher.py --category tech

# 生成 RSS 简报
python rss/rss_digest.py --category tech --hours 24

# 使用 Kimi API 生成摘要
python rss/rss_summarize.py --input news.json --method api
```

---

## 配置

### 环境变量

创建 `.env` 文件在 skill 根目录：

```bash
# === API Keys (至少配置一个) ===
KIMI_API_KEY=sk-xxx
MINIMAX_API_KEY=xxx
ANTHROPIC_API_KEY=sk-ant-xxx

# === OpenClaw Gateway (用于推送) ===
GATEWAY_URL=http://localhost:3000
GATEWAY_TOKEN=your-token

# === 推送配置 ===
DELIVERY_CHANNEL=slack
SLACK_CHANNEL=#general

# === 可选：自定义时间 ===
DAILY_DIGEST_TIME=09:00
TIMEZONE=Asia/Shanghai

# === RSS 配置 ===
NEWSMAN_CACHE_DIR=./.cache
NEWSMAN_MAX_ITEMS=10
NEWSMAN_SUMMARY_LENGTH=150
```

### 关注列表示例 (主动搜索)

```json
{
  "interests": [
    {
      "id": "uuid-1234",
      "type": "topic",
      "value": "人工智能",
      "keywords": ["AI", "大模型", "AGI"],
      "priority": "high"
    },
    {
      "id": "uuid-5678",
      "type": "person",
      "value": "马斯克",
      "keywords": ["Elon Musk", "Tesla", "SpaceX"],
      "priority": "medium"
    }
  ]
}
```

### RSS 源配置

编辑 `references/rss_sources.md` 添加新的 RSS/Atom feeds。

---

## Cron 配置

### 主动搜索模式 - 每日定时任务

```bash
openclaw cron add \
  --name "claw-news-daily" \
  --schedule "0 9 * * *" \
  --timezone "Asia/Shanghai" \
  --command "python ~/.openclaw/workspace/skills/claw-news/scripts/newsman.py --mode digest"
```

### Kickstarter 追踪模式 - 每周定时任务

```bash
# 每周一早上 9 点抓取 Kickstarter 超热门项目
openclaw cron add \
  --name "kickstarter-weekly" \
  --schedule "0 9 * * 1" \
  --timezone "Asia/Shanghai" \
  --command "python ~/.openclaw/workspace/skills/claw-news/scripts/kickstarter_tracker.py --threshold 1000"
```

### RSS 订阅模式 - 定时任务

```bash
# 每天早上 8 点生成 RSS 简报
openclaw cron add \
  --name "rss-morning-news" \
  --schedule "0 8 * * *" \
  --command "python ~/.openclaw/workspace/skills/claw-news/rss/rss_digest.py --category all"
```

---

## 文件结构

```
claw-news/
├── SKILL.md                    # 主文档
├── .env                        # 环境变量配置
├── scripts/                    # 主动搜索模式
│   ├── newsman.py
│   ├── interest_manager.py
│   ├── search_engine.py
│   ├── result_aggregator.py
│   ├── digest_generator.py
│   └── config.py
├── rss/                        # RSS 订阅模式
│   ├── rss_fetcher.py
│   ├── rss_summarize.py
│   ├── rss_digest.py
│   ├── kimi_client.py
│   └── config.toml
├── references/                 # 参考文档
│   ├── kimi_api.md
│   ├── minimax_api.md
│   ├── claude_api.md
│   └── rss_sources.md
├── assets/                     # 资源文件
│   └── digest_template.md
└── data/                       # 数据文件
```

---

## RSS 新闻分类

默认分类 (可在 `references/rss_sources.md` 中配置)：

| 分类 | 说明 |
|------|------|
| **tech** | 科技、AI、软件、硬件 |
| **finance** | 金融、市场、经济、加密货币 |
| **world** | 国际新闻、政治 |
| **science** | 科学、太空、研究 |
| **sports** | 体育新闻和赛事 |
