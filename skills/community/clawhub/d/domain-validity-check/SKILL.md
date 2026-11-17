---
name: domain-validity-check
description: "Verify corporate domain status to filter invalid domains, boost email deliverability and clean your CRM and email lists for exporters.\n\nTrigger: domain validity check, corporate domain verification, email‑list scrubbing, CRM data cleansing, sales lead validation"
metadata: {"version":"1.0.2","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"🌐","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# Domain Validity Check

Check domain validity, security, and sensitivity status using the Open Platform API.

## Overview

This skill provides access to domain validity detection through a single interface:
- **Domain Validity Check** (`domain_validity_check.py`): Check domain validity and security

## Running Scripts

### Environment Setup

1. **Check Python**: `python --version`
2. **Install dependencies**: `pip install -r requirements.txt`

Script directory: `scripts/*.py`
Run example: `python scripts/*.py`

**Important**: Always use direct script invocation like `python scripts/domain_validity_check.py`. **Do NOT use** shell compound commands like `cd scripts && python domain_validity_check.py`.

## Domain Validity Check (`domain_validity_check.py`)

Check domain validity and security status.

**Parameters**: See [Domain Validity API](references/domain-api.md)

**Examples**:
```bash
# Check single domain
python scripts/domain_validity_check.py --domains "google.com"

# Check multiple domains
python scripts/domain_validity_check.py --domains "google.com fake-domain-xyz123456.com github.com"
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
python scripts/error_report.py --params '{"requestPath":"/agent/validation/domain","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"Domain validity check failed with a server error"}'
```
- Do not report normal business conditions (insufficient balance, invalid API key, parameter errors) — handle them via their own flows
- Error reporting does not incur query fees
- **Parameters**: See [Error Report API](references/skill-error-report-api.md)

## Fees

**Domain validity check API calls incur fees**.
**Latest pricing**: Users can visit [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
Or use: `python scripts/auth.py --price_info` (returns complete pricing for all interfaces)

### Fee Confirmation Principle

**Any operation that incurs fees must first inform and wait for explicit user confirmation. Do not execute in the same message as the notification.**

## Workflow

### Decision Guide

| User Intent | Use API |
|-------------|---------|
| "Check if domain is safe" | Domain Validity Check |

## Error Handling

- **API key invalid/non-existent**: Check `UPKUAJING_API_KEY` in `~/.upkuajing/.env` file
- **Insufficient balance**: Guide user to top up
- **Invalid parameters**: **Must first check the corresponding API documentation in references/ directory**, get correct parameter names and formats from documentation, do not guess
- **Skill call errors / abnormal responses**: Explain to the user and, with user confirmation, report to the platform via `python scripts/error_report.py` (see [Report Skill Call Errors](#report-skill-call-errors))

### API Documentation Reference

- Domain Validity: Check [references/domain-api.md](references/domain-api.md)
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
