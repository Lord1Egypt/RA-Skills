## Description: <br>
每日财经推送专家版：当用户请求今日财经、财经日报、每日金融推送、设置财经推送或取消财经推送时，生成精简财经摘要、市场情绪指标，并可设置定时推送到飞书。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foxxc](https://clawhub.ai/user/foxxc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to generate concise daily finance digests from selected market-news sources and optionally schedule recurring Feishu delivery. It supports manual finance-news queries and cron-based push setup, preview, and cancellation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A recurring Feishu finance digest could be sent to the wrong channel, account, or local time if the schedule is not checked. <br>
Mitigation: Confirm the Feishu target and UTC-adjusted cron schedule before enabling delivery, then run the documented preview command. <br>
Risk: A scheduled finance digest can continue running after the user no longer wants it. <br>
Mitigation: Keep the documented cron removal command available and use it to stop the recurring push. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise finance digest text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Digest output is intended to be concise for Feishu reading, with scheduled delivery controlled through OpenClaw cron commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
