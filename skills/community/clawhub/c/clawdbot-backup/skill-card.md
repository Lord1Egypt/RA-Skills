## Description:

Backup and restore ClawdBot configuration, skills, commands, and settings. Sync across devices, version control with git, automate backups, and migrate to new machines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sebastian-buitrag0](https://clawhub.ai/user/sebastian-buitrag0)

### License/Terms of Use:


## Use Case:

Developers and ClawdBot users use this skill to generate backup, restore, sync, migration, and automation guidance for local ClawdBot configuration and skill files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups and sync targets may contain sensitive agent configuration, settings, MCP configuration, or credentials.

Mitigation: Review the contents of ~/.claude before backing up or syncing, narrow the backup scope, and prefer private encrypted storage.

Risk: Git and cloud sync workflows can accidentally upload private configuration or secrets.

Mitigation: Avoid git add . and unattended git push until exclusions are reviewed and the remote storage policy is confirmed.

Risk: Restore and rsync workflows can overwrite or delete local configuration.

Mitigation: Validate archives before restoring and run rsync with dry-run before using --delete.

Risk: Scheduled backups can repeatedly copy sensitive or unwanted files if the scope is too broad.

Mitigation: Do not schedule recurring jobs until backup paths, exclusions, and retention behavior have been reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sebastian-buitrag0/skills/clawdbot-backup)
- [ClawdBot Docs](https://docs.clawdbot.com)
- [ClawdBot Skills Guide](https://docs.clawdbot.com/skills)
- [ClawdBot MCP Setup](https://docs.clawdbot.com/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash snippets and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires git, tar, and rsync for the documented backup and sync workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
