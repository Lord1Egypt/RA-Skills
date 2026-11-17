## Description:

Address tracker and analysis for on-chain addresses, using Gate-Info MCP tools to retrieve address profiles, transaction history, and fund-flow traces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaixianggeng](https://clawhub.ai/user/gaixianggeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to inspect blockchain addresses, summarize balances, labels, risk signals, DeFi positions, and optionally trace large transactions or fund flows. It is intended for read-only on-chain address analysis, not trading or account mutation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on parent-directory runtime rule files that were not included in the reviewed package.

Mitigation: Review the referenced runtime rules before installation or use a packaged release that includes all required runtime rules.

Risk: The skill can automatically broaden a basic address lookup into deeper fund-flow tracing based on labels, balance, or risk flags.

Mitigation: Confirm user intent before escalating from basic profile lookup to deep fund-flow tracing, especially for sensitive investigations.

Risk: Tool declarations are inconsistent: the description lists three MCP tools while the skill body also lists info_onchain_get_transaction.

Mitigation: Keep the allowed MCP tool list consistent and review tool availability before execution.

## Reference(s):

- [Gate Address Tracker MCP Specification](references/mcp.md)
- [Scenarios & Prompt Examples](references/scenarios.md)
- [Gate.com](https://www.gate.com)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, API Calls, Guidance]

**Output Format:** [Markdown report with tables, summaries, risk notes, and missing-data guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only output based on Gate-Info MCP responses; deep tracing may be conditional on user intent, labels, balance size, or risk flags.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter version 2026.4.3-1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
