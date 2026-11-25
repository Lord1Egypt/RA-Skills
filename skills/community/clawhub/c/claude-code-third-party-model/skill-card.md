## Description:

帮助开发者将 Claude Code 连接到第三方 Anthropic 或 OpenAI 兼容模型端点，并排查模型、配置和连接性能问题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to connect Claude Code or WorkBuddy to third-party model endpoints, select and switch model profiles, and diagnose configuration or connection issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports an unauthenticated route to a tool-capable agent.

Mitigation: Keep the bridge limited to a trusted local environment, do not expose it to untrusted networks, and require client-token authentication wherever the gateway supports it.

Risk: Credentials and sensitive diagnostic information may be exposed through gateway configuration or logs.

Mitigation: Use dedicated credentials with limited access, protect configuration and diagnostic files, and inspect or disable request dumps before sending sensitive prompts.

Risk: Gateway process management may affect other running processes.

Mitigation: Review startup and shutdown behavior, run the gateway with least privilege, and verify which processes it may start or stop.

## Reference(s):

- [ClawHub release](https://clawhub.ai/oracis/skills/claude-code-third-party-model)
- [Project repository linked in the skill](https://github.com/oracis/claude-code-third-party-model)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, Code]

**Output Format:** [Markdown with shell commands, JSON configuration, and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.6.0 (source: server-resolved release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
