# Financial Report Tracker API Reference

## yfinance Core Methods

### Ticker Object

```python
import yfinance as yf
ticker = yf.Ticker("AAPL")
```

### Key Properties and Methods

| Method/Property | Description | Return Type |
|-----------------|-------------|-------------|
| `.info` | Company basic information, valuation, ratings | dict |
| `.calendar` | Earnings calendar | DataFrame |
| `.financials` | Quarterly/Annual financial data | DataFrame |
| `.quarterly_financials` | Quarterly financial data | DataFrame |
| `.earnings` | Historical earnings data | DataFrame |
| `.earnings_dates` | Historical earnings dates | DataFrame |
| `.recommendations` | Analyst recommendations | DataFrame |
| `.splits` | Stock split records | DataFrame |
| `.dividends` | Dividend records | Series |

### Key info Fields

| Field | Description |
|-------|-------------|
| `shortName` | Company short name |
| `longName` | Company full name |
| `marketCap` | Market capitalization |
| `currentPrice` | Current stock price |
| `forwardEps` | Forward EPS |
| `trailingEps` | Trailing EPS |
| `trailingPE` | P/E Ratio (Trailing) |
| `forwardPE` | P/E Ratio (Forward) |
| `profitMargins` | Net profit margin |
| `operatingMargins` | Operating margin |
| `grossMargins` | Gross margin |
| `revenueGrowth` | Revenue growth rate |
| `earningsGrowth` | Earnings growth rate |
| `returnOnEquity` | Return on equity (ROE) |
| `targetMeanPrice` | Analyst mean target price |
| `recommendationKey` | Analyst consensus rating |
| `numberOfAnalystOpinions` | Number of analyst opinions |
| `fiftyTwoWeekHigh` | 52-week high |
| `fiftyTwoWeekLow` | 52-week low |
| `debtToEquity` | Debt-to-equity ratio |
| `currentRatio` | Current ratio |

## Data Retrieval Examples

### Get Earnings Calendar

```python
ticker = yf.Ticker("AAPL")
next_earnings = ticker.info.get('earningsNextGrossProfit')
calendar = ticker.calendar
```

### Get Financial Data

```python
# Quarterly financials
quarterly = ticker.quarterly_financials
# Annual financials
annual = ticker.financials
# Earnings history
earnings = ticker.earnings
```

### Get Analyst Data

```python
recommendations = ticker.recommendations
earnings_dates = ticker.earnings_dates
```

## Error Handling

```python
try:
    ticker = yf.Ticker(symbol)
    info = ticker.info
    if 'regularMarketPrice' not in info:
        raise ValueError(f"Ticker symbol {symbol} does not exist")
except Exception as e:
    print(f"Data retrieval failed: {e}")
```

## Notes

1. **Data Latency**: yfinance data typically has a 15-20 minute delay
2. **Rate Limiting**: Avoid large numbers of requests in a short period; may be throttled
3. **Data Completeness**: Some small-cap stocks may have incomplete data
4. **Timezone Handling**: Earnings dates are typically in U.S. Eastern Time