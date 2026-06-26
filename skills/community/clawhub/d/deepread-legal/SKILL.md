---
name: deepread-legal
title: DeepRead Legal Documents
description: Extract structured data from contracts, legal agreements, court filings, and compliance documents. Pre-built schemas for parties, clauses, dates, obligations. PII redaction for privilege review. 97%+ accuracy. Free 2,000 pages/month.
metadata: {"openclaw":{"requires":{"env":["DEEPREAD_API_KEY"]},"primaryEnv":"DEEPREAD_API_KEY","homepage":"https://www.deepread.tech"}}
---

# DeepRead Legal Document Processing

Extract structured data from contracts, legal agreements, NDAs, court filings, leases, and compliance documents. Then redact privileged or sensitive information before sharing with opposing counsel, auditors, or external parties.

> This skill instructs the agent to POST documents to `https://api.deepread.tech` and poll for results. No system files are modified.

## What You Get Back

Submit a contract and get structured JSON:

```json
{
  "document_type": {"value": "Master Services Agreement", "hil_flag": false, "found_on_page": 1},
  "parties": {"value": [
    {"name": "Acme Corp", "role": "Service Provider", "address": "123 Tech Blvd, San Francisco, CA"},
    {"name": "GlobalCo Inc", "role": "Client", "address": "456 Market St, New York, NY"}
  ], "hil_flag": false, "found_on_page": 1},
  "effective_date": {"value": "2026-01-15", "hil_flag": false, "found_on_page": 1},
  "termination_date": {"value": "2027-01-14", "hil_flag": false, "found_on_page": 1},
  "governing_law": {"value": "State of California", "hil_flag": false, "found_on_page": 8},
  "contract_value": {"value": 250000.00, "hil_flag": true, "reason": "Multiple amounts found on different pages"},
  "payment_terms": {"value": "Net 45 from invoice date", "hil_flag": false, "found_on_page": 3},
  "key_clauses": {"value": [
    {"type": "Indemnification", "summary": "Provider indemnifies Client against third-party IP claims", "page": 5},
    {"type": "Limitation of Liability", "summary": "Capped at 12 months of fees paid", "page": 5},
    {"type": "Termination", "summary": "Either party may terminate with 30 days written notice", "page": 6},
    {"type": "Non-Compete", "summary": "12-month non-compete within same industry vertical", "page": 7}
  ], "hil_flag": false, "found_on_page": 5},
  "signatures": {"value": [
    {"name": "John Smith", "title": "CEO, Acme Corp", "date": "2026-01-10"},
    {"name": "Jane Doe", "title": "General Counsel, GlobalCo Inc", "date": "2026-01-12"}
  ], "hil_flag": false, "found_on_page": 8}
}
```

Fields with `hil_flag: true` need human review. Everything else is high-confidence.

## Setup

### Get Your API Key

```bash
open "https://www.deepread.tech/dashboard/?utm_source=clawhub"
```

Save it:
```bash
export DEEPREAD_API_KEY="sk_live_your_key_here"
```

## Contract Schema

Pre-built schema for contracts and legal agreements:

```json
{
  "type": "object",
  "properties": {
    "document_type": {"type": "string", "description": "Type of legal document (MSA, NDA, lease, employment agreement, etc.)"},
    "parties": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string", "description": "Full legal name of the party"},
          "role": {"type": "string", "description": "Role in the agreement (e.g., Licensor, Licensee, Landlord, Tenant)"},
          "address": {"type": "string", "description": "Address of the party"}
        }
      },
      "description": "All parties to the agreement"
    },
    "effective_date": {"type": "string", "description": "Date the agreement takes effect (YYYY-MM-DD)"},
    "termination_date": {"type": "string", "description": "End date or expiration of the agreement (YYYY-MM-DD)"},
    "governing_law": {"type": "string", "description": "Jurisdiction governing the agreement"},
    "contract_value": {"type": "number", "description": "Total contract value or consideration amount"},
    "payment_terms": {"type": "string", "description": "Payment schedule and terms"},
    "key_clauses": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "type": {"type": "string", "description": "Clause type (Indemnification, Limitation of Liability, Termination, Non-Compete, Confidentiality, IP Ownership, etc.)"},
          "summary": {"type": "string", "description": "Brief summary of the clause terms"},
          "page": {"type": "number", "description": "Page number where the clause appears"}
        }
      },
      "description": "Key clauses and their summaries"
    },
    "renewal_terms": {"type": "string", "description": "Auto-renewal terms if applicable"},
    "notice_period": {"type": "string", "description": "Required notice period for termination"},
    "signatures": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string", "description": "Signatory name"},
          "title": {"type": "string", "description": "Title and organization"},
          "date": {"type": "string", "description": "Date signed (YYYY-MM-DD)"}
        }
      },
      "description": "Signatories and execution dates"
    }
  }
}
```

## Extract Data From Legal Documents

### Python

```python
import requests
import json
import time

API_KEY = "sk_live_YOUR_KEY"
BASE = "https://api.deepread.tech"
headers = {"X-API-Key": API_KEY}

schema = json.dumps({
    "type": "object",
    "properties": {
        "document_type": {"type": "string", "description": "Type of legal document"},
        "parties": {
            "type": "array",
            "items": {"type": "object", "properties": {
                "name": {"type": "string", "description": "Full legal name"},
                "role": {"type": "string", "description": "Role in agreement"}
            }},
            "description": "All parties"
        },
        "effective_date": {"type": "string", "description": "Effective date (YYYY-MM-DD)"},
        "termination_date": {"type": "string", "description": "End date (YYYY-MM-DD)"},
        "governing_law": {"type": "string", "description": "Governing jurisdiction"},
        "contract_value": {"type": "number", "description": "Total value"},
        "key_clauses": {
            "type": "array",
            "items": {"type": "object", "properties": {
                "type": {"type": "string", "description": "Clause type"},
                "summary": {"type": "string", "description": "Summary of terms"},
                "page": {"type": "number"}
            }},
            "description": "Key clauses"
        },
        "signatures": {
            "type": "array",
            "items": {"type": "object", "properties": {
                "name": {"type": "string"},
                "title": {"type": "string"},
                "date": {"type": "string"}
            }},
            "description": "Signatories"
        }
    }
})

# Submit contract
with open("contract.pdf", "rb") as f:
    job = requests.post(
        f"{BASE}/v1/process",
        headers=headers,
        files={"file": f},
        data={"schema": schema},
    ).json()

job_id = job["id"]
print(f"Processing: {job_id}")

# Poll for results
delay = 5
while True:
    time.sleep(delay)
    result = requests.get(f"{BASE}/v1/jobs/{job_id}", headers=headers).json()

    if result["status"] == "completed":
        data = result["result"]["data"]
        print(json.dumps(data, indent=2))

        # Flag fields needing review
        for field, value in data.items():
            if isinstance(value, dict) and value.get("hil_flag"):
                print(f"\n  REVIEW: {field} — {value.get('reason')}")
        break
    elif result["status"] == "failed":
        print(f"Failed: {result.get('error')}")
        break

    delay = min(delay * 1.5, 15)
```

### cURL

```bash
curl -s -X POST https://api.deepread.tech/v1/process \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@contract.pdf" \
  -F 'schema={"type":"object","properties":{"document_type":{"type":"string","description":"Type of legal document"},"parties":{"type":"array","items":{"type":"object","properties":{"name":{"type":"string"},"role":{"type":"string"}}},"description":"All parties"},"effective_date":{"type":"string","description":"Effective date"},"governing_law":{"type":"string","description":"Governing jurisdiction"},"contract_value":{"type":"number","description":"Total value"},"key_clauses":{"type":"array","items":{"type":"object","properties":{"type":{"type":"string"},"summary":{"type":"string"}}},"description":"Key clauses"}}}'
```

## Privilege Review: Redact Before Sharing

Redact privileged or sensitive information before sharing with opposing counsel, auditors, or external parties:

```python
# Step 1: Extract the data you need
with open("contract.pdf", "rb") as f:
    extract_job = requests.post(
        f"{BASE}/v1/process",
        headers=headers,
        files={"file": f},
        data={"schema": schema},
    ).json()

# Step 2: Redact PII from the original before sharing
with open("contract.pdf", "rb") as f:
    redact_job = requests.post(
        f"{BASE}/v1/pii/redact",
        headers=headers,
        files={"file": f},
    ).json()

# Poll for redaction
redact_id = redact_job["id"]
delay = 5
while True:
    time.sleep(delay)
    result = requests.get(f"{BASE}/v1/pii/{redact_id}", headers=headers).json()
    if result["status"] == "completed":
        report = result["report"]
        print(f"Redacted {report['total_redactions']} PII instances")
        for pii_type, info in report["pii_detected"].items():
            print(f"  {pii_type}: {info['count']} found")
        pdf = requests.get(result["redacted_file_url"]).content
        with open("contract_redacted.pdf", "wb") as f:
            f.write(pdf)
        print("Saved: contract_redacted.pdf")
        break
    elif result["status"] == "failed":
        print(f"Failed: {result.get('error')}")
        break
    delay = min(delay * 1.5, 15)
```

## Use Cases

- **Contract Review** — Extract parties, dates, key clauses, and obligations from contracts and MSAs
- **NDA Analysis** — Pull confidentiality terms, duration, exclusions, and governing law
- **Lease Extraction** — Extract tenant, landlord, rent, term, renewal options from commercial leases
- **Court Filings** — Pull case numbers, parties, filing dates, and relief sought from legal filings
- **Legal Discovery** — Bulk-process documents, extract metadata, and redact privileged information
- **Compliance Audit** — Extract regulatory clauses, reporting obligations, and compliance deadlines
- **M&A Due Diligence** — Process stacks of contracts to extract key terms, liabilities, and change-of-control clauses
- **Employment Agreements** — Pull compensation, non-compete terms, equity vesting, and termination clauses

## Tips for Legal Documents

- **Specify clause types** — Listing expected clause types (Indemnification, Limitation of Liability, etc.) in the schema description improves extraction
- **Use page numbers** — Adding "page number where the clause appears" helps locate extracted terms in the original
- **Create blueprints for recurring document types** — If you process the same type of contract repeatedly (e.g., NDAs, MSAs), train a blueprint at deepread.tech/dashboard/optimizer for 20-30% accuracy improvement
- **Always redact before external sharing** — Use PII redaction before sending documents to opposing counsel, third-party reviewers, or LLMs

## BYOK — Zero Processing Costs

Connect your own OpenAI, Google, or OpenRouter key via the dashboard. All document processing routes through your provider — zero DeepRead LLM costs, page quota skipped.

Set it up: https://www.deepread.tech/dashboard/byok

## Related DeepRead Skills

- **deepread-ocr** — General OCR and structured extraction — `clawhub install uday390/deepread-ocr`
- **deepread-pii** — Redact PII from any document — `clawhub install uday390/deepread-pii`
- **deepread-form-fill** — Fill PDF forms with AI vision — `clawhub install uday390/deepread-form-fill`
- **deepread-invoice** — Invoice and receipt processing — `clawhub install uday390/deepread-invoice`
- **deepread-medical** — Medical records processing — `clawhub install uday390/deepread-medical`
- **deepread-agent-setup** — OAuth device flow authentication — `clawhub install uday390/deepread-agent-setup`
- **deepread-byok** — Bring Your Own Key setup — `clawhub install uday390/deepread-byok`

## Support

- **Dashboard**: https://www.deepread.tech/dashboard
- **Demo Repo**: https://github.com/deepread-tech/deepread-demo
- **n8n Node**: https://www.npmjs.com/package/n8n-nodes-deepread
- **Issues**: https://github.com/deepread-tech/deep-read-service/issues
- **Email**: hello@deepread.tech

---

**Get started free:** https://www.deepread.tech/dashboard/?utm_source=clawhub
