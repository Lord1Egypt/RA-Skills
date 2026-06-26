## Description: <br>
Interact with Slack workspaces - send messages, read channels, manage reactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devxoul](https://clawhub.ai/user/devxoul) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, AI agents, and workspace operators use this skill to read Slack workspace context, send messages, manage reactions, upload files, and generate workspace summaries from a command-line interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill extracts Slack desktop-session credentials and can access all logged-in workspaces with the same authority as the desktop session. <br>
Mitigation: Install only when that access level is acceptable, review the external npm package before use, and avoid granting Full Disk Access unless it is necessary for credential extraction. <br>
Risk: Message deletion, file upload, and broadcast-style actions can affect real Slack workspaces. <br>
Mitigation: Confirm destructive or broad actions before execution, especially delete, upload, and multi-channel message workflows. <br>
Risk: Credentials, memory, and workspace snapshots are stored locally and may contain sensitive workspace context. <br>
Mitigation: Protect local storage, do not store tokens or full message content in memory files, and delete credentials, memory, and snapshots when no longer needed. <br>


## Reference(s): <br>
- [Authentication Guide](references/authentication.md) <br>
- [Common Patterns](references/common-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/devxoul/agent-slack) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands typically return JSON by default, with a pretty output option for selected workflows.] <br>

## Skill Version(s): <br>
1.10.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
