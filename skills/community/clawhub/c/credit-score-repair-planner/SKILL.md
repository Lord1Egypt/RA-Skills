---
name: credit-score-repair-planner
description: "Use when repairing or building credit: decodes the 5 FICO factors for a specific profile, plans statement-date utilization timing (AZEO), writes validation/623/goodwill dispute letters, and models the score impact of payoffs, new accounts, and derogatory age-off dates."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [credit-score, credit-repair, FICO, utilization, dispute-letters, personal-finance]
---

# Credit Score Repair Planner

## Overview

Credit repair is sold as a mystery ($99/mo services) but the FICO model is public enough to
engineer: 35% payment history, 30% amounts owed, 15% age, 10% new credit, 10% credit mix.
Most "bad credit" situations are one or two fixable mechanisms — a 90-day-late that ages off
in 7 years, utilization reported at the wrong moment, or collections that can be removed
with a validation letter. This skill decomposes a real profile into its score-drag terms,
puts dates on when each derogatory ages off, and generates the actual letters (validation,
623 dispute, goodwill, pay-for-delete counter).

## When to Use

- User shares scores/report summary and asks "how do I raise my score" or "how fast"
- Planning a mortgage/auto loan 3–12 months out and need utilization timed
- Collections / late payments / charge-offs on the report — removal strategy
- Thin file (no credit history): fastest safe build path
- Deciding: pay in full vs settle vs pay-for-delete; close old cards or not

**Don't use for:** credit-repair scams advice (CPN numbers, EIN credit — refuse those),
or predicting exact FICO numbers (nobody can; we model *direction and rough magnitude*).

## The FICO Decomposition (what actually moves scores)

| Factor | Weight | Levers you control | Typical swing |
|---|---|---|---|
| Payment history | 35% | remove lates (goodwill/dispute), no new lates | 606. | +30–100 from one removed 90-late |
| Amounts owed | 30% | statement-date balance, paying before statement | +20–60 from 70%→<9% util |
| Length of history | 15% | keep old cards open, don't churn before a loan | slow; age is time |
| New credit | 10% | hard pulls, new accounts | −5–10 per pull, fades 12 mo |
| Mix | 10% | installment vs revolving | small, don't buy products for it |

**Utilization mechanics (the biggest fast lever):**
- Card issuers report the **statement balance** (a few: current balance daily/interval).
- Score bands (per-card AND aggregate): <9% excellent, 10–29% good, 30–49% fair, 50%+ hurt,
  0% on ALL cards is slightly worse than tiny balances (no signal).
- **AZEO (All Zero Except One)**: before a mortgage pull, let one card report a tiny
  balance (<9% of its limit, e.g. $20), pay all others to $0 *before their statement
  closes* — not before the due date. Statement date ≠ due date; it's ~21–25 days earlier.

## Numbered Workflow

1. Collect: score(s), each card (limit, current balance, statement day), loans, derogatory
   items (type, date opened / date of first delinquency), recent inquiries, goal + date.
2. Run `scripts/credit_plan.py profile.json` — produces:
   - Factor decomposition: which factor(s) are dragging THIS profile
   - Utilization plan with exact dates: which card to leave reporting, when to pay the rest
   - Derogatory age-off timeline (7 yr from first delinquency for lates/collections; 10 yr
     for Chapter 7; closed positive accounts stay 10 yr — keep them open)
   - Letter queue with drafts (validation to collectors, 623 to bureaus, goodwill to issuer)
3. Sequence the plan: disputes first (30–45 day cycles), utilization in the month before
   the loan pull, no new credit 12 months before a mortgage.
4. Guardrails: never dispute accurate info as "not mine" (FCRA §813 perjury exposure);
   never pay a collector without a pay-for-delete or written settlement in hand; statute
   of limitations on the debt ≠ credit reporting time (paying old debt can revive neither
   the report entry nor, in most states, the lawsuit clock — but see Mo. below).

## Pitfalls

1. **Paying before the statement closes** vs before the due date — the single most common
   mistake. The bureau sees the statement snapshot.
2. **Closing old cards** shortens average age and spikes utilization (limit disappears).
   Keep them open; use a $0-fee card once a year to avoid inactivity closure.
3. **Disputing everything** → disputes flagged as frivolous, accounts "verified" harder to
   remove later. One well-grounded dispute per item.
4. **Pay-for-delete**: collectors have no obligation; get it IN WRITING before paying.
   Original-creditor charge-offs rarely do PFD; collection agencies often will.
5. **Settling old debt**: resets nothing on the report (the 7-yr clock runs from first
   delinquency) but partial payment CAN revive statute-of-limitations for a lawsuit in
   some states. Check the debt's SOL before touching anything >2 yr old.
6. **New credit before a mortgage**: rate shopping window is 14–45 days (one FICO pull);
   outside that, each inquiry costs. Freeze new apps 12 months out.
7. **"Credit repair" CPN/EIN schemes** are fraud; secondary numbers = new file = illegal.

## Example

```
$ python3 scripts/credit_plan.py examples/thin-file-util.json

PROFILE: 3 cards, $9,500 total limit, $6,230 reported (65.6% util), score 612
DRAG: Amounts owed (util 66% >> 9% target) + one 30-day late (11 mo old)

STEP 1 (this cycle): pay Card B ($4,100 → report $0; statement the 12th — pay by the 9th)
STEP 2: Card A reports $40 on the 3rd (AZEO), Card C paid to $0 before the 24th
        → projected aggregate util 0.4%; per-card A 1.2%   [score band: excellent]
EXPECTED: +40–70 pts in 1–2 cycles (util only); late ages off 2033-05 or goodwill now.
LETTERS: goodwill-adverse-action.txt → issuer of Card C (11-mo-old late, clean since)
AGE-OFF: 30-day late (first delinq 2025-04) → removed 2032-04; keep Card A (2016) open forever.
MORTGAGE MODE: freeze new apps 12 mo out; AZEO cycle = the month before pre-approval.
```

## Verification Checklist

- [ ] Statement dates (not due dates) confirmed for every card
- [ ] Aggregate AND per-card utilization both planned
- [ ] Derogatory age-off dates computed from first delinquency
- [ ] Letters queued with real account references and FCRA/623 citations
- [ ] User warned: never sign dispute forms asserting false facts
- [ ] Score swings quoted as ranges, never exact predictions
