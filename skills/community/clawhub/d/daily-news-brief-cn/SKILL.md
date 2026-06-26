---
name: daily-news-brief
description: 每日新闻简报，自动抓取热点新闻并 AI 提炼重点。支持财经/科技/国际新闻，定时推送。
author: 小爪 AI
version: 1.0.0
metadata: {"clawdbot":{"emoji":"📰","requires":{"bins":["python3","uv"]}}}
---

# 每日新闻简报技能

自动抓取当日热点新闻，AI 提炼重点，定时推送到你的 QQ/微信/Telegram。

## 功能特点

- 📰 **多源抓取**: 知乎/微博/财经网站/科技媒体
- 🤖 **AI 提炼**: 不是简单聚合，而是智能总结重点
- ⏰ **定时推送**: 早 8 点/晚 8 点，可自定义
- 🎯 **行业定制**: 交易员→财经优先，开发者→科技优先

## 快速开始

### 1. 安装技能

```bash
clawdhub install daily-news-brief
```

### 2. 配置新闻源

编辑 `config/sources.json`:

```json
{
  "categories": ["财经", "科技", "国际"],
  "sources": {
    "财经": ["财新", "华尔街见闻", "金十数据"],
    "科技": ["36 氪", "虎嗅", "Product Hunt"],
    "国际": ["Reuters", "BBC", "联合早报"]
  }
}
```

### 3. 设置推送时间

编辑 `config/schedule.json`:

```json
{
  "morning": "08:00",
  "evening": "20:00",
  "timezone": "Asia/Shanghai"
}
```

### 4. 启用定时任务

```bash
# 手动测试
uv run scripts/fetch_news.py --test

# 启用定时推送
openclaw cron add daily-news-brief --time "08:00,20:00"
```

## 输出示例

```
📰 每日新闻简报 - 2026 年 3 月 24 日

【财经】
1. 国内油价今晚 24 时大幅上调，92 号汽油进入"9 元时代"
   - 中东局势紧张，国际原油突破 100 美元/桶
   - 加满一箱油多花 86 元

2. 李强出席中国发展高层论坛 2026 年年会
   - 聚焦经济合作与创新发展

【科技】
1. OpenAI 发布 GPT-5，推理能力提升 300%
   - 支持多模态实时交互
   - 订阅价格不变

【国际】
1. 美联储维持利率不变，暗示 5 月可能降息
   - 通胀数据持续放缓
   - 美股应声上涨

---
💡 简报由 AI 提炼，全文阅读请访问来源链接
```

## 自定义

### 添加新闻源

在 `config/sources.json` 中添加:

```json
{
  "custom_sources": [
    {
      "name": "我的博客",
      "url": "https://example.com/feed",
      "category": "科技"
    }
  ]
}
```

### 修改输出模板

编辑 `templates/brief.md`，自定义格式。

### 推送渠道

支持 QQ/微信/Telegram/Discord 等，通过 OpenClaw 自动路由。

## 常见问题

**Q: 可以只推送财经新闻吗？**
A: 可以！在 `config/sources.json` 中只保留"财经"分类。

**Q: 能推送多次吗？**
A: 可以！修改 `config/schedule.json`，添加更多时间点。

**Q: 新闻源可以自定义吗？**
A: 可以！支持 RSS/网站/API 多种方式。

## 技术细节

- 使用 SearXNG 隐私搜索
- 新闻抓取用 BeautifulSoup/Playwright
- AI 总结用 OpenClaw 内置模型
- 定时任务用 OpenClaw cron

## 更新日志

### v1.0.0 (2026-03-24)
- 首次发布
- 支持多源新闻抓取
- AI 智能总结
- 定时推送

## 许可证

MIT License

## 反馈

遇到问题或有建议？GitHub 提 Issue 或联系作者。
