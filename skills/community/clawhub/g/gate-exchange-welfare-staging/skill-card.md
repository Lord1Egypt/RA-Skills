## Description:

Gate welfare center and new-user task skill for checking welfare eligibility, rewards, and task status using real Gate MCP data only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaixianggeng](https://clawhub.ai/user/gaixianggeng)

### License/Terms of Use:

MIT-0

## Use Case:

Gate users and support-oriented agents use this skill to answer welfare, reward, and new-user task questions. It checks the user's eligibility first, then returns existing-user guidance or a new-user task list based only on live MCP data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads Gate welfare eligibility and new-user task status through the configured Gate MCP session.

Mitigation: Install only when account-specific welfare lookup is intended, keep credentials in the configured MCP session, and do not paste secrets into chat.

Risk: Ambiguous welfare, reward, or task requests may trigger an eligibility check.

Mitigation: Use the skill for Gate welfare and rewards intents, and stop on missing authentication, permission errors, or unavailable welfare tools.

Risk: Reward or task guidance can be misleading if values are fabricated or stale.

Mitigation: Render only fields returned by the documented MCP tools and direct failures or uncertain cases to the official Gate rewards hub.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gaixianggeng/skills/gate-exchange-welfare-staging)
- [Gate Skills Repository](https://github.com/gate/gate-skills)
- [Gate Rewards Hub](https://www.gate.com/rewards_hub)
- [Gate API Key Management](https://www.gate.com/myaccount/profile/api-key/manage)
- [Gate Welfare MCP Specification](artifact/references/mcp.md)
- [Gate MCP Data Usage Examples](artifact/references/mcp-data-usage.md)
- [Gate Welfare Runtime Rules](artifact/references/gate-runtime-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with Gate welfare eligibility, task details, reward fields, status labels, and fallback messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only output; uses configured Gate MCP credentials and must not claim rewards, trade, or modify account data.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter version 2026.4.3-1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
