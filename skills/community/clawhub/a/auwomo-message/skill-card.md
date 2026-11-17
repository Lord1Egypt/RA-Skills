## Description:

Auwomo Message helps agents send Feishu private messages to exact organization members through the auwomo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tyqqj0](https://clawhub.ai/user/tyqqj0)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and agents use this skill to send or preview Feishu private messages to organization members when the recipient is exactly known and enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send real Feishu private messages to organization members.

Mitigation: Use dry-run first and require explicit confirmation of both recipient and message before sending.

Risk: Broad message-related triggers could cause accidental sends.

Mitigation: Activate only when the user clearly asks to message, notify, or remind a specific recipient.

Risk: Shell-style command examples can become unsafe if message text is interpolated into a command string.

Mitigation: Invoke the CLI with structured arguments and keep user-provided message text out of shell interpolation.

## Reference(s):

- [message-send](references/message-send.md)
- [ClawHub release page](https://clawhub.ai/tyqqj0/skills/auwomo-message)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and CLI result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses dry-run previews and exact recipient matching before sending.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
