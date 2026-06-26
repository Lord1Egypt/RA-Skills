## Description: <br>
Interact with Microsoft Teams - send messages, read channels, manage reactions <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devxoul](https://clawhub.ai/user/devxoul) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and AI agents use this skill to inspect Microsoft Teams state, list teams and channels, send or delete messages, manage reactions, upload and list files, and summarize recent team activity through the agent-teams CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use the signed-in Microsoft Teams desktop session token and act in Teams as the user. <br>
Mitigation: Install and run it only on a trusted machine and only when the user is comfortable granting access through the active Teams desktop session. <br>
Risk: Message, delete, upload, broadcast, monitoring, and snapshot commands can affect Teams content or expose workspace information. <br>
Mitigation: Require explicit user approval before running commands that send, delete, upload, broadcast, monitor, or snapshot Teams data. <br>
Risk: Stored credentials and agent memory may persist after the task is complete. <br>
Mitigation: Periodically clear stored credentials and MEMORY.md when they are no longer needed, and never store tokens, credentials, full message content, or file contents in memory. <br>
Risk: The executable comes from the agent-messenger package declared in ClawHub install metadata. <br>
Mitigation: Verify the agent-messenger package source before installation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/devxoul/agent-teams) <br>
- [Authentication Guide](references/authentication.md) <br>
- [Common Patterns](references/common-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are intended for the agent-teams CLI and may read or act in Microsoft Teams as the signed-in user.] <br>

## Skill Version(s): <br>
1.10.5 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
