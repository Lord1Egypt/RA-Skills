# SKILL: stock-checker

## Description

Fetches the current stock price for a given ticker symbol using free public APIs. Returns the price in USD along with daily change data. No API key required.

## Usage

Use when you need to check a stock price, compare current values, or get a quick market snapshot for a ticker.

**Triggers:** "What's the price of AAPL?", "Check stock price for TSLA", "Get me a quote on MSFT"

## Inputs

| Parameter | Required | Type | Default | Description |
|-----------|----------|------|---------|-------------|
| `ticker` | Yes | string | — | Stock ticker symbol (e.g., `AAPL`, `TSLA`, `GOOGL`). Must be 1-5 uppercase alpha characters. |

## Outputs

Structured text response:

```
**<TICKER>** — $<price> USD
Change: <+/->$<amount> (<+/-><%>)
Volume: <volume>
As of: <timestamp>
```

## Steps

1. **Validate input** — Confirm `ticker` is 1-5 alphabetic characters. Convert to uppercase if needed. If invalid, return: "Invalid ticker symbol. Please provide 1-5 letters (e.g., AAPL)."

2. **Fetch stock data** — Use WebFetch to call:
   ```
   https://query1.finance.yahoo.com/v8/finance/chart/<TICKER>?range=1d&interval=1d
   ```

3. **Check response** — If the response contains an error or the result array is empty:
   - Return: "Could not find data for ticker '<TICKER>'. Verify the symbol and try again."

4. **Extract price data** from the JSON response:
   - `price`: `chart.result[0].meta.regularMarketPrice`
   - `previousClose`: `chart.result[0].meta.chartPreviousClose`
   - `volume`: `chart.result[0].meta.regularMarketVolume`
   - Calculate `change = price - previousClose`
   - Calculate `changePercent = (change / previousClose) * 100`

5. **Format and return**:
   ```
   **<TICKER>** — $<price> USD
   Change: <+/->$<change> (<+/-><%changePercent>)
   Volume: <volume>
   As of: <current timestamp>
   ```

## Error Handling

| Scenario | Action |
|----------|--------|
| Invalid ticker format | Return validation error with format hint |
| API unreachable / timeout | Return: "Unable to reach market data API. Try again shortly." |
| Ticker not found | Return: "No data found for '<TICKER>'. Check the symbol." |
| Market closed / stale data | Still return last known price, note "Market closed" in output |
