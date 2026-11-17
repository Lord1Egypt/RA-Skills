---
name: customs-analysis-trade-percent
description: "Query trade percentage analysis — retrieve company-level trade share data for a specified HS code.\n\nTrigger: trade percentage, company trade share, market share, HS code company breakdown, trade distribution by company"
metadata: {"version":"1.0.1","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"📊","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# Customs Analysis Trade Percent

Query trade percentage data from customs data using the UpKuaJing Open Platform API.

## Overview

This skill provides company-level trade percentage data for a specified HS code. Given an HS code, country type (exporter/importer), and recent months, it returns a ranked list of companies with their trade counts, percentages, quantities, amounts, and partner counts.

## Running Scripts

### Environment Setup

1. **Check Python**: `python --version`
2. **Install dependencies**: `pip install -r requirements.txt`

Script directory: `scripts/*.py`
Run example: `python scripts/*.py`

**Important**: Always use direct script invocation like `python scripts/customs_analysis_trade_percent.py`. **Do NOT use** shell compound commands like `cd scripts && python customs_analysis_trade_percent.py`

### Trade Percent Query (`customs_analysis_trade_percent.py`)
- **Return granularity**: One record per company, ranked by trade share
- **Use cases**: Identify major companies trading a specific product, analyze market concentration, find trade partners
- **Examples**:
  - "Show company trade share for HS code 04021000"
  - "Which companies export product 04021000 the most?"
  - "What is the market concentration for product 04021000?"
- **Parameters**: See [Trade Percent API](references/customs-analysis-trade-percent-api.md)

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
python scripts/error_report.py --params '{"requestPath":"/agent/customs/analysis/trade-percent","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"Trade percent query failed with a server error"}'
```
- Do not report normal business conditions (insufficient balance, invalid API key, parameter errors) — handle them via their own flows
- Error reporting does not incur query fees
- **Parameters**: See [Error Report API](references/skill-error-report-api.md)

## Fees

**All API calls incur fees**, different interfaces have different billing methods.

**Latest pricing**: Users can visit [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
Or use: `python scripts/auth.py --price_info` (returns complete pricing for all interfaces)

### Query Billing Rules

Billed by **number of calls**, each call returns one page of trade percentage data:
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
| "Show company trade share for HS code 04021000" | Trade Percent Query |
| "Which companies export product 04021000 the most?" | Trade Percent Query |
| "What is the market concentration for product 04021000?" | Trade Percent Query |

## Usage Examples

### Query Trade Percent

**User request**: "Show company trade share for HS code 04021000 in exporting countries over 12 months"
```bash
python scripts/customs_analysis_trade_percent.py --params '{"hscode":"04021000","countryType":1,"recentMonths":12}'
```

**Query importing companies for a specific country**:
```bash
python scripts/customs_analysis_trade_percent.py --params '{"hscode":"04021000","countryCode":"CN","countryType":2,"recentMonths":12}'
```

**Query the next page**:
```bash
python scripts/customs_analysis_trade_percent.py --params '{"hscode":"04021000","countryType":1,"recentMonths":12,"cursor":"eyJpZCI6MX0="}'
```

## Error Handling

- **API key invalid/non-existent**: Check `UPKUAJING_API_KEY` in `~/.upkuajing/.env` file
- **Insufficient balance**: Guide user to top up
- **Invalid parameters**: **Must first check the corresponding API documentation in references/ directory**, get correct parameter names and formats from documentation, do not guess
- **Skill call errors / abnormal responses**: Explain to the user and, with user confirmation, report to the platform via `python scripts/error_report.py` (see [Report Skill Call Errors](#report-skill-call-errors))

### API Documentation Reference

- Trade Percent: Check [references/customs-analysis-trade-percent-api.md](references/customs-analysis-trade-percent-api.md)
- Error Report: Check [references/skill-error-report-api.md](references/skill-error-report-api.md)

## Best Practices

1. **Check API documentation**:
   - **Before executing queries, must first check the corresponding API reference documentation**
   - Check [references/customs-analysis-trade-percent-api.md](references/customs-analysis-trade-percent-api.md)
   - Do not guess parameter names, get accurate parameter names and formats from documentation

2. **Country type**:
   - `countryType=1` means exporting companies (suppliers)
   - `countryType=2` means importing companies (buyers)

3. **Cross-skill usage**:
   - First use **customs-analysis-hscode-search** and **customs-analysis-hscode-detail** to find and understand HS codes
   - Use **customs-analysis-area** for geographic distribution, then this skill for company-level breakdown
   - Found company IDs can be used with **customs-company-stats** or **customs-company-trends** for detailed company analysis

## Notes
- `hscode`, `countryType`, and `recentMonths` are required parameters
- `countryCode` is optional — omit for global company breakdown
- `rn` is the rank number (1 = highest trade share)
- `percentTrade` is the company's trade percentage of total
- File paths use forward slashes on all platforms
- **Prohibit outputting technical parameter format**: Do not display code-style parameters in responses, convert to natural language
- **Do not** estimate or guess per-call fees — use `python scripts/auth.py --price_info` to get accurate pricing information
- **Do not** guess parameter names, get accurate parameter names and formats from documentation

## Related Skills

Other UpKuaJing skills you might find useful:

- customs-analysis-area — Query trade area distribution by HS code
- customs-analysis-trends — Query import/export trade trends by HS code
- customs-analysis-hscode-search — Search HS codes by product name and keywords
- customs-analysis-hscode-detail — Query HS code detail descriptions
- customs-company-stats — Query company basic trade statistics
- customs-company-trends — Query company trade trends (monthly breakdown)
- customs-company-partner-stats — Query company trade partner distribution
- customs-company-product-list — Query company product list
- customs-company-area-stats — Query company trade area statistics (aggregated)
- upkuajing-customs-trade-company-search — Search customs trade companies