## Description:

Backs up key OpenClaw configuration files and folders to a timestamped folder on the Desktop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meowlegemy-sudo](https://clawhub.ai/user/meowlegemy-sudo)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to back up OpenClaw configuration, agent definitions, credentials, and cron entries before maintenance, migration, or recovery work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The backup process copies OpenClaw credentials, including API keys, to the Desktop in plaintext.

Mitigation: Use a private restricted backup directory, exclude credentials by default, or encrypt backups that contain secrets.

Risk: The backup may expose sensitive configuration files if the Desktop is synced, shared, or broadly readable.

Mitigation: Review the backup destination before running the script and limit filesystem permissions on generated backup folders.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/meowlegemy-sudo/skills/finn-openclaw-backup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash commands and shell script guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates timestamped backup files under the user's Desktop when the shell script is executed.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
