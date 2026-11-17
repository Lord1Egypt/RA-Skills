## Description:

OS-level watchdog that monitors OpenClaw gateway health and auto-restarts on crash, then triggers session recovery so interrupted work can resume automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[russellfei](https://clawhub.ai/user/russellfei)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to add watchdog monitoring, automatic restart, and recovery signaling for OpenClaw gateway deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer creates persistent user-level scheduled execution for the gateway health check.

Mitigation: Review the exact crontab entry before enabling the skill and use the uninstall script to remove the scheduled job when it is no longer needed.

Risk: Unsafe cron or path handling can run an unintended script when installed from an unsuitable location.

Mitigation: Install only from a trusted, simple path and verify that the scheduled command points to the expected check-gateway.sh file.

Risk: The installer may modify HEARTBEAT.md and the watchdog writes gateway recovery status under the OpenClaw workspace logs.

Mitigation: Expect these file changes during installation and recovery; manually remove the HEARTBEAT.md recovery section if the behavior is no longer desired.

## Reference(s):

- [Gateway Keeper ClawHub Page](https://clawhub.ai/russellfei/skills/gateway-keeper)
- [russellfei ClawHub Publisher Profile](https://clawhub.ai/user/russellfei)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON recovery examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Installs or removes a user-level scheduled health check and writes gateway recovery status when restart succeeds.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
