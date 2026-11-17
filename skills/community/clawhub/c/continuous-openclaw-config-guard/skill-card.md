## Description:

Monitors OpenClaw's openclaw.json configuration file, creates backups, restarts the gateway after changes, and rolls back automatically when message activity is not detected within the configured timeout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cxlhyx](https://clawhub.ai/user/cxlhyx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators who manage OpenClaw gateway configuration use this skill to protect risky openclaw.json edits with automatic backup, restart, validation, and rollback behavior. It is intended for Linux environments where the user can review and adapt the service and script paths before enabling persistence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs as a persistent guard and can restart the OpenClaw gateway and roll back configuration changes.

Mitigation: Review and edit the service file and guard.sh before installation, run under the least-privileged suitable user, and validate paths, account, rollback behavior, and stop logic before enabling boot persistence.

Risk: The security evidence reports undisclosed status messages sent to a hard-coded Matrix room and account.

Mitigation: Remove or disable those message sends unless the notification target is intentional, or replace them with user-controlled notification settings.

Risk: An incorrect SESSION_FILE or installation path can make validation fail and cause unwanted rollbacks.

Mitigation: Set SESSION_FILE, OpenClaw paths, and systemd user values for the actual environment, then test the script manually before running it as a service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cxlhyx/skills/continuous-openclaw-config-guard)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs assume local OpenClaw paths, service user, and session file settings are reviewed and updated before use.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
