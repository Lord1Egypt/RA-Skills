---
name: a-share-analysis-enhanced
description: A 股全面分析工具（增强版），整合 Firecrawl 新闻情绪抓取、Elite Long-term Memory 历史分析、Coding Agent 代码优化。Use when user asks for: A 股股票分析、市场行情查询、技术指标分析、财务数据获取、投资建议、综合投资报告等 A 股相关分析需求。
---

# A 股分析技能（增强版）

## 🚀 新增功能

本增强版在原有基础上新增：

- 📰 **Firecrawl 新闻情绪** - 自动抓取财经新闻，AI 分析市场情绪
- 🧠 **Elite Memory 历史分析** - 存储和回顾历史分析记录，追踪投资决策
- 📝 **增强版报告生成** - 综合评分系统、一句话点评、目标价/止损价计算

## 快速开始

### 完整分析流程

```python
# 1. 获取实时行情
from scripts.fetch_realtime_data import AShareRealTimeFetcher
fetcher = AShareRealTimeFetcher()
stock_data = fetcher.fetch_stock_data("600519")

# 2. 技术分析
from scripts.fetch_technical_indicators import AShareTechnicalAnalyzer
analyzer = AShareTechnicalAnalyzer()
technical = analyzer.analyze_technical_indicators("0.600519")

# 3. 新闻情绪分析（新增）
from scripts.fetch_news_sentiment import AShareNewsSentimentAnalyzer
sentiment_analyzer = AShareNewsSentimentAnalyzer()
news_sentiment = sentiment_analyzer.analyze_stock_news("600519", "贵州茅台")

# 4. 获取历史分析（新增）
from scripts.memory_store import AShareMemoryStore
memory_store = AShareMemoryStore()
memory_history = memory_store.get_analysis_summary("600519")

# 5. 生成增强版报告（新增）
from scripts.generate_report_enhanced import AShareEnhancedReportGenerator
generator = AShareEnhancedReportGenerator()

analysis_data = {
    **stock_data,
    "technical": technical,
    "news_sentiment": news_sentiment,
    "memory_history": memory_history
}

report = generator.generate_enhanced_report(analysis_data)
filepath = generator.save_report(report, "600519", "贵州茅台")
```

## 新增脚本说明

### fetch_news_sentiment.py - 新闻情绪分析

使用 Firecrawl CLI 抓取财经新闻，分析市场情绪。

```python
from scripts.fetch_news_sentiment import AShareNewsSentimentAnalyzer

analyzer = AShareNewsSentimentAnalyzer()

# 分析个股新闻
result = analyzer.analyze_stock_news("600519", "贵州茅台")
# 返回：新闻数量、看多/看空/中性数量、情绪评分、总体情绪

# 分析大盘新闻
market_result = analyzer.analyze_market_news()
```

**返回数据结构**:
```python
{
    "stock_code": "600519",
    "stock_name": "贵州茅台",
    "news_count": 8,
    "bullish_count": 5,
    "bearish_count": 2,
    "neutral_count": 1,
    "avg_sentiment_score": 0.65,
    "overall_sentiment": "BULLISH",
    "news_items": [
        {
            "title": "贵州茅台业绩超预期",
            "sentiment_label": "BULLISH",
            "sentiment_score": 0.85,
            "url": "https://..."
        }
    ]
}
```

### memory_store.py - 记忆存储

使用 Elite Long-term Memory 系统存储分析历史。

```python
from scripts.memory_store import AShareMemoryStore

store = AShareMemoryStore()

# 存储分析记录
store.store_analysis({
    "stock_code": "600519",
    "stock_name": "贵州茅台",
    "price": 1800.50,
    "technical": {"signal": "bullish"},
    "sentiment": {"overall_sentiment": "BULLISH"},
    "recommendation": "买入",
    "key_points": ["均线多头排列", "MACD 金叉"],
    "importance": 0.85
})

# 获取历史摘要
summary = store.get_analysis_summary("600519")
```

**存储位置**:
- `memory/YYYY-MM-DD.md` - 每日分析日志
- `memory/a-share/{code}.json` - 股票专用历史
- `SESSION-STATE.md` - 活跃上下文
- `MEMORY.md` - 重要分析归档

### generate_report_enhanced.py - 增强版报告

生成包含综合评分、新闻情绪、历史回顾的专业报告。

**报告包含**:
1. 核心摘要（综合评分 0-10 分）
2. 实时行情
3. 技术分析（均线、MACD、RSI）
4. 基本面分析
5. 新闻情绪分析（Firecrawl 增强）
6. 历史分析回顾（Memory 增强）
7. 综合投资建议（含目标价/止损价）
8. 风险提示

**综合评分系统**:
- 8-10 分：🟢 强烈推荐
- 6-8 分：🟡 推荐
- 4-6 分：⚪ 观望
- 2-4 分：🟠 谨慎
- 0-2 分：🔴 回避

## 依赖要求

### Firecrawl（新闻情绪分析）
```bash
# 安装 Firecrawl CLI
npm install -g firecrawl-cli

# 登录认证
firecrawl login --browser

# 检查状态
firecrawl --status
```

### Elite Long-term Memory
已在 OpenClaw 中安装，需要配置：
```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "openai"
  },
  "plugins": {
    "entries": {
      "memory-lancedb": {
        "enabled": true
      }
    }
  }
}
```

## 使用示例

### 示例 1: 完整个股分析
```
老板，分析一下贵州茅台 (600519)
```

**执行流程**:
1. 获取实时行情
2. 计算技术指标
3. Firecrawl 抓取新闻并分析情绪
4. 查询历史分析记录
5. 生成增强版报告
6. 存储分析记录到 Memory

### 示例 2: 查看历史分析
```
查看贵州茅台的历史分析记录
```

**返回**:
- 分析次数
- 历史价格趋势
- 主要投资建议
- 平均情绪

### 示例 3: 市场概览
```
今天 A 股市场情绪如何
```

**执行**:
- Firecrawl 抓取大盘新闻
- 分析整体市场情绪
- 生成情绪报告

## 报告输出示例

```markdown
# 📊 贵州茅台 (600519) 深度分析报告

*生成时间：2026-03-01 10:30:00*

---

## 🎯 核心摘要

| 指标 | 数值 | 状态 |
|------|------|------|
| 当前价格 | ¥1800.50 | +0.87% |
| 技术信号 | bullish | 多头趋势 |
| 新闻情绪 | BULLISH | 评分：0.650 |
| 综合评分 | **7.5/10** | 🟡 推荐 |

**一句话点评**: 贵州茅台整体表现良好，可适度参与，注意仓位控制。

## 📈 实时行情
...

## 🔧 技术分析
...

## 📰 新闻情绪分析
...

## 🧠 历史分析回顾
...

## 💡 综合投资建议
🟡 **推荐** - 建议增持

**操作策略**: 适度参与，仓位控制在 5-6 成

**目标价位**: ¥1830.00
**止损价位**: ¥1726.60
```

## 注意事项

1. **Firecrawl 需要 API 密钥** - 首次使用需登录认证
2. **新闻情绪有延迟** - 基于已发布新闻，非实时
3. **历史分析需累积** - 首次使用无历史记录
4. **综合评分仅供参考** - 不构成投资建议
5. **投资有风险** - 请独立判断，谨慎决策

## 更新日志

- **2026-03-01**: 增强版发布
  - 新增 Firecrawl 新闻情绪分析
  - 新增 Elite Memory 历史分析存储
  - 新增综合评分系统
  - 优化报告生成器

---

*基于 OpenClaw + Firecrawl + Elite Long-term Memory 构建*
