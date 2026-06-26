# CMS Star Ratings Measures Reference

## Table of Contents
1. [Context: Why These Measures Matter More in 2027+](#context-why-these-measures-matter-more-in-2027)
2. [Triple-Weighted Part D Adherence Measures](#triple-weighted-part-d-adherence-measures)
3. [Other Key Part D Measures](#other-key-part-d-measures)
4. [Cutpoint Thresholds](#cutpoint-thresholds)
5. [Gap-to-Threshold Analysis Framework](#gap-to-threshold-analysis-framework)
6. [Measure Weight Impact on Overall Rating](#measure-weight-impact-on-overall-rating)

---

## Context: Why These Measures Matter More in 2027+

CMS's CY2027 proposed rule removes 12 measures from Star Ratings — seven focused on operational and administrative performance, three on process of care, and two on patient experience. The Part D adherence measures (D10, D11, D12) are NOT being removed. With fewer measures in the overall calculation, the triple-weighted adherence measures carry an even larger share of the total star rating. Every percentage point of improvement on these measures is worth more going forward than it was before.

### MY2026 Temporary Weight Change

For Measurement Year 2026 ONLY, CMS is temporarily reducing the triple-weighted adherence measures (D10, D11, D12) to single-weighted (1×). They are expected to return to triple-weighted (3×) in MY2027. This temporary change means the adherence measures carry less relative weight in the 2028 Star Ratings (which use MY2026 data) — but plans should NOT reduce adherence investment. The measures return to 3× weight the following year, and backsliding during a single-weight year makes recovery harder when the weight increases again.

### MY2026 Sociodemographic Status (SDS) Risk Adjustment

Starting MY2026, CMS will apply sociodemographic status (SDS) risk adjustment to adherence scores. Adherence measures will now account for age, gender, low-income subsidy (LIS) status, disability status, and dual eligibility. This means plans serving high-need populations may see adjusted scores that better reflect the difficulty of achieving adherence in those populations. Monitor how SDS adjustment affects your plan's specific scores relative to cutpoints.

### MY2026 PDC Calculation Change — IP/SNF Stays

Starting MY2026, days when members are hospitalized or in skilled nursing facilities (SNFs) will NO LONGER be excluded from PDC calculations. Previously, inpatient days were removed from the denominator. Now they count — which means members with hospitalizations may show lower PDC scores even if they were adherent before and after the stay. This is a methodology change that could lower PDC rates across the board and must be factored into gap-to-threshold projections.

---

## Triple-Weighted Part D Adherence Measures

These carry 3× weight in the overall star calculation. Small improvements here have outsized
impact on the overall star rating. With CY2027 measure removals, the relative weight of these measures increases further.

### D10 — Medication Adherence for Diabetes Medications
- **Numerator**: Members with PDC ≥ 80% for oral diabetes medications
- **Denominator**: Members with ≥2 fills of oral diabetes medications in the measurement year
- **Drug classes**: Biguanides (metformin), sulfonylureas (glipizide, glimepiride, glyburide), TZDs (pioglitazone, rosiglitazone), DPP-4 inhibitors (sitagliptin, saxagliptin, linagliptin, alogliptin), SGLT2 inhibitors (canagliflozin, dapagliflozin, empagliflozin, ertugliflozin), meglitinides (repaglinide, nateglinide), alpha-glucosidase inhibitors (acarbose, miglitol)
- **SGLT2 inhibitor note**: SGLT2 inhibitors are oral diabetes medications and ARE included in D10. Given the rapid expansion of SGLT2 inhibitor prescribing for diabetes, heart failure, and CKD, confirm that your platform correctly includes these agents in the D10 denominator. Patients prescribed an SGLT2 inhibitor primarily for heart failure or CKD (with or without diabetes) may appear in the D10 denominator if they also have diabetes medication claims — cross-reference diagnosis codes.
- **Exclusions**: Members with ESRD, insulin-only regimens. **Note: patients on insulin + oral agents (combo) ARE included — only insulin-only is excluded.**
- **Weight**: 3× (temporarily reduced to 1× for MY2026 only; returns to 3× in MY2027)
- **Note**: GLP-1 RAs are NOT currently included in the D10 adherence measure denominator (D10 covers oral agents only; GLP-1 RAs are injectable). However, CMS has discussed potential inclusion as the diabetes treatment landscape evolves and GLP-1 RA use increases dramatically. Verify GLP-1 RA status against the current year's CMS Technical Notes before each measurement year.

### D11 — Medication Adherence for RAS Antagonists
- **Numerator**: Members with PDC ≥ 80% for RAS antagonists
- **Denominator**: Members with ≥2 fills of ACEIs, ARBs, or direct renin inhibitors
- **Drug classes**: ACEIs, ARBs, aliskiren, ACEI/CCB combinations, ARB/CCB combinations
- **Inclusions**: Sacubitril/valsartan (Entresto) IS included — the ARB component (valsartan) counts toward D11 RAS adherence. Do not mistakenly exclude ARNI patients from the denominator. **Verification note**: Confirm ARNI inclusion against the current year's CMS Technical Notes. While clinically logical (the product contains valsartan, an ARB), explicit CMS confirmation in the measure specification is prudent, especially as ARNI prescribing volume grows in heart failure populations.
- **Exclusions**: None specific beyond standard measure exclusions (hospice, ESRD where applicable)
- **Weight**: 3× (temporarily reduced to 1× for MY2026 only; returns to 3× in MY2027)

### D12 — Medication Adherence for Cholesterol (Statins)
- **Numerator**: Members with PDC ≥ 80% for statin medications
- **Denominator**: Members with ≥2 fills of statin medications
- **Drug classes**: All statins including combination products (statin + ezetimibe, statin + CCB)
- **Exclusions**: Ezetimibe monotherapy, PCSK9 inhibitors (evolocumab, alirocumab), bempedoic acid, and inclisiran (PCSK9-pathway siRNA agent) are NOT included. Inclisiran lowers LDL but is not a statin — do not assume it counts toward D12.
- **Weight**: 3× (temporarily reduced to 1× for MY2026 only; returns to 3× in MY2027)

---

## Other Key Part D Measures

### D14 — Statin Use in Persons with Diabetes (SUPD)
- **Numerator**: Members with diabetes aged 40-75 who received a statin fill
- **Denominator**: Members aged 40-75 with diabetes (≥2 fills of diabetes meds OR diabetes diagnosis)
- **Exclusions**: Members with ESRD, hospice, rhabdomyolysis history
- **Weight**: 1×
- **Note**: Binary measure — any statin fill counts, not adherence-based

> **⚠️ CRITICAL: SUPD ≠ Statin Adherence.** SUPD (D14) requires only ONE statin fill during
> the measurement year. D12 (Statin Adherence) requires PDC ≥80%. These are different measures
> with different denominators. **A member who fills a statin once for SUPD but does not continue
> enters the D12 denominator as a non-adherent member — improving D14 while HURTING D12.**
> Every SUPD statin initiation MUST include an adherence support plan from day one. Failing to
> coordinate SUPD and D12 interventions is the single most common cross-measure mistake in Stars
> optimization. Do not initiate a statin for SUPD without a plan to keep the member adherent.

### D13 — MTM Completion Rate for CMR
- **Numerator**: Members who received a CMR
- **Denominator**: Members enrolled in MTM program
- **Weight**: 1×
- **Scoring status**: CMS decided NOT to retire the CMR completion rate measure. The measure remains on the display page. Verify the exact scoring timeline (display-only vs. scored) against the current year's CMS Technical Notes and the most recent Rate Announcement. **Verification note**: The 2026 Rate Announcement confirmed the measure will remain; verify whether scoring resumes in measurement year 2027 or remains display-only longer.
- **Note**: Regardless of exact scoring timeline, build CMR infrastructure now. Plans that wait until the measure scores again will be caught off-guard. See mtm-cmr.md for optimization logic.

### Polypharmacy Measures

#### COB — Concurrent Use of Opioids and Benzodiazepines
- **Numerator**: Members with ≥2 fills of an opioid AND ≥2 fills of a benzodiazepine with ≥30 concurrent days
- **⚠️ INVERSE MEASURE — lower rate = better performance.** A high rate is BAD. Improvement means REDUCING the numerator. When reporting plan rates, always label directionality.
- **Weight**: 1×

#### Poly-ACH — Use of High-Risk Medications in the Elderly (Anticholinergic Burden)
- **Numerator**: Members ≥65 with ≥2 fills of high-risk medications per AGS Beers Criteria
- **⚠️ INVERSE MEASURE — lower rate = better performance.** A high rate is BAD. Improvement means REDUCING the numerator (deprescribing, switching to safer alternatives). When reporting plan rates, always label directionality.
- **Weight**: 1×
- **Key drug classes**: First-generation antihistamines (diphenhydramine, hydroxyzine), tertiary TCAs (amitriptyline, doxepin), antispasmodics, skeletal muscle relaxants (cyclobenzaprine, methocarbamol), non-benzo hypnotics (zolpidem), certain antiarrhythmics (amiodarone for rhythm control in elderly), long-acting sulfonylureas (glyburide) in older adults
- **Note**: This is not exhaustive — reference the full AGS Beers Criteria list for comprehensive screening. Beers Criteria is updated approximately every 4 years (most recent 2023, next update expected ~2027).

---

## Cutpoint Thresholds

CMS publishes cutpoints annually. These shift based on national performance distribution.

### 2025 Star Rating Year Cutpoints (Reference)

Note: 2026 Star Ratings cutpoints have been published by CMS in the 2026 Star Ratings Data Tables, available at cms.gov/medicare/health-drug-plans/part-c-d-performance-data. Verify against the 2026 cutpoints for current analysis. The table below uses 2025 values as a reference baseline.

| Measure | 2-Star | 3-Star | 4-Star | 5-Star |
|---------|--------|--------|--------|--------|
| D10 Diabetes Adherence | <72% | 72-79% | 80-86% | ≥87% |
| D11 RAS Adherence | <74% | 74-81% | 82-87% | ≥88% |
| D12 Statin Adherence | <73% | 73-80% | 81-87% | ≥88% |
| D14 SUPD | <78% | 78-82% | 83-86% | ≥87% |
| D13 MTM/CMR | <60% | 60-74% | 75-89% | ≥90% |

> **Important**: Cutpoints shift annually based on clustering methodology. Always verify against
> the current year's **CMS Medicare Advantage and Part D Star Ratings Technical Notes**,
> published annually and available at **cms.gov/medicare/health-drug-plans/part-c-d-performance-data**.
> The above are representative thresholds — use actual published cutpoints for live plan analysis.

### Cutpoint Methodology
- CMS uses a clustering algorithm (not fixed percentiles) to set thresholds
- Cutpoints can tighten when national performance improves
- Plans must monitor mid-year performance against BOTH current and projected cutpoints

---

## Gap-to-Threshold Analysis Framework

### Input Required
- Plan-level performance rate for each measure (percentage)
- Current CMS cutpoints for the measurement year
- Plan's current overall star rating

### Analysis Steps

1. **Calculate absolute gap**: `threshold - plan_rate` for each measure at each star level
2. **Identify nearest achievable threshold**: The next star level up where the gap is smallest
3. **Estimate member impact**: `gap × eligible_denominator = members needed to convert`
4. **Rank by effort-to-impact ratio**: 
   - `impact_score = measure_weight × star_level_change / members_to_convert`
   - Triple-weighted measures get 3× multiplier
5. **Flag cliff measures in BOTH directions**:
   - **Upside cliff**: Where the plan is within 2% of reaching the NEXT star level
   - **Downside cliff**: Where the plan is within 5% of DROPPING a star level
   - Run both checks on every measure, every time. A plan focused only on climbing can backslide and lose a star it already had — especially on triple-weighted measures where that loss is 3× as damaging.

### Output Format

For each measure, report:
- Current rate and star level
- **Upside gap**: Distance to next star threshold (absolute % and member count)
- **Downside gap**: Distance to dropping a star level (absolute % and member count)
- **Cliff alert** (if within 2% upside or 5% downside) — label clearly as OFFENSIVE or DEFENSIVE
- Weighted impact score
- Recommended intervention focus

### Critical Thresholds

The 3-star to 4-star boundary is the most valuable:
- Plans at 3.5+ stars qualify for quality bonus payments (QBP)
- QBP can represent millions in additional revenue
- A single triple-weighted measure moving from 3-star to 4-star can shift the overall rating

---

## Measure Weight Impact on Overall Rating

### How Weights Work
- Part D measures are weighted and combined with Part C measures for overall star rating
- Triple-weighted measures (D10, D11, D12) have 3× impact on the Part D summary
- Part D summary contributes to overall star rating alongside Part C, CAHPS, and HOS
- With CY2027 removing 12 measures (mostly administrative), the remaining clinical measures — including all Part D adherence measures — carry a proportionally larger share of the overall rating

### Strategic Prioritization
1. **First priority**: Triple-weighted adherence measures below 4-star cutpoint
2. **Second priority**: Any measure at risk of dropping a star level (defensive)
3. **Third priority**: SUPD (1× weight but often high-volume, easy intervention — coordinate with D12)
4. **Fourth priority**: Polypharmacy measures (inverse — identify members driving the numerator)
5. **Fifth priority**: MTM/CMR (build infrastructure now regardless of scoring timeline)
