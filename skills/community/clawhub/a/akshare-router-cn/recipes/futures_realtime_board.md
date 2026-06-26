# Recipe: futures_realtime_board

## 适用问题
- “PTA 现在盘面怎么样？”
- “螺纹钢各合约实时行情/成交/持仓”
- “给我看某个期货品种当前可交易合约一览”

## 数据源
- `ak.futures_zh_realtime(symbol=<品种>)`

## 步骤
1) 如果用户给了中文品种名但不确定：提示可用 `ak.futures_symbol_mark()` 查。
2) 调用实时接口得到 df
3) 输出：按成交量/持仓量/涨跌幅排序的 TopN（默认 10），并提供“主力合约候选”（成交量最大或持仓最大）。

## 最小脚本
- `python3 skills/akshare-router-cn/scripts/futures_realtime.py --symbol PTA --top 10`

## 注意
- 字段列名可能变化：实现时使用“存在即用”的策略（例如优先找 close/最新价、成交量、持仓量）。
- TODO：补充各列名的标准化映射。
