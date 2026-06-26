## Description: <br>
Interact with Discord servers - send messages, read channels, manage reactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devxoul](https://clawhub.ai/user/devxoul) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to inspect Discord server state, read messages, post updates, manage reactions, upload files, and work with channel, server, user, DM, mention, friend, note, profile, member, and thread commands from a CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can extract and store a Discord user session token and then allow an agent to act broadly as that account. <br>
Mitigation: Install only when that access is acceptable; prefer a scoped Discord bot or a separate low-privilege account where possible. <br>
Risk: Agent-driven posting, deleting, uploading, acknowledging, monitoring, or exporting can affect Discord content and account activity. <br>
Mitigation: Require explicit user confirmation before those actions and review the target server, channel, message, file, and user IDs before execution. <br>
Risk: Credential, memory, and snapshot files may contain sensitive Discord access details or workspace context. <br>
Mitigation: Protect these files, keep credential files private, avoid storing tokens in memory, and delete credential, memory, and snapshot files when they are no longer needed. <br>


## Reference(s): <br>
- [Agent Discord on ClawHub](https://clawhub.ai/devxoul/agent-discord) <br>
- [devxoul publisher profile](https://clawhub.ai/user/devxoul) <br>
- [Authentication Guide](references/authentication.md) <br>
- [Common Patterns](references/common-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Discord Snowflake IDs for channels, messages, users, servers, and threads; CLI output is JSON by default with optional pretty formatting.] <br>

## Skill Version(s): <br>
1.10.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
