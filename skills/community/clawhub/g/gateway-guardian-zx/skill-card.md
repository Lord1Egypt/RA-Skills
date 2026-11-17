## Description:

OpenClaw Gateway Guardian monitors the local OpenClaw Gateway, restarts it after downtime, backs up configuration, and can switch to a fallback model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangss110](https://clawhub.ai/user/zhangss110)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to supervise a local OpenClaw Gateway, recover from outages, preserve configuration backups, and optionally send Feishu alerts or fail over models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent auto-run behavior through a Windows logon scheduled task.

Mitigation: Install it only on machines where automatic startup monitoring is acceptable, and verify the scheduled task and uninstall steps before deployment.

Risk: The watchdog can automatically kill a local process on the configured Gateway port and restart OpenClaw.

Mitigation: Review the configured port and startup path, avoid elevated privileges, and use the stop flag when automatic recovery should be paused.

Risk: Configuration backup, restore, and optional model failover can rewrite local OpenClaw configuration.

Mitigation: Test backup and restore on a non-critical profile first, keep model failover disabled unless the fallback model is approved, and review backups before restoration.

Risk: Feishu notifications can send operational details or log excerpts outside the local machine.

Mitigation: Leave the webhook unset unless external notifications are approved, and review log content before enabling alerting.

## Reference(s):

- [OpenClaw Gateway Guardian on ClawHub](https://clawhub.ai/zhangss110/skills/gateway-guardian-zx)
- [Publisher profile](https://clawhub.ai/user/zhangss110)
- [Project homepage listed in skill metadata](https://github.com/zhangss110/openclaw-watchdog)
- [Feishu custom bot documentation](https://open.feishu.cn/document/ukTMukTMukTM/uADOwUjLwgDM14CM4ATN)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown instructions with JSON configuration and shell or cmd command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local watchdog behavior through Python and JSON configuration when installed by the user.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
