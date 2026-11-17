# Credit Repair — Deep Reference

## FICO factor mechanics

### Payment history (35%)
Severity ladder: 30 < 60 < 90+ day late; one 90-day late ≈ "recency + severity" hit of
60–110 points depending on starting score (higher scores lose MORE — the model punishes
deviation from the profile's own history). Recency matters most: a late loses most of its
drag after 24 months clean.

### Amounts owed (30%)
- Aggregate utilization + per-card utilization + number of maxed cards.
- Bands: <9% best; 10–29% fine; 30–49% fair; 50%+ heavy drag; 100% maxed worst.
- All-zero is mildly negative (no active signal) — hence AZEO.
- Revolving >> installment in this bucket. Paying off a car loan barely moves util;
  paying cards moves it a lot.
- Charge-off with balance still hurts util AND history — settle/PFD helps both.

### Age (15%)
Average age of open accounts; oldest account age. Closing a card does NOT remove it from
age calculations for 10 years (closed positive accounts report ~10 yr) — the real damage
of closing is the limit vanishing from utilization.

### New credit (10%)
Hard inquiries: −5–10 pts each typically, fade at 12 months, off report at 24. Mortgage/
auto/student shopping: older FICO = 14-day de-dupe window, newer = 45. Credit cards NEVER
de-dupe.

### Mix (10%)
Revolving + installment both present is mildly better. Never open a loan for mix alone.

## Reporting mechanics (the real game)

- ~10% of large issuers report on month-end instead of statement (Amex historically
  reports statement; Chase statement; Discover statement; Capital One statement).
- If unsure: pay to $0 (or the AZEO target) 3–4 business days BEFORE the statement close.
- "Current balance" mid-cycle is invisible to bureaus unless the issuer reports mid-cycle.
- Authorized-user tradelines: count for util+age in most FICO models (legit: family
  adds you to an old clean card; you don't even need the physical card). Rent/utility
  reporting services move VantageScore more than FICO; some mortgage resellers ignore.

## Derogatory timelines (from date of FIRST delinquency)

| Item | Reports for | Notes |
|---|---|---|
| Late payments | 7 yr | each month's late falls off individually |
| Collection | 7 yr 180 d from first delinquency | paying doesn't reset the clock |
| Charge-off | 7 yr | status updates as sold/closed don't reset |
| Chapter 7 | 10 yr | from filing date |
| Chapter 13 | 7 yr | from filing date |
| Foreclosure | 7 yr | |
| Student loan default | 7 yr | rehabilitation removes it early |
| Closed positive account | 10 yr | keep old cards open |
| Hard inquiry | 2 yr | score impact 12 mo |

## The letter ladder

1. **Debt validation (FDCPA §1692g)** — to a COLLECTION AGENCY within 30 days of first
   contact: demand the amount, original creditor, and proof. They must cease collection
   until they validate. No 30-day window? They still must validate if you dispute in
   writing; they just may continue if they mark it "disputed."
2. **Bureau dispute (FCRA §611)** — mail Certified, to ONE bureau at a time for one item.
   30 days (45 if you used the free annual report). Unverified → deleted.
3. **Method-of-verification (§611(b)(1) follow-up)** — "how was this verified?" forces
   the bureau to name the furnisher; weak verification is removal leverage.
4. **Direct dispute (Reg V §1022.43 / "623 dispute")** — to the FURNISHER (the bank/
   collector). They must investigate like the bureaus do. Great when the bureau
   "verifies" wrongly.
5. **Goodwill letter** — for ACCURATE lates: polite, brief, clean-since story, ask for
   courtesy removal. Works best on 1) isolated, old, 2) issuer you still hold, 3) via
   executive office / social-media-escalation route. Not a right — a ask.
6. **Pay-for-delete** — collectors only (not OCs), get terms in writing, pay AFTER the
   signed agreement. "We will delete upon payment" language, not "paid in full" promise.

## Statute of limitations vs reporting (critical distinction)

- SOL (lawsuit window) by state: 3–10 yr, depends on debt type (written contract vs
  open account). Reset by payment in SOME states (partial payment restarts), by new
  written promise in most.
- Reporting clock (7 yr) NEVER resets from payment. Paying a 5-yr-old collection gets
  you a "paid" flag (scoring benefit in newer models, minor) but cannot extend the
  7-yr fall-off.
- On debts past SOL: paying is optional; a "time-barred debt" collector suit is
  winnable by asserting SOL — but never ignore a court summons.

## Mortgage-specific sequencing (3–12 months out)

1. 12 mo out: no new credit, no late, dispute junk now (cycles take 30–45 d)
2. 6 mo out: settle/PFD remaining collections; rescore check
3. 2 cycles out: begin AZEO — pay-down before STATEMENT dates
4. 1 cycle out: one card reports <$30, all others $0; pull your own FICO mortgage scores
   (myFICO or lender soft pull) — the mortgage tri-merge uses older FICO 2/4/5 models,
   which are HARSHER on util and inquiries than FICO 8/9/10 you see in apps.
5. During shopping: all mortgage pulls in a 14–45 day window count as one.

## Thin-file build path (fastest legal route)

1. Secured card (deposit = limit, no credit check at some issuers) OR student/starter card
2. Become authorized user on a family member's oldest, cleanest card (age + util inherit)
3. 6 months: first FICO generates (need 1 tradeline 6 mo old for a score at all)
4. 12 months: add a second card; keep both <9% statement reporting
5. Optional: credit-builder loan (Self, local CU) for installment mix — small score,
   real savings habit

## What NOT to do (fraud/gray zone — refuse)

- CPN/SCN "new credit file" numbers (felony, 18 U.S.C. §1029 territory)
- EIN-for-personal-credit swaps
- Disputing accurate items as "identity theft" (FCRA §813 perjury + §1519)
- Buying authorized-user tradelines from strangers (FICO 8 AI emulation filters some;
   mortgage lenders manually underwrite and may flag)
