# Recipe: options_iv_greeks (IV + Greeks)

## 适用问题
- “50ETF 当月某个合约的隐含波动率和 Delta/Gamma”
- “给我最活跃的几档期权 Greeks/IV”

## 数据源
- `ak.option_sse_list_sina(symbol='50ETF'|'300ETF')`：到期月份列表
- `ak.option_sse_codes_sina(symbol='看涨期权'|'看跌期权', trade_date='YYYYMM', underlying='510050'|'510300')`：合约内码列表
- `ak.option_sse_greeks_sina(symbol=<内码>)`：单合约 IV+Greeks（key-value 表）

## 步骤（MVP）
1) 确认标的：默认 `510050`（50ETF），可让用户指定 300ETF。
2) 确认到期月份：
   - 用户未指定 → 用 `option_sse_list_sina` 取列表，默认取最近月。
3) 拉取看涨/看跌合约内码列表。
4) 选取若干合约（策略二选一）：
   - 以行权价接近 ATM 为主（需要先获得标的现价；可用 `option_sse_underlying_spot_price_sina`，TODO 验证列）
   - 或者简单取列表前 N 个（MVP）
5) 对每个内码调用 `option_sse_greeks_sina`，按 `methods/greeks.md` 归一化字段。
6) 输出：一张小表（合约简称/行权价/最新价/IV/Delta/Gamma/Theta/Vega/成交量）。

## 最小脚本
- `python3 skills/akshare-router-cn/scripts/options_iv_greeks.py --underlying 510050 --trade_date 202603 --n 10`

## 注意
- greeks 接口返回 key-value：要容错字段缺失。
- TODO：完善 ATM 选择逻辑与“最活跃合约”逻辑（基于成交量字段）。
