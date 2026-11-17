## Description:

Gate platform activity and campaign hub skill. Use when the user asks about trading competitions, airdrops, or their enrolled activities. Triggers on 'recommend activities', 'trading competition', 'my activities', 'airdrop campaign'.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaixianggeng](https://clawhub.ai/user/gaixianggeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find Gate Exchange campaign activities, filter recommendations by activity type or scenario, search by activity name, and open their enrolled activities entry through a configured local Gate MCP session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses configured Gate API credentials through a local Gate MCP session.

Mitigation: Use an API key limited to Activity:Read and rely on the configured MCP session instead of pasting secrets into chat.

Risk: The skill may display API-provided absolute activity links that are not constrained to trusted Gate domains.

Mitigation: Verify that each destination is an expected Gate domain before signing in, claiming rewards, connecting wallets, or entering account information.

Risk: Activity availability, rewards, and deadlines can be time-sensitive or unavailable in returned data.

Mitigation: Display only API-returned activity data, avoid investment advice, and use explicit unavailable or empty-state guidance when data is missing.

## Reference(s):

- [Gate Skills Repository](https://github.com/gate/gate-skills)
- [Gate API Key Management](https://www.gate.com/myaccount/profile/api-key/manage)
- [Gate ActivityCenter MCP Specification](references/mcp.md)
- [Gate Activity Center Runtime Rules](references/gate-runtime-rules.md)
- [Activity Center Scenarios and Prompt Examples](references/scenarios.md)

## Skill Output:

**Output Type(s):** [markdown, guidance]

**Output Format:** [Markdown activity cards, tables, links, and empty-state guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Activity list queries are limited to three results per request; outputs preserve API-provided activity information and apply the documented URL processing rules.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter version 2026.4.3-1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
