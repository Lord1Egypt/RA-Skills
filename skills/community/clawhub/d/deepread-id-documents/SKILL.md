---
name: deepread-id-documents
title: DeepRead ID Documents
description: Extract structured data from passports, driver's licenses, and national ID cards for KYC/onboarding — name, document number, dates, nationality — as typed JSON. Vision AI reads scans and photos. Per-field confidence flags. PII redaction built in for compliant storage. Free 2,000 pages/month.
metadata: {"openclaw":{"requires":{"env":["DEEPREAD_API_KEY"]},"primaryEnv":"DEEPREAD_API_KEY","homepage":"https://www.deepread.tech"}}
---

# DeepRead ID Documents

Read passports, driver's licenses, and national ID cards — scans or phone photos — into clean, typed JSON for KYC and customer onboarding: name, document number, dates of birth/issue/expiry, and nationality. Every field carries a `needs_review` flag, because in identity verification, a confident-but-wrong character matters.

> **Use responsibly.** Only process identity documents you are authorized to handle, for legitimate KYC/onboarding/verification purposes, with the document holder's knowledge and applicable consent. This skill POSTs the document to `https://api.deepread.tech` and polls for results. No system files are modified. Review DeepRead's [privacy policy](https://www.deepread.tech/privacy) for data handling.

## What You Get Back

```json
{
  "schema_version": "dp02",
  "status": "completed",
  "extraction": {
    "fields": [
      {"key": "document_type", "value": "Passport", "needs_review": false, "location": {"page": 1}},
      {"key": "full_name", "value": "PRIYA NAIR", "needs_review": false, "location": {"page": 1}},
      {"key": "document_number", "value": "P1234567", "needs_review": true, "review_reason": "Glare on character 3", "location": {"page": 1}},
      {"key": "date_of_birth", "value": "1992-07-14", "needs_review": false, "location": {"page": 1}},
      {"key": "expiry_date", "value": "2031-05-02", "needs_review": false, "location": {"page": 1}},
      {"key": "nationality", "value": "IND", "needs_review": false, "location": {"page": 1}},
      {"key": "issuing_country", "value": "IND", "needs_review": false, "location": {"page": 1}}
    ]
  }
}
```

## Setup

```bash
open "https://www.deepread.tech/dashboard/?utm_source=clawhub"
export DEEPREAD_API_KEY="sk_live_your_key_here"
```

## Schema

```json
{
  "type": "object",
  "properties": {
    "document_type":  {"type": "string", "description": "Passport, Driver's License, National ID, etc."},
    "full_name":      {"type": "string", "description": "Full name as printed"},
    "document_number":{"type": "string", "description": "Document / license number"},
    "date_of_birth":  {"type": "string", "description": "Date of birth (YYYY-MM-DD)"},
    "issue_date":     {"type": ["string","null"], "description": "Issue date (YYYY-MM-DD)"},
    "expiry_date":    {"type": ["string","null"], "description": "Expiry date (YYYY-MM-DD)"},
    "nationality":    {"type": ["string","null"], "description": "Nationality (ISO 3-letter if shown)"},
    "issuing_country":{"type": ["string","null"], "description": "Issuing country / authority"},
    "sex":            {"type": ["string","null"], "description": "Sex/gender if printed"}
  }
}
```

## Extract + Expiry Check (Python)

```python
import datetime
fields = {f["key"]: f["value"] for f in result["extraction"]["fields"]}

# Flag expired or soon-to-expire IDs
exp = fields.get("expiry_date")
if exp:
    days = (datetime.date.fromisoformat(exp) - datetime.date.today()).days
    if days < 0:   print("⚠ EXPIRED document — reject")
    elif days < 90: print(f"⚠ expires in {days} days")

# Route low-confidence fields (glare, worn print) to manual review
for f in result["extraction"]["fields"]:
    if f.get("needs_review"):
        print(f"REVIEW {f['key']}: {f.get('review_reason')}")
```

## Use Cases

- **KYC / customer onboarding** — auto-fill identity fields from an uploaded ID
- **Age / expiry verification** — confirm DOB and that the document is valid
- **Account recovery / fraud ops** — structured ID data for verification workflows
- **Travel / hospitality check-in** — capture passport details quickly

## Store Compliantly — Redact the Image

After extracting the fields you need, redact the raw ID image before archiving or sharing, so you're not storing full identity documents in the clear:

```bash
curl -X POST https://api.deepread.tech/v1/pii/redact -H "X-API-Key: $DEEPREAD_API_KEY" -F "file=@id.jpg"
```

Install: `clawhub install uday390/deepread-pii`

## Tips

- **Photos work** — vision AI handles phone captures, but flat, glare-free, well-lit images extract best.
- **Expect `needs_review`** on worn cards/glare — that's the feature; verify those manually.
- **Don't store more than you need** — extract the minimum fields and redact the source.

## Related DeepRead Skills

- **deepread-form-fill** — fill onboarding forms from extracted ID data — `clawhub install uday390/deepread-form-fill`
- **deepread-pii** — redact identity documents — `clawhub install uday390/deepread-pii`
- **deepread-ocr** — general extraction — `clawhub install uday390/deepread-ocr`

## Support

- **Dashboard**: https://www.deepread.tech/dashboard
- **Email**: support@deepread.tech

---

**Get started free:** https://www.deepread.tech/dashboard/?utm_source=clawhub
