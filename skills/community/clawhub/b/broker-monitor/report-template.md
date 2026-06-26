# Report Template — US Retail Broker & Trading Ecosystem Weekly Monitor

Use this template to generate each report. Replace `{PLACEHOLDER}` markers with actual data from web searches.

---

```markdown
# 美股零售券商 & 全市场交易生态 | 周度监控报告

**报告周期**：{WEEK_START_MON} — {WEEK_END_FRI}（本周交易日）
**发布日期**：{PUBLISH_DATE}（周末/周一发布）
**下次更新**：{NEXT_WEEK_DATE}

### 📋 本期数据覆盖范围

| 数据模块 | 频率 | 状态 | 最新数据 | 下次更新 |
|----------|------|------|---------|---------|
| 美股股票交易量 | 周度 | ✅ | W{WEEK_NUM} ({WEEK_END_FRI}) | 下周一 |
| 美股期权交易量 | 周度/月度 | ✅ | W{WEEK_NUM} / {OCC_MONTH}月报 | 下周一 |
| 加密市场快照 | 周度 | ✅ | {CRYPTO_DATE} | 下周一 |
| 交易所市占率(CEX) | 月度 | {CEX_STATUS} | {CEX_MONTH}月 | {CEX_NEXT} |
| 预测市场 | 周度 | ✅ | W{WEEK_NUM} | 下周一 |
| IBKR | 月度(~1日) | {IBKR_STATUS} | {IBKR_MONTH}月 | {IBKR_NEXT} |
| SCHW | 月度(~15日)/Q | {SCHW_STATUS} | {SCHW_MONTH}月 | {SCHW_NEXT} |
| HOOD | 月度(~12日)/Q | {HOOD_STATUS} | {HOOD_MONTH}月 | {HOOD_NEXT} |
| FUTU | 季度 | {FUTU_STATUS} | {FUTU_QUARTER} | {FUTU_NEXT} |
| 估值/EPS | 实时 | ✅ | {PUBLISH_DATE} | 下周一 |

> ⏭️ 沿用上期（未到窗口） ✅ 新数据 🆕 首次发布

---

## 🚩 核心发现与预警信号

### ⬆️ 正面信号 (3–5项，覆盖五大支柱)

**1. {POSITIVE_SIGNAL_1}**
> 来源：{SOURCE_1}

**2. {POSITIVE_SIGNAL_2}**
> 来源：{SOURCE_2}

**3. {POSITIVE_SIGNAL_3}**
> 来源：{SOURCE_3}

### ⚠️ 降速/风险信号 (3–5项)

**1. 🚩 {WARNING_1}**
> 来源：{SOURCE}

**2. 🚩 {WARNING_2}**
> 来源：{SOURCE}

**3. 🚩 {WARNING_3}**
> 来源：{SOURCE}

---

## 〇、全市场交易生态总览

### 0.1 美股全市场交易量

#### 股票交易量

| 指标 | 本周 | 上周 | WoW | 4周均值 | YoY | 来源 |
|------|------|------|-----|--------|-----|------|
| 日均成交量 (B shares) | {VAL} | {PREV} | {WOW}% | {AVG4W} | {YOY}% | Cboe |
| 日均成交额 ($B) | {VAL} | {PREV} | {WOW}% | {AVG4W} | {YOY}% | Cboe |
| NYSE成交量 (B) | {VAL} | {PREV} | {WOW}% | — | — | NYSE |
| NASDAQ成交量 (B) | {VAL} | {PREV} | {WOW}% | — | — | NASDAQ |
| 暗池占比 (%) | {VAL}% | {PREV}% | {CHG}pp | — | — | FINRA ATS |

**📊 牛熊定位**

| 指标 | 🟢 熊底 | 🔵 常态 | 🟡 牛市活跃 | 🔴 极端亢奋 | ⬛ 本周 | 定位 |
|------|--------|--------|-----------|-----------|--------|------|
| 日均量(B) | 7-8 (2019) | 10-11 (2023-24) | 12-14 (2022加息) | 15-17 (2020.3 COVID/2021.1 Meme) | **{VAL}** | {○○●○} |
| 日均额($B) | 300-400 (2019) | 500-600 (2023) | 650-750 (2024-25) | 800+ (恐慌/狂热) | **{VAL}** | {○○●○} |
| 暗池占比(%) | 38-40% (低波动) | 40-42% (常态) | 42-44% (机构避险) | 44%+ (极端避险) | **{VAL}%** | {○●○○} |

#### 期权交易量

| 指标 | 本周 | 上周 | WoW | 4周均值 | YoY | 来源 |
|------|------|------|-----|--------|-----|------|
| 日均合约 (M) | {VAL} | {PREV} | {WOW}% | {AVG4W} | {YOY}% | OCC |
| 股票期权 (M) | {VAL} | {PREV} | {WOW}% | — | — | OCC |
| 指数期权 (M) | {VAL} | {PREV} | {WOW}% | — | — | OCC |
| ETF期权 (M) | {VAL} | {PREV} | {WOW}% | — | — | OCC |
| 0DTE占比 (%) | {VAL}% | {PREV}% | {CHG}pp | — | — | Cboe |
| Put/Call Ratio | {VAL} | {PREV} | — | {AVG4W} | — | Cboe |
| VIX | {VAL} | {PREV} | {CHG} | — | — | Cboe |

**📊 牛熊定位**

| 指标 | 🟢 熊底 | 🔵 常态 | 🟡 牛市活跃 | 🔴 极端 | ⬛ 本周 | 定位 |
|------|--------|--------|-----------|--------|--------|------|
| 日均合约(M) | 18-22 (2019) | 35-42 (2022-23) | 45-55 (2024-25) | 60+ (极端) | **{VAL}** | {○○●○} |
| 0DTE(%) | <20% (2020前) | 30-38% (2022-23) | 42-48% (2024-25) | 50%+ | **{VAL}%** | {○○●○} |
| P/C Ratio | <0.60 极乐观 | 0.65-0.80 中性 | 0.80-1.00 谨慎 | >1.00 恐慌 | **{VAL}** | {○○●○} |
| VIX | <14 极平静(ATL 9.1) | 14-20 常态 | 20-30 紧张 | 30-50+ 危机(ATH 82.7) | **{VAL}** | {○○●○} |

**券商关联**：{分析段落——全市场量 vs SCHW DAT / IBKR DARTs，"潮涨抬船"还是"份额增长"？0DTE对期权佣金影响。}

---

### 0.2 加密市场快照

| 指标 | 本周末 | 上周末 | WoW | 来源 |
|------|-------|-------|-----|------|
| 总市值 ($T) | {VAL} | {PREV} | {WOW}% | CoinGecko/CMC |
| 24h交易量 ($B) | {VAL} | {PREV} | {WOW}% | CoinGecko/CMC |
| BTC价格 ($) | {VAL} | {PREV} | {WOW}% | CoinGecko |
| BTC占比 (%) | {VAL}% | {PREV}% | {CHG}pp | CoinGecko |
| ETH价格 ($) | {VAL} | {PREV} | {WOW}% | CoinGecko |
| 稳定币市值 ($B) | {VAL} | {PREV} | {WOW}% | DefiLlama/CoinGecko |
| 恐惧贪婪指数 | {VAL} | {PREV} | {CHG} | Alternative.me |

**📊 牛熊定位**

| 指标 | 🟢 熊底(2022.11 FTX) | 🔵 恢复(2023) | 🟡 牛市中段(2024-25) | 🔴 极端亢奋(ATH) | ⬛ 本周 | 定位 |
|------|---------------------|-------------|-------------------|-----------------|--------|------|
| 总市值($T) | 0.8-1.0 | 1.2-1.8 | 2.0-2.8 | 3.0+ (2021.11 ATH $2.9T) | **{VAL}** | {○○●○} |
| BTC($K) | 16 | 25-45 | 55-75 | 80-110 (ATH $108K 2024.10) | **{VAL}** | {○○●○} |
| BTC占比(%) | 40-45% (alt season) | 48-55% (均衡) | 55-62% (BTC主导) | 62%+ (极端避险) | **{VAL}%** | {○○●○} |
| 24h量($B) | 30-50 (冷淡) | 60-100 (正常) | 100-200 (活跃) | 200-400+ (狂热/恐慌) | **{VAL}** | {○○●○} |
| 稳定币($B) | 120-130 | 140-165 | 170-200 | 200+ (链上充裕) | **{VAL}** | {○○●○} |
| 恐惧贪婪 | 10-25 极恐 | 40-55 中性 | 60-75 贪婪 | 80-95 极贪(2021.10) | **{VAL}** | {○●○○} |
| CEX月现货($B) | 300-500 (bear) | 600-900 (recovery) | 1000-1800 | 2000+ (2024.3 ATH) | **{VAL}** | {○○●○} |

**券商关联**：{分析段落——BTC价格对HOOD加密收入的阈值效应（$80K+爆发），Schwab入场影响，FUTU加密业务。}

---

### 0.3 交易所市占率 (CEX) — {月度，标注 ✅/⏭️}

| 交易所 | 现货份额 | 上月 | 变化 | 衍生品份额 | 来源 |
|--------|---------|------|------|-----------|------|
| Binance | {PCT}% | {PREV}% | {CHG}pp | {PCT}% | The Block |
| Coinbase | {PCT}% | {PREV}% | {CHG}pp | {PCT}% | The Block |
| OKX | {PCT}% | {PREV}% | {CHG}pp | {PCT}% | The Block |
| Bybit | {PCT}% | {PREV}% | {CHG}pp | {PCT}% | The Block |
| Upbit | {PCT}% | {PREV}% | {CHG}pp | — | The Block |

| 总量 | 最新月 | 上月 | MoM |
|------|-------|------|-----|
| CEX现货 ($B) | {VAL} | {PREV} | {MOM}% |
| CEX衍生品 ($T) | {VAL} | {PREV} | {MOM}% |
| DEX现货 ($B) | {VAL} | {PREV} | {MOM}% |
| DEX/CEX比 (%) | {VAL}% | {PREV}% | — |

---

### 0.4 预测市场

| 平台 | 周交易量 | 上周 | WoW | 活跃市场 | OI | 来源 |
|------|---------|------|-----|---------|-----|------|
| Polymarket | ${VAL}M | ${PREV}M | {WOW}% | {N} | ${VAL}M | Dune |
| Kalshi | ${VAL}M | ${PREV}M | {WOW}% | {N} | — | Kalshi |
| HOOD Events | {VAL}亿张 | {PREV}亿张 | {WOW}% | — | — | HOOD |

| 总量 | 本周 | 上周 | WoW | YoY |
|------|------|------|-----|-----|
| 全平台 ($M) | {VAL} | {PREV} | {WOW}% | {YOY}% |

**趋势判断**：{段落——volume trajectory, catalysts, CFTC, HOOD Events vs Polymarket/Kalshi positioning}

---

## 一、跨公司横向对比

### 1.1 客户数/账户数

| 公司 | {M-2} | {M-1} | {M-0} | MoM | YoY | 定位 |
|------|-------|-------|-------|-----|-----|------|
| SCHW (活跃账户, 万) | {DATA} | {DATA} | {DATA} | {MOM} | {YOY} | {NOTE} |
| HOOD (Funded, 万) | {DATA} | {DATA} | {DATA} | {MOM} | {YOY} | {NOTE} |
| IBKR (账户, 万) | {DATA} | {DATA} | {DATA} | {MOM} | {YOY} | {NOTE} |
| FUTU (付费, 万) | {DATA} | {DATA} | {DATA} | {MOM} | {YOY} | {NOTE} |

### 1.2 客户资产/AUM

| 公司 | {M-2} | {M-1} | {M-0} | MoM | YoY | 定位 |
|------|-------|-------|-------|-----|-----|------|
| SCHW ($T) | {DATA} | {DATA} | {DATA} | {MOM} | {YOY} | {NOTE} |
| IBKR ($B) | {DATA} | {DATA} | {DATA} | {MOM} | {YOY} | {NOTE} |
| HOOD ($B) | {DATA} | {DATA} | {DATA} | {MOM} | {YOY} | {NOTE} |
| FUTU ($B) | {DATA} | {DATA} | {DATA} | {MOM} | {YOY} | {NOTE} |

### 1.3 交易活跃度

| 公司 | {M-2} | {M-1} | {M-0} | MoM | YoY | 定位 |
|------|-------|-------|-------|-----|-----|------|
| SCHW DAT (M) | {DATA} | {DATA} | {DATA} | {MOM} | {YOY} | {NOTE} |
| IBKR DARTs (M) | {DATA} | {DATA} | {DATA} | {MOM} | {YOY} | {NOTE} |
| HOOD Eq Vol ($B) | {DATA} | {DATA} | {DATA} | {MOM} | {YOY} | {NOTE} |
| HOOD Crypto ($B) | {DATA} | {DATA} | {DATA} | {MOM} | {YOY} | {NOTE} |

### 1.4 净资金流入

| 公司 | {M-2} | {M-1} | {M-0} | 年化增速 | 定位 |
|------|-------|-------|-------|---------|------|
| SCHW Core NNA ($B) | {DATA} | {DATA} | {DATA} | {RATE} | {NOTE} |
| HOOD Net Dep ($B) | {DATA} | {DATA} | {DATA} | {RATE}% ann. | {NOTE} |
| IBKR信用余额变化 ($B) | {DATA} | {DATA} | {DATA} | {MOM} | {NOTE} |

---

## 二（续）、📐 衍生指标

### 2.5.1 AUC/Account ($K)

| 公司 | AUC/Account | 上期 | 趋势 | 公式 |
|------|------------|------|------|------|
| SCHW | {VAL}K | {PREV}K | {↗/↘} | 客户资产÷活跃账户 |
| IBKR | {VAL}K | {PREV}K | {↗/↘} | 权益÷账户 |
| FUTU | {VAL}K | {PREV}K | {↗/↘} | 资产÷付费账户 |
| HOOD | {VAL}K | {PREV}K | {↗/↘} | 平台资产÷Funded客户 |

### 2.5.2 年化ARPU ($)

| 公司 | ARPU | 计算方式 | 排名 |
|------|------|---------|------|
| IBKR | ${VAL} | 季度净收入×4÷期末账户 | {#} |
| FUTU | ${VAL} | 季度收入×4÷付费账户 | {#} |
| SCHW | ${VAL} | 季度收入×4÷活跃账户 | {#} |
| HOOD | ${VAL} | 公司披露(annualized) | {#} |

### 2.5.3 杠杆率

| 公司 | 保证金/资产 | 保证金余额 | 风险评估 |
|------|-----------|-----------|---------|
| IBKR | {PCT}% | ${VAL}B | {vs 2022 bear 11.8%} |
| SCHW | {PCT}‰ | ${VAL}B | {vs historical} |
| HOOD | — | ${VAL}B | {YoY growth rate} |

### 2.5.4 收入结构

| 公司 | 佣金 | NII | 其他 | 利率敏感度 |
|------|------|-----|------|-----------|
| IBKR | {PCT}% | {PCT}% | {PCT}% | 🔴 -$77M/yr per 25bp US |
| SCHW | ~8% | ~48% | ~44% | 🔴 NII主导 |
| HOOD | ~50%(PFOF) | ~22% | ~28% | 🟡 中 |
| FUTU | {PCT}% | {PCT}% | ~10% | 🟡 中 |

### 2.5.5 平台特色指标

| 指标 | 公司 | 值 | 公式/来源 |
|------|------|----|---------|
| Gold订阅率 | HOOD | {PCT}% | Subs÷Customers, HOOD 8-K |
| 每账户DART | IBKR | {VAL} | 月DARTs÷账户×252, IBKR月报 |
| Net Dep增速 | HOOD | {PCT}% | 月Dep×12÷资产, HOOD月报 |
| 现金/资产 | SCHW | {PCT}% | Sweep÷(资产×1000) |
| 毛利率 | FUTU | {PCT}% | FUTU PR |
| 加密/总收入 | HOOD | {PCT}% | HOOD 8-K |
| 事件合约/总交易 | HOOD | {PCT}% | HOOD月报 |

### 2.5.6 加密/预测市场衍生

| 指标 | 值 | 公式 | 来源 |
|------|----|------|------|
| HOOD加密占CEX现货 | {PCT}% | HOOD加密量÷CEX现货总量 | HOOD+The Block |
| Coinbase份额变化 | {CHG}pp | 最新月-上月 | The Block |
| 预测市场penetration | {PCT}% | 预测总量÷(CEX现货+预测) | Dune+The Block |
| HOOD Events份额 | {PCT}% | HOOD Events(折$)÷全平台 | HOOD+Dune |
| 加密/美股市值比 | {PCT}% | 加密总市值÷S&P总市值 | CoinGecko+S&P |

---

## 三、个股三个月滚动仪表盘

### 3.1 IBKR

| 指标 | {M-2} | {M-1} | {M-0} | MoM | YoY | 牛熊定位 |
|------|-------|-------|-------|-----|-----|---------|
| DARTs (M) | {V} | {V} | {V} | {%} | {%} | {context} |
| 账户 (万) | {V} | {V} | {V} | {%} | {%} | {context} |
| 权益 ($B) | {V} | {V} | {V} | {%} | {%} | {context} |
| 保证金 ($B) | {V} | {V} | {V} | {%} | {%} | {context} |
| 信用余额 ($B) | {V} | {V} | {V} | {%} | {%} | {context} |
| 佣金/单 ($) | {V} | {V} | {V} | {%} | — | {context} |
| 期权合约 (M) | {V} | {V} | {V} | {%} | {%} | {context} |
| 期货合约 (M) | {V} | {V} | {V} | {%} | {%} | {context} |

### 3.2 SCHW

| 指标 | {M-2} | {M-1} | {M-0} | MoM | YoY | 牛熊定位 |
|------|-------|-------|-------|-----|-----|---------|
| DAT (M) | {V} | {V} | {V} | {%} | {%} | {context} |
| 客户资产 ($T) | {V} | {V} | {V} | {%} | {%} | {context} |
| Core NNA ($B) | {V} | {V} | {V} | — | — | {context} |
| 新开户 (万) | {V} | {V} | {V} | {%} | {%} | {context} |
| 保证金 ($B) | {V} | {V} | {V} | {%} | {%} | {context} |
| Sweep Cash ($B) | {V} | {V} | {V} | {%} | — | {context} |
| 活跃账户 (万) | {V} | {V} | {V} | — | {%} | {context} |

### 3.3 HOOD

| 指标 | {M-2} | {M-1} | {M-0} | MoM | YoY | 牛熊定位 |
|------|-------|-------|-------|-----|-----|---------|
| Funded客户 (万) | {V} | {V} | {V} | {%} | {%} | {context} |
| 平台资产 ($B) | {V} | {V} | {V} | {%} | {%} | {context} |
| Net Dep ($B) | {V} | {V} | {V} | {%} | — | {context} |
| 股票交易 ($B) | {V} | {V} | {V} | {%} | {%} | {context} |
| 加密交易 ($B) | {V} | {V} | {V} | {%} | {%} | {context} |
| 事件合约 (亿张) | {V} | {V} | {V} | {%} | — | {context} |
| 保证金 ($B) | {V} | {V} | {V} | {%} | {%} | {context} |

### 3.4 FUTU (季度)

| 指标 | {Q-2} | {Q-1} | {Q-0} | QoQ | YoY | 牛熊定位 |
|------|-------|-------|-------|-----|-----|---------|
| 付费账户 (万) | {V} | {V} | {V} | {%} | {%} | {context} |
| 客户资产 ($B) | {V} | {V} | {V} | {%} | {%} | {context} |
| 交易量 ($B) | {V} | {V} | {V} | {%} | {%} | {context} |
| 收入 ($M) | {V} | {V} | {V} | {%} | {%} | {context} |
| 净利润 ($M) | {V} | {V} | {V} | {%} | {%} | {context} |
| WM AUM ($B) | {V} | {V} | {V} | {%} | {%} | {context} |
| 新增账户 (万) | {V} | {V} | {V} | {%} | {%} | {context} |

---

## 四、关键趋势分析

### 4.1 交易活跃度 — {HEADLINE}

| 周期 | SCHW DAT水平 | 背景 |
|------|-------------|------|
| 2018-2019 | ~350-450万 | 低波动牛市 |
| 2020.3 | ~700万 | COVID恐慌 |
| 2021.1-2 | ~830万 | Meme Stock |
| 2022 | ~530-600万 | 加息熊市 |
| 2023-2024 | ~580-700万 | 复苏 |
| **当前** | **{VAL}** | **{CONTEXT}** |

{分析段落：增速加速还是放缓？结构性还是周期性？}

### 4.2 客户资产 — {HEADLINE}

| 里程碑 | SCHW客户资产 | 时间 |
|--------|------------|------|
| $4T | 2019 | 基准 |
| $7T | 2022(含TD合并) | 并购驱动 |
| $10T | 2024 | 市场+有机 |
| **$12T+** | **2026** | **持续增长** |

{分析段落：市场驱动 vs 有机增长}

### 4.3 保证金贷款 — {HEADLINE}

{IBKR杠杆率 vs 2022 bear (11.8%)分析。SCHW $120B+创纪录。HOOD margin +98% YoY风险评估。}

### 4.4 FUTU的特殊位置

{FUTU增长 vs 估值错配分析。中概折价。地域扩展（马来西亚、日本）。}

### 4.5 加密交易生态演变

| 周期 | BTC | 总市值 | CEX月量 | 背景 |
|------|-----|--------|--------|------|
| 2022底 | ~$16K | ~$0.8T | ~$500B | FTX暴雷 |
| 2023底 | ~$42K | ~$1.6T | ~$800B | ETF预期 |
| 2024.3 | ~$73K | ~$2.7T | ~$2.5T | ATH+ETF |
| 2025 | ~$60-100K | ~$2-3T | ~$1-2T | 波动调整 |
| **当前** | **${VAL}** | **${VAL}T** | **${VAL}B** | **{CONTEXT}** |

{分析：CEX量趋势、DEX份额增长、Coinbase vs Binance、监管变化、Schwab入场影响}

### 4.6 预测市场发展轨迹

| 时期 | Polymarket | Kalshi | HOOD Events | 总量 | 催化 |
|------|-----------|--------|-------------|------|------|
| 2024前 | <$100M/月 | <$50M/月 | N/A | <$200M | 小众 |
| 2024大选 | ~$2B+/月 | ~$500M/月 | 起步 | ~$3B | 大选 |
| 大选后 | {VAL} | {VAL} | {VAL} | {VAL} | 回落 |
| **当前** | **${VAL}** | **${VAL}** | **{VAL}** | **${VAL}** | **{CONTEXT}** |

{分析：post-election持续性、新催化、CFTC监管、HOOD Events竞争}

---

## 五、估值深度分析

### 5.1 估值横向对比

| 指标 | SCHW | IBKR | HOOD | FUTU |
|------|------|------|------|------|
| 股价 | ${PRICE} | ${PRICE} | ${PRICE} | ${PRICE} |
| 市值 | {MKTCAP} | {MKTCAP} | {MKTCAP} | {MKTCAP} |
| TTM P/E | {PE}x | {PE}x | {PE}x | {PE}x |
| Forward P/E | {FPE}x | {FPE}x | {FPE}x | {FPE}x |
| TTM EPS | ${EPS} | ${EPS} | ${EPS} | ${EPS} |
| FY+1 EPS Est | ${EST} | ${EST} | ${EST} | ${EST} |
| FY+1 EPS增速 | {G}% | {G}% | {G}% | {G}% |
| 分析师共识 | {RATING} | {RATING} | {RATING} | {RATING} |

> 数据来源：{SOURCES_WITH_DATES}

### 5.2 历史PE区间

| 公司 | 熊底PE | 周期均值 | 牛市峰值 | 当前 | 定位 |
|------|-------|---------|---------|------|------|
| SCHW | 13.0x (2020.3) | 23x (10Y) | 31.5x (2017) | {VAL}x | {NOTE} |
| IBKR | ~15x (2022) | ~25x (5Y) | ~40x (2025) | {VAL}x | {NOTE} |
| HOOD | N/A (亏损) | ~35x (3Y) | 134x (2024.3) | {VAL}x | {NOTE} |
| FUTU | ~8x (2022) | ~18x (3Y) | 45x+ (2021) | {VAL}x | {NOTE} |

### 5.3 估值判断摘要

{SCHW判断段落}
{IBKR判断段落}
{HOOD判断段落}
{FUTU判断段落}

### 5.4 Forward EPS 下修追踪

| 公司 | 此前共识 | 最新共识 | 变化 | 时间 | 方向 | 驱动 | 来源 |
|------|---------|---------|------|------|------|------|------|
| SCHW | {PREV} | {CURR} | {CHG} | {DATE} | {↑/↓/→} | {REASON} | {SRC} |
| IBKR | {PREV} | {CURR} | {CHG} | {DATE} | {↑/↓/→} | {REASON} | {SRC} |
| HOOD | {PREV} | {CURR} | {CHG} | {DATE} | {↑/↓/→} | {REASON} | {SRC} |
| FUTU | {PREV} | {CURR} | {CHG} | {DATE} | {↑/↓/→} | {REASON} | {SRC} |

{每家判断段落，标注>5%下修的}

---

## 六、宏观环境与利率敏感性

| 宏观变量 | 当前状态 | 对板块影响 |
|----------|---------|----------|
| Fed Funds Rate | {STATUS} | {IMPACT on SCHW/IBKR NII} |
| VIX波动率 | {LEVEL} {牛熊定位} | {IMPACT on trading volumes} |
| S&P 500 | {LEVEL}, 周区间{RANGE}点 | {IMPACT on client assets} |
| 关税/贸易战 | {STATUS} | {IMPACT on sentiment} |
| Forward EPS增速 | {STATUS} | {IMPACT on market direction} |
| 加密(BTC/总市值) | BTC ${VAL}, {牛熊定位} | {IMPACT: HOOD/FUTU加密收入} |
| 预测市场监管(CFTC) | {STATUS} | {IMPACT: HOOD Events扩张上限} |
| CEX监管(SEC) | {STATUS} | {IMPACT: Coinbase合规成本, HOOD加密边界} |

---

## 七、下周/下月关注

| 事件 | 日期 | 关注要点 |
|------|------|---------|
| {EVENT_1} | {DATE} | {FOCUS} |
| {EVENT_2} | {DATE} | {FOCUS} |
| {EVENT_3} | {DATE} | {FOCUS} |

---

## 八、风险预警检查

| 预警项 | 状态 | 评估 |
|--------|------|------|
| 交易量持续萎缩 | {❌/⚠️/🔴} | {DETAIL} |
| 客户资产大规模外流 | {❌/⚠️/🔴} | {DETAIL} |
| 保证金贷款过高 | {❌/⚠️/🔴} | {DETAIL} |
| Cash Sorting恶化 | {❌/⚠️/🔴} | {DETAIL} |
| 监管冲击 | {❌/⚠️/🔴} | {DETAIL} |
| 利率急变 | {❌/⚠️/🔴} | {DETAIL} |
| 中概风险(FUTU) | {❌/⚠️/🔴} | {DETAIL} |
| 加密崩盘(>30%回撤) | {❌/⚠️/🔴} | {DETAIL} |
| 预测市场监管收紧 | {❌/⚠️/🔴} | {DETAIL} |
| CEX流动性危机 | {❌/⚠️/🔴} | {DETAIL} |

---

## 脚注与数据来源

| # | 来源 | 日期 |
|---|------|------|
| ¹ | {SOURCE} | {DATE} |
| ² | {SOURCE} | {DATE} |

**数据来源说明：**
- 美股交易量：Cboe (cboe.com), OCC (optionsclearing.com), NYSE, NASDAQ, FINRA ATS
- 券商月报：Business Wire, GlobeNewsWire, PR Newswire, company IR
- 估值/EPS：StockAnalysis, MacroTrends, Seeking Alpha, Zacks, TipRanks
- 加密：CoinGecko (coingecko.com), CoinMarketCap, DefiLlama
- 交易所份额：The Block (theblock.co/data), CCData, CoinDesk, Kaiko
- 预测市场：Dune Analytics (@polymarket, @rchen8), Polymarket blog, Kalshi blog
- 宏观：FRED, CME FedWatch

---

*本报告仅为投资研究参考，不构成投资建议。*
```
