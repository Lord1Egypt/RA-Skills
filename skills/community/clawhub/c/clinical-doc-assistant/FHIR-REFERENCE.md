# FHIR R4 Reference — Clinical Documentation Assistant

This reference covers FHIR resource mappings, query patterns, and data extraction logic used by the skill. Read this if you're customizing the skill, debugging data retrieval, or integrating with a non-standard FHIR server.

---

## Resource Mapping by Document Type

| Document Type       | FHIR Resources Used                                              |
|---------------------|------------------------------------------------------------------|
| SOAP Note           | Patient, Condition, MedicationRequest, Observation, Encounter    |
| Referral Letter     | Patient, Condition, MedicationRequest, Observation, Practitioner |
| Prior Auth          | Patient, Condition, MedicationRequest, Observation, Coverage     |
| Discharge Summary   | Patient, Condition, Procedure, MedicationRequest, Encounter      |
| After-Visit Summary | Patient, Condition, MedicationRequest, Appointment              |

---

## Key FHIR Query Patterns

### Active conditions with ICD-10 codes
```
GET /Condition?patient={id}&clinical-status=active&_include=Condition:asserter
```
Extract: `code.coding[system="http://hl7.org/fhir/sid/icd-10-cm"].code`

### Current medications
```
GET /MedicationRequest?patient={id}&status=active&_include=MedicationRequest:medication
```
Extract: `medicationCodeableConcept.text` or `medicationReference`

### Vital signs (last 10)
```
GET /Observation?patient={id}&category=vital-signs&_sort=-date&_count=10
```
LOINC codes for common vitals:
- BP systolic: `8480-6`
- BP diastolic: `8462-4`
- Heart rate: `8867-4`
- Weight: `29463-7`
- BMI: `39156-5`
- O2 sat: `2708-6`

### HbA1c
```
GET /Observation?patient={id}&code=4548-4&_sort=-date&_count=3
```
LOINC: `4548-4` (Hemoglobin A1c/Hemoglobin.total in Blood)

### Basic metabolic panel
```
GET /Observation?patient={id}&code=24323-8&_sort=-date&_count=1
```

### Insurance/coverage (for prior auth)
```
GET /Coverage?patient={id}&status=active
```
Extract: `payor[0].display`, `subscriberId`, `class[type=plan].value`

---

## ICD-10 to Clinical Text Mapping

The skill maps common ICD-10 codes to plain-English descriptions for patient-facing documents:

| ICD-10  | Description                          |
|---------|--------------------------------------|
| E11.9   | Type 2 Diabetes Mellitus             |
| I10     | Essential (primary) hypertension     |
| E78.5   | Hyperlipidemia, unspecified          |
| N18.2   | Chronic kidney disease, stage 2      |
| J44.1   | COPD with acute exacerbation         |
| F32.1   | Major depressive disorder, moderate  |
| M54.5   | Low back pain                        |
| Z79.4   | Long-term use of insulin             |

For codes not in the local map, the skill falls back to `Condition.code.text` from the FHIR response.

---

## SMART on FHIR Token Flow

```
1. Agent reads FHIR_TOKEN_URL, FHIR_CLIENT_ID, FHIR_CLIENT_SECRET
2. POST to token URL:
   grant_type=client_credentials
   client_id={FHIR_CLIENT_ID}
   client_secret={FHIR_CLIENT_SECRET}
   scope=system/Patient.read system/Condition.read ...
3. Receive: access_token, expires_in
4. All FHIR requests: Authorization: Bearer {access_token}
5. Auto-refresh when token is within 60s of expiry
```

For **Epic SMART on FHIR**, use JWT-based auth (backend services):
- Generate RSA key pair
- Register public key in Epic's developer portal
- Sign JWT with private key, send as `client_assertion`

---

## Handling Pagination

FHIR servers paginate large result sets. The skill follows `Bundle.link[relation=next]` automatically:

```
GET /Condition?patient=123&_count=50
→ Bundle with 50 entries + link.next
→ GET {link.next url}
→ Continue until no next link
```

For document generation, the skill caps retrieval at:
- Conditions: 100 (all active)
- Medications: 50 (active only)
- Observations: 20 most recent per category
- Encounters: 10 most recent

---

## Sandbox Test Patient IDs (HAPI Public Server)

For testing without real patient data:

| Patient ID  | Description                        |
|-------------|------------------------------------|
| `example`   | Basic adult patient                |
| `pat1`      | Patient with conditions and meds   |
| `pat2`      | Pediatric patient                  |

Base URL: `https://hapi.fhir.org/baseR4`

Example: `GET https://hapi.fhir.org/baseR4/Patient/pat1`

---

## EHR-Specific Notes

### Epic
- Requires app registration at https://fhir.epic.com
- Non-production apps get sandbox access immediately
- Production requires Epic review (2–4 weeks)
- Use JWT auth for backend (server-to-server) integrations

### Cerner
- Register at https://code.cerner.com
- Millennium FHIR endpoint pattern: `https://{tenant}.cernerworks.com/fhir/r4`
- Supports standard OAuth2 client credentials

### Azure Health Data Services
- FHIR service URL from Azure Portal
- Auth via Azure AD: set `FHIR_TENANT_ID`
- Managed Identity supported for Azure-hosted deployments

### HAPI FHIR (self-hosted)
- Full R4 compliance
- No auth required in default config
- Ideal for on-premise clinic deployments

---

*See SKILL.md for usage instructions and trigger phrases.*
