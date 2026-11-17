# Freelance Debt Collector

Professional, escalating late-payment workflow for freelancers and
small studios: aging report, 7-step reminder ladder with dated cadence
and late-fee math, small-claims readiness, demand letters, and the
stop-work notice.

## The Real Problem

Freelancers lose on average ~$6,000/year to late or missing payments.
The failure mode isn't the client — it's the chase: reminders sent
late, worded either apologetically or as an explosion, then abandoned
right where escalation should begin. Collections done professionally is
a predictable sequence with dates, escalating formality, compounding
fees, and a court-readable paper trail. Sequences beat moods: they get
paid more and preserve the relationship more often.

## What It Does

- **status** — aging buckets, total exposure, >60d at-risk line
- **ladders** — per-invoice ladder step + tone, accrued late fees
  (simple/compound), total with fees, DATED next step
- **smallclaims** — claim vs caps for all 50 US states (+UK/DE/ON),
  net recovery after filing fee, 6-item evidence checklist, formal
  demand letter
- **stopwork** — suspension notice that pauses without cancelling,
  resume condition stated
- **references/** — psychology typology, per-step scripts, contract
  clauses that make collection mechanical, agency economics, write-off
  notes, terms-by-payment-history table

## Quick Start

```bash
python3 scripts/late_invoice_nudge.py --invoices "$INV" --today 2026-10-17 status
python3 scripts/late_invoice_nudge.py --invoices "$INV" ladders
python3 scripts/late_invoice_nudge.py --invoices "$INV" smallclaims --jurisdiction TX --fee 46
python3 scripts/late_invoice_nudge.py --invoices "$INV" stopwork
```

Invoices JSON: `[{"client","no","due","amount"}]`. Stdlib only, offline.

## License

MIT © Denis Voronin
