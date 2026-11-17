## Description:

Build AI agents on Cloudflare Workers using the Agents SDK for stateful agents, durable workflows, real-time WebSocket apps, scheduled tasks, MCP servers, chat applications, voice agents, and browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[creativerezz](https://clawhub.ai/user/creativerezz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build and configure Cloudflare Agents SDK applications, including stateful agents, workflows, WebSocket clients, chat agents, MCP integrations, scheduling, queues, retries, observability, voice, and browser automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated agent code may copy under-scoped authentication, MCP, or approval-gating examples into production.

Mitigation: Review generated code before deployment and add authentication, allowlists, approval checks, logging redaction, and data-retention controls.

Risk: Examples involving token-in-URL flows, open MCP registration, unauthenticated MCP routes, or Codemode with sensitive tools can expose sensitive operations if reused as-is.

Mitigation: Treat these examples as starting points only; require production hardening and explicit review for routes, tools, credentials, and data handling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/creativerezz/skills/agents-sdk)
- [Cloudflare Agents documentation](https://developers.cloudflare.com/agents/)
- [Getting started](https://developers.cloudflare.com/agents/getting-started/quick-start/)
- [Configuration](https://developers.cloudflare.com/agents/api-reference/configuration/)
- [Agents API](https://developers.cloudflare.com/agents/api-reference/agents-api/)
- [Store and sync state](https://developers.cloudflare.com/agents/api-reference/store-and-sync-state/)
- [Routing](https://developers.cloudflare.com/agents/api-reference/routing/)
- [Callable methods](https://developers.cloudflare.com/agents/api-reference/callable-methods/)
- [Run workflows](https://developers.cloudflare.com/agents/api-reference/run-workflows/)
- [MCP integration](references/mcp.md)
- [Streaming chat](references/streaming-chat.md)
- [Human-in-the-loop](references/human-in-the-loop.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript, TSX, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses retrieved Cloudflare Agents documentation as supporting reference material.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
