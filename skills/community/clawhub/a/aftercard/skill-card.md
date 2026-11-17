## Description:

Use Aftercard for purchasing research, payments, funding, saved details, merchant accounts, agent email, subscriptions, receipts, choices, and payment recovery through its connected MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aftercard](https://clawhub.ai/user/aftercard)

### License/Terms of Use:

MIT-0

## Use Case:

Users and their agents use Aftercard to research options and manage purchases, payments, saved details, accounts, subscriptions, email, and payment recovery through an existing connected service. The agent follows the user's instructions and the host's permissions while reporting only observed outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment, funding, or transfer actions can have financial impact if the task, amount, recipient, or approval state is lost during a multi-step workflow.

Mitigation: Preserve the exact user intent and service-issued operation details; stop on cancellation and reconcile uncertain submissions instead of repeating a possibly dispatched payment.

Risk: Protected payment and account details could be exposed while completing forms.

Mitigation: Use only the host's supported targeted input for the intended task, and keep protected values out of chat, files, logs, and exported evidence.

## Reference(s):

- [Aftercard skill page](https://clawhub.ai/aftercard/skills/aftercard)
- [Connect Aftercard](references/connection.md)
- [Research and provider selection](references/research.md)
- [Payments and recovery](references/payments.md)
- [Browser checkout and merchant accounts](references/browser.md)
- [Saved details and secure forms](references/memory.md)
- [Choices and email](references/requests-and-email.md)
- [Accounts, receipts, and subscriptions](references/accounts.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, API calls]

**Output Format:** [Markdown guidance and service-defined tool requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses and actions depend on the user's task and the current connected service results; there is no fixed output schema.]

## Skill Version(s):

1.0.3 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
