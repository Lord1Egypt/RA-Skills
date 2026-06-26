---
name: deepread-medical
title: DeepRead Medical Records
description: Extract structured data from medical records, lab reports, prescriptions, and clinical documents. Pre-built schemas for patient info, diagnoses, medications, vitals. PII redaction for HIPAA compliance. 97%+ accuracy. Free 2,000 pages/month.
metadata: {"openclaw":{"requires":{"env":["DEEPREAD_API_KEY"]},"primaryEnv":"DEEPREAD_API_KEY","homepage":"https://www.deepread.tech"}}
---

# DeepRead Medical Records Processing

Extract structured data from medical records, lab reports, prescriptions, discharge summaries, and clinical documents. Then redact patient PII for HIPAA-compliant sharing, archiving, or LLM processing.

> This skill instructs the agent to POST documents to `https://api.deepread.tech` and poll for results. No system files are modified.

## What You Get Back

Submit a medical record and get structured JSON:

```json
{
  "patient_name": {"value": "Jane Smith", "hil_flag": false, "found_on_page": 1},
  "date_of_birth": {"value": "1990-03-15", "hil_flag": false, "found_on_page": 1},
  "mrn": {"value": "MRN-2026-004521", "hil_flag": false, "found_on_page": 1},
  "visit_date": {"value": "2026-03-28", "hil_flag": false, "found_on_page": 1},
  "provider": {"value": "Dr. Sarah Chen, MD", "hil_flag": false, "found_on_page": 1},
  "diagnoses": {"value": [
    {"code": "J06.9", "description": "Acute upper respiratory infection"},
    {"code": "R50.9", "description": "Fever, unspecified"}
  ], "hil_flag": false, "found_on_page": 2},
  "medications": {"value": [
    {"name": "Amoxicillin", "dosage": "500mg", "frequency": "3x daily", "duration": "10 days"},
    {"name": "Acetaminophen", "dosage": "500mg", "frequency": "as needed", "duration": "PRN"}
  ], "hil_flag": false, "found_on_page": 2},
  "vitals": {"value": {
    "blood_pressure": "128/82",
    "heart_rate": 88,
    "temperature": 101.2,
    "weight": "165 lbs"
  }, "hil_flag": false, "found_on_page": 1},
  "follow_up": {"value": "Return in 2 weeks if symptoms persist", "hil_flag": true, "reason": "Handwritten note, partial OCR"}
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

## Medical Record Schema

Use this pre-built schema for clinical documents. Customize it for your specific document types:

```json
{
  "type": "object",
  "properties": {
    "patient_name": {"type": "string", "description": "Patient full name"},
    "date_of_birth": {"type": "string", "description": "Patient date of birth (YYYY-MM-DD)"},
    "mrn": {"type": "string", "description": "Medical record number or patient ID"},
    "visit_date": {"type": "string", "description": "Date of visit or service (YYYY-MM-DD)"},
    "provider": {"type": "string", "description": "Treating physician or provider name with credentials"},
    "facility": {"type": "string", "description": "Hospital or clinic name"},
    "diagnoses": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "code": {"type": "string", "description": "ICD-10 diagnosis code if present"},
          "description": {"type": "string", "description": "Diagnosis description"}
        }
      },
      "description": "List of diagnoses or conditions"
    },
    "medications": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string", "description": "Medication name"},
          "dosage": {"type": "string", "description": "Dosage amount and unit"},
          "frequency": {"type": "string", "description": "How often taken"},
          "duration": {"type": "string", "description": "Duration of treatment"}
        }
      },
      "description": "Prescribed or current medications"
    },
    "vitals": {
      "type": "object",
      "properties": {
        "blood_pressure": {"type": "string", "description": "Blood pressure reading (systolic/diastolic)"},
        "heart_rate": {"type": "number", "description": "Heart rate in BPM"},
        "temperature": {"type": "number", "description": "Body temperature in Fahrenheit"},
        "weight": {"type": "string", "description": "Patient weight with unit"},
        "height": {"type": "string", "description": "Patient height with unit"}
      },
      "description": "Vital signs recorded during visit"
    },
    "procedures": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "code": {"type": "string", "description": "CPT procedure code if present"},
          "description": {"type": "string", "description": "Procedure description"}
        }
      },
      "description": "Procedures performed"
    },
    "lab_results": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "test_name": {"type": "string", "description": "Lab test name"},
          "value": {"type": "string", "description": "Result value with unit"},
          "reference_range": {"type": "string", "description": "Normal reference range"},
          "flag": {"type": "string", "description": "H (high), L (low), or normal"}
        }
      },
      "description": "Laboratory test results"
    },
    "allergies": {
      "type": "array",
      "items": {"type": "string"},
      "description": "Known allergies"
    },
    "follow_up": {"type": "string", "description": "Follow-up instructions or next appointment"},
    "notes": {"type": "string", "description": "Clinical notes or additional observations"}
  }
}
```

## Extract Data From Medical Records

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
        "patient_name": {"type": "string", "description": "Patient full name"},
        "date_of_birth": {"type": "string", "description": "Patient DOB (YYYY-MM-DD)"},
        "mrn": {"type": "string", "description": "Medical record number"},
        "provider": {"type": "string", "description": "Treating physician with credentials"},
        "diagnoses": {
            "type": "array",
            "items": {"type": "object", "properties": {
                "code": {"type": "string", "description": "ICD-10 code"},
                "description": {"type": "string"}
            }},
            "description": "Diagnoses"
        },
        "medications": {
            "type": "array",
            "items": {"type": "object", "properties": {
                "name": {"type": "string"},
                "dosage": {"type": "string"},
                "frequency": {"type": "string"}
            }},
            "description": "Medications"
        },
        "lab_results": {
            "type": "array",
            "items": {"type": "object", "properties": {
                "test_name": {"type": "string"},
                "value": {"type": "string"},
                "reference_range": {"type": "string"},
                "flag": {"type": "string", "description": "H, L, or normal"}
            }},
            "description": "Lab results"
        }
    }
})

# Submit medical record
with open("patient_record.pdf", "rb") as f:
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
  -F "file=@patient_record.pdf" \
  -F 'schema={"type":"object","properties":{"patient_name":{"type":"string","description":"Patient full name"},"mrn":{"type":"string","description":"Medical record number"},"diagnoses":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string","description":"ICD-10 code"},"description":{"type":"string"}}},"description":"Diagnoses"},"medications":{"type":"array","items":{"type":"object","properties":{"name":{"type":"string"},"dosage":{"type":"string"},"frequency":{"type":"string"}}},"description":"Medications"}}}'
```

## HIPAA Compliance: Redact Patient PII

After extracting data, redact patient PII from the original document before sharing, archiving, or sending to an LLM:

```python
# Step 1: Extract structured data (keep the data you need)
with open("patient_record.pdf", "rb") as f:
    extract_job = requests.post(
        f"{BASE}/v1/process",
        headers=headers,
        files={"file": f},
        data={"schema": schema},
    ).json()

# Step 2: Redact PII from the original (clean copy for filing)
with open("patient_record.pdf", "rb") as f:
    redact_job = requests.post(
        f"{BASE}/v1/pii/redact",
        headers=headers,
        files={"file": f},
    ).json()

# Poll for redaction results
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

        # Download redacted file
        pdf = requests.get(result["redacted_file_url"]).content
        with open("patient_record_redacted.pdf", "wb") as f:
            f.write(pdf)
        print("Saved: patient_record_redacted.pdf")
        break
    elif result["status"] == "failed":
        print(f"Failed: {result.get('error')}")
        break
    delay = min(delay * 1.5, 15)
```

DeepRead's PII redaction is context-aware for medical documents:

- **"Dr. Sarah Chen"** on letterhead — physician, SKIP
- **"Sarah Chen"** on intake form — patient, REDACT
- **"admissions@hospital.edu"** — institutional email, SKIP
- **"john.smith@gmail.com"** — personal email, REDACT
- **Invoice date** — not a DOB, SKIP
- **"Date of Birth: 03/15/1990"** — DOB, REDACT

14 PII types detected: names, SSNs, DOB, medical record numbers, phone, email, address, credit cards, passport, driver's license, bank accounts, IBANs, IPs, URLs.

## Use Cases

- **Clinical Data Extraction** — Pull diagnoses, medications, vitals, and lab results from patient records into your EHR or data warehouse
- **Lab Report Processing** — Extract test names, values, reference ranges, and abnormal flags from lab reports
- **Prescription Digitization** — Convert handwritten or printed prescriptions into structured medication data
- **Insurance Claims** — Extract procedure codes, diagnosis codes, and patient info for claims processing
- **Medical Research** — De-identify patient records for research datasets while preserving clinical data
- **Discharge Summary Processing** — Extract follow-up instructions, medications, and diagnoses from discharge paperwork
- **Prior Authorization** — Pull relevant clinical data to auto-fill prior auth forms

## Tips for Medical Documents

- **Use ICD-10/CPT code descriptions** — Adding "ICD-10 diagnosis code if present" in the schema description helps the model recognize code formats
- **Specify units** — "Temperature in Fahrenheit" or "Weight with unit (lbs or kg)" reduces ambiguity
- **Create blueprints for recurring form types** — If you process the same lab report format repeatedly, train a blueprint at deepread.tech/dashboard/optimizer for 20-30% improvement
- **Always redact before sharing** — Use the PII redaction endpoint before sending documents to LLMs, external systems, or non-clinical staff

## BYOK — Zero Processing Costs

Connect your own OpenAI, Google, or OpenRouter key via the dashboard. All document processing routes through your provider — zero DeepRead LLM costs, page quota skipped.

Set it up: https://www.deepread.tech/dashboard/byok

## Related DeepRead Skills

- **deepread-ocr** — General OCR and structured extraction — `clawhub install uday390/deepread-ocr`
- **deepread-pii** — Redact PII from any document — `clawhub install uday390/deepread-pii`
- **deepread-form-fill** — Fill PDF forms with AI vision — `clawhub install uday390/deepread-form-fill`
- **deepread-invoice** — Invoice and receipt processing — `clawhub install uday390/deepread-invoice`
- **deepread-agent-setup** — OAuth device flow authentication — `clawhub install uday390/deepread-agent-setup`
- **deepread-byok** — Bring Your Own Key setup — `clawhub install uday390/deepread-byok`

## Support

- **Dashboard**: https://www.deepread.tech/dashboard
- **Demo Repo**: https://github.com/deepread-tech/deepread-demo
- **Issues**: https://github.com/deepread-tech/deep-read-service/issues
- **Email**: hello@deepread.tech

---

**Get started free:** https://www.deepread.tech/dashboard/?utm_source=clawhub
