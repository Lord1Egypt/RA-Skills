## Description:

Guides reconciliation of Airwallex multicurrency wallets with Xero, including failed foreign-currency syncs, statement matching, owner funding, FX, and audit evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shellishack](https://clawhub.ai/user/shellishack)

### License/Terms of Use:

MIT-0

## Use Case:

Accountants, bookkeepers, and authorized finance teams use this skill to trace Airwallex wallet activity into Xero, resolve sync and currency discrepancies, and document balanced, auditable reconciliations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial records or credentials may be exposed during reconciliation.

Mitigation: Use scoped credentials and keep .env files, statements, and exports private.

Risk: Duplicate or incorrect entries may result from bulk posting or failed sync retries.

Mitigation: Preview changes, check source IDs and existing Xero entries before posting, and verify the final Xero state after writes.

Risk: Misclassified funding or FX entries may misstate the accounts.

Mitigation: Document rate and classification decisions and obtain approval from an accountant or authorized owner before final posting.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/shellishack/skills/airwallex-xero-reconciliation)
- [Reconciliation playbook](references/reconciliation-playbook.md)
- [Official sources to verify for a new setup](references/official-sources.md)
- [Airwallex Xero bank feed and wallet-currency mapping](https://help.airwallex.com/hc/en-gb/articles/6693947113871-What-is-Xero-bank-feed-or-sync-with-Airwallex)
- [Xero Accounting API bank transactions](https://developer.xero.com/documentation/api/accounting/banktransactions)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown with reconciliation tables and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Source-to-ledger mapping, documented FX treatment, and reconciliation checks; posting requires authorized review.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
