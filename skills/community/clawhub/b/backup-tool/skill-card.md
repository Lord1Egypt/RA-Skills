## Description:

Backup Tool helps agents create, inspect, and restore compressed tar archives for file backups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users can use this skill when an agent needs to create compressed file backups, list archive contents, or restore trusted backup archives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release claims encryption, exclusions, incremental backup, and integrity protections that are not implemented as published.

Mitigation: Treat generated archives as plaintext compressed tar files, do not depend on --exclude or incremental behavior, and verify required protections before using the skill for sensitive backups.

Risk: Restoring a crafted or untrusted archive can write outside the chosen destination.

Mitigation: Only restore archives from trusted sources after inspecting their contents, and avoid unattended restores until archive extraction is hardened.

Risk: Broad scheduled backups, such as backing up /home, can capture sensitive files without the documented protections.

Mitigation: Use narrowly scoped source directories, manually confirm archive contents, and avoid unattended broad backups for sensitive systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/backup-tool)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference generated backup archives, restore destinations, compression options, and security cautions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
