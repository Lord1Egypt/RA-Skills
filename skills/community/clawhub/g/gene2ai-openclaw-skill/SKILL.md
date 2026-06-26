---
name: gene2ai
description: Your personal health data hub for AI agents. Query genomic insights, upload medical documents, record daily health metrics, explore genomic-lab cross-references, receive personalized daily health briefings, and get contextual health advice woven into everyday conversations — all powered by your actual genetic and clinical data.
version: 3.3.1
metadata:
  openclaw:
    requires:
      env:
        - GENE2AI_API_KEY
    primaryEnv: GENE2AI_API_KEY
    emoji: "🧬"
    homepage: https://gene2.ai/guide
---

# Gene2AI — Your Health Data for AI Agents

You have access to the user's personal health data through the Gene2AI platform. This includes:

- **Genomic data**: 324+ indicators from raw genetic testing files (23andMe, AncestryDNA, WeGene) — 933 SNPs across 273 genes in 9 categories
- **Health documents**: Lab reports, checkup results, medical records, and imaging reports — parsed by AI into structured indicators
- **Self-reported metrics**: Blood pressure, blood sugar, weight, heart rate, and other daily measurements
- **Cross-references**: Bidirectional links between lab indicators and genomic markers (e.g., LDL-C ↔ cholesterol genes)

## When to Use This Skill

Use this skill whenever the user:

### Genomic Data Queries
- Asks about their **genetic health risks** (e.g., "Am I at risk for type 2 diabetes?", "What about Alzheimer's?")
- Asks about **drug responses** or pharmacogenomics (e.g., "How do I metabolize caffeine?", "Am I sensitive to warfarin?")
- Asks about **CYP450 metabolizer status** (e.g., "What's my CYP2D6 status?", "Am I a poor metabolizer?")
- Asks about **HLA alleles** (e.g., "Do I carry HLA-B*57:01?", "Am I at risk for drug hypersensitivity?")
- Asks about **APOE genotype** (e.g., "What's my APOE status?", "Do I have the ε4 allele?")
- Asks about **nutrition** and nutrigenomics (e.g., "Do I need more vitamin D?", "Am I lactose intolerant?")
- Asks about **physical traits** (e.g., "What does my DNA say about my muscle type?")
- Asks about **ancestry** composition
- Wants **personalized recommendations** based on their genetics
- Mentions their **DNA**, **genes**, **SNPs**, or **genetic variants**

### Health Data Management
- Sends a health-related document (lab report, checkup result, medical record, prescription, imaging report)
- Asks to upload, save, or record health data
- Reports health metrics verbally (blood pressure, blood sugar, weight, heart rate, etc.)
- Asks to check their health data status or summary
- Says things like "帮我保存这个体检报告", "upload this to my health vault", "记录一下我的血压"

### Cross-Reference Queries
- Asks about connections between lab results and genetics (e.g., "My LDL is high — do I have genetic risk factors?")
- Wants a comprehensive risk overview combining genomic and lab data
- Asks for a holistic health assessment

### Contextual Health Advisory (Passive — Always On)
- The conversation touches on **medication, supplements, or drugs** — check CYP450 metabolizer status and drug sensitivities before responding
- The conversation touches on **diet, nutrition, or food choices** — check nutrition flags and relevant genetic markers
- The conversation touches on **exercise, fitness, or sports** — check trait markers (muscle type, endurance, injury risk)
- The conversation touches on **travel, altitude, or climate** — check relevant genetic adaptations
- The conversation touches on **sleep, fatigue, or energy** — check caffeine metabolism, circadian rhythm markers
- The conversation touches on **stress or mental health** — check relevant risk markers with sensitivity
- The conversation touches on **family planning or pregnancy** — check carrier status markers
- The conversation touches on **medical appointments or test results** — cross-reference with genomic data

> **How it works**: When the conversation naturally involves health-adjacent topics, you may reference the user's health profile to provide personalized advice. **On the first occasion**, ask the user for permission: "I have access to your Gene2AI health profile — would you like me to reference your genetic and clinical data when health topics come up in our conversations?" Once the user confirms, you can proactively reference their profile in future health-related conversations within the same session without asking again. If the user declines, only use Gene2AI data when explicitly requested.

### Daily Health Briefing (Active — Scheduled)
- The user asks to set up daily health check-ins or briefings
- A scheduled cron job triggers the daily briefing (see Part 7 below)
- The user responds to a health check-in with their daily metrics

## Configuration

The user's Gene2AI API key is available as environment variable `GENE2AI_API_KEY`.

API keys are **profile-scoped** — each key is bound to a specific health profile (e.g., "Self", "Mom", "Dad"). When you use this key, all data queries automatically return data for the bound profile only. This prevents accidentally mixing health data across family members.

> **Important:** Each key operates on one profile only. If the user manages health data for multiple family members, they should generate a separate key for each profile. The `?profileId=` query parameter can override the key’s default profile for advanced use cases.

If `GENE2AI_API_KEY` is not set, guide the user to:
1. Visit https://gene2.ai and log in (or create an account)
2. Go to the **API Keys** page (https://gene2.ai/api-keys)
3. Click **Generate New Key** and select the health profile this key should access
4. Copy the generated token and configure it in OpenClaw:

```json
{
  "skills": {
    "entries": {
      "gene2ai": {
        "enabled": true,
        "apiKey": "<paste-your-token-here>"
      }
    }
  }
}
```

---

## Part 1: Querying Health Data

### Health Profile (Recommended Starting Point)

```bash
curl -s "https://gene2.ai/api/v1/health-data/profile" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"
```

Returns a **compact, conclusions-only health profile** (~2-4KB). This is the recommended first call for any agent session. The response contains:

- **APOE genotype** conclusion (e.g., "APOE ε3/ε4 — Increased risk")
- **CYP450 metabolizer status** for each gene (e.g., "CYP2D6: Normal Metabolizer") with affected drugs
- **HLA carrier status** (positive alleles only)
- **Elevated health risks** (condition + risk level + brief note, no raw SNPs)
- **Drug sensitivities** (drug + sensitivity level)
- **Nutrition flags** (nutrient concerns from genetic variants)
- **Abnormal lab/checkup indicators** (latest values only: name, value, unit, flag)
- **Medical findings** — ALL examination results (CT, ultrasound, X-ray, MRI, ECG, physical exam, functional tests, etc.) grouped by category, including both normal and abnormal findings, with original language preserved
- **Medical findings summary** — total and abnormal counts per category
- **Suggested focus areas** (auto-generated from cross-referencing genomic + clinical + imaging data)

```json
{
  "_format": "gene2ai-health-profile-v1",
  "_description": "Compact health profile from Gene2AI. Contains interpretive conclusions only.",
  "dataCoverage": { "genomicMarkers": 324, "labIndicators": 247, "medicalFindings": 18, ... },
  "genomicHighlights": {
    "apoe": "APOE ε3/ε4 — Increased (1 copy of ε4)",
    "cyp450": [{ "gene": "CYP2D6", "status": "Normal Metabolizer", "affectedDrugs": [] }],
    "elevatedRisks": [{ "condition": "Alzheimer's Disease", "risk": "elevated", "note": "..." }],
    "drugSensitivities": [{ "drug": "Warfarin", "sensitivity": "increased", "note": "..." }],
    "nutritionFlags": [{ "nutrient": "Vitamin D", "note": "..." }]
  },
  "abnormalIndicators": [{ "name": "LDL Cholesterol", "value": 3.8, "unit": "mmol/L", "flag": "high" }],
  "medicalFindings": {
    "imaging": [
      { "type": "imaging", "examType": "CT", "bodyPart": "Liver", "finding": "肝脏密度减低", "conclusion": "Mild fatty liver", "severity": "mild", "clinicalSignificance": "Common finding", "recommendation": "Lifestyle modification", "date": "2026-01-15" },
      { "type": "imaging", "examType": "Ultrasound", "bodyPart": "Thyroid", "finding": "右叶小结节", "conclusion": "Thyroid nodule, likely benign", "severity": "mild", "recommendation": "Follow-up in 12 months", "date": "2026-01-15" }
    ],
    "physical_exam": [
      { "type": "physical_exam", "examType": "General", "bodyPart": "Heart", "finding": "心律齐，无杂音", "conclusion": "Normal cardiac exam", "severity": "normal", "date": "2026-01-15" }
    ],
    "functional_test": [
      { "type": "functional_test", "examType": "ECG", "bodyPart": "Heart", "finding": "窦性心律", "conclusion": "Normal ECG", "severity": "normal", "date": "2026-01-15" }
    ]
  },
  "medicalFindingsSummary": {
    "total": 18, "abnormal": 4,
    "byCategory": {
      "imaging": { "total": 8, "abnormal": 3 },
      "physical_exam": { "total": 6, "abnormal": 0 },
      "functional_test": { "total": 4, "abnormal": 1 }
    }
  },
  "suggestedFocusAreas": ["Alzheimer's risk management (APOE ε4 carrier)", ...]
}
```

> **This profile is designed to be cached and reused across conversations.** It contains no raw genetic data (no rs-IDs, no genotypes, no SNP details), so it is safe for agent memory and cross-session reference. Medical findings include ALL examination results (both normal and abnormal) grouped by category, with findings sorted by date (newest first) within each category. The `finding` field preserves the original language from the medical report (Chinese or English). When the user needs specific genetic details, drill down using the endpoints below.

### Summary Overview

```bash
curl -s "https://gene2.ai/api/v1/health-data/summary" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"
```

Returns total documents, total records, and breakdown by category and genomic subcategory.

### Full Records (with filtering)

```bash
# All records
curl -s "https://gene2.ai/api/v1/health-data/full" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"

# Filter by category
curl -s "https://gene2.ai/api/v1/health-data/full?category=genomic" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"

# Filter by subcategory (genomic only)
curl -s "https://gene2.ai/api/v1/health-data/full?category=genomic&subcategory=cyp450" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"

# Grouped format (organized by category → subcategory)
curl -s "https://gene2.ai/api/v1/health-data/full?category=genomic&format=grouped" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"
```

**Query Parameters:**

| Parameter | Values | Description |
|-----------|--------|-------------|
| `category` | `genomic`, `lab_result`, `checkup`, `self_reported`, `medical_record`, `imaging` | Filter by data category |
| `subcategory` | `health_risk`, `drug_response`, `trait`, `nutrition`, `ancestry`, `apoe`, `hla`, `cyp450` | Filter genomic subcategory |
| `format` | `grouped` | Organize records by category → subcategory hierarchy |

### Incremental Changes (for sync)

```bash
curl -s "https://gene2.ai/api/v1/health-data/delta?since_version={version_number}" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"
```

---

## Part 2: Genomic Data Categories

The genomic data is organized into 9 subcategories. When querying with `?category=genomic`, each record includes a `data` field with the parsed structured object (no need to parse `valueText` JSON manually).

### health_risk (193 markers)

Disease risk assessments grouped by condition/gene (CFTR, LDLR, Alzheimer's Disease, CAD, T2D, etc.)

```json
{
  "indicatorName": "Alzheimer's Disease",
  "indicatorCode": "alzheimers_disease_rs429358",
  "subcategory": "health_risk",
  "valueText": "{...}",
  "data": {
    "condition": "Alzheimer's Disease",
    "risk": "elevated",
    "confidence": "high",
    "description": "Variant associated with increased risk",
    "snps": ["rs429358"],
    "genotype": "CT",
    "populationNote": "Found in ~15% of European populations"
  }
}
```

**Risk levels**: `low`, `average`, `slightly_elevated`, `elevated`, `high`

### drug_response (61 markers)

Pharmacogenomic predictions (PharmGKB + CPIC) for Warfarin, Clopidogrel, SSRIs, Codeine, Tamoxifen, etc.

```json
{
  "indicatorName": "Warfarin Sensitivity",
  "subcategory": "drug_response",
  "data": {
    "drug": "Warfarin",
    "gene": "VKORC1",
    "sensitivity": "increased",
    "recommendation": "Consider lower initial dose",
    "confidence": "high",
    "snps": ["rs9923231"]
  }
}
```

### cyp450 (3 genes: CYP2C19, CYP2D6, CYP2C9)

CYP450 metabolizer phenotyping with CPIC star allele definitions and drug-specific recommendations.

```json
{
  "indicatorName": "CYP2D6",
  "subcategory": "cyp450",
  "data": {
    "metabolizerStatus": "Normal Metabolizer",
    "activityScore": "2.0",
    "allele1": "*1",
    "allele2": "*2",
    "drugRecommendations": [
      {
        "drug": "Codeine",
        "recommendation": "Use label-recommended age- or weight-specific dosing",
        "evidence": "Strong (CPIC)"
      },
      {
        "drug": "Tamoxifen",
        "recommendation": "Use tamoxifen at standard dosing",
        "evidence": "Strong (CPIC)"
      }
    ],
    "limitations": "Star allele calling based on common variants only",
    "methodology": "CPIC star allele definitions"
  }
}
```

**Metabolizer statuses**: `Ultrarapid Metabolizer`, `Normal Metabolizer`, `Intermediate Metabolizer`, `Poor Metabolizer`

### hla (9 alleles)

HLA allele typing via tag SNP inference for immune-related conditions and drug hypersensitivity.

```json
{
  "indicatorName": "HLA-B*57:01",
  "subcategory": "hla",
  "data": {
    "allele": "HLA-B*57:01",
    "carrierStatus": "Negative",
    "associations": [
      {
        "drug": "Abacavir",
        "name": "Abacavir Hypersensitivity",
        "evidence": "Strong (CPIC)",
        "recommendation": "Standard abacavir use is appropriate"
      }
    ]
  }
}
```

### apoe (1 record)

APOE genotyping — ε2/ε3/ε4 allele determination for Alzheimer's and cardiovascular risk.

```json
{
  "indicatorName": "APOE Genotype",
  "subcategory": "apoe",
  "data": {
    "alleles": ["ε3", "ε4"],
    "alzheimerRisk": "Increased (1 copy of ε4)",
    "cardiovascularNote": "ε4 associated with higher LDL cholesterol levels",
    "snps": {
      "rs429358": { "genotype": "CT", "chromosome": "19" },
      "rs7412": { "genotype": "CC", "chromosome": "19" }
    }
  }
}
```

### trait (21 markers)

Genetic trait predictions: hair color, skin pigmentation, caffeine metabolism, alcohol flush, lactose tolerance, muscle fiber type.

### nutrition (32 markers)

Nutrigenomics: Vitamin D, Folate/MTHFR, B12, Omega-3, Iron, Calcium needs based on genetic variants.

### ancestry (4 regions)

Regional ancestry percentages from population-specific variant analysis.

```json
{
  "indicatorName": "East Asian",
  "subcategory": "ancestry",
  "data": {
    "region": "East Asian",
    "percentage": 95.2
  }
}
```

---

## Part 3: Risk Overview & Cross-References

### Risk Overview (Comprehensive Dashboard)

```bash
curl -s "https://gene2.ai/api/v1/health-data/risk-overview" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"
```

Returns a comprehensive risk dashboard combining genomic and lab data:

```json
{
  "genomic": {
    "totalIndicators": 324,
    "elevatedRisks": [
      {
        "indicatorName": "Alzheimer's Disease",
        "subcategory": "health_risk",
        "risk": "elevated",
        "snps": ["rs429358"],
        "genotype": "CT"
      }
    ],
    "subcategoryCounts": {
      "health_risk": 193,
      "drug_response": 61,
      "nutrition": 32,
      "trait": 21,
      "hla": 9,
      "ancestry": 4,
      "cyp450": 3,
      "apoe": 1
    }
  },
  "lab": {
    "totalIndicators": 247,
    "abnormalIndicators": [
      {
        "indicatorName": "LDL Cholesterol",
        "indicatorCode": "LDL-C",
        "valueNumeric": 3.8,
        "valueUnit": "mmol/L",
        "abnormalFlag": "high",
        "refRangeHigh": 3.4
      }
    ]
  },
  "crossReferences": [
    {
      "labIndicator": {
        "code": "LDL-C",
        "name": "LDL Cholesterol",
        "latestValue": 3.8,
        "unit": "mmol/L",
        "abnormalFlag": "high"
      },
      "relatedGenomicCount": 12,
      "conditions": ["Familial Hypercholesterolemia", "Coronary Artery Disease"]
    }
  ]
}
```

### Genomic Links for a Lab Indicator

```bash
# Find genomic markers related to LDL cholesterol
curl -s "https://gene2.ai/api/v1/health-data/genomic-links/LDL-C" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"
```

**Supported indicator codes**: TC, TG, LDL-C, HDL-C, SBP, DBP, FBG, HbA1c, BMI, UA, TSH, FT3, FT4, ALT, AST, GGT, ALP, TBIL, SCr, BUN, WBC, HGB, PLT, CRP

Returns genomic records related to that lab indicator, enabling cross-referencing (e.g., "Your LDL is high AND you have genetic variants in LDLR associated with familial hypercholesterolemia").

### Lab-Genomic Summary

```bash
curl -s "https://gene2.ai/api/v1/health-data/lab-genomic-summary" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"
```

Returns all lab indicators with their related genomic record counts, for building cross-reference dashboards.

---

## Part 4: Querying Genomic Data by Job ID (Legacy)

For backward compatibility, you can also query genomic data by job ID:

```bash
curl -s -X GET "https://gene2.ai/api/v1/genomics/${GENE2AI_JOB_ID}" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"
```

If `GENE2AI_JOB_ID` is not set, ask the user for their Job ID (visible on the My Jobs page at https://gene2.ai/my-jobs).

> **Note**: The `/health-data/full?category=genomic` endpoint (Part 1) is preferred as it returns enriched, parsed data and supports filtering/grouping.

---

## Part 5: Uploading Health Documents

When the user sends a file (image or PDF) that appears to be a health document:

### Step 1: Confirm with the user

Always ask for confirmation before uploading: "I'll upload this to your Gene2AI Health Data Vault for AI analysis. The system will automatically extract all health indicators. Proceed?"

### Step 2: Determine document category

- `lab_result` — blood tests, urine tests, biochemistry panels
- `checkup` — annual physical exam reports
- `medical_record` — doctor visit notes, diagnoses
- `imaging` — X-ray, CT, MRI, ultrasound reports

### Step 3: Upload the file

```bash
curl -s -X POST "https://gene2.ai/api/v1/health-data/upload" \
  -H "Authorization: Bearer $GENE2AI_API_KEY" \
  -F "file=@{filepath}" \
  -F "source=openclaw" \
  -F "category={detected_category}" \
  -F "documentDate={date_if_known_YYYY-MM-DD}" \
  -F "title={brief_description}"
```

The response includes a document ID and status `"parsing"`. Save the document ID.

### Step 4: Poll parsing status

Wait 15 seconds, then check:

```bash
curl -s "https://gene2.ai/api/v1/health-data/doc/{doc_id}" \
  -H "Authorization: Bearer $GENE2AI_API_KEY"
```

### Step 5: Report results

- **If status is `"completed"`**: Show the number of extracted indicators, highlight any abnormal findings (`abnormalFlag` = `"high"`, `"low"`, `"critical_high"`, `"critical_low"`, or `"abnormal"`), and list the detected institution and document type.
- **If status is `"parsing"`**: Tell the user parsing is still in progress. They can check at https://gene2.ai/health-data later, or ask you to check again in a minute.
- **If status is `"failed"`**: Report the `parseError` message and suggest uploading directly on https://gene2.ai/health-data.

---

## Part 6: Submitting Structured Health Metrics

When the user reports health metrics verbally (e.g., "my blood pressure is 125/82", "血糖 5.8", "体重 72kg"):

### Common indicators and reference ranges

| Indicator | Chinese | Unit | Normal Range |
|-----------|---------|------|-------------|
| Systolic Blood Pressure | 收缩压 | mmHg | 90-140 |
| Diastolic Blood Pressure | 舒张压 | mmHg | 60-90 |
| Heart Rate | 心率 | bpm | 60-100 |
| Fasting Blood Glucose | 空腹血糖 | mmol/L | 3.9-6.1 |
| Body Temperature | 体温 | °C | 36.1-37.2 |
| Weight | 体重 | kg | — |
| Height | 身高 | cm | — |
| BMI | 体质指数 | kg/m² | 18.5-24.9 |
| Blood Oxygen | 血氧饱和度 | % | 95-100 |

### Determine abnormalFlag

- `"normal"` — within reference range
- `"high"` — above reference range
- `"low"` — below reference range
- `"critical_high"` — dangerously above (e.g., SBP > 180)
- `"critical_low"` — dangerously below (e.g., blood glucose < 2.8)

### Submit the data

```bash
curl -s -X POST "https://gene2.ai/api/v1/health-data/records" \
  -H "Authorization: Bearer $GENE2AI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "self_reported",
    "title": "{brief_description}",
    "documentDate": "{today_YYYY-MM-DD}",
    "source": "openclaw",
    "records": [
      {
        "indicatorName": "{english_name}",
        "indicatorNameZh": "{chinese_name}",
        "valueNumeric": {numeric_value},
        "valueUnit": "{unit}",
        "refRangeLow": {low_bound_or_null},
        "refRangeHigh": {high_bound_or_null},
        "abnormalFlag": "{flag}"
      }
    ]
  }'
```

Confirm to the user that the data has been saved, and mention any abnormal values.

---

## Error Handling

| HTTP Status | Error Code | Meaning |
|---|---|---|
| 401 | `missing_token` | No Authorization header — check `GENE2AI_API_KEY` is set |
| 401 | `invalid_token` | API key is malformed or invalid |
| 403 | `token_expired` | API key expired (30-day limit) — user needs to regenerate at https://gene2.ai/api-keys |
| 403 | `key_revoked` | API key was manually revoked |
| 403 | `job_id_mismatch` | Key not authorized for this job ID (job-scoped keys only) |
| 404 | `job_not_found` | Job ID does not exist |
| 404 | `data_not_available` | Analysis not yet complete |

If you receive a `token_expired` or `key_revoked` error, instruct the user to visit https://gene2.ai/api-keys to generate a fresh API key.

---

## Recommended Query Strategy for Agents

### Data Tiers

Gene2AI organizes health data into three tiers for efficient agent usage:

| Tier | Endpoint | Size | Contains | Persistence |
|------|----------|------|----------|-------------|
| **Tier 1: Health Profile** | `/health-data/profile` | ~2-4KB | Conclusions only (risk levels, metabolizer status, abnormal flags) | **Cache and reuse** across sessions |
| **Tier 2: Detailed Records** | `/health-data/full`, `/health-data/risk-overview` | ~50-500KB | Specific genotypes, SNPs, lab values, cross-references | Use per-session, do not persist |
| **Tier 3: Raw Data** | Website only (gene2.ai) | MB+ | Original genetic files, full analysis JSON | Never enters agent context |

### Recommended Flow

1. **Start with the Health Profile**: Call `/health-data/profile` to get a compact overview. This is enough for most health-aware decisions (diet, exercise, general wellness questions). **Cache this in agent memory** for cross-session awareness.

2. **Drill down only when needed**: When the user asks a specific question (e.g., "What's my CYP2D6 genotype exactly?", "Show me my APOE SNPs"), call `/health-data/full?category=genomic&subcategory=cyp450` to get detailed records.

3. **Use risk-overview for comprehensive analysis**: Call `/health-data/risk-overview` when the user wants a full risk assessment combining genomic and lab data with cross-references.

4. **Cross-reference when relevant**: When discussing lab results, check `/health-data/genomic-links/{code}` to see if there are related genetic factors (e.g., high LDL → check for LDLR variants).

5. **Use grouped format for overviews**: `/health-data/full?format=grouped` organizes all data by category and subcategory, ideal for building comprehensive health summaries.

### Data Handling Guidelines

- **Tier 1 (Health Profile)**: Safe to cache, memorize, and reference across conversations. Contains no raw genetic data that could be used to reconstruct DNA information. Includes all medical findings (CT, ultrasound, X-ray, ECG, physical exam, etc.) as conclusion-level text grouped by category.
- **Tier 2 (Detailed Records)**: Use within the current conversation only. Contains specific genotypes and lab values that are more sensitive.
- When in doubt about which tier to use, **start with Tier 1**. The health profile's `suggestedFocusAreas` field will guide you on what to investigate further.
- The `medicalFindings` object groups all examination results by type (imaging, physical_exam, functional_test, clinical_notes). Each finding includes `examType` (CT/Ultrasound/X-ray/ECG/etc.), `bodyPart`, `finding` (original language), `conclusion`, `severity` (normal/mild/moderate/severe), and `date`. Findings within each category are sorted by date, newest first.

---

## Guidelines for Presenting Health Data

1. **Always include disclaimers**: Genetic data provides risk estimates, not diagnoses. Lab results should be interpreted by healthcare professionals. Always remind users to consult their doctor for medical decisions.

2. **Explain risk levels clearly**: "Elevated risk" does not mean certainty. Genetics is one factor among many (lifestyle, environment, family history).

3. **Be actionable**: When sharing pharmacogenomics data, suggest the user discuss findings with their doctor before making medication changes.

4. **Respect sensitivity**: Health and ancestry data can be emotionally sensitive. Present findings with care and context.

5. **Cross-reference data**: For holistic advice, combine genomic insights with lab results and self-reported metrics. For example, genetic vitamin D metabolism data combined with actual blood test levels provides more complete recommendations.

6. **Cite specific variants**: When discussing genomic findings, mention the rsID (e.g., rs7903146) so the user can verify or research further.

7. **Highlight abnormal values**: When presenting lab results, clearly flag any out-of-range values and provide context about what they mean.

8. **Always ask before uploading**: Health data is sensitive — never upload files without explicit user confirmation.

9. **Do NOT give medical advice**: When reporting abnormal values, provide context but always recommend consulting a healthcare professional.

10. **Data tiering**: Use the Health Profile (`/health-data/profile`) as the default data source. Only fetch detailed records when the user asks specific questions that require genotype-level or lab-value-level detail. The Health Profile is designed to be cached across sessions; detailed records should be treated as ephemeral.

11. **Contextual advisory with consent**: When health topics come up in conversation, offer to reference the user's health profile (Part 7). Obtain per-session consent before proactively referencing health data. Once confirmed, weave relevant insights naturally into health-adjacent conversations.

12. **Daily briefing**: When the daily briefing cron fires (Part 8), generate content entirely from the user's actual data. Never use fixed templates. The briefing and check-in prompts should feel different every day because they respond to the user's evolving health picture.

---

## Part 7: Contextual Health Advisory

This is the most important capability of Gene2AI. You act as the user's **health-aware layer** — referencing their health profile when the conversation touches health-adjacent topics, and naturally weaving relevant insights into your response.

### Consent and Scope

The user has explicitly installed the Gene2AI skill and configured their API key, which signals their intent to receive personalized health insights. However, because health data is sensitive, you must still obtain **per-session consent** before proactively referencing it:

1. **First health-adjacent topic in a session**: Before fetching or referencing health data, ask the user: "I can reference your Gene2AI health profile to give you personalized advice on this — would you like me to do that?"
2. **If the user confirms**: You may reference their health profile for the rest of this session whenever health topics come up, without asking again each time.
3. **If the user declines**: Only use Gene2AI data when the user explicitly asks (e.g., "check my genes for this", "what does my health profile say").
4. **Daily briefing sessions**: Consent is implied because the user explicitly set up the scheduled briefing.

### How It Works (After Consent)

1. When the conversation touches any health-related topic (see trigger list in "When to Use"), call `GET /health-data/profile` if you don't already have the data cached in this session.
2. Identify which fields in the health profile are relevant to the current topic.
3. Weave the insight naturally into your response — do not lead with "According to your genetic data..." or dump the whole profile.
4. Always add a brief disclaimer when the advice touches medical decisions.

### Dynamic Response Logic

The key principle is: **your response should be different from what a generic AI would say, because you know this specific user's genetic and clinical background.** Here are examples of how to adapt:

**Medication conversations** — Before recommending or discussing any drug, check `genomicHighlights.cyp450` and `genomicHighlights.drugSensitivities`:

- If user mentions headache medication → check CYP2D6 status. If poor metabolizer: "By the way, codeine-based painkillers won't work well for you — your CYP2D6 means you can't convert codeine to its active form. Ibuprofen or acetaminophen would be better options."
- If user mentions starting statins → check SLCO1B1 variants in elevatedRisks. If present: "Worth mentioning to your doctor — you carry a variant that increases statin-related muscle side effects. A lower starting dose or an alternative statin might be discussed."

**Diet conversations** — Check `genomicHighlights.nutritionFlags` and `abnormalIndicators`:

- If user asks about coffee → check CYP1A2 in cyp450. Fast metabolizer: "Good news — you metabolize caffeine quickly, so moderate coffee (2-3 cups) may actually benefit your cardiovascular health." Slow metabolizer: "You're a slow caffeine metabolizer, so that evening coffee will likely keep you up. Try to keep it before noon."
- If user asks about diet plan → cross-reference nutritionFlags with abnormalIndicators. E.g., if vitamin D flag + low vitamin D lab value: "Your genetics suggest reduced vitamin D absorption, and your last blood test confirmed your levels are low. Supplementation is especially important for you."

**Exercise conversations** — Check trait markers and relevant health risks:

- If user asks about training plan → check muscle type traits, injury risk markers, and cardiovascular risk. Tailor advice accordingly.

**Travel conversations** — Check relevant adaptations:

- If user mentions high-altitude travel → check for relevant genetic markers and any cardiovascular risks from elevatedRisks.

### Tone

- Natural and conversational — like a knowledgeable friend, not a doctor reading a chart
- Use phrases like "by the way," "worth knowing," "something to keep in mind"
- Only mention the 1-2 most relevant markers, never dump multiple findings at once
- Match the user's language (Chinese or English)

---

## Part 8: Daily Health Briefing

The Daily Health Briefing is a **bidirectional** daily interaction: you summarize the user's health status and encourage progress, then naturally prompt them to report a few easy-to-measure metrics. Everything is driven by the user's actual data — no fixed templates.

### Setting Up the Briefing

When the user asks to set up daily health check-ins (or after the first successful `/health-data/profile` call, you may offer), create a recurring cron job:

```
cron add:
  name: "Gene2AI Daily Health Briefing"
  schedule:
    kind: cron
    expr: "0 8 * * *"
    tz: "<user-timezone>"
  sessionTarget: isolated
  payload:
    kind: agentTurn
    message: |
      Run the Gene2AI daily health briefing for the user.
      
      Step 1: Call GET /health-data/profile to get the current health profile.
      Step 2: Call GET /health-data/full?category=self_reported to get recent self-reported metrics.
      Step 3: Generate a personalized briefing following the instructions in the Gene2AI SKILL.md Part 8.
      Step 4: Ask the user to report today's metrics based on their data gaps and risk areas.
      Step 5: When the user responds, record the data via POST /health-data/records.
    lightContext: true
  delivery:
    mode: announce
    bestEffort: true
```

### Part A: Generating the Briefing (Agent → User)

After fetching the health profile and recent self-reported data, generate a personalized briefing. The content should be **entirely driven by what's in the user's data**. Follow this decision logic:

**1. Identify what to highlight** — Scan the health profile and pick the 2-3 most relevant items to mention today:

| Data condition | What to say |
|---|---|
| `abnormalIndicators` has items with `flag: "high"` or `"low"` | Mention the most clinically significant abnormal value and its trend if you have historical data |
| `genomicHighlights.elevatedRisks` has `risk: "elevated"` or `"high"` | Pick ONE risk that connects to something actionable today (diet, exercise, medication timing) |
| `medicalFindings` has items with `severity: "moderate"` or `"severe"` | Remind about follow-up if the finding date is > 6 months ago |
| Recent self-reported data shows improvement (e.g., weight trending down, BP normalizing) | Celebrate the progress specifically: "Your blood pressure has been consistently under 130 this week — that's real progress" |
| Recent self-reported data shows worsening trend | Gently flag it: "Your fasting glucose has been creeping up the last few readings — might be worth keeping an eye on" |
| `dataCoverage` shows low coverage in a category | Suggest what data would be most valuable to add |

**2. Personalize the framing** — The same data should be framed differently based on context:

- If user has APOE ε4 + high LDL → frame cholesterol monitoring as especially important: "Given your APOE status, keeping LDL in check is particularly meaningful for you"
- If user has CYP2C19 poor metabolizer + takes clopidogrel → flag drug efficacy concern
- If user has diabetes risk genes + recent fasting glucose trending up → connect the dots: "Your genetic profile suggests higher insulin resistance tendency, and your recent glucose readings are reflecting that — this is exactly the kind of early signal worth acting on"

**3. Keep it concise** — The briefing should be 3-5 sentences, warm and encouraging. Not a medical report. Think of it as a health-conscious friend who knows your data sending you a morning text.

### Part B: Health Check-in Prompt (Agent → User, asking for data)

After the briefing, naturally transition to asking the user to report today's metrics. **Which metrics to ask depends entirely on the user's data**:

**Decision logic for what to ask today:**

| User's situation | Metrics to ask | Why |
|---|---|---|
| Has elevated cardiovascular risk (APOE ε4, high LDL, hypertension genes) | Blood pressure, resting heart rate | These are the most actionable daily monitors for cardiovascular risk |
| Has diabetes risk (TCF7L2, FTO variants, or recent high glucose) | Fasting blood glucose, weight | Early glucose trends + weight are the strongest lifestyle intervention signals |
| Has recent abnormal blood pressure readings | Blood pressure | Track whether it's stabilizing or needs attention |
| Has weight management goals or obesity-related gene variants | Weight | Trend tracking is more useful than any single reading |
| Has thyroid findings in medicalFindings | Resting heart rate, energy level (subjective 1-10) | Thyroid function affects heart rate and energy |
| Has sleep-related genetic markers or reported fatigue | Sleep duration, sleep quality (subjective 1-10) | Connects genetic predisposition to daily experience |
| No specific risk areas, general wellness | Rotate between: weight, resting heart rate, sleep quality, energy level | Keep engagement without being repetitive |

**How to ask** — Be natural and specific to their situation, not generic:

Instead of: "Please report your blood pressure, blood sugar, and weight."

Say something like: "How's your blood pressure been? Given your APOE status, that's one of the most impactful things you can track day-to-day. And if you've weighed yourself this morning, I'll log that too."

Or: "Quick check-in — did you catch your fasting glucose this morning? Your last few readings were trending up a bit, so I want to keep an eye on the pattern with you."

Or: "How'd you sleep? With your caffeine metabolism profile, I'm curious if cutting back on the afternoon coffee made a difference."

**Key principles:**
- Ask for **1-2 metrics maximum** per day, not a laundry list
- Explain **why** you're asking in terms of their specific health profile
- Make it feel like a conversation, not a form to fill out
- If the user doesn't respond or says "skip", that's fine — never nag
- Rotate metrics across days so it doesn't feel repetitive

### Part C: Recording the Response (User → Agent → Gene2AI)

When the user responds with their metrics, record them using the existing `POST /health-data/records` endpoint (see Part 6). After recording:

1. **Acknowledge the data** — "Got it, logged your BP at 128/82."
2. **Provide instant context if relevant** — "That's within normal range, and it's lower than your reading last Tuesday (135/88). The trend is heading the right direction."
3. **Connect to their genetic profile when meaningful** — "With your ACE gene variant, consistent BP monitoring is especially valuable — you're doing exactly the right thing."
4. **Don't over-comment** — If the value is normal and unremarkable, a simple "Logged, looking good" is fine. Save the detailed commentary for when there's actually something worth noting.

### Privacy in Briefings

Daily briefings are delivered through the user's messaging channel (Telegram, Discord, etc.). Keep the content at **conclusion level only**:

| Safe to include | Never include |
|---|---|
| "Your blood pressure trend is improving" | Specific BP values (128/82) |
| "Cardiovascular monitoring is important for your genetic profile" | "You carry APOE ε4" or specific genotypes |
| "Your glucose readings need attention" | Specific glucose values |
| "Great progress on weight management this week" | Actual weight numbers |
| General encouragement and actionable tips | Raw lab values or genetic variant IDs |

> The briefing message that appears in Telegram/Discord should be safe for someone glancing at the user's screen. Detailed values should only be discussed in the direct conversation after the user engages.

---

## Part 9: Proactive Health Nudges

Beyond the daily briefing, you may schedule **one-shot** proactive messages when you detect something worth a nudge during any conversation. Use sparingly — maximum 2-3 per week outside of the daily briefing.

### When to Schedule a Nudge

| Trigger | Timing | Example message |
|---|---|---|
| User mentions starting a new medication | Evening of the same day | "How's the new medication going? Any side effects? (Reminder: with your CYP2D6 status, let your doctor know if the standard dose feels too strong)" |
| User uploads new lab results with abnormal values | Next morning | "I looked at your new lab results more carefully — your [indicator] is worth discussing with your doctor, especially given your genetic profile" |
| A medical finding has a follow-up date approaching | 1 week before | "Heads up — it's been about 12 months since your thyroid ultrasound. Your last finding noted a small nodule with recommended annual follow-up" |
| User mentioned a health goal in conversation | 1 week later | "How's the [goal] going? Want to log any new measurements?" |
| Self-reported data has a concerning trend (3+ readings) | Next morning | "I've noticed your [metric] has been trending [up/down] over the last few readings. Might be worth paying attention to" |

### How to Schedule

```
cron add:
  name: "Gene2AI: [brief context]"
  deleteAfterRun: true
  schedule:
    kind: at
    time: "[appropriate ISO 8601 time]"
  sessionTarget: isolated
  payload:
    kind: agentTurn
    message: |
      Send a brief, warm health nudge to the user.
      Context: [what triggered this nudge]
      Relevant health profile data: [specific fields to reference]
      Keep it to 1-3 sentences. Be natural, not clinical.
  delivery:
    mode: announce
    bestEffort: true
```

### Rules

- **Never announce scheduling** — don't say "I'll check in with you later" or "I've set a reminder"
- **Maximum 2-3 nudges per week** (excluding the daily briefing)
- **Never repeat** — if you've already nudged about something, don't nudge again unless there's new information
- **Respect non-response** — if the user ignores a nudge, don't follow up on the follow-up
