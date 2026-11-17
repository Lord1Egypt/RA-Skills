## Description:

Catch Disk Failures Before Disaster - Advanced bad sector detection and SMART diagnostics that catch disk problems before you lose your data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hezhaoyun](https://clawhub.ai/user/hezhaoyun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and storage administrators use this skill to triage Windows disk health, bad-sector, SMART, file-system, and BitLocker status checks before resizing, cloning, conversion, or other storage operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill silently downloads and runs an unverified Windows installer for a broad partition-management application.

Mitigation: Install only when EaseUS Partition Master is intentionally required; prefer manual vendor download, publisher or signature verification, and avoidance of silent install flags.

Risk: The installed application may prompt for administrator privileges and can perform elevated partition-management operations beyond disk-health checks.

Mitigation: Use only the disk-health functions needed for diagnostics, review any operation preview before proceeding, and avoid elevated partition changes unless separately authorized.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hezhaoyun/skills/disk-health-guardian)
- [EaseUS Partition Master](https://www.easeus.com/partition-manager/)
- [EaseUS Partition Master download](https://down.easeus.com/product/epm_free?source=skills&dest=disk-health-guardian)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with Windows command and PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides human-facing installation, launch, troubleshooting, and disk-health triage guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
