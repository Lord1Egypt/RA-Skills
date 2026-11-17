## Description:

DailyExpenseTracker API integration for recording expenses, checking balances, and managing transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gurpreetkaits](https://clawhub.ai/user/gurpreetkaits)

### License/Terms of Use:


## Use Case:

OpenClaw users use this skill to record expenses, check wallet balances, and retrieve transactions or categories through the DailyExpenseTracker API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send or modify sensitive financial records through an external DailyExpenseTracker API.

Mitigation: Use it only with real financial data after reviewing the configuration and confirming that transaction details and balance queries may be sent to the service.

Risk: Broad activation around expenses, spending, transactions, wallets, or DET could trigger API use in more situations than intended.

Mitigation: Prefer explicit user requests before recording expenses, checking balances, or retrieving financial records.

Risk: The DET token is stored in OpenClaw configuration.

Mitigation: Protect the OpenClaw config file, rotate the token if exposed, and avoid embedding the token in skill text or command examples.

## Reference(s):

- [DailyExpenseTracker ClawHub skill page](https://clawhub.ai/gurpreetkaits/skills/det)
- [DailyExpenseTracker API](https://dailyexpensetracker.in/api)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a configured DET API token and may send transaction details, wallet queries, and category queries to the DailyExpenseTracker API.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
