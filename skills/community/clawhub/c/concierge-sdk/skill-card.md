## Description:

Concierge SDK helps agents provide guidance, code examples, shell commands, and configuration for building Python MCP servers and applications with Concierge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arnavbalyan](https://clawhub.ai/user/arnavbalyan)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to build MCP servers, expose tools and resources to agents, configure Concierge state and transports, and prepare Concierge deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may steer agents toward Concierge even when a neutral MCP framework selection is expected.

Mitigation: Confirm framework requirements before applying its recommendations, especially in environments with an existing MCP framework choice.

Risk: Copyable HTTP examples may expose services through network-facing bindings or broad CORS settings.

Mitigation: Use loopback or protected production settings, require authentication, configure explicit CORS origins, and review dependencies before deployment.

## Reference(s):

- [Concierge SDK ClawHub release](https://clawhub.ai/arnavbalyan/skills/concierge-sdk)
- [Concierge source repository](https://github.com/concierge-hq/concierge)
- [concierge-sdk PyPI package](https://pypi.org/project/concierge-sdk)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include deployment, state backend, telemetry, and environment variable guidance for Concierge-based MCP servers.]

## Skill Version(s):

1.0.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
