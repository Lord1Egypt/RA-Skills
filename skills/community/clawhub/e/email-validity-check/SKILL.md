---
name: email-validity-check
description: "Verify email validity and format, cut email bounce‑rates and clean contact lists for exporters, recruiters and B2B sales teams.\n\nTrigger: email address validation, reduce email bounce rate, email‑list scrubbing, CRM data cleansing, cold outreach optimization"
metadata: {"version":"1.0.2","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"📧","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# Email Validity Check

Check email address validity and status using the Open Platform API.

## Overview

This skill provides access to email validity detection through a single interface:
- **Email Validity Check** (`email_validity_check.py`): Check email address validity

## Running Scripts

### Environment Setup

1. **Check Python**: `python --version`
2. **Install dependencies**: `pip install -r requirements.txt`

Script directory: `scripts/*.py`
Run example: `python scripts/*.py`

**Important**: Always use direct script invocation like `python scripts/email_validity_check.py`. **Do NOT use** shell compound commands like `cd scripts && python email_validity_check.py`.

## Email Validity Check (`email_validity_check.py`)

Check email address validity.

**Parameters**: See [Email Validity API](references/email-api.md)

**Examples**:
```bash
# Check single email
python scripts/email_validity_check.py --emails "test@example.com"

# Check multiple emails
python scripts/email_validity_check.py --emails "test@example.com valid@gmail.com invalid-email"
```

## API Key and Account

- **API Key**: Stored in `~/.upkuajing/.env` file as `UPKUAJING_API_KEY`
- **First check**: If not set, prompt user to provide or apply at [Open Platform](https://developer.upkuajing.com/)

### **API Key Not Set**
First check if the `~/.upkuajing/.env` file has UPKUAJING_API_KEY;
If UPKUAJING_API_KEY is not set, prompt the user to choose:
1. User has one: User provides it (manually add to ~/.upkuajing/.env file)
2. User doesn't have one: Guide user to apply at [Open Platform](https://developer.upkuajing.com/)
Wait for user selection;

### **Account Top-up**
When API response indicates insufficient balance, explain and guide user to top up:
1. Create top-up order (`auth.py --new_rec_order`)
2. Based on order response, send payment page URL to user, guide user to open URL and pay, user confirms after successful payment;

### **Get Account Information**

### **Report Skill Call Errors**
When an API call fails or returns abnormal data (server error, timeout, malformed response, etc.), explain the anomaly to the user in natural language and ask whether to report it to the platform for troubleshooting. Only run the report after user confirmation:
```bash
python scripts/error_report.py --params '{"requestPath":"/agent/validation/email","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"Email validity check failed with a server error"}'
```
- Do not report normal business conditions (insufficient balance, invalid API key, parameter errors) — handle them via their own flows
- Error reporting does not incur query fees
- **Parameters**: See [Error Report API](references/skill-error-report-api.md)

## Fees

**Email validity check API calls incur fees**.
**Latest pricing**: Users can visit [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
Or use: `python scripts/auth.py --price_info` (returns complete pricing for all interfaces)

### Fee Confirmation Principle

**Any operation that incurs fees must first inform and wait for explicit user confirmation. Do not execute in the same message as the notification.**

## Workflow

### Decision Guide

| User Intent | Use API |
|-------------|---------|
| "Verify email address exists" | Email Validity Check |

## Error Handling

- **API key invalid/non-existent**: Check `UPKUAJING_API_KEY` in `~/.upkuajing/.env` file
- **Insufficient balance**: Guide user to top up
- **Invalid parameters**: **Must first check the corresponding API documentation in references/ directory**, get correct parameter names and formats from documentation, do not guess
- **Skill call errors / abnormal responses**: Explain to the user and, with user confirmation, report to the platform via `python scripts/error_report.py` (see [Report Skill Call Errors](#report-skill-call-errors))

### API Documentation Reference

- Email Validity: Check [references/email-api.md](references/email-api.md)
- Error Report: Check [references/skill-error-report-api.md](references/skill-error-report-api.md)

## Notes

- File paths use forward slashes on all platforms
- **Do not guess parameter names**, get accurate parameter names and formats from documentation
- **Prohibit outputting technical parameter format**: Do not display code-style parameters in responses, convert to natural language
- **Do not estimate or guess fees** — use `python scripts/auth.py --price_info` to get accurate pricing information

## Related Skills

Other skills you might find useful:

- linkedin-person-search — Search people from the LinkedIn source
- global-company-person-search — Search people from the global company database
- linkedin-company-search — Search companies from the LinkedIn source
- global-company-search — Search companies from the global company database
- global-company-shareholder — Query shareholder list from the global company database
- global-company-employee — Query employee list from the global company database
- global-company-person-colleague — Query colleague list from the global company database
- global-company-person-alumni — Query alumni list from the global company database
- global-company-person-experience — Query work experience list from the global company database
- global-company-person-education — Query education history list from the global company database
- global-company-person-school-detail — Query school detail from the global company database
- upkuajing-global-company-people-search — Global company and people search
- upkuajing-customs-trade-company-search — Search customs trade companies
- upkuajing-map-merchants-search — Map-based merchant search
- upkuajing-email-tool — Send emails and manage email tasks
- upkuajing-sms-tool — Send SMS and manage SMS tasks
- upkuajing-contact-info-validity-check — Check contact info validity
- phone-validity-check — Check phone number validity
- email-validity-check — Check email address validity
- domain-validity-check — Check domain validity and security
