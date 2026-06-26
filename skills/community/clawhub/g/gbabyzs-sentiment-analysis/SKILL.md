# Sentiment Analysis - 情绪分析工具

## 功能说明

分析股票相关社交媒体情绪，包括股吧、雪球评论。

## 核心功能

### 情绪指标
- 情绪指数 (0-100)
- 看涨/看跌比例
- 情绪趋势变化

### 热度分析
- 讨论热度
- 关注度变化
- 舆情传播路径

### 水军识别
- 异常评论检测
- 机器人账号识别
- 真实情绪过滤

## 使用示例

```python
from sentiment_analysis import analyze_stock_sentiment

# 分析情绪
sentiment = analyze_stock_sentiment(stock_code="300308")
```

## 安装依赖

```bash
pip install akshare pandas numpy jieba snownlp
```
