---
name: browser-automation-zh
description: >
  浏览器自动化 / 网页爬虫 / 自动化脚本 / web scraping / browser automation。自动填表、数据抓取、网页截图、自动化测试一站式解决。适配电商运营的比价监控、市场部的竞品跟踪、数据分析师的批量采集、技术团队的UI自动化测试。用户常搜：怎样自动爬取网页数据、批量填充表单、网页自动化测试工具、Puppeteer怎么用、如何监控竞品价格。
tags: [浏览器自动化, 网页爬虫, 数据抓取, web-scraping, 自动化脚本, 自动化测试, Puppeteer, Playwright, 竞品监控, 运营效率]
---

# 浏览器自动化

自动化控制浏览器完成网页导航、元素交互、数据提取、截图等操作，适用于爬虫采集、自动化测试和批量工作流。

## Tools Required
- browser_navigate
- browser_click
- browser_type
- browser_screenshot

## Usage
- "帮我抓取京东上这个商品类目下所有商品的名称、价格和链接"
- "自动登录后台系统，截图保存每日销售报表页面"
- "批量填写表单并提交，模拟用户操作流程做自动化测试"

## Examples
输入：抓取某电商平台前50条商品信息，包括商品名、价格、评论数
输出：
```json
[
  {"name": "iPhone 15 Pro 256G", "price": "7999", "reviews": "12843"},
  {"name": "华为Mate60 Pro", "price": "6999", "reviews": "9521"},
  ...
]
```

输入：每天早上9点自动截图公司数据看板并保存
输出：执行截图脚本，保存为 `dashboard_20240115_0900.png`，并输出操作日志确认成功