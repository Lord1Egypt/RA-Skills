---
name: web-scraper
description: "通用网页数据抓取工具 — 支持CSS选择器抓取链接、表格数据提取，输出CSV/JSON格式。无需配置，开箱即用。"
---

# Web Scraper — 通用网页数据抓取工具

AI agent 专用的网页数据抓取工具。输入网址和CSS选择器，自动抓取链接或表格数据，导出为CSV或JSON。

## 功能

- **链接抓取** — 抓取页面中所有匹配CSS选择器的链接
- **表格抓取** — 自动提取HTML表格数据
- **CSV导出** — 默认输出CSV格式
- **JSON导出** — 支持JSON格式输出
- **中文友好** — 完整支持中文网页编码

## 使用方式

```bash
# 抓取页面所有链接
python scraper.py https://example.com

# 自定义CSS选择器
python scraper.py https://example.com "a.article-link"

# 导出JSON格式
python scraper.py https://example.com "div.item" --json

# 抓取表格数据
python scraper.py https://example.com "table#data" --table --json
```

## 依赖安装

```bash
pip install requests beautifulsoup4
```

## 适用场景

- 数据采集和调研
- 竞品信息监控
- 市场情报收集
- 内容聚合

## Tags
scraping, web, data, python, automation, crawler, data-collection
