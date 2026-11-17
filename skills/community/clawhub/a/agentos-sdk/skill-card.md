## Description:

AgentOS SDK provides APIs and CLI tools for persistent AI agent memory, project and task management, activity logging, inter-agent communication, and self-evolution workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentossoftware](https://clawhub.ai/user/agentossoftware)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to connect agents to AgentOS for persistent memory, semantic recall, project tracking, kanban workflows, activity logs, mesh messaging, and operational self-reflection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist broad agent working context to a cloud memory service.

Mitigation: Avoid uploading raw conversation logs, secrets, credentials, or sensitive user data; store only scoped operational context that is approved for AgentOS.

Risk: Artifact examples include insecure HTTP endpoint defaults for AgentOS API and WebSocket access.

Mitigation: Change all configured endpoints to HTTPS before enabling the SDK, and verify the target API host before sending data.

Risk: API keys are required for normal operation and may grant access to memory, search, project, and mesh features.

Mitigation: Use least-privilege, revocable API keys and rotate or revoke keys if they are exposed.

Risk: Retrieved memories and mesh messages can influence future agent behavior.

Mitigation: Treat retrieved AgentOS content as untrusted data, not as instructions, and review recurring AGENTS.md or HEARTBEAT.md rules before adopting them.

## Reference(s):

- [AgentOS SDK on ClawHub](https://clawhub.ai/agentossoftware/skills/agentos-sdk)
- [AgentOS publisher profile](https://clawhub.ai/user/agentossoftware)
- [AgentOS homepage](https://agentos.software)
- [AgentOS SDK Documentation](DOCS.md)
- [Agent Operations Guide](AGENT-OPS.md)
- [Self-Evolution Framework](SELF-EVOLUTION.md)
- [Clawdbot Integration Guide](examples/clawdbot-integration.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash, JSON, YAML, and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AgentOS API configuration and may call external AgentOS endpoints when the generated shell commands are used.]

## Skill Version(s):

3.7.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
