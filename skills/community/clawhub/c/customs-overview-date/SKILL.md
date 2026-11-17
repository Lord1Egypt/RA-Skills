---
name: customs-overview-date
description: "Query date reference information — retrieve last year, last month, and same-month-last-year date values for use in trade queries.\n\nTrigger: date reference, last year, last month, same month last year, trade query dates, reference date info"
metadata: {"version":"1.0.1","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"📅","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# Customs Overview Date

Query date reference information using the UpKuaJing Open Platform API.

## Overview

This skill provides date reference values from UpKuaJing's system. It returns last year's year value, last month's year-month value, and the same month from last year. These reference dates are useful when constructing queries for other customs overview skills (summary, trade-list, trend, etc.).

## Running Scripts

### Environment Setup

1. **Check Python**: `python --version`
2. **Install dependencies**: `pip install -r requirements.txt`

Script directory: `scripts/*.py`
Run example: `python scripts/*.py`

**Important**: Always use direct script invocation like `python scripts/customs_overview_date.py`. **Do NOT use** shell compound commands like `cd scripts && python customs_overview_date.py`

### Date Reference Query (`customs_overview_date.py`)
- **Return granularity**: One set of date reference values per query
- **Use cases**: Get reference dates for constructing trade queries, find last year's year value for overview queries, find last month's month value for trend queries
- **Examples**:
  - "What's the last month for trade data"
  - "Get reference dates for customs overview queries"
- **Parameters**: See [Date Reference API](references/customs-overview-date-api.md)

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
python scripts/error_report.py --params '{"requestPath":"/agent/customs/overview/date","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"Date overview query failed with a server error"}'
```
- Do not report normal business conditions (insufficient balance, invalid API key, parameter errors) — handle them via their own flows
- Error reporting does not incur query fees
- **Parameters**: See [Error Report API](references/skill-error-report-api.md)

## Fees

**All API calls incur fees**, different interfaces have different billing methods.

**Latest pricing**: Users can visit [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
Or use: `python scripts/auth.py --price_info` (returns complete pricing for all interfaces)

### Query Billing Rules

Billed by **number of calls**, each call returns one set of date references:
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
| "Get reference dates for customs overview" | Date Reference Query |
| "What year and month values to use for trade queries" | Date Reference Query |
| "Find the last month with available trade data" | Date Reference Query |

## Usage Examples

### Query Date Reference

**User request**: "Get reference dates for customs overview"
```bash
python scripts/customs_overview_date.py --params '{}'
```

The response provides:
- `yesteryear`: Last year's year value (e.g., 2025)
- `lastMonth`: Last month's year-month value (e.g., 202604)
- `yesteryearMonth`: Same month last year (e.g., 202504)

## Error Handling

- **API key invalid/non-existent**: Check `UPKUAJING_API_KEY` in `~/.upkuajing/.env` file
- **Insufficient balance**: Guide user to top up
- **Invalid parameters**: **Must first check the corresponding API documentation in references/ directory**, get correct parameter names and formats from documentation, do not guess
- **Skill call errors / abnormal responses**: Explain to the user and, with user confirmation, report to the platform via `python scripts/error_report.py` (see [Report Skill Call Errors](#report-skill-call-errors))

### API Documentation Reference

- Date Reference: Check [references/customs-overview-date-api.md](references/customs-overview-date-api.md)
- Error Report: Check [references/skill-error-report-api.md](references/skill-error-report-api.md)

## Best Practices

1. **Check API documentation**:
   - **Before executing queries, must first check the corresponding API reference documentation**
   - Check [references/customs-overview-date-api.md](references/customs-overview-date-api.md)
   - Do not guess parameter names, get accurate parameter names and formats from documentation

2. **No business parameters required**:
   - Pass an empty JSON object `{}` as params
   - The API has no business request parameters

3. **Using the results**:
   - Use `yesteryear` for the `year` parameter in **customs-overview-summary**, **customs-overview-trade-list**, and **customs-overview-top-n** queries
   - Use `lastMonth` and `yesteryearMonth` as reference for `startDate`/`endDate` in **customs-overview-trend** queries
   - The date reference values are system-calculated based on the current date

4. **Cross-skill usage**:
   - Use this skill to get the correct date values before making other overview queries
   - Especially useful when users don't specify exact years or months

## Notes
- No business parameters are required — pass an empty JSON object `{}`
- `yesteryear` is the previous calendar year (4-digit)
- `lastMonth` is the previous calendar month (6-digit year-month format)
- `yesteryearMonth` is the same calendar month from the previous year
- File paths use forward slashes on all platforms
- **Prohibit outputting technical parameter format**: Do not display code-style parameters in responses, convert to natural language
- **Do not** estimate or guess per-call fees — use `python scripts/auth.py --price_info` to get accurate pricing information
- **Do not** guess parameter names, get accurate parameter names and formats from documentation

## Related Skills

Other UpKuaJing skills you might find useful:

- customs-overview-summary — Query trade overview summary (aggregated)
- customs-overview-trade-list — Query country trade list with paginated breakdown
- customs-overview-trend — Query import/export trade trends by month
- customs-overview-top-n — Query top N suppliers or buyers
- customs-overview-us-import — Query US import transaction statistics
- customs-company-stats — Query company basic trade statistics
- customs-company-trends — Query company trade trends (monthly breakdown)
- customs-company-partner-stats — Query company trade partner distribution
- customs-company-area-stats — Query company trade area statistics (aggregated)
- upkuajing-customs-trade-company-search — Search customs trade companies