## Description:

CloudPlus helps agents operate the CloudPlus enterprise messaging app to send messages or files, search users, group chats, files, messages, and light apps, retrieve chat history or collected content, open links or apps, and launch the desktop client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billyang1222](https://clawhub.ai/user/billyang1222)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, administrators, and support agents use this skill to act through a CloudPlus enterprise account for chat, file, contact, group, app, and history workflows from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A global npm install can add a persistent executable to the user's environment.

Mitigation: Review and trust the cloudplus-mcp-server package before installation, and avoid installing it in unmanaged or sensitive environments.

Risk: The skill can send messages and files, open links or apps, and retrieve chat history or collected content through a CloudPlus account.

Mitigation: Require explicit user confirmation before sends, file transfers, link or app opens, and sensitive data retrieval.

## Reference(s):

- [CloudPlus Skill on ClawHub](https://clawhub.ai/billyang1222/skills/cloudplus)
- [Node.js](https://nodejs.org)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with bash command examples and JSON command output conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require Node.js, npm, and the mcp-cloudplus CLI; command results should be summarized in natural language rather than shown as raw JSON.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
