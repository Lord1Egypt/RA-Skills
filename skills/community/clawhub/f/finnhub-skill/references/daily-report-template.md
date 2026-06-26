# Daily Stock News Report Template

Use this template when the user asks for a daily report on a stock such as TSLA, AAPL, NVDA, etc.

## Output Structure

### 标的
- Ticker

### 日期
- Report date

### 一、今日核心结论
- 总体情绪：偏空 / 中性偏空 / 中性 / 偏多 / 强多
- 一句话判断：概括当日最重要市场叙事

### 二、价格与交易概览
- 昨收 / 当前价 / 涨跌额 / 涨跌幅（优先用 quote）
- 日内高低点
- 开盘价 / 前收盘价
- **如果 candles/volume 可得：**
  - 成交量
  - 与前一交易日相比是放量/缩量
  - 价格与成交量关系（上涨放量 / 下跌放量 / 上涨缩量 / 下跌缩量）
- **如果 candles/volume 不可得：**
  - 明确说明：当前 Finnhub 计划未开放 candles/volume，以下仅基于 quote 与新闻判断

### 三、最重要的 3 条新闻
对每条新闻都给出：
- 标题
- 来源
- 内容摘要
- 影响方向：偏空 / 中性 / 偏多
- 影响强度：高 / 中 / 低
- 原因

### 四、市场主线拆解
按三个层级拆：
1. 公司基本面主线
2. 行业竞争/行业景气主线
3. 宏观环境主线

### 五、对股价的潜在影响
- 短期（1-3天）
- 中期（1-4周）
- 长期（1-2季度）

### 六、交易员视角
- 今天市场真正关心什么
- 哪个变量最可能决定下一步行情
- 如果新闻和价格出现背离，如何解释

### 七、最终判断
- 评级：偏空 / 中性 / 偏多
- 核心理由（3条）
- 一句话总结

## Writing Rules

1. Start with **price action first**, then news.
2. Separate **facts** from **interpretation**.
3. Never fabricate volume, candle, or historical comparison data.
4. If only quote + news are available, say so explicitly.
5. Prefer 3-5 most relevant news items, not a long dump.
6. Keep the final output concise enough to be readable in chat.

## Data Source Mapping

- Quote section → `/quote`
- News section → `/company-news` or `/news`
- Price/volume trend section → `/stock/candle` if available

## Fallback Logic

If `/stock/candle` returns permission denied or plan restriction:
- still produce the report
- include quote-based price summary
- omit volume comparison
- add a short note that candle/volume data is unavailable under current Finnhub access
