# Clinical Guideline Drift Detection

## Table of Contents
1. [What Is Guideline Drift](#what-is-guideline-drift)
2. [Context: Why Drift Detection Matters More in 2027+](#context-why-drift-detection-matters-more-in-2027)
3. [Drift Detection Framework](#drift-detection-framework)
4. [Drift Registry](#drift-registry)
5. [Detection Workflow](#detection-workflow)
6. [Mismatch Logging Template](#mismatch-logging-template)
7. [Sources to Monitor](#sources-to-monitor)

---

## What Is Guideline Drift

Guideline drift occurs when clinical practice guidelines update faster than the CMS measure
specifications or MIPS quality measures that reference them. This creates a gap where:

- **Clinicians** follow the updated guideline (evidence-based, current standard of care)
- **Measures** still reward or penalize based on the old guideline logic
- **Platforms** must decide whether to optimize for clinical accuracy or measure performance

This is not theoretical — it happens regularly. CMS measure specifications update on annual
cycles. Clinical guidelines update whenever the evidence warrants it. The lag creates
actionable mismatches that clinical pharmacists in Stars optimization roles must identify and
manage.

### Ethical Dimension

When guidelines and measures diverge, clinical teams face a genuine tension: do you follow the current evidence (which may hurt the measure score) or optimize for the measure (which may mean applying outdated clinical logic)? There is no universal answer. The role of this skill is to make the divergence visible so the decision is conscious and documented, not accidental.

---

## Context: Why Drift Detection Matters More in 2027+

CMS's CY2027 proposed rule removes 12 measures from Star Ratings — seven focused on operational and administrative performance, three on process of care, and two on patient experience. The clinical measures that remain carry a larger share of the overall rating. When a guideline drifts from a clinical measure specification, the impact on the star rating is now amplified. A mismatch between guideline-concordant care and measure-optimal behavior on a triple-weighted adherence measure is three times as costly as it was when administrative measures diluted the weight.

### Health Equity Considerations

CMS proposed in the CY2027 rule NOT to implement the "Excellent Health Outcomes for All" reward (previously called the Health Equity Index reward) and will continue the historical reward factor instead. CMS deferred this adjustment, but it may return in future rulemaking cycles. Monitor CMS Advance Notices and proposed rules for potential health equity reward implementation, as this could affect how measures are scored for plans serving vulnerable populations and may create new drift scenarios where guideline-concordant care intersects with equity-adjusted scoring.

---

## Drift Detection Framework

### Three-Source Comparison Model

Every clinical measure sits at the intersection of three sources. Drift occurs when any two
diverge:

```
┌─────────────────────┐
│  Clinical Guideline  │  (ACC/AHA, ADA, KDIGO, IDSA, AGS, etc.)
│  Current evidence    │
└──────────┬──────────┘
           │
    ┌──────┴──────┐
    │  MATCH?     │
    ├─────────────┤
    │             │
┌───▼───┐   ┌───▼────┐
│  CMS   │   │  MIPS   │
│ Star   │   │ Quality │
│ Measure│   │ Measure │
└───┬────┘   └───┬────┘
    │  MATCH?    │
    └─────┬──────┘
          ▼
```

### Drift Categories

**Category A — Guideline vs. CMS Star Measure**
Guideline updates a recommendation; Star measure still references old criteria.
*Impact*: Platform logic optimizing for the measure may give clinically outdated recommendations.

**Category B — Guideline vs. MIPS Quality Measure**
Guideline updates; MIPS measure still references old criteria.
*Impact*: Provider quality scores may penalize guideline-concordant care.

**Category C — CMS Star Measure vs. MIPS Measure**
Same clinical domain, different specifications between Stars and MIPS.
*Impact*: Dual-eligible patients or aligned plans may face contradictory optimization targets.

**Category D — Drug Class Definition Drift**
New drug classes or agents approved after measure specification was written.
*Impact*: New medications may not count toward measure numerators (e.g., novel diabetes agents).

### Severity Rating

- **Critical**: Drift directly affects measure scoring AND clinical recommendations diverge — following the guideline hurts the measure score or vice versa
- **Significant**: Drift creates confusion or suboptimal recommendations but doesn't directly invert measure performance
- **Monitoring**: Drift is emerging — guideline update is published but measure spec hasn't been tested against it yet

---

## Drift Registry

### Active Drifts

#### DRIFT-001: ASCVD Risk Assessment — PREVENT vs. PCE

| Field | Detail |
|-------|--------|
| **Category** | A + B (Guideline vs. CMS Star + MIPS) |
| **Severity** | Critical |
| **Guideline** | 2026 ACC/AHA Dyslipidemia Guideline |
| **Change** | Officially adopted AHA PREVENT equations as primary ASCVD risk calculator, replacing Pooled Cohort Equations (PCE). This is now the current standard of care — not a proposal, a published guideline change. |
| **CMS Star Impact** | D12 (Statin Adherence) and D14 (SUPD) measure specifications reference statin eligibility populations. Statin-benefit groups defined by risk thresholds were historically calibrated to PCE output. |
| **MIPS Impact** | MIPS Measure #438 (Statin Therapy for Prevention/Treatment of CVD) still references PCE-based risk thresholds for the eligible population denominator |
| **Clinical Significance** | PREVENT and PCE do NOT produce equivalent risk estimates for the same patient. PREVENT generally estimates lower 10-year ASCVD risk than PCE, particularly in younger patients and certain demographic groups. A patient with PCE-calculated risk above 7.5% may have PREVENT-calculated risk below 7.5%. |
| **Platform Implication** | If a platform uses PREVENT (guideline-concordant) to identify statin-eligible patients, it may identify FEWER patients than the PCE-based measure denominator expects. This creates a mismatch between clinical recommendations and measure optimization. |
| **Recommended Action** | (1) Flag the discrepancy in clinical logic. (2) Run both calculators and document when results diverge — dual-calculator approach allows guideline-concordant clinical recommendations while tracking measure-specification impact. (3) Monitor CMS Technical Notes for D12/D14 specification updates adopting PREVENT. (4) For platform logic: maintain PCE-based identification for measure compliance while flagging PREVENT-discordant cases for clinical review. (5) If CMS updates to PREVENT-based thresholds, be prepared for significant denominator changes — patient populations eligible for statin therapy may shift substantially. |
| **Date Identified** | March 2026 |
| **Status** | Active — 2026 guideline officially adopted PREVENT; no CMS measure spec update announced |

---

#### DRIFT-002: ADA Glycemic Targets — A1C vs. Time-in-Range (TIR)

| Field | Detail |
|-------|--------|
| **Category** | A (Guideline vs. CMS Star Measure) — Note: This is better classified as measure interpretation complexity rather than pure guideline drift. The guideline didn't change what medications to use — it changed how glycemic control is assessed. D10 measures medication adherence, not glycemic control. The tension is indirect but operationally real. |
| **Severity** | Significant |
| **Guideline** | 2023 ADA Standards of Care (and subsequent annual updates) |
| **Change** | Endorsed time-in-range (TIR) from continuous glucose monitoring (CGM) as a complementary — and in some cases preferred — glycemic target alongside A1C. TIR above 70% is now a recognized goal. |
| **CMS Star Impact** | D10 (Diabetes Medication Adherence) measures PDC for oral diabetes medications using pharmacy claims data. It does not measure glycemic outcomes. A patient managed primarily on CGM-guided insulin titration with minimal oral agent use could be clinically well-managed but appear non-adherent on D10 claims. |
| **MIPS Impact** | MIPS diabetes measures still reference A1C-based targets. No MIPS measure currently incorporates TIR. |
| **Clinical Significance** | A patient with excellent TIR on CGM-guided insulin therapy who takes minimal oral agents is not a D10 failure — they may be optimally managed. Pushing oral agent adherence in this context could be clinically inappropriate. |
| **Platform Implication** | Platforms flagging low oral diabetes PDC should cross-reference insulin claims and CGM device claims before targeting for adherence intervention. Patients on insulin-only regimens are excluded from D10; patients on insulin + oral agents are NOT excluded (see adherence-interventions.md for detail on this common targeting mistake). |
| **Recommended Action** | (1) Before flagging a diabetes patient for D10 non-adherence, check for concurrent insulin and CGM claims. (2) If patient is on insulin + oral agent combo with evidence of CGM use, prioritize clinical review over automated adherence outreach. (3) Document clinical rationale when oral agent non-adherence is assessed as clinically appropriate in CGM-managed patients. |
| **Date Identified** | March 2026 |
| **Status** | Active — ADA continues to emphasize TIR; CMS D10 specification unchanged |

---

#### DRIFT-003: GLP-1 Receptor Agonist Indication Ambiguity

| Field | Detail |
|-------|--------|
| **Category** | D (Drug Class Definition Drift) |
| **Severity** | Monitoring |
| **Guideline** | Multiple — ADA Standards of Care, ACC/AHA Obesity Guidelines, FDA labeling |
| **Change** | Semaglutide and other GLP-1 RAs are now widely prescribed for both type 2 diabetes AND obesity/weight management. FDA-approved indications span both conditions. Prescribing volume for obesity indications has grown dramatically. |
| **CMS Star Impact** | D10 (Diabetes Medication Adherence) denominator inclusion is drug-class-based, not indication-based. GLP-1 RAs are currently NOT in the D10 denominator (D10 covers oral diabetes medications only). However, GLP-1 RA fills may appear in pharmacy claims alongside oral diabetes agents, creating confusion about which patients are being treated for diabetes vs. obesity. |
| **MIPS Impact** | MIPS diabetes measures reference diabetes diagnosis codes. A patient filling semaglutide for obesity without a diabetes diagnosis should not appear in diabetes quality measure denominators — but claims data may not clearly distinguish indication. |
| **Clinical Significance** | A patient filling semaglutide for weight management who does not have diabetes should not be targeted for diabetes-related adherence interventions or Star measure optimization. |
| **Platform Implication** | Platforms should flag any patient with GLP-1 RA fills and no diabetes diagnosis (ICD-10 E11.x) for clinical review before D10 targeting. Monitor for CMS clarification on whether obesity-indication GLP-1 fills should be excluded from diabetes-related measure denominators. |
| **Recommended Action** | (1) Cross-reference GLP-1 RA fills with diabetes diagnosis codes before including in any diabetes measure targeting. (2) Flag patients on GLP-1 RA without E11.x diagnosis for clinical review. (3) Monitor CMS Technical Notes and PQA measure specifications for guidance on GLP-1 RA indication handling. (4) If CMS adds GLP-1 RAs to the D10 denominator in future specifications, prepare for significant denominator expansion. |
| **Date Identified** | March 2026 |
| **Status** | Monitoring — no CMS specification change; indication ambiguity growing as obesity prescribing increases |

---

#### DRIFT-004: Depression Screening and Follow-Up — New Measure

| Field | Detail |
|-------|--------|
| **Category** | New measure (not a drift — logged here because it affects resource allocation and clinical program planning) |
| **Severity** | Significant |
| **Guideline** | CY2027 Proposed Rule |
| **Change** | CMS proposes adding a Part C Depression Screening and Follow-Up measure starting with 2027 measurement year, scoring in 2029 Star Ratings. The measure tracks two rates: (a) percentage of eligible members screened for clinical depression, and (b) if screened positive, percentage who received follow-up care within 30 days. CMS will average the two rates for the Star Rating. This measure aligns with the USPSTF Grade B recommendation for depression screening in adults. PHQ-2 and PHQ-9 are the standard screening tools likely to be used for implementation. |
| **CMS Star Impact** | New measure added to Part C. Will contribute to overall star rating beginning 2029. Displayed on the display page for 2026 Star Ratings (2024 measurement year data) for baseline reporting. |
| **MIPS Impact** | Aligns with existing MIPS behavioral health screening measures. |
| **Clinical Significance** | Behavioral health integration into Star Ratings signals CMS prioritization of mental health. For platforms like Arine that serve populations with high comorbid depression (diabetes, cardiovascular disease, chronic pain), this measure creates opportunity to demonstrate value in cross-condition clinical programming. Depression is independently associated with medication non-adherence — members with unscreened/untreated depression are more likely to have open adherence gaps on D10, D11, and D12. Addressing depression can improve adherence outcomes. |
| **Platform Implication** | Platforms with behavioral health clinical pharmacist (BCPP) expertise can build integrated workflows that address both depression screening and medication adherence gaps in a single encounter. A member flagged for statin non-adherence who also screens positive for depression may need a fundamentally different intervention than a refill reminder — the depression may be driving the non-adherence. |
| **Recommended Action** | (1) Begin tracking depression screening rates in current member populations. (2) Identify members with comorbid depression and open medication adherence gaps — these patients may benefit from integrated interventions addressing both the behavioral health barrier and the adherence gap simultaneously. (3) Build follow-up workflows that ensure positive screens result in documented care within 30 days. (4) Monitor the 2026 display page data to establish baseline performance before the measure scores. (5) This measure aligns with the USPSTF Grade B recommendation for depression screening in adults. PHQ-2 and PHQ-9 are the standard screening tools — ensure platform workflows support structured screening documentation using these validated instruments. |
| **Date Identified** | March 2026 |
| **Status** | Active — proposed in CY2027 rule, display-only in 2026, scoring expected 2029 |

---

*Add new drifts below using the Mismatch Logging Template.*

---

## Detection Workflow

### When to Run Drift Detection

1. **Guideline publication**: Any major clinical guideline update (ACC/AHA, ADA, KDIGO, IDSA, AGS Beers, USPSTF)
2. **CMS annual update**: When new Star Ratings Technical Notes or Call Letter is published
3. **CMS mid-year updates**: CMS sometimes issues mid-year clarifications or technical corrections — do not assume specifications are static between annual cycles
4. **MIPS update cycle**: When MIPS measure specifications are updated
5. **FDA approval**: New drug class or indication that may affect measure denominators/numerators
6. **Measure retirement announcements**: When CMS announces measure retirements, assess impact on platform logic and resource allocation — a retired measure may free resources for remaining measures
7. **Health equity methodology changes**: CMS considered implementing a Health Equity Index (HEI / "Excellent Health Outcomes for All" reward) for 2027 Star Ratings but deferred it in the CY2027 proposed rule, continuing the historical reward factor instead. Monitor for future rulemaking — if HEI is implemented in a later cycle, it will affect how measures are scored for plans serving vulnerable populations and may create new drift scenarios where guideline-concordant care intersects with equity-adjusted scoring.
8. **Quarterly review**: Scheduled review of existing drifts for resolution status

### Detection Steps

1. **Identify the clinical domain** affected by the update
2. **Map to Star measures**: Which CMS Star measures reference this clinical domain?
3. **Map to MIPS measures**: Which MIPS quality measures reference this domain?
4. **Compare specifications**: Does the updated guideline change any of the following?
   - Risk thresholds used to define eligible populations
   - Drug class definitions (what counts, what doesn't)
   - Treatment targets (A1C goals, BP targets, LDL thresholds)
   - Screening/monitoring intervals
   - Recommended first-line agents
5. **Assess impact**: Does the change create a scenario where following the guideline diverges from measure-optimal behavior?
6. **Cross-measure impact assessment**: When a guideline changes, assess impact across ALL potentially affected measures, not just the obvious one. Example: a statin guideline change affects D12 (statin adherence), D14 (SUPD), and potentially D10 (if the patient also has diabetes). Assess all three.
7. **Account for contract-level aggregation**: Star Ratings are calculated at the contract level, not the plan level. A guideline change may affect different geographic regions or plan benefit packages within a contract differently, but the contract-level rating will not reflect this variation. When assessing drift impact, consider whether the drift disproportionately affects certain sub-populations within the contract.
8. **Log the drift** using the template below
9. **Recommend action**: Dual-logic, monitor, or flag for CMS feedback

---

## Mismatch Logging Template

Copy this template for each new drift entry:

```markdown
#### DRIFT-XXX: [Short Title]

| Field | Detail |
|-------|--------|
| **Category** | [A / B / C / D / New Measure] |
| **Severity** | [Critical / Significant / Monitoring] |
| **Guideline** | [Guideline name and year] |
| **Change** | [What changed in the guideline] |
| **CMS Star Impact** | [Which measures affected and how] |
| **MIPS Impact** | [Which MIPS measures affected and how] |
| **Clinical Significance** | [What this means for patient care] |
| **Platform Implication** | [What this means for platform logic / recommendations] |
| **Recommended Action** | [Specific steps to manage the drift] |
| **Date Identified** | [Month Year] |
| **Status** | [Active / Resolved / Monitoring] |
```

### Registry Maintenance

- Review all Active drifts quarterly
- Move to Resolved when CMS/MIPS measure specs align with guideline
- Archive Resolved drifts with resolution date and spec version
- Drifts in Monitoring status should be escalated if no spec update within 2 annual cycles

---

## Sources to Monitor

| Source | URL | Update Frequency | What to Watch For |
|--------|-----|-----------------|-------------------|
| CMS Star Ratings Technical Notes | cms.gov/medicare/health-drug-plans/part-c-d-performance-data | Annual (typically October) + mid-year corrections | Cutpoint changes, measure specification updates, methodology changes |
| CMS Advance Notice / Rate Announcement (Call Letter) | cms.gov/medicare/health-drug-plans/part-c-d-performance-data | Annual (February draft, April final) | New measures, measure retirements, weight changes, MTM eligibility threshold updates |
| CMS Proposed and Final Rules | cms.gov/newsroom/fact-sheets | Annual (proposed ~November, final ~April) | Major policy changes, measure additions/removals, health equity methodology, Star Ratings restructuring |
| MIPS Quality Measure Specifications | qpp.cms.gov | Annual | Measure denominator/numerator changes, new measures, retired measures |
| ACC/AHA Clinical Practice Guidelines | acc.org, professional.heart.org | As published (variable) | Risk calculator changes (PCE/PREVENT), treatment thresholds, drug class recommendations |
| ADA Standards of Care | diabetesjournals.org | Annual (January) + living updates | Glycemic targets, medication algorithms, TIR/CGM guidance, A1C goal modifications |
| AGS Beers Criteria | americangeriatrics.org | Every 4 years (next update ~2027) | High-risk medication list changes affecting Poly-ACH measure |
| KDIGO Guidelines | kdigo.org | As published (variable) | CKD management, RAS antagonist recommendations, BP targets in renal disease |
| USPSTF Recommendations | uspreventiveservicestaskforce.org | As published (variable) | Screening recommendations that may affect Part C measures, including depression screening |
| FDA New Drug Approvals | fda.gov/drugs | Ongoing | New drug classes, new indications for existing drugs, safety communications affecting prescribing |
| PQA (Pharmacy Quality Alliance) | pqaalliance.org | Annual | Measure specification updates — PQA develops many Part D Star measures including adherence and polypharmacy measures |
