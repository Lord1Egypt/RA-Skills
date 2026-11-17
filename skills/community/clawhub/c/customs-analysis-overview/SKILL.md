---
name: customs-analysis-overview
description: "Query analysis report overview data — retrieve supplier/buyer counts by country with cursor-based pagination.\n\nTrigger: analysis overview, country statistics, supplier buyer counts, trade overview by country, report overview"
metadata: {"version":"1.0.1","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"📋","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# Customs Analysis Overview

Query analysis report overview data from customs data using the UpKuaJing Open Platform API.

## Overview

This skill provides aggregated overview data from UpKuaJing's customs analysis report. It returns supplier and buyer counts grouped by country, allowing you to understand trade activity distribution across different countries.

## Running Scripts

### Environment Setup

1. **Check Python**: `python --version`
2. **Install dependencies**: `pip install -r requirements.txt`

Script directory: `scripts/*.py`
Run example: `python scripts/*.py`

**Important**: Always use direct script invocation like `python scripts/customs_analysis_overview.py`. **Do NOT use** shell compound commands like `cd scripts && python customs_analysis_overview.py`

### Overview Query (`customs_analysis_overview.py`)
- **Return granularity**: One record per country
- **Use cases**: Get overview of supplier and buyer counts by country, understand trade activity distribution, find active trade countries
- **Examples**:
  - "Show analysis overview of supplier and buyer counts by country"
  - "Get the overview data for trade activity distribution"
- **Parameters**: See [Overview API](references/customs-analysis-overview-api.md)

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
python scripts/error_report.py --params '{"requestPath":"/agent/customs/analysis/overview","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"Overview query failed with a server error"}'
```
- Do not report normal business conditions (insufficient balance, invalid API key, parameter errors) — handle them via their own flows
- Error reporting does not incur query fees
- **Parameters**: See [Error Report API](references/skill-error-report-api.md)

## Fees

**All API calls incur fees**, different interfaces have different billing methods.

**Latest pricing**: Users can visit [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
Or use: `python scripts/auth.py --price_info` (returns complete pricing for all interfaces)

### Query Billing Rules

Billed by **number of calls**, each call returns one page of overview data:
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
| "Show supplier and buyer counts by country" | Overview Query |
| "Get analysis report overview data" | Overview Query |
| "What countries have the most trade activity" | Overview Query |

## Usage Examples

### Query Overview

**User request**: "Show analysis overview of supplier and buyer counts by country"
```bash
python scripts/customs_analysis_overview.py --params '{}'
```

**Query the next page**:
```bash
python scripts/customs_analysis_overview.py --params '{"cursor":"eyJpZCI6MX0="}'
```

## Error Handling

- **API key invalid/non-existent**: Check `UPKUAJING_API_KEY` in `~/.upkuajing/.env` file
- **Insufficient balance**: Guide user to top up
- **Invalid parameters**: **Must first check the corresponding API documentation in references/ directory**, get correct parameter names and formats from documentation, do not guess
- **Skill call errors / abnormal responses**: Explain to the user and, with user confirmation, report to the platform via `python scripts/error_report.py` (see [Report Skill Call Errors](#report-skill-call-errors))

### API Documentation Reference

- Overview: Check [references/customs-analysis-overview-api.md](references/customs-analysis-overview-api.md)
- Error Report: Check [references/skill-error-report-api.md](references/skill-error-report-api.md)

## Best Practices

1. **Check API documentation**:
   - **Before executing queries, must first check the corresponding API reference documentation**
   - Check [references/customs-analysis-overview-api.md](references/customs-analysis-overview-api.md)
   - Do not guess parameter names, get accurate parameter names and formats from documentation

2. **Pagination**:
   - Use the `cursor` parameter from the response to fetch the next page
   - If no `cursor` is returned, there are no more pages

3. **Country codes**:
   - Response uses ISO 3166-1 alpha-2 country codes (e.g., "US" for United States)

4. **Cross-skill usage**:
   - Use this skill to get an overview, then drill down with **customs-analysis-hscode-search** to find specific HS codes
   - Combine with **customs-overview-summary** for detailed trade summary between countries

## Notes
- `cursor` is optional — omit to get the first page
- `countSeller` is the number of distinct suppliers
- `countBuyer` is the number of distinct buyers
- File paths use forward slashes on all platforms
- **Prohibit outputting technical parameter format**: Do not display code-style parameters in responses, convert to natural language
- **Do not** estimate or guess per-call fees — use `python scripts/auth.py --price_info` to get accurate pricing information
- **Do not** guess parameter names, get accurate parameter names and formats from documentation

## Related Skills

Other UpKuaJing skills you might find useful:

- customs-overview-summary — Query trade overview summary (aggregated)
- customs-overview-trend — Query import/export trade trends by month
- customs-overview-trade-list — Query country trade list with paginated breakdown
- customs-overview-top-n — Query top N suppliers or buyers
- customs-company-stats — Query company basic trade statistics
- customs-company-trends — Query company trade trends (monthly breakdown)
- customs-company-area-stats — Query company trade area statistics (aggregated)
- customs-company-product-list — Query company product list
- customs-company-hscode-list — Query company HS code list
- upkuajing-customs-trade-company-search — Search customs trade companies