## Description:

Provides OpenClaw configuration protection guidance and installer scripts that back up JSON configuration files, validate changes, and roll back when invalid configuration or gateway health failures are detected.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexduming](https://clawhub.ai/user/alexduming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to add rollback-oriented safeguards around AI-assisted configuration changes. It is intended for environments where invalid JSON or bad configuration values can prevent the OpenClaw gateway from starting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports persistent background changes and rollback behavior with unsafe uninstall and incomplete platform support.

Mitigation: Review the package carefully before installation, require explicit consent before enabling background jobs, and confirm the platform-specific installer assets are complete.

Risk: The security review reports unsafe uninstall behavior for scheduled background jobs.

Mitigation: Remove only this skill's own cron or scheduled-task entries during uninstall and preserve unrelated user jobs.

Risk: The security review calls out backup permission and rollback precision concerns.

Mitigation: Protect backup file permissions and verify rollback targets before restoring configuration files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexduming/skills/config-modification-safety)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with shell command snippets and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes platform-specific installation and rollback commands for macOS and Windows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
