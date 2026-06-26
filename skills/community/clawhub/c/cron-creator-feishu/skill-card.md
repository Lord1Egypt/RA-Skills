## Description: <br>
【针对飞书优化】定时任务创建指引，专门针对飞书、尤其是多 Agent 场景进行优化，解决定时任务不稳定问题。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jhc888007](https://clawhub.ai/user/jhc888007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to turn natural-language reminder requests into OpenClaw cron creation commands. It is optimized for Feishu private chats, group chats, and multi-Agent deployments where timezone, account, and recipient routing need to be explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A reminder may run at the wrong time if timezone assumptions are wrong. <br>
Mitigation: Confirm the resolved timezone and recurrence before relying on the scheduled job, and specify a timezone explicitly when not operating in Asia/Shanghai. <br>
Risk: A reminder may be sent to the wrong Feishu user, chat, or Agent account if routing context is incomplete. <br>
Mitigation: Confirm the recipient or chat ID, account, message, and delivery channel before creating each scheduled job. <br>
Risk: A generated cron command may not match the user's intended schedule or message. <br>
Mitigation: Review the proposed OpenClaw command and list the current cron configuration after creation to verify time, channel, timezone, and message. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jhc888007/cron-creator-feishu) <br>
- [OpenClaw cron troubleshooting guide](https://mp.weixin.qq.com/s/iQtW-SKRcvngzbpJXMSSxg) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces OpenClaw cron command guidance that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
