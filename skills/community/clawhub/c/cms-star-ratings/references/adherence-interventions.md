# Adherence Intervention Logic

## Table of Contents
1. [Context: Why Adherence Measures Matter More in 2027+](#context-why-adherence-measures-matter-more-in-2027)
2. [PDC Fundamentals](#pdc-fundamentals)
3. [Patient Prioritization Framework](#patient-prioritization-framework)
4. [Clinical Risk Layering](#clinical-risk-layering)
5. [Composite Priority Scoring](#composite-priority-scoring)
6. [Root Cause Analysis and Intervention Mapping](#root-cause-analysis-and-intervention-mapping)
7. [Intervention Timing](#intervention-timing)
8. [Important Considerations](#important-considerations)

---

## Context: Why Adherence Measures Matter More in 2027+

CMS's CY2027 proposed rule removes 12 measures from Star Ratings — mostly administrative and process measures where plans showed little performance variation. The Part D adherence measures (D10, D11, D12) are NOT being removed. With fewer measures in the overall calculation, the triple-weighted adherence measures carry an even larger share of the total star rating. Every percentage point of PDC improvement is worth more going forward than it was before. Plans that relied on easy administrative measures to pad their star rating will lose that safety net. Clinical measures — especially adherence — are now the game.

Additionally, starting MY2026, CMS is applying sociodemographic status (SDS) risk adjustment to adherence measures — accounting for age, gender, LIS status, disability, and dual eligibility. Plans serving high-need populations may see adjusted scores. The priority scoring in this skill focuses on clinical risk layering at the individual member level, which complements but is distinct from the plan-level SDS adjustment.

Note: For MY2026 only, adherence measures (D10, D11, D12) are temporarily reduced from triple-weighted (3×) to single-weighted (1×). They return to 3× in MY2027. This does not change the clinical importance of adherence — it temporarily reduces the measure's mathematical impact on the star rating. Do not reduce adherence investment during this window.

---

## PDC Fundamentals

### Calculating PDC
- PDC = (days covered by medication in measurement period) / (days in measurement period) × 100
- Threshold: ≥80% = adherent
- Each fill's days supply covers specific dates; overlapping fills shift forward
- Only the measurement year counts — carryover from prior year fills applies to day 1

### Key PDC Nuances
- **Switching within class**: If a patient switches from lisinopril to losartan (ACEI to ARB), both count toward D11 PDC — the class is RAS antagonists, not individual drugs
- **Combination products**: Amlodipine/valsartan counts for D11 (RAS component)
- **90-day fills**: Dramatically improve PDC — a single 90-day fill covers a quarter of the year
- **Late fills**: A fill on December 1 for 30-day supply only covers 31 days of the year (Dec 1-31), but it converts the member to 80%+ if they were at ~72% through November

### MY2026 PDC Methodology Change — IP/SNF Stays
Starting MY2026, days when members are hospitalized or in skilled nursing facilities are NO LONGER excluded from PDC calculations. Previously, inpatient days were removed from the denominator, effectively "pausing" the PDC clock during a hospitalization. Now those days count toward the denominator. This means:
- Members with hospitalizations may show lower PDC scores even if adherent before and after the stay
- Post-discharge medication reconciliation becomes even more critical — ensure the member restarts fills immediately after discharge
- Plans should model the PDC impact of this change on their current population to recalibrate gap-to-threshold projections
- Pair this with CMR outreach in the 7-14 day post-discharge window (see mtm-cmr.md)

### PDC Calculation Variability
PDC is not calculated identically across all platforms and PBMs. Differences in how overlapping fills, mid-year switches, hospital days, and early refills are handled can produce different PDC values for the same patient. When working with a platform like Arine, understand how their specific PDC engine handles these edge cases — a 1-2% difference in calculation methodology can move a patient across the 80% threshold in either direction. Always verify the platform's calculation logic against the CMS Technical Notes specification for the applicable measurement year.

---

## Patient Prioritization Framework

### Tier 1: High-Conversion Patients (PDC 75-79%)
- Within striking distance of 80% threshold
- Often need only 1-2 additional fills or a fill timing adjustment
- Highest ROI per intervention dollar
- **Action**: Immediate outreach — refill reminder, 90-day conversion, mail order

### Tier 2: Moderate-Gap Patients (PDC 60-74%)
- Need sustained engagement, not a single touchpoint
- Often have identifiable barriers (cost, side effects, complexity)
- **Action**: Barrier assessment, medication synchronization, prescriber collaboration

### Tier 3: Significant-Gap Patients (PDC below 60%)
- May have discontinued intentionally or been lost to follow-up
- Requires clinical assessment — is non-adherence clinically appropriate?
- **Action**: Clinical review first — confirm therapy is still indicated before pushing adherence

### Tier 4: New-to-Therapy Patients
- Started medication mid-year, limited PDC runway
- High risk of early discontinuation (especially statins, RAS antagonists)
- **Action**: Early touchpoint at 30-60 days, address side effects proactively

---

## Clinical Risk Layering

PDC alone is insufficient. Layer clinical risk to distinguish claims-level adherence gaps from
clinically urgent interventions.

### Statin Adherence (D12) — Risk Factors

| Factor | Data Source | Risk Amplification |
|--------|------------|-------------------|
| ASCVD risk score at or above 20% | Claims + lab data | High — guideline-concordant therapy, non-adherence = preventable events |
| Prior MI/stroke/revascularization | Claims (ICD-10, CPT) | Very high — secondary prevention population |
| LDL above 190 mg/dL | Lab data | High — familial hypercholesterolemia likely |
| Diabetes comorbidity | Claims/Rx data | Moderate — overlaps D10, dual measure impact |
| LDL at goal on current therapy | Lab data | Low for intervention *prioritization*. **However: if LDL is at goal BECAUSE of the statin, discontinuation will cause LDL to rebound. Evidence shows that discontinuing statins even when LDL is controlled leads to increased cardiovascular events and mortality. "At goal" does not mean "doesn't need the med." Low priority for outreach sequencing, but discontinuation is still clinically inappropriate. The exception: patients who achieved LDL goal through lifestyle changes alone — this is a clinical judgment call requiring lab trends and history review.** |

### RAS Antagonist Adherence (D11) — Risk Factors

| Factor | Data Source | Risk Amplification |
|--------|------------|-------------------|
| BP above 140/90 on most recent reading | Lab/vitals data | High — uncontrolled hypertension |
| CKD Stage 3+ | Claims (ICD-10) | High — RAS inhibition is renoprotective |
| Heart failure with reduced EF | Claims (ICD-10) | Very high — mortality benefit |
| Proteinuria/albuminuria | Lab data | High — RAS inhibition slows progression |
| BP at goal | Vitals data | Low — controlled, though discontinuation still not recommended |

### Diabetes Medication Adherence (D10) — Risk Factors

| Factor | Data Source | Risk Amplification |
|--------|------------|-------------------|
| A1C at or above 9% | Lab data | Very high — uncontrolled, complications risk |
| A1C 7-9% | Lab data | Moderate — above most targets |
| Recent hospitalization for hyperglycemia | Claims | Very high — acute decompensation |
| Hypoglycemia history | Claims (ICD-10) | Context-dependent — non-adherence may be fear-driven. **If a patient stopped a sulfonylurea after a hypoglycemic episode, this may be a rational safety decision. Flag as a potential deprescribing opportunity, NOT an adherence gap. Do not push adherence on someone who stopped a medication for a legitimate safety reason.** |
| ESRD / dialysis | Claims | Exclusion — check if patient should be excluded from measure |
| On insulin only (no oral agents) | Rx data | Exclusion — not in D10 denominator |
| On insulin + oral agents (combo) | Rx data | **NOT excluded** — patients on insulin AND oral agents (e.g., insulin + metformin) ARE in the D10 denominator. Only insulin-only regimens are excluded. This is a common targeting mistake — do not exclude combo patients. |

---

## Composite Priority Scoring

### Formula
```
Priority Score = PDC_Proximity x Clinical_Risk x Measure_Weight x Timing_Factor
```

### Component Definitions

**PDC_Proximity** — How close is this member to converting at the 80% threshold?
Higher score = closer to threshold = less effort to convert.

| PDC Range | Score | Rationale |
|-----------|-------|-----------|
| 78-79% | 10 | 1-2 fills may convert. Highest ROI per intervention. |
| 75-77% | 8 | Likely needs 3-5 fills or 90-day conversion. Achievable. |
| 70-74% | 5 | Needs sustained engagement over multiple months. |
| 60-69% | 3 | Significant gap. Barrier assessment required. |
| Below 60% | 1 | May have discontinued. Assess clinical appropriateness first. |

**Clinical_Risk** — How clinically urgent is adherence for THIS patient?
Based on the risk layering tables above (statin/RAS/diabetes sections).

| Risk Level | Score | Example |
|------------|-------|---------|
| Very High | 4 | Post-MI patient non-adherent to statin. A1C 9.2% non-adherent to metformin. HFrEF non-adherent to ARB. |
| High | 3 | ASCVD risk over 20%, CKD Stage 3+ on RAS, A1C 7-9% on oral diabetes meds. |
| Moderate | 2 | Diabetes + statin (dual D10/D12 measure impact), proteinuria on RAS. |
| Low | 1 | Controlled on current therapy (BP at goal, A1C at target, LDL at goal). Non-adherence is still suboptimal but less clinically urgent. |

**Measure_Weight** — How much does this measure impact the overall star rating?

| Measure | Weight Score | Rationale |
|---------|-------------|-----------|
| D10, D11, D12 | 3 (1 for MY2026 only) | Triple-weighted in overall star calculation — temporarily reduced to single-weight for MY2026 only, returns to 3× in MY2027. With CY2027 measure removals, these carry an even larger share of the total rating when at full weight. Even at 1× for MY2026, adherence remains a strategic priority because backsliding during a reduced-weight year makes recovery harder when the weight increases. |
| D14, D13, COB, Poly-ACH | 1 | Single-weighted. |

**Timing_Factor** — How much measurement year is left to intervene?

| Months Remaining | Score | Rationale |
|-----------------|-------|-----------|
| 6 or more (Jan-Jun) | 1.0 | Full runway. Build the pipeline. |
| 3-5 (Jul-Sep) | 1.5 | Urgency increasing. Escalate Tier 2 patients. |
| 1-2 (Oct-Nov) | 2.0 | Critical window. Focus exclusively on Tier 1. |
| Less than 1 (Dec) | 2.5 | Last chance. 90-day fill or single fill to close the gap. |

### Worked Examples

**Example 1 — High priority:**
Member on atorvastatin, PDC 78%, history of MI (secondary prevention), October.
```
PDC_Proximity: 10 (78% PDC)
Clinical_Risk: 4 (Very High — post-MI, secondary prevention)
Measure_Weight: 3 (D12, triple-weighted)
Timing_Factor: 2.0 (October, 1-2 months remaining)
Score = 10 x 4 x 3 x 2.0 = 240
```
Interpretation: Immediate intervention. Senior pharmacist outreach. One 90-day fill converts this member and addresses a direct mortality-reduction gap.

**Example 2 — Moderate priority:**
Member on lisinopril, PDC 72%, BP at goal (128/78), July.
```
PDC_Proximity: 5 (72% PDC)
Clinical_Risk: 1 (Low — BP at goal on current therapy)
Measure_Weight: 3 (D11, triple-weighted)
Timing_Factor: 1.5 (July, 3-5 months remaining)
Score = 5 x 1 x 3 x 1.5 = 22.5
```
Interpretation: Monitoring priority. Intervention if resources allow — 90-day conversion and auto-refill could close this gap without intensive outreach.

**Example 3 — Low priority (investigate first):**
Member on metformin, PDC 45%, no recent labs available, March.
```
PDC_Proximity: 1 (below 60%)
Clinical_Risk: 2 (Moderate — diabetes, but no data to escalate)
Measure_Weight: 3 (D10, triple-weighted)
Timing_Factor: 1.0 (March, 6+ months remaining)
Score = 1 x 2 x 3 x 1.0 = 6
```
Interpretation: Low priority for adherence push. Investigate first — did the prescriber discontinue? Did the patient switch to insulin (which would exclude from D10)? Is there an A1C showing control without the med? Clinical appropriateness review before intervention.

### Score Interpretation Ranges

| Score | Priority Level | Action |
|-------|---------------|--------|
| 60 or above | Immediate — highest priority | Assign to senior pharmacist. Intervene within 48 hours. |
| 30-59 | Active — standard priority | Schedule outreach within 1-2 weeks. |
| 10-29 | Monitoring | Intervene if resources allow. Auto-refill, 90-day conversion. |
| Below 10 | Low / Investigate | Review clinical appropriateness before pushing adherence. |

---

## Root Cause Analysis and Intervention Mapping

### Common Root Causes and Matched Interventions

| Root Cause | Indicators | Intervention |
|-----------|-----------|-------------|
| Cost/copay barrier | Claims show fills at quarter boundaries, gaps after plan stage changes | Therapeutic substitution to lower-cost alternative, patient assistance programs, LIS eligibility check |
| Side effects | Fill pattern shows 1-2 fills then stop, restart, stop | Prescriber discussion re: alternative agent, dose adjustment, timing change |
| Complexity/polypharmacy | 10+ concurrent meds, multiple daily dosing | **Medication synchronization (med sync)** — align all fill dates to a single date per month. One pharmacy visit, all meds filled, all PDCs covered simultaneously. This matters for Stars because a single med sync enrollment can reduce gaps across D10, D11, and D12 at once while simplifying the patient's regimen. Coordinate with pharmacy to short-fill or extend fills to align dates, then maintain the sync date going forward. Also supports adherence packaging and simplification review. |
| Forgetfulness/logistics | Irregular fill patterns, no clinical reason | Auto-refill enrollment, 90-day supply conversion, mail order pharmacy |
| Intentional non-adherence | Patient-reported, provider notes | Motivational interviewing, shared decision-making, clinical pharmacist consult |
| Therapy perceived unnecessary | Statin in primary prevention, asymptomatic HTN | Education focus — but respect patient autonomy, document discussion |
| Access/transportation | Gaps correlate with rural zip codes, no mail order | Mail order conversion, community pharmacy outreach, delivery programs |
| Prescriber discontinuation | No refill authorized after office visit | Verify — if intentional, flag for measure exclusion consideration |
| Safety-driven discontinuation | Hypoglycemic episode then stopped sulfonylurea, fall then stopped sedative | **Do not treat as an adherence gap.** This may be a rational safety decision. Flag as potential deprescribing opportunity. Verify with prescriber. If clinically appropriate to remain off therapy, document rationale and investigate measure exclusion. |

### SUPD/D12 Cross-Measure Trap

> **⚠️ CRITICAL**: When intervening on SUPD (D14) by initiating a new statin, the member enters
> the D12 (Statin Adherence) denominator immediately. If the member fills once and stops, SUPD
> improves but D12 gets WORSE. **Every SUPD statin initiation must include an adherence support
> plan from day one.** Pair with: 90-day supply, auto-refill enrollment, follow-up at 30 days.
> This is the single most common cross-measure mistake in Stars optimization.

### Intervention Escalation Ladder
1. **Automated**: Refill reminder (IVR, text, app notification)
2. **Technician outreach**: Fill transfer, 90-day conversion, mail order setup, **med sync alignment**
3. **Pharmacist outreach**: Barrier assessment, clinical intervention, prescriber fax
4. **Prescriber collaboration**: Therapy modification, alternative agent, documented rationale
5. **In-person/telehealth CMR**: Comprehensive review for complex patients

Note on intervention intensity: Evidence consistently shows that more intensive interventions (pharmacist-led motivational interviewing, comprehensive medication reviews) produce larger adherence improvements than automated reminders alone. However, intensive interventions cost more per member. Match intervention intensity to priority score — reserve senior pharmacist time for scores above 60, use automated and technician-level interventions for scores 10-29. This maximizes clinical impact per resource dollar spent.

---

## Intervention Timing

### Quarterly Checkpoints
- **Q1 (Jan-Mar)**: Baseline identification, new-to-therapy monitoring, carryover fill assessment
- **Q2 (Apr-Jun)**: Mid-year review, identify members falling below trajectory, 90-day conversions, **med sync enrollment**
- **Q3 (Jul-Sep)**: Escalation window — members below 70% PDC need intensive engagement
- **Q4 (Oct-Dec)**: Critical window — every fill counts, focus on Tier 1 patients, last-chance 90-day fills

### December Crunch
- A 90-day fill in early October covers the member through December 31
- A 30-day fill on December 1 covers December (31 days) — can be enough to push over 80%
- Plans that wait until Q4 to intervene are playing catch-up — build the pipeline in Q1-Q2
- **Important**: While Q4 fills count and the December playbook is operationally necessary, sustainable adherence interventions started in Q1-Q2 produce better long-term outcomes than last-minute gap-closing. Plans should not design their entire Stars strategy around the December crunch — it should be a safety net, not the primary approach.

---

## Important Considerations

### The Healthy Adherer Effect
Adherent patients tend to have better outcomes — but adherence is also a marker for overall healthy behavior. Patients who reliably fill medications are more likely to keep appointments, follow dietary recommendations, and engage with their care. This doesn't negate the importance of adherence interventions, but it means that pushing PDC from 45% to 80% through refill reminders alone may not produce the same clinical benefit as a patient who organically maintains 85% PDC because they're broadly engaged in their health. The implication for Stars programs: pair adherence interventions with broader health engagement strategies when possible, especially for Tier 2 and Tier 3 patients. A refill reminder fixes PDC. A pharmacist conversation that addresses barriers, builds trust, and connects the patient to resources fixes the patient.

### Adherence ≠ Clinical Success
An 80% PDC does not guarantee therapeutic success. A patient can be perfectly adherent to a subtherapeutic dose, a wrong drug for their condition, or a medication they no longer need. Adherence is a process measure, not an outcome measure. The clinical risk layering in this skill exists specifically to prevent the trap of optimizing adherence on a medication that shouldn't be continued. Always ask: is this the right drug, at the right dose, for the right patient — before asking whether they're taking it consistently.
