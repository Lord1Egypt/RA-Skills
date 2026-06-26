## Description: <br>
Agent Slackbot lets agents interact with Slack workspaces using bot tokens to send messages, read channels, and manage reactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devxoul](https://clawhub.ai/user/devxoul) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agent builders use this skill to connect an agent to Slack through a bot token for channel reads, message posting, reactions, and workflow notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad Slack read and write access, including access to private-channel metadata or user email data when those scopes are granted. <br>
Mitigation: Create a dedicated Slack app, grant only the scopes needed for the workflow, and avoid private-channel and user-email scopes unless they are necessary. <br>
Risk: Slack bot tokens may be stored in a local plaintext credential file. <br>
Mitigation: Prefer environment variables or a secret manager for automation, keep local credential files restricted, and clear stored credentials when access is no longer needed. <br>
Risk: Agent-managed memory can persist workspace IDs, channel IDs, user IDs, aliases, and preferences across sessions. <br>
Mitigation: Do not store tokens, full message content, credentials, or file contents in memory, and periodically review or clear the memory file. <br>
Risk: The skill depends on the external agent-messenger package. <br>
Mitigation: Install only if the publisher and external package are trusted for the Slack workspace where the bot will operate. <br>


## Reference(s): <br>
- [Agent Slackbot on ClawHub](https://clawhub.ai/devxoul/agent-slackbot) <br>
- [Authentication Guide](references/authentication.md) <br>
- [Common Patterns](references/common-patterns.md) <br>
- [Slack Apps](https://api.slack.com/apps) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands, shell templates, and JSON command output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default CLI output is JSON; pretty output and runnable shell templates are also documented.] <br>

## Skill Version(s): <br>
1.10.5 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
