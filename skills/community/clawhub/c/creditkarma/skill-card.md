## Description:

Access Credit Karma transaction data via MCP. Use when the user asks about their Credit Karma transactions, spending by category or merchant, account summaries, account balances, or wants to sync or query their financial data. Triggers on phrases like "sync my transactions", "what did I spend on", "show my Credit Karma data", "spending by category", "top merchants", or any request involving personal finance data from Credit Karma. Requires creditkarma-mcp installed and the creditkarma server registered (see Setup below).

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to sync and query their Credit Karma transactions, review spending by category or merchant, and inspect account summaries and balances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credit Karma session cookies grant account access and could be exposed if copied into chat histories, logs, shared configuration, or version control.

Mitigation: Treat cookies like passwords, keep them out of shared locations, use a reviewed local authentication flow, and check bridge permissions and the exact package version before installation.

## Reference(s):

- [creditkarma-mcp package](https://www.npmjs.com/package/creditkarma-mcp)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)
- [Credit Karma](https://www.creditkarma.com)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [Natural-language transaction, spending, and account summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Freshness depends on the latest successful sync; balance results identify their source and may be stale.]

## Skill Version(s):

3.4.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
