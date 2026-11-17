## Description:

Helps an agent preview and optionally delete multiple messages from a specified Discord channel using a Python purge tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ghjbku](https://clawhub.ai/user/ghjbku)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and Discord server operators use this skill to prepare Discord channel cleanup commands, preview affected messages, and run live deletion only after confirming the target channel and count.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete Discord messages when used with a bot token that has message-management permissions.

Mitigation: Run the active script in dry-run mode first, then confirm the exact channel ID and message count before using --delete or -d.

Risk: Token handling guidance includes token.json, which can expose a Discord bot token if shared or committed.

Mitigation: Prefer DISCORD_TOKEN or a secret manager, and never commit or share token.json.

Risk: The package includes legacy backup files for a no-dry-run version of the deletion tool.

Mitigation: Remove or ignore the backup no-dry-run files and use the active script with dry-run behavior.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run previews and live-delete command variants; no structured machine-readable output is promised.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
