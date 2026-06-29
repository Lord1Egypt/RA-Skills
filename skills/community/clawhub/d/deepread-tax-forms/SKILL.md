---
name: deepread-tax-forms
title: DeepRead Tax Forms
description: Extract structured data from W-2s, 1099s, 1040s, and other tax forms — employer/payer, recipient, wages, withholdings, box-by-box amounts — as typed JSON. Works on PDFs and scans. Per-field confidence flags. PII redaction built in. Free 2,000 pages/month.
metadata: {"openclaw":{"requires":{"env":["DEEPREAD_API_KEY"]},"primaryEnv":"DEEPREAD_API_KEY","homepage":"https://www.deepread.tech"}}
---

# DeepRead Tax Forms

Turn W-2s, 1099-NEC/MISC/INT/DIV, 1040s, and other tax documents into clean, typed JSON — employer/payer details, recipient info, and the box-by-box amounts — with a `needs_review` flag on every field so nothing wrong slips into a filing or an income calculation.

> This skill instructs the agent to POST documents to `https://api.deepread.tech` and poll for results. No system files are modified.

## What You Get Back (W-2 example)

```json
{
  "schema_version": "dp02",
  "status": "completed",
  "extraction": {
    "fields": [
      {"key": "form_type", "value": "W-2", "needs_review": false, "location": {"page": 1}},
      {"key": "tax_year", "value": 2025, "needs_review": false, "location": {"page": 1}},
      {"key": "employer_name", "value": "Acme Corp", "needs_review": false, "location": {"page": 1}},
      {"key": "employer_ein", "value": "12-3456789", "needs_review": false, "location": {"page": 1}},
      {"key": "employee_name", "value": "Jordan Rivera", "needs_review": false, "location": {"page": 1}},
      {"key": "wages_box1", "value": 84500.00, "needs_review": false, "location": {"page": 1}},
      {"key": "federal_tax_withheld_box2", "value": 12180.00, "needs_review": false, "location": {"page": 1}},
      {"key": "social_security_wages_box3", "value": 84500.00, "needs_review": false, "location": {"page": 1}}
    ]
  }
}
```

## Setup

```bash
open "https://www.deepread.tech/dashboard/?utm_source=clawhub"
export DEEPREAD_API_KEY="sk_live_your_key_here"
```

No key yet? `clawhub install uday390/deepread-agent-setup` — your agent fetches one via OAuth device flow.

## Schema (W-2)

```json
{
  "type": "object",
  "properties": {
    "form_type":   {"type": "string", "description": "Tax form type, e.g. W-2, 1099-NEC, 1040"},
    "tax_year":    {"type": "number", "description": "Tax year on the form"},
    "employer_name": {"type": "string", "description": "Employer / payer name"},
    "employer_ein":  {"type": "string", "description": "Employer EIN"},
    "employee_name": {"type": "string", "description": "Employee / recipient name"},
    "employee_ssn_last4": {"type": ["string","null"], "description": "Last 4 of SSN only"},
    "wages_box1":    {"type": "number", "description": "Box 1 — wages, tips, other compensation"},
    "federal_tax_withheld_box2": {"type": "number", "description": "Box 2 — federal income tax withheld"},
    "social_security_wages_box3": {"type": ["number","null"], "description": "Box 3 — Social Security wages"},
    "medicare_wages_box5": {"type": ["number","null"], "description": "Box 5 — Medicare wages"},
    "state_wages_box16": {"type": ["number","null"], "description": "Box 16 — state wages"}
  }
}
```

For **1099-NEC** swap to `payer_name`, `payer_tin`, `recipient_name`, `nonemployee_compensation_box1`. The pattern is the same — describe each box clearly and DeepRead maps it.

## Extract (cURL)

```bash
curl -s -X POST https://api.deepread.tech/v1/process \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@w2.pdf" \
  -F 'schema={"type":"object","properties":{"form_type":{"type":"string"},"tax_year":{"type":"number"},"employer_name":{"type":"string"},"wages_box1":{"type":"number"},"federal_tax_withheld_box2":{"type":"number"}}}'
# → {"id":"...","status":"queued"} — then GET /v1/jobs/{id}
```

## Use Cases

- **Tax prep software** — auto-populate returns from uploaded W-2s/1099s instead of manual box entry
- **Lending / underwriting** — verify income from tax documents
- **Accounting firms** — bulk-ingest client tax forms each season
- **Payroll audits** — cross-check W-2 totals against payroll records

## Handle PII Responsibly — Redact Before Sharing

Tax forms are dense with SSNs, EINs, and addresses. Extract only what you need (`employee_ssn_last4`), and redact full documents before sharing with `deepread-pii`:

```bash
curl -X POST https://api.deepread.tech/v1/pii/redact -H "X-API-Key: $DEEPREAD_API_KEY" -F "file=@w2.pdf"
```

Install: `clawhub install uday390/deepread-pii`

## Tips

- **Name each box explicitly** ("Box 1 — wages…") — far better than "wages".
- **Recurring form type?** Build a blueprint at `https://www.deepread.tech/dashboard/optimizer` for a 20–30% accuracy lift.
- **Check `needs_review`** — only flagged boxes need a human.

## Related DeepRead Skills

- **deepread-ocr** — general extraction — `clawhub install uday390/deepread-ocr`
- **deepread-pay-stubs** — income verification from pay stubs — `clawhub install uday390/deepread-pay-stubs`
- **deepread-pii** — redact sensitive data — `clawhub install uday390/deepread-pii`

## Support

- **Dashboard**: https://www.deepread.tech/dashboard
- **Email**: support@deepread.tech

---

**Get started free:** https://www.deepread.tech/dashboard/?utm_source=clawhub
