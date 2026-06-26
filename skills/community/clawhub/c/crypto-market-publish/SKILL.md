---
name: crypto-market
description: Comprehensive cryptocurrency market monitoring and economic data analysis. Use when tracking crypto prices, market sentiment, economic data releases, or analyzing how economic indicators impact crypto markets. Supports price alerts, economic calendar management, actual value updates, and automated reporting. After installation, run from your crypto workspace (default path in INSTALL.md).
---

# Crypto Market Monitor

Complete cryptocurrency market monitoring system with price tracking, economic data releases, and impact analysis.

## Installation

Quick install:
```bash
clawhub install crypto-market
```

For manual installation, see [INSTALL.md](INSTALL.md).

## Quick Start

### Price Monitoring
Monitor 13 major cryptocurrencies (BTC, ETH, XRP, BNB, SOL, ADA, AVAX, DOGE, TRX, LINK, SUI, WLFI, XAUT) with real-time prices, volatility alerts (±5%), market sentiment analysis, and EMA technical indicators.

**From your crypto workspace:**
```bash
cd scripts
python3 crypto_monitor_telegram.py
```

### Economic Data Reports
View upcoming economic data releases (7-day forecast) with importance levels (high/medium) and countdown timers.

**From your crypto workspace:**
```bash
cd economic
python3 daily_economic_report_v2.py
```

## Economic Data Analysis

### Update Actual Values
When economic data is released, update actual values to trigger automatic bullish/bearish analysis.

**From your crypto workspace:**
```bash
cd economic
python3 update_economic_data.py update "数据名称" "实际值" --datetime "发布时间"
```

**Examples:**
```bash
# CPI data (lower is bullish)
python3 update_economic_data.py update "CPI 消费者价格指数" "2.1%" --datetime "2026-03-13 21:30"

# NFP data (higher is bullish)
python3 update_economic_data.py update "非农就业数据" "+280K" --datetime "2026-03-14 21:30"

# GDP data (higher is bullish)
python3 update_economic_data.py update "GDP 季度报告" "1.8%" --datetime "2026-03-20 21:30"

# Unemployment rate (lower is bullish)
python3 update_economic_data.py update "失业率" "4.0%" --datetime "2026-03-14 21:30"
```

### Quick Analysis (No Save)
Analyze data impact without saving to database.

```bash
python3 update_economic_data.py analyze "数据名称" "实际值" "预期值" "前值"
```

**Example:**
```bash
python3 update_economic_data.py analyze "CPI" "2.1%" "2.3%" "2.4%"
```

### View Updated Data
Check all economic data with actual values.

```bash
python3 update_economic_data.py list
```

## Bullish/Bearish Analysis

### Bullish Indicators (Higher is Bullish) 🟢
- Non-Farm Payrolls (NFP)
- GDP
- Retail Sales
- ADP Employment
- Manufacturing PMI
- Services PMI

**Rule:** Actual > Expected (+2%+) = Bullish

### Bearish Indicators (Lower is Bullish) 🟢
- CPI (Inflation)
- PPI (Prices)
- Unemployment Rate
- Interest Rates (FOMC)

**Rule:** Actual < Expected (-2%+) = Bullish (pressure relief)

## Scheduled Reports

### Daily Economic Report
- **Time:** 08:00 AM daily
- **Content:** 7-day economic data forecast
- **Format:** High importance events with expected/previous values and countdown

### Comprehensive Monitoring
- **Time:** Every 30 minutes
- **Content:** Crypto prices + economic data reminders
- **Features:** Volatility alerts, market sentiment, EMA indicators

## Default Workspace Structure

```
crypto/                    # Your crypto workspace
├── economic/            # Economic data scripts
├── scripts/             # Monitoring scripts
├── data/                # Data storage (actual_data.json)
└── logs/                # Log files
```

## Data Types

### High Importance
- Non-Farm Payrolls (NFP) - First Friday monthly, 21:30
- CPI - Mid-month, 21:30
- FOMC Interest Rate - Quarterly, 02:00
- GDP - Quarterly end, 21:30
- Unemployment Rate - First Friday monthly, 21:30

### Medium Importance
- ADP Employment - First Wednesday monthly, 21:15
- Retail Sales - Mid-month, 21:30
- Manufacturing PMI - First day monthly, 22:00
- Services PMI - First day monthly, 22:00
- PPI - Mid-month, 21:30

**See [data-types.md](references/data-types.md) for detailed information on each indicator.**

## Scripts

**Core modules (in economic/):**
- `economic_calendar.py` - Economic calendar management
- `economic_analyzer.py` - Bullish/bearish analysis engine
- `update_economic_data.py` - Actual value management

**Monitoring (in scripts/):**
- `crypto_monitor_telegram.py` - Price monitoring + economic data

**References:**
- [quick-reference.md](references/quick-reference.md) - Command cheat sheet
- [data-types.md](references/data-types.md) - Economic indicator details
- [usage-examples.md](references/usage-examples.md) - Real-world scenarios

## Customization

### Change Workspace
Edit paths in scripts or create a config file. See [INSTALL.md](INSTALL.md) for details.

### Modify Alert Threshold
Edit `scripts/crypto_monitor_telegram.py`:
```python
ALERT_THRESHOLD = 5.0  # Change to your preferred threshold
```

### Add/Remove Tokens
Edit `scripts/crypto_monitor_telegram.py` `TOKENS` dictionary.

## Important Notes

1. **Timezone:** All times are Asia/Shanghai (Beijing Time)
2. **Data Storage:** Actual values saved to `data/actual_data.json`
3. **Impact Analysis:** Automatic bullish/bearish determination based on actual vs expected deviation
4. **Alert Thresholds:** Price volatility alerts trigger at ±5% change

**For detailed installation, customization, and usage scenarios, see [INSTALL.md](INSTALL.md) and [usage-examples.md](references/usage-examples.md).**
