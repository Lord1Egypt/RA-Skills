---
name: daily-hot-aggregator
description: "🔥 一键获取全平台热榜！B站+抖音+微博+头条，一站搞定所有热点。自媒体运营必备！免费使用，定制开发请联系作者。"
homepage: https://github.com/openclaw/daily-hot-aggregator
metadata:
  {
    "openclaw":
      {
        "emoji": "🔥",
        "requires": { "bins": ["python3"] },
      },
  }
---

# 🔥 全平台热榜聚合 v7.0

一个技能搞定所有平台热榜！B站 + 抖音 + 微博 + 头条

## ✨ v7.0 新功能

- ✅ **企微群推送** - 自动推送热榜到企微群
- ✅ **热点预警** - 新上榜、高热度话题实时预警
- ✅ **选题推荐** - AI推荐各平台创作选题
- ✅ **数据分析** - 数据对比、热词提取、HTML报告
- ✅ **定时任务** - 每日自动收集、推送、分析

## 📦 安装

```bash
npx clawhub@latest install daily-hot-aggregator
```

## 🚀 使用

### 数据收集
```bash
# 获取所有平台 Top 5
python3 fetch_all.py --top 5

# 获取指定平台
python3 fetch_all.py --bilibili --top 10
python3 fetch_all.py --douyin --top 10
python3 fetch_all.py --weibo --top 10
python3 fetch_all.py --toutiao --top 10

# 生成摘要
python3 fetch_all.py --summary --output daily_report.json
```

### 数据分析
```bash
# 生成HTML美化报告
python3 analyzer.py --date 2026-03-29 --html

# 提取热词
python3 analyzer.py --date 2026-03-29 --keywords

# 与前一天对比
python3 analyzer.py --date 2026-03-29 --compare
```

### 热点预警
```bash
# 运行预警检测
python3 hot_alert.py --date 2026-03-29

# 添加监控关键词
python3 hot_alert.py --add-keyword "周杰伦"

# 查看所有关键词
python3 hot_alert.py --list-keywords
```

### 选题推荐
```bash
# 单平台推荐
python3 content_recommender.py --platform douyin --top 3

# 全平台推荐
python3 content_recommender.py --date 2026-03-29
```

### 企微推送
```bash
# 添加推送群（webhook方式）
# 1. 在企微群添加群机器人，获取webhook地址
# 2. 编辑 wechat_push_config.json 添加配置

# 查看所有群
python3 wechat_push.py --list-groups

# 测试推送
python3 wechat_push.py --test "群ID"
```

**Webhook 配置示例** (`wechat_push_config.json`)：
```json
{
  "groups": [
    {
      "group_id": "数智天团",
      "group_name": "数智天团",
      "webhook": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY",
      "platforms": ["bilibili", "douyin", "weibo", "toutiao"],
      "enabled": true
    }
  ]
}
```

## ⏰ 定时任务配置

使用 OpenClaw cron 功能设置自动收集：

### 每日热榜收集（每天 9:00）
```
任务名：🔥 每日热榜收集
时间：每天 09:00
功能：自动收集四平台热榜数据并保存
```

### 小红书热榜收集（每天 9:30）
```
任务名：📕 小红书热榜收集
时间：每天 09:30
功能：使用浏览器获取小红书真实数据
```

### 每周趋势分析（每周一 10:00）
```
任务名：📊 每周热榜趋势分析
时间：每周一 10:00
功能：分析本周热点趋势，生成周报
```

### HTML美化报告（每天 12:00）
```
任务名：📈 生成热榜美化报告
时间：每天 12:00
功能：生成HTML可视化报告，提取热词
```

### 每日选题推荐（每天 12:30）
```
任务名：💡 每日选题推荐
时间：每天 12:30
功能：为各平台推荐创作选题
```

### 热点预警检测（每天 4次）
```
任务名：🔔 热点预警检测
时间：每天 10:00, 14:00, 18:00, 22:00
功能：检测新上榜、高热度话题并预警
```

## 📁 数据存储

数据自动保存到 `hot_reports/` 目录：

```
hot_reports/
├── daily_report_2026-03-29.json      # 四平台热榜数据
├── daily_report_2026-03-30.json
├── xiaohongshu_report_2026-03-29.json # 小红书热榜
├── weekly_summary_2026-03-29.json     # 每周趋势报告
└── report_2026-03-29.html             # HTML美化报告
```

## 📊 支持平台

| 平台 | 状态 | 数据内容 |
|------|------|---------|
| B站 | ✅ 正常 | 热门视频排行榜 |
| 抖音 | ✅ 正常 | 热搜榜 |
| 微博 | ✅ 正常 | 热搜榜 |
| 今日头条 | ✅ 正常 | 热点新闻 |

## 💰 定制服务

**免费使用本技能，如需以下服务请联系作者：**

- 🔧 **定制开发**：多平台数据聚合方案
- 📊 **数据分析**：跨平台热点趋势分析
- 🤖 **自动化部署**：完整的数据监控系统
- 📱 **系统集成**：对接企业内部系统

**联系方式：**
- 📱 QQ：2595075878
- 📧 邮箱：2595075878@qq.com

## ⚖️ 免责声明

本技能所获取的数据来自各平台公开API，仅用于个人学习和技术研究目的。

- 📌 **数据来源**：B站、抖音、微博、今日头条公开API接口
- 📌 **非商业性质**：本技能为开源免费工具，不涉及任何商业引导
- 📌 **版权说明**：所有数据内容的版权归各平台所有
- 📌 **使用限制**：请遵守各平台用户协议，禁止用于非法用途
- 📌 **免责条款**：本技能按"现状"提供，使用者需自行承担使用风险

## 📄 许可证

MIT License
