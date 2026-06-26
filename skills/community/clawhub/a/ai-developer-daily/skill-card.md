## Description: <br>
AI开发者日报每天整理国际和中国 AI/开发者新闻，国际新闻在前、中国新闻在后，支持编号回复展开详情，并可自动定时推送或由用户主动触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[homer212416](https://clawhub.ai/user/homer212416) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to receive a daily AI and developer news digest, either on a scheduled 08:00 Asia/Shanghai cron delivery or on demand. Users can reply with an item number to request a short deeper brief for a specific story. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create an ongoing scheduled message job and may automatically select the delivery channel or recipient. <br>
Mitigation: Before setup, require the agent to show the schedule, timezone, channel, recipient, and full cron command, then confirm how to list, disable, or remove the cron job. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/homer212416/ai-developer-daily) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown news digest with links, optional short follow-up briefs, and inline shell commands for cron setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and may configure an OpenClaw cron job for scheduled delivery.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
