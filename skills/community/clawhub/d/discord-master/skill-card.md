## Description:

Discord中心 helps agents work with Discord Bot API workflows for interactions, commands, messages, operations automation, multi-channel sending, and delivery callbacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to automate Discord bot tasks such as sending messages, responding to interactions, executing commands, using message templates, and tracking delivery status. It is not intended for complex decisions that require human judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags broad host-level read, command execution, and file-writing capabilities for Discord-related work.

Mitigation: Run the skill in a constrained workspace and require explicit confirmation before it sends messages, runs commands, or changes files.

Risk: Discord or API credentials could be exposed or over-permissioned.

Mitigation: Use environment variables or a secret manager, avoid committing secrets, and prefer narrowly scoped Discord tokens.

Risk: Bulk messaging, templates, and delivery callbacks can create unintended message volume or disclosure.

Mitigation: Review message targets and content before sending, apply rate limits, and avoid including sensitive information in message templates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/discord-master)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include execution logs, message receipts, status metadata, and API key configuration guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
