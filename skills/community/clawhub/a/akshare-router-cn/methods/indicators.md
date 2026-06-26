# Methods: indicators (MVP)

目标：给期货 5m/30m 级别 K 线在 **AKShare 原始数据之上** 做二次加工。

## 输入
- DataFrame：来自 `ak.futures_zh_minute_sina(symbol=<contract>, period=<1|5|15|30|60>)`
- 要求至少包含：时间戳 + OHLC(或 close) + volume
  - TODO：确认 AKShare 返回列名（不同品种/时期可能不同），实现时用“列名猜测+fallback”。

## 输出（建议）
在原 df 上新增列：
- `ma_5`, `ma_10`, `ma_20`
- `ema_12`, `ema_26`
- `macd`, `macd_signal`, `macd_hist`
- `rsi_14`

## 计算（解释性）
- MA：rolling mean
- EMA：ewm(span=, adjust=False).mean()
- MACD：
  - macd_line = ema12 - ema26
  - signal = EMA(macd_line, span=9)
  - hist = macd_line - signal
- RSI(14)：用 close 的涨跌幅，经典 Wilder 平滑或简单 rolling 皆可；MVP 可用简单版本。

## 风险与注意
- 分钟数据可能缺失/不连续（夜盘/休市），指标窗口需在缺失处自然 NaN。
- 5m/30m：优先直接调用 AKShare period=5/30；
  - 若用户给的是 1m 但要 5m：再做 resample（见 `methods/resample.md`）。
