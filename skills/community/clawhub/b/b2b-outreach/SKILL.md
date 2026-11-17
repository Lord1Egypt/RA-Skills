---
name: b2b-outreach
description: "B2B outreach toolkit: send bulk cold email and global SMS, harvest Google Maps merchants, and validate contact info (phone/WhatsApp, email, domain) before reaching out. Monitor email/SMS delivery status, cleanse CRM contact lists, and run end-to-end cross-border outreach campaigns.\n\nTrigger: bulk cold email, email send, email open rate tracker, business domain emails, mass mail for exporters, global bulk SMS, two-way SMS replies, SMS delivery reports, cross-border SMS marketing, Google maps business scraper, merchant data download, radius-based lead search, distributor sourcing, phone number validation, WhatsApp status check, email address validation, domain validity security check, CRM data cleansing, bulk SMS pre-verification, B2B outreach campaign"
metadata: {"version":"1.0.1","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"🚀","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# B2B Outreach

Aggregate skill for outbound engagement: **email** + **SMS** + **map merchant harvesting** + **contact validation**. 11 scripts, flat layout (no indexes - script count is small enough to list directly).

## Overview

Four capability groups:

| Group | Scripts | Purpose |
|-------|---------|---------|
| Email | mail_send, mail_task_list, mail_task_record_list | Bulk cold email + delivery tracking |
| SMS | sms_send, sms_task_list, sms_task_record_list | Global SMS (two-way) + delivery tracking |
| Map merchants | merchants_search, geography_list | Google Maps business data harvesting |
| Validation | phone_validity_check, email_validity_check, domain_validity_check | Clean/verify contacts before outreach |

## Running Scripts

### Environment Setup

1. **Check Python**: `python --version`
2. **Install dependencies**: `pip install -r requirements.txt`

Script directory: `scripts/*.py`

**Important**: Always use direct script invocation like `python scripts/mail_send.py`. **Do NOT use** shell compound commands like `cd scripts && python mail_send.py`.

## Scripts

### Email

#### `mail_send.py` - Send emails
Send emails to one or many recipients.
- **Parameters**: See [Email Send API](references/email-send-api.md)
```bash
python scripts/mail_send.py \
  --subject "Test Email" \
  --content "This is the email content" \
  --emails '["recipient@example.com"]'
```

#### `mail_task_list.py` - Email task list
View email tasks with optional time-range / status filter.
- **Parameters**: See [Email Task List API](references/email-task-list-api.md)
```bash
python scripts/mail_task_list.py --page_no 1 --page_size 10
```

#### `mail_task_record_list.py` - Email task records
View delivery records for a specific email task.
- **Parameters**: See [Email Task Record List API](references/email-task-record-list-api.md)
```bash
python scripts/mail_task_record_list.py --task_id 1496 --page_no 1 --page_size 10
```

### SMS

#### `sms_send.py` - Send SMS
Send SMS to phone numbers; `--channel_type 1` enables two-way (reply) mode.
- **Parameters**: See [SMS Send API](references/sms-send-api.md)
```bash
python scripts/sms_send.py \
  --content "This is SMS content" \
  --phones '["13800138000"]'
```

#### `sms_task_list.py` - SMS task list
- **Parameters**: See [SMS Task List API](references/sms-task-list-api.md)
```bash
python scripts/sms_task_list.py --page_no 1 --page_size 10
```

#### `sms_task_record_list.py` - SMS task records
- **Parameters**: See [SMS Task Record List API](references/sms-task-record-list-api.md)
```bash
python scripts/sms_task_record_list.py --task_id 1496 --page_no 1 --page_size 10
```

### Map Merchants

#### `merchants_search.py` - Merchant search
Search Google Maps merchants by keywords + location. Two modes: country/province/city search, or nearby (lat/lon + radius via `geoDistance`).
- **Parameters**: See [Merchants Search API](references/merchants-search-api.md)
```bash
python scripts/merchants_search.py \
  --params '{"keywords":["restaurant"],"countryCodes":["BR"]}' \
  --query_count 100
```

#### `geography_list.py` - Geography list
Get country/province/city IDs to build `merchants_search` parameters.
```bash
python scripts/geography_list.py --type country
python scripts/geography_list.py --type province --country_id 1
python scripts/geography_list.py --type city --country_id 1
```
- Country list: [country-list](references/country-list-api.md) | Province list: [province-list](references/province-list-api.md) | City list: [city-list](references/city-list-api.md)

### Contact Validation

#### `phone_validity_check.py` - Phone validity
Check phone validity, type, and WhatsApp registration status.
- **Parameters**: See [Phone Validity API](references/validity-phone-api.md)
```bash
python scripts/phone_validity_check.py --phones "+8613812345678 +14155551234"
```

#### `email_validity_check.py` - Email validity
Check email address validity / deliverability.
- **Parameters**: See [Email Validity API](references/validity-email-api.md)
```bash
python scripts/email_validity_check.py --emails "a@example.com b@example.com"
```

#### `domain_validity_check.py` - Domain validity
Check domain validity and security.
- **Parameters**: See [Domain Validity API](references/validity-domain-api.md)
```bash
python scripts/domain_validity_check.py --domains "example.com foo.org"
```

## Core Workflow: Validate Before Outreach

The signature workflow this aggregate enables (clean -> reach -> monitor):

1. **Collect contacts** - export from CRM, or harvest via `merchants_search` (map), or receive from `b2b-lead-generation` (decision-maker lookup).
2. **Validate & cleanse** - run `phone_validity_check` / `email_validity_check` / `domain_validity_check` to drop invalid contacts. (Reduces wasted sends & fees.)
3. **Reach out** - `mail_send` (cold email) and/or `sms_send` (global SMS, two-way for replies).
4. **Monitor delivery** - `mail_task_list` / `sms_task_list` -> `*_task_record_list` to check delivery status.

> Validation is itself billable - but it is far cheaper than sending to dead contacts. Inform the user of the validation cost first.

## API Key and Top-up

This skill requires an API key, stored in `~/.upkuajing/.env`:
```bash
cat ~/.upkuajing/.env
```
```
UPKUAJING_API_KEY=your_api_key_here
```

### API Key Not Set
First check if `~/.upkuajing/.env` has `UPKUAJING_API_KEY`. If not, prompt the user to choose:
1. User has one: user provides it (manually add to `~/.upkuajing/.env`)
2. User doesn't have one: apply via `auth.py --new_key` (auto-saved to `~/.upkuajing/.env`)

Wait for user selection.

### Account Top-up
When API response indicates insufficient balance:
1. Create top-up order (`auth.py --new_rec_order`)
2. Send the payment page URL to the user, guide them to open & pay; proceed after they confirm success.

### Get Account Information
`python scripts/auth.py --account_info`

Newly applied keys must be registered/bound at [UpKuaJing Open Platform](https://developer.upkuajing.com/).

### **Report Skill Call Errors**
When an API call fails or returns abnormal data (server error, timeout, malformed response, etc.), explain the anomaly to the user in natural language and ask whether to report it to the platform for troubleshooting. Only run the report after user confirmation:
```bash
python scripts/error_report.py --params '{"requestPath":"/agent/mail/send","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"Email send failed with a server error"}'
```
- Do not report normal business conditions (insufficient balance, invalid API key, parameter errors) — handle them via their own flows
- Error reporting does not incur query fees
- **Parameters**: See [Error Report API](references/skill-error-report-api.md)

## Fees

**Send/search/validate calls incur fees**; task list & record list queries are free.

**Latest pricing**: visit [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html), or run:
```bash
python scripts/auth.py --price_info
```
(returns complete pricing for all interfaces - the aggregate auth.py queries the full price list and falls back to per-original-skill lookup if needed.)

### Billing rules (summary)
- **Email/SMS send**: charged per send request, cost scales with recipient count.
- **Merchant search**: billed by calls, each returns up to 100 records -> calls = `ceil(query_count / 100)`.
- **Phone/email/domain validity**: charged per check (per number/email/domain).
- **Free**: `geography_list`; all `*_task_list` / `*_task_record_list`.
- Per-interface billing detail lives in the corresponding `references/<xxx>-api.md`.

### Fee Confirmation Principle

**Any operation that incurs fees must first inform the user and wait for explicit confirmation in a separate message. Do not execute in the same message as the notification.** When `query_count` exceeds one page, inform the user of the expected number of calls first.

## Error Handling

- **API key invalid/non-existent**: check `UPKUAJING_API_KEY` in `~/.upkuajing/.env`
- **Insufficient balance**: guide user to top up
- **Invalid parameters**: **must first check the corresponding API doc in `references/`** - get correct parameter names/formats from documentation, do not guess
- **Skill call errors / abnormal responses**: Explain to the user and, with user confirmation, report to the platform via `python scripts/error_report.py` (see [Report Skill Call Errors](#report-skill-call-errors))

### API Documentation Reference

**Email**
- [email-send](references/email-send-api.md) | [email-task-list](references/email-task-list-api.md) | [email-task-record-list](references/email-task-record-list-api.md)

**SMS**
- [sms-send](references/sms-send-api.md) | [sms-task-list](references/sms-task-list-api.md) | [sms-task-record-list](references/sms-task-record-list-api.md)

**Map merchants**
- [merchants-search](references/merchants-search-api.md) | [country-list](references/country-list-api.md) | [province-list](references/province-list-api.md) | [city-list](references/city-list-api.md)

**Validation** (prefixed `validity-` to distinguish from email-send docs)
- [validity-phone](references/validity-phone-api.md) | [validity-email](references/validity-email-api.md) | [validity-domain](references/validity-domain-api.md)
- Error Report: Check [references/skill-error-report-api.md](references/skill-error-report-api.md)

## Notes

- Email/SMS send is **synchronous submission, asynchronous delivery**: the API returns immediately; check `status` via task records. Email status: `0`-pending `1`-sending `2`-completed. SMS status: `1`-sending `2`-completed `3`-failed `4`-partial.
- `task_data/` stores results under UUID subdirectories.
- Country codes use ISO 3166-1 alpha-2 (e.g., CN, US, BR). Map search keywords/industries should be in **English**.
- File paths use forward slashes on all platforms.
- **Prohibit outputting technical parameter format**: convert code-style params to natural language in responses.
- **Do not** estimate per-call fees - use `auth.py --price_info` for accurate pricing.
- **Do not** guess parameter names - read the `references/<xxx>-api.md` first.

## Related Skills

Other UpKuaJing skills you might find useful:

- b2b-lead-generation - Customs trade intelligence, global-company deep due-diligence, LinkedIn professional data (find leads to outreach to)
- upkuajing-email-tool - Standalone email send & task tracking
- upkuajing-sms-tool - Standalone SMS send & task tracking
- upkuajing-map-merchants-search - Standalone Google Maps merchant harvesting
- upkuajing-contact-info-validity-check - Standalone contact info validity check (phone/email/domain)
- upkuajing-customs-trade-company-search (= upkuajing-trade-company-search) - Search companies with real customs trade records
- upkuajing-company-people-search (= upkuajing-global-company-people-search) - Quick shallow company/person lookup + contact info
