# Methods: resample-kline (optional)

当数据源只给到 1m，而用户要 5m/30m 时使用。

## 输入
- 1m OHLCV DataFrame，必须有 datetime index 或可解析的时间列。

## 输出
- 目标周期 OHLCV：
  - open = first
  - high = max
  - low = min
  - close = last
  - volume = sum

## 注意
- 期货夜盘跨日：按交易日/自然日 resample 会有差异。
- MVP 默认按自然时间连续 resample；高级版可引入“交易时段日历”。

TODO：补充中国期货交易时段日历与跨日规则。
