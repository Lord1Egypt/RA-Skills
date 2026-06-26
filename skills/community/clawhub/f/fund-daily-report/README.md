# 基金日报 — 天天基金网数据

基于天天基金网 (fund.eastmoney.com) 和东方财富 Choice 数据，每日生成基金市场分析报告。

## 功能

- 📊 **近30天净值涨幅 TOP 10** — 开放式基金（股票型+混合型）
- 💰 **近30天资金流入 TOP 10** — ETF场内基金（按资金关注度）
- 🏭 **近30天行业资金流 TOP 5** — 概念板块主力资金
- 📈 **近30天基金加仓 TOP 10 股票** — 按资金关注度排序

## 安装

```bash
pip install akshare jqdatasdk pandas numpy
```

## 使用

```bash
python fund_daily_report.py
```

## 建议执行时间

每个交易日 **15:30** 之后（收盘后净值更新）

## 数据源

| 数据源 | 接口 | 覆盖 |
|--------|------|------|
| 天天基金网 | `fund_open_fund_rank_em` | 19,584只开放式基金 |
| 天天基金网 | `fund_exchange_rank_em` | 1,501只ETF基金 |
| 东方财富 | `stock_fund_flow_concept` | 概念板块资金流 |
| JQData | `get_price` + 成分股 | 沪深300个股数据（降级） |

## 注意事项

- 公司网络可能拦截东方财富 push2 API
- 基金净值 T+1 更新
- 建议配合 OpenClaw Heartbeat 每日自动运行
