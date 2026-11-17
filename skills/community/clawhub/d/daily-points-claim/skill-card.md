## Description:

每日自动执行多站点积分签到，并帮助配置、检查和排查领取结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[junci003](https://clawhub.ai/user/junci003)

### License/Terms of Use:

MIT-0

## Use Case:

面向希望自动领取每日奖励的用户，帮助配置站点、运行或定时执行签到，并检查和排查领取结果。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Login cleanup may close unrelated programs.

Mitigation: Restrict cleanup to the browser process created by this tool before using that flow.

Risk: Request previews, logs, or shared messages may expose account credentials.

Mitigation: Enter credentials locally, redact secrets from previews, logs, and chat, and protect config.json and browser-profile.

Risk: Disabling certificate verification weakens the security of site connections.

Mitigation: Keep certificate verification enabled and enable only intended sites and schedules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/junci003/skills/daily-points-claim)
- [Configuration guide](artifact/references/config-guide.md)
- [Troubleshooting guide](artifact/references/troubleshooting.md)
- [WorkBuddy](https://www.workbuddy.cn)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Text summaries, JSON]

**Output Format:** [Markdown guidance, shell commands, configuration, and JSON result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-site results; local configuration may contain login credentials.]

## Skill Version(s):

1.1.0 (source: server-resolved ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
