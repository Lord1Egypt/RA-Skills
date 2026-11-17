## Description:

Accountant guides agents through bookkeeping workflows including double-entry coding, reconciliations, period close, financial statements, tax filing figures, and persistent local bookkeeping notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users can use this skill to maintain bookkeeping records, reconcile accounts, close periods, prepare management statements, and assemble figures for tax or audit workflows. It is intended for ledger-focused accounting work, not forecasting, fundraising, invoicing, document archiving, or bank payment operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently change financial records and close or lock periods without requiring explicit user approval first.

Mitigation: Confirm the entity, period, and write policy before use, and require proposed changes before ledger locks, corrections, deletions, filings, or shared finance, contact, or project updates.

Risk: Financial workflows may involve credentials, full account numbers, national IDs, e-file PINs, or payroll provider keys.

Mitigation: Do not provide raw credentials, full account numbers, national IDs, or e-file PINs; use credential pointers and limited working data such as account nicknames or last four digits.

Risk: Accounting and tax outcomes can depend on jurisdiction, period, filing status, and recently changed rates or thresholds.

Mitigation: Confirm the relevant entity, jurisdiction, filing year, and source documents before relying on filing figures, deadlines, locks, or corrections.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/accountant)
- [Clawic skill homepage](https://clawic.com/skills/accountant)
- [Skill overview](artifact/SKILL.md)
- [Bookkeeping guidance](artifact/bookkeeping.md)
- [Reconciliation guidance](artifact/reconciliation.md)
- [Close guidance](artifact/close.md)
- [Statement guidance](artifact/statements.md)
- [Tax guidance](artifact/tax.md)
- [Memory template](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and structured plain-text bookkeeping entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or record local bookkeeping memory and accounting artifacts; credentials should be represented only by pointers.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
