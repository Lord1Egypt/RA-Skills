---
name: customs-overview-us-import
description: "Query US import transaction statistics — retrieve import records, container counts, and last-90-day data grouped by state or city, with cursor-based pagination.\n\nTrigger: US import stats, US import by state, US import by city, American import records, US container import data"
metadata: {"version":"1.0.1","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"🚢","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# Customs Overview US Import

Query US import transaction statistics using the UpKuaJing Open Platform API.

## Overview

This skill provides US import transaction statistics from UpKuaJing's customs database. You can query import data grouped by state or city, including total import records, container counts, and recent 90-day activity data.

## Running Scripts

### Environment Setup

1. **Check Python**: `python --version`
2. **Install dependencies**: `pip install -r requirements.txt`

Script directory: `scripts/*.py`
Run example: `python scripts/*.py`

**Important**: Always use direct script invocation like `python scripts/customs_overview_us_import.py`. **Do NOT use** shell compound commands like `cd scripts && python customs_overview_us_import.py`

### US Import Query (`customs_overview_us_import.py`)
- **Return granularity**: One record per state or city
- **Use cases**: Analyze US import distribution by state or city, monitor recent import activity, understand container traffic patterns
- **Examples**:
  - "Show US import statistics by state"
  - "Get US import data grouped by city"
- **Parameters**: See [US Import API](references/customs-overview-us-import-api.md)

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
python scripts/error_report.py --params '{"requestPath":"/agent/customs/overview/us-import","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"US import query failed with a server error"}'
```
- Do not report normal business conditions (insufficient balance, invalid API key, parameter errors) — handle them via their own flows
- Error reporting does not incur query fees
- **Parameters**: See [Error Report API](references/skill-error-report-api.md)

## Fees

**All API calls incur fees**, different interfaces have different billing methods.

**Latest pricing**: Users can visit [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
Or use: `python scripts/auth.py --price_info` (returns complete pricing for all interfaces)

### Query Billing Rules

Billed by **number of calls**, each call returns one page of US import statistics:
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
| "Show US import statistics by state" | US Import Query (type=state) |
| "Get US import data grouped by city" | US Import Query (type=city) |
| "Which US cities have the most import activity" | US Import Query (type=city) |

## Usage Examples

### Query US Import Statistics

**User request**: "Show US import statistics by state"
```bash
python scripts/customs_overview_us_import.py --params '{"type":"state"}'
```

**Query by city**:
```bash
python scripts/customs_overview_us_import.py --params '{"type":"city"}'
```

**Query the next page**:
```bash
python scripts/customs_overview_us_import.py --params '{"type":"state","cursor":"eyJzdGFydCI6MH0="}'
```

## Error Handling

- **API key invalid/non-existent**: Check `UPKUAJING_API_KEY` in `~/.upkuajing/.env` file
- **Insufficient balance**: Guide user to top up
- **Invalid parameters**: **Must first check the corresponding API documentation in references/ directory**, get correct parameter names and formats from documentation, do not guess
- **Skill call errors / abnormal responses**: Explain to the user and, with user confirmation, report to the platform via `python scripts/error_report.py` (see [Report Skill Call Errors](#report-skill-call-errors))

### API Documentation Reference

- US Import: Check [references/customs-overview-us-import-api.md](references/customs-overview-us-import-api.md)
- Error Report: Check [references/skill-error-report-api.md](references/skill-error-report-api.md)

## Best Practices

1. **Check API documentation**:
   - **Before executing queries, must first check the corresponding API reference documentation**
   - Check [references/customs-overview-us-import-api.md](references/customs-overview-us-import-api.md)
   - Do not guess parameter names, get accurate parameter names and formats from documentation

2. **Query type**:
   - `type=state` groups results by US state (e.g., "California")
   - `type=city` groups results by US city
   - `type` is the only required parameter

3. **Data fields**:
   - `records` is the total number of import records
   - `recordsLast90Days` shows recent import activity
   - `containers` is the total container count
   - `containersLast90Days` shows recent container activity

4. **Pagination**:
   - Use the `cursor` parameter from the response to fetch the next page
   - If no `cursor` is returned, there are no more pages

5. **Cross-skill usage**:
   - Use **customs-overview-summary** for overall trade volume, then this skill for US-specific breakdown
   - Results can complement **customs-company-port-list** for port-level analysis

## Notes
- `type` is the only required parameter
- `name` in the response contains the state or city name
- The 90-day data fields help identify recent trade activity trends
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
- customs-overview-date — Query date reference information
- customs-company-stats — Query company basic trade statistics
- customs-company-trends — Query company trade trends (monthly breakdown)
- customs-company-port-list — Query company trade port list
- customs-company-area-stats — Query company trade area statistics (aggregated)
- upkuajing-customs-trade-company-search — Search customs trade companies