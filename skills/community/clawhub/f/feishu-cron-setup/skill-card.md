## Description:

设置飞书定时任务投递，确保 cron 任务能稳定地将结果发送到飞书。

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicccmy](https://clawhub.ai/user/nicccmy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create, repair, and troubleshoot OpenClaw cron jobs that deliver scheduled task results to Feishu channels or users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Troubleshooting commands that read OpenClaw configuration may expose private account or delivery configuration in logs, chats, or agent context.

Mitigation: Use a structured query that returns only Feishu account names, avoid pasting configuration contents into shared systems, and review command output before sharing.

Risk: Incorrect cron delivery parameters can cause scheduled jobs to report success while Feishu delivery still fails.

Mitigation: Require an explicit Feishu account, channel, recipient, and delivery verification step before treating a scheduled task as fully working.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nicccmy/skills/feishu-cron-setup)
- [Publisher profile](https://clawhub.ai/user/nicccmy)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and troubleshooting tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OpenClaw cron command templates, Feishu delivery parameters, and verification checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
