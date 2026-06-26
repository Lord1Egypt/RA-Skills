---
name: Content Auto Poster
slug: content-auto-poster-xiaomolongxia
version: 1.0.0
description: "自动发布内容到多个平台，支持微信公众号、微博、知乎等平台定时发布。"
changelog: "1.0.0 - 初始版本"
metadata: {"openclaw":{"emoji":"📝","os":["win32","darwin","linux"]}}
---

# Content Auto Poster 📝

自动将一篇内容发布到多个平台，省时省力。

## 功能

- 📱 **多平台支持**: 微信公众号、微博、知乎、简书
- ⏰ **定时发布**: 设置最佳发布时间
- 📊 **数据统计**: 阅读量、点赞、评论汇总
- 🔄 **内容适配**: 自动调整格式适配各平台

## 输入

- 内容标题
- 正文内容
- 目标平台列表
- 发布时间（可选）

## 输出

```json
{
  "success": true,
  "posts": [
    {"platform": "wechat", "url": "https://...", "status": "published"},
    {"platform": "zhihu", "url": "https://...", "status": "scheduled"}
  ],
  "total_reach": 1250
}
```

## 使用场景

- 博客同步到多个平台
- 产品发布公告
- 定期内容更新

## 配置

```json
{
  "platforms": ["wechat", "zhihu", "jianshu"],
  "default_schedule": "09:00",
  "timezone": "Asia/Shanghai"
}
```

## 价格

¥49/月