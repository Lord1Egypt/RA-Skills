---
name: airwallex-xero-reconciliation
description: Reconcile Airwallex multicurrency wallets with Xero, including failed foreign-currency syncs, base-currency bookkeeping, statement matching, owner funding, FX, and audit evidence. Use for Airwallex-to-Xero cleanup or repeatable import workflows; not for unrelated payment providers.
license: MIT-0
---

# Airwallex and Xero reconciliation

Use this skill to produce a traceable ledger and reconciled balances when Airwallex holds several currencies and Xero may support only its base currency. First identify the Xero organisation, base currency, subscription capabilities, Airwallex legal entity, wallet currencies, and the exact period. Do not assume that a card's billing currency identifies the wallet that funded it.

## Decide how each wallet is represented

- An Airwallex wallet currency maps to a separate Xero bank account when Xero supports that currency. A base-currency-only Xero organisation cannot hold a true foreign-currency bank account. Keep the supported base-currency feed connected and use a clearly named base-currency tracking account for an unsynced foreign wallet when needed.
- A foreign-priced card payment funded by automatic conversion from the base-currency wallet belongs to the base-currency feed at its actual deducted amount. A payment funded from the foreign-currency wallet belongs to that wallet's tracking account. Check wallet balance activity before posting either case.
- Treat the Airwallex connection, Xero bank feed, and Expenses/Bills sync as distinct integrations. A failed expense sync does not prove that the related wallet movement is absent from Xero.
- If a feed is faulty, prefer Airwallex **Reconnect** over **Disconnect**; disconnecting can lose history and currency mappings. Do not enable an unsupported foreign-currency feed or retry manually booked expenses without a duplicate check.

## Build the source-to-ledger mapping

Read [references/reconciliation-playbook.md](references/reconciliation-playbook.md) when preparing or posting entries. It covers settled-item selection, FX, deposits, fees, conversions, refunds, and the reconciliation checks.

For every source movement, preserve the Airwallex transaction or balance-history ID, wallet currency, signed wallet amount, posting date, counterpart, and evidence. Map it to one Xero entry or explain an exclusion. Check the same period and legal entity on both sides. Use source IDs and Xero references for idempotency; also inspect existing Xero transactions by date, amount, merchant, and wallet, since older entries may lack the source ID.

For a base-currency-only Xero organisation, value foreign-wallet movements in base currency using the actual Airwallex conversion when there was one. Otherwise apply a consistent, documented historical-rate policy. Never substitute today's rate for a past movement or invent a rate for a missing date. Revalue material foreign-currency monetary balances at the reporting date under the accounting standard applicable to the organisation.

Classify funding by its legal substance: repayable director/shareholder funding is a liability; a documented permanent contribution is equity; customer receipts are income or settlement of a receivable. Do not use a balancing entry to hide missing funding. An account named “Funds Introduced” may be configured as a liability in one Xero chart and equity in another—inspect its actual account type and the agreed repayment terms.

## Reconcile and verify

1. Compare the independent Airwallex statement or balance-activity report with Xero for each wallet and date range. Tie opening balance plus signed movements to the closing balance in the original currency, then tie the base-currency carrying amount after FX adjustments.
2. Separate a **book-versus-statement balance difference** from **unreconciled statement lines**. Equal balances do not mean that every line has been matched. An imported statement and a posted Spend/Receive Money entry are also distinct objects.
3. When importing a CSV statement, verify the mapped Xero fields before completion: Date → Transaction Date, signed Amount → Transaction Amount, Payee → Payee, Description → Description, and source Reference → Reference. Preview positive and negative rows, row count, period, and net amount. A misplaced Reference field can obscure the audit trail or impede matching.
4. Match each statement line to the already posted Xero transaction using date, direction, amount, wallet, and source reference. Use Xero's suggested **Match / OK** only after checking the proposed transaction. Do not choose **Create** when the corresponding book entry already exists. Verify the pending count decreases and ends at zero, and confirm Xero displays the account as reconciled.
5. If Xero's reconciliation rows fail to load, verify what was imported and what was posted through available read-only views. Report the pending count accurately. Retry a bounded number of times or resume after service recovery; do not claim reconciliation merely because balances tie.

For audit handoff, keep the independent Airwallex statements, invoices/receipts, deposit evidence, FX-rate sources, source-ID-to-Xero mapping, and year-end reconciliation. A synthetic statement generated from Xero's own entries can make Xero's workflow match, but it is **not independent proof** of the wallet balance; check it separately against Airwallex. Airwallex may continue to say “Sync failed” after direct Xero posting. Record that exception and prevent a later retry from duplicating the entry.

## API, access, and private data

Use CSV for a small historical backlog or an API connector for recurring volume. Airwallex balance-history access should use a scoped read-only key; Xero access uses OAuth with only the needed granular scopes. API access cannot bypass Xero's multicurrency subscription restrictions.

For a connector, create a local `.env.example` with placeholder variable names and an ignored local `.env` for actual credentials. Ask the user to enter Airwallex client ID/API key and Xero OAuth client secret in their local `.env`; store refresh tokens there too, or in an operating-system secret store when available. Never ask the user to paste a secret into chat or commit it to the skill, repository, examples, logs, URLs, command arguments, or exported evidence. Do not print the contents of `.env` or token files while validating setup. If a secret was exposed, stop using it and have its owner rotate it.

Keep company statements, transaction exports, source IDs, personal names, and account-specific mappings outside the publishable skill folder. A published skill should contain generic instructions and placeholders only; user data belongs in the user's private workspace. Preview and reconcile before any bulk posting, use stable idempotency references, and confirm the final Xero state after writes.

Current Airwallex/Xero plan names, prices, scope names, endpoints, and rate availability can change. Verify them against the [official references](references/official-sources.md) for a new setup. User authorisation for one task does not imply permission to create credentials, change a connection, or post unrelated entries.
