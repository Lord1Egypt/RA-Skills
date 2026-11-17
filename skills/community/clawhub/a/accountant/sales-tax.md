# Sales Tax, VAT, And GST — Money You Collect For Someone Else

Transaction tax is never the entity's income and never its expense. It is a liability from the moment it is charged, and the liability survives every mistake made handling it.

**Before any transaction-tax work**, read `## Registrations` in `~/Clawic/data/accountant/memory.md` (where registered, at what frequency, since when) and `filings/<year>.md` if `## Boxes` points there. Filing the wrong frequency, or filing in a jurisdiction that was deregistered, both create assessments.

## The Two Systems

| | Sales tax (US) | VAT / GST (most of the world) |
|---|---|---|
| Charged at | The final retail sale only | Every stage of the chain |
| Business purchases | Exempt with a resale or exemption certificate | Taxed, then reclaimed as input tax |
| What you remit | Everything collected | Output tax − input tax |
| Registration trigger | Nexus in the state | Turnover threshold, or immediately for some activities |
| Input tax on costs | Not recoverable — it is part of the cost | Recoverable when the supply is taxable and the invoice is valid |
| Filing | Per state, often monthly or quarterly | Per country, monthly or quarterly, with annual reconciliations in some regimes |

This single difference changes the bookkeeping completely: under sales tax, tax paid on purchases is capitalized into the cost; under VAT, it is a receivable.

## The Entries

```
Sale with tax collected:
Dr Accounts receivable / cash      gross
  Cr Revenue                                    net
  Cr Sales tax or VAT payable                   tax

Purchase with recoverable input tax (VAT regimes):
Dr Expense or asset                net
Dr VAT receivable                  input tax
  Cr Accounts payable / cash                    gross

Filing the return:
Dr VAT / sales tax payable         tax due
  Cr VAT receivable                             input tax reclaimed (VAT regimes)
  Cr Bank                                       net payment
```

- **Never credit revenue with the gross.** It inflates turnover — which is what registration thresholds, covenants, and valuation multiples read — and hides money owed to an authority (SKILL.md, Traps).
- The liability account balance must equal returns filed and unpaid plus tax collected since the last return, at every close (SKILL.md ties).
- Where a platform collects and remits on your behalf, the tax never becomes your liability, but the **gross revenue still does**. Booking only the net payout as revenue understates turnover against thresholds (`reconciliation.md`).

## Where You Owe: Nexus And Thresholds

- **US economic nexus**, post-*Wayfair* (2018): selling into a state creates an obligation once its threshold is crossed, with no physical presence needed. A common threshold is 100,000 of sales into the state in the current or prior year; several states also or instead use a transaction count, and a number of states have dropped the transaction test since. Thresholds and measurement periods differ per state — check each one, and never generalize from the state you know.
- **Physical nexus** still exists and is easier to trigger than expected: an employee or contractor working in the state, inventory held in a fulfilment warehouse there, trade show attendance in some states.
- **Marketplace facilitator laws** shift the collection duty to the platform for sales made through it — but your direct sales into the same state still count toward your own threshold in most states.
- **VAT/GST**: registration is usually a turnover threshold measured on a rolling basis, with immediate registration for certain activities and for non-established businesses. Cross-border digital services are typically taxed where the customer is, with simplified single-registration schemes in several regions.
- **Crossing a threshold creates the obligation from the crossing date**, not from when it is noticed. Back tax, interest, and penalties run from then, and voluntary disclosure programs usually offer a shorter lookback than an assessment would — which is why this is an escalation the moment it is suspected (SKILL.md, Escalate).
- Track the running total per jurisdiction against its threshold as a `## Due` review, quarterly. Discovering a crossing at year-end costs a year of exposure.

## Rates, Exemptions, And Certificates

- **The rate depends on the destination in most US states** and on the customer's location for cross-border digital supplies — plus local district rates stacked on the state rate. A single "sales tax rate" for a multi-state seller is always wrong somewhere.
- **What is taxable varies by product and by jurisdiction**: food, clothing, digital goods, software as a service, and professional services are treated inconsistently across states and countries. Classify the product once per jurisdiction and record it (`## Coding Rules`).
- **Exemption and resale certificates**: collect the certificate **before** the exempt sale, keep it, and re-verify on the jurisdiction's schedule. Under audit, an exempt sale without a valid certificate becomes a taxable sale and the tax is assessed on the seller, who can rarely recover it from the customer years later. Missing certificates are the single largest finding in most sales tax audits.
- **Reverse charge and zero-rating** in VAT regimes shift the accounting to the buyer or remove the tax; both require specific invoice wording and the counterparty's registration number, verified rather than assumed. An invalid number invalidates the treatment.
- **Import VAT and duty** are separate from the supplier invoice, arrive from the carrier or customs, and are recoverable on different terms. Duty is never recoverable and belongs in the cost of inventory (`inventory.md`).

## Filing And Paying

- Frequency is assigned by the authority based on volume and gets **reassessed**, often annually. A changed frequency arrives by notice and is missed constantly; record the current one and its effective date in `## Registrations`.
- **File nil returns.** A skipped return is a missed filing with its own penalty, whatever the amount due.
- Several US states offer a small **vendor discount** for filing on time; it is other income, not a reduction of the tax.
- Reconcile the return to the ledger before filing: taxable sales per the return should agree to revenue in the same span, adjusted for exempt and out-of-jurisdiction sales. A return that does not tie to the books is the one that triggers an audit.
- File the confirmation reference in `filings/<year>.md` in the same turn.
- **Deregistration is an action, not a lapse**: closing a location or stopping sales into a jurisdiction requires a final return and a formal deregistration, or the filing obligation continues and penalties accrue for returns nobody knew were due.

## Corrections

- An error found before filing: fix the entry, in the period it belongs to if still open.
- An error found after filing: most authorities want an **amended return** for the affected period; some allow correcting within a threshold on the next return. Both exist, and using the wrong one creates a mismatch that surfaces later. It is a jurisdiction rule, so check rather than assume.
- **Tax undercharged to a customer** is still owed by the seller. Whether it can be billed back is a contract question, and the answer is usually no once time has passed.
- **Tax overcharged** must be refunded to the customer or remitted; keeping it is not an option in any regime.

**Write when this file produced something durable**: a registration, a deregistration, or a frequency change → `## Registrations`, with the new dates in `## Due`. Each return filed, including nil → `filings/<year>.md`. A product's taxability classification per jurisdiction → `## Coding Rules`. A threshold approaching or crossed → `## Open Items` and an escalation. Certificate collection and re-verification → a `## Due` row (`memory-template.md`).
