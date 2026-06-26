# Recipe: futures_kline_indicators (5m/30m + 指标)

## 适用问题
- “IF 主力 30 分钟 MACD/RSI”
- “给我 PTA 5 分钟 MA(5/10/20)”

## 数据源
- `ak.futures_zh_minute_sina(symbol=<合约>, period=<1|5|15|30|60>)`

## 步骤
1) 明确合约 `contract`：
   - 如果用户只说“IF/螺纹钢”，可先用 `recipes/futures_realtime_board.md` 找主力候选，再让用户确认。
2) period：
   - 用户明确 5m/30m → 直接用 period=5/30
   - 否则默认 5m（更贴近盘中需求）
3) 获取分钟数据 df
4) 调用 `methods/indicators.md` 计算指标
5) 输出：最近 N 根（默认 30）K 线的 close + 指标，并给出简短解读（例如 MACD 金叉/死叉、RSI 超买超卖）

## 最小脚本
- `python3 skills/akshare-router-cn/scripts/futures_indicators.py --contract IF2008 --period 30 --tail 60`

## 注意
- AKShare 的分钟数据列名不完全一致：脚本实现需做列名猜测（open/high/low/close 或者 中文列名）。
- TODO：加入交易时段过滤（夜盘/午休）。
