## Description:

Gate platform activity and campaign hub skill for activity recommendations, trading competitions, airdrops, and enrolled activity lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find Gate Exchange activity campaigns such as hot activities, airdrops, trading competitions, VIP activities, and asset- or scenario-based campaigns. It can also direct a configured user to their Gate activity entry for enrolled and ongoing activities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Gate credentials and may retrieve account-specific activity entry data through the local MCP session.

Mitigation: Install only if read-only Gate activity access is acceptable, and use the configured local MCP session rather than pasting secrets into chat.

Risk: Broad activity requests could expose account-specific activity entry behavior if intent is not explicit.

Mitigation: Call the My Activities flow only when the user explicitly asks for account-specific or enrolled activity information.

Risk: Activity links may need stronger host validation before being shown to users.

Mitigation: Prefer versions that validate activity links against approved Gate HTTPS hosts and review returned links before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gate-exchange/skills/gate-exchange-activitycenter)
- [Gate skills homepage](https://github.com/gate/gate-skills)
- [Gate ActivityCenter MCP Specification](references/mcp.md)
- [Gate Activity Center Runtime Rules](references/gate-runtime-rules.md)
- [Scenarios and Prompt Examples](references/scenarios.md)
- [Gate API key management](https://www.gate.com/myaccount/profile/api-key/manage)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown tables, links, and concise status or setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only activity results; account-specific responses require configured Gate credentials.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata; artifact frontmatter and changelog report 2026.4.3-1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
