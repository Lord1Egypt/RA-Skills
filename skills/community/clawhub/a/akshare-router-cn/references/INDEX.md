# References Index (AKShare) — akshare-router-cn

本索引用于**快速定位**一期 MVP 需要的 AKShare 接口。字段/列名会随上游页面变化，依赖 recipe 的“容错处理”。

## 期货（Futures）

### 实时/盘面
- `ak.futures_zh_realtime(symbol: str='PTA') -> DataFrame`
  - 说明：某品种当前时刻所有可交易合约实时数据（Sina）
  - `symbol` 可由 `ak.futures_symbol_mark()` 查。

### 分钟线（1/5/15/30/60m）
- `ak.futures_zh_minute_sina(symbol: str='IF2008', period: str='1') -> DataFrame`
  - `period` ∈ {"1","5","15","30","60"}

### 日线/历史（备选源）
- `ak.futures_hist_em(symbol: str='热卷主连', period: str='daily', start_date='19900101', end_date='20500101') -> DataFrame`
  - period ∈ {daily, weekly, monthly}
  - TODO：统一“symbol 命名”到内部字典（东方财富主连命名 vs 合约名）。

## 期权（Options）— 上交所 ETF 期权（Sina）

### 到期月份列表
- `ak.option_sse_list_sina(symbol: str='50ETF') -> List[str]`
  - 返回类似 ["202603","202604",...]

### 合约代码列表
- `ak.option_sse_codes_sina(symbol: str='看涨期权', trade_date: str='202603', underlying: str='510050') -> DataFrame`
  - 输出含 `期权代码`（Sina 内码，例如 10009633），后续用于 spot/greeks 接口。

### 单合约实时价
- `ak.option_sse_spot_price_sina(symbol: str='10003720') -> DataFrame`

### 单合约 Greeks + IV
- `ak.option_sse_greeks_sina(symbol: str='10003045') -> DataFrame`
  - 实测返回两列：`字段`,`值`
  - 典型字段：Delta/Gamma/Theta/Vega/隐含波动率/最新价/行权价/理论价值...

### 分钟线（仅当日）
- `ak.option_sse_minute_sina(symbol: str='10003720') -> DataFrame`
  - 限制：只能取当前交易日

## 期权（Options）— 全市场行情（东方财富）
- `ak.option_current_em() -> DataFrame`
  - TODO：字段梳理 + 与 Sina 内码/交易代码的关联策略。

---

## 二次加工（自研方法，见 methods/）
- RR25：`methods/rr25.md`
- 指标计算：`methods/indicators.md`

> 原则：只要 AKShare 直接返回就不用算；否则用 methods 中的“可解释计算”。
