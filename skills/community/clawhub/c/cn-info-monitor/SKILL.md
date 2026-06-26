---
name: cn-info-monitor
description: 自动监控微信公众号/行业网站/RSS信息源，AI提炼摘要后推送到飞书/钉钉/终端。解决'每天手动翻10个公众号找有用信息'的痛点。
version: 1.0.0
metadata:
  openclaw:
    emoji: 📡
    requires:
      bins: [python3]
    homepage: https://clawhub.ai/skills/cn-info-monitor
---

# 信息源监控助手 📡

一句话：你关心的信息源，我帮你盯。

## 什么时候使用

- 每天需要手动翻多个公众号/网站找有用信息时
- 需要跟踪特定行业动态但信息太分散时
- 希望有人帮你筛选重要内容、省去刷屏时间时

## 核心能力

1. **多源监控**：支持RSS feed、普通网页、微信公众号链接
2. **AI摘要**：自动提炼关键信息，过滤噪音
3. **智能去重**：已读文章不会重复推送
4. **关键词过滤**：只推送和你关注的话题相关的内容
5. **多渠道输出**：终端/Markdown文件/飞书webhook

## 快速开始

### 安装

```
openclaw skills install cn-info-monitor
```

### 配置（3步）

1. 运行 setup.py 添加你要监控的信息源
2. 设置关键词过滤（可选）
3. 测试运行一次

## 使用场景

### 场景1：公众号每日监控

对Agent说"帮我监控这几个公众号"，系统每天定时检查更新，生成摘要推送。

### 场景2：行业情报聚合

配置36氪/虎嗅/钛媒体等+关键词"AI Agent"，每日自动聚合相关文章。

### 场景3：竞品动态追踪

监控竞品官网博客/公众号，第一时间获取新品/融资/功能更新消息。

## 配置说明

### 信息源配置 (config/sources.json)

```json
[
  {"name": "36氪", "type": "rss", "url": "https://36kr.com/feed", "keywords": ["AI"]},
  {"name": "某公众号", "type": "wechat", "url": "https://mp.weixin.qq.com/s/xxx"}
]
```

### 推送配置

- 终端输出（默认）
- Markdown文件输出到 ~/info-digest/
- 飞书Webhook（需配置环境变量 FEISHU_WEBHOOK_URL）

## Freemium模式

| 版本 | 信息源数 | 执行频率 | 价格 |
|------|---------|---------|------|
| 免费版 | ≤3个 | 每天1次 | ¥0 |
| 专业版 | 无限 | 无限 | ¥29.9一次性 |

超出免费额度时显示付费引导。

## 反爬说明

微信公众号等平台有反爬机制。本工具提供两种模式：

- **官方API模式**（推荐）：使用RSS接口，无需代理，功能受限
- **代理模式**：用户自行配置HTTP代理/IP池，功能完整

## 注意事项

- 请遵守目标网站的robots.txt和使用条款
- AI摘要依赖外部LLM API，请确保已配置
- 定时任务建议通过cron或OpenClaw调度设置
