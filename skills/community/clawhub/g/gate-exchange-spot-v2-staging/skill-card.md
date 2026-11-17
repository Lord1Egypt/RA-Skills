## Description:

Gate spot trading and account operations skill for buy/sell actions, account value checks, conditional or trigger orders, order management, and fill verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaixianggeng](https://clawhub.ai/user/gaixianggeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to route Gate spot-trading requests through configured Gate credentials, including portfolio checks, order drafts, confirmed spot orders, amendments, cancellations, and post-trade verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place, amend, or cancel real Gate spot orders when configured with write-capable credentials.

Mitigation: Use the minimum required API key permissions, keep credentials in the configured MCP session, and require an order draft plus immediate explicit user confirmation before every write action.

Risk: Security evidence reports inconsistent confirmation requirements for cancellation and amendment flows, especially cancel-all behavior.

Mitigation: Review cancellation, amendment, and cancel-all flows before enabling the skill, and enforce manual confirmation for every write action when operating it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gaixianggeng/skills/gate-exchange-spot-v2-staging)
- [Gate Skill Homepage](https://github.com/gate/gate-skills)
- [Gate API Key Management](https://www.gate.com/myaccount/profile/api-key/manage)
- [Gate Publisher Website](https://www.gate.com)
- [Gate Runtime Rules](references/gate-runtime-rules.md)
- [Gate Spot MCP Specification](references/mcp.md)
- [Gate Spot Scenarios](references/scenarios.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, API calls]

**Output Format:** [Markdown responses with structured order drafts, execution reports, account summaries, and setup or recovery guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use configured Gate MCP tools for read-only account and market queries or confirmed write actions.]

## Skill Version(s):

1.0.1 (source: server release metadata); artifact frontmatter version 2026.4.3-1

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
