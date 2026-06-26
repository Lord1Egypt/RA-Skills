# Crypto Market Monitor - Quick Reference

## Directory Structure

```
crypto/                    # Your crypto workspace
├── economic/            # Economic data scripts
│   ├── economic_calendar.py
│   ├── economic_analyzer.py
│   ├── daily_economic_report_v2.py
│   └── update_economic_data.py
├── scripts/             # Monitoring scripts
│   └── crypto_monitor_telegram.py
├── data/                # Data storage
│   └── actual_data.json
└── logs/                # Log files
```

## Core Commands

### Price Monitoring
```bash
cd scripts
python3 crypto_monitor_telegram.py
```

### Economic Data Report
```bash
cd economic
python3 daily_economic_report_v2.py
```

### Update Economic Data
```bash
cd economic
python3 update_economic_data.py update "数据名称" "实际值" --datetime "发布时间"
```

### View Updated Data
```bash
cd economic
python3 update_economic_data.py list
```

### Quick Analysis
```bash
cd economic
python3 update_economic_data.py analyze "数据名称" "实际值" "预期值" "前值"
```

## Common Data Names

Complete names (for update command):
- "CPI 消费者价格指数"
- "PPI 生产者价格指数"
- "非农就业数据"
- "GDP 季度报告"
- "失业率"
- "FOMC 利率决议"
- "零售销售月率"
- "ADP 就业数据"
- "制造业PMI"
- "服务业PMI"

## Bullish/Bearish Rules

### Bullish Indicators (Higher is Bullish) 🟢
- 👷 NFP (Non-Farm Payrolls)
- 🏛️ GDP
- 🛒 Retail Sales
- 💼 ADP Employment
- 🏭 Manufacturing PMI
- 🏢 Services PMI

**Rule:** Actual > Expected (+2%+) = Bullish
**Rule:** Actual < Expected (-2%+) = Bearish

### Bearish Indicators (Lower is Bullish) 🟢
- 📊 CPI (Inflation)
- 📈 PPI (Prices)
- 📉 Unemployment Rate
- 🏦 Interest Rates (FOMC)

**Rule:** Actual < Expected (-2%+) = Bullish (pressure relief)
**Rule:** Actual > Expected (+2%+) = Bearish (pressure increases)

## Monitored Tokens

BTC, ETH, XRP, BNB, SOL, ADA, AVAX, DOGE, TRX, LINK, SUI, WLFI, XAUT

## Data Sources

- CoinGecko API (primary)
- Binance API (backup)

## Log Locations

From your crypto workspace:
- Economic data: `logs/economic_report.log`
- Comprehensive: `logs/crypto_monitor.log`

## Installation

```bash
clawhub install crypto-market
```

For manual installation, see [INSTALL.md](../INSTALL.md).
