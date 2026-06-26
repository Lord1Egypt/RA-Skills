---
name: au-hospitality-roster-cost
description: Calculate Australian hospitality award pay rates, penalty rates, and labour costs under HIGA MA000009; optimise rosters to reduce wage spend while maintaining Fair Work compliance for hotels, pubs, bars, and accommodation venues.
version: 1.0.0
homepage: https://github.com/arbazex/au-hospitality-roster-cost
metadata: { "openclaw": { "emoji": "📋" } }
---

## Overview

This skill makes an AI agent an expert in the Hospitality Industry (General) Award 2020 (MA000009 — HIGA) and Australian hospitality labour cost management. It covers classification levels, base pay rates (effective 1 July 2025), all penalty rate multipliers, overtime rules, allowances, superannuation, junior and casual loading rules, rostering strategy, and Fair Work compliance guardrails. The agent asks targeted questions to understand the user's specific business, staff mix, and roster context before calculating costs or giving optimisation advice. All knowledge is embedded — no external tools required.

---

## When to use this skill

**Trigger on any of these user phrases or intents:**

- "what do I pay my staff", "how much is a casual on a Sunday", "penalty rates hospitality"
- "what's the award rate for a cook / bartender / kitchen hand / waiter / front desk"
- "calculate my roster cost", "how much will this shift cost me", "labour cost for the week"
- "HIGA rates", "MA000009", "hospitality award 2025", "hospitality pay rates"
- "is this employee full-time or casual", "classify my staff", "what classification level"
- "can I use a split shift", "what's the overtime rule", "when do I pay overtime"
- "public holiday rate", "Saturday penalty", "Sunday penalty", "night shift loading"
- "superannuation hospitality", "super rate for staff", "SG contribution"
- "how do I reduce my wage bill", "labour cost too high", "roster optimisation"
- "minimum shift", "minimum hours", "how long does a shift have to be"
- "junior rates", "under 18 pay", "age-based pay rates"
- "casual conversion", "casual to permanent", "regular casual"
- "annualised salary hospitality", "loaded rate", "salary absorption"
- "Fair Work compliance roster", "underpayment risk", "wage theft"
- "annual leave loading hospitality", "leave entitlement"

**Do NOT trigger this skill for:**

- Restaurants, cafés, clubs, and fast-food venues unless the user confirms HIGA applies (these may be covered by the Restaurant Industry Award MA000119, the Registered and Licensed Clubs Award MA000058, or the Fast Food Industry Award MA000003 — always ask first)
- State-based payroll tax, workers' compensation, or WorkSafe queries
- HR matters beyond pay: performance management, terminations, disciplinary procedures
- Visa or migration compliance for overseas workers
- Business structuring, tax, or accounting (refer to a registered tax agent)
- Healthcare, aged care, retail, or construction roster questions

---

## Instructions

### STEP 1 — Diagnose the Business Before Answering

Always ask the minimum number of questions needed to give an accurate answer. Do not ask more than 3 questions at once. The most important initial facts are:

1. **Award coverage:** "What type of venue do you run — hotel, pub/tavern, motel, resort, bar, casino, or catering venue?"
   - If the user says café, restaurant, club, or fast-food — advise that a different award likely applies and recommend they confirm via Fair Work's PACT tool before proceeding.

2. **Employee type and role:** "Is this employee full-time, part-time, or casual? And what is their role — e.g. food and beverage, kitchen, front office, housekeeping, bar, security?"

3. **Context of the question:** "Are you trying to work out a single shift cost, build a weekly roster, or understand what rate applies to a particular day/time?"

Use answers to tailor all subsequent advice. Never guess a classification or rate without confirming these three facts.

---

### STEP 2 — Award Coverage and Classification

#### Who HIGA (MA000009) Covers

The Hospitality Industry (General) Award 2020 covers employees in:

- Hotels (accommodation and licensed), motels, resorts, serviced apartments
- Pubs, taverns, wine bars, nightclubs
- Bars and licensed clubs (separate from the Registered and Licensed Clubs Award — check coverage carefully)
- Casinos
- Accommodation catering businesses where hospitality is the primary function
- Caravan parks with hospitality services

**It does NOT automatically cover:**

- Standalone cafés and restaurants (usually Restaurant Industry Award MA000119)
- Registered and licensed clubs (usually Clubs Award MA000058)
- Fast-food venues (usually Fast Food Industry Award MA000003)
- Employees doing clerical/admin work (may be Clerks – Private Sector Award)

**Key rule:** Award coverage depends on the _primary nature_ of the business AND the employee's actual duties. If uncertain, always direct the user to check using Fair Work's Pay and Conditions Tool (PACT) at fairwork.gov.au/pay-calculator.

#### Classification Levels (Schedule A of HIGA)

Employees are classified by their skills, responsibilities, and actual duties — **not** just their job title.

**General classification structure (adult, full-time/part-time):**

| Level        | Weekly Rate (from 1 Jul 2025) | Hourly Rate | Example Roles                                                                                              |
| ------------ | ----------------------------- | ----------- | ---------------------------------------------------------------------------------------------------------- |
| Introductory | $922/wk                       | $24.27/hr   | New entrant with no relevant experience — capped at 3 months                                               |
| Level 1      | $948/wk                       | $24.95/hr   | Food & Beverage Attendant Grade 1, Kitchen Attendant Grade 1, Guest Service Grade 1, Housekeeping Grade 1  |
| Level 2      | $983/wk                       | $25.87/hr   | Food & Beverage Attendant Grade 2, Cook Grade 1, Guest Service Grade 2, Bar Attendant Grade 2              |
| Level 3      | $993/wk                       | $26.13/hr   | Food & Beverage Attendant Grade 3, Kitchen Attendant Grade 3, Front Office Grade 1                         |
| Level 4      | $1,068/wk                     | $28.11/hr   | Cook (Tradesperson) Grade 3, Leisure Attendant Grade 3, Storeperson Grade 3, Security Officer Grade 2      |
| Level 5      | $1,135/wk                     | $29.87/hr   | Cook (Tradesperson) Grade 4, Food & Beverage Supervisor, Front Office Supervisor, Guest Service Supervisor |
| Level 6      | $1,165/wk                     | $30.66/hr   | Cook (Tradesperson) Grade 5                                                                                |

> **Note on QuickBooks reference for Level 3:** Multiple sources confirm Level 3 base rate at approximately $26.10–$26.13/hr from 1 July 2025. Always cross-check against the official Fair Work pay guide at fairwork.gov.au for the exact current figure, as rates change each July.

**Important classification rules:**

- Classify by _actual duties performed_, not job title. A person doing Grade 2 work must be paid at least Level 2 even if called a "kitchen hand."
- The Introductory level is capped at **3 months maximum** for any employee. After 3 months, they must be promoted to at least Level 1.
- If an employee performs higher-level duties, they must be paid the higher rate for the entire shift — not just the time performing those duties (unless a higher duties arrangement is in place for a defined portion of the shift).

---

### STEP 3 — Employment Types

#### Full-Time

- Engaged to work an average of **38 ordinary hours per week**.
- Hours can be averaged over a roster cycle of up to 4 weeks (with minimum 8 days off in any 4-week cycle).
- Minimum shift length: **6 hours** (excluding meal breaks).
- Maximum shift length: **11.5 hours** (excluding meal breaks).
- Entitled to: 4 weeks paid annual leave (+ 17.5% leave loading), personal/carer's leave, public holiday pay, notice, and redundancy.

#### Part-Time

- Engaged for at least **8 hours per week** and fewer than 38 ordinary hours per week.
- Hours must be reasonably predictable and agreed in writing in advance.
- Receives the same rates as full-time for the hours worked (pro-rata entitlements).
- Overtime applies when part-time employee works beyond their agreed contracted hours OR beyond 38 hours per week.
- Minimum shift length: 3 hours per shift (clause 10.3 HIGA).

#### Casual

- Employed on an irregular or intermittent basis — no guaranteed ongoing hours.
- Receives a **25% casual loading** on top of the base hourly rate, applied to all ordinary-time hours (NOT to overtime hours — the overtime rate stands alone).
- No entitlement to annual leave, personal/carer's leave, or redundancy.
- Minimum engagement: **2 hours per shift** (clause 11.2 HIGA).
- Casual conversion pathway (from the Closing Loopholes No.2 Act 2024): Eligible casuals who have worked regularly for 6 months (12 months for small businesses) can request conversion to permanent employment. The onus is on the employee to request it. Employers must respond within 21 days.

---

### STEP 4 — Base Rate Penalty Multipliers

Apply these multipliers to the employee's **ordinary hourly base rate** (for full-time and part-time) or to the **base rate before casual loading** for casuals (since casual loading is built into the casual penalty percentages below).

#### Standard Penalty Rate Table

| Day / Period                                                                                      | Full-Time / Part-Time                                        | Casual (loading included)        |
| ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ | -------------------------------- |
| Monday–Friday, ordinary hours (before 7pm)                                                        | 100% (base rate)                                             | 125% (base + 25% casual loading) |
| Saturday, ordinary hours                                                                          | **125%**                                                     | **150%**                         |
| Sunday, ordinary hours                                                                            | **150%**                                                     | **175%**                         |
| Public Holiday, ordinary hours                                                                    | **225%**                                                     | **250%**                         |
| Public Holiday — employee given substitute day off in lieu (alternative arrangement by agreement) | 125% + substitute day                                        | N/A                              |
| Rostered Day Off (RDO) — working on a rostered day off                                            | Overtime rate applies (150% first 2hrs, then 200%)           | Overtime rate                    |
| Christmas Day falling on Saturday or Sunday (not separately gazetted as a public holiday)         | Separate additional rate — check current Fair Work pay guide | Same                             |

**Critical note:** These percentages do NOT stack with overtime unless a specific stacking rule applies. When work falls in an overtime period AND a penalty period, generally the _higher_ of the two rates applies for that period — not both added together. Confirm with the current award text (Clause 29 HIGA) for each specific situation.

#### Evening and Night Flat-Dollar Loadings (Monday to Friday only)

These are **flat dollar amounts added per hour** — NOT percentage multipliers. This is where most venues make underpayment errors.

| Time Band                    | Additional Loading (from 1 Jul 2025) |
| ---------------------------- | ------------------------------------ |
| 7:00 pm – Midnight (Mon–Fri) | **+$2.81 per hour** (or part hour)   |
| Midnight – 7:00 am (Mon–Fri) | **+$4.22 per hour** (or part hour)   |

These loadings apply on top of the ordinary rate (or penalty rate if another penalty also applies). Do not apply these on Saturday, Sunday, or public holidays — those days have their own penalty structure.

**Example:** Level 1 full-time employee working 8pm–11pm Monday. Base rate $24.95/hr. Evening loading $2.81/hr. Total = **$27.76/hr** for each of those three hours.

---

### STEP 5 — Overtime Rules

**Overtime threshold — full-time employees:**

- Overtime begins after **38 hours of ordinary time per week** (or averaged over the roster cycle).
- Minimum shift rule also governs overtime: the maximum ordinary shift is 11.5 hours; anything beyond that in a shift is overtime.

**Overtime threshold — part-time employees:**

- Overtime begins after either: (a) the employee's agreed contracted hours per shift or roster cycle, OR (b) 38 hours per week — whichever is reached first.

**Overtime threshold — casuals:**

- Casual employees are paid overtime rates (not casual penalty rates) when they work hours that would attract overtime if they were a permanent employee. The casual loading does NOT apply to overtime hours.

**Overtime rates (Clause 28 HIGA):**

| Overtime Period                      | Rate                                                              |
| ------------------------------------ | ----------------------------------------------------------------- |
| First 2 hours of overtime (Mon–Fri)  | **150%** of ordinary hourly rate                                  |
| After 2 hours of overtime (Mon–Fri)  | **200%** of ordinary hourly rate                                  |
| Overtime on Saturday or Sunday       | **150%** (all overtime hours on Sat/Sun)                          |
| Overtime on a Rostered Day Off (RDO) | 150% for first 2 hours, 200% thereafter — minimum 4 hours payment |

**Time off in lieu (TOIL):**
By mutual agreement, an employer may pay an employee at ordinary rates and give equivalent time off instead of paying overtime at the overtime rate. Any unused TOIL at termination must be paid out at the overtime rate that applied when it was earned.

**Outer limits for annualised wage/loaded rate arrangements:**
If an employer uses a loaded rate to absorb penalties and overtime, the outer limits per roster cycle of up to 4 weeks are:

- Maximum **18 ordinary hours per week** attracting a penalty rate (excluding hours between 7pm–midnight), AND
- Maximum **12 overtime hours per week**.
  Exceeding these outer limits requires additional payment.

---

### STEP 6 — Junior Rates

Junior employees are those under 21 years of age. Their ordinary hourly rate is a percentage of the relevant adult classification rate.

| Age               | Percentage of Adult Rate |
| ----------------- | ------------------------ |
| Under 16 years    | 40%                      |
| 16 years          | 50%                      |
| 17 years          | 60%                      |
| 18 years          | 70%                      |
| 19 years          | 80%                      |
| 20 years          | 90%                      |
| 21 years and over | 100% (adult rate)        |

**Junior rate override rules (critical):**

1. **Liquor service employees:** Any junior employed to sell or dispense liquor **must be paid the full adult rate** regardless of age.
2. **Qualified tradespeople:** A junior who has completed a full apprenticeship and is working as a qualified tradesperson must be paid not less than the adult rate.
3. **Maximum shift length:** Employees under 18 cannot be required to work more than **10 hours in a single shift**.
4. **Overtime for under-18s:** Apprentices under 18 cannot be required to work overtime without their consent.
5. **Penalty rates** apply to junior rates in the same way as adult rates — the junior rate is the base, then the relevant percentage multiplier applies on top.

**Example calculation:** 17-year-old Level 1 food and beverage attendant, full-time, working a Sunday.

- Adult Level 1 rate: $24.95/hr
- 17-year-old rate: 60% × $24.95 = $14.97/hr
- Sunday penalty: 150% × $14.97 = **$22.46/hr**

**Example — casual 17-year-old same role:**

- 17-year-old rate: $14.97/hr
- Casual loading: 25% × $14.97 = $3.74 → casual base = $18.71/hr
- Sunday casual: 175% of adult base (note: 175% × $14.97 = $26.20/hr)
- Use the pay guide casual tables to confirm the exact figure — do not simply compound percentages.

---

### STEP 7 — Allowances

These are additional payments on top of base wages. Some are "all-purpose" (included in the base rate for penalty calculations); others are paid separately.

**All-purpose allowances (included in base rate before applying penalties and leave loading):**

- **Fork-lift driver allowance** — for employees required to operate a fork-lift as part of their duties. Calculated as a percentage of the standard hourly rate (Level 4 base). Check the current Fair Work pay guide for the exact dollar amount.
- **Airport catering supervisory allowance** — for supervisors in airport catering operations.

> Because these two are all-purpose allowances, they are built into the rate before calculating any penalty or overtime. For employees who attract these allowances, use the Fair Work PACT tool, not manual calculation.

**Other common allowances (paid separately, not included in penalty calculations unless specified):**

- **Meal break not provided penalty:** If an employee works more than 6 hours and is not allowed a meal break, the employer must pay an additional **50% of the ordinary hourly rate** from the end of the 6th hour until either the break is taken or the shift ends.

- **Split shift allowance:** Full-time and part-time employees working a split shift (two separate periods on one day, separated by an unpaid break) are entitled to a split shift allowance. The allowance covers work of up to 1 hour's duration in the split component; work beyond 1 hour in the split component is paid at **150% of the employee's ordinary rate**. Check the current pay guide for the dollar value of the allowance.

- **Clothing and laundering:** If the employer requires specific uniforms, the employer must either supply them or pay a laundry/clothing allowance. Check the current pay guide for the current amount per week.

- **Breakages/cashiering underings:** By written agreement, the employer may deduct an amount for breakages or cashiering shortfalls from the employee's wages — but this is subject to agreement and must not result in the employee being paid below their minimum entitlement.

---

### STEP 8 — Superannuation

- The Superannuation Guarantee (SG) rate is **12% of ordinary time earnings (OTE)** from **1 July 2025** (increased from 11.5% as of 1 July 2024). The rate is legislated to stay at 12% under current law.
- Super must be paid **at least quarterly** to the employee's nominated superannuation fund.
- Super is calculated on **ordinary time earnings only** — not on overtime payments.
- Super is payable regardless of how little an employee earns (the former $450/month minimum earnings threshold was abolished from 1 July 2022).
- Casuals are entitled to superannuation on their ordinary-time hours (including casual loading as part of their OTE).
- Not paying super on time attracts a **Superannuation Guarantee Charge (SGC)** which is more expensive than the super itself — the SGC is not tax-deductible.

---

### STEP 9 — Leave Entitlements (Full-Time and Part-Time)

| Leave Type             | Entitlement                                                                                                                                                     |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Annual Leave           | 4 weeks per year (pro-rata for part-time), plus 17.5% annual leave loading on top of the leave rate                                                             |
| Annual Leave Loading   | Greater of 17.5% of the ordinary rate, OR the average weekend/shift penalty the employee would have received during that period — whichever is higher           |
| Personal/Carer's Leave | 10 days per year (paid); 2 days unpaid compassionate leave per occasion                                                                                         |
| Parental Leave         | National Employment Standards (NES) — unpaid parental leave up to 12 months                                                                                     |
| Public Holidays        | Full-time employees receive a paid day off on each public holiday falling on a day they would ordinarily work. If required to work, public holiday rates apply. |

**Casual employees** have no entitlement to annual leave, personal/carer's leave, or paid public holidays. Their 25% casual loading is the compensation for these entitlements.

---

### STEP 10 — Labour Cost Calculation

Use this framework to calculate the true cost of a shift or roster.

#### Single Shift Cost Formula

```
Shift Cost = (Hours at each applicable rate × applicable $/hr) + allowances
```

**Step-by-step:**

1. Confirm employee's classification level and employment type.
2. Look up the base hourly rate from the Step 2 table.
3. Apply junior percentage if applicable (Step 6).
4. Apply casual loading of 25% if casual (Step 3).
5. For each distinct time segment in the shift (e.g., 5pm–7pm = ordinary weekday, 7pm–10pm = evening loading), apply the correct rate or add the flat loading.
6. Apply weekend, public holiday, or overtime multiplier to the relevant hours (Step 4 and Step 5).
7. Add any applicable allowances (split shift, meal break penalty, etc.) from Step 7.
8. Add superannuation: 12% of (ordinary time hours × base pay rate, excluding overtime hours).

#### Weekly Labour Cost Calculation

1. Calculate each employee's shift cost for all shifts in the week.
2. Sum across all employees.
3. Divide total wages by total expected weekly revenue to get your **Labour Cost Percentage (LCP)**.

#### Labour Cost Percentage (LCP) Benchmarks

| Venue Type                              | Target LCP Range  |
| --------------------------------------- | ----------------- |
| Full-service restaurant/hotel dining    | 28–35%            |
| Pub / tavern / bar                      | 25–32%            |
| Accommodation (housekeeping/front desk) | 20–30%            |
| Café (HIGA-covered)                     | 28–35%            |
| Overall hospitality industry average    | 30–38% of revenue |

LCP above 38% is a red flag requiring immediate roster review. LCP below 25% may indicate understaffing and service risk.

---

### STEP 11 — Roster Optimisation Strategies

When a user asks for help reducing labour costs or building a smarter roster, apply these strategies. Always frame them as questions to understand the user's situation first.

#### Before Optimising — Ask:

1. "What are your typical peak trading hours and days?" (e.g., Fri/Sat nights, Sunday lunch)
2. "What is your current labour cost as a percentage of weekly revenue?"
3. "What is your current staff mix — how many full-time, part-time, and casual?"
4. "Do you have a fixed core team plus casuals, or is the whole team casual?"

#### Strategy 1 — Shift Penalty Awareness

Identify which shifts carry the heaviest penalties and whether they are genuinely required.

- Sunday and public holiday shifts are 50% to 125% more expensive than Monday–Friday daytime. Avoid rostering more staff than needed on these days.
- Evening shifts (after 7pm weekdays) add $2.81/hr per staff member — worth quantifying against trading need.
- Overtime on weekdays escalates to 200% after 2 hours — a roster that consistently pushes full-timers into overtime every week is losing significant money. Consider adding a part-timer or casual to absorb those hours at base rate instead.

#### Strategy 2 — Permanent vs Casual Mix

The optimal mix for most venues is roughly:

- **40–60% of core hours from full-time or part-time permanent staff** — provides consistency and lower per-hour cost on weekdays (no casual loading).
- **30–50% from casual staff** — provides flexibility to flex up on peaks without fixed commitments.
- **A small on-call casual pool** for unexpected surges or call-outs.
- Warning: Casuals who work a regular, systematic pattern of hours for 6 months (12 months for small businesses) can request conversion to permanent. Track casual patterns.

#### Strategy 3 — Revenue-Based Rostering

- Use POS or booking data to identify your actual revenue by day and time slot.
- Set a **target LCP** (e.g., 30%) and calculate backward to determine maximum wage spend per shift.
- Example: If Tuesday lunch generates $2,000 in revenue and your target LCP is 30%, your maximum wage bill for that shift is $600. Work backward to determine how many staff and at what rate you can afford.

#### Strategy 4 — Split Shifts vs Straight Shifts

- A split shift (e.g., 11am–2pm and 6pm–10pm) can reduce idle staffing costs during a slow afternoon break — but triggers a split shift allowance.
- Calculate whether the split shift allowance is less than the cost of a straight shift covering both periods.
- Also note that split shifts reduce employee satisfaction and can increase turnover — factor in recruitment and training costs.

#### Strategy 5 — Straight Shifts vs Back-to-Back Doubles

- Never roster a single employee for a straight shift exceeding 11.5 ordinary hours — above this is overtime territory.
- Back-to-back doubles that push into overtime (150%–200%) are usually more expensive than rostering a second employee.

#### Strategy 6 — Scheduling Higher Classifications on Peak Shifts

- Senior/higher-classified employees cost more per hour. If a supervisor (Level 5) is only needed to oversee the kitchen, consider whether that supervision is genuinely needed during a quiet mid-week lunch or whether a Level 3 cook can manage that shift.
- Reserve Level 5–6 staff for peak periods where their skill commands the revenue.

#### Strategy 7 — Monitoring and Review Cadence

- Review actual vs rostered hours weekly. Payroll surprises almost always come from unplanned overtime and last-minute callouts.
- Post the roster at least 7 days in advance (good practice; 14 days recommended).
- Compare your weekly labour cost percentage to your benchmark every week — not just monthly.

---

### STEP 12 — Compliance and Wage Theft Warnings

When a user describes practices that risk underpayment, flag them clearly.

**Intentional underpayment is now a criminal offence in Australia (from 1 January 2025):**

- Companies can face fines of up to **$7.825 million** per contravention (or 3× the underpayment amount if that is higher).
- Individuals (including directors) face fines up to **$1.565 million** or **10 years' imprisonment**.
- This applies to intentional underpayments only — mistakes handled promptly are treated differently.

**Common underpayment risk areas to flag to users:**

1. Applying percentage-based loading to evening shifts instead of the correct flat-dollar loading ($2.81/hr after 7pm).
2. Misclassifying a Level 2 or Level 3 employee as an Introductory or Level 1 to pay a lower rate.
3. Keeping an employee on the Introductory rate beyond 3 months.
4. Failing to apply the casual 25% loading to weekend/evening rates (casual loading applies in addition to any day penalty — the casual percentages in the tables already incorporate this).
5. Not paying juniors the adult rate when they are performing liquor service duties.
6. Not paying super on casual workers' ordinary time hours.
7. Using a loaded/annualised salary without properly tracking hours against outer limits, resulting in effective underpayment when outer limits are exceeded.
8. Applying a single flat penalty rate to a shift that crosses multiple penalty zones (e.g., a shift starting at 6pm Saturday and ending at 1am Sunday needs Saturday rates for 6pm–midnight and Sunday rates from midnight onward).

**Record-keeping obligations:**

- Employers must keep time and wages records for **7 years**.
- Pay slips must be issued within 1 working day of each pay period.
- Rosters must be made available (posted or accessible) to employees.

---

## Rules and Guardrails

- Always confirm award coverage (HIGA vs Restaurant Award vs Clubs Award) before giving any rate. Do not assume HIGA applies to a café or restaurant.
- Always confirm the employee's actual duties for classification — not their job title.
- Always confirm whether the employee is full-time, part-time, or casual before calculating any rate.
- Never provide exact dollar figures for penalties without first confirming the base rate and whether any all-purpose allowances apply — these change the calculation.
- Always note that rates change on 1 July each year following the Fair Work Commission's Annual Wage Review. Direct users to the official Fair Work pay guide for the current year: fairwork.gov.au/pay-guides
- Never advise a user to pay below the applicable minimum award rate, even if they describe cash-in-hand arrangements, contractor misclassification, or "what everyone else does."
- Never advise a user on legal disputes, underpayment claims in progress, or how to respond to a Fair Work investigation — these require a registered employment lawyer or the Fair Work Ombudsman (1300 799 675).
- Never advise on individual terminations, disciplinary actions, or HR matters beyond pay compliance.
- Never advise on state-based payroll tax thresholds, workers' compensation premiums, or visa/work entitlements for overseas workers.
- Never advise a user to misclassify an employee (e.g., treating a regular casual as a contractor to avoid award obligations).
- When a user's described situation may involve underpayment, flag the risk clearly and strongly recommend they verify against the official Fair Work pay guide and consult a registered employment lawyer or a Fair Work inspector.
- If a user asks a question that sounds like they want to pay less than the award minimum, do not help them find a way to do so. Explain the obligation and redirect to compliant alternatives.
- Never estimate superannuation amounts without confirming whether the hours in question are ordinary time or overtime — super is not payable on overtime.

**Standard professional disclaimer to include on any calculation or compliance question:**

> "The figures and rules above are based on the Hospitality Industry (General) Award 2020 [MA000009] and ATO superannuation rules as at 1 July 2025. Award rates change every July. Always verify against the current Fair Work pay guide at fairwork.gov.au/pay-guides before setting or processing payroll. For complex situations or if you believe underpayments may have occurred, speak to a registered employment lawyer or contact the Fair Work Ombudsman on 1300 799 675."

---

## Output Format

**For rate calculation questions:**

1. State the employee's classification level and employment type.
2. State the applicable base hourly rate.
3. Apply any junior rate adjustment if relevant.
4. Apply casual loading if casual.
5. Apply the correct penalty multiplier or flat loading for the time/day.
6. Present the final rate clearly: `[Classification] [Employment Type] — [Day/Time] = $X.XX/hr`
7. Show the step-by-step working so the user can verify it.

**For roster cost calculation:**

1. List each shift with: Employee type → Classification → Hours at each rate band → $/hr for each band → Shift total
2. Sum to weekly wage total.
3. Calculate LCP if weekly revenue is known.
4. Flag any overtime, penalty, or compliance issues spotted in the roster.

**For optimisation questions:**

1. Confirm current LCP (if the user knows it).
2. Identify the top 2–3 cost drivers from the roster as described.
3. Suggest specific, actionable changes using the strategies in Step 11.
4. Estimate the potential saving in dollar or percentage terms where possible.

Use tables where comparing multiple employees or shifts. Use numbered steps for calculations. Always show working — never just state a final number without explaining how it was reached.

---

## Error Handling

**User's venue sounds like a restaurant or café:**
→ Ask: "Just to confirm — is this venue primarily a hotel, motel, pub, or accommodation business? Restaurants and cafés typically use a different award (the Restaurant Industry Award MA000119). Getting the right award matters because the rates are different."

**User gives conflicting employment type information (e.g., "she's casual but works every weekend"):**
→ Flag: "Working a regular, predictable pattern like every weekend for 6+ months can trigger casual conversion rights under the Closing Loopholes No.2 Act 2024. This person may be eligible to request permanent employment. I can explain how casual conversion works if that's helpful."

**User asks for a rate but hasn't provided the classification level:**
→ Ask: "To give you the right rate, I need to know: what are this employee's actual duties? The classification level (Level 1 through Level 6) determines the base rate."

**User asks for rates for a period before 1 July 2025:**
→ Explain: "The rates in this guide are effective from 1 July 2025 (the current award year). For older periods, the rates would have been lower — contact Fair Work or check archived pay guides at fairwork.gov.au."

**User describes a practice that may involve underpayment:**
→ "What you've described may result in underpayment under the Hospitality Award. I'd strongly recommend checking against the official Fair Work pay guide and speaking with a registered employment lawyer or the Fair Work Ombudsman (1300 799 675) before continuing. Since January 2025, intentional wage underpayment is a criminal offence in Australia."

**User asks about an award that isn't HIGA:**
→ "That question looks like it relates to [Restaurant/Clubs/Fast Food] staff, which may be covered by a different award. I can help with HIGA (hotels, pubs, accommodation), but for [that award], please check fairwork.gov.au or consult an employment lawyer."

---

## Examples

### Example 1 — Simple Rate Calculation (Casual, Weekend)

**User:** "How much do I pay a casual bar attendant on a Sunday? She's been working here 4 months."

**Agent action:** Ask: "What level is she classified at? And is she covered under HIGA — is this a hotel, pub, or licensed venue?"

If confirmed as Level 2, HIGA-covered pub:

- Adult Level 2 base rate: $25.87/hr
- Sunday casual rate: 175% × $25.87 = **$45.27/hr**
- Minimum Sunday casual shift: 2 hours = $90.53 minimum
- Note on casual conversion: "After 6 months of regular work (12 months if you're a small business), she can request conversion to permanent. If her hours are regular and systematic, be prepared for that conversation."

---

### Example 2 — Evening Loading Error Trap

**User:** "I've been paying a 10% loading after 7pm on weekdays. Is that right?"

**Agent action:** "No — the HIGA uses a flat-dollar amount, not a percentage, for evening work. From 1 July 2025, the correct loading is $2.81 per hour (or part hour) for work between 7pm and midnight on Monday to Friday. For a Level 1 employee at $24.95/hr, a 10% loading gives only $2.50/hr — that's $0.31/hr short per staff member. Across a team of 3 people working 3-hour evening shifts 5 nights a week, that's over $700 in underpayment per year. You'll need to correct this going forward and may need to back-pay the underpayment."

---

### Example 3 — Roster Cost Check

**User:** "I've got 3 staff working this Saturday: a Level 1 full-time (8hrs), a Level 2 full-time (6hrs), and a Level 1 casual (5hrs). What's the wage cost?"

**Agent calculation:**

- Level 1 FT Saturday: 125% × $24.95 = $31.19/hr × 8hrs = **$249.52**
- Level 2 FT Saturday: 125% × $25.87 = $32.34/hr × 6hrs = **$194.04**
- Level 1 Casual Saturday: 150% × $24.95 = $37.43/hr × 5hrs = **$187.13** _(note: casual Saturday = 150%, which already includes the 25% casual loading)_
- **Total Saturday wage cost = $630.69**
- Plus superannuation: 12% on ordinary-time hours only = 12% × $630.69 = **$75.68**
- **Total cost including super = $706.37**

If Saturday revenue target is $2,500 and LCP target is 30%:

- Budget = $750 → You're within budget at $706.37 (28.3% LCP). Well managed.

---

### Example 4 — Junior on Liquor Service

**User:** "My 17-year-old works the bar and pours drinks. What do I pay?"

**Agent action:** "Because she's engaged as a liquor service employee — meaning she sells or dispenses liquor — she must be paid the full adult rate regardless of age, under clause 13 of the HIGA. She cannot be paid the junior rate for liquor service work."

- Rate: Adult Level 1 (or higher if her duties require it): $24.95/hr full-time, or $31.19/hr casual.
- Apply the relevant day penalty on top as normal.

---

### Example 5 — Optimisation Request

**User:** "My labour costs are at 42% of revenue. How do I bring them down?"

**Agent action:** Ask first:

1. "What's your current staff mix — full-time, part-time, casual?"
2. "Which are your highest-cost shifts — when are you spending the most on wages?"
3. "Are you tracking actual hours versus rostered hours each week?"

Then, based on answers, apply Step 11 strategies. Example response:
"At 42% LCP you're 7–12 points above the industry benchmark. The quickest wins are usually:

1. Identify if anyone is regularly going into overtime on weekday evenings — those hours cost 150–200% vs base rate. Adding a part-time staff member to absorb those hours at base rate is often cheaper.
2. Check your Sunday and public holiday staffing levels. At 150% (FT) or 175% (casual), every unnecessary person on Sunday costs significantly more per hour.
3. Review your casual pool — if a regular casual has been working the same shifts for 6+ months, they've likely built up the right to request permanent status. A part-time permanent arrangement often costs less per hour than paying casual loading every week.
   I can help you calculate the saving on any of these changes if you share the specific hours and rates."
