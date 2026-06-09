---
name: "Douban Bookmark"
description: "输入图书名称，把它加入豆瓣读书的「想读」收藏。适用于“把《xxx》加入豆瓣想读 / 愿望清单 / 想读列表”这类请求。实现方式：先用 HTTP 解析豆瓣搜索结果拿到最优图书详情页，再用 Playwright 持久化浏览器登录态打开详情页，执行豆瓣真实的两段式收藏流程（点“想读”→ 点“保存”）。首次登录后可长期复..."
category: "other"
source: "ClawHub"
tags: [bookmark, books, douban, playwright]
platforms: []
author: ""
version: ""
license: ""
installCmd: "hermes skills install clawhub/douban-bookmark"
sourceUrl: "https://clawhub.ai/skills/douban-bookmark"
---

# Douban Bookmark

> 输入图书名称，把它加入豆瓣读书的「想读」收藏。适用于“把《xxx》加入豆瓣想读 / 愿望清单 / 想读列表”这类请求。实现方式：先用 HTTP 解析豆瓣搜索结果拿到最优图书详情页，再用 Playwright 持久化浏览器登录态打开详情页，执行豆瓣真实的两段式收藏流程（点“想读”→ 点“保存”）。首次登录后可长期复...

- **Category:** Other
- **Source:** ClawHub
- **Author:** 
- **Version:** 
- **License:** 
- **Platforms:** All
- **Install Command:** `hermes skills install clawhub/douban-bookmark`
- **Source URL:** [https://clawhub.ai/skills/douban-bookmark](https://clawhub.ai/skills/douban-bookmark)

## Overview


## Installation
To install this skill, run the following command in your terminal:
```bash
hermes skills install clawhub/douban-bookmark
```
