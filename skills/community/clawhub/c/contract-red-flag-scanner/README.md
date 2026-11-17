# Contract Red Flag Scanner

**First-pass triage for contracts you're about to sign — before you need a lawyer.**

You're about to sign a lease, a job offer, or a gym contract. It's 14 pages of
legalese. Studies estimate that actually reading all the agreements an average
person encounters would take **76 work-days per year** — so nobody does, and the
fine print wins: auto-renewal traps lock people into extra lease years, rent
acceleration clauses turn a broken lease into a five-figure bill, and
arbitration waivers quietly remove the right to sue.

The Contract Red Flag Scanner is the missing layer between you and the fine
print:

- **20+ high-risk clause detectors** — auto-renewal windows, rent acceleration,
  arbitration/class-action waivers, one-sided late fees, indemnification,
  non-competes, unilateral amendments, and more
- **Contract-type inference** — lease / employment / ToS / subscription, with
  type-specific analysis
- **Risk-ranked report** — HIGH / MEDIUM / LOW with the *exact matched contract
  language*, a plain-English explanation, and the question to ask before signing
- **Missing-clause checklist** — protections that SHOULD be there but aren't
  (a lease with no repair obligation, no deposit-return deadline)
- **Scrutiny score** (0–100) — how adversarial is this document?
- **Copy-paste question list** — for your email to the landlord / HR / vendor

100% offline, pure Python stdlib. Your contract never leaves your machine.

## Quick Start

```bash
# Scan a lease (paste the contract text into a .txt file first)
python3 scripts/contract_scanner.py scan references/sample-lease.txt

# JSON for pipelines / agent use
python3 scripts/contract_scanner.py scan contract.txt --json

# See every detector
python3 scripts/contract_scanner.py list-detectors
```

## Example Output

```
CONTRACT TYPE: lease (confidence 0.86)
SCRUTINY SCORE: 74/100 — 5 HIGH, 6 MEDIUM, 2 LOW findings

[HIGH] AUTO-RENEWAL WITH STRICT NOTICE WINDOW
  Matched: "shall automatically renew for successive twelve (12) month terms
  unless Tenant provides written notice not less than sixty (60) days prior..."
  Plain language: Miss the 60-day window by a day and you're locked in for
  another FULL year.
  Ask: "Can renewal go month-to-month, or notice drop to 30 days?"

MISSING-CLAUSE CHECKLIST (lease):
  [ ] Landlord repair / habitability obligation — NOT FOUND
  ...
```

## What a Finding Looks Like

Every finding quotes the contract's own words, explains the harm in plain
language, and gives you the negotiation question:

| | |
|---|---|
| **Matched** | "all remaining rent for the balance of the term shall become immediately due and payable" |
| **Means** | Break the lease in month 3 of a 2-year term → owe ~21 months of rent at once |
| **Ask** | "Can we cap early-exit exposure at two months' rent?" |

## Why Missing Clauses Matter

Users fixate on what's flagged. But a lease with **no repair obligation**, **no
deposit-return deadline**, and **no entry-notice requirement** leaves you on
default rules the landlord counted on. The scanner checks for the protections a
fair contract of its type should contain and reports the ones that are absent.

## Is This Legal Advice?

No. It's pattern-based triage: it tells you *whether* you need a lawyer and
*exactly what to ask* — a targeted review of two flagged clauses costs a
fraction of a full contract review. False negatives are possible; a clean scan
is not clearance. For HIGH findings or big money, get a licensed attorney.

## License

MIT — see [LICENSE](LICENSE). Sample lease in `references/` is synthetic.
