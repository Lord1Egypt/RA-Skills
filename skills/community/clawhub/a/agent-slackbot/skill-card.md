## Description:

Interact with Slack workspaces using bot tokens - send messages, read channels, manage reactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devxoul](https://clawhub.ai/user/devxoul)

### License/Terms of Use:


## Use Case:

Agents and developers use Agent Slackbot to send Slack messages, read channel and user information, manage reactions, and run notification or monitoring workflows with Slack bot tokens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends broad Slack permissions, including private-channel and email-related scopes.

Mitigation: Install only after a Slack administrator reviews the exact scopes; grant least privilege and avoid private-channel or email scopes unless required.

Risk: Slack bot tokens may be stored locally in a plaintext credential file.

Mitigation: Protect the credential file, keep it out of backups and shared environments, and prefer environment variables for automated environments when appropriate.

Risk: Cross-session memory may retain stale or incorrect workspace, channel, user, or bot aliases.

Mitigation: Periodically review or clear the memory file, avoid storing tokens or message contents, and verify IDs before sensitive actions.

## Reference(s):

- [Agent Slackbot ClawHub release](https://clawhub.ai/devxoul/skills/agent-slackbot)
- [Authentication Guide](references/authentication.md)
- [Common Patterns](references/common-patterns.md)
- [Slack App Configuration](https://api.slack.com/apps)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON command output examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent CLI commands output JSON by default, with optional pretty human-readable output.]

## Skill Version(s):

1.10.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
