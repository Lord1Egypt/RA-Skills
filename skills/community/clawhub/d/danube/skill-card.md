## Description:

Governed tool access for your agent — one Danube API key unlocks your organization's own tools plus a large, growing catalog of ready-made services. Search, inspect, and execute tools over native MCP or plain curl, with explicit confirmation before anything that writes, sends, spends, or deletes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[preston-thiele](https://clawhub.ai/user/preston-thiele)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Danube to discover and call organization connected tools and marketplace services through MCP or REST. The skill explains how to inspect tools, configure credentials, handle confirmation requests, and interpret results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feedback submissions and persistent defaults may be created without prior approval.

Mitigation: Require approval for saved defaults, ratings, and reports after showing their exact content and destination.

Risk: Credential and automation controls may not limit access as expected; documented OAuth scopes and tool-list filters do not restrict authority.

Mitigation: Use an explicitly restricted API key for the intended organization, and avoid schedules unless their credential and editing boundaries are acceptable.

## Reference(s):

- [Danube OpenClaw documentation](https://docs.danubeai.com/sdk/openclaw)
- [Danube REST API reference](artifact/references/rest-api.md)
- [Danube troubleshooting guide](artifact/references/troubleshooting.md)
- [Danube skill release on ClawHub](https://clawhub.ai/preston-thiele/skills/danube)
- [Danube MCP server](https://mcp.danubeai.com/mcp)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration instructions, Text]

**Output Format:** [Markdown instructions, shell commands, JSON API requests, and tool response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool availability and results depend on the connected Danube account and its permissions.]

## Skill Version(s):

8.1.51 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
