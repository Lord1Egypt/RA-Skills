# Recipe: options_rr25 (RR25)

## 适用问题
- “50ETF 当月 RR25 多少？”
- “给我 25D 风险逆转，并告诉我选的是哪两个合约”

## 数据源
- 同 `recipes/options_iv_greeks.md`

## 方法
- 见 `methods/rr25.md`

## 步骤（MVP）
1) 确认 underlying（默认 510050）与 trade_date（默认最近月）
2) 拉取看涨/看跌内码列表
3) 对所有内码抓取 greeks/iv（注意速率；MVP 可抓取前 24 个，通常够覆盖不同 strike）
4) 按 `methods/rr25.md` 选择最接近 ±0.25 delta 的合约
5) 计算 RR25 并输出：
   - RR25 数值
   - 选中 call/put：合约简称、行权价、delta、iv、最新价

## 最小脚本
- `python3 skills/akshare-router-cn/scripts/options_rr25.py --underlying 510050 --trade_date 202603`

## 注意
- 这是近似 RR25（离散 delta），用于盘中监控/比较。
- TODO：二期做 smile 拟合 + 插值，得到更稳定 RR25。
