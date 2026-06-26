## Description: <br>
Interact with Discord servers using bot tokens - send messages, read channels, manage reactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devxoul](https://clawhub.ai/user/devxoul) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI agents use this skill to operate a Discord bot from command-line workflows, including posting messages, reading channels, managing reactions, uploading files, and summarizing server state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read from or post to Discord servers where the configured bot has access. <br>
Mitigation: Use a dedicated bot with the minimum required Discord permissions and verify channel IDs before posting, reading, or uploading files. <br>
Risk: Bot credentials are stored locally and grant bot-level access to authorized servers. <br>
Mitigation: Keep the credential file protected, periodically clear stored credentials when no longer needed, and avoid storing tokens in agent memory or shared logs. <br>
Risk: Broad server snapshots and retained memory can expose more server, channel, user, or message context than needed. <br>
Mitigation: Avoid broad snapshots unless necessary and clear ~/.config/agent-messenger/MEMORY.md when stored server context is no longer needed. <br>


## Reference(s): <br>
- [Authentication Guide](references/authentication.md) <br>
- [Common Patterns](references/common-patterns.md) <br>
- [Discord Developer Portal](https://discord.com/developers/applications) <br>
- [jq Download](https://jqlang.github.io/jq/download/) <br>
- [ClawHub Skill Page](https://clawhub.ai/devxoul/agent-discordbot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands, JSON examples, and reusable shell templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces CLI-oriented guidance for Discord bot authentication, message operations, channel and server inspection, reactions, files, threads, snapshots, and troubleshooting.] <br>

## Skill Version(s): <br>
1.10.5 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
