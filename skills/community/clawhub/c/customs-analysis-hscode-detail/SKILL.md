---
name: customs-analysis-hscode-detail
description: "Query HS code detail information — retrieve Chinese and English descriptions for a given HS code.\n\nTrigger: HS code detail, tariff code description, customs code lookup, HS code meaning, product classification"
metadata: {"version":"1.0.1","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"📋","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# Customs Analysis HS Code Detail

Query HS code detail information from customs data using the UpKuaJing Open Platform API.

## Overview

This skill retrieves detailed description information for a given HS (Harmonized System) code, including both Chinese and English descriptions. This helps you understand what products a specific HS code represents.

## Running Scripts

### Environment Setup

1. **Check Python**: `python --version`
2. **Install dependencies**: `pip install -r requirements.txt`

Script directory: `scripts/*.py`
Run example: `python scripts/*.py`

**Important**: Always use direct script invocation like `python scripts/customs_analysis_hscode_detail.py`. **Do NOT use** shell compound commands like `cd scripts && python customs_analysis_hscode_detail.py`

### HS Code Detail Query (`customs_analysis_hscode_detail.py`)
- **Return granularity**: One record per query
- **Use cases**: Look up product classification for an HS code, get Chinese/English descriptions of tariff codes
- **Examples**:
  - "What does HS code 04021000 mean?"
  - "Get the description for HS code 04021000"
- **Parameters**: See [HS Code Detail API](references/customs-analysis-hscode-detail-api.md)

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
python scripts/error_report.py --params '{"requestPath":"/agent/customs/analysis/hscode/detail","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"HS code detail query failed with a server error"}'
```
- Do not report normal business conditions (insufficient balance, invalid API key, parameter errors) — handle them via their own flows
- Error reporting does not incur query fees
- **Parameters**: See [Error Report API](references/skill-error-report-api.md)

## Fees

**All API calls incur fees**, different interfaces have different billing methods.

**Latest pricing**: Users can visit [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
Or use: `python scripts/auth.py --price_info` (returns complete pricing for all interfaces)

### Query Billing Rules

Billed by **number of calls**, each call returns one HS code detail:
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
| "What does HS code 04021000 mean?" | HS Code Detail Query |
| "Get description of tariff code 04021000" | HS Code Detail Query |
| "Explain product classification for 04021000" | HS Code Detail Query |

## Usage Examples

### Query HS Code Detail

**User request**: "What does HS code 04021000 mean?"
```bash
python scripts/customs_analysis_hscode_detail.py --params '{"hscode":"04021000"}'
```

## Error Handling

- **API key invalid/non-existent**: Check `UPKUAJING_API_KEY` in `~/.upkuajing/.env` file
- **Insufficient balance**: Guide user to top up
- **Invalid parameters**: **Must first check the corresponding API documentation in references/ directory**, get correct parameter names and formats from documentation, do not guess
- **Skill call errors / abnormal responses**: Explain to the user and, with user confirmation, report to the platform via `python scripts/error_report.py` (see [Report Skill Call Errors](#report-skill-call-errors))

### API Documentation Reference

- HS Code Detail: Check [references/customs-analysis-hscode-detail-api.md](references/customs-analysis-hscode-detail-api.md)
- Error Report: Check [references/skill-error-report-api.md](references/skill-error-report-api.md)

## Best Practices

1. **Check API documentation**:
   - **Before executing queries, must first check the corresponding API reference documentation**
   - Check [references/customs-analysis-hscode-detail-api.md](references/customs-analysis-hscode-detail-api.md)
   - Do not guess parameter names, get accurate parameter names and formats from documentation

2. **HS code format**:
   - Use complete 8-digit HS code format (e.g., "04021000")

3. **Cross-skill usage**:
   - First use **customs-analysis-hscode-search** to find matching HS codes, then use this skill to get descriptions
   - Combine with **customs-analysis-trends**, **customs-analysis-area**, or **customs-analysis-trade-percent** for detailed analysis after understanding the HS code meaning

## Notes
- `hscode` is the only required parameter
- `descZh` is the Chinese description of the HS code
- `descEn` is the English description of the HS code
- File paths use forward slashes on all platforms
- **Prohibit outputting technical parameter format**: Do not display code-style parameters in responses, convert to natural language
- **Do not** estimate or guess per-call fees — use `python scripts/auth.py --price_info` to get accurate pricing information
- **Do not** guess parameter names, get accurate parameter names and formats from documentation

## Related Skills

Other UpKuaJing skills you might find useful:

- customs-analysis-hscode-search — Search HS codes by product name and keywords
- customs-analysis-trends — Query import/export trade trends by HS code
- customs-analysis-area — Query trade area distribution by HS code
- customs-analysis-trade-percent — Query trade percentage by company
- customs-overview-summary — Query trade overview summary (aggregated)
- customs-overview-trend — Query import/export trade trends by month
- customs-company-hscode-list — Query company HS code list
- customs-company-product-list — Query company product list
- customs-company-stats — Query company basic trade statistics
- upkuajing-customs-trade-company-search — Search customs trade companies