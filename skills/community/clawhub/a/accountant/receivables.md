# Receivables — Money Owed To You

Receivables are the asset most likely to be worth less than the balance sheet says. The work is knowing which ones will convert, and booking the rest honestly.

**Before answering any receivables question**, read `## Open Items` in `~/Clawic/data/accountant/memory.md` — a customer already in dispute is not an aging problem — and the aging total against the AR control account (`reconciliation.md`). An aging that does not tie to the ledger cannot be acted on.

## The Aging

Buckets by **due date**, never by invoice date: an invoice on 60-day terms issued 45 days ago is current, and bucketing by issue date makes it look overdue.

| Bucket | What it means | Default action |
|---|---|---|
| Current | Within terms | Nothing |
| 1-30 overdue | Usually administrative — wrong contact, missing PO, invoice never received | Confirm receipt and the payment date; resend with the PO reference |
| 31-60 | The customer has decided not to pay yet | Named person, a date, and the consequence stated |
| 61-90 | A dispute nobody has raised, or a cash problem | Stop extending credit; find out which one it is before escalating |
| 90+ | Recovery rate falls steeply; the invoice is now a collections matter | Payment plan, formal demand, or write-off decision |

Concentration matters more than the total: one customer at 40% of receivables is a different risk from forty customers at 1%, at the same balance. Report both.

## Metrics That Change Behavior

- **DSO** = (average receivables ÷ credit sales for the period) × days in period. Compare against **stated terms**, not against an ideal: DSO of 47 on 30-day terms means 17 days of collection slippage, and against 45-day terms it means the process works.
- **Best possible DSO** = (current receivables ÷ credit sales) × days. The gap between actual and best possible is the part collections can fix; the rest is terms.
- **Collection effectiveness** = (opening receivables + credit sales − closing receivables) ÷ (opening receivables + credit sales − closing current receivables). It isolates whether the overdue portion is moving, which DSO alone hides when sales grow.
- Every 30 days of DSO on annual revenue R ties up roughly R ÷ 12 in working capital. On 1.2M of revenue, cutting DSO from 60 to 45 releases about 50,000 of cash — one-off, but real.

## Allowance For Doubtful Accounts

Two acceptable methods, and one that is not.

- **Aging method** (default): apply a loss rate to each bucket. Derive the rates from **this entity's own write-off history over three years**, not from a textbook table — a business selling to governments and one selling to consumers have loss curves that differ by an order of magnitude. With no history, start from the observed 90+ write-off proportion and revisit at each year-end.
- **Specific identification**: name the invoices at risk and provide for those. Correct when receivables are few and large; unworkable with hundreds of small balances.
- **A flat percentage of revenue** is not a method. It provides against sales that were collected and ignores the aging that actually predicts loss.

Entries:

```
Provision:   Dr Bad debt expense            / Cr Allowance for doubtful accounts
Write-off:   Dr Allowance                   / Cr Accounts receivable
Recovery:    Dr Accounts receivable         / Cr Allowance      (reinstate)
             Dr Cash                        / Cr Accounts receivable
```

- Writing off **directly to expense** without an allowance is the direct write-off method: simple, permitted for tax in many regimes, and it misstates the period, because the loss lands whenever someone gives up rather than when the sale was made.
- Never delete the original invoice. Deleting removes the revenue from a period that has been reported and probably filed (SKILL.md Rule 7).
- **Tax treatment differs from book treatment.** Many regimes deduct a bad debt only when it is actually written off, not when provided for — so the allowance is usually a book-tax difference (`tax.md`).

## Collections

Escalation by stage, with the entry at each point:

1. **Before it is late**: confirm the invoice was received and matches a purchase order. Most 30-day slippage is a routing failure, not a decision.
2. **Overdue, first contact**: state the invoice number, the amount, the due date, and ask for a payment date. Ask a person, not an inbox.
3. **Overdue 45+**: put the consequence in writing — work stops, service is suspended, statutory interest starts. A consequence that is stated and then not applied removes every future consequence.
4. **Payment plan**: acceptable, in writing, with the balance staying on the books at full value unless the plan itself concedes an amount. A concession is a credit note, dated when agreed.
5. **Formal demand or collections agency**: the receivable stays on the books; the agency's fee is an expense when incurred. Selling the debt derecognizes the receivable at the proceeds and books the difference as a loss.
6. **Statute of limitations**: in every jurisdiction there is a deadline after which a debt cannot be enforced. It is a legal question, not an accounting one — check before writing off a large balance on age alone.

Statutory late-payment interest exists in many jurisdictions and can be charged without a contract clause. Charging it is a commercial decision; booking it is not — recognize it only when collection is probable, because interest accrued on a debt that is not paying inflates both revenue and the receivable.

## Customer Deposits And Credits

- A deposit received is a **liability**, not revenue and not a negative receivable: Dr cash / Cr customer deposits, released when the obligation is met (`revenue.md`).
- Credit notes reduce revenue in the period they are issued unless they correct an error in a closed period, in which case cutoff rules apply (`close.md`).
- A customer that is also a supplier is **not** netted on the balance sheet without a legal right of set-off. Netting hides both balances and misstates working capital.
- Unapplied cash — money received that matches no invoice — sits in a suspense or unapplied-receipts account, never as a negative invoice. It appears in `## Open Items` until identified.

## Credit Control Before The Sale

The cheapest receivables work happens before the invoice exists.

- Terms in writing, on the quote and the invoice, with the due date as a **date** rather than "net 30" — the ambiguity of when the clock starts is the most common excuse.
- Deposit or milestone billing for anything long or large; the deposit is the credit check that actually works.
- A credit limit per customer, checked at order rather than at collection, and lowered the first time a bucket slips past 60.
- New customers on shorter terms until two invoices have been paid on time.
- Invoice on the day the obligation is met. Every day of delay in issuing is a day added to DSO that no collections effort can recover (`invoice` handles the issuing mechanics).

**Write when this file produced something durable**: an allowance rate, its derivation, or a change to it → `artifacts/policy-doubtful-accounts.md` with its `## Boxes` line. A write-off, a payment plan, or a dispute → `## Open Items` until resolved, and the entry in the ledger. A customer's agreed terms or credit limit → `## Coding Rules`. A named person at the customer who handles payment → `~/Clawic/data/contacts/contacts.md` (`memory-template.md`).
