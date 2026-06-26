---
name: chinese-tech-news
description: 采集钛媒体、虎嗅、36氪、爱范儿四大中文科技媒体的最新资讯，整理成带原文链接的快讯。无需 API Key，直接抓取 RSS 源。
metadata:
  openclaw:
    emoji: "📱"
    requires:
      bins: ["node"]
    tags: ["chinese", "news", "tech", "tmtpost", "huxiu", "36kr", "ifanr"]
---

# 中文科技资讯抓取

> 版权：© Shanqiu Technology

从四大中文科技媒体（钛媒体、虎嗅、36氪、爱范儿）抓取最新资讯，通过 RSS 源获取，无需 API Key。

## 数据源

| 媒体 | RSS 地址 | 每次取 |
|------|----------|--------|
| 钛媒体 | https://www.tmtpost.com/rss | 20条 |
| 虎嗅 | https://www.huxiu.com/rss/0.xml | 10条 |
| 36氪 | https://36kr.com/feed | 30条 |
| 爱范儿 | https://www.ifanr.com/feed | 20条 |

## 执行方式

```bash
cd skills/chinese-tech-news && node fetch.js
```

## 输出格式

每条包含：
- 序号
- 来源媒体（钛媒体/虎嗅/36氪/爱范儿）
- 标题
- 原文链接

默认输出约 20 条，按抓取顺序排列。

## 技术细节

- 纯 Node.js，无外部依赖
- 支持重定向跟随（支持短链 RSS）
- 支持 `<![CDATA[...]]` 包裹的 link 字段（36氪格式）
- 自动过滤图片类无效链接

## 更新日志

### v1.0.0
- 首发版本，支持四大中文科技媒体 RSS 抓取
- 无需 API Key，纯 RSS 源获取
- 支持标题和原文链接提取
