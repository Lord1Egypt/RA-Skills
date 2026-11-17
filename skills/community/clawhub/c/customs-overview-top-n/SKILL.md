---
name: customs-overview-top-n
description: "Query top N suppliers or buyers by trade volume — retrieve ranked lists of suppliers or buyers for a given country pair and year, with cursor-based pagination.\n\nTrigger: top suppliers, top buyers, supplier ranking, buyer ranking, trade volume ranking, company top N"
metadata: {"version":"1.0.1","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"🏆","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# Customs Overview Top N

Query top N suppliers or buyers by trade volume using the UpKuaJing Open Platform API.

## Overview

This skill provides ranked lists of top suppliers or buyers from UpKuaJing's customs database. Given an origin country, arrival country, year, and company type, it returns a paginated list of top companies ranked by trade volume, including quarterly and monthly trade statistics.

## Running Scripts

### Environment Setup

1. **Check Python**: `python --version`
2. **Install dependencies**: `pip install -r requirements.txt`

Script directory: `scripts/*.py`
Run example: `python scripts/*.py`

**Important**: Always use direct script invocation like `python scripts/customs_overview_top_n.py`. **Do NOT use** shell compound commands like `cd scripts && python customs_overview_top_n.py`

### Top N Query (`customs_overview_top_n.py`)
- **Return granularity**: One record per company
- **Use cases**: Find top suppliers or buyers in a trade route, identify key trading partners, analyze market concentration
- **Examples**:
  - "Show top 10 suppliers from China to US in 2025"
  - "List top buyers importing from China to US in 2025"
- **Parameters**: See [Top N API](references/customs-overview-top-n-api.md)

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
python scripts/error_report.py --params '{"requestPath":"/agent/customs/overview/top-n","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"Top N query failed with a server error"}'
```
- Do not report normal business conditions (insufficient balance, invalid API key, parameter errors) — handle them via their own flows
- Error reporting does not incur query fees
- **Parameters**: See [Error Report API](references/skill-error-report-api.md)

## Fees

**All API calls incur fees**, different interfaces have different billing methods.

**Latest pricing**: Users can visit [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
Or use: `python scripts/auth.py --price_info` (returns complete pricing for all interfaces)

### Query Billing Rules

Billed by **number of calls**, each call returns one page of top N rankings:
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
| "Show top 10 suppliers from China to US in 2025" | Top N Query (companyType=1) |
| "List top buyers importing from China to US in 2025" | Top N Query (companyType=2) |
| "Find the largest exporters from China to US" | Top N Query (companyType=1) |

## Usage Examples

### Query Top N

**User request**: "Show top suppliers from China to US in 2025"
```bash
python scripts/customs_overview_top_n.py --params '{"originCountryCode":"CN","arrivalCountryCode":"US","year":2025,"companyType":1}'
```

**Query top buyers**:
```bash
python scripts/customs_overview_top_n.py --params '{"originCountryCode":"CN","arrivalCountryCode":"US","year":2025,"companyType":2}'
```

**Query the next page**:
```bash
python scripts/customs_overview_top_n.py --params '{"originCountryCode":"CN","arrivalCountryCode":"US","year":2025,"companyType":1,"cursor":"eyJzdGFydCI6MH0="}'
```

## Error Handling

- **API key invalid/non-existent**: Check `UPKUAJING_API_KEY` in `~/.upkuajing/.env` file
- **Insufficient balance**: Guide user to top up
- **Invalid parameters**: **Must first check the corresponding API documentation in references/ directory**, get correct parameter names and formats from documentation, do not guess
- **Skill call errors / abnormal responses**: Explain to the user and, with user confirmation, report to the platform via `python scripts/error_report.py` (see [Report Skill Call Errors](#report-skill-call-errors))

### API Documentation Reference

- Top N: Check [references/customs-overview-top-n-api.md](references/customs-overview-top-n-api.md)
- Error Report: Check [references/skill-error-report-api.md](references/skill-error-report-api.md)

## Best Practices

1. **Check API documentation**:
   - **Before executing queries, must first check the corresponding API reference documentation**
   - Check [references/customs-overview-top-n-api.md](references/customs-overview-top-n-api.md)
   - Do not guess parameter names, get accurate parameter names and formats from documentation

2. **Company type**:
   - `companyType=1` for suppliers (exporters/sellers)
   - `companyType=2` for buyers (importers/purchasers)

3. **Pagination**:
   - Use the `cursor` parameter from the response to fetch the next page
   - If no `cursor` is returned, there are no more pages

4. **Cross-skill usage**:
   - Use **customs-overview-summary** first to get overview, then drill into top companies
   - Company IDs from results can be used in **customs-company-stats** or **customs-company-trends** for detailed company analysis
   - Company names from results can be searched in **upkuajing-customs-trade-company-search**

## Notes
- `year` and `companyType` are both required
- `companyId` is the internal ID for the company in UpKuaJing's database
- `latestTradeDate` is a Unix timestamp in milliseconds
- File paths use forward slashes on all platforms
- **Prohibit outputting technical parameter format**: Do not display code-style parameters in responses, convert to natural language
- **Do not** estimate or guess per-call fees — use `python scripts/auth.py --price_info` to get accurate pricing information
- **Do not** guess parameter names, get accurate parameter names and formats from documentation

## Related Skills

Other UpKuaJing skills you might find useful:

- customs-overview-summary — Query trade overview summary (aggregated)
- customs-overview-trade-list — Query country trade list with paginated breakdown
- customs-overview-trend — Query import/export trade trends by month
- customs-overview-us-import — Query US import transaction statistics
- customs-overview-date — Query date reference information
- customs-company-stats — Query company basic trade statistics
- customs-company-trends — Query company trade trends (monthly breakdown)
- customs-company-partner-stats — Query company trade partner distribution
- customs-company-area-stats — Query company trade area statistics (aggregated)
- upkuajing-customs-trade-company-search — Search customs trade companies