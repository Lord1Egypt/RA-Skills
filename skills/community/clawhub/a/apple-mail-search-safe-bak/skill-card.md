## Description:

Apple Mail search on macOS with fast metadata lookup and full body access for finding, opening, and reading local Mail.app messages by subject, sender, recipient, date, or unread status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hellohushuai](https://clawhub.ai/user/hellohushuai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users on macOS use this skill to search local Apple Mail messages, inspect metadata, open matching messages, and retrieve full email bodies when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose Apple Mail search results and full message bodies to the agent.

Mitigation: Use narrow queries, request body text only when needed, and avoid running the skill in contexts where sensitive email content should not be shared.

Risk: The skill depends on an external npm CLI installed as fruitmail.

Mitigation: Verify or pin the apple-mail-search-cli package before installation and install it only in trusted environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hellohushuai/skills/apple-mail-search-safe-bak)
- [Publisher profile](https://clawhub.ai/user/hellohushuai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and plain text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or request JSON output from the fruitmail CLI when the skill uses JSON-capable commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
