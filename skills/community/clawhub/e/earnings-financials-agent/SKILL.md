---
name: earnings-financials-agent
description: An autonomous agent for monitoring corporate earnings and analyzing financial statements using yfinance.
version: 1.0.3
author: assix
keywords:
  - earnings
  - financials
  - stocks
  - investment-assistant
  - alpha
  - finance-agent
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - pip
---

# EarningsFinancialsAgent

This agent provides deep-dive analysis into quarterly earnings and corporate financial health. It is designed to run locally and uses the `yfinance` library for reliable, real-time data retrieval.

## Setup
Before using this skill, ensure the dependencies are installed in your environment:
```bash
pip install yfinance
```

## User Instructions
The agent can handle a variety of financial inquiries. Use these as templates for your requests:

* **Earnings Performance:** "Summarize the latest earnings for NVDA and check if they beat revenue estimates."
* **Direct Comparison:** "Compare the net income of Google vs Meta for the last 4 quarters."
* **Financial Ratios:** "What is the debt-to-equity ratio and quick ratio for TSLA?"
* **Cash Flow Analysis:** "Give me a summary of Amazon's cash flow from the most recent report."
* **Growth Trends:** "Show me the revenue growth trend for Netflix over the last year."
* **Calendar Checks:** "Is Broadcom reporting earnings this week? If so, when?"
* **Profitability:** "Analyze the profit margins for AMD based on their latest financials."
* **Dividend Health:** "Check the dividend payout ratio for Coca-Cola to see if it's sustainable."

## Tools

### `get_earnings`
Fetches the most recent earnings results and compares them to analyst estimates.
- **Inputs:** `ticker` (string)
- **Call:** `python3 logic.py --tool get_earnings --ticker {{ticker}}`

### `get_financials`
Retrieves key balance sheet, income statement, and cash flow metrics.
- **Inputs:** `ticker` (string)
- **Call:** `python3 logic.py --tool get_financials --ticker {{ticker}}`
