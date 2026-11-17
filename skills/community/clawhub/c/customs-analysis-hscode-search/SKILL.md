---
name: customs-analysis-hscode-search
description: "Search HS codes for analysis reports — find matching HS codes by product name and HS code keywords.\n\nTrigger: HS code search, product HS code lookup, customs code search, find HS code, tariff code search"
metadata: {"version":"1.0.1","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"🔍","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# Customs Analysis HS Code Search

Search HS codes from customs data using the UpKuaJing Open Platform API.

## Overview

This skill allows you to search for HS (Harmonized System) codes by providing a product name and HS code keywords. It returns a list of matching HS codes that can be used in other analysis report skills.

## Running Scripts

### Environment Setup

1. **Check Python**: `python --version`
2. **Install dependencies**: `pip install -r requirements.txt`

Script directory: `scripts/*.py`
Run example: `python scripts/*.py`

**Important**: Always use direct script invocation like `python scripts/customs_analysis_hscode_search.py`. **Do NOT use** shell compound commands like `cd scripts && python customs_analysis_hscode_search.py`

### HS Code Search (`customs_analysis_hscode_search.py`)
- **Return granularity**: One or more matching HS codes
- **Use cases**: Find HS codes by product name, look up customs classification codes, search tariff codes
- **Examples**:
  - "Search HS codes for milk powder"
  - "Find HS codes starting with 0402"
- **Parameters**: See [HS Code Search API](references/customs-analysis-hscode-search-api.md)

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
python scripts/error_report.py --params '{"requestPath":"/agent/customs/analysis/hscode/search","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"HS code search query failed with a server error"}'
```
- Do not report normal business conditions (insufficient balance, invalid API key, parameter errors) — handle them via their own flows
- Error reporting does not incur query fees
- **Parameters**: See [Error Report API](references/skill-error-report-api.md)

## Fees

**All API calls incur fees**, different interfaces have different billing methods.

**Latest pricing**: Users can visit [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
Or use: `python scripts/auth.py --price_info` (returns complete pricing for all interfaces)

### Query Billing Rules

Billed by **number of calls**, each call returns one page of HS code search results:
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
| "Search HS codes for milk powder" | HS Code Search |
| "Find HS codes starting with 0402" | HS Code Search |
| "Look up tariff codes for a product" | HS Code Search |

## Usage Examples

### Search HS Codes

**User request**: "Search HS codes for milk powder with prefix 0402"
```bash
python scripts/customs_analysis_hscode_search.py --params '{"product":"milk powder","hscode":"0402"}'
```

**Query the next page**:
```bash
python scripts/customs_analysis_hscode_search.py --params '{"product":"milk powder","hscode":"0402","cursor":"eyJpZCI6MX0="}'
```

## Error Handling

- **API key invalid/non-existent**: Check `UPKUAJING_API_KEY` in `~/.upkuajing/.env` file
- **Insufficient balance**: Guide user to top up
- **Invalid parameters**: **Must first check the corresponding API documentation in references/ directory**, get correct parameter names and formats from documentation, do not guess
- **Skill call errors / abnormal responses**: Explain to the user and, with user confirmation, report to the platform via `python scripts/error_report.py` (see [Report Skill Call Errors](#report-skill-call-errors))

### API Documentation Reference

- HS Code Search: Check [references/customs-analysis-hscode-search-api.md](references/customs-analysis-hscode-search-api.md)
- Error Report: Check [references/skill-error-report-api.md](references/skill-error-report-api.md)

## Best Practices

1. **Check API documentation**:
   - **Before executing queries, must first check the corresponding API reference documentation**
   - Check [references/customs-analysis-hscode-search-api.md](references/customs-analysis-hscode-search-api.md)
   - Do not guess parameter names, get accurate parameter names and formats from documentation

2. **Search parameters**:
   - Both `product` and `hscode` are required
   - Provide both product name and HS code prefix for best results

3. **Cross-skill usage**:
   - Use found HS codes with **customs-analysis-hscode-detail** to get code descriptions
   - Use found HS codes with **customs-analysis-trends** or **customs-analysis-area** for detailed analysis

## Notes
- `product` and `hscode` are both required parameters
- The response `list` contains matching HS code strings
- File paths use forward slashes on all platforms
- **Prohibit outputting technical parameter format**: Do not display code-style parameters in responses, convert to natural language
- **Do not** estimate or guess per-call fees — use `python scripts/auth.py --price_info` to get accurate pricing information
- **Do not** guess parameter names, get accurate parameter names and formats from documentation

## Related Skills

Other UpKuaJing skills you might find useful:

- customs-analysis-hscode-detail — Query HS code detail descriptions
- customs-analysis-trends — Query import/export trade trends by HS code
- customs-analysis-area — Query trade area distribution by HS code
- customs-analysis-trade-percent — Query trade percentage by company
- customs-overview-summary — Query trade overview summary (aggregated)
- customs-overview-trend — Query import/export trade trends by month
- customs-company-hscode-list — Query company HS code list
- customs-company-product-list — Query company product list
- customs-company-stats — Query company basic trade statistics
- upkuajing-customs-trade-company-search — Search customs trade companies