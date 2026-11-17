## Description:

Recover corrupted exFAT USB drives on Windows without formatting, including diagnosis of boot region corruption, repair with chkdsk or TestDisk, and prevention with write cache fixes, shutdown flush scripts, and automated boot region backups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, sysadmins, and Windows users use this skill to diagnose exFAT USB drives that Windows reports as needing formatting, attempt recovery without formatting, and apply prevention steps for future corruption.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recovery instructions include high-impact raw disk writes that can damage data if the wrong disk, offset, filesystem, or backup file is used.

Mitigation: Create a full disk image first, independently verify the drive number, serial/model, partition offset, filesystem type, and backup size, and avoid writing to the disk until those checks pass.

Risk: Prevention steps include persistent SYSTEM-level Windows automation through a scheduled task or shutdown hook.

Mitigation: Use an administrator-protected script location, document removal steps, and review the persistence mechanism before installing it.

## Reference(s):

- [Prevention Scripts Setup](references/prevention-scripts.md)
- [TestDisk](https://www.cgsecurity.org/wiki/TestDisk)
- [ClawHub skill page](https://clawhub.ai/solomonneas/skills/exfat-recovery)
- [Publisher profile](https://clawhub.ai/user/solomonneas)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Windows administrative recovery and prevention steps that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
