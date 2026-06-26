---
name: caixin
description: Fetch and summarize Chinese tech news from 财新网 (caixin.com). Use when user asks about caixin tech news, tech updates from 财新, or wants news from caixin.com/tech/.
---

# 财新科技新闻

Fetch tech news from https://www.caixin.com/tech/

## Usage

Use `web_fetch` to get content from:
- https://www.caixin.com/tech/

Extract the latest news articles (titles, summaries, dates). Present in clean Chinese format with:
- 日期
- 标题
- 简要摘要

## Output Format

按时间倒序排列今日/昨日要闻，每条包含：
- 新闻标题
- 一句话摘要
- 相关链接

过滤掉纯股票代码、重复内容、无意义噪音。
