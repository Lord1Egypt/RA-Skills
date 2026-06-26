## Description: <br>
Operate a Discord message cleanup workflow with an official bot token and Discord HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ginhoor](https://clawhub.ai/user/ginhoor) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Discord server moderators and operators use this skill to preview and execute scoped guild-channel cleanup, including filtered message deletion jobs and channel recreation when channel history can be discarded. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform destructive Discord message deletion and channel deletion flows. <br>
Mitigation: Run a preview first, require the generated confirmation code, review counts and filters manually, and avoid deletion when the scope is uncertain. <br>
Risk: Using a broad or over-privileged Discord bot token can expand the impact of mistakes. <br>
Mitigation: Use a dedicated least-privileged bot restricted to the intended guild and channels, and provide the token through environment or secret tooling. <br>
Risk: Channel nuke mode with original-channel deletion can permanently remove channel history. <br>
Mitigation: Use nuke mode only when preserving channel history is unnecessary, and avoid --delete-old unless the operator has explicitly accepted that loss. <br>


## Reference(s): <br>
- [Discord Cleanup Limits](references/discord-limits.md) <br>
- [Discord API v10](https://discord.com/api/v10) <br>
- [ClawHub Skill Page](https://clawhub.ai/ginhoor/discord-purge-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON run summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write preview, state, and result JSON files for audit-friendly cleanup runs.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
