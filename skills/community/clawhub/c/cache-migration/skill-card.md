## Description:

Helps agents guide Windows users through moving developer tool cache, plugin, and data directories to another drive using NTFS Junctions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunliangzesmile](https://clawhub.ai/user/sunliangzesmile)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and power users use this skill to identify large Windows application cache or data directories, migrate them to a specified destination, and verify Junction-based redirection after migration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Migration scripts can delete source directories and create persistent NTFS Junctions.

Mitigation: Run only after confirming exact source and destination paths, closing affected applications, and making a backup or restore point.

Risk: VS Code migration can modify launcher scripts and settings.

Mitigation: Avoid launcher-editing options with untrusted or unusual destination strings, and prefer app-supported cache or extension path settings when available.

Risk: Running PowerShell with elevated privileges increases impact if paths are wrong.

Mitigation: Avoid administrator PowerShell unless required and review all generated commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunliangzesmile/skills/cache-migration)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with PowerShell and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets Windows 10/11 NTFS Junction workflows and requires user-supplied source and destination paths.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
