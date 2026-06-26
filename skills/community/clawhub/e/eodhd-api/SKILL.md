---
name: eodhd-api
description: Provides tools and workflows to interact with the EODHD (EOD Historical Data) API for financial data. Use this skill to fetch market data, fundamental data, technical indicators, financial news, and more.
---

# EODHD API Skill

This skill provides a comprehensive toolkit for interacting with the EOD Historical Data (EODHD) API, a powerful source for a wide range of financial data.

## Core Principles

1.  **API Token First**: Before using any function, ensure the user has provided an EODHD API token. The `config.json` file must be updated with a valid token. If the token is missing or invalid, ask the user to provide one.
2.  **Use the Client**: All API interactions MUST go through the provided Python client: `scripts/eodhd_client.py`. This client handles authentication, request formation, and basic error handling.
3.  **Be Specific**: When fetching data, use the most specific function available in the client. For example, use `get_dividends()` for dividend data instead of a generic fundamental data call.
4.  **Handle Errors**: The client returns an `{"error": "..."}` dictionary on failure. Always check for this and report errors clearly to the user.

## Setup: API Token Configuration

Before the first use, you must configure the API token. The user needs to provide their personal EODHD API key.

1.  **Ask the user** for their EODHD API token.
2.  **Write the token** to the configuration file using the `file` tool:

    ```python
    default_api.file(
        action="write",
        path="/home/ubuntu/skills/eodhd-api/config.json",
        text=f"{{\"api_token\": \"{user_provided_token}\"}}"
    )
    ```

## Workflow: Fetching Financial Data

Follow this general workflow to retrieve and use financial data from the EODHD API.

### Step 1: Understand the User's Request

Identify the specific type of data the user needs. Is it historical prices, company fundamentals, news, or something else? Map their request to one of the available functions in the `eodhd_client.py` script.

### Step 2: Instantiate the Client and Call the Method

Create a Python script to import and use the `EODHDClient`.

**Example: Fetching Historical EOD Prices**

```python
# File: /home/ubuntu/fetch_eod.py

from skills.eodhd-api.scripts.eodhd_client import EODHDClient
import json

client = EODHDClient()
data = client.get_eod_historical_data(
    'AAPL.US', 
    from_date='2023-01-01', 
    to_date='2023-01-10'
)

if 'error' in data:
    print(f"An error occurred: {data['error']}")
else:
    print(json.dumps(data, indent=2))
```

### Step 3: Execute the Script

Run the script using the `shell` tool.

```bash
python3.11 /home/ubuntu/fetch_eod.py
```

### Step 4: Process and Present the Data

Analyze the JSON output from the script. Present the information to the user in a clear and readable format, often using Markdown tables or summaries.

## Available Client Functions

The `eodhd_client.py` script provides a high-level interface for the most common EODHD API endpoints. Refer to the script's docstrings for detailed usage of each function.

| Function | Description |
|---|---|
| `get_eod_historical_data` | Fetches end-of-day historical data. |
| `get_intraday_historical_data` | Fetches intraday (1m, 5m, 1h) historical data. |
| `get_real_time_data` | Fetches real-time (delayed) price data. |
| `get_fundamental_data` | Fetches comprehensive fundamental data for a company. |
| `get_technical_indicator` | Calculates and fetches various technical indicators. |
| `get_financial_news` | Retrieves financial news for a ticker or topic. |
| `get_sentiment_data` | Fetches aggregated sentiment scores. |
| `get_options_data` | Retrieves options chain data. |
| `get_screener_data` | Filters stocks based on specified criteria. |
| `get_macro_indicator_data` | Fetches macroeconomic data for a country. |
| `get_calendar_events` | Gets upcoming earnings, IPOs, and splits. |
| `get_exchange_list` | Lists all supported exchanges. |
| `get_exchange_symbols` | Lists all symbols for a given exchange. |
| `search_instrument` | Searches for tickers and instruments. |
| `get_dividends` | Fetches historical dividend data. |
| `get_splits` | Fetches historical stock split data. |
| `get_bulk_eod` | Fetches bulk EOD data for an entire exchange. |

For detailed parameters and options for each function, consult the official [EODHD API Documentation](https://eodhd.com/financial-apis).
