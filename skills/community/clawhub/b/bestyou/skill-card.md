## Description:

Connect your AI agent to BestYou health intelligence via MCP, using wearable and HealthKit-derived insights to query readiness, generate workouts, analyze meals, and manage an adaptive daily action plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kentsteffen](https://clawhub.ai/user/kentsteffen)

### License/Terms of Use:

MIT-0

## Use Case:

External users connect their agent to BestYou's MCP server to review readiness, daily plans, workouts, nutrition, progress, and weekly health trends from processed BestYou insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a BestYou API key for authenticated MCP access.

Mitigation: Treat BESTYOU_API_KEY like a password, keep it out of commits and shared logs, and store it in a secure environment or secret store.

Risk: The skill connects an agent to personal health insights through an external MCP service.

Mitigation: Confirm the user trusts BestYou, review granted scopes in the BestYou app, and avoid exposing raw auth values or sensitive health details beyond the conversation.

Risk: Setup depends on installing and configuring mcporter.

Mitigation: Install mcporter from a trusted package source and verify the MCP server configuration before using health tools.

## Reference(s):

- [BestYou Health Intelligence Skill](https://clawhub.ai/kentsteffen/skills/bestyou)
- [BestYou](https://bestyou.ai)
- [BestYou OpenClaw Setup Guide](https://bestyou.ai/openclaw-setup)
- [BestYou MCP Playground](https://mcp.bestyou.ai/openclaw)
- [Security & Privacy](references/security.md)
- [BestYou MCP Setup Guide](references/setup.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance]

**Output Format:** [Markdown or conversational text with MCP tool calls and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses BESTYOU_API_KEY for authenticated MCP requests; returns processed health insights, plans, workouts, and nutrition analysis.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
