---
name: deepread-resume-parser
title: DeepRead Resume Parser
description: Parse resumes and CVs into structured JSON — contact info, work history, education, skills, and total years of experience. Works on PDF, Word-exported PDF, and scanned resumes in any layout. Per-field confidence flags. PII redaction for bias-free screening. Free 2,000 pages/month.
metadata: {"openclaw":{"requires":{"env":["DEEPREAD_API_KEY"]},"primaryEnv":"DEEPREAD_API_KEY","homepage":"https://www.deepread.tech"}}
---

# DeepRead Resume Parser

Turn any resume or CV — PDF, scanned, or wildly creative two-column design — into clean, structured JSON: contact details, work history with dates and titles, education, skills, and computed years of experience. Each field carries a `needs_review` flag, so your ATS ingests the confident fields and routes only the ambiguous ones to a recruiter.

> This skill instructs the agent to POST documents to `https://api.deepread.tech` and poll for results. No system files are modified.

## Why resumes break normal parsers

Resumes have no standard layout: two columns, sidebars, icons, tables, graphics, dates as "Jan 2021 – Present." Regex/template parsers shatter on the first creative design. DeepRead reads the document the way a human does — visual + semantic — runs **multi-model consensus**, and flags low-confidence fields instead of silently mangling a job title.

## What You Get Back

```json
{
  "schema_version": "dp02",
  "status": "completed",
  "extraction": {
    "fields": [
      {"key": "full_name", "value": "Priya Nair", "needs_review": false, "location": {"page": 1}},
      {"key": "email", "value": "priya.nair@email.com", "needs_review": false, "location": {"page": 1}},
      {"key": "phone", "value": "+1 415 555 0148", "needs_review": false, "location": {"page": 1}},
      {"key": "years_experience", "value": 7, "needs_review": true, "review_reason": "Computed from overlapping roles", "location": {"page": 1}},
      {"key": "work_history", "value": [
        {"company": "Stripe", "title": "Senior Backend Engineer", "start_date": "2021-06", "end_date": "present", "location": "Remote"},
        {"company": "Shopify", "title": "Backend Engineer", "start_date": "2018-08", "end_date": "2021-05", "location": "Toronto, CA"}
      ], "needs_review": false, "location": {"page": 1}},
      {"key": "education", "value": [
        {"institution": "UC Berkeley", "degree": "B.S. Computer Science", "year": "2018"}
      ], "needs_review": false, "location": {"page": 1}},
      {"key": "skills", "value": ["Python", "Go", "PostgreSQL", "Kubernetes", "gRPC"], "needs_review": false, "location": {"page": 1}}
    ]
  }
}
```

## Setup

```bash
open "https://www.deepread.tech/dashboard/?utm_source=clawhub"
export DEEPREAD_API_KEY="sk_live_your_key_here"
```

No key yet? `clawhub install uday390/deepread-agent-setup` and your agent fetches one via OAuth device flow.

## Resume Schema

```json
{
  "type": "object",
  "properties": {
    "full_name": {"type": "string", "description": "Candidate's full name"},
    "email":     {"type": ["string", "null"], "description": "Email address"},
    "phone":     {"type": ["string", "null"], "description": "Phone number"},
    "location":  {"type": ["string", "null"], "description": "City / region of residence"},
    "headline":  {"type": ["string", "null"], "description": "Professional headline or current title"},
    "years_experience": {"type": ["number", "null"], "description": "Total years of professional experience"},
    "work_history": {
      "type": "array",
      "description": "Employment history, most recent first",
      "items": {"type": "object", "properties": {
        "company":    {"type": "string", "description": "Employer name"},
        "title":      {"type": "string", "description": "Job title"},
        "start_date": {"type": ["string", "null"], "description": "Start (YYYY-MM)"},
        "end_date":   {"type": ["string", "null"], "description": "End (YYYY-MM) or 'present'"},
        "location":   {"type": ["string", "null"], "description": "Role location"}
      }, "required": ["company", "title"]}
    },
    "education": {
      "type": "array",
      "description": "Education history",
      "items": {"type": "object", "properties": {
        "institution": {"type": "string", "description": "School / university"},
        "degree":      {"type": ["string", "null"], "description": "Degree and field"},
        "year":        {"type": ["string", "null"], "description": "Graduation year"}
      }, "required": ["institution"]}
    },
    "skills": {"type": "array", "items": {"type": "string"}, "description": "Listed skills / technologies"}
  }
}
```

## Parse a Resume

### Python

```python
import requests, json, time

API_KEY = "sk_live_YOUR_KEY"
BASE = "https://api.deepread.tech"
headers = {"X-API-Key": API_KEY}

schema = json.dumps({
    "type": "object",
    "properties": {
        "full_name": {"type": "string", "description": "Candidate full name"},
        "email": {"type": ["string", "null"], "description": "Email"},
        "phone": {"type": ["string", "null"], "description": "Phone"},
        "years_experience": {"type": ["number", "null"], "description": "Total years experience"},
        "work_history": {"type": "array", "items": {"type": "object", "properties": {
            "company": {"type": "string"}, "title": {"type": "string"},
            "start_date": {"type": ["string", "null"]}, "end_date": {"type": ["string", "null"]}
        }, "required": ["company", "title"]}},
        "skills": {"type": "array", "items": {"type": "string"}, "description": "Skills"}
    }
})

with open("resume.pdf", "rb") as f:
    job = requests.post(f"{BASE}/v1/process", headers=headers,
                        files={"file": f}, data={"schema": schema}).json()

job_id = job["id"]
delay = 5
while True:
    time.sleep(delay)
    result = requests.get(f"{BASE}/v1/jobs/{job_id}", headers=headers).json()
    if result["status"] in ("completed", "failed"):
        break
    delay = min(delay * 1.5, 20)

if result["status"] == "completed":
    cand = {f["key"]: f["value"] for f in result["extraction"]["fields"]}
    print(f"{cand.get('full_name')} — {len(cand.get('work_history', []))} roles, skills: {', '.join(cand.get('skills', [])[:5])}")
    # Route only flagged fields to a recruiter
    for f in result["extraction"]["fields"]:
        if f.get("needs_review"):
            print(f"  REVIEW {f['key']}: {f.get('review_reason')}")
```

### cURL

```bash
curl -s -X POST https://api.deepread.tech/v1/process \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@resume.pdf" \
  -F 'schema={"type":"object","properties":{"full_name":{"type":"string"},"email":{"type":["string","null"]},"skills":{"type":"array","items":{"type":"string"}},"work_history":{"type":"array","items":{"type":"object","properties":{"company":{"type":"string"},"title":{"type":"string"}}}}}}'
```

## Use Cases

- **ATS ingestion** — auto-populate candidate records from uploaded resumes, no manual entry
- **Talent sourcing** — bulk-parse a folder of CVs into a searchable, structured database
- **Recruiting agencies** — standardize candidates from every format into one schema
- **Skills matching** — extract the `skills` array and match against a job's requirements
- **Job boards** — let applicants upload a resume and pre-fill the application form (pair with `deepread-form-fill`)

## Bias-Free Screening — Redact PII First

For blind/anonymized first-pass screening, redact names, photos, addresses, and other PII before the resume reaches a reviewer — reducing unconscious bias and supporting fair-hiring policies:

```bash
curl -X POST https://api.deepread.tech/v1/pii/redact \
  -H "X-API-Key: $DEEPREAD_API_KEY" \
  -F "file=@resume.pdf"
```

Install: `clawhub install uday390/deepread-pii`

## Tips for Best Accuracy

- **Describe fields precisely** — "Total years of professional experience" beats "experience".
- **Use `["string","null"]`** for optional fields (email/phone often missing) so they default to null cleanly.
- **High-volume from one source?** Build a blueprint at `https://www.deepread.tech/dashboard/optimizer` for a 20–30% lift.
- **Check `needs_review`** — overlapping roles and gap years are the usual flags; everything else auto-imports.

## BYOK — Zero Processing Costs

Bring your own OpenAI/Google/OpenRouter key in the dashboard — processing routes through your account, page quota skipped. https://www.deepread.tech/dashboard/byok

## Related DeepRead Skills

- **deepread-ocr** — general OCR + structured extraction — `clawhub install uday390/deepread-ocr`
- **deepread-form-fill** — fill application forms from parsed data — `clawhub install uday390/deepread-form-fill`
- **deepread-pii** — redact for blind screening — `clawhub install uday390/deepread-pii`

## Support

- **Dashboard**: https://www.deepread.tech/dashboard
- **Issues**: https://github.com/deepread-tech/deep-read-service/issues
- **Email**: support@deepread.tech

---

**Get started free:** https://www.deepread.tech/dashboard/?utm_source=clawhub
