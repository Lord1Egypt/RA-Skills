---
name: estate-settlement-navigator
description: Use in the first weeks after a death — builds the ordered admin cascade nobody can think straight to do (how many certified death certificates to order, who to notify first and WHY — SSA before banks to stop clawback, credit bureaus to prevent deceased identity theft), survivor-benefit screening (widow(er) age gates 60/50, $255 lump-sum window, children's benefits), a dated settlement timeline through final tax returns, and generates the notification letters banks, insurers and utilities require.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [bereavement, estate, executor, death-admin, survivor-benefits, probate]
---

# Estate Settlement Navigator

The weeks after a death are an administrative gauntlet run on zero sleep:
10–20 organizations each want an **original certified** death certificate,
notify them in the wrong order and you invite clawbacks and deceased-
identity theft, and real money (survivor benefits, life insurance, pension
elections) quietly expires if nobody claims it on time. This skill turns
grief brain into a checklist: the cascade order, the document math, the
benefit windows, and the letters.

## When to Use

- Someone died days or weeks ago and the family is starting the admin
- You are named executor / personal representative and don't know where to start
- Surviving spouse asking "what money am I entitled to?"
- Closing accounts: banks, credit cards, utilities, subscriptions, DMV
- Deciding whether probate / an attorney is actually needed
- Preparing the death certificate order at the funeral home (right now is the cheapest moment to order extra copies)

**Don't use for:** contested wills or litigation (attorney, immediately);
tax advice on large/complex estates (CPA + estate attorney); any
jurisdiction-specific legal question beyond the general maps here.

## The Method

1. **`certificates`** — count the organizations (banks × each account
   holder, insurers, DMV, property, employer) → recommended certified-copy
   count (orgs + spares; originals, not photocopies) with cost estimate.
2. **`cascade --country us|uk`** — the ordered notification list with
   timing and the WHY for each slot: SSA first (stop payments before they
   must be clawed back), credit bureaus early (deceased identity theft is
   real), banks, insurers, employer benefits, utilities last.
3. **`benefits`** — survivor screening from ages: widow(er) gates (60, or
   50 if disabled, or any age caring for child under 16), $255 lump-sum
   death benefit (2-year claim window), child benefits to 18/19, the
   "claim small one early, switch to big one at FRA/70" strategy, pension
   survivor-annuity and employer-plan flags.
4. **`timeline --date YYYY-MM-DD`** — dated milestones: first week, first
   month, months 2–6 (probate, titles, final bills), tax year items
   (final 1040, estate 1041 over $600 income, estate-tax only far above
   the ~$14M exemption).
5. **`letter --type close|claim|transfer`** — generates the notification
   letter an institution needs: deceased's details, certified copy
   enclosed, what you're asking for (close / pay beneficiary / transfer),
   and your executor/next-of-kin authority statement.

Run `python3 scripts/estate_admin.py <cmd> --help` for all flags.

## Judgment Rules

- **Order is money:** Social Security before bank closures (a benefit
  paid for the month of death gets pulled back — from an account you
  already emptied, that's a mess). Bureaus before debt collectors circle.
- **Small-estate bypass:** assets with named beneficiaries, POD/TOD
  designations, and joint tenancy pass OUTSIDE probate. Only the remainder
  counts against the small-estate-affidavit threshold — often no probate
  court needed at all.
- **Non-spouse retirement accounts:** inherited-IRA rules (typically the
  10-year payout under SECURE) — do not merge into your own IRA.
- **Keep one bank account open** (estate or joint) until final bills are
  paid; cancel autopays on the deceased's solo accounts early.
- **UK:** one "Tell Us Once" call covers DWP/HMRC/DVLA; Bereavement
  Support Payment must be claimed within 3 months for full backdating.

## Common Pitfalls

1. Ordering 2 certificates "to start" — every bank wants its own
   original; reorder fees cost more than spares ordered at the funeral
   home.
2. Photocopies — almost every institution rejects them.
3. Not notifying credit bureaus — the deceased's identity gets used for
   loans for years; the file needs the deceased flag/freeze.
4. Missing the COBRA-like windows: employer group life claims, pension
   survivor elections, Bereavement Support Payment (UK, 3 months).
5. Rushing to close the joint household account before final utility
   bills and the funeral invoice clear.
6. Assuming probate is required — beneficiary designations usually
   transfer the majority of a normal estate directly.
7. Filing no final tax return — the deceased owes one for the year of
   death, and the estate another (1041) if it earns over $600.

## Verification Checklist

- [ ] Certified-copy count ordered ≥ organizations + spares
- [ ] SSA notified; month-of-death payment returned, not clawed back
- [ ] All three credit bureaus have the deceased flag
- [ ] Every life-insurance policy claimed (search unknown ones: bank
      autopays, employer HR, old statements, state unclaimed property)
- [ ] Survivor benefits screened (spouse + each child)
- [ ] Small-estate vs probate decision made explicitly
- [ ] Final 1040 + estate 1041 calendar entries created
- [ ] Mail redirected; DMA "deceased, do not contact" submitted

## One-Shot Recipe

Fresh loss, US, surviving spouse 61 with a 14-year-old child:

```bash
python3 scripts/estate_admin.py certificates --orgs 14
python3 scripts/estate_admin.py cascade --country us
python3 scripts/estate_admin.py benefits --spouse-age 61 --kids-under-16 1
python3 scripts/estate_admin.py timeline --date 2026-10-14
python3 scripts/estate_admin.py letter --type close --to "Card Bank" \
    --deceased "John M. Doe (SSN xxx-xx-1234)" --requester "Mary Doe, spouse"
```

References: `references/cascade-and-documents.md` (order, documents,
US/UK maps), `references/benefits-and-taxes.md` (survivor math, probate
bypass, final returns).
