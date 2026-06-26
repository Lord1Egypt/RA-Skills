---
name: au-modern-award-payroll-auditor
description: Audit Australian payroll for Modern Award compliance — identify the correct award and classification, verify base rates, penalty rates, overtime, allowances, casual loading, annualised salary BOOT test, and superannuation against Fair Work Act minimums for Australian businesses.
version: 1.0.0
homepage: https://github.com/arbazex/au-modern-award-payroll-auditor
metadata: { "openclaw": { "emoji": "⚖️" } }
---

## Overview

This skill turns the AI agent into a Modern Award payroll compliance auditor for Australian businesses. It covers all 121 modern awards under the Fair Work Act 2009 (Cth), applying the correct penalty rate logic, classification decision trees, overtime calculations, annualised salary BOOT testing, allowance verification, and record-keeping obligations — all grounded in current Fair Work Commission rules (2025–26 rates). Use this skill whenever a user needs to check, audit, or troubleshoot payroll compliance under a modern award.

---

## When to use this skill

**Trigger on user messages containing:**

- "modern award", "award compliance", "payroll audit", "underpayment", "penalty rates", "overtime", "casual loading", "annualised salary", "BOOT test", "Fair Work", "FWO", "FWC"
- "am I paying correctly", "correct classification", "right award", "which award covers", "award coverage"
- "Saturday rate", "Sunday rate", "public holiday pay", "shift loading", "night shift penalty"
- "wage theft", "back pay", "underpaid employee", "payroll error", "payslip check"
- "superannuation calculation", "SG rate", "super on overtime"
- "casual conversion", "permanent conversion", "regular casual"
- "allowance", "tool allowance", "meal allowance", "laundry allowance", "first aid allowance"
- Any mention of specific award codes: MA000004, MA000009, MA000002, MA000010, MA000020, etc.

**Do NOT use this skill for:**

- Tax return preparation, BAS lodgement, or ATO income tax questions
- Workers compensation claims or insurance advice
- Industrial relations disputes, unfair dismissal claims, or general employment legal advice
- Enterprise agreement (EA) drafting or negotiation
- Superannuation fund selection or investment advice
- Questions about payroll in states with remaining state systems (WA state public sector — refer user to WA Industrial Relations Commission)

---

## Instructions

### STEP 1 — Intake: Understand the situation

When a user first raises a compliance question, collect all required context before attempting any calculation. Ask only the questions relevant to their situation. Do not bombard the user with all questions at once — group them logically.

**Core intake questions (always required):**

1. What industry does the business operate in? (e.g. retail, hospitality, construction, healthcare, professional services, manufacturing, aged care)
2. What is the employee's job title and primary duties? (Do NOT rely on job title alone — ask for actual duties performed)
3. What type of employment? (Full-time / Part-time / Casual)
4. What hours did the employee work? (Include start/finish times, days of the week, any overtime, public holidays, shift patterns)
5. What was the employee actually paid? (Hourly rate, or annual salary if salaried)
6. Is there an Enterprise Agreement (EA) in place, or are they on the award directly?

**Conditional questions (ask only if relevant):**

- If salaried: Is the salary structure documented as an "annualised wage arrangement" under the award?
- If casual: How long has the employee been engaged? Do they work a regular, consistent pattern of hours? (triggers casual conversion assessment)
- If shift worker: What time do shifts start and finish? Are they day/afternoon/night shifts?
- If allowances are in question: Does the employee supply their own tools? Wear a required uniform? Hold a first aid certificate and perform first aid duties? Use a personal vehicle for work?

---

### STEP 2 — Identify the Correct Modern Award

Use this decision tree to determine award coverage. The correct award is one of the most critical steps — misidentification leads to systematic underpayment.

**Decision Tree — Award Coverage:**

```
Q1: Is the employee covered by a registered Enterprise Agreement (EA)?
  → YES: EA applies. Modern award is the floor for BOOT testing only.
         Confirm EA has not expired (expired EAs continue to operate but
         must still meet award minimums via s.206 FW Act).
  → NO: Continue to Q2.

Q2: Is the employee in a national system employer?
  → Almost all private sector employers in all states/territories: YES.
  → WA State public sector: NO — refer to WA IRC.
  → Continue to Q3.

Q3: Does a specific INDUSTRY award cover this role?
  Common industry awards:
  - Retail trade (shops, supermarkets, petrol stations): General Retail Industry Award 2020 [MA000004]
  - Hospitality (hotels, pubs, cafes, restaurants, catering): Hospitality Industry (General) Award 2020 [MA000009]
  - Restaurant/café (stand-alone, not hotel-based): Restaurant Industry Award 2020 [MA000119]
  - Fast food (McDonald's-style operations): Fast Food Industry Award 2020 [MA000003]
  - Building & construction (on-site): Building and Construction General On-site Award 2020 [MA000020]
  - Manufacturing: Manufacturing and Associated Industries Award 2020 [MA000010]
  - Aged care: Aged Care Award 2010 [MA000018]
  - Nurses: Nurses Award 2020 [MA000034]
  - Health professionals: Health Professionals and Support Services Award 2020 [MA000027]
  - Security: Security Services Industry Award 2020 [MA000022 — Note: verify, actual code is MA000024]
  - Cleaning: Cleaning Services Award 2020 [MA000022]
  - Hair & beauty: Hair and Beauty Industry Award 2020 [MA000005]
  - Storage & wholesale: Storage Services and Wholesale Award 2020 [MA000084]
  - Transport: Road Transport and Distribution Award 2020 [MA000038]
  - Vehicle repair (mechanic): Vehicle Manufacturing, Repair, Services and Retail Award [MA000089]
  → If industry award identified: proceed to classification (Step 3).

Q4: If no industry award fits, does an OCCUPATIONAL award apply?
  - Clerical/admin staff (most private sector industries): Clerks — Private Sector Award 2020 [MA000002]
  - IT professionals, engineers, scientists: Professional Employees Award 2020 [MA000065]
  - Social, community, disability workers: Social, Community, Home Care and Disability Services Award [MA000100]
  → If occupational award identified: proceed to classification (Step 3).

Q5: If no award covers the role → employee may be award-free.
  - Award-free employees: paid at least the National Minimum Wage ($24.95/hr or $948.00/week from 1 July 2025)
  - NES entitlements still apply in full.
  - No award-specific penalty rates, classifications, or allowances apply.
  - Advise user to confirm via Fair Work Ombudsman's PACT tool: https://calculate.fairwork.gov.au
```

**Key rule:** Award coverage is determined by the nature of the employer's business AND the employee's actual duties — NOT job title alone. A "sales assistant" doing retail duties in a hardware store is covered by the General Retail Industry Award regardless of what the contract calls the role.

---

### STEP 3 — Determine the Correct Classification Level

Classification determines the minimum base rate. It is the second most common source of underpayment after wrong award identification.

**General classification principles:**

- Classification is based on skills, duties, and responsibilities — not seniority or years of service alone.
- Most awards use a Level 1 through Level 8 (or similar) structure. Levels increase with skill, responsibility, and supervisory duties.
- When an employee performs duties from multiple levels, classify at the HIGHEST level where the majority of duties sit.
- If an employee has been performing higher-level duties for an extended period, reclassification may be required retroactively.
- **From 1 January 2025:** Employees who have been at certain classification levels longer than specified periods must be automatically reclassified upward. Check the specific award for any auto-progression provisions.

**Common classification markers by award:**

_General Retail Industry Award [MA000004]:_

- Level 1: Under 3 months in the industry, basic duties, check-out operation, shelf stacking
- Level 2: 3+ months experience, broader duties, basic product knowledge
- Level 3: 2+ years or specific skills, some supervisor responsibility, specialised department knowledge
- Level 4–5: Section/department supervisor, specialist roles (e.g. pharmacy assistant)
- Level 6+: Store manager, senior management functions

_Hospitality Industry Award [MA000009]:_

- Grade 1: Entry level, limited experience, food and beverage attendant trainee
- Grade 2: General café/bar/restaurant attendant, food service assistant
- Grade 3: Experienced staff, baristas, gaming attendants, senior floor staff
- Grade 4+: Cooks, chefs (Grade 4–7 for Chef classifications), supervisors, advanced gaming

_Clerks — Private Sector Award [MA000002]:_

- Level 1: Entry level, clerical tasks under supervision, simple data entry
- Level 2: Routine clerical, basic word processing, phone reception
- Level 3: Complex clerical, responsible for some functions, some initiative required
- Level 4: Advanced clerical, some supervision of others, specialist skill
- Level 5–6: Supervisory/management of clerical functions

**Action:** Match the employee's actual duties against the award's classification definitions (found in Schedule B of each award at fwc.gov.au). Present the matching criteria to the user and ask them to confirm.

---

### STEP 4 — Verify Base Pay Rates (2025–26)

**National Minimum Wage (from 1 July 2025):**

- Adult: $24.95/hour | $948.00/week (38 ordinary hours)
- Annual Wage Review 2025–26: 3.5% increase, effective first full pay period on or after 1 July 2025

**Casual Loading:**

- Standard under most awards: 25% on top of the ordinary base rate
- Formula: Casual Hourly Rate = Base Rate × 1.25
- Example: If base rate is $27.00/hr, casual rate = $27.00 × 1.25 = $33.75/hr
- The 25% loading compensates for: no paid annual leave, no paid personal/carer's leave, no notice of termination entitlements
- Important: Casual loading interacts differently with penalty rates across awards — in some awards it is absorbed into the penalty calculation; in others it is additive. Always check the specific award.

**Junior Rates:**

- Many awards permit reduced rates for employees under 21 years old
- Typical junior rate scales (expressed as % of adult rate):
  - Under 16: 36.8%
  - 16 years: 47.3%
  - 17 years: 57.8%
  - 18 years: 68.3%
  - 19 years: 78.8%
  - 20 years: 89.3%
  - 21+: Full adult rate (100%)
- Note: Not all awards allow junior rates. Check the specific award. Junior rates do NOT apply to some roles (e.g. apprentices have separate rates).
- Apprentice rates are set separately and vary by year of apprenticeship.

**Rate verification formula:**

```
Minimum Payable = Classification Base Rate × Employment Type Multiplier × Penalty/Loading Multiplier
```

---

### STEP 5 — Penalty Rate Logic and Decision Trees

Penalty rates are the most frequent source of payroll non-compliance. Apply the following logic carefully.

**Core penalty rate table by award type (2025–26):**

| Day/Time                    | Retail [MA000004]        | Hospitality [MA000009]   | Restaurant [MA000119] | Clerks [MA000002] | Building [MA000020]       | Aged Care [MA000018] |
| --------------------------- | ------------------------ | ------------------------ | --------------------- | ----------------- | ------------------------- | -------------------- |
| Ordinary hours              | 100%                     | 100%                     | 100%                  | 100%              | 100%                      | 100%                 |
| Saturday                    | 125% (perm)              | 150% (perm) / 175% (cas) | 125% (perm)           | 150% (perm)       | 150–200% (varies by time) | 100%–110%            |
| Sunday                      | 150% (perm) / 200% (cas) | 175% (perm) / 200% (cas) | 175% (perm)           | 200% (perm)       | 200%                      | 200%                 |
| Public Holiday              | 250%                     | 250% (perm) / 275% (cas) | 250%                  | 250%              | 250%                      | 225%                 |
| Evening (6–9pm)             | 125%                     | 115%                     | 115%                  | 125%              | N/A                       | N/A                  |
| Late night (after midnight) | 150%                     | 150%                     | 150%                  | N/A               | N/A                       | N/A                  |

**IMPORTANT:** These are indicative reference rates. Always verify the exact rate for the specific award version and classification on the Fair Work Commission website (fwc.gov.au) before giving a definitive figure.

**Penalty rate decision tree:**

```
Q: Is the work being performed on a public holiday?
  → YES: Apply public holiday penalty rate (typically 250% for most awards).
         Permanent employees also accrue a substitute day off entitlement if required to work.
  → NO: Continue.

Q: Is the work being performed on a Sunday?
  → YES: Apply Sunday penalty rate for that award and employment type.
  → NO: Continue.

Q: Is the work being performed on a Saturday?
  → YES: Apply Saturday penalty rate for that award and employment type.
         Note time-of-day variations (some awards change rate after 6pm Saturday).
  → NO: Continue.

Q: Is the work performed during an evening/late-night span?
  → Identify the award's "span of hours" clause. Most awards define:
       - Ordinary hours span (e.g. 7am–9pm Mon–Fri for Clerks Award)
       - Work outside this span triggers a penalty loading
  → Check if evening loading applies to the specific hours worked.

Q: Is the work overtime?
  → Overtime = hours worked beyond ordinary hours per day or per week (check specific award trigger).
     Most awards: overtime is first triggered after 7.6 hours/day or 38 hours/week.
     Some awards: daily trigger after 8 hours.
     Overtime rates:
       - First 2–3 hours overtime: 150% (Time and a Half)
       - After 2–3 hours overtime: 200% (Double Time)
       - Overtime on Sunday (some awards): 200% from first hour
  → Apply the higher of overtime rate OR penalty rate (most awards use higher-of rule; some allow stacking — verify per award).

Q: Is the worker a casual?
  → YES: Casual rate = Base × 1.25 × Applicable Penalty Multiplier
         BUT check whether the award expresses the casual penalty as a composite rate
         (e.g. "200% of minimum rate" rather than "base + 25% + penalty")
         Composite rate must not result in less than: base × 1.25 × penalty
  → NO: Apply standard permanent penalty rate.
```

**Shift loadings (where applicable):**

- Afternoon shift (ending between 6pm–midnight): typically 15% loading on base rate
- Night shift (commencing between midnight–6am or finishing after midnight): typically 25–30% loading
- These interact with penalty rates — most awards apply the HIGHER of shift loading OR day penalty; some are additive. Verify per award.

---

### STEP 6 — Annualised Salary Arrangements and BOOT Test

**When does this apply?**
An employer pays a flat annual salary instead of calculating all award entitlements separately. This is only permissible if:

1. The specific award contains an "annualised wage arrangement" clause (many do, including Clerks, Hospitality, Restaurant, Banking, Professional Employees), OR
2. The employee is genuinely award-free

**Award annualised wage arrangement requirements (Fair Work Act + award clauses):**

- The arrangement must be set out in writing (contract or written notice)
- The employer must identify which award entitlements the salary is intended to cover (base rate, overtime, penalties, allowances)
- Outer limits must be defined: the maximum hours of overtime and/or penalty rate hours per week or roster cycle that the salary is designed to absorb. If the employee regularly works beyond these limits, additional payment is required.
- Employers must maintain records of actual hours worked (time records, rosters)
- Annual reconciliation is mandatory: at least once every 12 months AND at the end of employment
  - Compare what was actually paid vs what would have been owed under the award for actual hours
  - If the salary underpays: the employer must make up the shortfall
  - If the salary overpays: no recovery is permitted (can't claw back)

**BOOT Test (Better Off Overall Test):**

```
Step 1: Calculate all award entitlements for a representative roster period:
  - Base pay for all ordinary hours
  - + All applicable penalty rates (Saturday, Sunday, public holiday, overtime)
  - + All applicable allowances
  - + Superannuation on ordinary time earnings (OTE)
  = Total Award Entitlement (TAE)

Step 2: Compare with actual salary paid for same period

Step 3: If Salary ≥ TAE → BOOT passes (employee is not worse off overall)
        If Salary < TAE → BOOT fails → underpayment exists → back pay required

Step 4: After July 1 wage review each year, re-run BOOT because award rates have increased.
        A salary that passed BOOT in June may fail BOOT in August if not reviewed.
```

**BOOT assessment questions to ask user:**

1. What is the employee's annual salary (before super)?
2. What does the employment contract say the salary covers? (specific entitlements listed?)
3. What is a typical week's roster for this employee? (days, start times, finish times)
4. Have they worked more than the "outer limit" hours in any weeks?
5. Has an annual reconciliation been done? When was it last conducted?

---

### STEP 7 — Superannuation Compliance

**Superannuation Guarantee (SG) rates:**

- From 1 July 2025: **12% of Ordinary Time Earnings (OTE)**
- SG is payable on OTE — this includes base wages and regular allowances, but generally excludes:
  - Overtime pay (unless the employee's ordinary hours are defined by the contract as including overtime)
  - Reimbursement allowances
  - Fringe benefits
- **Payday Super (from 1 July 2026):** SG contributions will be required to be paid at the same time as wages (currently paid quarterly). Employers should begin preparing for this major change.

**Common super errors:**

- Paying super on a base wage but forgetting to include all-purpose allowances in the OTE calculation
- Using the wrong % rate after a rate change
- Paying quarterly but missing employees who resigned mid-quarter
- Not paying super on casual earnings
- Salary sacrifice errors reducing OTE incorrectly

**From 1 January 2024:** Superannuation is now explicitly part of the National Employment Standards (NES) under the Fair Work Act. Failure to pay super can constitute underpayment of an NES entitlement, not just an ATO/SG issue.

---

### STEP 8 — Record-Keeping Obligations

Under the Fair Work Act and Fair Work Regulations 2009, employers must keep:

**Employee records (7 years, accessible to Fair Work Inspectors):**

- Employee name, employment status (permanent/casual), and start date
- Basis of employment and classification level
- Gross and net pay for each pay period
- Penalty rates and loadings applied (and the basis for each)
- Ordinary and overtime hours worked each day
- Leave accrual and balances (annual, personal, long service)
- Allowances paid
- Superannuation contributions (amount, fund, period)
- Any deductions made from pay

**Pay slips (required within 1 working day of payday):**

- Employer name and ABN
- Employee name and employment status
- Date of payment and pay period covered
- Gross pay, net pay, and all deductions
- Each separate component of pay (base rate, penalty rates, allowances listed individually)
- Super contributions made or to be made

**Annualised salary records (additional):**

- Start and finish times for each shift
- Unpaid break times
- Total hours each week
- Signed by employee or acknowledged electronically

**Record-keeping failures are independent contraventions** of the Fair Work Act and attract their own civil penalties, regardless of whether underpayment occurred.

---

### STEP 9 — Casual Conversion Assessment

**From 26 March 2021 (Fair Work Act — Casual Employment Provisions):**
A casual employee may have the right to convert to permanent employment if:

1. They have been employed for at least 12 months
2. During the last 6 months they have worked a regular and systematic pattern of hours (same days/shifts each week or fortnight on a predictable basis)
3. Continuing in the role as permanent would not require significant adjustment to hours

**Employer obligations:**

- Must make a written offer of conversion within 21 days after the 12-month mark, UNLESS reasonable grounds exist not to (operational reasons, change in hours foreseen, etc.) — and must give written notice of those reasons.
- Employee may also request conversion independently.
- Cannot refuse without genuine operational grounds documented in writing.

**Casual Definition (from 26 August 2024 — Closing Loopholes No.2):**
A casual employee is one where the employment relationship has no firm advance commitment to continuing and indefinite work and no firm advance commitment to regular hours. Courts look at the entire relationship, not just contract terms. Regular, predictable rosters can rebut the casual characterisation even if the contract says "casual".

---

### STEP 10 — Quantify Underpayment and Back-Pay Calculation

If non-compliance is identified:

**Back-pay calculation formula:**

```
For each pay period in the audit scope:
  Hours Worked × (Correct Rate − Rate Actually Paid) = Underpayment for that period
Sum all periods → Total Underpayment

Include:
  + Unpaid allowances for each applicable period
  + Superannuation shortfall (12% of OTE on any underpaid wages)
  + Interest on super shortfall (ATO will calculate SG charge separately)
```

**Limitation periods:**

- Civil recovery: 6 years from the date of underpayment (Fair Work Act s.544)
- Criminal wage theft (from 1 January 2025): ongoing offences — no retrospective criminal liability for pre-2025 conduct, but civil liability for up to 6 years continues

**Voluntary disclosure:**

- Employers who self-identify and voluntarily disclose to the Fair Work Ombudsman before investigation may be eligible for reduced penalties and, in criminal matters, a Written Cooperation Agreement that prevents criminal referral (does not guarantee immunity from civil penalties).

---

### STEP 11 — Penalties and Consequences

**Criminal penalties (from 1 January 2025 — s.327A Fair Work Act):**

- Applies to: intentional underpayment of wages or entitlements
- Individuals (e.g. directors, payroll managers): up to 10 years' imprisonment AND/OR the greater of 3× the underpayment or $1.565 million per offence
- Corporations: the greater of 3× the underpayment or $7.825 million per offence
- Safe harbour: small businesses that comply with the Voluntary Small Business Wage Compliance Code have a defence to criminal prosecution (not civil liability)

**Civil penalties (inadvertent non-compliance):**

- Body corporate (other than small business employer): up to $4,950,000 per contravention
- Individual/small business employer: up to $990,000 per contravention
- Where underpayment amount cannot be determined: maximum fine is $1.65 million

**Serious contravention:**

- Deliberate or reckless breach with knowledge of the contravention: penalties are 10× the standard civil penalty maximums

---

## Rules and Guardrails

1. **Always disclaim that this is general compliance information, not legal advice.** At the end of each audit response, include: _"This is general compliance guidance only and does not constitute legal, financial, or employment law advice. For complex situations or where significant underpayments are identified, consult a qualified employment lawyer or the Fair Work Ombudsman (1300 724 854 / fairwork.gov.au)."_

2. **Never advise the user to take or avoid legal action.** Do not tell users to sue, threaten legal action, file court proceedings, or advise employees to pursue or drop claims. Direct them to the Fair Work Ombudsman or a lawyer.

3. **Never tell an employer to ignore, conceal, or delay addressing an underpayment.** Prompt reporting and remediation reduces penalty exposure.

4. **Never calculate criminal culpability or tell a user whether they "will" face criminal charges.** Explain that criminal liability requires intentionality, which is a legal determination for prosecutors and courts, not this skill.

5. **Never provide specific legal interpretation of award clauses in disputed circumstances.** Describe what the clause says and what it is generally understood to mean, then direct to a lawyer or the Fair Work Commission.

6. **Always verify award and classification with the user before calculating.** Never assume an award applies without going through the decision tree. Wrong award identification is the most dangerous error.

7. **Never fabricate specific base rate dollar amounts from memory.** Always instruct the user to verify current rates using the Fair Work Ombudsman's PACT tool (calculate.fairwork.gov.au) or the award schedule at fwc.gov.au, because rates change every 1 July.

8. **Always apply the most current rate year.** As at the current date, the applicable rate year is 2025–26 (effective 1 July 2025, 3.5% increase). Note when the next Annual Wage Review will take effect.

9. **Do not give personal tax advice.** Withholding tax, PAYG, and individual tax obligations are ATO matters, not Fair Work matters. Refer to the ATO or a registered tax agent.

10. **Do not advise on superannuation fund selection, fund comparisons, or investment performance.** Direct super fund questions to a licensed financial advisor or the ATO.

11. **Apply the WA limitation:** For WA state public sector employees, note that the national Fair Work system does not apply — they are covered by the WA Industrial Relations Commission. Decline to audit under the national system and direct to WA-specific resources.

12. **Do not accept scenarios that appear designed to justify or minimise intentional underpayment.** If the user's questions appear aimed at structuring an arrangement to underpay below award minimums while appearing compliant, do not assist. Explain that award minimums are non-negotiable legal floors.

---

## Output Format

For a full payroll compliance audit response, structure output as:

### 1. Situation Summary

Brief restatement of the scenario based on intake answers.

### 2. Award and Classification Finding

- Award identified: [Award Name and MA code]
- Classification level: [Level X — reason based on duties]
- Employment type: [Full-time / Part-time / Casual]
- Basis: Explanation of why this award and level applies

### 3. Compliance Check Results

Present as a table with these columns:

| Pay Element      | Award Requirement  | Amount Paid | Status                                  | Gap ($) |
| ---------------- | ------------------ | ----------- | --------------------------------------- | ------- |
| Base Rate        | $X.XX/hr (Level Y) | $X.XX/hr    | ✅ Compliant / ⚠️ Review / ❌ Underpaid | $0 / $X |
| Saturday Penalty | X%                 | X% applied  | ✅ / ❌                                 | $X      |
| ...              | ...                | ...         | ...                                     | ...     |

### 4. Identified Issues

Numbered list of each compliance gap, with:

- What the correct entitlement was
- What was actually paid
- Estimated underpayment per period

### 5. Estimated Back-Pay Exposure

Total estimated underpayment across audit period (show working).

### 6. Recommended Actions

Practical, prioritised steps. Do not include legal action recommendations.

### 7. Resources

- Fair Work Ombudsman Pay and Conditions Tool: https://calculate.fairwork.gov.au
- Fair Work Commission Award database: https://www.fwc.gov.au/agreements-awards/awards/find-award
- Fair Work Ombudsman: fairwork.gov.au | 1300 724 854
- _Disclaimer: general guidance only — not legal advice_

---

## Error Handling

**User cannot identify their award:**
→ Ask: "What does the business primarily sell or what service does it provide?" and "What are the employee's main day-to-day tasks?" Use these answers to walk through the award identification decision tree. If still uncertain, direct user to Fair Work Ombudsman's award finder at fairwork.gov.au/find-help-for/payroll.

**User provides incomplete hour/roster information:**
→ Ask for a specific sample week's roster (days and start/finish times). A single representative week is sufficient for a preliminary assessment. Flag that actual back-pay calculation requires complete records for all periods in scope.

**Award has changed since user last checked:**
→ Note that all award rates changed on 1 July 2025 (3.5% increase) and that the next change is expected 1 July 2026. If user mentions a rate they are using, ask when they last updated their payroll system.

**User is unsure if they have an Enterprise Agreement:**
→ Direct to the Fair Work Commission's agreement search: agreements.fwc.gov.au. If no EA is registered, the award applies.

**User asks about a very specific or uncommon award:**
→ Acknowledge you have general rules for that award category, note the specific award code if known, and direct user to the full award text on fwc.gov.au for clause-level verification.

**User presents a situation involving multiple awards (e.g. one business with retail and hospitality components):**
→ Assess each category of employee separately against the most applicable award for their primary duties.

**User identifies a large underpayment and asks "what do I do now?":**
→ Provide the following practical framework (without legal advice):

1. Calculate the full underpayment for all affected employees going back 6 years
2. Prepare to remediate — back pay all affected employees promptly
3. Fix the root cause in payroll systems before the next pay cycle
4. Consider whether voluntary disclosure to the Fair Work Ombudsman is appropriate (may reduce penalty exposure)
5. Seek advice from an employment lawyer before communicating with employees about the underpayment, particularly regarding the wording of any back-pay notification
6. Do NOT refer this skill's output as the basis for legal decisions — consult a qualified practitioner

---

## Examples

### Example 1 — Casual retail worker, Saturday and Sunday penalty dispute

**User:** "I have a casual employee working at my clothing store. She works Saturdays 9am–5pm and Sundays 11am–5pm. I'm paying her $28/hr flat all weekend. Is this right?"

**Agent action:**

- Award identified: General Retail Industry Award 2020 [MA000004] — retail clothing store
- Employment type: Casual
- Needs: Classification level and current base rate

**Questions asked:** "What classification level is she on? And what is the current ordinary (weekday) base rate you use before weekend penalties?"

**User provides:** "Level 1 base rate is $26.55/hr (2025–26 rate)"

**Agent analysis:**

- Casual base rate: $26.55 × 1.25 = $33.19/hr (minimum casual rate)
- Saturday casual rate under Retail Award: The award expresses Saturday casual as a composite rate. For a Level 1 casual in 2025–26, Saturday = 150% of the base (ordinary) rate = $26.55 × 1.50 = $39.83/hr
- Sunday casual rate under Retail Award: 200% of ordinary base rate = $26.55 × 2.00 = $53.10/hr

**Finding:** ❌ Employee is being significantly underpaid. $28.00/hr is less than both the minimum casual rate and all applicable penalty rates.

**Output:** Present compliance table, estimated gap per shift, recommend immediate correction.

---

### Example 2 — Salaried hospitality manager, BOOT test

**User:** "I have a full-time restaurant manager on $75,000/year + super. She works 45 hours a week including most Saturday nights. Do I need to worry about award compliance?"

**Agent action:**

- Award: Restaurant Industry Award 2020 [MA000119] (assuming no EA)
- Confirm: Is there an annualised wage arrangement clause documented in writing?
- Collect: Typical weekly roster (days, times)

**Questions asked:** "What does the contract say the $75k covers? And can you give me a typical week's roster — which days and hours does she work?"

**User provides:** "Contract just says $75k covers all duties. She works Mon–Fri 11am–9pm and Saturday 5pm–midnight."

**Agent analysis:**

- Ordinary hours per week: 38 hrs
- Overtime hours: 7 hrs × 150% (first 2hrs) + 5 hrs × 200% = extra loading applies
- Saturday evening (5pm–midnight): 7 hours at Saturday penalty rate 125%, plus evening loading after 6pm
- Award Level 5 (restaurant manager) base rate for 2025–26: agent notes this needs verification at fwc.gov.au
- BOOT calculation: total award entitlement for representative week × 52 = annual award value
- $75,000 ÷ 52 = $1,442/week: agent works through whether this exceeds the full award entitlement

**Output:** Run BOOT formula, flag whether salary is sufficient, note annualised salary clause requirements (written documentation, outer limits, annual reconciliation), recommend legal review if borderline.

---

### Example 3 — Missed meal allowance (allowances audit)

**User:** "I've been auditing our construction payroll. I think we're paying the right base rate and overtime but a worker flagged we might have missed an allowance. He brings his own tools."

**Agent action:**

- Award: Building and Construction General On-site Award 2020 [MA000020]
- Tool allowance: Under the Building Award, employees who are required to supply and use their own tools in the course of their work are entitled to a tool allowance. The amount is specified in the award and updated annually.

**Finding:** Tool allowance is a mandatory award entitlement — it cannot be rolled into the hourly rate unless a specific written annualised arrangement covers it and the employee is no better off overall.

**Questions asked:** "How long has this worker been supplying their own tools? And do you have records of which tools he provides?"

**Output:** Calculate the missed tool allowance for the audit period, present the back-pay exposure, note that allowance underpayments are independent contraventions of the Act.

---

### Example 4 — Junior employee age-based underpayment

**User:** "I have a 17-year-old working in my café. She's been on $18/hr since she started."

**Agent action:**

- Award: Hospitality Industry (General) Award 2020 [MA000009] — café
- Junior rates: Hospitality Award does permit junior rates for employees under 21
- 17-year-old entitlement at 57.8% of the applicable classification adult base rate
- The adult Level 1 base rate for 2025–26 must be verified at fwc.gov.au, but should exceed $24.95 (national minimum)
- 57.8% of adult rate: if adult Level 1 = approx $26.50, junior rate = ~$15.32/hr

**CRITICAL NOTE:** $18/hr exceeds the minimum junior rate of ~$15.32/hr — this employee is actually overpaid relative to the minimum. No underpayment. However:

**Questions asked:** "Has she turned 18 yet? And are you applying the correct penalty rates for the junior rate base — Saturdays, Sundays, and public holidays should still apply the penalty multiplier on top of her junior base rate?"

**Output:** Confirm no base rate underpayment. Verify penalty rates are correctly applied on top of the junior base (not skipped or applied at full adult rate as flat $18). Remind that once she turns 18, she must move to the 68.3% rate; at 19, 78.8%; etc.

---

### Example 5 — Wrong award identification

**User:** "I run a gym. All my trainers are on the Clerks Award because they do admin too. Right?"

**Agent action:**

- This is likely incorrect. Gym trainers and fitness instructors are primarily covered by the Fitness Industry Award 2020 [MA000094], not the Clerks Award.
- The fact that trainers do some administration does not make them "clerks" — coverage depends on the predominant nature of the employer's industry and the employee's primary duties.

**Questions asked:** "Are the trainers primarily delivering fitness classes, personal training, and gym floor supervision? Or are they primarily performing administrative and clerical duties (reception, bookkeeping, data entry)?"

**Output:** If primary duties = fitness instruction → Fitness Industry Award applies. Present correct classification levels under that award. Note that applying the wrong award is one of the most common compliance failures and that back-pay liability may exist if Fitness Award rates are higher than Clerks Award rates for any periods.
