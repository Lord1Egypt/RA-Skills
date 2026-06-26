# 事实核验规范

## 事实记录格式

每条关键事实必须先形成标准化记录，再写入正文：

```json
{
  "claim": "美国3月CPI同比上涨3.2%",
  "exact_value": "3.2%",
  "as_of": "2026-03-13",
  "source_url": "https://www.bls.gov/news.release/cpi.nr0.htm",
  "source_name": "U.S. Bureau of Labor Statistics",
  "publish_time": "2026-03-13T08:30:00-04:00",
  "data_type": "同比, 季调",
  "verified": true,
  "cross_check_source": "https://www.reuters.com/markets/us/..."
}
```

## 核验规则

### 必须交叉核验的数据（至少 2 个独立来源）

- 主要股指收盘点位及涨跌幅
- 美元指数 (DXY)
- 主要汇率（USD/CNY, EUR/USD, USD/JPY）
- 美债收益率（2Y, 10Y, 30Y）
- 原油价格（WTI, Brent）
- 黄金价格
- 关键宏观数据（CPI, GDP, 非农等）

### 来源优先级

1. **官方**：政府机构、央行、统计局原始发布页
2. **监管/交易所**：证监会、交易所官方数据
3. **权威通讯社/媒体**：Reuters, Bloomberg, AP
4. **财经媒体**：CNBC, 财联社, 华尔街见闻
5. **数据聚合站**：Investing.com, Yahoo Finance, 东方财富

### 冲突处理

- 不同来源数字冲突时，按上述优先级取值
- **禁止**自行取中间值或平均值
- 必须注明口径差异：收盘价/盘中价、同比/环比、初值/终值、季调/非季调

### 禁止事项

- 禁止使用无主体判断："市场普遍认为""分析人士指出"
- 禁止只写站点名不附 URL
- 禁止段尾堆叠来源冒充覆盖整段
- 禁止将未核验数据（`verified=false`）写入正文
- 禁止在"明日前瞻"中写无法确认的推测性事项

## evidence_map.json 格式

最终日报必须同步输出此文件，逐条映射正文事实与来源：

```json
{
  "report_date": "2026-03-14",
  "generated_at": "2026-03-14T08:00:00+08:00",
  "facts": [
    {
      "module": "核心股市表现",
      "claim": "标普500指数收于5,234.18点，涨0.57%",
      "exact_value": "5234.18 / +0.57%",
      "as_of": "2026-03-13",
      "source_url": "https://www.google.com/finance/quote/.INX:INDEXSP",
      "source_name": "Google Finance",
      "publish_time": "2026-03-13T16:00:00-04:00",
      "verified": true,
      "cross_check_url": "https://finance.yahoo.com/quote/%5EGSPC/"
    }
  ]
}
```
