# MTM/CMR Optimization

## Table of Contents
1. [Context: Why CMR Infrastructure Matters Now](#context-why-cmr-infrastructure-matters-now)
2. [CMR as a Star Measure](#cmr-as-a-star-measure)
3. [CMR Candidate Prioritization](#cmr-candidate-prioritization)
4. [Structuring CMRs for Clinical Impact](#structuring-cmrs-for-clinical-impact)
5. [Cross-Measure Alignment](#cross-measure-alignment)
6. [Completion Rate Optimization](#completion-rate-optimization)

---

## Context: Why CMR Infrastructure Matters Now

CMS's CY2027 proposed rule removes 12 measures from Star Ratings — mostly administrative and process measures. The clinical measures that remain carry a larger share of the overall rating. CMR completion rate (D13) is not being removed, and CMS decided not to retire it despite considering doing so. With expanded MTM eligibility criteria effective 2025, the eligible population has grown — which means both the opportunity and the operational challenge have increased. Plans that build CMR infrastructure now will be positioned to perform when the measure matters most.

---

## CMR as a Star Measure

### D13 — MTM Completion Rate for CMR

- **What it measures**: Percentage of MTM-enrolled members who received a CMR
- **Scoring status**: Display-only through MY2026 (not scored toward Star Rating). CMS decided NOT to retire the measure — the 2026 Rate Announcement (April 2025) confirmed it will remain due to expanded MTM eligibility requirements. Scoring is expected to resume in MY2027 (impacting 2029 Star Ratings), per industry analysis including Arine's own published strategy guidance. **Verify scoring timeline annually against the most recent CMS Technical Notes and Rate Announcement.**
- **Why it matters now**: Even while display-only, CMS is collecting and publishing the data. Plans that ignore this measure will be caught off-guard when scoring resumes. Build infrastructure now.

### CMS MTM Program Eligibility (Current Criteria — Effective January 1, 2025)

The CY2024 Final Rule (April 2024) established expanded MTM targeting criteria effective January 1, 2025:

- **Chronic conditions**: ≥3 chronic conditions from the **10 core chronic diseases** (plans must target all 10):
  1. Alzheimer's disease
  2. Bone disease — arthritis (osteoporosis, osteoarthritis, rheumatoid arthritis)
  3. Chronic heart failure
  4. Chronic kidney disease
  5. Diabetes
  6. Dyslipidemia
  7. End-stage liver disease
  8. HIV/AIDS
  9. Hypertension
  10. Mental health (depression, schizophrenia, bipolar disorder, chronic/disabling mental health conditions)
- **Medications**: ≥2-8 Part D covered medications (plans set threshold within this range; CMS proposed lowering the maximum from 8 to 5 but did NOT finalize this change)
- **Cost threshold**: Likely to exceed **$1,276 in 2026** in annual Part D drug costs (indexed annually in the CMS Call Letter — always check the current year's threshold)
- Plans may use lower thresholds for any criteria (and many do to maximize intervention reach)

> **⚠️ DENOMINATOR TRAP**: Lowering MTM eligibility thresholds expands the D13 denominator. If
> outreach capacity doesn't scale proportionally, completion rate drops. A plan that voluntarily
> lowers thresholds or that sees expanded eligibility from the 2025 criteria changes without
> adding pharmacist capacity may inadvertently hurt D13 performance. CMS estimated a 2-3x
> increase in eligible population from the original proposed criteria changes, though the actual
> increase is smaller because the drug count threshold was not lowered from 8 to 5.

### The Completion Rate Problem
Many plans chase CMR completion rate as a checkbox: call the member, get them on the phone for 15 minutes, document the CMR, move on. This hits the numerator but wastes a clinical touchpoint. The skill should optimize for both completion AND clinical impact.

---

## CMR Candidate Prioritization

### Prioritization Matrix

Score each MTM-eligible member on two axes:
1. **Clinical complexity** — how much benefit could a CMR deliver?
2. **Completion likelihood** — how likely is the member to engage?

#### Clinical Complexity Scoring

| Factor | Points | Rationale |
|--------|--------|-----------|
| Open adherence gap on triple-weighted measure (D10/D11/D12) | +5 | CMR directly addresses Star measure |
| ≥12 concurrent medications | +4 | High polypharmacy burden, more DRPs likely |
| Recent hospitalization (≤90 days) | +4 | Transition of care = medication discrepancies |
| High-risk medication per AGS Beers (≥65 years) | +3 | Deprescribing opportunity |
| A1C ≥9% or BP >150/90 | +3 | Uncontrolled chronic condition |
| COB flag (concurrent opioid + benzo) | +3 | Safety concern + Star measure impact |
| ≥3 prescribers | +2 | Fragmented care, reconciliation needed |
| Renal/hepatic impairment | +2 | Dose adjustment opportunities |
| Recent formulary change or generic conversion | +1 | Confusion, potential non-adherence |

#### Completion Likelihood Scoring

| Factor | Points | Rationale |
|--------|--------|-----------|
| Completed CMR in prior year | +4 | Strong predictor of repeat engagement |
| Engaged with pharmacy (≥1 call answered in past 6 months) | +3 | Reachable member |
| Preferred language = English (or bilingual pharmacist available) | +2 | Reduces barrier |
| Has caregiver on file | +2 | Alternative contact for engagement |
| Multiple failed contact attempts | -3 | Resource drain, consider alternative channels |
| Cognitive impairment documented | -1 | May need caregiver involvement (not a disqualifier). **CMS allows caregiver-assisted CMRs — per 42 CFR § 423.153(d)(1)(vii)(B)(2), if the beneficiary is unable to accept the offer to participate, the MTM provider may perform the CMR with the beneficiary's prescriber, caregiver, or other authorized representative. Without noting this, teams skip cognitively impaired patients entirely and lose completions they could have captured.** |
| Declined CMR previously | -2 | Respect autonomy, try different approach |

#### Combined Priority Score
```
CMR Priority = Clinical_Complexity × Completion_Likelihood_Modifier
```

- **Tier 1** (Score ≥30): Schedule first, assign to senior clinical pharmacist
- **Tier 2** (Score 15-29): Schedule in standard rotation
- **Tier 3** (Score <15): Batch outreach, consider abbreviated review if resources are limited

---

## Structuring CMRs for Clinical Impact

### Beyond the Checkbox: Clinical Framework

A CMR that just verifies the medication list is a waste of a pharmacist's time. Structure every CMR around three pillars:

#### Pillar 1 — Medication Reconciliation
- Verify every active medication against fill data, provider records, and patient report
- Identify discrepancies: medications on the list not being taken, medications being taken not on the list
- Flag duplications, therapeutic overlaps, and missing therapies
- **Output**: Accurate, reconciled medication list

#### Pillar 2 — Drug Therapy Problem Identification
- Screen for DRPs using structured categories:
  - Unnecessary drug therapy
  - Needs additional therapy (gaps in evidence-based treatment)
  - Ineffective drug (wrong drug for condition)
  - Dose too low / too high
  - Adverse drug reaction
  - Drug-drug interactions (often the highest-severity finding in polypharmacy CMRs — screen explicitly using interaction databases, flag severity as major/moderate/minor with clinical significance)
  - Non-adherence (with root cause assessment)
- Prioritize DRPs by clinical severity and actionability
- **Output**: Prioritized DRP list with recommendations for prescriber

#### Pillar 3 — Star Measure Integration
- For every CMR, explicitly check:
  - Is this member below 80% PDC on any triple-weighted measure?
  - Is this member on the COB or Poly-ACH numerator?
  - Does this member qualify for SUPD but lack a statin fill?
  - Are there 90-day supply or mail order conversion opportunities?
- **Output**: Measure-specific interventions documented and tracked

### CMR Documentation Standards
- Use CMS-required format: Personal Medication List (PML) + Medication Action Plan (MAP)
- Include specific, actionable recommendations (not generic "discuss with doctor")
- Document prescriber outreach and outcomes
- Track DRP resolution rates — this is your quality metric
- CMS encourages beneficiaries to bring their PML and MAP to their annual wellness visit or any medical encounter — reinforce this during every CMR

---

## Cross-Measure Alignment

### Using CMRs to Move Multiple Measures Simultaneously

Every CMR is an opportunity to impact multiple Star measures in a single encounter:

| During CMR, Check For | Star Measure Impacted |
|----------------------|----------------------|
| PDC gap on diabetes meds | D10 (3× weight) |
| PDC gap on RAS antagonists | D11 (3× weight) |
| PDC gap on statins | D12 (3× weight) |
| No statin fill in diabetic patient 40-75 | D14 (SUPD) |
| Concurrent opioid + benzo use | COB (inverse) |
| High-risk med in elderly per Beers | Poly-ACH (inverse) |
| CMR completed | D13 |

A single well-executed CMR for a complex patient can impact 3-5 measures. This is the efficiency argument for investing in clinical pharmacist-led CMRs rather than checkbox completions.

### Cross-Measure Conflict Resolution
Sometimes measure optimization conflicts. Never sacrifice clinical judgment for a measure.

**Example 1 — Psychiatric Beers medication:**
- Patient on a Beers-listed medication for a valid psychiatric indication (BCPP territory)
- Stopping the medication helps Poly-ACH but may destabilize the patient
- **Resolution**: Document clinical rationale. Flag the conflict. Psychiatric stability takes precedence.

**Example 2 — Concurrent opioid + benzodiazepine (COB + Poly-ACH):**
- Patient on long-term low-dose benzodiazepine for GAD plus chronic opioid for pain
- Hits both COB and Poly-ACH measures simultaneously
- Abrupt benzodiazepine discontinuation is clinically dangerous — seizure risk, rebound anxiety, withdrawal
- **Resolution**: Document rationale. Attempt gradual taper if clinically appropriate (e.g., 10-25% reduction every 2-4 weeks). Never deprescribe unsafely to hit a measure. If taper is not appropriate, document why and accept the measure impact. This is a common scenario that Stars programs handle badly when driven by claims analysts instead of clinical pharmacists.

---

## Completion Rate Optimization

### Outreach Strategy

| Channel | Best For | Completion Rate |
|---------|----------|----------------|
| Telephonic (pharmacist-led) | Complex patients, relationship-based | Highest |
| Video/telehealth | Tech-comfortable patients, visual aid helpful | High |
| In-person (community pharmacy) | Patients who prefer face-to-face | High but limited scale |
| Asynchronous (portal-based review) | Simple med lists, engaged patients | Moderate |

### Scheduling Optimization
- **Avoid Q4 surge**: Spread CMRs across the year; Q4-only strategy leads to rushed, low-quality encounters
- **Pair with refill calls**: When a pharmacy calls about a refill, offer CMR scheduling
- **Post-discharge window**: 7-14 days after hospitalization — highest clinical relevance, member is engaged
- **Annual wellness visit alignment**: Coordinate with PCP AWV for comprehensive encounter

### Tracking Metrics
- **Completion rate**: Numerator/denominator (the Star measure)
- **Time-to-CMR post-MTM enrollment**: Days from MTM enrollment to CMR completion. Plans that enroll members in MTM but delay the CMR for months lose completions as members disenroll, become unreachable, or the measurement year ends. **Best practice target: CMR within 60 days of MTM enrollment.**
- **DRP identification rate**: Average DRPs per CMR (target: ≥2 actionable DRPs per CMR)
- **DRP resolution rate**: Percentage of identified DRPs with prescriber follow-through
- **Measure conversion rate**: Members who cross 80% PDC threshold after CMR intervention
- **Cost avoidance**: Hospitalization/ED visit reduction in CMR-completed population vs. matched controls
