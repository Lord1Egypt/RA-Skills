## Description:

Manage EnvelopeBudget budgets, transactions, accounts, envelopes, payees, and reports through the EnvelopeBudget.com API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djedi](https://clawhub.ai/user/djedi)

### License/Terms of Use:

MIT-0

## Use Case:

EnvelopeBudget users can ask an agent to inspect budgets, accounts, envelopes, transactions, payees, and spending reports, and to prepare or run EnvelopeBudget API calls for routine personal finance management. The skill can also help create, update, transfer, reconcile, archive, or delete budget records when the user explicitly approves those live changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an EnvelopeBudget API key and can access financial budgeting data.

Mitigation: Store the API key only in the ENVELOPE_BUDGET_API_KEY environment variable, avoid displaying it in agent responses or logs, and install only when API-key access is acceptable.

Risk: POST, PUT, PATCH, and DELETE requests can make live changes to budget records.

Mitigation: Require the agent to show the proposed method, endpoint, and JSON body, then obtain explicit user approval before running any mutating request.

Risk: Incorrect budget, account, envelope, payee, date, amount, or sign values can create misleading financial records.

Mitigation: Fetch the relevant budget, account, envelope, and payee IDs first, confirm cents-based amounts and positive or negative direction with the user, and prefer read-only calls when the requested action is ambiguous.

## Reference(s):

- [EnvelopeBudget API Reference](artifact/references/api-reference.md)
- [EnvelopeBudget Website](https://envelopebudget.com)
- [ClawHub EnvelopeBudget Skill Page](https://clawhub.ai/djedi/skills/envelopebudget)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include formatted JSON API responses from EnvelopeBudget.com.]

## Skill Version(s):

1.2.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
