# SKILL.md - Find Profitable Stocks (自由现金流掘金)

## Description
Find truly profitable companies using **Free Cash Flow (FCF)** and fundamental analysis strategy.

**Free Cash Flow = Operating Cash Flow - Capital Expenditure**

This skill screens for companies that generate real cash profit, not just accounting earnings.

## When to Use
- User asks "find profitable stocks"
- User asks "free cash flow analysis"
- User asks "真正的赚钱公司" / "现金流好的股票"
- User asks "筛选优质股票"
- User wants to analyze a specific stock's cash flow quality

## How It Works
1. Fetches financial data from public APIs (East Money / Sina / Tencent)
2. Calculates health scores based on:
   - Valuation (PE/PB)
   - Profitability (ROE, profit margin)
   - Growth (revenue/profit growth)
   - Technical (price action, volume)
3. Ranks and outputs results

## Usage

### Analyze a single stock
```
分析 600938 的基本面
筛选 股票 159201
```

### Screen for profitable stocks
```
筛选自由现金流好的股票
找真正赚钱的公司
帮我选几只优质股票
```

### Compare multiple stocks
```
对比 600938 和 600519
```

## Output Format
Returns:
- Health Score (0-100)
- Grade (A/B/C/D)
- Key metrics (PE, ROE, growth, etc.)
- Analysis summary

## Data Sources
- **Primary**: East Money API (push2.eastmoney.com)
- **Fallback**: Demo/Mock data (when network unavailable)
- **Note**: Requires internet access for real-time data

## Requirements
- Python 3.x
- requests package
- Internet connection

## Status
**Ready for use** - Network dependent (will show demo data if offline)
