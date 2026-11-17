## Description:

Use the DAX Ledger API to authenticate, list portfolios, retrieve portfolio KPIs, list findings, retrieve position snapshots, and list/filter transactions with pagination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pedromxavier14](https://clawhub.ai/user/pedromxavier14)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to choose DAX Ledger API endpoints and request authenticated portfolio, transaction, tax, compliance, KPI, findings, and position data with appropriate pagination and filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide authenticated access to sensitive financial, tax, and compliance data.

Mitigation: Keep API credentials in a trusted secret mechanism, avoid pasting secrets into chat, and request only the portfolio, transaction, tax, or compliance fields needed for the task.

Risk: Over-broad API requests can expose more account data than a task requires.

Mitigation: Use pagination, endpoint selection, and filters to limit responses to the minimum data needed.

## Reference(s):

- [DAX Ledger API Reference](references/apis.md)
- [DAX Ledger API Base URL](https://app.daxledger.io)
- [ClawHub Skill Page](https://clawhub.ai/pedromxavier14/skills/daxledger-api)

## Skill Output:

**Output Type(s):** [guidance, markdown, API calls, configuration]

**Output Format:** [Markdown with endpoint paths, query parameters, JSON examples, and credential configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DAXLEDGER_API_KEY and DAXLEDGER_API_SECRET; may include pagination, filtering, and Base64 filter encoding guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
