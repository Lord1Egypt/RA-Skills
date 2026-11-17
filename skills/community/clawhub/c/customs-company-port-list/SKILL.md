---
name: customs-company-port-list
description: "Query paginated port trade data for a company — retrieve port-level trade statistics with counts, amounts, and percentages for logistics analysis.\n\nTrigger: customs port list, paginated port query, company trade port details, import-export port analysis, trade logistics drill-down"
metadata: {"version":"1.0.1","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"⚓","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# Customs Company Port Trade List

Query paginated port trade data for a company from customs data using the UpKuaJing Open Platform API.

## Overview

This skill provides access to paginated port trade data from UpKuaJing's customs database. Given a company ID and company type, it returns a list of ports with trade statistics including trade count, amount, quantity, weight, and percentage.

## Running Scripts

### Environment Setup

1. **Check Python**: `python --version`
2. **Install dependencies**: `pip install -r requirements.txt`

Script directory: `scripts/*.py`
Run example: `python scripts/*.py`

**Important**: Always use direct script invocation like `python scripts/customs_company_port_list.py`. **Do NOT use** shell compound commands like `cd scripts && python customs_company_port_list.py`

### Company Port List Query (`customs_company_port_list.py`)
- **Return granularity**: One record per port
- **Use cases**: Browse through a company's trade ports with detailed stats, analyze logistics routes and port-level trade volume
- **Examples**:
  - "List trade ports for company 100001 as a supplier"
  - "Get port-level trade details for company 100001 as a buyer"
- **Parameters**: See [Company Port List API](references/customs-company-port-list-api.md)

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
python scripts/error_report.py --params '{"requestPath":"/agent/customs/company/port/list","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"Company port list query failed with a server error"}'
```
- Do not report normal business conditions (insufficient balance, invalid API key, parameter errors) — handle them via their own flows
- Error reporting does not incur query fees
- **Parameters**: See [Error Report API](references/skill-error-report-api.md)

## Fees

**All API calls incur fees**, different interfaces have different billing methods.

**Latest pricing**: Users can visit [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
Or use: `python scripts/auth.py --price_info` (returns complete pricing for all interfaces)

### Query Billing Rules

Billed by **number of calls**, each call returns a page of port list for one company:
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
| "List trade ports for company 100001 as a supplier" | Company Port List Query |
| "Show port-level trade breakdown for company 100001" | Company Port List Query |

## Usage Examples

### Query Company Port List

**User request**: "List trade ports for company 100001 as a supplier"
```bash
python scripts/customs_company_port_list.py --params '{"companyId":100001,"companyType":1}'
```

**Query the next page**:
```bash
python scripts/customs_company_port_list.py --params '{"companyId":100001,"companyType":1,"cursor":"eyJsYXN0X2lkIjogMTAwMX0="}'
```

**Query with filters**:
```bash
python scripts/customs_company_port_list.py --params '{"companyId":100001,"companyType":1,"dateStart":1700000000000,"dateEnd":1735689599999,"countryCodes":["KR"]}'
```

## Error Handling

- **API key invalid/non-existent**: Check `UPKUAJING_API_KEY` in `~/.upkuajing/.env` file
- **Insufficient balance**: Guide user to top up
- **Invalid parameters**: **Must first check the corresponding API documentation in references/ directory**, get correct parameter names and formats from documentation, do not guess
- **Skill call errors / abnormal responses**: Explain to the user and, with user confirmation, report to the platform via `python scripts/error_report.py` (see [Report Skill Call Errors](#report-skill-call-errors))

### API Documentation Reference

- Company Port List: Check [references/customs-company-port-list-api.md](references/customs-company-port-list-api.md)
- Error Report: Check [references/skill-error-report-api.md](references/skill-error-report-api.md)

## Best Practices

1. **Check API documentation**:
   - **Before executing queries, must first check the corresponding API reference documentation**
   - Check [references/customs-company-port-list-api.md](references/customs-company-port-list-api.md)
   - Do not guess parameter names, get accurate parameter names and formats from documentation

2. **Pagination**:
   - Use the `cursor` parameter from the response to fetch the next page
   - If no `cursor` is returned in the response, there are no more pages

3. **Data interpretation**:
   - `percentTrade` is the percentage of trade (as a decimal, e.g., 45.67 means 45.67%)
   - `port` is the port name (e.g., "BUSAN")

4. **Cross-skill usage**:
   - The company ID can be obtained from **customs-company-stats** or **upkuajing-customs-trade-company-search**
   - Port names from results can be used to filter data in **customs-company-trends** and **customs-company-partner-stats**

## Notes
- `companyType` determines the company's role (1=supplier, 2=buyer)
- Use `cursor` for pagination — it's a base64-encoded string
- File paths use forward slashes on all platforms
- **Prohibit outputting technical parameter format**: Do not display code-style parameters in responses, convert to natural language
- **Do not** estimate or guess per-call fees — use `python scripts/auth.py --price_info` to get accurate pricing information
- **Do not** guess parameter names, get accurate parameter names and formats from documentation

## Related Skills

Other UpKuaJing skills you might find useful:

- customs-company-area-stats — Query company trade area statistics
- customs-company-area-list — Query company trade area list
- customs-company-hscode-stats — Query company trade HS code statistics
- customs-company-hscode-list — Query company trade HS code list
- customs-company-product-list — Query company trade product list
- customs-company-stats — Query company basic trade statistics
- customs-company-trends — Query company trade trends (monthly breakdown)
- customs-company-partner-stats — Query company trade partner distribution
- upkuajing-customs-trade-company-search — Search customs trade companies
- upkuajing-global-company-people-search — Unified company and people search across all sources