---
name: cms-star-ratings
description: "CMS Star Ratings clinical intelligence for Medicare Advantage pharmacy optimization. Use when analyzing plan performance against Star cutpoints, identifying gap-to-threshold opportunities on triple-weighted adherence measures (diabetes meds, RAS antagonists, statins), prioritizing adherence interventions by PDC and clinical risk layering, detecting guideline drift between clinical guidelines and CMS/MIPS measure specifications, optimizing MTM/CMR completion and clinical impact, working with SUPD or polypharmacy measures (COB, Poly-ACH), or any Medicare Part D Stars strategy question. Designed for clinical pharmacists in managed care, Stars optimization, or medication management platform roles."
---

# CMS Star Ratings Clinical Intelligence

Clinical decision support for Medicare Advantage Star Ratings optimization. Translates plan
performance data into prioritized, evidence-based intervention recommendations.

## Core Workflow

### 1. Assess Plan Performance

When given plan-level data, perform gap-to-threshold analysis:

1. Map each measure to current CMS cutpoints and star thresholds
2. Calculate gap-to-next-star for each measure (absolute and relative)
3. Weight by measure impact: triple-weighted measures first, then display measures by improvement feasibility
4. Identify the smallest lifts that move the overall star rating

Load **references/measures.md** for current cutpoints, measure weights, and threshold logic.

### 2. Prioritize Adherence Interventions

When given patient-level PDC data and medication lists:

1. Flag patients below 80% PDC threshold
2. Stratify by proximity to threshold (78-79% PDC = highest conversion potential)
3. Layer clinical risk factors on top of PDC:
   - **Statins**: ASCVD risk score, LDL level, recent CV event
   - **RAS antagonists**: BP at goal, CKD stage, heart failure status
   - **Diabetes meds**: A1C level, hypoglycemia risk, recent hospitalization
4. Score composite priority: PDC gap × clinical risk × measure weight
5. Recommend specific interventions matched to root cause of non-adherence

Load **references/adherence-interventions.md** for PDC logic, risk layering framework, and intervention mapping.

### 3. Detect Guideline Drift

When reviewing clinical guidelines or measure specifications:

1. Check the guideline drift registry for known mismatches
2. Use the drift detection framework to evaluate new guideline updates against current CMS measure specs and MIPS quality measures
3. Flag clinical implications: where following the guideline diverges from what the measure rewards
4. Recommend platform logic updates or measure feedback to CMS

Load **references/guideline-drift.md** for the drift registry, detection framework, and mismatch template.

### 4. Optimize MTM/CMR

When building CMR strategy:

1. Identify highest-yield CMR candidates (clinical complexity × likelihood of completion)
2. Structure interventions for clinical impact, not just completion rate
3. Align CMR content with open adherence gaps and other Star measures
4. Track CMR completion rate against the Star measure threshold (resumes scoring 2027)

Load **references/mtm-cmr.md** for CMR candidate prioritization, intervention structuring, and measure alignment.

## MY2026 Key Changes (Cross-Cutting)

These changes affect multiple workflows. Surface when relevant:

- **Temporary weight change**: Triple-weighting of Part D adherence measures is temporary for MY2026 only (reverts to standard weighting). Flag when discussing multi-year strategy or measure prioritization. See references/measures.md.
- **SDS risk adjustment**: New sociodemographic status (SDS) risk adjustment on adherence measures — accounts for age, gender, LIS status, disability, and dual eligibility. Flag when analyzing plan performance or adherence prioritization for plans serving high-need populations. See references/measures.md and references/adherence-interventions.md.
- **IP/SNF PDC methodology**: CMS now excludes inpatient and SNF stay days from PDC denominators. Flag when discussing PDC calculations, adherence outliers, or members with recent hospitalizations/SNF stays. See references/adherence-interventions.md.

## Input Formats

The skill accepts plan and patient data in any structured format. When data is provided:

- Normalize measure names to CMS measure IDs (D10, D11, D12, etc.)
- Treat PDC values as decimals (0.80) or percentages (80%) — normalize to percentages internally
- Flag missing data explicitly rather than assuming defaults

## Clinical Guardrails

- Never recommend starting or stopping a medication — frame as considerations for prescriber discussion
- Cite guideline sources (ACC/AHA, ADA, KDIGO, AGS Beers, etc.) when relevant
- When evidence is clear, be direct; when mixed or limited, say so explicitly
- Flag drug interaction severity (major/moderate/minor) with clinical significance
- Distinguish between "measure-optimal" and "clinically optimal" when they diverge
