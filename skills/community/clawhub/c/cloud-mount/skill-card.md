## Description:

Cloud Mount helps an agent guide users through mounting rclone-supported cloud storage, such as OneDrive or Google Drive, as local filesystem paths with status checks and optional autostart.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liqiuyue9597](https://clawhub.ai/user/liqiuyue9597)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and technical users use this skill to configure rclone remotes, mount cloud storage locally, check mount health, and set up user-level autostart behavior. It is suited for personal file access, development backups, server operations, and cloud-backed content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autostart and service-management guidance can affect host startup behavior or prompt users to run elevated commands.

Mitigation: Review the autostart script before enabling it, prefer the documented systemd user service path, and avoid running the autostart script with sudo unless it has been audited and adapted as a system service.

Risk: The rclone configuration file can contain cloud-storage tokens and other sensitive credentials.

Mitigation: Protect ~/.config/rclone/rclone.conf with restrictive permissions, exclude it from backups and repositories, and use dedicated cloud-storage accounts with least-privilege access where possible.

Risk: Broad scheduled backup examples for /etc and /home can copy secrets or delete cloud-side data when synchronization flags are misused.

Mitigation: Replace broad backup paths with explicit allowlists, add exclusions for secrets, test with dry-runs, use encryption where appropriate, and verify the mounted destination before scheduled writes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liqiuyue9597/skills/cloud-mount)
- [ClawHub publisher profile](https://clawhub.ai/user/liqiuyue9597)
- [rclone documentation](https://rclone.org/docs/)
- [rclone downloads](https://rclone.org/downloads/)
- [Artifact skill guide](artifact/SKILL.md)
- [Artifact README](artifact/README.md)
- [Artifact publish log](artifact/PUBLISH_LOG.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill proposes local shell commands and configuration changes for rclone mounts, systemd user services, and mount-health checks.]

## Skill Version(s):

1.5.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
