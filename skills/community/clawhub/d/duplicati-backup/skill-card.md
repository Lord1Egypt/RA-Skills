## Description:

Undo for agents. Take an encrypted offsite checkpoint with Duplicati before risky changes, and restore files from any earlier point in time. Use before bulk edits, deletes, migrations, upgrades, or when the user asks to back up, undo, roll back, or recover files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duplicati](https://clawhub.ai/user/duplicati)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents and their operators use this skill to create encrypted, versioned Duplicati checkpoints before risky file changes, then find and restore files when rollback or recovery is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access tokens or backup passphrases could be exposed, or the configured backup scope may include files beyond those needed.

Mitigation: Keep credentials private, review the token permissions and backup scope before setup, and limit the token to the required backup.

Risk: Restoring files in place can overwrite current versions.

Mitigation: Review the selected files and restore target, and obtain confirmation before overwriting unless the user explicitly requested that undo.

## Reference(s):

- [Duplicati MCP documentation](https://docs.duplicati.com/automation-and-integration/using-duplicati-with-ai-agents-mcp)
- [OpenClaw setup instructions](references/openclaw.md)
- [ClawHub release](https://clawhub.ai/duplicati/skills/duplicati-backup)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown instructions with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
