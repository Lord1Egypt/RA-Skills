## Description: <br>
Build AI agents on Cloudflare Workers using the Agents SDK for stateful agents, durable workflows, real-time WebSocket apps, scheduled tasks, MCP servers, chat applications, voice agents, and browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[creativerezz](https://clawhub.ai/user/creativerezz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build and modify Cloudflare Agents SDK projects with current documentation for persistent state, callable RPC, workflows, queues, observability, chat, voice, MCP, webhooks, and browser automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples may involve OAuth tokens, wallet-related flows, or other sensitive credentials. <br>
Mitigation: Avoid long-lived tokens in URLs, keep credentials in managed secrets, and adapt examples before production use. <br>
Risk: MCP and browser automation examples can expose powerful external actions to a model. <br>
Mitigation: Connect only trusted MCP servers, filter model-accessible tools, and restrict browser automation to authorized domains and non-sensitive sessions. <br>
Risk: Webhook examples can be unsafe if request bodies are parsed before verification. <br>
Mitigation: Verify webhooks with a single buffered raw body before processing event payloads. <br>


## Reference(s): <br>
- [Cloudflare Agents documentation](https://developers.cloudflare.com/agents/) <br>
- [Quick start](https://developers.cloudflare.com/agents/getting-started/quick-start/) <br>
- [Configuration](https://developers.cloudflare.com/agents/api-reference/configuration/) <br>
- [Agents API](https://developers.cloudflare.com/agents/api-reference/agents-api/) <br>
- [State & Scheduling](references/state-scheduling.md) <br>
- [Callable Methods](references/callable.md) <br>
- [Routing](references/routing.md) <br>
- [Streaming Chat with AIChatAgent](references/streaming-chat.md) <br>
- [Client SDK](references/client-sdk.md) <br>
- [Workflows Integration](references/workflows.md) <br>
- [Durable Execution](references/durable-execution.md) <br>
- [Queue & Retries](references/queue-retries.md) <br>
- [MCP Integration](references/mcp.md) <br>
- [Email Handling](references/email.md) <br>
- [Webhooks & Push Notifications](references/webhooks-push.md) <br>
- [Observability](references/observability.md) <br>
- [Human-in-the-Loop](references/human-in-the-loop.md) <br>
- [Server-Driven Messages](references/server-driven-messages.md) <br>
- [Think](references/think.md) <br>
- [Voice](references/voice.md) <br>
- [Codemode](references/codemode.md) <br>
- [Browse the Web](references/browse-the-web.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript, JSONC, TSX, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Cloudflare documentation references and includes implementation gotchas for Agents SDK projects.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
