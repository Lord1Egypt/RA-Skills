# geriatric-care-needs-assessment

**Domain:** Geriatric Care Management  
**Skill:** `geriatric-care-needs-assessment`  
**Version:** 0.1.0

## What It Does

Converts client intake information into a structured, multi-domain care needs assessment for an older adult, following Aging Life Care Association (ALCA) standards. Covers functional status, cognitive and behavioral observations, safety screening, social supports, home environment, and financial/legal status — and produces prioritized care recommendations.

Produces a **DRAFT** for Aging Life Care Manager (ALCM) or licensed social worker review before any care plan is implemented, shared, or billed.

## When to Use

Use this skill when an Aging Life Care Manager (ALCM), certified geriatric care manager, licensed clinical social worker, eldercare coordinator, or discharge planner needs to:

- Draft an initial comprehensive care needs assessment for a new older adult client
- Organize intake information collected from a home visit into a structured document
- Produce a prioritized care recommendations table for family and care team review
- Document functional status, cognitive observations, and safety concerns for a Medicaid waiver or long-term care insurance referral
- Prepare an elder care assessment to support attorney-directed care planning (elder law, guardianship, trust administration)

## Scope and Boundaries

**This skill covers:**
- Medical summary (diagnoses, medications, care team, advance directives)
- Functional assessment: ADLs (Katz Index domains) and IADLs (Lawton-Brody domains)
- Cognitive and behavioral status — formal scores and observational documentation
- Safety screening: fall risk, home safety, driving, self-neglect, elder abuse and exploitation indicators
- Social supports and caregiver burden assessment
- Environmental assessment (home suitability, community resources)
- Financial and legal status (insurance, benefits enrollment, legal documents, exploitation risk)
- Prioritized findings table: URGENT / HIGH / MEDIUM / MONITORING
- Reassessment plan

**This skill does not:**
- Make clinical diagnoses or prescribe treatment
- Render a psychiatric or neuropsychological opinion
- Submit assessments to any agency, Medicaid portal, or insurance payer
- Replace the licensed professional's clinical judgment
- File a mandatory report to Adult Protective Services (APS) — the care manager must file this directly

## Safety Boundaries

- When elder abuse, self-neglect, or financial exploitation indicators are present, the DRAFT will flag an **URGENT** alert and include a mandatory reporter reminder — the care manager must independently fulfill any mandatory reporting obligation under their state's law.
- This skill will not record Social Security Numbers, financial account numbers, or detailed financial assets in the DRAFT.
- Assessment content must not be shared with any third party without client or authorized representative authorization.

## Output

A structured Markdown care needs assessment labeled **DRAFT**, with:
- URGENT concerns surfaced at the top of the document
- ADL/IADL tables with level-of-function ratings
- Prioritized findings and care recommendations table
- Licensed professional review and sign-off block

## Example Use Cases

- A care manager at an eldercare consulting firm has completed a home visit with a 79-year-old woman referred by her adult children after a fall. She needs a structured assessment documenting functional decline, fall risk factors, caregiver strain, and care recommendations for a family meeting.
- An elder law attorney has engaged an ALCM to assess a client's capacity and care needs for a guardianship proceeding. The ALCM needs a comprehensive, defensible assessment document.
- A hospital social worker is arranging discharge for an 84-year-old patient with dementia and no family in the area. She needs a care needs assessment to support a Medicaid waiver referral.
- A long-term care insurance company has authorized a geriatric care manager to produce an initial assessment as a condition of benefit activation.

## Feedback & Contributions

Have feedback or a use case this skill doesn't cover? Open an issue at:  
https://github.com/archlab-space/Open-Skill-Hub/issues
