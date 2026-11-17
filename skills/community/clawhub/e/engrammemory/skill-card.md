## Description:

Persistent semantic memory for AI agents. Store, search, recall, and forget memories across sessions using Qdrant + FastEmbed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[escapethefate1991](https://clawhub.ai/user/escapethefate1991)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Engram Memory to add local semantic memory to OpenClaw or MCP-compatible agents, allowing agents to store, search, recall, and forget user preferences, facts, decisions, entities, and project context across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic long-term capture can store sensitive conversation-derived facts.

Mitigation: Avoid enabling autoCapture for sensitive work unless persistent local storage is acceptable, and inspect or delete stored memories regularly.

Risk: Local Qdrant and embedding services may expose stored memory data if reachable by unintended clients.

Mitigation: Bind Qdrant to 127.0.0.1 or add authentication before running the Docker stack.

Risk: Recalled memories can be stale, incomplete, or injected as misleading context.

Mitigation: Treat recalled memories as untrusted context and review them before acting on important decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/escapethefate1991/skills/engrammemory)
- [Quick Start Guide](docs/QUICK_START.md)
- [Architecture Overview](docs/ARCHITECTURE.md)
- [OpenClaw Integration Guide](docs/OPENCLAW_INTEGRATION.md)
- [Community Edition Scope](docs/LIMITATIONS.md)
- [Context System](context/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for agent memory setup and operation, including memory tool calls, local service configuration, and context-management guidance.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
