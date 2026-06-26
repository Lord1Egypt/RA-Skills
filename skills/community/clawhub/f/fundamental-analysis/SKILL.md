---
name: fundamental-analysis
description: A-share listed company fundamental analysis — key financial indicators (PE, PB, ROE, gross margin, net margin), data sourcing from East Money (东方财富) / Hexun (同花顺), valuation analysis, industry peer comparison, and structured report output.
emoji: 📈
metadata:
  openclaw:
    requires:
      bins:
        - curl
    envVars:
      - name: EASTMONEY_REFERER
        required: false
        description: Custom referer for East Money API (defaults to https://data.eastmoney.com)
---

# Fundamental Analysis — A股上市公司基本面分析

Systematic fundamental analysis for A-share listed companies. Covers financial health, valuation metrics, profitability ratios, and industry positioning. Produces structured Markdown analysis reports.

## When to Use

| Scenario | Trigger |
|:---------|:--------|
| Stock pick due diligence | User asks "帮我分析一下 XX 股票的基本面" |
| Quarterly/annual report review | After earnings release |
| Valuation check | Before entering/exiting a position |
| Industry comparison | "XX 在行业中估值水平如何？" |
| Investment memo prep | Building a research report |

## Key Financial Indicators

### Valuation Ratios (估值指标)

| Indicator | Formula | What It Tells You |
|:----------|:--------|:------------------|
| **PE (市盈率)** | Price ÷ EPS | 股价是每股盈利的多少倍。>行业均值可能高估，<可能低估。分静态PE、滚动PE(TTM)、动态PE |
| **PB (市净率)** | Price ÷ Book Value Per Share | 股价相对每股净资产的倍数。银行、周期股常用。PB<1表示破净 |
| **PS (市销率)** | Market Cap ÷ Revenue | 适用于亏损企业或高增长公司的估值 |
| **PCF (市现率)** | Price ÷ Cash Flow Per Share | 现金流角度的估值，排除会计造假的干扰 |

### Profitability Ratios (盈利指标)

| Indicator | Formula | Healthy Range |
|:----------|:--------|:--------------|
| **ROE (净资产收益率)** | Net Profit ÷ Avg Equity | >15%优秀，>20%卓越。巴菲特最看重的指标 |
| **ROA (总资产收益率)** | Net Profit ÷ Total Assets | >5%及格，>10%优秀 |
| **Gross Margin (毛利率)** | (Revenue - COGS) ÷ Revenue | 取决于行业。消费>40%，制造>20%为佳 |
| **Net Margin (净利率)** | Net Profit ÷ Revenue | >10%较好。越高说明费用控制越好 |
| **Operating Margin** | Operating Profit ÷ Revenue | 反映主营业务的盈利质量 |

### Growth Indicators (成长指标)

| Indicator | What to Watch |
|:----------|:--------------|
| **Revenue Growth (营收增长率)** | 连续3年>10%为成长型，>20%为高成长 |
| **Net Profit Growth (净利润增长率)** | 看扣非净利润，排除一次性收益干扰 |
| **Operating Cash Flow Growth** | 经营现金流增速需匹配利润增速 |

### Financial Health (财务健康)

| Indicator | Threshold |
|:----------|:----------|
| **Debt-to-Asset (资产负债率)** | <50%安全，>70%需警惕（金融企业除外） |
| **Current Ratio (流动比率)** | >2 安全，<1 短期偿债压力大 |
| **Quick Ratio (速动比率)** | >1 安全，<0.5 危险 |
| **Free Cash Flow (自由现金流)** | 持续为正说明造血能力强 |

## Data Sources & APIs

### 1. 东方财富 East Money (推荐 — 最全)

**Stock Profile & Financial Summary (F10页面):**
```
https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code=SZ000858&color=w#/cwfx
```
Code format: SH=1, SZ=0 → map to `1.600519` (贵州茅台), `0.000858` (五粮液)

**Financial Data API (JSON):**
```
https://datacenter.eastmoney.com/securities/api/data/v1/get
```
Params include `reportName`, `filter`, `pageNumber`, `sortColumns`, etc.

**Key reports to query:**
- `RPT_F10_FINANCE_MAINFINADATA` — Main financial data
- `RPT_F10_PROFITABILITY` — Profitability ratios
- `RPT_F10_DEBTPAYING` — Debt-paying ability
- `RPT_DMSK_FN_GROWTH` — Growth indicators

**Quick way using web_fetch:**
```python
# Fetch from East Money F10 finance summary (basic data)
# URL format: http://f10.eastmoney.com/cwfx.html?code=sh600519
response = await web_fetch("http://f10.eastmoney.com/cwfx.html?code=sh600519")
```

### 2. 同花顺 Hexun / 10jqka

**Stock overview page:**
```
https://basic.10jqka.com.cn/600519/
```

**Financial analysis page:**
```
https://basic.10jqka.com.cn/600519/finance.html
```

### 3. Sina Finance

**Real-time PE/PB (for ultra-fast check):**
```
https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sh600519&scale=5&ma=no&datalen=1
```

### 4. Financial Report URLs (获取财报PDF/在线报告)

| Data | URL Pattern |
|:-----|:------------|
| 东方财富年报页面 | `http://f10.eastmoney.com/ccbgg.html?code=sh600519` |
| 巨潮资讯(巨潮)年报 | `http://www.cninfo.com.cn/new/disclosure/stock?stockCode=600519` |

## Valuation Analysis Methods

### Method 1: PE Band (市盈率区间法)

1. Fetch historical PE (5+ years) for the stock
2. Calculate current PE percentile
3. Compare with industry median PE
4. Judgment:
   - PE < 历史20%分位 → 低估 (Undervalued) 🟢
   - PE 在20%-80%分位 → 合理 (Fair) ⚪
   - PE > 历史80%分位 → 高估 (Overvalued) 🔴

### Method 2: PB Band (市净率区间法)

Best for: Banking, insurance, securities, cyclical stocks

### Method 3: DCF (现金流折现法)

1. Estimate future free cash flows (3-5 year projection)
2. Apply discount rate (WACC, typically 8%-12%)
3. Calculate terminal value
4. Sum = intrinsic value

*Note: DCF is sensitive to assumptions — always provide a sensitivity range.*

### Method 4: Relative Valuation (相对估值法)

Compare PE/PB of target with:
- Industry average
- Direct competitors (top 3-5 peers)
- Global peers (if applicable)

## Workflow: Fundamental Analysis Report

### Step 1: Gather Raw Data

Collect from East Money / 10jqka:
- Basic info: stock code, name, industry, market cap
- Balance sheet: total assets, total liabilities, equity
- Income statement: revenue, COGS, net profit
- Cash flow: operating/ investing/ financing cash flow
- Key ratios: PE, PB, ROE, gross margin, net margin (last 5 years)

**Using web_fetch (recommended approach):**
```python
# Step-by-step data gathering
f10_url = f"http://f10.eastmoney.com/cwfx.html?code=sh{stock_code}"
raw_page = await web_fetch(f10_url)

# Also fetch industry peer data for comparison
industry_data = await web_fetch(
    f"http://push2.eastmoney.com/api/qt/clist/get?...industry={industry_code}"
)
```

### Step 2: Compute Indicators

```python
def compute_ratios(revenue, cost, net_profit, total_assets,
                   total_liabilities, equity, market_cap, shares_outstanding):
    gross_margin = (revenue - cost) / revenue * 100  # %
    net_margin = net_profit / revenue * 100          # %
    roe = net_profit / equity * 100                  # %
    roa = net_profit / total_assets * 100            # %
    debt_ratio = total_liabilities / total_assets * 100  # %
    eps = net_profit / shares_outstanding
    bvps = equity / shares_outstanding
    pe = market_cap / net_profit                     # PE
    pb = market_cap / equity                         # PB

    return {
        "gross_margin": round(gross_margin, 2),
        "net_margin": round(net_margin, 2),
        "roe": round(roe, 2),
        "roa": round(roa, 2),
        "debt_ratio": round(debt_ratio, 2),
        "eps": round(eps, 2),
        "bvps": round(bvps, 2),
        "pe": round(pe, 2),
        "pb": round(pb, 2),
    }
```

### Step 3: Industry Comparison

Build a comparison table with key metrics:

```markdown
### 行业对比：白酒行业 (SW白酒III)

| 股票 | 市值 | PE(TTM) | PB | ROE | 毛利率 | 净利率 |
|:----|:----|:--------|:---|:----|:------|:------|
| 贵州茅台 | 2.1万亿 | 28.5x | 9.2x | 32.1% | 91.8% | 52.5% |
| 五粮液 | 5600亿 | 18.2x | 4.8x | 26.5% | 75.3% | 36.2% |
| 泸州老窖 | 2400亿 | 16.5x | 5.6x | 33.8% | 86.6% | 42.1% |
| **行业均值** | — | **22.1x** | **6.5x** | **30.8%** | **84.5%** | **43.6%** |
```

**Interpretation:**
- PE < 行业均值 → 相对低估
- PE > 行业均值 → 相对高估（但有成长溢价可能）
- ROE > 行业均值 → 盈利能力强
- 毛利率 > 行业均值 → 有定价权/护城河

### Step 4: 5-Year Trend Analysis

Check if the key metrics are improving, stable, or deteriorating:

```markdown
| Year | ROE | 毛利率 | 净利率 | 营收增长率 |
|:----|:----|:------|:------|:----------|
| 2021 | 29.9% | 91.5% | 50.4% | +16.3% |
| 2022 | 30.2% | 91.9% | 51.3% | +14.2% |
| 2023 | 31.8% | 92.0% | 52.1% | +15.8% |
| 2024 | 32.1% | 91.8% | 52.5% | +12.5% |
| 预测 | ~30% | ~91% | ~51% | ~10% |

**趋势判断:**
- ROE: 稳定抬升 ✅
- 毛利率: 极稳，说明定价权强 ✅
- 营收增速: 略有放缓 ⚠️ 但仍在双位数
```

### Step 5: Write Structured Report

Output in the following format:

```markdown
# 📈 基本面分析报告：XX股票

## 📋 基本信息
- 股票代码: XXXXXX
- 所属行业: XX行业
- 总市值: XXXX亿
- 当前股价: XXXXX (YYYY-MM-DD)

## 📊 核心财务指标

| 指标 | 当前值 | 行业均值 | 评价 |
|:----|:------|:---------|:----|
| PE(TTM) | XX.x | XX.x | 🟢 低估 / ⚪ 合理 / 🔴 高估 |
| PB | X.x | X.x | 🟢/⚪/🔴 |
| ROE | XX.x% | XX.x% | 🟢/⚪/🔴 |
| 毛利率 | XX.x% | XX.x% | 🟢/⚪/🔴 |
| 净利率 | XX.x% | XX.x% | 🟢/⚪/🔴 |
| 资产负债率 | XX.x% | XX.x% | 🟢/⚪/🔴 |

## 📈 5年趋势
[趋势数据表和判断]

## 🏭 行业对比
[行业对比表和分析]

## 💡 估值分析
[PE/PB band analysis or relative valuation]

## ⚠️ 风险提示
- 行业风险：...
- 财务风险：...
- 估值风险：...
- 其他：...

## 📝 综合评述

**结论：** 🟢积极 / ⚪中性 / 🔴谨慎
**建议：** 简要的操作建议
```

## Sample User Requests

> "帮我分析一下贵州茅台(600519)的基本面"

→ 行动：获取财务数据 → 计算指标 → 行业对比 → 产出结构化报告

> "五粮液和泸州老窖哪个基本面更好？"

→ 行动：对比两者所有指标 → 行业位置 → 谁更便宜（估值）

> "XX股票PE 50倍，贵不贵？"

→ 行动：看行业均值、历史PE百分位、增长率判断PEG

## Notes

- Always use TTM (滚动市盈率) rather than static PE for timeliness
- For cyclical stocks (周期股), use PB instead of PE as primary valuation metric
- For high-growth stocks, consider PEG (PE ÷ Growth) — PEG < 1 may indicate undervaluation
- Financial/banking stocks: focus on PB, NIM (净息差), NPL (不良率)
- Distinguish between 扣非净利润 (recurring net profit) and total net profit — always use 扣非 for trend analysis
- Free float (流通股本) matters for market cap calculations of non-fully-circulated A-shares
- Data source attribution: include "数据来源：东方财富 / 同花顺" at the end of each report
