---
name: daily-briefing-generator
description: 每日简报生成器。自动聚合多个信息源（RSS、网页、Tavily搜索），生成结构化每日简报，支持定时推送。当用户需要：生成每日行业简报、汇总多渠道资讯、制作早报/晚报、定时推送简报给团队时使用此技能。
---

# Daily Briefing Generator

每日简报生成器。聚合多源资讯，生成结构化每日简报并推送。

## 核心能力

1. **多源聚合** — RSS订阅、网页抓取、Tavily搜索
2. **内容去重** — 智能合并相似内容
3. **结构化输出** — 按行业/主题分类的简报格式
4. **定时推送** — 每日定时推送到企业微信/飞书/钉钉

## 快速开始

### 生成今日简报

```bash
python3 scripts/generate_briefing.py \
  --sources "AI科技,电商,政策" \
  --max-items 10 \
  --output ./daily_briefing.md
```

### 订阅 RSS 并生成简报

```bash
python3 scripts/generate_briefing.py \
  --rss ./feeds.txt \
  --output ./daily.md
```

### 创建每日定时推送

```bash
python3 scripts/schedule_briefing.py \
  --sources "AI科技" \
  --schedule "0 8 * * *" \
  --channel wecom \
  --timezone "Asia/Shanghai"
```

## 脚本说明

### scripts/generate_briefing.py

生成每日简报。

```bash
python3 scripts/generate_briefing.py \
  --sources "<关键词1,关键词2>" \
  --max-items <数量> \
  --output <文件> \
  [--rss <rss文件路径>]
```

**参数：**
- `--sources`: 逗号分隔的信息源关键词
- `--max-items`: 每类最大条目数
- `--output`: 输出文件路径
- `--rss`: RSS订阅文件（每行一个URL）

### scripts/schedule_briefing.py

创建每日简报定时推送任务。

```bash
python3 scripts/schedule_briefing.py \
  --sources "<关键词>" \
  --schedule "<cron>" \
  --channel <wecom|feishu|ddingtalk> \
  [--timezone <时区>]
```

## 输出格式

```markdown
# 每日简报 — YYYY-MM-DD

## 今日要点
- 概要1
- 概要2

## 行业动态
### AI / 科技
1. [标题](链接) — 摘要
2. ...

### 电商 / 零售
1. ...

## 政策风向
1. ...

## 本周关注
1. ...

---
*由 daily-briefing-generator 生成 | YYYY-MM-DD*
```

## 推荐 RSS 订阅配置

在 `feeds.txt` 中每行一个 RSS 地址，例如：
```
https://feeds.example.com/tech
https://feeds.example.com/ecommerce
```
