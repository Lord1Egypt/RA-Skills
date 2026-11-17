# Credit Score Repair Planner

FICO repair without the $99/month mystery. Decomposes a real credit profile into the five
FICO factors, tells you exactly which one is dragging YOUR score, plans statement-date
AZEO utilization timing with pay-by dates, builds a derogatory age-off timeline, and drafts
the actual dispute/goodwill/validation letters with FCRA/FDCPA citations.

## The real-world problem

- 79 million Americans have subprime or thin credit files; "credit repair" companies charge
  $60–150/month for form letters you can generate yourself.
- The biggest fast score lever — **statement-date utilization** — is invisible to most
  people: they pay by the *due date*, but bureaus snapshot the *statement* balance weeks
  earlier. One timing mistake caps the whole pay-down effort.
- A 612 → 680 move changes a 30-yr mortgage rate by ~0.5–1% = **$30k–$80k** over the loan.

## What it does

`scripts/credit_plan.py` takes a JSON profile (cards + limits/balances/statement days,
derogatory items with first-delinquency dates, inquiries, goal) and outputs:

1. **Factor drag analysis** — severity-ranked: which FICO bucket hurts this profile, with
   the fix and realistic point-range swing
2. **AZEO utilization plan** — picks the reporter card, computes exact PAY-BY dates
   (statement close − 3 business days), projects before/after aggregate + per-card bands
3. **Age-off timeline** — 7-yr (lates/collections/charge-offs) and 10-yr (Ch.7) removal
   dates from first delinquency; reporting clock never resets on payment
4. **Letter queue** — drafts goodwill (accurate lates), FDCPA validation (collections),
   FCRA 623 direct disputes (furnishers), ready to mail Certified
5. **Mortgage mode** — 12-month sequencing, FICO 2/4/5 warning (mortgage pulls are harsher
   than app scores), inquiry de-dupe window rules

## Quick start

```bash
python3 scripts/credit_plan.py examples/thin-file-util.json --letters-out ./letters
```

Example output (real run):

```
=== UTILIZATION / AZEO PLAN ===
  current aggregate util: 65.6% (heavy drag) -> after plan: 0.32% (excellent)
  Card A  statement 2026-11-03 | PAY BY 2026-10-31: let ~$30 report (0.6%) — AZEO reporter
  Card B  statement 2026-11-12 | PAY BY 2026-11-09: pay to $0 BEFORE statement close
```

## Guardrails built in

- Never disputes accurate info as inaccurate (FCRA §813 perjury warning in every run)
- SOL vs reporting clock distinction — paying old debt can revive lawsuit rights in some
  states; the tool tells you which clock is which
- Refuses the fraud toolkit: CPN/EIN new-file schemes, purchased tradelines — flagged red

## Reference

`references/fico-mechanics.md` — full factor weights, reporting mechanics per issuer,
derogatory tables, the 6-rung letter ladder, state SOL notes, thin-file build path.

## License

MIT © Denis Voronin
