---
slug: cn-news-brief
name: 中文新闻简报
version: "1.0.0"
author: 千策
---

# 📰 CN News Brief — 中文新闻简报

3分钟了解天下事。

## 核心功能

| 功能 | 说明 |
|------|------|
| 每日简报 | 国内+国际+科技+财经，分类呈现 |
| AI摘要 | 每条新闻一句话总结 |
| 多源聚合 | 央视/新华网/澎湃/36氪/虎嗅 |
| 情绪标注 | 正面/负面/中性，快速判断基调 |

## 使用方式

```bash
# 今日简报
python3 scripts/news_brief.py --today

# 指定分类
python3 scripts/news_brief.py --category 科技

# 输出JSON
python3 scripts/news_brief.py --today --json

# 指定条数
python3 scripts/news_brief.py --today --limit 5
```

## 示例输出

```
📰 今日新闻简报（4月13日）
━━━━━━━━━━━━━━━━━━━━━━

🇨🇳 国内
  1. 🔵 多所高校强基计划取消竞赛破格（新华网）
  2. 🔵 24岁主播直播晕倒被辞退，已申请仲裁（澎湃）

🌍 国际
  3. 🔴 美国3月CPI创两年最大涨幅（路透社）

💻 科技
  4. 🟢 OpenClaw发布新版智能体框架（36氪）
  5. 🔵 华为自研芯片良率突破（虎嗅）

💰 财经
  6. 🔴 伊朗资产解冻引发市场波动（财联社）
```

## 数据源

| 来源 | 类型 | 更新频率 |
|------|------|---------|
| 百度热搜 | 综合 | 实时 |
| 微博热搜 | 社交 | 实时 |
| 36氪 | 科技 | 每日 |
| 虎嗅 | 科技商业 | 每日 |
| 澎湃新闻 | 综合 | 实时 |

本地运行，无需API Key。

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
