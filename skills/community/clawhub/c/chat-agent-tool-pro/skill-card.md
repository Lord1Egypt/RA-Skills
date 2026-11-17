## Description:

聊天Agent工具专业版 helps agents configure and operate an enterprise multi-agent chat platform with persistent rooms, message replay, enterprise authentication, encryption, branding, auditing, and high-availability guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, independent builders, and enterprise teams use this skill to plan and configure multi-agent chat rooms with persistence, replay, authentication, encryption, auditing, and deployment examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad agent authority, including file editing and shell command execution.

Mitigation: Install it only in workspaces where those permissions are intended, review commands before execution, and restrict use to chat-platform administration workflows.

Risk: Retained messages and replay access may expose sensitive or regulated conversations.

Mitigation: Set strict retention policies, limit replay access by role, audit access to retained messages, and use encryption for stored message data.

Risk: Callbacks, webhooks, CRM/IM synchronization, and external URLs can move chat data outside the intended environment.

Mitigation: Validate external URLs, allowlist integration endpoints, avoid sending secrets or unnecessary conversation data, and monitor webhook delivery logs.

Risk: OAuth, database, callback, and encryption credentials are needed for enterprise deployment.

Mitigation: Provide credentials through environment variables or a managed secret store and avoid writing tokens, keys, or connection strings into skill files or shared configuration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/chat-agent-tool-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with CLI commands, Python/YAML/nginx snippets, and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include configuration snippets, command examples, troubleshooting steps, and structured result examples.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
