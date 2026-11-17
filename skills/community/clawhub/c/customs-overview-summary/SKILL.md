---
name: customs-overview-summary
description: "Query national trade overview summary data — retrieve annual trade totals, quarterly trade volume, and supplier/buyer counts by country pair.\n\nTrigger: trade overview summary, annual trade statistics, country trade totals, supplier buyer counts, trade volume summary"
metadata: {"version":"1.0.1","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"📊","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# Customs Overview Summary

Query national trade overview summary data from customs data using the UpKuaJing Open Platform API.

## Overview

This skill provides aggregated trade summary data from UpKuaJing's customs database. Given an origin country, arrival country, and year, it returns trade totals, quarterly volume, and counts of suppliers and buyers — a high-level overview of trade activity between country pairs.

## Running Scripts

### Environment Setup

1. **Check Python**: `python --version`
2. **Install dependencies**: `pip install -r requirements.txt`

Script directory: `scripts/*.py`
Run example: `python scripts/*.py`

**Important**: Always use direct script invocation like `python scripts/customs_overview_summary.py`. **Do NOT use** shell compound commands like `cd scripts && python customs_overview_summary.py`

### Overview Summary Query (`customs_overview_summary.py`)
- **Return granularity**: One record per query (aggregated summary for a country pair)
- **Use cases**: Get a high-level trade summary between two countries, understand annual trade volume, compare supplier vs buyer counts
- **Examples**:
  - "Get trade summary between China and US for 2025"
  - "Show annual trade overview from China to US in 2025"
- **Parameters**: See [Overview Summary API](references/customs-overview-summary-api.md)

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
python scripts/error_report.py --params '{"requestPath":"/agent/customs/overview/summary","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"Overview summary query failed with a server error"}'
```
- Do not report normal business conditions (insufficient balance, invalid API key, parameter errors) — handle them via their own flows
- Error reporting does not incur query fees
- **Parameters**: See [Error Report API](references/skill-error-report-api.md)

## Fees

**All API calls incur fees**, different interfaces have different billing methods.

**Latest pricing**: Users can visit [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
Or use: `python scripts/auth.py --price_info` (returns complete pricing for all interfaces)

### Query Billing Rules

Billed by **number of calls**, each call returns one trade overview summary:
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
| "Get trade summary between China and US for 2025" | Overview Summary Query |
| "Show annual trade overview for CN to US in 2025" | Overview Summary Query |
| "How many suppliers and buyers traded between China and US in 2025" | Overview Summary Query |

## Usage Examples

### Query Overview Summary

**User request**: "Get trade summary between China and US for 2025"
```bash
python scripts/customs_overview_summary.py --params '{"originCountryCode":"CN","arrivalCountryCode":"US","year":2025}'
```

**Query without origin country (all origins to US)**:
```bash
python scripts/customs_overview_summary.py --params '{"arrivalCountryCode":"US","year":2025}'
```

**Query without destination country (from CN to all destinations)**:
```bash
python scripts/customs_overview_summary.py --params '{"originCountryCode":"CN","year":2025}'
```

## Error Handling

- **API key invalid/non-existent**: Check `UPKUAJING_API_KEY` in `~/.upkuajing/.env` file
- **Insufficient balance**: Guide user to top up
- **Invalid parameters**: **Must first check the corresponding API documentation in references/ directory**, get correct parameter names and formats from documentation, do not guess
- **Skill call errors / abnormal responses**: Explain to the user and, with user confirmation, report to the platform via `python scripts/error_report.py` (see [Report Skill Call Errors](#report-skill-call-errors))

### API Documentation Reference

- Overview Summary: Check [references/customs-overview-summary-api.md](references/customs-overview-summary-api.md)
- Error Report: Check [references/skill-error-report-api.md](references/skill-error-report-api.md)

## Best Practices

1. **Check API documentation**:
   - **Before executing queries, must first check the corresponding API reference documentation**
   - Check [references/customs-overview-summary-api.md](references/customs-overview-summary-api.md)
   - Do not guess parameter names, get accurate parameter names and formats from documentation

2. **Country codes**:
   - Use ISO 3166-1 alpha-2 country codes (e.g., "CN" for China, "US" for United States)
   - `originCountryCode` is the origin country (exporter's country)
   - `arrivalCountryCode` is the destination country (importer's country)
   - Both are optional parameters — omit one or both to get broader overview

3. **Year format**:
   - Use 4-digit year format (e.g., 2025)

4. **Cross-skill usage**:
   - Use this skill to get a high-level summary, then drill down with **customs-overview-trade-list** for per-country breakdowns or **customs-overview-trend** for monthly trends
   - Country pairs from this skill can be used in **customs-company-stats** for company-level analysis

## Notes
- `year` is the only required parameter
- `tradeTotal` is the annual total trade volume
- `quarterTradeTotal` is the latest quarter's trade volume
- `sellerCount` and `buyerCount` are the number of distinct suppliers and buyers respectively
- File paths use forward slashes on all platforms
- **Prohibit outputting technical parameter format**: Do not display code-style parameters in responses, convert to natural language
- **Do not** estimate or guess per-call fees — use `python scripts/auth.py --price_info` to get accurate pricing information
- **Do not** guess parameter names, get accurate parameter names and formats from documentation

## Related Skills

Other UpKuaJing skills you might find useful:

- customs-overview-trade-list — Query country trade list with paginated breakdown
- customs-overview-trend — Query import/export trade trends by month
- customs-overview-top-n — Query top N suppliers or buyers
- customs-overview-us-import — Query US import transaction statistics
- customs-overview-date — Query date reference information
- customs-company-stats — Query company basic trade statistics
- customs-company-trends — Query company trade trends (monthly breakdown)
- customs-company-partner-stats — Query company trade partner distribution
- customs-company-area-stats — Query company trade area statistics (aggregated)
- upkuajing-customs-trade-company-search — Search customs trade companies