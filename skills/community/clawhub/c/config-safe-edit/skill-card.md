## Description:

Safe configuration file editing workflow. Before modifying openclaw.json, models.json, or any system config file, activate this skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucy6692](https://clawhub.ai/user/lucy6692)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when changing configuration files that affect application startup, credentials, ports, channels, or security settings. It guides the agent to scope the requested change, back up the file, edit precisely, inspect the diff, and recover from mistakes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups of credential-bearing configuration files can expose secrets or remain available longer than intended.

Mitigation: Store backups with restrictive permissions outside synced or indexed locations, and delete or rotate sensitive backups after the recovery window.

Risk: A startup-critical configuration edit can leave a system unable to restart or behaving unexpectedly.

Mitigation: Scope exact key paths before editing, keep a dated snapshot for high-risk changes, validate JSON, and verify the diff before restart.

Risk: Using inconsistent backup filenames or diff targets can make recovery unreliable.

Mitigation: Use one exact backup path throughout each edit and confirm the diff compares that backup with the edited file.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell and PowerShell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on reversible configuration edits, backup checks, diffs, JSON validation, and recovery steps.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
