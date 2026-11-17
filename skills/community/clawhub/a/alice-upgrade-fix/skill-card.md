## Description:

OpenClaw Upgrade Fix helps maintain OpenClaw 2026.4.x by backing up configuration, upgrading OpenClaw, checking permissions, and repairing common post-upgrade issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoyoyosan](https://clawhub.ai/user/yoyoyosan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to upgrade OpenClaw 2026.4.x, preserve local configuration backups, restore expected tool permissions, and diagnose Gateway or plugin-runtime issues after an upgrade.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The upgrade and repair scripts can perform a global OpenClaw npm upgrade, restart the Gateway, delete plugin runtime directories, and edit OpenClaw configuration.

Mitigation: Review the scripts before running them, confirm backups exist, and execute them only in the intended OpenClaw environment.

Risk: The scripts may copy auth, memory, and configuration files into local backups.

Mitigation: Keep backup directories access-controlled and remove stale backups when they are no longer needed.

Risk: The maintenance flow can set tools.profile to full and check for exec and gateway permissions, broadening agent capability.

Mitigation: Use the full tool profile only when maintenance requires it, then recheck and reduce permissions after the upgrade is complete.

## Reference(s):

- [OpenClaw Upgrade Fix on ClawHub](https://clawhub.ai/yoyoyosan/skills/alice-upgrade-fix)
- [yoyoyosan ClawHub profile](https://clawhub.ai/user/yoyoyosan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes maintenance guidance for OpenClaw configuration, backups, plugin runtime directories, Gateway state, and tool permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
