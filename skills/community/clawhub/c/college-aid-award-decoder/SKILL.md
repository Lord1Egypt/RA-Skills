---
name: college-aid-award-decoder
description: Use when comparing college financial aid award letters, deciding between schools on money, or decoding an aid offer before accepting — classifies every award line as gift aid vs work-study vs loan (the letters deliberately blur this), computes true Net Price per school, projects 4-year loan debt with monthly repayment at real rates, flags MISLEADING letters that count loans as "aid", and drafts the professional-judgment appeal letter for special circumstances (job loss, medical bills) that can add thousands in grants.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [college, financial-aid, education, student-loans, net-price, comparison]
---

# College Aid Award Decoder

## Overview
Financial aid award letters are the least honest documents families routinely receive. There is **no federal template**: one school labels a $5,500 Direct Unsubsidized Loan "Financial Aid Award," another buries a grant in the same table as a PLUS loan parents must repay, and a third front-loads grants to freshman year then lets them decay while tuition climbs. Studies of award letters consistently find a third or more don't even show the total Cost of Attendance — without which "aid" is meaningless. Families compare the BIG NUMBER at the bottom, which is exactly what the letter is engineered to inflate.

This decoder treats an award letter as what it is: an unordered pile of money from four fundamentally different sources. It classifies every line (gift aid you keep, work-study you earn hourly, federal loans you repay at known rates, parent/private loans that shouldn't be in the letter at all), computes **Net Price = COA − gift aid** (the only cross-school comparable), projects debt at graduation under a standard 10-year repayment plan, and flags letters that would fail the federal Aid Summary requirements.

## When to Use
- Award letters from 2+ schools arrived and the family is comparing them
- A letter's bottom line looks great but something feels off (it's usually loans relabeled as aid)
- Deciding whether a "cheaper" school's offer is actually cheaper after 4 years
- Family finances changed after FAFSA (job loss, medical, divorce) — appeal letter time
- Deciding work-study vs a part-time job off campus (work-study hours are capped and taxed the same)

**Don't use for:** CSS Profile / FAFSA form filling itself (that's application-stage), student loan *repayment* strategy after graduation (that's student-loan-strategist territory), or 529/savings planning (different instrument).

## Quick Start
```bash
# Side-by-side decode of two schools (or run --demo for a worked example)
python3 scripts/aid_compare.py compare \
    --school "State U" --coa 28400 \
        --award "Pell Grant,3748" "University Grant,6000" "Direct Subsidized,3500" "Work-Study,2000" \
    --school "Private College" --coa 62000 \
        --award "Merit Scholarship,22000" "Direct Subsidized,3500" "Direct Unsubsidized,2000" "PLUS,12000"

# Project one school's 4-year debt and monthly payment
python3 scripts/aid_compare.py debt --school "State U" --sub 3500 --unsub 2000 --years 4

# Appeal letter after a job loss changed everything
python3 scripts/aid_compare.py appeal --school "State U" --circumstance "parent job loss March 2026" \
    --income-drop 42000 --aid-year 2026-27 > appeal_letter.txt
```

## How the Classification Works
Every award line is keyword-matched to one of four classes — the classification IS the tool:

| Class | Keywords matched | Counts toward Net Price? | Repaid? |
|---|---|---|---|
| GIFT | pell, grant, scholarship, fellowship, tuition remission, merit, need-based | ✅ reduces net price | never |
| WORK | work-study, work study, campus job, student employment | ❌ earned hourly, ~10-15 h/wk | n/a |
| FED_LOAN | direct subsidized, direct unsubsidized, stafford, perkins | ❌ | yes, fixed federal rates |
| OTHER_LOAN | plus, parent plus, private, alternative, institutional loan | ❌ | yes — and it shouldn't be counted as aid at all |

Rates used for projections (2026-27 academic year, undergrad): Direct Subsidized/Unsubsidized ≈ 6.3-6.5%, Grad PLUS/Parent PLUS ≈ 9%. Subsidized interest is paid by ED while in school; unsubsidized accrues from disbursement — the script models both honestly.

## The Five Letter Red Flags (checked automatically)
1. **Loans presented as aid** — if FED_LOAN + OTHER_LOAN + WORK > 40% of the total award, the letter is flagged MISLEADING.
2. **No COA shown** — aid without a price tag is meaningless; script refuses to rank schools without it.
3. **Front-loaded grants** — ask "is this renewable at what GPA, for how many years?" (checklist in references/).
4. **PLUS in the aid package** — a parent loan is never "aid"; schools include it to shrink the apparent gap.
5. **Rounded monthly "payment plans"** presented instead of interest costs — always recompute.

## Numbered Workflow
1. Enter each school's full COA (tuition+fees+room+board+books+transport) — reject letters that don't state it.
2. Enter every award line as `"Name,amount"` — use the letter's exact wording so classification is honest.
3. Read the comparison: Net Price per school, gap after family contribution, debt at graduation, monthly payment.
4. Check flags: MISLEADING letters get re-read with the four-class table printed.
5. Run the appeal letter if circumstances changed — special circumstances reviews (34 CFR 673.4 "professional judgment") can convert loans to grants.
6. Verify renewal terms for every gift line before deciding (references/award-letter-audit.md).

## Pitfalls
1. **Comparing total aid instead of Net Price** — a $40k award against a $62k COA is worse than $12k against $14k. Always rank by net price.
2. **Forgetting work-study isn't guaranteed** — it's a capped hourly job you must find; budget it at 60% realization.
3. **Treating PLUS as the student's loan** — it's the parent's, credit-checked, at ~9%; exclude it before comparing offers.
4. **Using freshman-year grants as the 4-year average** — grants decay, tuition rises ~3-5%/yr; the debt projection assumes flat awards (already optimistic).
5. **Ignoring fees inside COA vs billed separately** — use one consistent COA definition per comparison or the ranking flips.

## Verification Checklist
- [ ] Every school compared with the same COA definition
- [ ] Every award line classified (script prints unknown lines as UNKNOWN — resolve these manually)
- [ ] Net Price, gap, and debt-at-graduation compared side by side
- [ ] MISLEADING flag reviewed for each letter
- [ ] Renewal terms confirmed for all gift aid before deposit deadline (usually May 1)
- [ ] Appeal letter sent to the financial aid office, not admissions

## One-Shot Recipes
**"Two schools, one kid, decision deadline May 1"** → `compare` both letters, read Net Price delta, run `debt` on the cheaper-net school, sanity-check the delta against 4 years of payments; if delta < $5k total and the other school is strongly preferred, that's a knowable price, not a trap.
**"Dad got laid off in March"** → `appeal` with income-drop quantified; attach termination letter + final paystub; request review for BOTH the current and next aid year.
**"Letter shows only 'Aid: $38,000'"** → demand the itemized list — no COA, no decision.
