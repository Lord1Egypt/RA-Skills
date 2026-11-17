---
name: customs-company-area-stats
description: "Query company customs trade statistics by region dimension — analyze trade volume, amount, monthly trends, and country distribution across global markets.\n\nTrigger: customs trade area statistics, regional trade analysis, company import-export country distribution, global trade intelligence, supplier market coverage"
metadata: {"version":"1.0.1","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"🌍","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# Customs Company Area Trade Statistics

Query company trade statistics aggregated by region/country dimension from customs data using the UpKuaJing Open Platform API.

## Overview

This skill provides access to company trade statistics by region dimension from UpKuaJing's customs database. Given a company ID and company type, it returns the trade summary broken down by region, including total trade count, amount, quantity, weight, monthly trade trends, and country distribution.

## Running Scripts

### Environment Setup

1. **Check Python**: `python --version`
2. **Install dependencies**: `pip install -r requirements.txt`

Script directory: `scripts/*.py`
Run example: `python scripts/*.py`

**Important**: Always use direct script invocation like `python scripts/customs_company_area_stats.py`. **Do NOT use** shell compound commands like `cd scripts && python customs_company_area_stats.py`

### Company Area Trade Statistics Query (`customs_company_area_stats.py`)
- **Return granularity**: One record per company, containing region-dimension aggregated trade statistics
- **Use cases**: View a company's trade distribution by country/region, analyze market coverage and regional trade volume
- **Examples**:
  - "Get area trade statistics for company 100001 as a supplier"
  - "Query regional trade distribution for company 100001 as a buyer"
- **Parameters**: See [Company Area Trade Statistics API](references/customs-company-area-stats-api.md)

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
python scripts/error_report.py --params '{"requestPath":"/agent/customs/company/area/stats","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"Company area stats query failed with a server error"}'
```
- Do not report normal business conditions (insufficient balance, invalid API key, parameter errors) — handle them via their own flows
- Error reporting does not incur query fees
- **Parameters**: See [Error Report API](references/skill-error-report-api.md)

## Fees

**All API calls incur fees**, different interfaces have different billing methods.

**Latest pricing**: Users can visit [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
Or use: `python scripts/auth.py --price_info` (returns complete pricing for all interfaces)

### Query Billing Rules

Billed by **number of calls**, each call returns area statistics for one company:
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
| "Get area trade statistics for company 100001 as a supplier" | Company Area Trade Statistics Query |
| "Show country distribution of trade for company 100001" | Company Area Trade Statistics Query |

## Usage Examples

### Query Company Area Trade Statistics

**User request**: "Get area trade statistics for company 100001 as a supplier"
```bash
python scripts/customs_company_area_stats.py --params '{"companyId":100001,"companyType":1}'
```

**Query with date range and filters**:
```bash
python scripts/customs_company_area_stats.py --params '{"companyId":100001,"companyType":1,"dateStart":1700000000000,"dateEnd":1735689599999,"countryCodes":["US","KR"]}'
```

## Error Handling

- **API key invalid/non-existent**: Check `UPKUAJING_API_KEY` in `~/.upkuajing/.env` file
- **Insufficient balance**: Guide user to top up
- **Invalid parameters**: **Must first check the corresponding API documentation in references/ directory**, get correct parameter names and formats from documentation, do not guess
- **Skill call errors / abnormal responses**: Explain to the user and, with user confirmation, report to the platform via `python scripts/error_report.py` (see [Report Skill Call Errors](#report-skill-call-errors))

### API Documentation Reference

- Company Area Trade Statistics: Check [references/customs-company-area-stats-api.md](references/customs-company-area-stats-api.md)
- Error Report: Check [references/skill-error-report-api.md](references/skill-error-report-api.md)

## Best Practices

1. **Check API documentation**:
   - **Before executing queries, must first check the corresponding API reference documentation**
   - Check [references/customs-company-area-stats-api.md](references/customs-company-area-stats-api.md)
   - Do not guess parameter names, get accurate parameter names and formats from documentation

2. **Data interpretation**:
   - `countTrade` is the total number of trade transactions
   - `tradeDates` shows monthly active trading months
   - `tradeCountries` shows country-level distribution with percentage
   - `percentTrade` is the percentage of trade (as a decimal, e.g., 21.05 means 21.05%)

3. **Cross-skill usage**:
   - The company ID from results can be used with **customs-company-area-list** to get detailed area breakdown
   - The company ID can also be used with **customs-company-trends** to get monthly trade trends

## Notes
- `companyType` determines the company's role (1=supplier, 2=buyer)
- `month` is a millisecond timestamp, while `monthText` provides a human-readable string (e.g., "2024-01")
- File paths use forward slashes on all platforms
- **Prohibit outputting technical parameter format**: Do not display code-style parameters in responses, convert to natural language
- **Do not** estimate or guess per-call fees — use `python scripts/auth.py --price_info` to get accurate pricing information
- **Do not** guess parameter names, get accurate parameter names and formats from documentation

## Related Skills

Other UpKuaJing skills you might find useful:

- customs-company-area-list — Query company trade area list
- customs-company-hscode-stats — Query company trade HS code statistics
- customs-company-hscode-list — Query company trade HS code list
- customs-company-product-list — Query company trade product list
- customs-company-port-list — Query company trade port list
- customs-company-stats — Query company basic trade statistics
- customs-company-trends — Query company trade trends (monthly breakdown)
- customs-company-partner-stats — Query company trade partner distribution
- upkuajing-customs-trade-company-search — Search customs trade companies
- upkuajing-global-company-people-search — Unified company and people search across all sources