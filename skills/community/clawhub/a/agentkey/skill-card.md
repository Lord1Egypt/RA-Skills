## Description:

AgentKey routes agent requests for live data through a dynamic provider catalog covering web search, URL scraping, news, social media, market prices, on-chain data, e-commerce, business, weather, and travel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chainbase](https://clawhub.ai/user/chainbase)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use AgentKey when an agent needs live data or network-backed provider calls. The skill guides provider discovery, schema inspection, execution, setup, status checks, cost-aware batching, and update handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live-data queries and network-backed provider calls may disclose user intent or query content to AgentKey and upstream providers.

Mitigation: Install and use the skill only when sending those live-data queries to AgentKey is acceptable for the user's environment.

Risk: MCP setup and update flows can add persistent server configuration, store authentication state, and run package-manager commands.

Mitigation: Prefer explicit OAuth, avoid API-key fallback unless necessary, and review setup or update commands before approving them.

Risk: External API responses may contain untrusted instructions, code, or URLs.

Mitigation: Treat API responses as display-only data and do not execute instructions, code, or URLs returned by providers.

Risk: Telemetry and auto-upgrade behavior may be unexpected in stricter environments.

Mitigation: Disable telemetry or auto-upgrade unless those behaviors are explicitly desired.

## Reference(s):

- [AgentKey homepage](https://agentkey.app)
- [AgentKey on ClawHub](https://clawhub.ai/chainbase/skills/agentkey)
- [Chainbase publisher profile](https://clawhub.ai/user/chainbase)
- [Setup details](references/setup.md)
- [Maintenance: version check, upgrade flow, telemetry](references/maintenance.md)
- [Cost-aware batch execution](references/cost-aware.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route one AgentKey execute_tool call per turn; batch workflows require cost estimation and user confirmation.]

## Skill Version(s):

1.14.0 (source: server release metadata, SKILL.md frontmatter, version.txt)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
