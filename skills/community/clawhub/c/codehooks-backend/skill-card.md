## Description:

Deploy serverless backends for REST APIs, webhooks, data storage, scheduled jobs, queue workers, and autonomous workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canuto](https://clawhub.ai/user/canuto)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to give OpenClaw agents a Codehooks backend for REST APIs, webhooks, persistent data, scheduled jobs, queue workers, and autonomous workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can receive broad authority to deploy code, query data, and manage a live Codehooks backend.

Mitigation: Use a dedicated project, grant the least-privileged or shortest-lived token available, and review deployments before they go live.

Risk: The Codehooks admin token can be exposed through prompts, logs, or source control if handled carelessly.

Mitigation: Keep CODEHOOKS_ADMIN_TOKEN out of prompts, logs, and source control, and rotate it after use.

Risk: Workflow callbacks can send results to unintended endpoints if callback URL patterns are not checked.

Mitigation: Validate callback URL patterns before using workflow callback examples in production.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/canuto/skills/codehooks-backend)
- [Codehooks documentation](https://codehooks.io/docs)
- [Codehooks CLI reference](https://codehooks.io/docs/cli)
- [Codehooks AI development prompt](https://codehooks.io/llms.txt)
- [Codehooks templates](https://github.com/RestDB/codehooks-io-templates)
- [Codehooks MCP server](https://github.com/RestDB/codehooks-mcp-server)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the coho CLI and CODEHOOKS_ADMIN_TOKEN for non-interactive deployment workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
