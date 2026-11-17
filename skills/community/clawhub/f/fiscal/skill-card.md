## Description:

Fiscal acts as a personal accountant using the fscl (fiscal) CLI for Actual Budget, helping with personal finances, budgeting, spending, bills, subscriptions, bank imports, accounts, and categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benbjurstrom](https://clawhub.ai/user/benbjurstrom)

### License/Terms of Use:


## Use Case:

External users and developers use Fiscal to manage Actual Budget workflows through an agent that turns plain-language finance requests into reviewed fscl commands, imports, categorization, rules, budget updates, and spending summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive financial data and Actual Budget credentials.

Mitigation: Prefer local-only mode unless a remote Actual Budget server is intentional, avoid sharing real passwords in chat or command-line flags, and require HTTPS for non-local servers.

Risk: Imports, rules, category changes, budget edits, and deletes can materially change a user's budget data.

Mitigation: Preview imports and draft/apply workflows before committing, confirm financial decisions with the user, and back up the budget before bulk edits or deletes.

Risk: Unpinned package execution or skill installation can introduce supply-chain uncertainty.

Mitigation: Pin and verify fscl and skill installer versions instead of running unpinned npx commands.

## Reference(s):

- [Actual Budget](https://actualbudget.org/)
- [Workflow: New Budget Onboarding](references/workflow-onboarding.md)
- [Workflow: Budget Optimization](references/workflow-optimization.md)
- [Workflow: Budget Maintenance](references/workflow-maintenance.md)
- [Command Cheat Sheet](references/commands.md)
- [Command Reference](references/command-reference.md)
- [Budgeting Concepts](references/budgeting.md)
- [Importing Transactions](references/import-guide.md)
- [Transaction Rules](references/rules.md)
- [Credit Cards](references/credit-cards.md)
- [Query Library](references/query-library.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown with plain-language summaries, tables, and inline bash or JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses fscl JSON output internally but should present human-readable summaries rather than raw JSON.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
