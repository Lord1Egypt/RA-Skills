# Metrics by Broker — Complete Tracking List

## Interactive Brokers (IBKR)

| Metric | Unit | Frequency | Source | Historical Context |
|--------|------|-----------|--------|-------------------|
| DARTs | M trades | Monthly (1st biz day) | Business Wire | 2022 bear ~175万; 2021 Meme ~300万; 2026 ~430万+ |
| Client Accounts | 万 | Monthly | Business Wire | 2019 ~78万; 2022 ~215万; 2026 ~475万 |
| Client Equity | $B | Monthly | Business Wire | 2022 bear ~$340B; 2024 ~$570B; 2026 ~$790-820B |
| Margin Loans | $B | Monthly | Business Wire | 2022 bear ~$40B; 2024 ~$64B; 2026 ~$86-90B |
| Client Credit Balances | $B | Monthly | Business Wire | Risk-off indicator when rising simultaneously with margin decline |
| Avg Commission/Order | $ | Monthly | Business Wire | Reflects product mix (options/futures = higher) |
| Annualized DART/Account | # | Monthly | Business Wire | Activity engagement rate |
| NII Sensitivity | $M per 25bp | Quarterly (earnings call) | TipRanks/SEC | -$77M/year per 25bp US rate cut; -$31M per 25bp non-USD |

## Charles Schwab (SCHW)

| Metric | Unit | Frequency | Source | Historical Context |
|--------|------|-----------|--------|-------------------|
| Total Client Assets | $T | Monthly (~15th) | Business Wire | 2019 ~$4.0T; 2022 ~$7.1T; 2026 ~$12.2T |
| Core Net New Assets (NNA) | $B | Monthly | Business Wire | Key organic growth indicator; note one-time items |
| New Brokerage Accounts | 万 | Monthly | Business Wire | 2020-2023 ~300-350万/year; 2025 420万+ |
| Daily Average Trades (DAT) | M trades | Monthly | Business Wire | 2021 Meme ~830万; 2022 bear ~530万; 2026 ~990万 |
| Margin Loan Balances | $B | Monthly | Business Wire | 2022 ~$55B; 2026 ~$120B (record) |
| Transactional Sweep Cash | $B | Monthly | Business Wire | Peak $970B+ (2023.5); stabilized ~$430B (2026) |
| Active Brokerage Accounts | 万 | Monthly | Business Wire | Cumulative total, steadily rising |
| Workplace Plan Participants | 万 | Monthly | Business Wire | |
| NIM (Net Interest Margin) | % | Quarterly | SEC Filing | Q3'25: 2.86%; target ~3.0% |
| FY Guidance EPS | $ | Annual (Jan earnings) | SEC Filing | FY2026 guidance: $5.70-$5.80 |

## Robinhood (HOOD)

| Metric | Unit | Frequency | Source | Historical Context |
|--------|------|-----------|--------|-------------------|
| Funded Customers | 万 | Monthly (~12th-15th) | GlobeNewsWire | 2021 Meme peak ~2,280万; 2023 ~2,300万; 2026 ~2,740万 |
| Total Platform Assets | $B | Monthly | GlobeNewsWire | 2022 ~$62B; 2024 ~$190B; 2026 ~$314B |
| Net Deposits | $B | Monthly | GlobeNewsWire | Monthly + LTM annualized growth rate |
| Equity Notional Trading Vol | $B | Monthly | GlobeNewsWire | 2021 Meme ~$100B/mo; 2026 ~$194-226B |
| Options Contracts Traded | 百万张 | Monthly | GlobeNewsWire | |
| Crypto Notional Trading Vol | $B | Monthly | GlobeNewsWire | Split: Robinhood App + Bitstamp (since June 2025) |
| Event Contracts Traded | 亿张 | Monthly | GlobeNewsWire | New product, launched 2025 |
| Margin Balances | $B | Monthly | GlobeNewsWire | |
| Gold Subscribers | 万 | Quarterly | SEC Filing | Q4'25: 420万 |
| ARPU | $ | Quarterly | SEC Filing | Q1'25: $145 |

## Futu Holdings (FUTU)

| Metric | Unit | Frequency | Source | Historical Context |
|--------|------|-----------|--------|-------------------|
| Funded/Paying Accounts | 万 | Quarterly | PR Newswire/SEC | 2021 ~150万; 2023 ~190万; 2025 ~337万 |
| Total Client Assets | HK$T / $B | Quarterly | PR Newswire | 2022 ~HK$400B; 2025 HK$1.23T (~$158B) |
| Quarterly Trading Volume | HK$T / $B | Quarterly | PR Newswire | Q4'25: HK$3.98T ($511B), record |
| Revenue | HK$B / $M | Quarterly | SEC Filing | Q4'25: $827M (+45% YoY); FY'25: $2.94B (+68%) |
| Non-GAAP Net Income | HK$B / $M | Quarterly | SEC Filing | Q4'25: $444M (+77%); FY'25: $1.50B (+102%) |
| WM AUM | $B | Quarterly | PR Newswire | Q4'25: $23.1B (+62% YoY) |
| Net New Funded Accounts | K/quarter | Quarterly | PR Newswire | Q4'25: ~23.4万; FY'25: 95.4万 |
| Annual Guidance (new accts) | 万 | Annual (Q4 call) | Earnings Call | 2026 guidance: 80万 |
| Gross Margin | % | Quarterly | SEC Filing | FY'25: 87.1% (vs 82.0% in FY'24) |
| US Options Traders Growth | % YoY | Quarterly | PR Newswire | Q4'25: +55% YoY traders, +85% YoY transactions |

## Valuation Metrics (All Four)

| Metric | Source | Frequency | Notes |
|--------|--------|-----------|-------|
| TTM P/E | MacroTrends, FullRatio | Daily | |
| Forward P/E | GuruFocus | Daily | Based on NTM EPS estimates |
| FY EPS (actual) | SEC Filing | Quarterly | |
| FY+1 EPS estimate | Zacks, WallStreetZen | Updated continuously | Track revisions (up/down count in 90 days) |
| Analyst consensus rating | Seeking Alpha, MarketBeat | Updated continuously | |
| Analyst TP (mean/high/low) | MarketBeat, Public.com | Updated continuously | |
| EPS Revision Direction | Seeking Alpha (Earnings Revisions tab) | 90-day rolling | Key signal: # of up revisions vs down |
| Historical PE Range | FullRatio (10Y), MacroTrends | Static | Bear bottom / cycle avg / bull peak |

## Derived / Calculated Metrics (Cross-Company)

These metrics require secondary calculation from raw data. Every value MUST be accompanied by the formula, inputs, and sources.

### AUC per Account
| Broker | Formula | Data Inputs |
|--------|---------|-------------|
| IBKR | Client Equity ($B) ÷ Accounts (M) × 10000 ÷ 1000 | Client Equity from monthly metrics; Accounts from monthly metrics |
| SCHW | Total Client Assets ($T) × 1e12 ÷ Active Accounts (M) × 10000 ÷ 1000 | Both from Monthly Activity Report |
| HOOD | Platform Assets ($B) ÷ Funded Customers (M) × 10000 ÷ 1000 | Both from Monthly Operating Data |
| FUTU | Client Assets ($B) ÷ Funded Accounts (M) × 10000 ÷ 1000 | Both from Quarterly Earnings |

### ARPU (Annual Revenue Per User)
| Broker | Formula | Data Inputs | Caveats |
|--------|---------|-------------|---------|
| IBKR | Quarterly Net Revenue ($M) × 4 ÷ (Accounts ÷ 100) | Revenue from quarterly 8-K; Accounts from monthly report | Uses period-end, not avg; slightly understates |
| SCHW | Quarterly Revenue ($M) × 4 ÷ (Active Accounts ÷ 100) | Revenue from quarterly 8-K; Accounts from monthly report | Same caveat |
| HOOD | **Company-disclosed** | Directly from 8-K | Definition: Total Revenue ÷ avg(start, end Funded Customers), annualized |
| FUTU | Quarterly Revenue ($M) × 4 ÷ (Funded Accounts ÷ 100) | Revenue from quarterly earnings PR | Same caveat as IBKR |

### Margin Utilization Rate
| Broker | Formula | Historical Reference |
|--------|---------|---------------------|
| IBKR | Margin Loans ($B) ÷ Client Equity ($B) × 100 | 2022 bear: ~11.8%; 2024: ~11.2%; Current: ~10.9% |
| SCHW | Margin Loans ($B) ÷ (Client Assets ($T) × 1000) × 100 | Very low (~1%) because denominator includes all $12T+ |
| HOOD | Not directly comparable | Margin balance disclosed but AUC definition differs |

### Revenue Mix
| Broker | Commission Source | NII Source | Other Source |
|--------|------------------|------------|--------------|
| IBKR | "Commissions" line in quarterly 8-K P&L | "Total net interest income" in 8-K | "Other fees and services" + "Other income" |
| SCHW | "Trading revenue" in 8-K | "Net interest revenue" in 8-K | "Asset management and administration fees" |
| HOOD | "Transaction-based revenues" in 8-K/10-K | "Net interest revenues" | "Other revenues" (Gold subs, etc.) |
| FUTU | "Brokerage commission" in earnings PR | "Interest income" minus "Interest expense" | "Other income" (WM, corporate services) |

### NII Rate Sensitivity
| Broker | Sensitivity per 25bp | Source |
|--------|---------------------|--------|
| IBKR | US: -$77M/year; Non-USD: -$31M/year | Q4'25 Earnings Call (TipRanks transcript) |
| SCHW | Significant but offset by balance sheet restructuring | Management commentary; NIM target ~3.0% |
| HOOD | Moderate; diversified revenue reduces impact | 10-K risk factors |
| FUTU | Asian rate environment differs from US | Limited direct disclosure |

### Platform-Specific
| Metric | Broker | Formula | Source |
|--------|--------|---------|--------|
| Gold Adoption Rate | HOOD | Gold Subscribers ÷ Funded Customers × 100 | Both from 8-K / monthly data |
| DARTs per Account (Ann.) | IBKR | Monthly DARTs ÷ Accounts × 252 | IBKR monthly report (directly disclosed) |
| Net Deposit Growth Rate | HOOD | Monthly Net Deposits × 12 ÷ Period-End Platform Assets × 100 | HOOD monthly report (directly disclosed) |
| Cash / Assets Ratio | SCHW | Sweep Cash ($B) ÷ (Client Assets ($T) × 1000) × 100 | SCHW monthly report |
| Gross Margin | FUTU | Gross Profit ÷ Revenue × 100 | FUTU quarterly earnings (directly disclosed) |
| Pretax Margin | IBKR | Pretax Income ÷ Net Revenue × 100 | IBKR quarterly 8-K (directly disclosed) |
| Retirement AUC | HOOD | Absolute value | HOOD quarterly 8-K |
| Strategies AUM | HOOD | Absolute value | HOOD quarterly 8-K |
