---
name: battery-market-watch
description: |
  电池行业国际市场动态监控系统。监控中国、美国、印度、俄罗斯、韩国的政策补贴、法规、安全事件和行业投资动态,优先使用官方/行业 RSS 与 Google News RSS 获取稳定新闻源,再抓取详情、分类利好利空并生成偏证券研究风格的周报。支持非中文新闻的原文摘要、中文翻译、以及每条新闻的单条行业解读。用户要求"运行电池市场监控"、"优化电池市场监控 skill"、"做五国电池政策/事故周报"、"追踪国际电池政策补贴新闻"时使用。
---

# 电池行业国际市场动态监控 Skill

## 工作流

```text
[Step 1] scripts/search_news.py
  先抓 RSS,再抓 Google News RSS,不够再回退搜索页

[Step 2] scripts/fetch_detail.py
  抓详情页正文、日期,并做初步类型/情绪分类

[Step 3] scripts/analyze_sentiment.py
  汇总利好/利空/中性,写影响分析

[Step 4] scripts/generate_report.py
  生成偏证券研究简报风格的 Markdown 和 Word 周报
```

## 关键文件

- `config.json`:国家、关键词、RSS、过滤词、输出上限
- `scripts/search_news.py`:核心搜索入口,已经重构
- `scripts/fetch_detail.py`:详情抽取
- `scripts/analyze_sentiment.py`:分析汇总
- `scripts/generate_report.py`:报告生成

## 运行方式

### 手动全流程

按顺序运行:

```bash
py scripts/search_news.py
py scripts/fetch_detail.py
py scripts/analyze_sentiment.py
py scripts/generate_report.py
```

### 快速联调

```bash
py scripts/quick_test.py
```

## 报告特点

- 非中文新闻保留**原文摘要 + 中文翻译**
- 每条新闻带**单条行业解读**
- 报告加入**投资结论 / 风险提示**
- Word/Markdown 统一按更偏**研究简报**结构输出,并对重点词做高亮

## 输出结果

- 原始新闻:`data/news_raw_YYYYMMDD.json`
- 详情解析:`data/news_parsed_YYYYMMDD.json`
- 分析结果:`data/news_analyzed_YYYYMMDD.json`
- 分析摘要:`data/news_analysis_YYYYMMDD.md`
- 周报:`data/周报_YYYYMMDD.md`
- Word周报:`data/周报_YYYYMMDD.docx`

## 适用场景

- 每周五生成五国电池市场周报
- 跟踪补贴、法规、召回、火灾、扩产投资
- 快速看某国最近电池政策风向
