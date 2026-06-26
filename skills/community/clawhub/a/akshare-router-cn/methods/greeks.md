# Methods: greeks/iv normalization

一期不自己推 Greeks（避免模型假设错误），优先使用 `ak.option_sse_greeks_sina` 返回的 Delta/Gamma/Theta/Vega/隐含波动率。

## 输入
- `ak.option_sse_greeks_sina(symbol=<sina_option_code>)` 返回的两列表：字段/值

## 归一化输出（建议内部字段名）
- name
- volume
- price_last
- strike
- iv
- delta, gamma, theta, vega
- theo_value
- trade_code (交易代码)

## 字段映射（MVP）
- "期权合约简称" → name
- "成交量" → volume
- "最新价" → price_last
- "行权价" → strike
- "隐含波动率" → iv
- "Delta"/"Gamma"/"Theta"/"Vega" → 同名小写
- "理论价值" → theo_value
- "交易代码" → trade_code

> TODO：确认是否存在 Rho 字段；以及不同标的/版本下中文字段是否变化。
