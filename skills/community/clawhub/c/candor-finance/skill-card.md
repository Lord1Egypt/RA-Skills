## Description:

Opens the person's Candor workspace, says where their money stands, and routes to the right Candor workflow. Use when the person asks about their money, spending, balances, bills, debts, goals, or plans and no more specific Candor skill fits, including a quick question about a balance, a bill, or a charge, or a life decision that costs or earns money even when money is not named.

This skill is ready for commercial/non-commercial use.

## Publisher:

[candor](https://clawhub.ai/user/candor)

### License/Terms of Use:

MIT-0

## Use Case:

External users use the skill with an authenticated Candor workspace to understand their finances, organize records, and work through questions about spending, bills, debts, goals, and plans. It routes each request to a relevant finance workflow and helps keep the workspace current.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is marked suspicious because scanners reported broad financial data changes and external actions beyond its stated role; the review is incomplete.

Mitigation: Before installation, review the write and external-action scope, automatic reporting and retention practices, and the portions that were not fully analyzed; consider waiting until that review is complete.

Risk: Product reports may be sent to Candor automatically under the default reporting preference.

Mitigation: Check the workspace reporting preference and choose ask or off when appropriate; reports should describe product behavior without amounts, account numbers, merchant or institution names, or people's names.

Risk: The skill can change financial records in the Candor workspace, and its workflows may involve actions outside Candor.

Mitigation: Review proposed record changes and get the person's okay before external actions such as payments, transfers, cancellations, disputes, messages, applications, or trades.

## Reference(s):

- [Candor setup guide](https://candor.money/START.md)
- [Candor Finance on ClawHub](https://clawhub.ai/candor/skills/candor-finance)
- [Access and recovery](references/access-and-recovery.md)
- [Reports](references/reports.md)
- [Adding financial records](workflows/candor-add-records/WORKFLOW.md)
- [Planning a financial goal](workflows/candor-plan-a-goal/WORKFLOW.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, JSON, Reports]

**Output Format:** [Conversational text and Markdown, with Candor CLI commands and structured JSON inputs or reports as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update workspace records and create reports; actions outside Candor that affect finances require the person's okay.]

## Skill Version(s):

1.3.9 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
