# Market Breadth Analyzer

Quantify market breadth health with a data-driven 0-100 composite score based on participation metrics.

## Description

Market Breadth Analyzer provides an objective, quantitative assessment of market health by analyzing six key breadth components: advance-decline trends, new highs/lows, percentage of stocks above key moving averages, and distribution days. The skill generates a single composite score (0-100) where 100 represents maximum breadth health and 0 indicates critical weakness.

## Key Features

- **0-100 composite score** - Single number summarizing overall market breadth health
- **Six scored components** - Advance-decline, new highs/lows, MA participation, distribution
- **Zone classification** - Strong (80+), Healthy (60-79), Neutral (40-59), Weak (20-39), Critical (<20)
- **Automated data fetching** - Uses publicly available CSV data (no API key needed)
- **Freshness validation** - Warns if data is stale (>5 days old)
- **Weight redistribution** - Automatically handles missing components

## Quick Start

```bash
# Install dependencies
pip install pandas requests

# Run breadth analysis
python3 scripts/market_breadth_analyzer.py \
  --detail-url "https://tradermonty.github.io/market-breadth-analysis/market_breadth_data.csv" \
  --summary-url "https://tradermonty.github.io/market-breadth-analysis/market_breadth_summary.csv"
```

**Output:**
```
MARKET BREADTH HEALTH: 72/100 (Healthy)

Component Breakdown:
- Advance-Decline Trend: 85/100
- New Highs vs Lows: 68/100
- Stocks Above 50-day MA: 74/100
- Stocks Above 200-day MA: 71/100
- Breadth Thrust: 65/100
- Distribution Days: 70/100

Interpretation: Breadth is healthy with good participation across most components.
Market rally is broad-based. Risk: on if breadth holds above 60.
```

## What It Does NOT Do

- Does NOT provide individual stock recommendations
- Does NOT predict future market movements (it's a current-state assessment)
- Does NOT replace comprehensive market analysis (use alongside other tools)
- Does NOT track sector-specific breadth (market-wide only)
- Does NOT work with real-time tick data (daily resolution only)

## Requirements

- Python 3.8+
- pandas, requests
- No API keys required
- Internet connection to fetch CSV data

## Data Source

Uses TraderMonty's public breadth data (updated regularly):
- Detail CSV: ~2,500 rows of historical breadth metrics
- Summary CSV: 8 current market metrics

## License

MIT
