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

# 🔥 全平台热榜聚合 v4.0

一个技能搞定所有平台热榜！B站 + 抖音 + 微博 + 头条

## ✨ v4.0 新功能

- ✅ 新增抖音热搜支持
- ✅ 新增今日头条热榜支持
- ✅ 优化数据结构
- ✅ 改善可视化报告

## 📦 安装

```bash
npx clawhub@latest install daily-hot-aggregator
```

## 🚀 使用

```bash
# 获取所有平台 Top 5
python3 fetch_all.py --top 5

# 获取指定平台
python3 fetch_all.py --bilibili --top 10
python3 fetch_all.py --douyin --top 10

# 生成摘要
python3 fetch_all.py --summary --output daily_report.json
```

## 📊 支持平台

| 平台 | 状态 | 数据内容 |
|------|------|---------|
| B站 | ✅ 正常 | 热门视频排行榜 |
| 抖音 | ✅ 正常 | 热搜榜 |
| 今日头条 | ⚠️ 部分 | 热点新闻 |
| 微博 | ❌ 需Cookie | 热搜榜 |
| 知乎 | ❌ 需授权 | 热榜 |

## 💰 定制服务

**免费使用本技能，如需以下服务请联系作者：**

- 🔧 **定制开发**：多平台数据聚合方案
- 📊 **数据分析**：跨平台热点趋势分析
- 🤖 **自动化部署**：完整的数据监控系统
- 📱 **系统集成**：对接企业内部系统

**联系方式：**
- 📱 QQ：2595075878
- 📧 邮箱：2595075878@qq.com

## 📄 许可证

MIT License
