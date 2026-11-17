# Receipts — Evidence That Still Works in Three Years

Receipt files live in `~/Clawic/data/expenses/receipts/`; the ledger row holds the filename and nothing else points at them. **Before answering any question about whether a receipt is needed or still needed**, read `config.yaml` for `receipt_threshold` and `tax_year_start`, and `platform.jurisdiction` — every rule below is jurisdiction-shaped and the defaults are US-flavoured.

**Contents:** [What a Receipt Has To Contain](#what-a-receipt-has-to-contain) · [When a Receipt Is Actually Required](#when-a-receipt-is-actually-required) · [Capture](#capture) · [Naming and Storage](#naming-and-storage) · [The Missing Receipt](#the-missing-receipt) · [Retention](#retention) · [Foreign and Digital Receipts](#foreign-and-digital-receipts)

## What a Receipt Has To Contain

A card slip proves that money left an account. It does not prove what was bought, and in a VAT/GST country it does not support an input-tax claim at all. The two documents are different and users conflate them constantly.

| Document | Proves | Enough for |
|---|---|---|
| Card slip / bank line | Payment happened, amount, date | Personal tracking; reconciliation |
| Simple receipt | What was bought, from whom, when | Most employer reimbursement |
| Tax invoice | The above **plus** the supplier's tax registration number, the tax amount broken out, and (above the local simplified-invoice ceiling) the buyer's name and tax number | Input VAT/GST recovery, business deduction in most jurisdictions |

If the business needs to recover input tax, the moment to ask for a proper tax invoice is at the counter. Retroactive reissue is possible almost everywhere and painful everywhere; a month later the merchant no longer cares.

## When a Receipt Is Actually Required

Defaults, all of which need confirming against the user's jurisdiction and their employer's policy:

- **`receipt_threshold` (default 75)** — the US rule for travel, entertainment, gift and vehicle expenses requires documentary evidence at or above $75, with **lodging always requiring a receipt regardless of amount** (Treas. Reg. §1.274-5(c)(2)(iii)). The default in this skill comes from there; it is not a universal number.
- **Employer policies are usually stricter than the tax rule** and frequently demand a receipt for everything. The policy, not the regulation, governs a claim (`reimbursement.md`).
- **Per diem removes the requirement** for the items the per diem covers — that is the entire point of a per diem. Logging those receipts is wasted work.
- **VAT/GST recovery has no de minimis in the sense people assume**: many jurisdictions allow a *simplified* invoice below a threshold, which still must carry the supplier's tax number. A plain card slip fails at any amount.
- Below the threshold, the ledger row **is** the record — which is why the purpose field matters more than the paper (SKILL.md Rule 8).

## Capture

- **Photograph on the day.** Thermal paper fades to blank, sometimes within months and faster in a hot car or a wallet. A faded receipt is not a receipt.
- Frame the **whole** document: merchant name, date, line items, total, and the tax line. A crop that loses the tax line loses the deduction.
- One receipt per file. A photo of four receipts fanned out is unsearchable and half of it is out of focus.
- Email receipts: save the PDF, not a screenshot of the inbox. The PDF carries the sender and the date.
- The card slip stapled to the receipt is redundant — the statement already holds that fact.

## Naming and Storage

`<YYYY-MM-DD>-<vendor>-<amount><CCY>.<ext>` — `2026-07-06-ichiran-8400JPY.jpg`. Lowercase, kebab vendor, no spaces.

That shape sorts chronologically, is greppable by vendor and by amount, and survives being dumped into an accountant's folder without a covering note. A second receipt from the same vendor on the same day gets `-2`.

Never rename a stored receipt to match a corrected ledger row — add the correction to the row instead. The filename is a pointer, and pointers that change break silently.

## The Missing Receipt

Lost receipts are normal; undocumented lost receipts are what fails a review. The substitute is a **contemporaneous note**, written now and not at audit time, in the ledger row's purpose field or as a short `artifacts/` note if the amount justifies it:

```
date · vendor · amount with currency · business purpose · who was present (for meals)
· why there is no receipt · the statement line that corroborates it
```

Two things make this work: it was written close to the event, and it is corroborated by a payment record. Neither is true of a note written the week before a filing deadline. A pattern of missing receipts on one category is itself the finding — fix the capture habit rather than perfecting the notes.

## Retention

The clock starts at the filing date of the return the expense belongs to, and `tax_year_start` decides which year that is. Confirm each of these against the current rules for the user's jurisdiction before relying on them:

| Jurisdiction | Common rule |
|---|---|
| US (individual and business) | 3 years from filing generally; **6 years** where income is understated by more than 25%; indefinite where no return was filed |
| UK self-employed | At least 5 years after the 31 January submission deadline of the relevant tax year |
| UK company | 6 years from the end of the accounting period |
| EU VAT | Commonly 5-10 years depending on the member state; property-related records run longer |
| Employer claims | Until reimbursed plus the employer's own audit window, commonly one to two years |

Practical policy: keep everything business or reimbursable for the longest applicable window; personal receipts below `receipt_threshold` can go once the month is reconciled and closed, because the ledger row plus the statement is already a complete personal record.

Purge on a schedule, never ad hoc — a `## Due` row (`Receipt retention purge`, yearly). Deleting by hand when the folder feels large is how the one receipt that mattered leaves.

## Foreign and Digital Receipts

- Keep the **original** document. A translated summary is an annotation, never a replacement.
- Note only what is not machine-readable: what was bought, if the receipt is in a script the reader will not have.
- Digital copies are accepted in most jurisdictions provided they are complete, legible and unaltered — but "most" is not "all", and a few still require originals for specific categories. Verify before discarding paper for a business.
- A receipt in a foreign currency pairs with a ledger row carrying all three currency fields (`currency.md`); the receipt shows the local amount, the row explains the home amount.
- Screenshots of app-based payments (transit, ride-hailing, food delivery) are receipts when they show merchant, date, amount and tax. Most in-app trip summaries do not show tax — fetch the emailed invoice for anything business.

**Write on the way out.** A captured receipt is saved under `receipts/` with the canonical filename and its filename written into the ledger row in the same turn; a missing-receipt note goes in the row's purpose field, or in `artifacts/` when it is long enough to be read on its own; a retention decision or purge writes its `## Due` row; a jurisdiction rule the user confirms is a declaration and goes to `config.yaml` under `platform`. Formats in `memory-template.md`.
