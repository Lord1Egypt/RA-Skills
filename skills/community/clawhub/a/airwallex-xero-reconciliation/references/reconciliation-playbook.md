# Reconciliation playbook

Read this reference when preparing or posting Airwallex-to-Xero entries. Apply it to the organisation's actual base currency, chart of accounts, period, and evidence. Never carry account codes or names from a previous organisation into a new one without checking its chart of accounts.

## Source inventory and cutoff

Collect the Airwallex expense export, wallet Balance Activity or official currency statements, and Xero bank transactions and statement lines. For each candidate, check legal entity, status, wallet posting or settlement date, original/billing amount, actual wallet movement, fees, and unique source ID. Exclude authorisation holds, releases, pending transactions, reversals already netted elsewhere, and out-of-period movements from the posted balance roll-forward. A failed sync in Expenses may be only a failed accounting-data sync; check whether the HKD bank feed already posted the wallet movement.

Build an independent roll-forward for each currency:

`opening wallet balance + deposits + refunds + conversion buys + other credits − purchases − fees − conversion sells − transfers = closing wallet balance`

Match the source closing balance to Airwallex's own statement. Record timing differences separately. Then compare the Xero book balance with Xero's imported statement balance and count of unreconciled lines. Explain both numbers; neither alone proves the account is fully reconciled.

## Posting map

| Source event | Base-currency-only Xero treatment |
| --- | --- |
| Card charge funded by base wallet | Match the actual base-currency deduction already supplied by that wallet's feed; code the expense once. |
| Card charge funded by foreign wallet | Spend from the base-currency tracking account at the documented historical value; code the expense once. |
| Foreign-wallet deposit from director/shareholder | Receive into the tracking account, offset to an appropriate loan liability if repayable. Document currency, interest, and repayment terms when relevant. |
| Deposit or transfer from a customer | Use the related receivable or revenue account, not the director-loan account. |
| Wallet or deposit fee | Spend to the bank-fee account, with the actual wallet currency and historical base-currency value retained in the description/evidence. |
| Card refund | Receive to the tracking account, normally reversing the original expense or charge; compare the original charge and any credit note. |
| USD → HKD conversion | Record both wallet sides. Use the actual Airwallex sold and bought amounts; connect the sides through a clearing account or documented transfer treatment. Clear the intermediary account and explain any FX difference. |
| Closing foreign-wallet balance | Translate the remaining monetary balance at the reporting-date rate and record any revaluation difference in the appropriate FX gain/loss account. Do not post an unexplained plug. |

Rate hierarchy: actual executed Airwallex conversion rate for a conversion; otherwise a documented rate for the transaction date, applied consistently. If the exact date is absent (weekend or an unpublished period), identify the chosen prior published rate and its date. Do not silently reuse a rate from weeks earlier. Recalculate a foreign-currency loan liability separately if it is contractually repayable in that currency.

## Posting and matching controls

- Before posting, check Xero bank transactions and imported statement lines for the same source ID. Also compare date, signed amount, merchant, and wallet to catch older entries without IDs.
- Post only settled, approved, in-scope activity and the necessary funding, fee, conversion, refund, and FX entries. Record source ID in the Xero reference and original currency amount plus rate policy in the description or supporting schedule.
- After posting, re-query Xero and verify count, total, bank account, account codes, tax treatment, and status. A failed bulk request may be partially applied, so inspect before retrying.
- For a statement CSV, use an independent Airwallex source when possible. If a base-currency-equivalent CSV must be created from book entries to support Xero's matching workflow, label it as derived, reconcile it to original Airwallex activity, and preserve the transformation. The derived CSV is not a substitute for the official wallet statement.
- Check CSV column mapping before import. In one reconciliation, a source ID was mistakenly mapped into **Transaction Type** rather than **Reference**; Xero still allowed manual matching by date and amount, but the imported statement's reference field was wrong. Correct this in future imports.
- In Xero, **Reconcile (N)** means N statement lines still need matching, even if statement and book balances are equal. After matching, verify the pending count is zero and that the account displays **Reconciled**. Do not create another expense while reconciling a line that already has a corresponding book transaction.

## Audit handoff and exceptions

Retain original Airwallex statements or balance reports, card invoices/receipts, director deposit evidence, Xero transaction IDs, a source-ID crosswalk, FX-rate source and date, and the final Xero reconciliation report. Record manual-booking exceptions where Airwallex still shows “Sync failed”; an automatic retry may duplicate them. Check the actual year-end date and activity after the last imported statement. An auditor can review the file before every workflow label is cleared, but unresolved differences, unsupported entries, and missing evidence should be disclosed rather than described as complete.
