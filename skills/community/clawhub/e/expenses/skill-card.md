## Description:

Expenses helps an agent record, split, categorize, reconcile, and report spending across daily expenses, shared costs, reimbursements, receipts, project budgets, and trip budgets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill with an agent to maintain local expense records, including purchases, refunds, shared balances, reimbursement claims, receipts, bounded budgets, travel spend, and statement reconciliation. It is intended for expense tracking and reporting, not net worth planning, debt planning, bookkeeping, invoicing, or payment processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct durable edits to local financial records, including ledgers, shared balances, claims, budgets, statement imports, and related configuration.

Mitigation: Before use, require preview and user approval for file writes, deletions, migrations, recategorization, statement imports, and shared contact or account updates.

Risk: Expense workflows may involve sensitive financial information or credentials pasted by the user.

Mitigation: Keep records local, avoid saving credential values, and store only pointer references for secrets such as keychain, password-manager, environment-variable, or file locators.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/expenses)
- [Clawic Expenses homepage](https://clawic.com/skills/expenses)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Concise natural-language responses and structured Markdown records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains local expense data under declared configuration paths and reports amounts with currencies and as-of dates.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
