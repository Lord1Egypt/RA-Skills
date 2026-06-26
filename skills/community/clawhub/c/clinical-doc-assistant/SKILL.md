---
name: clinical-doc-assistant
version: "1.0.4"
description: "Use this skill when a clinician, practice manager, or healthcare developer needs to draft, structure, or retrieve clinical documentation — including SOAP notes, referral letters, prior authorization forms, discharge summaries, and care plan narratives. Connects to FHIR R4-compliant APIs (Epic, Cerner, Azure Health Data Services, HAPI FHIR) to pull structured patient data and generate documentation drafts. Also supports manual input when no EHR connection is available. DO NOT use for direct diagnosis, prescribing decisions, or any task requiring a licensed clinical judgment — this skill assists with documentation only."
tags: ["healthcare", "fhir", "clinical", "ehr", "documentation", "soap", "prior-auth", "referral", "discharge"]
author: "optimusprime19"
license: "MIT"
homepage: https://github.com/optimusprime19/clinical-doc-assistant
repository: https://github.com/optimusprime19/clinical-doc-assistant
requiredEnv:
  - FHIR_BASE_URL        # e.g. https://your-ehr.example.com/fhir/R4 (not needed if FHIR_SANDBOX_MODE=true)
  - FHIR_CLIENT_ID       # OAuth2 client ID from your EHR app registration
  - FHIR_CLIENT_SECRET   # OAuth2 client secret
  - FHIR_TOKEN_URL       # Token endpoint for SMART on FHIR auth
optionalEnv:
  - FHIR_TENANT_ID       # Required for Azure Health Data Services only
  - FHIR_SANDBOX_MODE    # Set to "true" to use public HAPI sandbox — no credentials needed
  - CLINICAL_DOC_API_URL # Hosted backend URL for credit-based generation (see backend.py)
  - CLINICAL_DOC_API_KEY # API key for the hosted backend
  - ANTHROPIC_API_KEY    # Required server-side if you self-host backend.py. When the hosted backend is used, patient_context is forwarded to Anthropic's API to generate documents. Do NOT use with real PHI unless you have a BAA with Anthropic and your backend is deployed in a HIPAA-eligible environment.
---

# Clinical Documentation Assistant

## Overview

This skill enables an OpenClaw agent to connect to any FHIR R4-compliant EHR, retrieve structured patient data, and generate high-quality clinical documentation drafts. It covers the most time-consuming document types in outpatient and inpatient settings.

**Supported document types:**
- SOAP notes (Subjective / Objective / Assessment / Plan)
- Referral letters (specialist, imaging, therapy)
- Prior authorization requests (insurance)
- Discharge summaries
- Care plan narratives
- Patient-facing after-visit summaries

**Supported FHIR backends:**
- Epic (SMART on FHIR)
- Cerner (Millennium)
- Azure Health Data Services
- HAPI FHIR (public sandbox for testing)
- Any R4-compliant server

> ⚠️ **Clinical Disclaimer:** All output is a documentation *draft* intended to be reviewed, edited, and signed by a licensed clinician. This skill does not provide clinical advice, diagnoses, or prescriptions.

> 🔒 **Privacy / PHI Warning:** FHIR data is fetched into the agent's context for the session only and is not written to disk by this skill. If you use the hosted backend (`CLINICAL_DOC_API_URL`), patient context is transmitted to that server — only use a backend you control in a HIPAA-eligible environment. **Do not use a third-party hosted backend with real patient data unless a BAA is in place.** For development and testing, always use `FHIR_SANDBOX_MODE=true` with synthetic data only.

---

## Quick Start (Sandbox Mode — No EHR Needed)

Set `FHIR_SANDBOX_MODE=true` to use the public HAPI R4 sandbox. No credentials required. Ideal for testing and development.

```bash
export FHIR_SANDBOX_MODE=true
```

Then ask your agent:
> "Pull patient John Smith from the FHIR sandbox and draft a SOAP note for today's hypertension follow-up."

---

## Authentication

This skill uses **SMART on FHIR** (OAuth2) for EHR connections. Set up once per environment.

### Step 1 — Register your app with your EHR

Each EHR has its own developer portal:
- **Epic:** https://fhir.epic.com → create a non-production app → note Client ID
- **Cerner:** https://code.cerner.com → register app → note Client ID + Secret
- **Azure AHDS:** Azure Portal → FHIR service → Authentication

### Step 2 — Set environment variables

```bash
export FHIR_BASE_URL="https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4"
export FHIR_CLIENT_ID="your-client-id"
export FHIR_CLIENT_SECRET="your-client-secret"
export FHIR_TOKEN_URL="https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token"
```

### Step 3 — Test the connection

Ask the agent:
> "Check my FHIR connection status."

The agent will attempt a token fetch and a `GET /metadata` call, then report back.

---

## FHIR Data Retrieval

The agent fetches only the resources needed for the requested document. All calls are read-only GET requests.

### Patient lookup

```
"Find patient [name] born [DOB]"
"Look up patient MRN 1234567"
"Search for patients with last name Rodriguez"
```

Internally calls:
```
GET /Patient?name=Rodriguez&birthdate=1975-04-12
GET /Patient/[id]
```

### Condition list

```
"What are the active conditions for this patient?"
```

Calls:
```
GET /Condition?patient=[id]&clinical-status=active
```

### Medication list

```
"Pull current medications for patient [id]"
```

Calls:
```
GET /MedicationRequest?patient=[id]&status=active
```

### Recent vitals

```
"Get the last set of vitals for this patient"
```

Calls:
```
GET /Observation?patient=[id]&category=vital-signs&_sort=-date&_count=10
```

### Lab results

```
"Pull recent labs — focus on HbA1c and BMP"
```

Calls:
```
GET /Observation?patient=[id]&category=laboratory&_sort=-date&_count=20
```

### Encounter history

```
"Show encounters from the last 6 months"
```

Calls:
```
GET /Encounter?patient=[id]&date=ge2025-09-01&_sort=-date
```

---

## Document Generation

Once patient data is retrieved, ask the agent to generate any document type.

### SOAP Note

**Trigger phrases:**
- "Draft a SOAP note for today's visit"
- "Write a SOAP note for this patient's diabetes follow-up"
- "Generate a clinical note — chief complaint is chest pain"

**What the agent does:**
1. Retrieves active conditions, current meds, recent vitals, and relevant labs
2. Asks you for any additional subjective information (chief complaint, HPI)
3. Structures the note into S / O / A / P sections
4. Flags any data gaps (missing vitals, no recent labs)

**Example output structure:**

```
SUBJECTIVE:
Patient is a 58-year-old male presenting for routine diabetes follow-up.
Reports improved energy since medication adjustment. No hypoglycemic episodes.
Denies chest pain, shortness of breath, or lower extremity edema.

OBJECTIVE:
Vitals (2026-03-15): BP 132/78, HR 72, Wt 198 lbs, BMI 29.4
HbA1c (2026-02-10): 7.2% (↓ from 7.9% in November)
Current Meds: Metformin 1000mg BID, Lisinopril 10mg daily

ASSESSMENT:
1. Type 2 Diabetes Mellitus — improving, at goal
2. Hypertension — controlled

PLAN:
1. Continue current regimen
2. Repeat HbA1c in 3 months
3. Annual ophthalmology referral ordered
4. Follow up in 3 months or sooner if concerns
```

---

### Referral Letter

**Trigger phrases:**
- "Write a referral to cardiology for this patient"
- "Draft a referral letter to Dr. Chen for physical therapy"
- "Generate an imaging referral for MRI of the lumbar spine"

**What the agent does:**
1. Pulls relevant conditions, meds, and recent encounter notes
2. Asks for referring provider name, specialty, and clinical question
3. Formats a professional referral letter with clinical context

**Example:**

```
[Date]

Re: [Patient Name], DOB [Date], MRN [Number]

Dear Dr. [Specialist],

I am referring the above-named patient for cardiology evaluation.
[Patient] is a 64-year-old female with a history of hypertension and
hyperlipidemia presenting with exertional dyspnea over the past 6 weeks.
Recent ECG showed non-specific ST changes. Echo has not been performed.

Current medications: Amlodipine 5mg, Atorvastatin 40mg, ASA 81mg.

I would appreciate your evaluation and recommendations.

Sincerely,
[Referring Provider]
```

---

### Prior Authorization Request

**Trigger phrases:**
- "Draft a prior auth for [medication/procedure]"
- "Generate a prior authorization for Humira for this patient"
- "Write a PA request for MRI lumbar spine — payer is BlueCross"

**What the agent does:**
1. Retrieves diagnosis codes (ICD-10) from active conditions
2. Looks up the requested item's typical HCPCS/CPT code
3. Generates a structured PA narrative with clinical justification
4. Lists supporting labs or imaging that strengthen the case

**Key fields generated:**
- Member ID (from input)
- Requesting provider NPI (from input)
- Diagnosis codes (from FHIR Condition resources)
- Requested service + procedure/drug code
- Clinical justification narrative
- Supporting documentation checklist

---

### Discharge Summary

**Trigger phrases:**
- "Generate a discharge summary for this patient"
- "Draft a hospital discharge note — patient is going home today"

**What the agent does:**
1. Pulls the current/recent encounter, active conditions, procedures, and meds
2. Asks for admission diagnosis, hospital course summary, and discharge instructions
3. Formats a complete discharge summary with follow-up plan

---

### After-Visit Summary (Patient-Facing)

**Trigger phrases:**
- "Write a patient-friendly after-visit summary"
- "Generate an AVS in plain language for this patient"

**What the agent does:**
1. Translates clinical note content into plain English (8th-grade reading level)
2. Lists medications with plain-language instructions
3. Includes follow-up appointments and warning signs to watch for

---

## Manual Mode (No FHIR Connection)

If no EHR is connected, the agent will prompt you to provide patient data manually. Useful for small practices, telehealth, or demos.

Ask: "Draft a SOAP note — I'll provide the patient data manually."

The agent will ask for:
- Chief complaint and HPI
- Vitals
- Active conditions and medications
- Assessment and plan outline

---

## Hosted Backend (Credit-Based Generation)

For high-volume use or team deployments, a managed API backend handles generation, audit logging, and HIPAA-aligned data handling.

Set these variables to enable:
```bash
export CLINICAL_DOC_API_URL="https://api.yourdomain.com/v1"
export CLINICAL_DOC_API_KEY="your-api-key"
```

When set, document generation routes through the hosted backend instead of the local LLM. Credits are deducted per document generated. Visit [your site] to purchase credits and manage your account.

**Hosted backend advantages:**
- Audit log of every document draft (for compliance)
- No patient data stored — stateless processing
- Team accounts with per-provider usage tracking
- 99.9% uptime SLA

---

## Data Privacy & HIPAA Considerations

- **Local mode:** Patient data is fetched into the agent's context for the duration of the session only. No data is written to disk by this skill.
- **Hosted mode:** Requests are processed statelessly. No PHI is retained after response delivery. Review the hosted backend's BAA before use in production.
- **Audit trail:** Clinicians should save final signed documents in their EHR per their organization's policies. This skill generates drafts only.
- **De-identification:** For development and testing, use `FHIR_SANDBOX_MODE=true` with synthetic data only.

> 🔒 Before using with real patient data, ensure your deployment satisfies your organization's HIPAA security requirements and that a Business Associate Agreement (BAA) is in place with any third-party service.

---

## Troubleshooting

**"FHIR connection failed: 401 Unauthorized"**
- Token may have expired. The skill auto-refreshes tokens, but check that `FHIR_CLIENT_SECRET` is current.
- Confirm your app registration is approved and not in sandbox-only mode.

**"Patient not found"**
- Try searching by MRN instead of name (name matching varies by EHR).
- Check that your app has `Patient.read` and `Patient.search` scopes granted.

**"Missing vitals / labs in output"**
- The patient may not have recent observations in the EHR.
- The agent will flag missing data sections in the draft and prompt you to fill them in manually.

**"SMART on FHIR scopes error"**
- Ensure your registered app includes these scopes:
  `patient/Patient.read patient/Condition.read patient/MedicationRequest.read patient/Observation.read patient/Encounter.read`

**Sandbox mode not working**
- Public HAPI sandbox: `https://hapi.fhir.org/baseR4`
- Confirm `FHIR_SANDBOX_MODE=true` is set and `FHIR_BASE_URL` is unset or points to the sandbox.

---

## Example Workflows

### Full outpatient visit workflow
```
User: "Pull patient Jane Doe, DOB 1968-03-22, from the FHIR server."
Agent: [Fetches Patient, Condition, MedicationRequest, Observation]
       "Found Jane Doe (MRN 7823991). Active conditions: HTN, T2DM, CKD stage 2.
        Current meds: Lisinopril, Metformin, Amlodipine. Last vitals: 3 weeks ago."

User: "She's here for a diabetes follow-up. Chief complaint: fatigue, better than last visit.
       Draft a SOAP note."
Agent: [Generates full SOAP note with populated O section from FHIR data]
       "Here is the draft SOAP note. Vitals from today's visit are missing —
        please add them before signing."
```

### Quick prior auth
```
User: "Generate a prior auth for Ozempic for this patient — payer is Aetna."
Agent: [Pulls active conditions, labs (HbA1c), current meds]
       "Draft PA narrative ready. Diagnosis: T2DM (E11.9). Supporting:
        HbA1c 8.4% (2026-02-01), inadequate response to Metformin 2000mg.
        Do you want to add any additional clinical notes before I finalize?"
```

---

## Version History

| Version | Date       | Changes                              |
|---------|------------|--------------------------------------|
| 1.0.4   | 2026-03-29 | Fixed misleading ANTHROPIC_API_KEY comment; clarified patient_context is forwarded to Anthropic when backend is used; added CORS production warning. |
| 1.0.3   | 2026-03-29 | Fixed env var declarations (moved optional vars out of requiredEnv); added ANTHROPIC_API_KEY to optionalEnv with context; added PHI/privacy warning. |
| 1.0.0   | 2026-03-29 | Initial release. SOAP, referral, prior auth, discharge, AVS. SMART on FHIR auth. Sandbox mode. |

---

*Questions or issues? Open a GitHub issue or reach out via the OpenClaw Discord.*
