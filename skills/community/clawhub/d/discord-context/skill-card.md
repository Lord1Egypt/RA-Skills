## Description: <br>
Syncs and caches per-thread context for Discord Forum channels so agents can poll active threads, list cached context, inspect a thread cache, or link a thread to a memory QMD file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[demitrim](https://clawhub.ai/user/demitrim) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to fetch Discord Forum thread metadata, match active threads to workspace memory notes, and inspect or refresh cached thread context for agent work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Discord bot tokens can grant access to server content if exposed or over-permissioned. <br>
Mitigation: Store DISCORD_TOKEN only in the environment, use a minimally permissioned bot, and avoid hardcoding secrets in scripts or configuration. <br>
Risk: Cached Discord context and workspace memory files may contain sensitive content. <br>
Mitigation: Review generated memory/discord-cache files and source memory notes before sharing or using them in broader agent workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/demitrim/discord-context) <br>
- [Publisher profile](https://clawhub.ai/user/demitrim) <br>
- [Discord Developer Portal](https://discord.com/developers/applications) <br>
- [Discord active threads API](https://discord.com/api/v10/guilds/{guildId}/threads/active) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [CLI text, optional JSON, and local context cache files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and DISCORD_TOKEN; reads and writes under the workspace memory tree.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
