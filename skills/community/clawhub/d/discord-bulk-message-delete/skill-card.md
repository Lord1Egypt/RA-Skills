## Description: <br>
Guides an agent through previewing and deleting multiple messages from a Discord channel using a Python Discord purge script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ghjbku](https://clawhub.ai/user/ghjbku) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they need an agent to help preview and purge recent messages from a specific Discord channel. It is intended for channel cleanup workflows that require an explicit channel ID, message count, and user confirmation before live deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead to destructive Discord message deletion if a channel ID, message count, or live deletion flag is wrong. <br>
Mitigation: Require a dry-run or preview first, then confirm the exact channel ID and message count before using --delete or -d. <br>
Risk: Broad Discord moderation permissions could allow deletion in channels where cleanup is not acceptable. <br>
Mitigation: Restrict the bot to the exact server and channels where deletion is approved, and avoid production or audit-sensitive channels unless explicitly authorized. <br>
Risk: The artifact includes a backup no-dry-run command path that can bypass the safer preview-first workflow. <br>
Mitigation: Use the dry-run-capable script path for normal operation and review any no-dry-run backup path before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ghjbku/discord-bulk-message-delete) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may run in dry-run preview mode or live deletion mode depending on flags and user confirmation.] <br>

## Skill Version(s): <br>
1.0.5 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
