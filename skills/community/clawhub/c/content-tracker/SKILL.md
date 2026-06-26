---
name: content-tracker
version: 1.0.0
description: |
  内容追踪技能。高时效性话题追踪、链接更新监控、第三方热点聚合。
  
  USE FOR:
  - "追踪AI行业动态", "追踪某某话题最新进展"
  - "监控这个链接的更新", "这个网站有新内容吗"
  - "今天的热点", "最新新闻"
  - 定期简报生成（配合日程使用）

author: changsheng0804
license: MIT
homepage: https://github.com/changsheng0804/workbuddy-skills
tags: [tracking, news, content, monitoring, automation]

metadata:
  openclaw:
    emoji: 📡
    requires:
      bins: ["bash", "python3"]
      skills: ["topic_tracking"]

---

# 内容追踪技能

高时效性内容追踪工具，支持话题搜索、链接监控、热点聚合。

## 核心能力

### 1. 话题追踪
- 智能搜索接口，过滤高时效性内容
- 按事件主体去重，避免重复推送
- 支持首次/非首次执行模式

### 2. 链接追踪
- 监控指定URL的内容更新
- 自动识别新增内容
- 生成更新简报

### 3. 第三方数据源
- 微博热搜 (weibo_hot)
- 36氪 (thirty_six_kr)
- 腾讯新闻 (tencent_news)
- 华尔街见闻 (wallstreet_cn)
- 每日热点汇总 (daily_report)

## 使用场景

✅ **适用**：
- 行业动态追踪（AI、金融、科技等）
- 竞品/新闻监控
- 定期简报生成
- 链接更新通知

❌ **不适用**：
- 需要登录的内容
- 动态JS渲染的页面
- 视频为主的页面

## 输出格式

所有追踪结果保存为 Markdown 简报：
```
./我的追踪/{yyyy_mm_dd}/{话题名称}.md
```

简报内容：
- 来源标题（引用链接）
- 核心内容总结
- 时效性标注

## 快速开始

```
用户：追踪一下AI Agent行业的最新动态
AI：[执行话题追踪] → 生成简报 → 返回链接
```

## 配合日程使用

可创建重复日程，自动定期追踪：

| 场景 | 频率 | 建议 |
|------|------|------|
| 行业动态 | 每日 | 下午3点执行 |
| 热点追踪 | 每日 | 早晚各一次 |
| 链接监控 | 每周 | 周一执行 |

## 依赖

- 技能：topic_tracking（需预先安装）
- 环境：Python3 + requests

## 注意事项

- 首次执行使用 `--is-first-time true` 参数
- 无结果表示确实没有新内容，不会重复推送
- 内容来源于原文总结，不做推断或编造
