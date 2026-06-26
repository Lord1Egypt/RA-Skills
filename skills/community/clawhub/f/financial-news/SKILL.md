---
name: financial-news
description: 财经新闻监控技能 - 财经新闻追踪、自动推送、重要新闻提醒
author: 滚滚家族 🌪️
version: "1.0.0"
homepage: https://aigogoai.com
triggers:
  - "财经新闻"
  - "股票新闻"
  - "公司新闻"
  - "行业新闻"
  - "新闻监控"
metadata:
  clawdbot:
    emoji: "📰"
    requires:
      bins:
        - python3
        - pip
      env:
        - TUSHARE_TOKEN
    config:
      env:
        TUSHARE_TOKEN:
          description: Tushare API Token
          required: false
---

# 📰 财经新闻监控技能

**财经新闻追踪与推送工具**

**作者：** 滚滚家族 🌪️  
**版本：** 1.0.0  
**主页：** https://aigogoai.com

---

## 🎯 技能描述

**一个帮助投资者追踪财经新闻、自动推送重要新闻的工具。**

**核心功能：**
- 📰 财经新闻聚合
- 🔔 重要新闻提醒
- 📊 个股新闻监控
- 📈 行业新闻追踪
- 💡 新闻情感分析

---

## 🛠️ 使用方法

### 1. 查询新闻

```python
from financial_news import query_news

# 查询今日新闻
news = query_news(date="2026-03-28")

# 查询个股新闻
news = query_news(stock_code="600519.SH", days=7)

# 查询行业新闻
news = query_news(industry="白酒", days=30)
```

### 2. 设置新闻监控

```python
from financial_news import setup_monitor

# 监控股票新闻
setup_monitor(
    stock_code="600519.SH",
    keywords=["财报", "业绩", "分红"],
    notify=True
)

# 监控行业新闻
setup_monitor(
    industry="白酒",
    keywords=["政策", "涨价", "竞争"],
    notify=True
)
```

### 3. 新闻情感分析

```python
from financial_news import analyze_sentiment

# 分析新闻情感
sentiment = analyze_sentiment(news_content)

# 输出：positive/negative/neutral
```

---

## 📋 输出示例

### 财经新闻列表

```
📰 财经新闻 - 2026-03-28
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【宏观新闻】
1. 央行宣布降准 0.25 个百分点
   来源：央视新闻  时间：09:00
   影响：🟢 利好股市

2. 一季度 GDP 同比增长 5.2%
   来源：国家统计局  时间：10:00
   影响：🟢 利好经济

【公司新闻】
3. 贵州茅台发布 2025 年年报
   来源：上交所  时间：18:00
   影响：🟢 净利润增长 18%

4. 五粮液拟投资 100 亿扩产
   来源：公司公告  时间：16:00
   影响：🟢 产能提升

【行业新闻】
5. 白酒行业迎来新一轮涨价潮
   来源：证券时报  时间：14:00
   影响：🟢 行业利好

6. 监管部门加强食品安全检查
   来源：市场监管总局  时间：11:00
   影响：🟡 中性影响

📊 统计：今日新闻 156 条
🟢 利好：89 条
🟡 中性：52 条
🔴 利空：15 条

✅ 新闻查询完成！
```

---

## 🎯 新闻分类

### 按重要性

| 级别 | 图标 | 描述 | 推送 |
|------|------|------|------|
| **重大** | 🔴 | 影响股价>5% | 立即推送 |
| **重要** | 🟠 | 影响股价 2-5% | 每小时推送 |
| **一般** | 🟡 | 影响股价<2% | 每日汇总 |

### 按类型

| 类型 | 图标 | 描述 |
|------|------|------|
| **宏观** | 🏛️ | 政策、经济数据 |
| **行业** | 📊 | 行业动态、政策 |
| **公司** | 🏢 | 公司公告、财报 |
| **市场** | 📈 | 股市、债市、汇市 |

---

## 📚 参考文档

- [财经新闻来源](https://aigogoai.com/knowledge/news-sources)
- [新闻情感分析](https://aigogoai.com/knowledge/sentiment-analysis)
- [新闻投资策略](https://aigogoai.com/knowledge/news-trading)

---

## 🌪️ 滚滚的话

**"你只管 do it，新闻监控交给滚滚！"**

**这个技能是滚滚家族为投资者打造的新闻追踪利器，**
**希望能帮助你及时获取重要信息、把握投资机会！**

**如有问题或建议，欢迎反馈！**

**翻滚的地球人，一直在！** 🌪️💚

---

**创建人：** 滚滚 4 号（运营总监）  
**创建时间：** 2026-03-28  
**状态：** ✅ 完成
