---
name: customs-overview-trend
description: "Query import/export trade trend data — retrieve monthly trade volume trends within a specified time range, with cursor-based pagination.\n\nTrigger: trade trend, import export trend, monthly trade volume, trade time series, trade date range query"
metadata: {"version":"1.0.1","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"📈","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# Customs Overview Trend

Query import/export trade trend data from customs data using the UpKuaJing Open Platform API.

## Overview

This skill provides monthly import/export trade volume trend data from UpKuaJing's customs database. Given a time range (start and end months), it returns a paginated list of monthly trade totals, allowing you to analyze trade patterns and seasonal trends.

## Running Scripts

### Environment Setup

1. **Check Python**: `python --version`
2. **Install dependencies**: `pip install -r requirements.txt`

Script directory: `scripts/*.py`
Run example: `python scripts/*.py`

**Important**: Always use direct script invocation like `python scripts/customs_overview_trend.py`. **Do NOT use** shell compound commands like `cd scripts && python customs_overview_trend.py`

### Trend Query (`customs_overview_trend.py`)
- **Return granularity**: One record per month
- **Use cases**: Analyze trade trends over time, identify seasonal patterns, compare month-over-month trade volumes
- **Examples**:
  - "Show trade trend from China to US from Jan to Dec 2025"
  - "Get monthly trade volume between CN and US in 2025"
- **Parameters**: See [Trend API](references/customs-overview-trend-api.md)

## API Key and Top-up

This skill requires an API key. The API key is stored in the `~/.upkuajing/.env` file:
```bash
cat ~/.upkuajing/.env
```
**Example file content**:
```
UPKUAJING_API_KEY=your_api_key_here
```
### **API Key Not Set**
First check if the `~/.upkuajing/.env` file has UPKUAJING_API_KEY;
If UPKUAJING_API_KEY is not set, prompt the user to choose:
1. User has one: User provides it (manually add to ~/.upkuajing/.env file)
2. User doesn't have one: You can apply using the interface (`auth.py --new_key`), the new key will be automatically saved to ~/.upkuajing/.env
Wait for user selection;

### **Account Top-up**
When API response indicates insufficient balance, explain and guide user to top up:
1. Create top-up order (`auth.py --new_rec_order`)
2. Based on order response, send payment page URL to user, guide user to open URL and pay, user confirms after successful payment;

### **Get Account Information**
Use this script to get account information for UPKUAJING_API_KEY: `auth.py --account_info`

## API Key and UpKuaJing Account
- Newly applied API key: Register and login at [UpKuaJing Open Platform](https://developer.upkuajing.com/), then bind account

### **Report Skill Call Errors**
When an API call fails or returns abnormal data (server error, timeout, malformed response, etc.), explain the anomaly to the user in natural language and ask whether to report it to the platform for troubleshooting. Only run the report after user confirmation:
```bash
python scripts/error_report.py --params '{"requestPath":"/agent/customs/overview/trend","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"Trade trend query failed with a server error"}'
```
- Do not report normal business conditions (insufficient balance, invalid API key, parameter errors) — handle them via their own flows
- Error reporting does not incur query fees
- **Parameters**: See [Error Report API](references/skill-error-report-api.md)

## Fees

**All API calls incur fees**, different interfaces have different billing methods.

**Latest pricing**: Users can visit [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
Or use: `python scripts/auth.py --price_info` (returns complete pricing for all interfaces)

### Query Billing Rules

Billed by **number of calls**, each call returns one page of trend data:
- Each API call incurs a fee
- **Before execution:**
  1. Inform user that this query will incur a fee
  2. Stop, wait for explicit user confirmation in a separate message, then execute script

### Fee Confirmation Principle

**Any operation that incurs fees must first inform and wait for explicit user confirmation. Do not execute in the same message as the notification.**

## Workflow

### Decision Guide

| User Intent | Use API |
|-------------|---------|
| "Show monthly trade trend from China to US in 2025" | Trend Query |
| "Get trade volume for each month between CN and US" | Trend Query |
| "Compare trade volumes month over month" | Trend Query |

## Usage Examples

### Query Trade Trend

**User request**: "Show trade trend from China to US from Jan to Dec 2025"
```bash
python scripts/customs_overview_trend.py --params '{"originCountryCode":"CN","arrivalCountryCode":"US","startDate":202501,"endDate":202512}'
```

**Query the next page**:
```bash
python scripts/customs_overview_trend.py --params '{"originCountryCode":"CN","arrivalCountryCode":"US","startDate":202501,"endDate":202512,"cursor":"eyJzdGFydCI6MH0="}'
```

**Query for a specific quarter**:
```bash
python scripts/customs_overview_trend.py --params '{"originCountryCode":"CN","arrivalCountryCode":"US","startDate":202501,"endDate":202503}'
```

## Error Handling

- **API key invalid/non-existent**: Check `UPKUAJING_API_KEY` in `~/.upkuajing/.env` file
- **Insufficient balance**: Guide user to top up
- **Invalid parameters**: **Must first check the corresponding API documentation in references/ directory**, get correct parameter names and formats from documentation, do not guess
- **Skill call errors / abnormal responses**: Explain to the user and, with user confirmation, report to the platform via `python scripts/error_report.py` (see [Report Skill Call Errors](#report-skill-call-errors))

### API Documentation Reference

- Trend: Check [references/customs-overview-trend-api.md](references/customs-overview-trend-api.md)
- Error Report: Check [references/skill-error-report-api.md](references/skill-error-report-api.md)

## Best Practices

1. **Check API documentation**:
   - **Before executing queries, must first check the corresponding API reference documentation**
   - Check [references/customs-overview-trend-api.md](references/customs-overview-trend-api.md)
   - Do not guess parameter names, get accurate parameter names and formats from documentation

2. **Date format**:
   - Use 6-digit year-month format (e.g., 202501 for January 2025)
   - `startDate` and `endDate` are both required

3. **Pagination**:
   - Use the `cursor` parameter from the response to fetch the next page
   - If no `cursor` is returned, there are no more pages

4. **Cross-skill usage**:
   - Use **customs-overview-summary** for high-level annual figures, then this skill for monthly breakdown
   - Combine with **customs-company-trends** for company-level trend analysis

## Notes
- `startDate` and `endDate` are both required parameters
- `tradeDate` in the response is in year-month format (e.g., 202501)
- `tradeTotal` is the total trade volume for that month
- File paths use forward slashes on all platforms
- **Prohibit outputting technical parameter format**: Do not display code-style parameters in responses, convert to natural language
- **Do not** estimate or guess per-call fees — use `python scripts/auth.py --price_info` to get accurate pricing information
- **Do not** guess parameter names, get accurate parameter names and formats from documentation

## Related Skills

Other UpKuaJing skills you might find useful:

- customs-overview-summary — Query trade overview summary (aggregated)
- customs-overview-trade-list — Query country trade list with paginated breakdown
- customs-overview-top-n — Query top N suppliers or buyers
- customs-overview-us-import — Query US import transaction statistics
- customs-overview-date — Query date reference information
- customs-company-stats — Query company basic trade statistics
- customs-company-trends — Query company trade trends (monthly breakdown)
- customs-company-partner-stats — Query company trade partner distribution
- customs-company-area-stats — Query company trade area statistics (aggregated)
- upkuajing-customs-trade-company-search — Search customs trade companies