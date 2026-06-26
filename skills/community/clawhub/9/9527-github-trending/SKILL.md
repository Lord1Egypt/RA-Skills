---
name: 9527-github-trending
description: 每日自动获取 GitHub Trending 热门项目，推送通知。支持自定义语言、时间范围、推送渠道（Telegram/钉钉/企业微信）。零成本运行。
version: 1.0.0
author: 9527
license: MIT
---

# GitHub Trending 每日推送

自动获取 GitHub Trending 热门项目，推送到你的通知渠道。

## 功能

- 每日自动获取 GitHub Trending
- 支持过滤编程语言
- 支持多种推送渠道（Telegram、钉钉、企业微信）
- 零成本运行
- 可设置为 Cron 定时任务

## 快速开始

```bash
# 获取今日热门项目
python3 trending.py

# 只看 Python 项目
python3 trending.py --language python

# 推送到 Telegram
python3 trending.py --telegram --token YOUR_BOT_TOKEN --chat_id YOUR_CHAT_ID

# 推送到钉钉
python3 trending.py --dingtalk --webhook YOUR_WEBHOOK_URL
```

## Cron 定时任务

```bash
# 每天 9:00 推送
0 9 * * * python3 /path/to/trending.py --telegram --token xxx --chat_id xxx
```

## 收入模式

1. 上架 ClawHub 免费分享
2. 提供定制服务（付费）
3. 接受 GitHub Sponsors
