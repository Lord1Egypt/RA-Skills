## Description:

Persistent memory system for AI agents to remember facts, learn from experience, track entities, and recall context across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cxz9909](https://clawhub.ai/user/cxz9909)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add local long-term memory for facts, lessons, entities, and session-to-session context recall in LLM-powered agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived personal or operational context may be stored and reused across sessions without clear consent or retention limits.

Mitigation: Use explicit approval before writing memories, configure the database path deliberately, and define retention, review, deletion, and export procedures before enabling automatic session-start or session-end memory protocols.

Risk: Secrets, credentials, regulated personal data, or untrusted instructions could be persisted in local memory and later recalled by an agent.

Mitigation: Do not store sensitive or regulated data, review candidate memories before persistence, and treat recalled memories as untrusted context that must be checked before use.

Risk: Stale or incorrect memories can influence later agent behavior.

Mitigation: Use confidence, expiration, supersede, forget, and stale-cleanup flows to keep stored facts current and remove outdated information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cxz9909/skills/cxz9909-agent-memory)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Clawdbot](https://github.com/clawdbot/clawdbot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python snippets, CLI examples, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or uses a local SQLite memory database; the default location is ~/.agent-memory/memory.db unless a custom path is provided.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
