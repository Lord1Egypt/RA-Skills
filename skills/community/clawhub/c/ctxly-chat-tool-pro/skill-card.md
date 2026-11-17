## Description:

匿名聊天(专业版) supports Agent chat-room workflows with multi-room management, message persistence and export, webhook notifications, rate limiting and retry guidance, encryption guidance, and Agent identity verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and Agent teams use this skill to coordinate anonymous or team chat-room workflows across multiple Agent participants, including room management, message export, webhook delivery, retry behavior, and token-scoped operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is flagged as suspicious because its instructions are broad and mismatched for a chat tool with file and shell access.

Mitigation: Review before installing and limit use to chat-room management and message workflows rather than database, system administration, or unrelated file operations.

Risk: Chat tokens, exported archives, webhook destinations, and conversation content may expose sensitive information.

Mitigation: Use least-privilege tokens, keep secrets in environment or secret-management systems, validate webhook destinations, and review exports before sharing or storing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ctxly-chat-tool-pro)
- [ctxly chat service](https://chat.ctxly.app)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with inline shell commands, JSON examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe chat-room API calls, webhook setup, token handling, export formats, and operational safeguards.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
