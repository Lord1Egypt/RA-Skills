## Description:

Interact with Slack workspaces - send messages, read channels, manage reactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devxoul](https://clawhub.ai/user/devxoul)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to inspect Slack workspace state, send messages, manage reactions, upload files, and automate common Slack workflows from command-line interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically extract Slack desktop session credentials and store tokens locally in plaintext.

Mitigation: Install only where user-equivalent Slack access is acceptable, protect the local credential file, and avoid using shared, synced, repository, or CI workspaces for credentialed runs.

Risk: The skill can read broad workspace state and generate snapshots or summaries that may include sensitive Slack content.

Mitigation: Run snapshot and export-style templates only in trusted local directories and review generated files before sharing or committing them.

Risk: Some template install guidance names an unsafe or contradictory package.

Mitigation: Use the server-resolved OpenClaw installation metadata: install the node package agent-messenger and use its agent-slack binary.

## Reference(s):

- [Agent Slack ClawHub Page](https://clawhub.ai/devxoul/skills/agent-slack)
- [Authentication Guide](references/authentication.md)
- [Common Patterns](references/common-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may read, write, update, delete, upload, react to, search, and summarize Slack workspace content depending on authenticated workspace permissions.]

## Skill Version(s):

1.10.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
