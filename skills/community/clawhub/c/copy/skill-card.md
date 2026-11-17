## Description:

Copy operations reference for file duplication, rsync patterns, copy-on-write behavior, buffer strategies, and cross-platform synchronization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as a command-reference guide for duplicating files, synchronizing directories, planning backups or mirrors, and troubleshooting copy-related errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copy and synchronization examples can overwrite, delete, or move data if adapted with the wrong paths or destructive options.

Mitigation: Review source and destination paths, use dry-run modes where available, and keep recoverable backups before running commands such as rsync --delete, dd, or source-file removal.

Risk: Commands involving sudo or remote SSH targets can affect privileged files or systems outside the local workspace.

Mitigation: Confirm the target host, account, permissions, and command flags before execution, and prefer least-privilege access.

## Reference(s):

- [Copy skill on ClawHub](https://clawhub.ai/bytesagain-lab/skills/copy)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command-reference output; review generated copy or sync commands before execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
