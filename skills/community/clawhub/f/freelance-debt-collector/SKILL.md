---
name: freelance-debt-collector
description: Use when freelance/small-studio invoices are unpaid past due — aging-bucket report, the escalating 7-step reminder ladder (pre-due courtesy → firm reminders → final demand) with dated next-step scheduling and late-fee math (simple or monthly-compound), small-claims readiness vs local caps (all 50 US states + UK/EU reference) with evidence checklist, filing-fee-vs-recovery math and a formal demand letter, plus the stop-work suspension notice that protects active projects.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [freelance, invoicing, late-payment, collections, small-claims, accounts-receivable, cashflow]
---

# Freelance Debt Collector

Freelancers lose ~$6,000/year on average to slow or missing payments, and
the reason is rarely the client's bank account — it's that chasing money
feels awkward, so reminders happen late, sound either apologetic or
radioactive, and stop entirely at exactly the moment escalation should
start. Professional collections is a sequence, not a mood: predictable
dates, escalating formality, fees that compound, and a paper trail a
court can read. This skill runs that sequence.

## When to Use

- An invoice is unpaid at due date (or about to be) — start the ladder
  at step 0, not step 4
- Several invoices outstanding across clients: aging report to see
  where the real risk is concentrated
- 30+ days late: is small claims realistic? (amount vs local cap,
  filing fee vs recovery, evidence completeness)
- Client keeps promising "Friday": acknowledgment documentation and
  the decision point at day 45
- Active project for a client who owes on earlier phases: stop-work
  notice that pauses without cancelling

**Don't use for:** clients in bankruptcy (stop — automatic stay applies;
file a proof of claim instead); suspected fraud (different playbook);
wage claims (labor board, not small claims); amounts large enough to
need a real collections attorney.

## The Method

1. **`status`** — aging buckets (current / 1-30 / 31-60 / 61-90 / 90+),
   total exposure, >60-day at-risk line. Run weekly; that's the whole
   monitoring cost.
2. **`ladders`** — per invoice: current ladder step + tone, accrued late
   fees (simple or compound, from day 8), total with fees, and the
   DATED next step. The dates matter: an escalation that arrives on a
   predictable cadence reads as process; random escalations read as
   anger.
3. **`smallclaims`** — claim amount (+fees) vs jurisdiction cap for all
   50 US states (+UK/DE/ON reference), net recovery after filing fee,
   the 6-item evidence checklist, and the formal demand letter.
4. **`stopwork`** — the suspension notice: pause, don't cancel; resume
   condition stated; licensing of delivered work tied to payment terms.

```bash
INV='[{"client":"Acme Corp","no":"INV-1042","due":"2026-08-01","amount":4200},
{"client":"Beta LLC","no":"INV-1051","due":"2026-09-15","amount":1850}]'

python3 scripts/late_invoice_nudge.py --invoices "$INV" --today 2026-10-17 status
python3 scripts/late_invoice_nudge.py --invoices "$INV" --today 2026-10-17 ladders
python3 scripts/late_invoice_nudge.py --invoices "$INV" --today 2026-10-17 \
    smallclaims --jurisdiction TX --fee 46
python3 scripts/late_invoice_nudge.py --invoices "$INV" stopwork
```

## The Ladder (what the steps mean)

| Days | Step | Tone rule |
|---|---|---|
| -3 | pre-due courtesy reminder | friendly; assumes goodwill ("in case it slipped") |
| +1 | reminder #1 | friendly-firm; states amount + due date passed |
| +7 | reminder #2 + late-fee notice | firm; fees start accruing, says so |
| +14 | reminder #3 | firm; "final notice" framing appears |
| +30 | formal demand letter | formal; 10-business-day deadline; legal remedies named |
| +45 | decision point | collections agency / small claims / write-off — decide, don't drift |
| +60 | escalate | file or sell the debt; the letter trail is your exhibit |

The two fatal behaviors this cadence prevents: skipping steps (client
escalates the relationship conflict because you exploded at day 40) and
stalling at reminder #3 forever (the invoice ages out of collectability
— most small-claims judges respect a diligent trail, and debt buyers
pay pennies for stale paper).

## Late-Fee Math

Default 10%/yr monthly-compound from day 8 (configurable `--rate`,
`--mode simple|compound`). Two rules that keep fees enforceable:

1. Fees must be in the contract (or statutory — e.g., UK Late Payment
   of Commercial Debts Act: 8% + fixed sums £40-100).
2. Invoices and letters must SHOW the fee accrual — retroactive fee
   bombs at day 60 read as bad faith and get struck.

## Common Pitfalls

1. **Waiting to start.** The ladder starts 3 days BEFORE due. Early
   professional contact is the strongest single predictor of on-time
   payment.
2. **Apologizing or threatening.** Neither. The drafts are deliberately
   neutral-process: dates, amounts, next step.
3. **No log of sent reminders.** The trail IS the small-claims case
   (and the deterrent). Log date/step/channel for every send.
4. **Continuing work on a late account.** Every hour after due date is
   unsecured credit you're extending. Use `stopwork` at ~2 weeks late.
5. **Skipping the demand letter.** Many jurisdictions require a formal
   demand before filing; it also converts "dispute" into "acknowledged
   debt" when they reply.
6. **Small claims for the wrong amounts.** Over cap → civil court
   (lawyer economics change); under ~2× filing fee → collection
   letters only. The `smallclaims` command shows net recovery so this
   is a number, not a vibe.
7. **Shutting up after payment.** Send the receipt + thanks, and note
   the client's payment behavior for next engagement's terms (deposit
   %, shorter net).

## Verification Checklist

- [ ] Every open invoice has: current step, last-send date, next-send date
- [ ] Late fees shown in writing before being charged
- [ ] Stop-work decision made consciously at 14d (either paused or
      explicitly extended)
- [ ] Day-45 decision recorded: collections / court / write-off
- [ ] Evidence checklist complete BEFORE filing (contract, invoice,
      delivery proof, acceptance, reminder trail, acknowledgment)
- [ ] Payment terms for future work adjusted per client payment history

## References

- `references/collections-playbook.md` — psychology and scripts per
  step, contract clauses that make collection mechanical (fees, venue,
  suspension, kill-fee), collections-agency economics, write-off/tax
  notes, and preventing recurrence via terms.
