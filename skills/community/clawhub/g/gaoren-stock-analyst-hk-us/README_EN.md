# Stock Analyst - Intelligent Stock Analysis System

[中文](./README.md) | English

Intelligent stock analysis assistant, supporting real-time quotes for A-shares, HK stocks, and US stocks with technical analysis and trend prediction.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

### 1. Real-time Quotes
- **A-shares**: Tencent Finance API (6-digit codes)
- **HK stocks**: Tencent Finance API (5-digit codes)
- **US stocks**: Finnhub API (ticker symbols)

### 2. Technical Analysis
- Real-time price change
- Open/High/Low/Close prices
- Trading volume
- Amplitude calculation
- Distance from high/low
- Support/Resistance levels

### 3. Comprehensive Analysis
- Trend prediction (Strong Up/Slight Up/Sideways/Slight Down/Strong Down)
- Bull/Bear analysis
- Risk alerts
- Trading suggestions

## Supported Stock Codes

### A-Shares (6-digit)
| Stock | Code |
|-------|------|
| PetroChina | 601857 |
| Kweichow Moutai | 600519 |
| CATL | 300750 |
| BYD | 002594 |

### HK Stocks (5-digit)
| Stock | Code |
|-------|------|
| JD Logistics | 02618 |
| JD.com | 09618 |
| Tencent | 00700 |
| Alibaba | 09988 |
| Meituan | 03690 |

### US Stocks (Ticker)
| Stock | Code |
|-------|------|
| JD.com | JD |
| Alibaba | BABA |
| Tesla | TSLA |
| Apple | AAPL |
| NVIDIA | NVDA |

## Usage

```bash
# Analyze A-share
python analyze_stock.py 601857

# Analyze HK stock
python analyze_stock.py 02618

# Analyze US stock
python analyze_stock.py JD
```

## Installation

```bash
git clone https://github.com/gaoren36-arch/stock-analyst.git
cd stock-analyst
pip install requests
```

## Tech Stack

- **Language**: Python 3.10+
- **Data Sources**:
  - Tencent Finance (HK/A-shares)
  - Finnhub API (US stocks)
- **Dependencies**: requests

## Version History

- v1.1.0: Added A-share support, enhanced technical analysis
- v1.0.0: Initial release

## License

MIT License

## Author

- GitHub: [@gaoren36-arch](https://github.com/gaoren36-arch)
