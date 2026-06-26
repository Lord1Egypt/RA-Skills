---
name: market-intel
description: "金融市场情报聚合系统：恐慌指数、指数行情、市场要闻、财经日历、加密货币技术分析。Trigger on: 恐慌指数, 恐惧贪婪, fear greed, 行情, 指数, 大盘, 股价, 要闻, 快讯, 财经日历, 宏观事件, NFP, FOMC, CPI, PPI, PMI, LPR, 非农, 美联储, 欧央行, BTC, ETH, TON, 加密货币, 走势分析, 技术分析, 背离, 顶背离, 底背离"
version: 1.1.0
license: MIT
---

# Market Intel 📊

金融市场情报聚合系统 — 对标 investing.com 核心功能，全免费数据源。

## What it does

- **恐慌贪婪指数**: 美股(CNN) + 加密货币双市场实时情绪，含分化分析和策略建议
- **指数行情**: A股(上证/深证/沪深300/科创50/创业板) + 美股(纳斯达克/标普500/道琼斯)
- **市场要闻**: CNBC + MarketWatch RSS 实时快讯
- **财经日历**: 本周/下周重要宏观事件（FOMC、NFP、CPI、ECB等）
- **加密货币技术分析**: 多周期指标分析框架（量能/背离/波动率/合约/消息面），支持 BTC/ETH/TON/LINK/SOL 等

## Scripts

| Script | Trigger | Purpose |
|--------|---------|---------|
| `scripts/fear-greed.sh` | 恐慌指数/恐惧贪婪 | 双市场恐慌贪婪指数快照 |
| `scripts/quotes.sh` | 行情/指数/大盘 | A股+美股指数实时行情 |
| `scripts/news.sh` | 要闻/快讯 | CNBC+MarketWatch市场快讯 |
| `scripts/ecal.sh` | 财经日历/日历 | 本周/下周宏观事件安排 |
| `scripts/crypto-data.sh <COIN>` | BTC/ETH/TON 走势 | 一键获取多周期K线+技术指标+合约数据 |

## Analysis Framework

加密货币技术分析遵循 `references/crypto-analysis.md` 中的七维分析框架。当用户请求任何代币走势分析时，必须使用该框架，覆盖以下维度：

1. **量能分析** — 当前成交量 vs 7日均值，判断放量/缩量
2. **多周期背离检测** — 15m/4H/1D 的 RSI+MACD 顶背离/底背离
3. **关键位置** — 支撑/阻力位（前高前低、EMA、布林带）
4. **波动率评估** — 24h波动率 vs 7日均值
5. **合约市场** — 资金费率 + 持仓量(OI)方向
6. **消息面** — 跨引用要闻快讯
7. **浓缩信号** — 3-5条后续关注重点 + 方向预判

## Data Sources

| 来源 | 用途 | 费用 |
|------|------|------|
| Alternative.me | Crypto Fear & Greed | 免费 |
| CNN Dataviz API | 美股 Fear & Greed | 免费 |
| 东方财富 push2 API | A股+美股指数行情 | 免费 |
| CNBC RSS | 美股市场要闻 | 免费 |
| MarketWatch RSS | 美股市场头条 | 免费 |

## Output Style

- 纯 ASCII 标题 `===== 恐慌贪婪指数 =====`（手机安全不折行）
- 5颗星评级 `★★☆☆☆` 替代进度条（直观不错位）
- 简洁一行一条指数行情