# Payables — Money You Owe

Payables is where cash is quietly won or lost: through discounts nobody computes, duplicates nobody catches, and costs that never reach the period they belong to.

**Before answering any payables question**, read the AP aging total against the AP control account and `~/Clawic/data/finances/subscriptions.md` — a recurring charge that stopped appearing is a missing bill, not a saving. Read `## Open Items` for anything already disputed.

## The Three-Way Match

Before a bill is approved for payment, three documents must agree:

| Document | Says | Mismatch means |
|---|---|---|
| Purchase order | What was ordered, at what price | Price rise never agreed, or an order nobody placed |
| Goods received note / acceptance | What actually arrived, when | Short delivery, or a service billed before performance |
| Supplier invoice | What is being charged | Quantity, price, tax, or a duplicate |

In a small entity the "PO" is often an email and the "GRN" is a person confirming. The discipline still holds: **someone other than the person who pays confirms the thing arrived**. That single separation is the most valuable control a three-person company can implement (`audit.md`).

Tolerances make it workable: accept price differences under a stated amount and quantity differences under a stated percentage without re-approval, and write both into the policy. Zero tolerance means every rounding difference blocks a payment and the control gets bypassed within a month.

## Accruing What Has Not Been Billed

The bill's arrival date is irrelevant to the period (SKILL.md Rule 1). At close:

- Goods received, not invoiced → Dr the expense or inventory / Cr accrued liabilities (**not** accounts payable — AP holds documented invoices, and mixing them breaks the subledger tie).
- Services delivered, not invoiced → same, estimated from the contract rate or last invoice, with the basis in the memo.
- Recurring vendors that did not bill this period → check `subscriptions.md`; silence usually means a lost invoice.
- Follow the account's accrual discipline from `## Coding Rules`, and never mix disciplines on one account (SKILL.md, Adjusting Entries).

## Early-Payment Discounts

The most consistently ignored return in small-business finance. Formula:

```
Annualized rate = discount% ÷ (100% − discount%) × 365 ÷ (full term days − discount days)
```

| Terms | Calculation | Annualized |
|---|---|---|
| 2/10 net 30 | 2 ÷ 98 × 365 ÷ 20 | ~37.2% |
| 1/10 net 30 | 1 ÷ 99 × 365 ÷ 20 | ~18.4% |
| 2/10 net 60 | 2 ÷ 98 × 365 ÷ 50 | ~14.9% |
| 1/15 net 45 | 1 ÷ 99 × 365 ÷ 30 | ~12.3% |

Decision rule: take the discount whenever the annualized rate exceeds the cost of the money used to pay early — the credit facility rate, or the return on the cash if there is no borrowing. At 2/10 net 30 that is true for nearly every business. Record discounts taken as a reduction of the expense or of inventory cost, not as other income: the purchase genuinely cost less.

The mirror also holds: offering 2/10 net 30 to customers costs you ~37% annualized. It is an expensive way to accelerate collections, and cheaper than a bad debt (`receivables.md`).

## Duplicate And Fraudulent Payments

The four patterns that account for most duplicates:

1. Same invoice entered from the PDF and from the supplier statement.
2. Invoice number entered with and without a prefix, so the software's duplicate check misses it.
3. A credit note applied as a payment, leaving the original still open.
4. A paid invoice re-imported by a feed and paid again in a later run.

Controls that catch them: unique invoice number per supplier enforced at entry, a same-amount/same-supplier/±10-days scan before each payment run, and reconciliation of every supplier statement quarterly. Duplicates found after payment become a receivable from the supplier, not a reduction of expense in the current period — otherwise the original period keeps the overstated cost.

**Bank detail changes are the highest-risk event in payables.** A supplier's account number changing by email is the standard invoice-fraud pattern. Verify on a phone number obtained before the change, from a record that predates the request, and record what was verified and how (`~/Clawic/data/contacts/contacts.md`). Never verify using a number on the changed document. The document-side controls live in `invoices`.

## Paying, And When

- **DPO** = (average payables ÷ purchases) × days in period. Rising DPO is either deliberate negotiation or the first visible symptom of a cash problem; the two look identical in the ratio and completely different in the aging detail.
- Pay to terms, not early and not late by default: paying early donates the discount rate above; paying late costs relationships, priority, and sometimes statutory interest.
- Batch payment runs on a fixed weekday. Ad hoc payments are where duplicates and unapproved invoices enter.
- **Never pay from a statement.** Statements aggregate, omit credits, and repeat items already paid; pay from invoices matched to receipts.
- Personal cards and owner payments for business costs are a due-to-owner liability or a contribution, reimbursed on a schedule, never invisible (`owner-pay.md`).

## Supplier Credits, Disputes, And Vendor Records

- A credit note is applied against the specific invoice, not netted against the next payment. Netting makes both the aging and the supplier's statement untieable.
- A disputed invoice stays in payables at full value, flagged, with the disputed amount named in `## Open Items`. Removing it makes the liability disappear from the balance sheet while the obligation continues.
- A supplier deposit or prepayment is an **asset** (prepaid or supplier advance), released when delivered.
- Retentions held back on construction and similar contracts stay as a liability until release, and their release date is a `## Due` row — retentions are forgotten more often than any other balance.
- What each supplier is, its terms, and how it bills belongs with the invoice archive (`invoices`); here, only the coding rule and any standing commitment (`~/Clawic/data/finances/subscriptions.md`) are recorded.

## Contractors And Withholding

Payments to individuals and unincorporated businesses often carry reporting or withholding duties, and the deadline is annual with a penalty per form. Collect the tax identification document **before the first payment** — chasing it in January, after the work is done and the leverage is gone, is the standard failure. Which payments are reportable, at what threshold, and by when: `payroll.md` and `tax.md`.

**Write when this file produced something durable**: an accrual that will repeat → `recurring-entries.md`. A recurring vendor commitment → `~/Clawic/data/finances/subscriptions.md`. Agreed terms, a discount policy, or a coding rule for a supplier → `## Coding Rules`. A duplicate found, a dispute, or a verified bank-detail change → `## Open Items`, with the verification detail on the person's row in `~/Clawic/data/contacts/contacts.md`. A payment-approval policy worth repeating → `artifacts/` with its `## Boxes` line (`memory-template.md`).
