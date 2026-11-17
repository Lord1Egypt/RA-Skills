## Description:

Gate multi-account asset and balance query skill for checking total assets, account balances, and specific coin holdings across all accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaixianggeng](https://clawhub.ai/user/gaixianggeng)

### License/Terms of Use:

MIT-0

## Use Case:

External Gate users use this skill to query read-only asset overviews, per-coin holdings, and account-specific balances through a configured local Gate MCP session. It helps summarize spot, margin, futures, options, unified, finance, and TradFi balances without placing trades or transfers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured Gate credentials allow the agent to retrieve sensitive financial account balances.

Mitigation: Install only for users who want balance lookups through the local Gate MCP session, and limit responses to values returned by documented read-only tools.

Risk: Gate API keys with trading or transfer permissions could expand impact beyond the skill's read-only behavior.

Mitigation: Use read-only Gate API keys with only the listed read permissions, and avoid enabling trading or transfer permissions for this skill.

Risk: Broad balance requests may trigger account lookups that reveal more financial data than the user intended.

Mitigation: Clarify account or currency scope when ambiguous, and mark partial or degraded results when an account module is unavailable.

## Reference(s):

- [Gate Exchange Assets Runtime Rules](references/gate-runtime-rules.md)
- [Gate Assets MCP Specification](references/mcp.md)
- [Gate Skills Homepage](https://github.com/gate/gate-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown balance summaries with account distributions, valuation notes, and degraded-result markers when account modules are unavailable.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only responses based on Gate MCP data; TradFi and payment balances are separated from CEX total valuation when applicable.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata); bundled skill frontmatter version 2026.4.8-1

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
